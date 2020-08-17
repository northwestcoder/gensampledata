import string
import pandas as pd
import os
import datetime

import settings as s 
import rando as r


#
# READ AND WRITE COUNTERS
#

def getLastCustomerID():

	id = 1000000000
	if not os.path.exists(s.counterdir + "/ID_customer"):
		return id
	else:
		with open(s.counterdir + "/ID_customer", "r") as ID_customer:
			ID_customerIncrement = int(ID_customer.read())
			ID_customer.close()
			return ID_customerIncrement

def getLastTransactionID():

	id = 100000000000
	if not os.path.exists(s.counterdir + "/ID_Transactions"):
		return id
	else:
		with open(s.counterdir + "/ID_Transactions", "r") as ID_eCommerceTransactions:
			ID_eCommerceTransactionsIncrement = int(ID_eCommerceTransactions.read())
			ID_eCommerceTransactions.close()
			return ID_eCommerceTransactionsIncrement

def getLastEcID():
	id = 1000000000
	if not os.path.exists(s.counterdir + "/ID_ec"):
		return id
	else:
		with open(s.counterdir + "/ID_ec", "r") as ID_EC:
			ID_EcIncrement = int(ID_EC.read())
			ID_EC.close()
			return ID_EcIncrement

def getLastClickstreamID():

	id = 1000000000
	if not os.path.exists(s.counterdir + "/ID_clickstream"):
		return id
	else:
		with open(s.counterdir + "/ID_clickstream", "r") as ID_clickstream:
			ID_clickstreamIncrement = int(ID_clickstream.read())
			ID_clickstream.close()
			return ID_clickstreamIncrement



class gen_incrementor(object):
	def __init__(self, start):
		self.count=start
	def __call__(self, jump=1):
		self.count += jump
		return self.count
	def current(self):
		return self.count

nextCustomerID 			= gen_incrementor(getLastCustomerID())
nextTransID    			= gen_incrementor(getLastTransactionID())
nextEcID      			= gen_incrementor(getLastEcID())
nextClickstreamID		= gen_incrementor(getLastClickstreamID())


totalRowsCreated = gen_incrementor(0)

def CustomerIDWriter():
	print(nextCustomerID.current())
	ID_customerWriter = open(s.counterdir + "/ID_customer", "w+")
	ID_customerWriter.write(str(nextCustomerID.current()))
	ID_customerWriter.close()

def TransactionIDWriter():
	ID_eCommerceTransactionsWriter = open(s.counterdir + "/ID_Transactions", "w+")
	ID_eCommerceTransactionsWriter.write(str(nextTransID.current()))
	ID_eCommerceTransactionsWriter.close()

def EcIDWriter():
	ID_EcWriter = open(s.counterdir + "/ID_ec", "w+")
	ID_EcWriter.write(str(nextEcID.current()))
	ID_EcWriter.close()

def ClickstreamIDWriter():
	ID_ClickstreamWriter = open(s.counterdir + "/ID_clickstream", "w+")
	ID_ClickstreamWriter.write(str(nextClickstreamID.current()))
	ID_ClickstreamWriter.close()



#
# File Writing
#

def amp_filewriter(DF: pd.DataFrame, filename: string):

	#this updates our total row count for this one session
	totalRowsCreated(DF.shape[0])

	if not os.path.exists(s.outputdir):
		os.makedirs(s.outputdir)

	fname = ''
	fnamejson = ''
	#build stable path
	if s.USE_TODAY_DATE:
		fname = s.outputdir + "/" + s.today + s.fileprefix + filename + '.csv'
	else:
		fname = s.outputdir + "/" + s.fileprefix + filename + '.csv'


	if s.USE_TODAY_DATE:
		fnamejson = s.outputdir + "/" + s.today + s.fileprefix + filename + '.json'
	else:
		fnamejson = s.outputdir + "/" + s.fileprefix + filename + '.json'


	# if first time then we need column headers
	if s.LOAD_TYPE == "truncate" and s.ITERNUM==1:
		with open(fname, 'w') as f:
			DF.to_csv(fname, mode='a', header=True, index=False, quoting=1)
			f.close()
		with open(fnamejson, 'w') as f:
			DF.to_json(fnamejson, orient='records', lines = True)
			f.close()


	# else no headers
	elif s.LOAD_TYPE == "truncate" and s.ITERNUM != 1:
		with open(fname, 'a') as f:
			DF.to_csv(fname, mode='a', header=False, index=False, quoting=1)
			f.close()
		with open(fnamejson, 'a') as f:
			DF.to_json(fnamejson, orient='records', lines = True)
			f.close()			

	#same as above, but with file append, not truncate
	elif s.LOAD_TYPE != "truncate" and s.ITERNUM == 1:
		with open(fname, 'a') as f:
			DF.to_csv(fname, mode='a', header=True, index=False, quoting=1)
			f.close()
	else:
		with open(fname, 'a') as f:
			DF.to_csv(fname, mode='a', header=False, index=False, quoting=1)
			f.close()




