import boto3
from boto3.s3.transfer import S3Transfer
import shutil, os
import settings as s

def sendToS3(date):

	if s.AMP_S3_PREFIX != '' and s.AMP_S3_BUCKETNAME != '':
		print("sending files to your s3 bucket...")
		s3 = boto3.resource('s3')
		client = s3.meta.client
		transfer = S3Transfer(client)
		for filename in os.listdir(s.outputdir):
			if filename.endswith(".csv") and filename.startswith(date):
				transfer.upload_file(s.outputdir+"/"+filename,s.AMP_S3_BUCKETNAME,s.AMP_S3_PREFIX + filename,extra_args={'ServerSideEncryption': 'AES256'})
	else:
		print("aborted")