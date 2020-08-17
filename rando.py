import numpy as np
import random
import os
import string
import settings as s
from faker import Faker


# various randomizers


def id_generator(size=8, chars=string.ascii_lowercase + string.digits):
    uniqueid = ''.join(random.choice(chars) for _ in range(size))
    return uniqueid


def randomlySelected(chanceof, range):
	# e.g. if 6 out of 13 chance odds
	if np.random.randint(range) < chanceof:
		return True
	else:
		return False

# NOTE: at the time of generation we still roll a "sample" dice a few different times, 
# so you should NOT expect the following example:
# iterate is 20, dupeRate is 5, thus I am guaranteed 20 + (5 * .5 +/- variance) rows.
# it will be in a close range, but still a throw of the dice for pandas.sample()

def currentDupeRate():
	tempVarianceRate = s.VARIANCE_DUPE_RATE/100
	if s.OVERALL_DUPE_RATE - s.OVERALL_DUPE_RATE*tempVarianceRate < 0:
		tempLower = 0
	else:	
		tempLower = s.OVERALL_DUPE_RATE - s.OVERALL_DUPE_RATE*tempVarianceRate
	if s.OVERALL_DUPE_RATE + s.OVERALL_DUPE_RATE*tempVarianceRate < 0:
		tempUpper = 0
	else: 
		tempUpper = s.OVERALL_DUPE_RATE + s.OVERALL_DUPE_RATE*tempVarianceRate
	nowDupeRate = random.randint(int(tempLower),int(tempUpper))
	return nowDupeRate

# some other quick lists

middleInitial = map(chr, range(ord('A'), ord('Z') + 1))

typeAccountStatus = ['Active', 'Active','Closed', 'DNC', 'Remarket', 'Active', 'Active', 'Active']

injuryReportType = ['Incident', 'Near Miss', 'Observation', 'Injury']

reportPriority = ['Critical', 'Normal', 'Low']

# squirrel for creating realistic looking emails using first name, last name, and company name

def genEmail(first_name, last_name, employ):

	temptld = random.choice(staticdata.tld())

	# out of 100, what are we going to do for a variety of emails?
	dice = random.randint(1,100)
	if dice >= 75:
		# email gen random word plus first name
		fragment0 = ''.join(random.choice(staticdata.randowords())) + "_"
		fragment1 = first_name.lower() + "@" + ''.join(e for e in employ if e.isalnum()).lower() + '.' + temptld
		return (fragment0 + fragment1)
	elif dice >= 50:
		# FIRST AND LAST NAME
		fragment0 = first_name.lower() + last_name.lower() + "@" + ''.join(e for e in employ if e.isalnum()).lower() + '.' + temptld
		return (fragment0)
	elif dice >= 25:
		#FIRST INITIAL, LAST NAME, AND A INTEGER
		fragment0 = first_name[0].lower() + last_name.lower() + str(random.randint(100,999)-1) + "@" + ''.join(e for e in employ if e.isalnum()).lower() + '.' + temptld
		return (fragment0)
	else:
		# FIRST INITIAL AND LAST NAME
		fragment0 = first_name[0].lower() + last_name.lower() + "@" + ''.join(e for e in employ if e.isalnum()).lower() + '.' + temptld
		return (fragment0)


#always generate dates from last 24 hours and last 1 hour for recent transactions
def RegenDates():

	fake = Faker('en_US')

	print("rebuilding 50000 timestamps for last 5 years...")

	lastfiveyeardates = []
	for _ in range(50000):		
		lastfiveyeardates.append(fake.past_datetime(start_date="-1825d", tzinfo=None))
	with open(s.supportdir + "/lastfiveyeardates.csv", "w") as output:
		for idx, val in enumerate(lastfiveyeardates):
			if idx != len(lastfiveyeardates)-1:
				output.write(str(val) + '\n')
			else:
				output.write(str(val))
	output.close()

	print("rebuilding 5000 timestamps for last 24 hours...")

	last24hoursdates = []
	for _ in range(5000):		
		last24hoursdates.append(fake.past_datetime(start_date="-1d", tzinfo=None))
	with open(s.supportdir + "/last24hoursdates.csv", "w") as output:
		for idx, val in enumerate(last24hoursdates):
			if idx != len(last24hoursdates)-1:
				output.write(str(val) + '\n')
			else:
				output.write(str(val))
	output.close()

	print("rebuilding 1000 timestamps for last 1 hour...")
	last1hourdates = []
	for _ in range(1000):		
		last1hourdates.append(fake.past_datetime(start_date="-1h", tzinfo=None))
	with open(s.supportdir + "/last1hourdates.csv", "w") as output:
		for idx, val in enumerate(last1hourdates):
			if idx != len(last1hourdates)-1:
				output.write(str(val) + '\n')
			else:
				output.write(str(val))
	output.close()

	print("done!")


# loading a bunch of static text files into memory which is lazy but works
if s.TRANS_TYPE == 'daily':
	RegenDates()

for filename in os.listdir(s.supportdir):
	#first, if we want current dates, regen this file prior to loading into memory
	if filename.endswith(".csv") or filename.endswith(".txt"): 
		arrayname = os.path.join(filename[:-4])
		globals()["df_"+arrayname] = 0
		with open(s.supportdir + "/" + filename, "r") as file:
			globals()["df_"+arrayname] = file.read().split('\n')
			file.close()
	else:
		continue

#and then, another lazy load-into-memory to become a singleton.
class StaticData():

	def prefix_female(self):
			return df_prefix_female
	def prefix_male(self):
		return df_prefix_male
	def lastnames(self):
		return df_lastnames
	def firstnames_female(self):
		return df_firstnames_female
	def firstnames_male(self):
		return df_firstnames_male
	def companies(self):
		return df_companies
	def streetnames(self):
		return df_streetnames
	def streetnames2(self):
		return df_streetnames2
	def cities(self):
		return df_cities
	def postalcodes(self):
		return df_postalcodes
	def states(self):
		return df_states
	def birthdates(self):
		return df_birthdates
	def jobs(self):
		return df_jobs
	def phones(self):
		return df_phones
	def jobs(self):
		return df_jobs
	def lmscreatedates(self):
		return df_lmscreatedates
	def last24hoursdates(self):
		return df_last24hoursdates
	def last1hourdates(self):
		return df_last1hourdates		
	def lastfiveyeardates(self):
		return df_lastfiveyeardates
	def uuid4(self):
		return df_uuid4
	def uris(self):
		return df_uris
	def city_state_combos(self):
		return df_us_cities_states_counties	
	def ipv6(self):
		return df_ipv6	
	def user_agent(self):
		return df_user_agent		
	def emailcampaigns(self):
		return df_emailcampaigns
	def domains(self):
		return df_domains
	def loyaltytiers(self):
		return df_loyaltytiers
	def loyaltyprograms(self):
		return df_loyaltyprograms
	def emailCampaignFormats(self):
		return ['HTML','s/mime','plaintext']
	def tld(self):
		return df_tld
	def sha256(self):
		return df_sha256
	def randowords(self):
		return df_randowords
	def injuries(self):
		return df_injuries
	def latlongs(self):
		return df_latlongs

#and thus, our happy singleton guy:
staticdata = StaticData()
