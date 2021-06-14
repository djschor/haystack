from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
import boto3
import os
from datetime import datetime
from uuid import uuid4
from hayback.models.accountModel import create_account, retrieve_account, update_account, update_holdings, update_transactions, process_save_accounts, delete_account, retrieve_user_accounts
import logging
from .plaid.backend import get_transactions, get_holdings, get_link_token, get_access_token
import json
from decimal import Decimal
import pickle
DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table('Bluechip')

class AccountApi(Resource):
    '''
    Post: create account
    1. get user identity
    2. exchange public token for access token 
    2. save item_id and account access_token
    3. pull transactions, balance
    4. Get account type from transactions
    5. save account
    '''
    @jwt_required
    def post(self): 
        current_user = get_jwt_identity()
        body = request.get_json()
        print('cur user', current_user)
        source = body['source']
        if source == 'plaid':
            public_token = body['public_token']
            account_id = body['institution']['account_id']
            #account_name = body['institution']['name']
            # retrieve institution 
            acc = retrieve_account(current_user, account_id)
            print('acc', acc)
            # if the account is already in the db
            if isinstance(acc, dict) and ('Date_Added' in acc.keys()):
                print('Institution already in db')
                access_token = acc['access_token']
                trans_resp = get_transactions(access_token)
                update_trans = update_transactions(current_user, account_id, trans_resp['investment_transactions'])
                print('updated transactions resp:\n', update_trans)
                hold_resp = get_holdings(access_token)
                update_hold = update_holdings(current_user, account_id, hold_resp['holdings'])
                print('updated holdings resp:\n', update_hold)
                acc = retrieve_account(current_user, account_id)
                return acc, 200
            # if the institution isn't in db
            else:
                # exchange public token for access token 
                l = get_access_token(public_token)
                print('Access token response: ', l)
                access_token, item_id = get_access_token(public_token)
                print(access_token)
                print('PUBTOKEN: ', public_token)
                print('access token: ', access_token, '\nitem_id: ', item_id)
                # save institution to DB
                trans_resp = get_transactions(access_token)
                hold_resp = get_holdings(access_token)
                save_accounts_resp = process_save_accounts(current_user, hold_resp, trans_resp)
            return save_accounts_resp, 200
        else: 
            return 'Not source plaid', 400

    # def put(self, user_id, account_name, account_type):
    #     # get transactions from plaid 
    #     # clean transactions 
    #     # trans = get_transactions()
    #     # clean_trans = clean_transactions(trans, 'plaid')
    #     # accountModel.update_account(user_id, account_name, account_type, {'Transactions': clean_trans})
    #     x = get_link_token(1) #main()
    #     response = {'success': True}
    #     status_code = 200
    #     return x        
    
    def delete(self, email, account_id):
          '''Delete message'''
          r_delete = delete_account(email, account_id)
          status_code = 200
          return r_delete, status_code

    def get(self, email, account_id):
        '''Retrieve message'''
        # app.logger.info(userModel.isThereAShit())
        user_item = retrieve_account(email, account_id)
        return user_item, 200
        #return Response(user_item, mimetype="application/json", status=status_code)

class AccountsApi(Resource):
#@jwt_required
    def get(self, email): 
        user_accounts = retrieve_user_accounts(email)
        return user_accounts, 200