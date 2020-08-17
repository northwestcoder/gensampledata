import pandas as pd
import string
import sys as sys
import random
import numpy as np
import random
from io import BytesIO, StringIO
from csv import writer 
import time

import rando as r
import settings as s 
import fuzzmap as fuzz
import datawriter
import datatypemap as dtm 
import archival

dupeRate = r.currentDupeRate()

# you may be curious as to why this is a frankensteinian mess
# of a) straight pythonic array work mixed with b) pandas usage
#
# the answer is that it's a crime I was even allowed to do this
# project in the first place
#
# but seriously, the other answer is that pandas
# is very expensive with some of its older codeline, like
# cell by cell or row by row appends
# so instead we constructed our frames using StringIO and writer
# 
# but meanwhile some of the newer pandas codeline around 
# map/reduce and lambda was much faster
#
# and finally, pandas is super convenient for lobbing data frames around
# in functions and also referring to their header names, or using all
# the other pandas goodness that isn't slow af
#
# anyhow that's our reason and we're sticking to it...

#############################
# PopulatePrimaryCustomers is CUSTOMERS #1
# e.g. a starting place from which any second 
# or nth data source is created

def PopulatePrimaryCustomers(filename: str) -> pd.DataFrame():

	output = StringIO()
	csv_writer = writer(output)

	columnData = dtm.primaryCustomerColumns

	customerStaging = pd.DataFrame(columns=columnData)
	customerStaging.astype(str)
	corruptCustomerStaging = pd.DataFrame(columns=columnData)
	corruptCustomerStaging.astype(str)

	# Step One: create some brand new customers

	listOfNewRows = []
	for newrow in range(s.LOOPER):
		#our temp row array for append
		newrow = []
		if s.USE_ALPHA_KEY:
			newrow.append(str(datawriter.nextCustomerID()) + "-" + r.id_generator())
		else:
			newrow.append(datawriter.nextCustomerID())
		tempEmployer = random.choice(r.staticdata.companies())
		# some squirrel to create gender based names
		if r.randomlySelected(6, 11):  # construct female name slightly more often (54% of the time)
			tempFirstName = random.choice(r.staticdata.firstnames_female())
			tempLastName = random.choice(r.staticdata.lastnames())
			newrow.append(random.choice(r.staticdata.prefix_female()))
			newrow.append(tempFirstName)
			newrow.append(tempLastName)
			newrow.append("F")
		else:
			tempFirstName = random.choice(r.staticdata.firstnames_male())
			tempLastName = random.choice(r.staticdata.lastnames())
			newrow.append(random.choice(r.staticdata.prefix_male()))
			newrow.append(tempFirstName)
			newrow.append(tempLastName)
			newrow.append("M")
		tempEmail = r.genEmail(tempFirstName, tempLastName, tempEmployer)
		newrow.append(tempEmail)
		newrow.append(random.choice(r.typeAccountStatus))
		newrow.append(str(random.randint(100,9999)) + " " + random.choice(r.staticdata.streetnames()))
		
		# starting in June 2019, we decided to get real cities and states
		# as the risk of accidentally generating a real human is pretty low... 
		tempCityStateCombo = random.choice(r.staticdata.city_state_combos()).split(',')
		whichStateType = np.random.randint(2)
		newrow.append(tempCityStateCombo[0])
		newrow.append(tempCityStateCombo[whichStateType+1])
		newrow.append(random.choice(r.staticdata.postalcodes()))
		newrow.append(random.choice(r.staticdata.birthdates()))
		newrow.append(tempEmployer)
		newrow.append(random.choice(r.staticdata.jobs()))
		newrow.append(random.choice(r.staticdata.phones()))
		newrow.append(s.dtUpdateDate)
		listOfNewRows.append(newrow)

	csv_writer.writerows(listOfNewRows)

	output.seek(0) # we need to get back to the start of the BytesIO
	customerStaging = pd.read_csv(output, names=columnData)

	# Step Two: copy *some* customers using dupeRate into new frame for fuzzing

	frameForCorruptCustomerStaging = customerStaging.sample(frac=(dupeRate/100))
	frameForCorruptCustomerStaging.astype(str)

	# next two lines is the magic moment where we use a map to all our fuzzing code in fuzzmap.py
	for column in frameForCorruptCustomerStaging.columns[0:]:
		frameForCorruptCustomerStaging[column] = frameForCorruptCustomerStaging[column].map(lambda cellvalue: fuzz.fuzzMap(column, str(cellvalue)))

	# Step three: attempt to get some customers from an existing csv file, 
	# re-add them as net new customers with new PK's and fuzz them
	
	archivedCustomers = pd.DataFrame(columns=columnData)
	
	if s.USE_ARCHIVAL:
		i = 0
		while i < s.ARCHIVAL_COUNT: 
			#print('adding archived customers ' + str(i))
			tempdf = archival.archivalCustomerReader()
			archivedCustomers = archivedCustomers.append(tempdf)
			i += 1
	
	# Step Four: copy all three frames into one final frame 

	if s.USE_ARCHIVAL:
		finalFrame = pd.concat([customerStaging,frameForCorruptCustomerStaging,archivedCustomers])
	else:
		finalFrame = pd.concat([customerStaging,frameForCorruptCustomerStaging])

	
	if s.CREATE_PRIMARY_TRANSACTIONS:
		populateTransactions(finalFrame, filename+'Transactions')

	if s.CREATE_PRIMARY_CUSTOMERS:
		datawriter.amp_filewriter(finalFrame, filename)

	# after all of the above, return the non-corrupted dataframe for use downstream (mobile data, LMS, clickstream, etc)
	
	return customerStaging


