import random
import fuzzies as f
import operator
import datawriter

# A simple mapping of field names to handler "groups" each of which
# in turn have a basket of child corruption handlers.
# if you have the same field names in different contexts (outside of this program)
# it doesn't really matter, since this program treats these things abstractly,
# just list them once, even if they occur multiple times in your specific customer experience
# if you do not list a handler below, we just pass the value through unchanged. so, no harm no foul

fuzzOptions = {
"master_id" : "fuzzyDoNothingHandler",
"customer_id" : "nextCustomerID",
"addr_ln_1_txt" : "fuzzyAddressHandler",
"name_first": "fuzzyFirstNameHandler",
"name_last": "fuzzyLastNameHandler",
"email" : "fuzzyEmailHandler",
"city" : "fuzzyCityHandler",
"birth_dt" : "fuzzyBirthDateHandler",
"phone" : "fuzzyPhoneHandler",
"address1" : "fuzzyAddressHandler",
"gender" : "fuzzyGenderHandler",
"postal_code" : "fuzzyPostalCodeHandler",
"full_name" : "fuzzyStringHandler",
"state" : "fuzzyStateAddrHandler",
"EMAIL" : "fuzzyEmailHandler",
"birthdate" : "fuzzyBirthDateHandler",
"fname" : "fuzzyFirstNameHandler",
"lname" : "fuzzyLastNameHandler"
	}

# sub-handlers for everything you saw before this point
# also see the fuzzies themselves in fuzzies.py
# Yes naming python variables dynamically 
# and storing them using globals() is not a good pattern.

def weightedDiceRole(fuzzWeight):
	index, maxDiceValue = max(enumerate(fuzzWeight), key=operator.itemgetter(1))
	rollDice = random.randint(0,maxDiceValue)
	first_index = next(index for index, value in enumerate(fuzzWeight) if rollDice <= value)
	return first_index

def nextCustomerID(input):
	newID = datawriter.nextCustomerID()
	return newID

def fuzzyDoNothingHandler(input):
	return input

def fuzzyFirstNameHandler(input):
	options = {
	0 : f.corruptFirstInitialOnly,
	1 : f.corruptCharacterDyslexia,
	2 : f.corruptUpper,
	3 : f.corruptUpperFirstChunk,
	4 : f.corruptNickName,
	5 : f.corruptNothingCorrupted
	}
	fuzzWeight = [5,10,15,20,99,100] # correlates to the above option list: left-to-right = top-to-bottom
	result = options[weightedDiceRole(fuzzWeight)](input)
	return result

def fuzzyLastNameHandler(input):
	options = {
	0 : f.corruptFirstInitialOnly,
	1 : f.corruptCharacterDyslexia,
	2 : f.corruptUpper,
	3 : f.corruptUpperFirstChunk,
	4 : f.corruptNewLastName,
	5 : f.corruptNothingCorrupted
	}
	fuzzWeight = [10,15,20,25,95,100] # correlates to the above option list: left-to-right = top-to-bottom
	result = options[weightedDiceRole(fuzzWeight)](input)
	return result

def fuzzyStringHandler(input):
	options = {
		0 : f.corruptFatFingered,
		1 : f.corruptWordDyslexia,
		2 : f.corruptCharacterDyslexia,
		3 : f.corruptFirstInitialOnly,
		4 : f.corruptNothingCorrupted
	}
	fuzzWeight = [10,30,40,50,100] # correlates to the above option list: left-to-right = top-to-bottom
	result = options[weightedDiceRole(fuzzWeight)](input)
	return result

def fuzzyCityHandler(input):
	options = {
		0 : f.corruptNewCity,
		1 : f.corruptWordDyslexia,
		2 : f.corruptCharacterDyslexia,
		3 : f.corruptFirstInitialOnly,
		4 : f.corruptNothingCorrupted
	}
	fuzzWeight = [50,60,80,95,100] # correlates to the above option list: left-to-right = top-to-bottom
	result = options[weightedDiceRole(fuzzWeight)](input)
	return result

def fuzzyBirthDateHandler(input):
	options = {
	0 : f.corruptCellDeleted,
	1 : f.corruptBirthDate,
	2 : f.corruptNothingCorrupted
	}
	fuzzWeight = [2,40,45] # correlates to the above option list: left-to-right = top-to-bottom
	result = options[weightedDiceRole(fuzzWeight)](input)
	return result

def fuzzyEmailHandler(input):
	options = {
	0 : f.corruptEmailLiar,
	1 : f.corruptCharacterDyslexia,
	2 : f.corruptFatFingered,
	3 : f.corruptNothingCorrupted
	}
	fuzzWeight = [10,30,40,50] # correlates to the above option list: left-to-right = top-to-bottom
	result = options[weightedDiceRole(fuzzWeight)](input)
	return result

def fuzzyPhoneHandler(input):
	options = {
	0 : f.corruptCharacterDyslexia,
	1 : f.corruptFatFingered,
	2 : f.corruptNewPhone,
	3 : f.corruptNothingCorrupted
	}
	fuzzWeight = [10,20,70,90] # correlates to the above option list: left-to-right = top-to-bottom
	result = options[weightedDiceRole(fuzzWeight)](input)
	return result

def fuzzyAddressHandler(input):
	options = {
	0 : f.corruptCharacterDyslexia,
	1 : f.corruptFatFingered,
	2 : f.corruptNewAddress,
	3 : f.corruptNothingCorrupted,
	4 : f.corruptWordDyslexia
	}
	fuzzWeight = [10,20,45,60, 80] # correlates to the above option list: left-to-right = top-to-bottom
	result = options[weightedDiceRole(fuzzWeight)](input)
	return result

def fuzzyGenderHandler(input):
	options = {
	0 : f.corruptGenderSwap,
	1 : f.corruptNothingCorrupted
	}
	fuzzWeight = [8,30] # correlates to the above option list: left-to-right = top-to-bottom
	result = options[weightedDiceRole(fuzzWeight)](input)
	return result

def fuzzyPostalCodeHandler(input):
	options = {
	0 : f.corruptCellDeleted,
	1 : f.corruptCharacterDyslexia,
	2 : f.corruptNewPostalCode,
	3 : f.corruptFatFingered,
	4 : f.corruptNothingCorrupted
	}
	fuzzWeight = [10,20,60,90,100] # correlates to the above option list: left-to-right = top-to-bottom
	result = options[weightedDiceRole(fuzzWeight)](input)
	return result

def fuzzyStateAddrHandler(input):
	options = {
	0 : f.corruptCellDeleted,
	1 : f.corruptNothingCorrupted,
	2 : f.corruptNewState,
	}
	fuzzWeight = [50,70,100] # correlates to the above option list: left-to-right = top-to-bottom
	result = options[weightedDiceRole(fuzzWeight)](input)
	return result

###############################################
# final handler of sub-handlers
# also see the fuzzmaps above
###############################################

def fuzzMap(type, value: str):
	options = fuzzOptions
	if options.get(type) is None:
		return value
	else:
		result = globals()[options.get(type)](value)
		return result
