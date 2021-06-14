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

# class FakeChartData(Resource):
#     def get(self):
#   'GET  /api/fake_chart_data': {
#     visitData,
#     visitData2,
#     salesData,
#     searchData,
#     offlineData,
#     offlineChartData,
#     salesTypeData,
#     salesTypeDataOnline,
#     salesTypeDataOffline,
#     radarData,
#   },

class CurrentUser(Resource):
    def get(self):
      curUserDict = {
        'name':'Serati Ma',
        'avatar':'https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png',
        'userid': '00000001',
        'email':'antdesign@alipay.com',
        'signature':'Inclusive of all rivers, tolerance is great',
        'title':'Interaction Expert',
        'group':'Ant Group-XX Business Group-XX Platform Department-XX Technology Department-UED',
        'tags': [
          {
            'key': '0',
            'label':'Very thoughtful',
          },
          {
            'key': '1',
            'label':'Focus on design',
          },
          {
            'key': '2',
            'label':'Spicy~',
          },
          {
            'key': '3',
            'label':'Long legs',
          },
          {
            'key': '4',
            'label':'Chuanmeizi',
          },
          {
            'key': '5',
            'label':'Inclusive of all rivers',
          },
        ],
        'notifyCount': 12,
        'unreadCount': 11,
        'country':'China',
        'geographic': {
          'province': {
            'label':'Zhejiang',
            'key': '330000',
          },
          'city': {
            'label':'Hangzhou City',
            'key': '330100',
          },
        },
        'address': '77 Gongzhuan Road, Xihu District',
        'phone': '0752-268888888',
      }
      return curUserDict

class AntUsers(Resource):
    def get(self): 
        usersList = [{
          'key': '1',
          'name': 'John Brown',
          'age': 32,
          'address': 'New York No. 1 Lake Park',
        },
        {
          'key': '2',
          'name': 'Jim Green',
          'age': 42,
          'address': 'London No. 1 Lake Park',
        },
        {
          'key': '3',
          'name': 'Joe Black',
          'age': 32,
          'address': 'Sidney No. 1 Lake Park'}]
        return usersList

class Error500(Resource):
    def get(self):
        return {
          'timestamp': 1513932555104,
          'status': 500,
          'error': 'error',
          'message': 'error',
          'path': '/base/category/list',
        }

class Error404(Resource):
    def get(self):
        return {
          'timestamp': 1513932643431,
          'status': 404,
          'error': 'Not Found',
          'message': 'No message available',
          'path': '/base/category/list/2121212',
        }
class Error403(Resource):
    def get(self):
        return {
          'timestamp': 1513932555104,
          'status': 403,
          'error': 'Unauthorized',
          'message': 'Unauthorized',
          'path': '/base/category/list',
        }

class Error401(Resource):
    def get(self):
        return {
          'timestamp': 1513932555104,
          'status': 401,
          'error': 'Unauthorized',
          'message': 'Unauthorized',
          'path': '/base/category/list',
        }

class Captcha(Resource):
    def get(self):
        return 'captcha-xxx'

class Notices(Resource):
    def get(self):
        return [
    {
      'id': '000000001',
      'avatar':'https://gw.alipayobjects.com/zos/rmsportal/ThXAXghbEsBCCSDihZxY.png',
      'title':'You have received 14 new weekly reports',
      'datetime': '2017-08-09',
      'type':'notification',
    },
    {
      'id': '000000002',
      'avatar':'https://gw.alipayobjects.com/zos/rmsportal/OKJXDXrmkNshAMvwtvhu.png',
      'title':'Qu Nini you recommended has passed the third round of interview',
      'datetime': '2017-08-08',
      'type':'notification',
    },
    {
      'id': '000000003',
      'avatar':'https://gw.alipayobjects.com/zos/rmsportal/kISTdvpyTAhtGxpovNWd.png',
      'title':'This template can distinguish multiple notification types',
      'datetime': '2017-08-07',
      'read': True,
      'type':'notification',
    },
    {
      'id': '000000004',
      'avatar':'https://gw.alipayobjects.com/zos/rmsportal/GvqBnKhFgObvnSGkDsje.png',
      'title':'The icon on the left is used to distinguish different types',
      'datetime': '2017-08-07',
      'type':'notification',
    },
    {
      'id': '000000005',
      'avatar':'https://gw.alipayobjects.com/zos/rmsportal/ThXAXghbEsBCCSDihZxY.png',
      'title':'The content should not exceed two lines, and it will be truncated when it exceeds',
      'datetime': '2017-08-07',
      'type':'notification',
    },
    {
      'id': '000000006',
      'avatar':'https://gw.alipayobjects.com/zos/rmsportal/fcHMVNCjPOsbUGdEduuv.jpeg',
      'title':'Qu Lili commented on you',
      'description':'Description information description information description information',
      'datetime': '2017-08-07',
      'type':'message',
      'clickClose': True,
    },
    {
      'id': '000000007',
      'avatar':'https://gw.alipayobjects.com/zos/rmsportal/fcHMVNCjPOsbUGdEduuv.jpeg',
      'title':'Zhu Pianyou replied to you',
      'description':'This template is used to remind who has interacted with you, put the avatar of "who" on the left side',
      'datetime': '2017-08-07',
      'type':'message',
      'clickClose': True,
    },
    {
      'id': '000000008',
      'avatar':'https://gw.alipayobjects.com/zos/rmsportal/fcHMVNCjPOsbUGdEduuv.jpeg',
      'title':'Title',
      'description':'This template is used to remind who has interacted with you, put the avatar of "who" on the left side',
      'datetime': '2017-08-07',
      'type':'message',
      'clickClose': True,
    },
    {
      'id': '000000009',
      'title':'Task name',
      'description':'The task needs to be started before 20:00 on 2017-01-12',
      'extra':'Not started',
      'status':'todo',
      'type':'event',
    },
    {
      'id': '000000010',
      'title':'Third-party emergency code changes',
      'description':'Guanlin submitted on 2017-01-06, the code change task must be completed before 2017-01-07',
      'extra':'Expires soon',
      'status':'urgent',
      'type':'event',
    },
    {
      'id': '000000011',
      'title':'Information Security Examination',
      'description':'Assign Zhuer to complete the update and release before 2017-01-09',
      'extra':'Elapsed 8 days',
      'status':'doing',
      'type':'event',
    },
    {
      'id': '000000012',
      'title':'ABCD version release',
      'description':'Guanlin submitted on 2017-01-06, the code change task must be completed before 2017-01-07',
      'extra':'In progress',
      'status':'processing',
      'type':'event',
    },
  ]