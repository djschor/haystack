from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
import boto3
import os
from datetime import datetime, date, time, timedelta
from uuid import uuid4
import json
#import models
#from models import accountModel
import logging
import plaid

DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table(DDB_TABLE_NAME)

PLAID_CLIENT_ID = os.environ.get('PLAID_CLIENT_ID')
PLAID_SECRET = os.environ.get('PLAID_SECRET')
PLAID_PUBLIC_KEY = os.environ.get('PLAID_PUBLIC_KEY')
PLAID_ENV = os.environ.get('PLAID_ENV')

access_token = 'access-development-ee08d166-0503-4446-9b40-2738815298b9'
item_id = '13mEnz6nXjtg0wNqL31LIbbKLvEn7XCnNBnyL'

# PLAID_PRODUCTS is a comma-separated list of products to use when initializing
# Link. Note that this list must contain 'assets' in order for the app to be
# able to create and retrieve asset reports.
PLAID_PRODUCTS = os.environ.get('PLAID_PRODUCTS', 'transactions')
PLAID_COUNTRY_CODES = os.getenv('PLAID_COUNTRY_CODES', 'US,CA,GB,FR,ES,IE,NL')

client = plaid.Client(client_id = PLAID_CLIENT_ID, secret=PLAID_SECRET,
                      environment=PLAID_ENV, api_version='2019-05-29')


def get_transactions(access_token, item_id, start_date = '2017-09-29', end_date = '{:%Y-%m-%d}'.format(datetime.now())): 
    try:
      transactions_response = client.Transactions.get(access_token, start_date, end_date)
    except plaid.errors.PlaidError as e:
      return e
    pretty_print_response(transactions_response)
    return transactions_response

def get_balance():
    try:
      balance_response = client.Accounts.balance.get(access_token)
    except plaid.errors.PlaidError as e:
      return {'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type } }
    pretty_print_response(balance_response)
    return balance_response

def pretty_print_response(response):
  print(json.dumps(response, indent=2, sort_keys=True))


# def dynamo_expenses_to_df(mongo_account_data): 
    # home = transactions['transactions']
  # return home
def format_error(e):
  return {'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type, 'error_message': e.message } }
import plaid

def get_link_token(email):
    # Get the client_user_id by searching for the current user
    # Create a link_token for the given user
    response = client.LinkToken.create({
      'user': {
        'client_user_id': str(email),
      },
      'products': ['transactions'],
      'client_name': 'Cashboard',
      'country_codes': ['US'],
      'language': 'en',
      'webhook': 'http://localhost:8001/home',
    })
    link_token = response['link_token']
    # Send the data to the client
    return link_token

def get_access_token(public_token):
  try:
    exchange_response = client.Item.public_token.exchange(public_token)
  except plaid.errors.PlaidError as e:
    return jsonify(format_error(e))

  pretty_print_response(exchange_response)
  access_token = exchange_response['access_token']
  item_id = exchange_response['item_id']
  print("ACC TOKEN AND ITEM ID IN BACKEND: ", access_token, item_id)
  return access_token, item_id