#############################
# CUSTOMERS Secondary - e.g. a second POS or other data source 

def PopulateSecondaryCustomers(columnNames: int, incoming_DF: pd.DataFrame, filename: str):

	output = StringIO()
	csv_writer = writer(output)

	columnData = dtm.secondaryCustomerColumns[columnNames]

	# 1. Take the incoming frame from our primary customers and sample based on dupe rate
	incoming_DF = incoming_DF.sample(n=int( s.LOOPER * (dupeRate/100) ) )


	# 2. also create a new secondary group of customers, original size minus dupe rate
	# 3. and, fuzz a (dupe rate) percentage of these new customers
	secondaryCustomerStaging = pd.DataFrame(columns=columnData)
	corruptSecondaryCustomerStaging = pd.DataFrame(columns=columnData)

	listOfNewRows = []
	
	for _ in range(s.LOOPER - int( s.LOOPER * (dupeRate/100)) ):	
		#our single row array for appending cells
		newrow = []
		newrow.append(datawriter.nextCustomerID())
		tempEmployer = random.choice(r.staticdata.companies())
		# some squirrel to create gender based names
		if r.randomlySelected(6, 11):  # construct female name slightly more often (54% of the time)
			tempFirstName = random.choice(r.staticdata.firstnames_female())
			tempLastName = random.choice(r.staticdata.lastnames())
			newrow.append(random.choice(r.staticdata.prefix_female()))
			newrow.append(tempFirstName)
			newrow.append(tempLastName)
			newrow.append("F")
		else:
			tempFirstName = random.choice(r.staticdata.firstnames_male())
			tempLastName = random.choice(r.staticdata.lastnames())
			newrow.append(random.choice(r.staticdata.prefix_male()))
			newrow.append(tempFirstName)
			newrow.append(tempLastName)
			newrow.append("M")
		tempEmail = r.genEmail(tempFirstName, tempLastName, tempEmployer)
		newrow.append(tempEmail)
		newrow.append(random.choice(r.typeAccountStatus))
		newrow.append(str(random.randint(100,9999)) + " " + random.choice(r.staticdata.streetnames()))
		# starting in June 2019, we decided to get real cities and states
		# as the risk of accidentally generating a real human is pretty low... 
		tempCityStateCombo = random.choice(r.staticdata.city_state_combos()).split(',')
		whichStateType = np.random.randint(2)
		newrow.append(tempCityStateCombo[0])
		newrow.append(tempCityStateCombo[whichStateType+1])
		newrow.append(random.choice(r.staticdata.postalcodes()))
		newrow.append(random.choice(r.staticdata.birthdates()))
		newrow.append(tempEmployer)
		newrow.append(random.choice(r.staticdata.jobs()))
		newrow.append(random.choice(r.staticdata.phones()))
		newrow.append(s.dtUpdateDate)

		listOfNewRows.append(newrow)

	csv_writer.writerows(listOfNewRows)

	output.seek(0) # we need to get back to the start of the BytesIO
	secondaryCustomerStaging = pd.read_csv(output, names=columnData)

	corruptSecondaryCustomerStaging = secondaryCustomerStaging.sample(frac=(dupeRate/100))

	# next two lines is the magic moment where we use a map to all our fuzzing code in fuzzmap.py
	for column in corruptSecondaryCustomerStaging.columns[0:]:
		corruptSecondaryCustomerStaging[column] = corruptSecondaryCustomerStaging[column].map(lambda cellvalue: fuzz.fuzzMap(column, str(cellvalue)))

	# also need/want to fuzz up our inbound copy of customers from the primary source:
	for column in incoming_DF.columns[0:]:
		incoming_DF[column] = incoming_DF[column].map(lambda x: fuzz.fuzzMap(column, x))


	# final frame here is our sampled original customers, a group of new customers, and a group of fuzzed version of the new customers
	finalFrame = pd.concat([incoming_DF, secondaryCustomerStaging,corruptSecondaryCustomerStaging])

	populateTransactions(secondaryCustomerStaging, filename+'Transactions')

	datawriter.amp_filewriter(finalFrame, filename)

	return finalFrame


