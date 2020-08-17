# archival.py has two methods


#1. archivalCustomerReader: attempts to find existing files, read 10% of our
# iterate loop, and readds these customers after fuzzing them up

#2. archivalTransactionsOnly: similar to above, but generates a set of transactions only.

import csv
import pandas as pd
import shutil, os
import datetime
import random
import fnmatch

import rando as r
import fuzzies as f
import fuzzmap as fuzz
import settings as s
import datatypes as dt 
import datatypemap as dtm


def archivalCustomerReader() -> pd.DataFrame():

	# IF we find some customer files, let's try to read one and randomly pick
	# older rows, then fuzz, then assign new ID, and reinsert back into our writing frames

	filenames = []
	for root, dirs, files in os.walk(s.outputdir):
			for f in files:
				if fnmatch.fnmatch(f,'*' + s.primaryfilenamefragment + '.csv'):
					filenames.append(f)
	
	if len(filenames) > 0:

		fname = s.outputdir + "/" + random.choice(filenames)

		with open(fname, 'r') as the_file:

			reader = the_file.readlines()
			row_count, back_ten_percent = sum(1 for row in reader), int( sum(1 for row in reader) / 10)


			rowback = row_count-back_ten_percent

			# we will only attempt to add 1% of existing customers as new fuzzed customers:
			archivedCustomers = pd.read_csv(fname, skiprows=rowback, nrows=int(s.ITERATE*.01), names=dtm.primaryCustomerColumns)

			for column in archivedCustomers.columns[1:]:
				archivedCustomers[column] = archivedCustomers[column].map(lambda x: fuzz.fuzzMap(column, str(x)))

		return archivedCustomers
	else:
		archivedCustomers = pd.DataFrame(columns=dtm.primaryCustomerColumns)
		return archivedCustomers


def archivalTransactionsOnly():

	# If we find some customer files, let's try to read one and randomly pick
	# older rows, then fuzz, then assign new ID, and reinsert back into our writing frames

	filenames = []
	for root, dirs, files in os.walk(s.outputdir):
			for f in files:
				if fnmatch.fnmatch(f,'*CustomerseCommerce.csv'):
					filenames.append(f)
	
	if len(filenames) > 0:

		fname = s.outputdir + "/" + random.choice(filenames)
		with open(fname, 'r') as the_file:
			reader = the_file.readlines()			
			archivedCustomers = pd.read_csv(fname, skiprows=1, names=dtm.primaryCustomerColumns)
			dt.populateTransactions(archivedCustomers, 'NoCustomersTransactionsOnly')



