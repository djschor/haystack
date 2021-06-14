import boto3
import os
from datetime import datetime
from uuid import uuid4
from hayback.models.accountModel import update_account, retrieve_account
from collections import OrderedDict

# DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table('Bluechip')

def set_plaid_account_cred(email, account_id, access_token, item_id): 
    # saves most recent update date to dynamo 
    item = {'Access_Token': access_token, 'Item_ID': item_id}

    return update_account(email, account_id, item)


def set_update_date(email, account_id, update_date): 
    # saves most recent update date to dynamo 
    item = {'Last_Updated': update_date}
    return update_account(email, account_id, item)

def get_update_date(account_item): 
    if 'Last_Updated' in account_item: 
      return account_item['Last_Updated']
    else: 
      return '1/1/2000, 00:00:00'