#############################
# Transactions 

def populateTransactions(DF: pd.DataFrame, filename: string) -> pd.DataFrame():

	output = StringIO()
	csv_writer = writer(output)

	finalFrame = pd.DataFrame(columns=dtm.transColumnData)

	listOfNewRows = []

	for _ in range(len(DF.index)):
		sendID = DF.iloc[_]['customer_id']
		for _ in range(random.randint(1,s.MAX_TRANS_PER_CUSTOMER)):   # for each customer we gen 1-N transactions, change as desired
			newrow = []
			transtotal = random.triangular(100, 2000) # triangular is awesome and creates a nice normal distro of values
			numitems = random.randint(1,15)
			newrow.append(sendID)
			newrow.append(datawriter.nextTransID())
			if s.TRANS_TYPE.lower() == "daily":
				newrow.append(random.choice(r.staticdata.last24hoursdates()))
			else: 
				newrow.append(random.choice(r.staticdata.lastfiveyeardates()))
			newrow.append(round(transtotal,2))
			newrow.append(round(transtotal*(s.POINTS_EARNED/100)))
			newrow.append(numitems)
			newrow.append(round(transtotal / (numitems+.000000001),2))
			prodcode = random.randint(700000000,900000000)
			newrow.append(prodcode)
			newrow.append("PR" + str(prodcode)[:3])
			storeorwebcode = random.randint(100,300)
			newrow.append(storeorwebcode)
			listOfNewRows.append(newrow)

	csv_writer.writerows(listOfNewRows)

	output.seek(0) # we need to get back to the start of the BytesIO
	finalFrame = pd.read_csv(output, names=dtm.transColumnData)

	datawriter.amp_filewriter(finalFrame, filename)
	return finalFrame

#############################
# Loyalty Data

def populateLoyalty(DF: pd.DataFrame) -> pd.DataFrame():

	output = StringIO()
	csv_writer = writer(output)
	
	lmsStaging = pd.DataFrame(columns=dtm.lmsColumns)
	corruptLmsStaging = pd.DataFrame(columns=dtm.lmsColumns)

	lmsStaging.astype(str)
	corruptLmsStaging.astype(str)

	listOfNewRows = []
	for _ in range(len(DF.index)):
		#for each customer, create 1 LMS record
		#todo: for each customer create a pareto of multiple mismatches		
		newrow = []
		sendID = 'LM' + str(DF.iloc[_]['customer_id'])
		newrow.append(sendID)
		newrow.append(DF.iloc[_]['name_first'])
		newrow.append(DF.iloc[_]['name_last'])
		newrow.append(DF.iloc[_]['email'])
		newrow.append(DF.iloc[_]['gender'])
		newrow.append(DF.iloc[_]['addr_ln_1_txt'])
		newrow.append(DF.iloc[_]['city'])
		newrow.append(DF.iloc[_]['state'])
		newrow.append(DF.iloc[_]['postal_code'])
		newrow.append(DF.iloc[_]['birth_dt'])
		newrow.append(random.choice(r.staticdata.lmscreatedates()))
		newrow.append(DF.iloc[_]['phone'])
		newrow.append(round(random.randint(1000,120000) / 1000) * 1000)
		newrow.append(random.choice(r.staticdata.loyaltytiers()))
		newrow.append(random.choice(r.staticdata.loyaltyprograms()))
		newrow.append(s.dtUpdateDate)

		listOfNewRows.append(newrow)

	csv_writer.writerows(listOfNewRows)

	output.seek(0) # we need to get back to the start of the BytesIO
	lmsStaging = pd.read_csv(output, names=dtm.lmsColumns)

	corruptLmsStaging = lmsStaging.sample(frac=(dupeRate/100))
		
	# next two lines is the magic moment where we use a map to all our fuzzing code in fuzzmap.py	
	for column in corruptLmsStaging.columns[1:]:
		corruptLmsStaging[column] = corruptLmsStaging[column].map(lambda cellvalue: fuzz.fuzzMap(column, str(cellvalue)))

	finalFrame = pd.concat([lmsStaging,corruptLmsStaging])

	datawriter.amp_filewriter(finalFrame, "Lms")

	return finalFrame

