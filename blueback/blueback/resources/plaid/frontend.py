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
from .backend import get_link_token, get_access_token
from cacheback.models.operations import set_plaid_account_cred
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


class AccessToken(Resource):
# returns the link token for the user
    def get(self, email, account_type, account_name):
        '''Retrieve message'''
        # app.logger.info(userModel.isThereAShit())
        access_token = request.get_json()
        print(access_token)
        status_code = 200
        return {'': str(id)}, 200
        #return Response(user_item, mimetype="application/json", status=status_code)

class PublicToken(Resource):
# returns the link token for the user
    def post(self):
        '''Retrieve message'''
        # app.logger.info(userModel.isThereAShit())
        public_token = request.get_json()
        print(public_token)
        access_token, item_id = get_access_token(public_token['public_token'])
        save_items = set_plaid_account_cred(1, 'Robinhood', 'Invest', access_token, item_id)
        print(access_token)
        status_code = 200
        return {'': str(1), 'response': save_items}, 200
        #return Response(user_item, mimetype="application/json", status=status_code)

class LinkToken(Resource):
# returns the link token for the user
    def get(self, email, account_type, account_name):
        '''Retrieve message'''
        # app.logger.info(userModel.isThereAShit())
        link_token = get_link_token(email)
        status_code = 200
        return user_item
        #return Response(user_item, mimetype="application/json", status=status_code)

