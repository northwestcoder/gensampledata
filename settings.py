import os
import datetime

# SETTINGS

# Are we doing a full load or an append load?
LOAD_TYPE = "truncate"    # choices are append or truncate

# How many records in general?
ITERATE = 1000

# if true, injects an 8 bit alpha key into the primary key, else just an INT
USE_ALPHA_KEY = True 

# In percentage displayed as 0-100%, how many dupes in customers, lms and other data types?
OVERALL_DUPE_RATE = 0

# Vary the above dupe rate as 0-100 on our current run, this is a percent of a percent
# I.e. OVERALL_DUPE_RATE + (OVERAL_DUPE_RATE * +/- VARIANCE_DUPE_RATE)
# this is only useful when you automate this client on a daily basis
VARIANCE_DUPE_RATE = 0

# For transactions, our loyalty point system defaults to 2% or this value e.g 0-100:
POINTS_EARNED = 2

# For Transactions that we generate, you can specify either 'full' e.g. last five years
# Or 'daily' for last 24 hours
TRANS_TYPE = "full" # choices are full or daily

# we'll generate 1 to N transactions per customer. N can be set here as a maximum:
MAX_TRANS_PER_CUSTOMER = 4

# leave the following alone, this tells the program to batch job the data gen in X row increments
# we found that 100-1,000 is a good bell curve number that doesn't peg your machine's CPU and RAM
LOOPER = 1000
ITERNUM = 1

# Whether or not to prepend YYYY_MM_DD to the csv file names
USE_TODAY_DATE = True

# This app uses S3 if available. Enter your bucket name 
# and prefix (path) below - if null then we skip this part
SEND_TO_S3 = False
AMP_S3_BUCKETNAME = 'amperity-customer-85ofzb'
AMP_S3_PREFIX = 'acme2/ingest/'  # do not use a leading slash and DO use a trailing slash

# for testing, you can set to false for any of the data we normally create.
# if everything below is False, we would create a single customer file 
# (with dupes) and a single transaction file to go with it.

CREATE_PRIMARY_CUSTOMERS = True
CREATE_PRIMARY_TRANSACTIONS = True
CREATE_DS_SECONDARY = True
CREATE_DS_LOYALTY = True
CREATE_DS_EMAILCAMPAIGN = True
CREATE_DS_CLICKSTREAM = True
CREATE_DS_MOBILE = True
CREATE_DS_WIFI = True
CREATE_SAFETY = True
CREATE_TILEDATA = True
CREATE_CUSTOM_OBJECT = True

DEBUG = False

# Show timing during generation
SHOW_TIMER = True

# Use mysterious tracer data feature - see tracer.py for info
TRACER_DATA = False

# Use mysterious add-archived-customers feature, see archival.py for info
USE_ARCHIVAL = False
# Archival Count will iterate through the discovered, archived customers
# this is for graeme, to create high cardinality clusters :)
ARCHIVAL_COUNT = 5

# The rest of this is stock stuff, we recommend leaving it alone

datagendir = os.path.dirname(__file__)
counterdir = os.path.join(datagendir, 'counters')
outputdir = os.path.join(datagendir, 'output')
tracerdir = os.path.join(datagendir, 'tracer')
supportdir = os.path.join(datagendir, 'support')
edndir = os.path.join(datagendir, 'EDN')

today = str(datetime.date.today().strftime('%Y_%m_%d'))

dtUpdateDate = str(datetime.datetime.today())

fileprefix = 'Customers'
primaryfilenamefragment = ""