#############################
# Email Campaign Data

def populateEmailCampaign(DF: pd.DataFrame) -> (pd.DataFrame()):

	output = StringIO()
	csv_writer = writer(output)


	finalFrame = pd.DataFrame(columns=dtm.emailColumns)

	listOfNewRows = []
	for _ in range(len(DF.index)):
		sendEmail = DF.iloc[_]['email']
		sendCustID = DF.iloc[_]['customer_id']
		#for each customer, generate some email campaign data transactions
		for _ in range(random.randint(1,s.MAX_TRANS_PER_CUSTOMER)): 
			newrow = []
			newrow.append(datawriter.nextEcID())
			newrow.append(random.choice(r.staticdata.emailcampaigns()))
			newrow.append(random.randint(1,3))
			newrow.append(random.randint(10,30))
			newrow.append(sendCustID)
			newrow.append(random.choice(r.staticdata.lastfiveyeardates()))
			newrow.append(random.choice(r.staticdata.lastfiveyeardates()))
			newrow.append(int(round(random.randint(1000,12000) / 100) * 100))
			newrow.append(int(round(random.randint(1000,12000) / 1000) * 1000))
			newrow.append(sendEmail)
			newrow.append(random.choice(r.staticdata.emailCampaignFormats()))
			newrow.append(random.randint(10000,200000) / 100)
			newrow.append(random.choice(r.staticdata.lastfiveyeardates()))
			newrow.append(s.dtUpdateDate)
			listOfNewRows.append(newrow)

	csv_writer.writerows(listOfNewRows)

	output.seek(0) # we need to get back to the start of the BytesIO
	finalFrame = pd.read_csv(output, names=dtm.emailColumns)

	datawriter.amp_filewriter(finalFrame, "EmailCampaign")
		
	return finalFrame

#############################
# Clickstream Data

