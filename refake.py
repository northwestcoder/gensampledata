import random
import csv
import pandas as pd
from faker import Faker
import numpy as np
import os
import rando as r
import settings as s

fake = Faker('en_US')


def main():

	print("please be patient, this make take a few moments")

	if not os.path.exists(s.supportdir):
		os.makedirs(s.supportdir)

	#all of this will do a bunch of one time work, this will regenerate Faker() data and save for future in ./support dir

	#generate birthdates
	birthdates = []
	for _ in range(3000):		
		birthdates.append(fake.date_between(start_date="-90y", end_date="-18y").strftime('%m/%d/%Y'))
	with open(s.supportdir + "/birthdates.csv", "w") as output:
		for idx, val in enumerate(birthdates):
			if idx != len(birthdates)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	#generate cities
	cities = []
	for _ in range(30000):		
		cities.append(fake.city())
	with open(s.supportdir + "/cities.csv", "w") as output:
		for idx, val in enumerate(cities):
			if idx != len(cities)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	# common given names
	# is a static file for now

	#generate fake company names:
	companies = []
	for _ in range(100000):
		companies.append(fake.company())
	with open(s.supportdir + "/companies.csv", "w") as output:
		for idx, val in enumerate(companies):
			if idx != len(companies)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	# popular domains
	domains = ["aol.com","att.net","comcast.net","facebook.com","gmail.com","gmx.com","googlemail.com","google.com","hotmail.com","hotmail.co.uk","mac.com","me.com","mail.com","msn.com","live.com","sbcglobal.net","verizon.net","yahoo.com","yahoo.co.uk","email.com","fastmail.fm","games.com","gmx.net","hush.com","hushmail.com","icloud.com","iname.com","inbox.com","lavabit.com","love.com","outlook.com","pobox.com","protonmail.com","rocketmail.com","safe-mail.net","wow.com","ygm.com","ymail.com","zoho.com","yandex.com","bellsouth.net","charter.net","cox.net","earthlink.net","juno.com","btinternet.com","virginmedia.com","blueyonder.co.uk","freeserve.co.uk","live.co.uk","bt.com","abc.com","nodns.com"]
	with open(s.supportdir + "/domains.csv", "w") as output:
		for idx, val in enumerate(domains):
			if idx != len(domains)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	# emailcampaigns
	# is meant to be a static file

	#generate female first names
	firstnames_female = []
	for _ in range(10000):
		firstnames_female .append(fake.first_name_female())
	with open(s.supportdir + "/firstnames_female.csv", "w") as output:
		for idx, val in enumerate(firstnames_female):
			if idx != len(firstnames_female)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	#generate male first names
	firstnames_male = []
	for _ in range(10000):
		firstnames_male.append(fake.first_name_male())
	with open(s.supportdir + "/firstnames_male.csv", "w") as output:
		for idx, val in enumerate(firstnames_male):
			if idx != len(firstnames_male)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	#generate ip addrs
	ipv6 = []
	for _ in range(2000):		
		ipv6.append(fake.ipv4())
	with open(s.supportdir + "/ipv6.csv", "w") as output:
		for idx, val in enumerate(ipv6):
			if idx != len(ipv6)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	#generate ip addrs
	ip_addresses = []
	for _ in range(1000):		
		ip_addresses.append(fake.ipv4())
	for _ in range(1000):
		ip_addresses.append(fake.ipv4_private())
	with open(s.supportdir + "/ip_addresses.csv", "w") as output:
		for idx, val in enumerate(ip_addresses):
			if idx != len(ip_addresses)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	#generate jobs
	jobs = []
	for _ in range(30000):		
		jobs.append(fake.job())
	with open(s.supportdir + "/jobs.csv", "w") as output:
		for idx, val in enumerate(jobs):
			if idx != len(jobs)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	#generate dates from last 24 hours
	last24hoursdates = []
	for _ in range(9000):		
		last24hoursdates.append(fake.past_datetime(start_date="-1d", tzinfo=None))
	with open(s.supportdir + "/last24hoursdates.csv", "w") as output:
		for idx, val in enumerate(last24hoursdates):
			if idx != len(last24hoursdates)-1:
				output.write(str(val) + '\n')
			else:
				output.write(str(val))
	output.close()

		#generate dates from last 1 hour
	last1hourdates = []
	for _ in range(3000):		
		last1hourdates.append(fake.past_datetime(start_date="-1h", tzinfo=None))
	with open(s.supportdir + "/last1hourdates.csv", "w") as output:
		for idx, val in enumerate(last1hourdates):
			if idx != len(last1hourdates)-1:
				output.write(str(val) + '\n')
			else:
				output.write(str(val))
	output.close()

	#generate dates from last 5 years
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

	#generate last names
	asiatic_names = ["Mammadov","Aliyev","Hasanov","Huseynov","Guliyev","Hajiev","Rasulov","Suleymanov","Musayev","Abbasov","Babayev","Valiyev","Orujov","Ismayilov","Ibrahimov","Beridze","Mammadov","Mamedovi","Kapanadze","Gelashvili","Aliyev","Alievi","Maisuradze","Giorgadze","Lomidze","Tsiklauri","Bolkvadze","Kvaratskhelia","Nozadze","Khutsishvili","Shengelia","Abuladze","Mikeladze","Tabatadze","Mchedlishvili","Bairamov","Bairamovi","Gogoladze","Mukherjee","Banerjee","Chatterjee","Ganguly","Ghoshal","Goswami","Sanyal","Chakraborty","Bhattacharya","Sengupta","Dasgupta","Duttagupta","Gupta","Sen-Sharma","Cohen","Levi","Levy","Mizrachi","Mizrahi","Peretz","Biton","Dahan","Avraham","Friedman","Malka","Malcah","Azoulay","Katz","Yosef","David","Amar","Omer","Ohayon","Ochion","Hadad","Chadad","Gabai","Ben-David","Adrei","Edry","Adary","Levin","Tal","Klein","Chen","Khen","Shapira","Chazan","Hazan","Moshe","Ashkenazi","Ohana","Segal","Segel","Golan","Sato","Suzuki","Takahashi","Tanaka","Watanabe","Ito","Nakamura","Kobayashi","Yamamoto","Kato","Yoshida","Yamada","Sasaki","Yamaguchi","Matsumoto","Inoue","Kimura","Shimizu","Hayashi","Saito","Saito","Yamazaki","Yamasaki","Nakajima","Nakashima","Mori","Abe","Ikeda","Hashimoto","Ishikawa","Yamashita","Ogawa","Ishii","Hasegawa","Goto","Okada","Kondo","Maeda","Fujita","Endo","Aoki","Sakamoto","Murakami","ota","Kaneko","Fujii","Fukuda","Nishimura","Miura","Takeuchi","Nakagawa","Okamoto","Matsuda","Harada","Nakano","Ono","Tamura","Fujiwara","Fujihara","Nakayama","Ishida","Kojima","Wada","Morita","Uchida","Shibata","Sakai","Hara","Takagi","Takaki","Yokoyama","Ando","Miyazaki","Miyasaki","Ueda","Ueta","Shimada","Kudo","ono","Miyamoto","Sugiyama","Imai","Maruyama","Masuda","Takada","Takata","Murata","Hirano","otsuka","Sugawara","Sugahara","Takeda","Taketa","Arai","Koyama","Oyama","Noguchi","Sakurai","Chiba","Iwasaki","Sano","Taniguchi","Ueno","Matsui","Kono","Kawano","Ichikawa","Watanabe","Watabe","Nomura","Kikuchi","Kinoshita","Song","Han","Shin","Kwon","Min","Jo","Hur","Seong","Son","Hon","Perera","Fernando","de Silva","Bandara","Kumara","Dissanayake","Mohamed","Gamage","Liyanage","Jayasinghe","Ranasinghe","Herath","Weerasinghe","Peiris","Rathnayake","Wickramasinghe","Wijesinghe","Hettiarachchi","Nanayakkara","Ahamed","Rajapaksha","Mendis","Pathirana","Ekanayake","Gunasekara","Dias","Sampath","Amarasinghe","Ratnayake","Chathuranga","Senanayake","Samarasinghe","Lakmal","Munasinghe","Rodrigo","Seneviratne","Rathnayaka","Edirisinghe","Jayawardena","Fonseka","Sanjeewa","Gunawardana","Gunawardena","Karunaratne","Jayaweera","Jayasekara","Ranaweera","Jayawardana","Jayasuriya","Madusanka"]
	lastnames = []
	for i in range(16):
		if i % 2 == 0:
			for i in range(len(asiatic_names)):
				lastnames.append(asiatic_names[i])
		for _ in range(3000):		
			lastnames.append(fake.last_name())
	with open(s.supportdir + "/lastnames.csv", "w") as output:
		for idx, val in enumerate(lastnames):
			if idx != len(lastnames)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	# generate LMS create dates
	lmscreatedates = []
	for _ in range(30000):		
		lmscreatedates.append(fake.date_between(start_date="-25y", end_date="-5y").strftime('%m/%d/%Y'))
	with open(s.supportdir + "/lmscreatedates.csv", "w") as output:
		for idx, val in enumerate(lmscreatedates):
			if idx != len(lmscreatedates)-1:
				output.write(str(val) + '\n')
			else:
				output.write(str(val))
	output.close()

	# loyaltyprograms is meant to be hand-entered

	# loyaltytiers is meant to be hand-entered

	# generate mac addr
	macaddr = []
	for _ in range(1000):		
		macaddr.append(fake.mac_address())
	with open(s.supportdir + "/macaddr.csv", "w") as output:
		for idx, val in enumerate(macaddr):
			if idx != len(macaddr)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	# generate phones
	phones = []
	for _ in range(300000):		
		phones.append(fake.phone_number())
	with open(s.supportdir + "/phones.csv", "w") as output:
		for idx, val in enumerate(phones):
			if idx != len(phones)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	#generate postal codes:
	postalcodes = []
	for _ in range(30000):
		if r.randomlySelected(2,9):
			addfour = random.randint(1000,9999)
			postalcodes.append(fake.postcode() + "-" + str(addfour))
		else:
			postalcodes.append(fake.postcode())
	with open(s.supportdir + "/postalcodes.csv", "w") as output:
		for idx, val in enumerate(postalcodes):
			if idx != len(postalcodes)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	#generate female prefix:
	prefix_female = []
	for _ in range(300):		
		prefix_female.append(fake.prefix_female())
	with open(s.supportdir + "/prefix_female.csv", "w") as output:
		for idx, val in enumerate(prefix_female):
			if idx != len(prefix_female)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	#generate male prefix:
	prefix_male = []
	for _ in range(300):		
		prefix_male.append(fake.prefix_male())
	with open(s.supportdir + "/prefix_male.csv", "w") as output:
		for idx, val in enumerate(prefix_male):
			if idx != len(prefix_male)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	#generate random words:
	randowords = []
	for _ in range(3000):		
		randowords.append(fake.words(nb=1))
	with open(s.supportdir + "/randowords.csv", "w") as output:
		for idx, val in enumerate(randowords):
			if idx != len(randowords)-1:
				for v in val:
					output.write(str(v))
				output.write('\n')
			else:
				for v in val:
					output.write(str(v))
	output.close()

	#generate sha256:
	sha256 = []
	for _ in range(4000):		
		sha256.append(fake.sha256())
	with open(s.supportdir + "/sha256.csv", "w") as output:
		for idx, val in enumerate(sha256):
			if idx != len(sha256)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	#generate states:
	states = []
	for _ in range(300):		
		states.append(fake.state())
	for _ in range(300):
		states.append(fake.state_abbr())
	with open(s.supportdir + "/states.csv", "w") as output:
		for idx, val in enumerate(states):
			if idx != len(states)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	#generate address line 1:
	streetnames = []
	addr_suffix = ['St','Rd','Circle','Alley','Avenue','Backroad','Boulevard','Byway','Close','Crescent','Court','Drive','Frontage road','Highway','Lane','Place','Road','Route','Street','Way']
	for _ in range(30000):
		streetnames.append(fake.street_name())
	with open(s.supportdir + "/streetnames.csv", "w") as output:
		for idx, val in enumerate(streetnames):
			if idx != len(streetnames)-1:
				stri = val + " " + random.choice(addr_suffix)
				output.write(stri + '\n')
			else:
				stri = val + " " + random.choice(addr_suffix)
				output.write(stri)
	output.close()

	#generate address line 2:
	streetnames2 = []
	for _ in range(1000):
		streetnames2.append(fake.secondary_address())
	with open(s.supportdir + "/streetnames2.csv", "w") as output:
		for idx, val in enumerate(streetnames2):
			if idx != len(streetnames2)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	#generate domain tld's:
	tld = []
	for _ in range(300):		
		tld.append(fake.tld())
	with open(s.supportdir + "/tld.csv", "w") as output:
		for idx, val in enumerate(tld):
			if idx != len(tld)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	#generate uri paths:
	uris = []
	for _ in range(1000):		
		uris.append(fake.uri_path())
	with open(s.supportdir + "/uris.csv", "w") as output:
		for idx, val in enumerate(uris):
			if idx != len(uris)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()


	latlongs = []
	for _ in range(100000):
		latlongs.append(fake.local_latlng())
	with open(s.supportdir + "/latlongs.csv", "w") as output:
		for idx, val in enumerate(latlongs):
			if idx != len(uris)-1:
				output.write(val[0] + "," + val[1] + '\n')
			else:
				output.write(val[0] + "," + val[1])
	output.close()



	#generate user agent
	user_agent = []
	for _ in range(1000):
		rollDice = random.randint(0,20)
		if rollDice < 2:
			user_agent.append(fake.firefox())
		elif rollDice < 3:
			user_agent.append(fake.opera())
		elif rollDice < 4:
			user_agent.append(fake.windows_platform_token())
		elif rollDice < 9:
			user_agent.append(fake.chrome(version_from=13, version_to=63, build_from=800, build_to=899))
		elif rollDice < 13:
			user_agent.append(fake.internet_explorer())
		elif rollDice < 16:
			user_agent.append(fake.safari())
	with open(s.supportdir + "/user_agent.csv", "w") as output:
		for idx, val in enumerate(user_agent):
			if idx != len(user_agent)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	#generate UUID's:
	uuid4 = []
	for _ in range(30000):		
		uuid4.append(fake.uuid4())
	with open(s.supportdir + "/uuid4.csv", "w") as output:
		for idx, val in enumerate(uuid4):
			if idx != len(uuid4)-1:
				output.write(val + '\n')
			else:
				output.write(val)
	output.close()

	print("Done!")

if __name__ == '__main__':
	main()

