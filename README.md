![acme anvil](anvil.png)

## gensampledata

#### The original fake data -generating CLI

---

**TL/DR:**


`%>python3 gensampledata.py` 

(built with python 3.7.x your mileage may vary with other versions)

This will default to generating 1000 customers with a 0% dupe rate. That's right you read correctly: you can set a dupe rate above 0% at which point this app will copy some of its own data and then fuzz/corrupt the copies. Wut?

 More specifically, it will generate:

- 1000 customers in a fictitious Customers csv file and this file will have a 0% dupe rate. Configurable.
- 1000 times 1-N transactions e.g. a few thousand transactions for the above customer master file. Configurable.
- A second CustomerPos file which uses customer info from the first file ... and a transactions2 file to go with it. At this point we have four files.
- 1000 customers in a fictitious Loyalty Systenm (LMS) master csv file, again using _some_ info from the first customer master file. At this point we have five files.
- 1000 Email Campaign records in an email master csv file, again using _some_ info from the first customer master file. At this point we have six files.
- Clickstream data!
- Mobile data!
- Wifi data!
- Safety Inspections Data

Each of the above can be turned on or off in settings.py

Oh hey let's talk about settings.py and why we didn't build command line options or argv: the premise here was to run multiple instances of this client in various directories. We wanted the directory location itself to identity the "purpose" of the invoked python app. Put another way, we didn't want a ridiculously long python command with a bunch of arguemnts.

All files have referential integrity - they are meant to be loaded into a RDBMS and then joined against each other - with "customerID" linking throughout. 

Each time it is run, by default the files are truncated and rebuilt on a _daily_ basis - see below for overrides. The creation is done in batches of 1000 records to keep the memory footprint reasonable. While there are probably ways to improve performance, it's worth noting that there is a lot of fuzzing and corruption of data on a cell by cell basis. On a mac laptop, 100,000 "customers" - which is really several hundred thousand records in total - takes about 8 minutes to create. Not too bad...

**Requirements**

#### [pyenv](https://github.com/yyuu/pyenv)
	
This project was created for python 3.7.x. You can try to install manually if you wish, but we recommend pyenv:

1. `brew install pyenv pyenv-virtualenv readline`
2. `brew link readline` -- use force option if prompted
3. `sudo nano ~/.bash_profile`
4. copy-paste the following into an empty part of the file, then hit ctrl-O and ctrl-X to save and quit:
>if which pyenv > /dev/null; then eval "$(pyenv init -)"; fi
>
>if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi
5. Restart your shell
6. `pyenv install 3.7.0`
7. `pip install --upgrade pip` to upgrade pip to the latest version
8. `pip install awscli` to enabled support for sending your fake data to your S3 bucket
9. `pip install boto3` to enabled support for sending your fake data to your S3 bucket
10. `pip install faker` required for this app to run
11. `pip install pandas` required for this app to run
12. `pip install numpy` required for this app to run
13. `pip install hvac` required for using hashicorp vault when publishing to S3

(we also include a pip freeze requirements file)

navigate to the dir where gensampledata is copied, and run:

13. `python refake.py` this generates local text files for use by this program

**Overrides:**

We'll get this python-packaged up in the near future. For now, all the flags are in *settings.py*:

ITERATE

_number of customers to iterate, default is 1000_

OVERALL_DUPE_RATE

_dupe rate 0-100, default is 15_

VARIANCE_DUPE_RATE

_variance using the above duperate, default is 0_

LOAD_TYPE

_choices are "truncate" which will blow away the csv files (but keep the last generated ID seeds) or "append" which will append to the files, default is truncate. Note: this is on a "daily" basis, anything older is left alone_

TRANS_TYPE

_choices are "full" or "daily". For our fake transaction files, do you want "5 years of historical dates" (full) or "timestamps from the last 24 hours" "daily", default is "full"_

MAX_TRANS_PER_CUSTOMER

_for two of the data sources (ecomm and POS) we also generate transactions. This setting sets a ceiling for each customer, during data gen we will generate 1 to N transactions based on this setting._

AMP_S3_BUCKETNAME & AMP_S3_PREFIX

_attempts to publish to a bucket with prefix called "prefixpathname" (you need to change this pls! :) in your S3 bucket as configured by aws cli on your client machine._

SHOW_TIMER

_whether or not to show timers_

CREATE_DS_*

_there are a bunch of flags to turn off various data sources, these are all turned on by default_

TRACER_DATA

_take a look at tracer.py or see below - basically this attempts to load humanly created data into the primary data source_

USE_ARCHIVAL

_in production, when this python client is scheduled to run on a daily basis, this flag will attempt to a) retrieve a random customer file that was generated in the past, b) pull out 1% of the records, c) fuzz them up, and d) insert them into the stream._

ARCHIVAL_COUNT

_with the above, this is the number of loops to retrieve archived customers. I.E. higher value creates a higher cluster count for these id's_


---

Installation:

- On a totally virgin machine you'll need to get the following sorted out:
	- Built using python 3.7.x and pyenv
	- pip installs of note: awscli, boto3, faker, pandas, numpy
	- you can call refake.py if you want to regenerate the random data
	- flat file structure, no other dependencies should be needed.
	- if you use the S3 settings in *settings.py* we assume you have configured your client machine with a particular aws IAM key and secret key, else error.


---


Fuzzing:

A dupe rate above 0% means you are deliberately generating multiple copies of the same "human being". We use a variety of common patterns for this which you can study in fuzzies.py and fuzzmap.py

---

Tracer Program:

If in settings.py you set TRACER_DATA = True then you will have enabled the tracer feature. This will require you to place a single csv file into a sub-directory called "tracer" - we have provided a sample in "tracer_orig". The reason there is a tracer_orig is that the code will delete the CSV file once it consumes it, the premise being that in "production" this data gen client should _not_ be repeatedly ingesting the same file over and over again.

If this data client finds a file named tracer.csv in the tracer sub-directory, it will consume that info and place it into the eCommerce customer file.

---

Future work:


- vault integration for aws keys.
- performance improvements and refactoring.
- abstraction of data types and csv file types,
	- e.g. let people define what kinds of csv files they want to create,
	- or maybe we read an JSON file to define all of this. The code is already leaning toward these ideas.
- i'm really bad at all of this, pls play nice.

---
