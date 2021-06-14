import boto3
import os
from datetime import datetime
from uuid import uuid4
import json

DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table('Bluechip')

def create_user(email: str, first_name: str, last_name: str, password: str, phone: str) -> dict:
    '''Transform item to put into DDB'''
    dt = datetime.utcnow()
    item = {}
    item['pk'] = 'USER#{}'.format(email)
    item['sk'] = 'METADATA#{}'.format(email)
    item['first_name'] = first_name
    item['last_name'] = last_name
    item['email'] = email
    item['password'] = password
    item['phone_number'] = phone
    item['created_date'] = dt.strftime("%m/%d/%Y")
    if 'plan' not in item.keys():
        item['plan'] = 'premium'
    r = ddb_table.put_item(
        Item=item
    )
    return {'User Created': item['email'], 'Response': r}

def retrieve_user(email: str) -> dict:
    '''Get user item in DDB'''
    print(DDB_TABLE_NAME)

    r = ddb_table.get_item(
        Key={
            'pk': 'USER#{}'.format(email),
            'sk':  'METADATA#{}'.format(email)
        }
    )
    item = r.get('Item', {})

    return item

def scan_all_users() -> dict:
    '''Get all user items in DDB'''
    scan_kwargs = {
        'FilterExpression': Key('pk').begins_with('USER#') & Key('sk').begins_with('METADATA#') 
    }
    done = False
    start_key = None
    save_items = []
    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = ddb_table.scan(**scan_kwargs)
        print_stocks(response.get('Items', []))
        [save_items.append(x) for x in response.get('Items', [])]
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    return save_items
    

def update_user(email: str, item: dict) -> dict:
    # item = request.get_json(force=True)
    attribute_updates = {}
    for key in item.keys():
        attribute_updates[key] = {'Action': 'PUT', 'Value': item.get(key)}

    r = ddb_table.update_item(
        Key={
            'pk': 'USER#{}'.format(email),
            'sk':  'METADATA#{}'.format(email)
        },
        AttributeUpdates=attribute_updates
    )
    return r 

def delete_user(email: str) -> dict:
    # email = get_jwt_identity()
    '''Delete item in DDB'''
    r = ddb_table.delete_item(
        Key={
            'pk': 'USER#{}'.format(email),
            'sk':  'METADATA#{}'.format(email)
        },
    )
    return r

def get_role_permissions(role):
    if role == 'premium': 
        role_obj = create_premium_role()
    elif role == 'boss':
        role_obj = create_boss_role()
    elif role == 'free':
        role_obj = create_free_role()
    elif role == 'insider':
        role_obj = create_insider_role()
    else: 
        print('Error!\nRole requested does not exist: {}\n'.format(role))
        return 'Error! Role requested does not exist: {}\n'.format(role)
    return role_obj
        
def create_premium_role():
    dt = datetime.utcnow()
    role_object = {
        'id': 'premium',
        'name': 'premium user',
        'describe': 'premium user permissions',
        'status': 1,
        'creatorId': 'system',
        'createTime': dt.strftime("%m/%d/%Y"),
        'deleted': 0,
        'permissions': [{
        'roleId': 'admin',
        'permissionId': 'premium',
        'permissionName': 'premium',
        'actions': '[{"action":"add","defaultCheck":False,"describe":"Add"},{"action":"query","defaultCheck":False,"describe":"查询"},{"action":"get","defaultCheck":False,"describe":"详情"},{"action":"update","defaultCheck":False,"describe":"修改"},{"action":"delete","defaultCheck":False,"describe":"删除"}]',
        'actionEntitySet': [{
            'action': 'add',
            'describe': 'Add',
            'defaultCheck': False
        }, {
            'action': 'query',
            'describe': 'query',
            'defaultCheck': False
        }, {
            'action': 'get',
            'describe': 'get',
            'defaultCheck': False
        }, {
            'action': 'update',
            'describe': 'Update',
            'defaultCheck': False
        }, {
            'action': 'delete',
            'describe': 'Delete',
            'defaultCheck': False
        }],
        'actionList': None,
        'dataAccess': None
        }]
    }
    return role_object
        