def populateClickstream(DF: pd.DataFrame) -> pd.DataFrame():

	output = StringIO()
	csv_writer = writer(output)

	finalFrame = pd.DataFrame(columns=dtm.clickstreamColumns)

	listOfNewRows = []
	for _ in range(len(DF.index)):
		sendID = DF.iloc[_]['customer_id']
		sendEmail = DF.iloc[_]['email']
		for _ in range(random.randint(1,2)):   # for each customer we gen 1-2 transactions, change as desired
			newrow = []
			newrow.append(sendID)
			newrow.append("1")
			newrow.append(random.choice(r.staticdata.last24hoursdates()))
			newrow.append(random.choice(r.staticdata.uris()))
			newrow.append("AAM Campaigns")
			newrow.append(random.choice(r.staticdata.ipv6()))
			newrow.append(random.choice(r.staticdata.last24hoursdates()))
			newrow.append(random.choice(r.staticdata.last24hoursdates()))
			newrow.append(random.choice(r.staticdata.uuid4()))
			newrow.append(sendEmail)
			newrow.append(random.choice(r.staticdata.user_agent()))
			newrow.append(random.choice(r.staticdata.uris()))
			prodcode = random.randint(1,999)
			newrow.append("PR" + str(prodcode))
			newrow.append(datawriter.nextClickstreamID())
			newrow.append(s.dtUpdateDate)
			listOfNewRows.append(newrow)

	# now let's create new humans in click stream data that do not exist anywhere else
	# instead of passing in a customer ID we insert "0" which reflects actual Adobe usage :) 
	for _ in range(int(s.LOOPER*(dupeRate/100))):
		newrow = []
		tempEmployer = random.choice(r.staticdata.companies())
		# some squirrel to create gender based names
		if r.randomlySelected(6, 11):  # construct female name slightly more often (54% of the time)
			tempFirstName = random.choice(r.staticdata.firstnames_female())
			tempLastName = random.choice(r.staticdata.lastnames())
		else:
			tempFirstName = random.choice(r.staticdata.firstnames_male())
			tempLastName = random.choice(r.staticdata.lastnames())
		tempEmail = r.genEmail(tempFirstName, tempLastName, tempEmployer)
		newrow.append(datawriter.nextMasterID())
		newrow.append(0)
		newrow.append('1')
		newrow.append(random.choice(r.staticdata.last24hoursdates()))
		newrow.append(random.choice(r.staticdata.uris()))
		newrow.append(random.choice("AAM Campaigns"))
		newrow.append(random.choice(r.staticdata.ipv6()))
		newrow.append(random.choice(r.staticdata.last24hoursdates()))
		newrow.append(random.choice(r.staticdata.last24hoursdates()))
		newrow.append(random.choice(r.staticdata.uuid4()))
		newrow.append(tempEmail)
		newrow.append(random.choice(r.staticdata.user_agent()))
		newrow.append(random.choice(r.staticdata.uris()))
		prodcode = random.randint(1,999)
		newrow.append("PR" + str(prodcode))
		newrow.append(datawriter.nextClickstreamID())
		newrow.append(s.dtUpdateDate)
		listOfNewRows.append(newrow)

	csv_writer.writerows(listOfNewRows)

	output.seek(0) # we need to get back to the start of the BytesIO
	finalFrame = pd.read_csv(output, names=dtm.clickstreamColumns)

	datawriter.amp_filewriter(finalFrame, "Clickstream")
		
	return finalFrame


#############################
# Mobile Data

def populateMobile(DF: pd.DataFrame) -> pd.DataFrame():

	output = StringIO()
	csv_writer = writer(output)

	finalFrame = pd.DataFrame(columns=dtm.mobileColumns)

	listOfNewRows = []
	for _ in range(len(DF.index)):
		sendEmail = DF.iloc[_]['email']
		for _ in range(random.randint(1,2)):   # for each customer we gen 1-2 mobile clicks/transactions, change as desired
			newrow = []
			newrow.append(sendEmail)
			newrow.append(random.randint(1000,9000)/100)
			newrow.append(random.choice(r.staticdata.uris()))
			newrow.append(random.choice(r.staticdata.ipv6()))
			newrow.append(random.choice(r.staticdata.last24hoursdates()))
			newrow.append(random.choice(r.staticdata.sha256()))
			newrow.append(random.choice(r.staticdata.uuid4()))
			newrow.append(s.dtUpdateDate)
			listOfNewRows.append(newrow)

	csv_writer.writerows(listOfNewRows)

	output.seek(0) # we need to get back to the start of the BytesIO
	finalFrame = pd.read_csv(output, names=dtm.mobileColumns)

	datawriter.amp_filewriter(finalFrame, "Mobile")
		
	return finalFrame


#############################
# Wifi Data

def populateWifi(DF: pd.DataFrame) -> pd.DataFrame():

	output = StringIO()
	csv_writer = writer(output)

	finalFrame = pd.DataFrame(columns=dtm.wifiColumns)

	listOfNewRows = []
	for _ in range(len(DF.index)):
		sendEmail = DF.iloc[_]['email']
		sendFirstName = DF.iloc[_]['name_first']
		sendLastName = DF.iloc[_]['name_last']
		sendPostalCode = DF.iloc[_]['postal_code']
		newrow = []
		newrow.append(sendEmail)
		newrow.append(sendFirstName)
		newrow.append(sendLastName)
		newrow.append(random.randint(100,900))
		newrow.append(sendPostalCode)
		newrow.append(random.choice(r.staticdata.ipv6()))
		newrow.append(random.choice(r.staticdata.last24hoursdates()))
		newrow.append(random.choice(r.staticdata.sha256()))
		newrow.append(random.choice(r.staticdata.uuid4()))
		newrow.append(s.dtUpdateDate)
		listOfNewRows.append(newrow)

	csv_writer.writerows(listOfNewRows)

	output.seek(0) # we need to get back to the start of the BytesIO
	wifiFrame = pd.read_csv(output, names=dtm.wifiColumns)

	corruptwifiFrame = wifiFrame.sample(frac=(dupeRate/100))
		
	# next two lines is the magic moment where we use a map to all our fuzzing code in fuzzmap.py		
	for column in corruptwifiFrame.columns[1:]:
		corruptwifiFrame[column] = corruptwifiFrame[column].map(lambda cellvalue: fuzz.fuzzMap(column, str(cellvalue)))

	finalFrame = pd.concat([wifiFrame,corruptwifiFrame])

	datawriter.amp_filewriter(finalFrame, "Wifi")
		
	return finalFrame

