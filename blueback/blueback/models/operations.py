import boto3
import os
from datetime import datetime
from uuid import uuid4
from .accountModel import update_account, retrieve_account
from collections import OrderedDict

# DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table('Cache')

def set_plaid_account_cred(email, account_name, account_type, access_token, item_id): 
    # saves most recent update date to dynamo 
    item = {'Access_Token': access_token, 'Item_ID': item_id}

    return update_account(email, account_name, account_type, item)


def set_update_date(email, account_name, account_type, update_date): 
    # saves most recent update date to dynamo 
    item = {'Last_Updated': update_date}
    return update_account(email, account_name, account_type, item)

def get_update_date(account_item): 
    if 'Last_Updated' in account_item: 
      return account_item['Last_Updated']
    else: 
      return '1/1/2000, 00:00:00'

def set_transactions(email, account_name, account_type, transactions_item): 
    # saves most recent transactions to dynamo 
    # TODO: ensure only setting dates not in db 

    item = {'Transactions': transactions_item}
    return update_account(email, account_name, account_type, item)

def get_expense_transactions(account_item): 
    # returns most recent expense transactions from dynamo 
    if 'Transactions' in account_item: 
        if 'Expenses' in account_item:
            return account_item['Transactions']['Expenses']
        else: 
          return 'No Expenses in Transactions in User Account'
    else: 
        return 'No Transactions Error'

def get_income_transactions(): 
    return account_item['Transactions']['Income']

def set_balance(email, account_name, account_type, account_item, balance):
    date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    balance_dict = get_balances(account_item) 
    # saves balance from plaid to dynamo 
    balance_dict[date] = balance
    item = {'Balances': transactions_item}
    return update_account(email, account_name, account_type, item)

def get_balances(account_item): 
    # returns all balances associated with account
    # balances are a dictionary where the key is the update date and the value is the balance
    if "Balance" in account_item:
        return account_item['Balances']
    else: 
        return 'No Balances'
  
def get_recent_balance(account_item): 
    # sorts balance dictionary by converting the date string to datetime in '%m/%d/%Y' format
    # returns most recent balance
    if "Balance" in account_item:
        recent_balance = OrderedDict(sorted(account_item['Balances'].items(), key=lambda t: datetime.strptime(t[0], '%m/%d/%Y, %H:%M:%S'), reverse=True))
        return recent_balance
    else: 
        return 'No Balances'
     