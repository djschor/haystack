import boto3
import os
from decouple import config
import pickle
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')#os.chdir('/Users/dschorin/Documents/projects/PersonalFinance/BluechipAWSBackend/hayback')
# aws_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
# print(aws_key)
# %env AWS_SECRET_ACCESS_KEY='YNeRUHOeMb7PQoIbpFTjcJjjbsy8GYcFnoJBUGuZ'
# %env AWS_ACCESS_KEY_ID = 'AKIATK6G7UOGVX6QXWVQ'
import sys
print(sys.path)
from boto3.dynamodb.conditions import Key
import os
from datetime import datetime
from uuid import uuid4
import json
from hayback.models.accountModel import create_account, process_save_accounts, retrieve_account, retrieve_user_accounts, update_account, update_transactions, update_holdings, delete_account
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table('Bluechip')

def test_create_account(new_test_account):
  """
  GIVEN a User model
  WHEN a new User is created
  THEN check the email, hashed_password, and role fields are defined correctly
  """
  resp = create_account(new_test_account[0], new_test_account[1])
  print(resp)
  print('response: ', resp)
  assert resp['Response']['ResponseMetadata']['HTTPStatusCode'] == 200

def test_retrieve_account():
  email = "test@gmail.com"
  resp = retrieve_account(email, '123')
  print(resp)
  assert resp['pk'] == 'USER#test@gmail.com'
  assert resp['sk'] == 'ACC#123'

def test_update_account():
  email = "test@gmail.com"
  account_id = '123'
  item = {'transactions': [1, 2, 3], 'holdings': [1, 2, 3]}
  resp = update_account(email, account_id, item)
  print(resp)
  assert resp['ResponseMetadata']['HTTPStatusCode'] == 200

def test_update_transactions(transactions_test_obj):
  email = "test@gmail.com"
  account_id = '123'
  resp = update_transactions(email, account_id, transactions_test_obj['investment_transactions'])
  print(resp)
  assert resp['ResponseMetadata']['HTTPStatusCode'] == 200

def test_update_holdings(holdings_test_obj):
  email = "test@gmail.com"
  account_id = '123'
  resp = update_holdings(email, account_id, holdings_test_obj['holdings'])
  print(resp)
  assert resp['ResponseMetadata']['HTTPStatusCode'] == 200

def test_process_save_accounts(holdings_test_obj, transactions_test_obj):
  email = "test@gmail.com"
  resp = process_save_accounts(email, holdings_test_obj, transactions_test_obj)
  print(resp)
  assert isinstance(resp, list)
  assert len(resp) == 3

def test_retrieve_user_accounts():
  email = "test@gmail.com"
  resp = retrieve_user_accounts(email)
  print(resp)
  assert isinstance(resp, dict)

def test_delete_account():
  email = "test@gmail.com"
  resp = delete_account(email, '123')
  accounts = retrieve_user_accounts(email)
  print(resp)
  for acc in accounts['Items']:
    print('acc:\n', acc)
    r = delete_account(email, acc['account_id'])
    print(r)
    assert r['ResponseMetadata']['HTTPStatusCode'] == 200
  assert resp['ResponseMetadata']['HTTPStatusCode'] == 200

