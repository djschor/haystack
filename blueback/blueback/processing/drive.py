import pandas as pd
import numpy as np 
pd.options.mode.chained_assignment = None  # default='warn'
from datetime import datetime
import time
from cacheback.models.operations import get_update_date #, set
from .clean import clean_transactions
from cacheback.resources.plaid.backend import get_transactions, get_balance
from cacheback.models.accountModel import retrieve_account, retrieve_accounts_by_type
import boto3 
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table('Cache')

def main(): 
    account = retrieve_account(1, 'TCF', 'Bank')
    pulled_update_resp = pull_update_transactions(account)
    return get_expense_transactions(account)

def pull_update_transactions(account_item): 
    '''
    0. get most recent pull date
    1. pull transactions after that date
    2. clean transactions 
    3. update transactions 
    '''
    email = account_item['PK'].split('#')[-1]
    acc_name = account_item['Name']
    acc_type = account_item['Type']
    last_update = get_update_date(account_item)
    transactions = get_transactions()
    cleaned_transactions = clean_transactions(transactions, 'plaid')
    save_transactions = set_transactions(email, acc_name, acc_type, cleaned_transactions)
    return save_transactions

def pull_update_balance(account_name, account_type): 
    pass

'''
export_graph_data
 1. find out which accounts to grab expenses from 
 2. grab expenses from dynamo
 2. turn into datafrmae 
 3. get all (relevant?) outputs from graphs 
 4. return object containing graph info
'''
def export_graph_data(email): 
    pass

'''
def find_expense_accounts
1. list expense account types
2. for each account: 
  - retrieve the account 
  - put it into a data frame
  - assign column value 'ACCOUNT' and 'Account Type' 
  - put df into list
  - concat dfs 
'''
def expense_accounts_to_df(email):
    df_list = []
    exp_acc_types = ['BANK', 'CREDITCARD', 'PAYPAL', 'VENMO']
    for acc_type in exp_acc_types: 
      accounts_set = retrieve_accounts_by_type(email, acc_type)
      for acc in json.loads(accounts_set['Items']):
        expenses = acc['Transactions']['Expenses']
        exp_df = pd.json_normalize(expenses)
        exp_df = exp_df[['amount', 'date', 'merchant_name', 'transaction_description', 'transaction_id', 'transaction_type', 'primary_category',	'secondary_category']]
        df_list.append(exp_df)
    expenses_comb = pd.concat(df_list)
    return expenses_comb