def create_boss_role():
    dt = datetime.utcnow()
    role_object = {
        'id': 'boss',
        'name': 'god level boss privileges',
        'describe': 'with great power comes great responsibility',
        'status': 1,
        'creatorId': 'god',
        'createTime': dt.strftime("%m/%d/%Y"),
        'deleted': 0,
        'permissions': [{
        'roleId': 'boss',
        'permissionId': 'boss',
        'permissionName': 'boss',
        'actions': '[{"action":"add","defaultCheck":False,"describe":"Add"},{"action":"query","defaultCheck":False,"describe":"查询"},{"action":"get","defaultCheck":False,"describe":"详情"},{"action":"update","defaultCheck":False,"describe":"修改"},{"action":"delete","defaultCheck":False,"describe":"删除"}]',
        'actionEntitySet': [{
            'action': 'add',
            'describe': 'Add',
            'defaultCheck': False
        }, {
            'action': 'query',
            'describe': 'query',
            'defaultCheck': False
        }, {
            'action': 'get',
            'describe': 'get',
            'defaultCheck': False
        }, {
            'action': 'update',
            'describe': 'Update',
            'defaultCheck': False
        }, {
            'action': 'delete',
            'describe': 'Delete',
            'defaultCheck': False
        }]
        }]
    }
    return role_object
  
def create_free_role():
    dt = datetime.utcnow()
    role_object = {
        'id': 'free',
        'name': 'free user',
        'describe': 'free user on basic plan with limited access',
        'status': 1,
        'creatorId': 'system',
        'createTime': dt.strftime("%m/%d/%Y"),
        'deleted': 0,
        'permissions': [{
        'roleId': 'free',
        'permissionId': 'free',
        'permissionName': 'free',
        'actions': '[{"action":"add","defaultCheck":False,"describe":"Add"},{"action":"query","defaultCheck":False,"describe":"查询"},{"action":"get","defaultCheck":False,"describe":"详情"},{"action":"update","defaultCheck":False,"describe":"修改"},{"action":"delete","defaultCheck":False,"describe":"删除"}]',
        'actionEntitySet': [{
            'action': 'add',
            'describe': 'Add',
            'defaultCheck': False
        }, {
            'action': 'query',
            'describe': 'query',
            'defaultCheck': False
        }, {
            'action': 'get',
            'describe': 'get',
            'defaultCheck': False
        }, {
            'action': 'update',
            'describe': 'Update',
            'defaultCheck': False
        }, {
            'action': 'delete',
            'describe': 'Delete',
            'defaultCheck': False
        }]
        }]
    }
    return role_object
  

def create_insider_role():
    dt = datetime.utcnow()
    role_object = {
        'id': 'insider',
        'name': 'insider user',
        'describe': 'top tier coveted insider dedicated to the gains',
        'status': 1,
        'creatorId': 'system',
        'createTime': dt.strftime("%m/%d/%Y"),
        'deleted': 0,
        'permissions': [{
        'roleId': 'insider',
        'permissionId': 'insider',
        'permissionName': 'insider',
        'actions': '[{"action":"add","defaultCheck":False,"describe":"Add"},{"action":"query","defaultCheck":False,"describe":"查询"},{"action":"get","defaultCheck":False,"describe":"详情"},{"action":"update","defaultCheck":False,"describe":"修改"},{"action":"delete","defaultCheck":False,"describe":"删除"}]',
        'actionEntitySet': [{
            'action': 'add',
            'describe': 'Add',
            'defaultCheck': False
        }, {
            'action': 'query',
            'describe': 'query',
            'defaultCheck': False
        }, {
            'action': 'get',
            'describe': 'get',
            'defaultCheck': False
        }, {
            'action': 'update',
            'describe': 'Update',
            'defaultCheck': False
        }, {
            'action': 'delete',
            'describe': 'Delete',
            'defaultCheck': False
        }]
        }]
    }
    return role_object