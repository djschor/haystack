from flask import Response, request, jsonify
# from database.models import User, Account, Primary_Categories, Categories
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
import boto3
import os
from datetime import datetime
from uuid import uuid4
#import models
from hayback.models import userModel
import logging

# DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table('Bluechip')

class UsersApi(Resource):    
    def get(self):
        all_users = userModel.scan_all_users()
        return all_users, 200

class UserApi(Resource):
# shows a single user item and lets you delete a todo item
    @jwt_required
    def put(self):
        email = get_jwt_identity()
        item = {} #request.get_json(force=True)
        userModel.update_user(email, item)
        response = {'success': True}
        status_code = 200
        return response, status_code        
        
    @jwt_required
    def delete(self):
        email = get_jwt_identity()
        userModel.delete_user(email)
        response = {'success': True}
        status_code = 200
        return response, status_code
    
    @jwt_required
    def get(self):
        print('in get')
        email = get_jwt_identity()
        print('email')
        user_item = userModel.retrieve_user(email)
        role_obj = userModel.get_role_permissions(user_item['plan'])
        user_item['role'] = role_obj
        status_code = 200
        return user_item

class CreateUserApi(Resource):
    # @jwt_required
    def post(self): # remember to add inputs from the response
        '''Transform item to put into DDB'''
        # try:
        #item = request.get_json(force=True)
        user_item = request.get_json()
        new_user_response = userModel.create_user(user_item['email'], user_item['first_name'], user_item['last_name'], user_item['password'], user_item['phone_number'])
        status_code = 200
        return new_user_response, status_code