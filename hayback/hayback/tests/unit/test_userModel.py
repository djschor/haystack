import os
import sys
import pickle
from datetime import datetime
from uuid import uuid4
import json
from decouple import config
import boto3
os.chdir('../../')
from hayback.models.userModel import create_user, retrieve_user, update_user, delete_user
from boto3.dynamodb.conditions import Key

print(sys.path)
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')#os.chdir('/Users/dschorin/Documents/projects/PersonalFinance/BluechipAWSBackend/hayback')
# aws_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
# print(aws_key)
# %env AWS_SECRET_ACCESS_KEY='YNeRUHOeMb7PQoIbpFTjcJjjbsy8GYcFnoJBUGuZ'
# %env AWS_ACCESS_KEY_ID = 'AKIATK6G7UOGVX6QXWVQ'

ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table('Bluechip')

def test_create_user(new_test_user):
  resp = create_user(new_test_user['email'], new_test_user['first_name'], new_test_user['last_name'], new_test_user['password'], new_test_user['phone_number'])
  print('response: ', resp)
  assert resp['Response']['ResponseMetadata']['HTTPStatusCode'] == 200

def test_retrieve_user(new_test_user):
  resp = retrieve_user(new_test_user['email'])
  print(resp)
  assert resp['pk'] == 'USER#{}'.format(new_test_user['email'])
  assert resp['sk'] == 'METADATA#{}'.format(new_test_user['email'])

def test_update_user(new_test_user):
  item = {'transactions': [1, 2, 3], 'holdings': [1, 2, 3]}
  resp = update_user(new_test_user['email'], item)
  print(resp)
  assert resp['ResponseMetadata']['HTTPStatusCode'] == 200

def test_delete_user(new_test_user):
  resp = delete_user(new_test_user['email'])
  print(resp)
  assert resp['ResponseMetadata']['HTTPStatusCode'] == 200

