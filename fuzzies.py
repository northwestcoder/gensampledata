import pandas as pd
import string
import random
import datetime
import rando as r
import csv, gzip
import os
import settings as s

# Some General Notes:
# I think I could spend a lifetime in this one file... sigh.
#
# also for now, we've added in a default "do nothing" handler, 
# because of all the dice rolling...
# it can start to look a little too severe if we don't.

# Do Nothing handler

def corruptNothingCorrupted(input):
	return input

# Kill the cell entirely handler

def corruptCellDeleted(input):
	return ''

# email fuzz

def corruptEmailLiar(input):
	if input is not None:
		if str(input).find("@"):
			chunk = str(input).split("@")[0]
			tempdomain = random.choice(r.staticdata.domains())
			result = chunk + '@' + tempdomain
			return result
		else:
			return input
	else:
		return input

# String and Name Fuzz

# nickname database and fuzz
def Create_NonNan_Set(a):
	return list(set(filter(lambda x: x != 'NAN' , a)))
df_given_name = pd.read_csv(s.supportdir + '/given_name_alternatives.csv', sep=',', header=None, names=['Name','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'])
df_given_name = df_given_name.applymap(str.lower)
df_given_name['Alter_all'] = df_given_name[['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']].apply(Create_NonNan_Set, axis=1)
dict_given_name = dict(zip(df_given_name.Name, df_given_name.Alter_all))

def open_gzip_csv_to_list(file_name):
	with open(file_name, "r") as f:
		f=csv.reader(f, delimiter=',')
		return list(f)[0]

common_given_names = map(str.upper, open_gzip_csv_to_list(s.supportdir + '/common_given_names.csv'))

def corruptNickName(name):
	test = name.lower()
	result = random.choice(dict_given_name.get(test, [name]))
	if result == "nan":
		return name
	else:
		return result

def corruptNewLastName(input):
	return random.choice(r.staticdata.lastnames())


def corruptNewPostalCode(input):
	return random.choice(r.staticdata.postalcodes())

def corruptNewCity(input):
	tempCity = random.choice(r.staticdata.city_state_combos()).split(',')
	return tempCity[0]

def corruptNewAddress(input):
	return random.choice(r.staticdata.streetnames())

# Date Fuzz
def corruptDateDelete(input):
	return ''

def corruptBirthDate(birthdate_orig):
	if str(birthdate_orig) == '' or str(birthdate_orig) is "nan" or len(str(birthdate_orig)) < 10:
		return birthdate_orig
	else:
		k = random.randint(0, 24)	
		if k <= 2: # do nothing
			if s.DEBUG:
				print("no change to date")
			birthdate = birthdate_orig
			return birthdate
		elif k <= 10: # add 1 to birth year

			birthdate = birthdate_orig[:6] + str(int(birthdate_orig[6:])+1) 
			return birthdate

		elif k <= 14: # minus 1 to birth year
			if s.DEBUG:
				print("minus 1 to year")
			birthdate = birthdate_orig[:6] + str(int(birthdate_orig[6:])-1)
			return birthdate
		
		elif k <= 16: # swap month and day
			if s.DEBUG:
				print("swap month and day")
			if len(birthdate_orig) == 10:
				m, d, y = birthdate_orig.split('/')
				birthdate = str(min(int(d), 12))  + '/' + m + '/' + y
				return birthdate
			else:
				return birthdate_orig

		elif k <= 21: # JAN 1
			if s.DEBUG:
				print("set to Jan 1")
			m, d, y = birthdate_orig.split('/')
			birthdate = '01/01/' + y
			return birthdate
		
		else: 		# set to 1900
			if s.DEBUG:
				print("set to 1900")
			m, d, y = birthdate_orig.split('/')
			birthdate = m  + '/' + d + '/' + "1900"
			return birthdate

def corruptUpperFirstChunk(input):
	if len(input) > 3:
		return input[:3].upper()
	else:
		return input.upper()

def corruptFatFingered(input):
	inp = str(input)
	if inp != '':
		char = random.randint(0,len(inp)-1)
		#don't ever fat finger an @ sign
		if inp[char] != "@":
			if char == 0:
				inp = inp[:1] + inp[0:]
				return inp
			else:
				inp = inp[:char] + inp[char-1:]
				return inp
		else:
			inp = inp[:char-1] + inp[(char+1):]
	else:
		return inp

def corruptUpper(input):
	return input.upper()

def corruptWordDyslexia(input):
	words = str(input).split()
	randomWords = ' '.join(random.sample(words, len(words))) if len(words) > 2 else ' '.join(str(input).split()[::-1])
	return randomWords

def corruptCharacterDyslexia(input):
	if str(input) != '' and len(str(input))>2:
		location1 = random.randint(0,len(str(input))-1)
		location2 = location1+1 if location1 == 0 else location1-1
		result = list(str(input))
		result[location1], result[location2] = result[location2], result[location1]
		return ''.join(result)
	else:
		return input

def corruptFirstInitialOnly(input):
	if input != '':
		return str(input)[0]
	else:
		return input

# Gender Fuzz
def corruptGenderSwap(input):
	if input[0].upper() == "F":
		return "M"
	else: 
		return "F"

# Phone Fuzz
def corruptNewPhone(input):
	#print(input[3])
	if input[3] == "-":
		phone = str(random.randint(201,895)) + "-" + str(random.randint(0,999)) + "-" + str(random.randint(1000,9999))
		return phone
	elif input[0] == "(" and input[4] == ")":
		return "(" + str(random.randint(201,895)) + ") " + input[-8:] 
	else:
		return input

def corruptNewAddress(input):
	return str(random.randint(200,3400)) + " " + random.choice(r.staticdata.streetnames())

# State Fuzz
def corruptNewState(input):
	tempState = random.choice(r.staticdata.city_state_combos()).split(',')
	return tempState[1]


