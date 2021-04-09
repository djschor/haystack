from flask import Response, request, jsonify
# from database.models import User, Account, Primary_Categories, Categories
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
import boto3
import os
from datetime import datetime
from uuid import uuid4
#import models
from cacheback.models import userModel
import logging

DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table(DDB_TABLE_NAME)

class UsersApi(Resource):
# shows a list of all users, and lets you POST to add new useres
    # def get(self):
        
    #     r = ddb_table.get_item(
    #         Key={
    #             'UserID': email,
    #         }
    #     )
    #     user_item = r.get('Item', {})
    #     return Response(user_item, mimetype="application/json", status=200)

    @jwt_required
    def post(self): # remember to add inputs from the response
        '''Transform item to put into DDB'''
        # try:
        #item = request.get_json(force=True)
        email = userModel.create_user({})
        response = {
            'success': True,
            'message': email
        }
        status_code = 200
        return email, status_code

            # item = {}
            # dt = datetime.utcnow()
            # item['UserID'] = '3'
            # item['Username'] = 'kschor'
            # item['Name'] = 'Mama Schorin'
            # item['Password'] = 'snappybart'
            # item['Email'] = 'kschorin@comcast.net'
            # r = ddb_table.put_item(
            #     Item=item
            # )
            # return {'email': item['UserID']}, 200
            
        # except Exception as e:
        #     raise InternalServerError


class UserApi(Resource):
# shows a single user item and lets you delete a todo item

    # @jwt_required
    def put(self, email):
        '''Update message'''
        item = {} #request.get_json(force=True)
        userModel.update_user(email, item)
        response = {'success': True}
        status_code = 200
        return (response), status_code        
        
    
    # @jwt_required
    def delete(self, email):
        '''Delete message'''
        userModel.delete_user(email)
        response = {'success': True}
        status_code = 200
        return response, status_code

    def get(self, email):
        '''Retrieve message'''
        user_item = userModel.retrieve_user(email)
        status_code = 200
        return user_item
        #return Response(user_item, mimetype="application/json", status=status_code)