#############################
# Safety Reports

def populateSafetyReportData(DF: pd.DataFrame) -> pd.DataFrame():

	output = StringIO()
	csv_writer = writer(output)

	finalFrame = pd.DataFrame(columns=dtm.safetyReportColumns)

	listOfNewRows = []
	for _ in range(len(DF.index)):
		sendID = DF.iloc[_]['customer_id']
		for _ in range(random.randint(1,s.MAX_TRANS_PER_CUSTOMER)):   # for each customer we gen 1-N transactions, change as desired
			newrow = []
			newrow.append(sendID)
			newrow.append(random.choice(r.staticdata.lastfiveyeardates()))
			newrow.append(random.choice(r.injuryReportType))
			newrow.append(random.choice(r.reportPriority))
			newrow.append(random.choice(r.staticdata.injuries()))
			listOfNewRows.append(newrow)

	csv_writer.writerows(listOfNewRows)

	output.seek(0) # we need to get back to the start of the BytesIO
	safetyReportFrame = pd.read_csv(output, names=dtm.safetyReportColumns)


	datawriter.amp_filewriter(safetyReportFrame, "SafetyReports")
		
	return finalFrame



#############################
# Tile Data

def populateTileData(DF: pd.DataFrame) -> pd.DataFrame():

	output = StringIO()
	csv_writer = writer(output)

	finalFrame = pd.DataFrame(columns=dtm.tiledataReportColumns)

	listOfNewRows = []
	for _ in range(len(DF.index)):
		sendID = DF.iloc[_]['customer_id']
		for _ in range(random.randint(1,s.MAX_TRANS_PER_CUSTOMER)):   # for each customer we gen 1-N transactions, change as desired
			newrow = []
			newrow.append(sendID)
			newrow.append(random.choice(r.staticdata.lastfiveyeardates()))
			#newrow.append(random.choice(r.reportPriority))
			newrow.append("Tile")
			newrow.append(random.choice(r.staticdata.latlongs()))
			listOfNewRows.append(newrow)

	csv_writer.writerows(listOfNewRows)

	output.seek(0) # we need to get back to the start of the BytesIO
	tiledataFrame = pd.read_csv(output, names=dtm.tiledataReportColumns)


	datawriter.amp_filewriter(tiledataFrame, "LatLongs")
		
	return finalFrame





#############################
# CUSTOMERS Secondary - e.g. a second POS or other data source 

def populateCustomObject(DF: pd.DataFrame):

	output = StringIO()
	csv_writer = writer(output)

	columnData = ['Email','FirstName','LastName','StreetAddress','City','State','PostalCode','Country']

	finalFrame = pd.DataFrame(columns=columnData)


	listOfNewRows = []	
	for _ in range(len(DF.index)):
		newrow = []
		newrow.append((DF.iloc[_]['customer_id']) + (DF.iloc[_]['email']))
		newrow.append(DF.iloc[_]['name_first'])
		newrow.append(DF.iloc[_]['name_last'])
		newrow.append(DF.iloc[_]['addr_ln_1_txt'])
		newrow.append(DF.iloc[_]['city'])
		newrow.append(DF.iloc[_]['state'])
		newrow.append(DF.iloc[_]['postal_code'])
		newrow.append("USA")
		listOfNewRows.append(newrow)

	csv_writer.writerows(listOfNewRows)

	output.seek(0) # we need to get back to the start of the BytesIO

	# final frame here is our sampled original customers, a group of new customers, and a group of fuzzed version of the new customers
	finalFrame = pd.read_csv(output, names=columnData)

	datawriter.amp_filewriter(finalFrame, "customObject")

	return finalFrame





