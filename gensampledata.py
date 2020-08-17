import time
import shutil, os
import datetime
import sys
from faker import Faker

import rando as r
import datatypes as dt
import settings as s
import datatypemap as dtm
import s3client
import datawriter
import tracer
import archival


def GenData():

	if not os.path.exists("counters"):
		os.makedirs("counters")

	r.RegenDates()

	print("iterations: %s, duperate: %s, variance: %s" % (s.ITERATE, (str(s.OVERALL_DUPE_RATE)+"%"), str(s.VARIANCE_DUPE_RATE))+"%")		

	overall_start_time = time.time()	
	currentIter = round(s.ITERATE / s.LOOPER) * s.LOOPER 
	
	# BEGIN main bulk of work calling into datatypes.py

	# our use of pandas combined with fuzzy function lookups is
	# exponentially expensive as our desired row count goes up
	# so we loop through the generation, keeping each loop to 1000 records

	# if truncate, we delete any files with today's date, this needs work but it's ok for now
	
	# lastly, if "-transonly" in sys.argv then we skip all of this work 
	# and instead generate a transactions file for the eCommerce customers (from archive)
	# this is for generating a near-real-time ingest of only transactions into an amp tenant

	if "-transactionsonly" in sys.argv:
		print("only generating transactions from existing customers")
		archival.archivalTransactionsOnly()
		datawriter.TransactionIDWriter()

	else:

		if s.LOAD_TYPE == "truncate":
			for root, dirs, files in os.walk(s.outputdir):
				for f in files:
					if f.startswith(s.today):
						os.unlink(os.path.join(root, f))

		s.ITERNUM = 1
		for i in range(int(currentIter / s.LOOPER)):

			if s.SHOW_TIMER:
				loop_start_time = time.time()
			
			#PopulatePrimaryCustomers takes a file name fragment as its argument
			primaryCustomers = dt.PopulatePrimaryCustomers(s.primaryfilenamefragment)
			
			# Take Batch-minus-duperate to use for some of our other data source types
			smallerPrimaryCustomers = primaryCustomers.sample(n=s.LOOPER - (int( s.LOOPER * (dt.dupeRate/100))))
			
			if s.CREATE_DS_SECONDARY:

				for index, item in enumerate(dtm.secondaryCustomerColumns):
					#intent here is to create a secondary system of customers, and some of those 
					#should also end up in the LMS system or other systems
					#PopulateSecondaryCustomers takes a file name fragment as its argument, e.g. "Pos"
					secondaryCustomers = dt.PopulateSecondaryCustomers(index, primaryCustomers, "Pos")
					secondaryCustomers = secondaryCustomers.sample(n=s.LOOPER - (int( s.LOOPER * (dt.dupeRate/100))))

				del secondaryCustomers

			if s.CREATE_DS_LOYALTY:
				lmsTransactions = dt.populateLoyalty(smallerPrimaryCustomers)
				del lmsTransactions

			if s.CREATE_DS_EMAILCAMPAIGN:
				emailCampaignStaging = dt.populateEmailCampaign(smallerPrimaryCustomers)
				del emailCampaignStaging
			if s.CREATE_DS_CLICKSTREAM:
				clickstream = dt.populateClickstream(smallerPrimaryCustomers)
				del clickstream
			if s.CREATE_DS_MOBILE:
				mobile = dt.populateMobile(smallerPrimaryCustomers)
				del mobile
			if s.CREATE_DS_WIFI:
				wifi = dt.populateWifi(smallerPrimaryCustomers)
				del wifi
			if s.CREATE_SAFETY:
				safety = dt.populateSafetyReportData(smallerPrimaryCustomers)	
				del safety

			if s.CREATE_TILEDATA:
				tiledata = dt.populateTileData(smallerPrimaryCustomers)	
				del tiledata

			if s.CREATE_CUSTOM_OBJECT:
				customObject = dt.populateCustomObject(smallerPrimaryCustomers)	
				del customObject

			# close out our increment ID storage files
			
			datawriter.CustomerIDWriter()
			datawriter.TransactionIDWriter()
			datawriter.EcIDWriter()
			datawriter.ClickstreamIDWriter()
			
			del primaryCustomers, smallerPrimaryCustomers

			s.ITERNUM += 1
			if s.SHOW_TIMER:
				loop_finished_time = time.time() 
				loop_elapsed_time = loop_finished_time - loop_start_time
				print("generated ~ %d records, chunk finished at %s, duration: %f seconds" % ((s.LOOPER*(i+1)), (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(loop_finished_time))), (loop_elapsed_time)))
		
	# END main bulk of work
	
	# Run our tracer program, if file exists
	if s.TRACER_DATA:
		if os.path.isfile(s.tracerdir + '/tracer.csv'):
			print("injecting tracer data...")
			tracer.PopulateTracerCustomers()

	overall_finished_time = time.time() 
	overall_elapsed_time = overall_finished_time - overall_start_time
	print("all chunks finished at %s, duration: %f minutes" % ((time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(overall_finished_time))), (overall_elapsed_time/60)))
	print("total rows created across all files: %d (%d rows per second)" % (datawriter.totalRowsCreated.current(), (datawriter.totalRowsCreated.current() / overall_elapsed_time ) ))


	if s.SEND_TO_S3:
		if s.AMP_S3_PREFIX != '' and s.AMP_S3_BUCKETNAME != '':
			s3client.sendToS3(s.today)
			print('Done sending to S3!')
	else:
		print("send to S3 is set to false")

if __name__ == '__main__':
	GenData()