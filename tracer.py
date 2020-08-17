# tracer.py
#
# 1. this routine will inject known data into the primary fake data stream.
# 2. meant to be run only once per ingest.
# 3. purpose is to inject known-good QA data for stitch testing
# 4. assumes the data model is the same as the rest of this program (needs work...)
# 5. reads from an arbitrarily specified location 'tracer', indicated below
# 6. appends to existing CSV files using the s.today value

# Note:
# This only uses the one originating customer file e.g. "CustomerseCommerce". It does not attempt
# to create loyalty, mobile, clickstream or transaction data.
# its singular purpose is to create multiple customers for a single data silo, for stitch QA purposes...

import pandas as pd
import datetime
import string
import sys as sys
import os
import settings as s 
import datawriter

# which file are we injecting this tracer data into:
# (this all needs some serious refactoring)
filename = 'eCommerce'

def PopulateTracerCustomers():

	tracerData = pd.read_csv(s.tracerdir+"/tracer.csv")
	tracerData.astype(str)
	tracerData['master_id'] = tracerData['customer_id'].map(lambda cellvalue: '9999999999')
	tracerData['customer_id'] = tracerData['customer_id'].map(lambda cellvalue: datawriter.nextCustomerID())
	tracerData['dtUpdateDate'] = s.dtUpdateDate
	# we dont use the regular file writer and instead hardwire logic here:
	# we always will append this tracer data to our existing file of the same name
	if not os.path.exists(s.outputdir):
		os.makedirs(s.outputdir)

	fname = ''
	fname = s.outputdir + "/" + s.today + s.fileprefix + filename + '.csv'

	with open(fname, 'a') as f:
		tracerData.to_csv(fname, mode='a', header=False, index=False, quoting=1)
		f.close()

	datawriter.CustomerIDWriter()

	# delete our tracer file afterward
	# because it's meant to be a ONE TIME thing...
	for root, dirs, files in os.walk(s.tracerdir):
		for f in files:
			os.unlink(os.path.join(root, f))