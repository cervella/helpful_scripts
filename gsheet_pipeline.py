import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine
import pandas as pd
from configparser import ConfigParser
from os.path import isfile, expanduser
import boto3
import csv
import json
import pandas
import luigi
from luigi.contrib import redshift
from luigi.contrib.s3 import S3Target
import datetime


config = ConfigParser()
homepath = expanduser('~')
config.read(homepath+'/.aws/credentials')
aws_key = config.get('default', 'aws_access_key_id')
aws_secret = config.get('default', 'aws_secret_access_key')

redshift_host = config.get('redshift', 'host')
redshift_db = config.get('redshift', 'db')
redshift_user = config.get('redshift', 'user')
redshift_pass = config.get('redshift', 'pass')

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name(homepath+'\\Desktop\\'+'My Project-a1c7a00fe86e.json', scope)
client = gspread.authorize(creds)

class ExportResponses(luigi.ExternalTask):
    
    #Export local csv from google sheets

    date = luigi.DateParameter(default=datetime.date.today())

    #check for s3 copy
    def output(self):
        return luigi.contrib.s3.S3Target('s3://afscme-analytics-etl/DOA_reporting.csv')
    
    def requires(self):
    	return None

    def run(self):

        sheet = client.open('Day of Action 2018 (Responses)').sheet1
        dataz = sheet.get_all_values()
        df = pandas.DataFrame(data=dataz)
        df.to_csv("./DOA_reporting.csv", sep=',', index=False, header=False, date_format=string)

        try:
        	s3=boto3.resource('s3')
        	s3file = s3.Object('afscme-analytics-etl/{}'.format(self.date.strftime('DOA_reporting%Y%m%d.csv')))
        	s3file.put(Body=open('./DOA_reporting.csv', 'rb'))
        except:
        	raise IOError('Responses Failed to Copt to S3')


class ResponsesLoad(redshift.S3CopyToTable):

    host = redshift_host
    database = redshift_db
    user = redshift_user
    password = redshift_pass
    aws_access_key = aws_key
    aws_secret_access_key = aws_secret
    do_truncate_table = True
    table = 'doa'
    columns = [
      ('timestamp', 'datetime')
    , ('reportingday', 'date')
    , ('city', 'varchar')
    , ('yourname', 'varchar')
    , ('howmanyinterested', 'int')
    , ('howmanygoing', 'int')
    , ('rsvpscollected', 'int')
    , ('organizationfromwhichrsvpwascollected', 'varchar')
    , ('didyouneedtoaddanotherorganization', 'varchar')
    , ('rsvpscollected_9', 'int'	)
    , ('organizationfromwhichrsvpwascollected_10', 'varchar')
    , ('positionofnote', 'varchar')
    , ('nameofspeaker', 'varchar')
    , ('vettedstatus', 'varchar')
    , ('doyouhaveanymorepotentialspeakerstoday', 'varchar')
    , ('positionofnote_15', 'varchar')
    , ('nameofspeaker_16', 'varchar')
    , ('vettedstatus_17', 'varchar')
    , ('doyouhaveanymorepotentialspeakerstoday_18', 'varchar')
    , ('positionofnote_19', 'varchar')
    , ('nameofspeaker_20', 'varchar')
    , ('vettedstatus_21', 'varchar')
    , ('doyouhaveanymorepotentialspeakerstoday_22', 'varchar')
    , ('positionofnote_23', 'varchar')
    , ('nameofspeaker_24', 'varchar')
    , ('doyouhaveanymorepotentialspeakerstoday_25', 'varchar')
    , ('rsvpscollected_26', 'int')
    , ('organizationfromwhichrsvpwascollected_27', 'varchar')
    , ('didyouneedtoaddanotherorganization_28', 'varchar')
        ]
    #this file has a header
    copy_options = r"REGION 'us-east-1' CSV EMPTYASNULL FILLRECORD IGNORE1ROW"

    def s3_load_path(self):
        return 's3://afscme-analytics-etl/DOA_reporting.csv'

    def requires(self):
       	return [ExportResponses(datetime.date.today())]

class GoogleLoop(luigi.task.WrapperTask):
	'''wrapper to initiate'''
	def requires(self):
		return [ExportResponses(datetime.date.today())]
	def complete(self):
		return False


if __name__ == '__main__':
    luigi.run(['ResponsesLoad', '--workers', '2'])