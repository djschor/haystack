from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
import boto3
import os
from datetime import datetime
from uuid import uuid4
from cacheback.models.accountModel import retrieve_institution, create_institution, create_account, retrieve_instution_accounts_object, retrieve_account, update_account
import logging
from cacheback.processing.clean import clean_transactions, input_transactions_to_df
from .plaid.backend import get_transactions, get_link_token, get_access_token
from cacheback.processing.drive import main 
import json
from decimal import Decimal
import pickle
DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table('Cache')

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
        created_responses = []
        if source == 'plaid':
            public_token = body['public_token']
            ins_id = body['institution']['institution_id']
            ins_name = body['institution']['name']
            # retrieve institution 
            inst = retrieve_institution(current_user, ins_id)
            print('inst', inst)
            # if the institution is already in the db
            if isinstance(inst, dict) and ('Date_Added' in inst.keys()):
                print('Institution already in db')
                item_id = inst['Item_Id']
                # get transactions (todo: later add mechanism to check for recency of last pull, to mininimize unneccessary plaid api calls)
                access_token = inst['Access_Token']
                last_updated = inst['Last_Updated']
                # try to use saved item id ad access token to get transactions
                try:
                    trans_resp = get_transactions(access_token, item_id)
                    print(trans_resp)
                    num_accounts = len(trans_resp['accounts'])
                    print('num_accounts: ', num_accounts)
                    ins_transactions = trans_resp['transactions']
                    trans_df = input_transactions_to_df(ins_transactions, 'plaid')
                # if that doesn't work, use link to get new access token and item id
                except: 
                    print('exception occurred, getting new access token')
                    access_token, item_id = get_access_token(public_token)
                    print(access_token)
                    print('PUBTOKEN: ', public_token)
                    print('access token: ', access_token, '\nitem_id: ', item_id)
                    item = {"Access_Token": access_token, 
                            "Item_Id": item_id
                            }
                    # update institution info in DB
                    update_ins = update_institution(current_user, ins_id, item)
                    print("Updated Institution Access Id and Item ID", update_ins)
                    # get transactions and convert to df 
                    trans_resp = get_transactions(access_token, item_id)
                    num_accounts = len(trans_resp['accounts'])
                    ins_transactions = trans_resp['transactions']
                    trans_df = input_transactions_to_df(ins_transactions, 'plaid')
                    
                # if there's only 1 account associated with institution, check if the account is saved and then return
                if num_accounts == 1: 
                    acc_name = trans_resp['accounts'][0]['official_name']
                    acc_type = trans_resp['accounts'][0]['type']
                    acc_subtype = trans_resp['accounts'][0]['subtype']
                    acc_id = trans_resp['accounts'][0]['account_id']

                    balances = trans_resp['accounts'][0]['balances']
                    balances['current'] = str(balances['current'])
                    dt = datetime.utcnow()
                    balances['date'] = dt.strftime("%m/%d/%Y")
                    acc_trans = trans_df[trans_df['account_id'] == acc_id]
                    cleaned_trans = clean_transactions(acc_trans, source)
                    print('cleaned_transactions')
                    # see if account is already saved in db
                    acc = retrieve_account(current_user, ins_name, acc_type, acc_id)
                    if isinstance(acc, dict) and ('Date_Added' in acc.keys()):
                        # if already in db, update acc transactions
                        update_item = {'Transactions': json.dumps(cleaned_trans)}
                        update_resp = update_account(current_user, acc_name, acc_type, update_item)
                    else: 
                        # if not in db, add to db and save response to created responses
                        account_creation = create_account(current_user, acc_id, acc_name, acc_type, acc_subtype, ins_name, balances, cleaned_trans)
                        created_responses.append(account_creation)
                # if more than 1 account
                else: 
                    # if there's more than 1 account, iterate through them, check if in db
                     for acc in trans_resp['accounts']:
                        # if "official_name" in acc.keys():
                        acc_name = acc['official_name']
                        acc_type = acc['type']
                        acc_subtype = acc['subtype']
                        acc_id = acc['account_id']

                        balances = acc['balances']
                        balances['current'] = str(balances['current'])
                        dt = datetime.utcnow()
                        balances['date'] = dt.strftime("%m/%d/%Y")
                        acc_trans = trans_df[trans_df['account_id'] == acc_id]
                        cleaned_trans = clean_transactions(acc_trans, source)
                        
                        # see if account is already saved in db
                        acc = retrieve_account(current_user, ins_name, acc_type, acc_id)
                        if isinstance(acc, dict) and ('Date_Added' in acc.keys()):
                            # if already in db, update acc transactions
                            update_item = {'Transactions': json.dumps(cleaned_trans)}
                            update_resp = update_account(current_user, acc_name, acc_type, update_item)
                        else: 
                        # if not in db, add to db and save response to created responses
                            account_creation = create_account(current_user, acc_id, acc_name, acc_type, acc_subtype, ins_name, balances, cleaned_trans)
                            created_responses.append(account_creation)   
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
                create_ins = create_institution(current_user, ins_name, ins_id, item_id, access_token)
            
                # get transactions and convert to df 
                trans_resp = get_transactions(access_token, item_id)
                num_accounts = len(trans_resp['accounts'])
                ins_transactions = trans_resp['transactions']
                trans_df = input_transactions_to_df(ins_transactions, 'plaid')
                
                if num_accounts == 1: 
                    acc_name = trans_resp['accounts'][0]['official_name']
                    acc_type = trans_resp['accounts'][0]['type']
                    acc_subtype = trans_resp['accounts'][0]['subtype']
                    acc_id = trans_resp['accounts'][0]['account_id']

                    balances = trans_resp['accounts'][0]['balances']
                    balances['current'] = str(balances['current'])
                    dt = datetime.utcnow()
                    balances['date'] = dt.strftime("%m/%d/%Y")
                    acc_trans = trans_df[trans_df['account_id'] == acc_id]
                    cleaned_trans = clean_transactions(acc_trans, source)
                    print('cleaned_transactions')
                    # see if account is already saved in db
                    acc = retrieve_account(current_user, ins_name, acc_type, acc_id)
                    if isinstance(acc, dict) and ('Date_Added' in acc.keys()):
                        # if already in db, update acc transactions
                        update_item = {'Transactions': json.dumps(cleaned_trans)}
                        update_resp = update_account(email, acc_name, acc_type, update_item)
                        print('Updated Item: ', update_resp)
                    else: 
                        # if not in db, add to db and save response to created responses
                        account_creation = create_account(current_user, acc_id, acc_name, acc_type, acc_subtype, ins_name, balances, cleaned_trans)
                        created_responses.append(account_creation)
                # if more than 1 account
                else: 
                    # if there's more than 1 account, iterate through them, check if in db
                     for acc in trans_resp['accounts']:
                        # if "official_name" in acc.keys():
                        acc_name = acc['official_name']
                        acc_type = acc['type']
                        acc_subtype = acc['subtype']
                        acc_id = acc['account_id']

                        balances = acc['balances']
                        balances['current'] = str(balances['current'])
                        dt = datetime.utcnow()
                        balances['date'] = dt.strftime("%m/%d/%Y")
                        acc_trans = trans_df[trans_df['account_id'] == acc_id]
                        cleaned_trans = clean_transactions(acc_trans, source)
                        
                        # see if account is already saved in db
                        acc = retrieve_account(current_user, ins_name, acc_type, acc_id)
                        if isinstance(acc, dict) and ('Date_Added' in acc.keys()):
                            # if already in db, update acc transactions
                            update_item = {'Transactions': json.dumps(cleaned_trans)}
                            update_resp = update_account(email, acc_name, acc_type, update_item)
                        else: 
                        # if not in db, add to db and save response to created responses
                            account_creation = create_account(current_user, acc_id, acc_name, acc_type, acc_subtype, ins_name, balances, json.dumps(cleaned_trans))
                            created_responses.append(account_creation) 
            ins_obj = retrieve_instution_accounts_object(current_user, ins_name)
            print('ins_pbj: ', ins_obj)#, created_responses)
            # get account data for the account
            response = {
                'success': True,
                'message': created_responses
            }
            status_code = 200

            return ins_obj, status_code
        else: 
            return 'Not source plaid'

    def put(self, user_id, account_name, account_type):
        # get transactions from plaid 
        # clean transactions 
        # trans = get_transactions()
        # clean_trans = clean_transactions(trans, 'plaid')
        # accountModel.update_account(user_id, account_name, account_type, {'Transactions': clean_trans})
        x = get_link_token(1) #main()
        response = {'success': True}
        status_code = 200
        return x        
        # try:
        #     '''Update message'''
            
        # except:
        #     return "idk"

    def delete(self, user_id):
        try:
          '''Delete message'''
          accountModel.delete_account(user_id)
          response = {'success': True}
          status_code = 200
          return jsonify(response), status_code

        except DoesNotExist:
            raise DeletingMovieError
        except Exception:
            raise InternalServerError

    def get(self, user_id, account_type, account_name):
        '''Retrieve message'''
        # app.logger.info(userModel.isThereAShit())
        user_item = accountModel.retrieve_account(user_id, account_name, account_type)
        status_code = 200
        return user_item
        #return Response(user_item, mimetype="application/json", status=status_code)
