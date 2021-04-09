import boto3
import os
from decouple import config

# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')#os.chdir('/Users/dschorin/Documents/projects/PersonalFinance/CacheAWSBackend/cacheback')
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

#from .models.accountModel import create_account, create_institution
#from ..models import accountModel

# DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table('Cache')

def test_create_account() -> dict:
  email = "test@gmail.com"
  account_id = "123"
  account_name = "testAcc"
  acount_type = "credit"
  account_subtype = ""
  ins_name = "testIns"
  balances = ""
  transactions = ""
  resp = create_account(email, account_id, account_name, account_type, account_subtype, ins_name, balances, transactions)
  print('response: ', resp)
  assert isinstance(resp, dict)
