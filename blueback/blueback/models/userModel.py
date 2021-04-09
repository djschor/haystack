import boto3
import os
from datetime import datetime
from uuid import uuid4

DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table('Cache')

def create_user(email: str, first_name: str, last_name: str, password: str, phone: str) -> dict:
    '''Transform item to put into DDB'''
    dt = datetime.utcnow()
    item = {}
    item['PK'] = 'USER#{}'.format(email)
    item['SK'] = '#METADATA#{}'.format(email)
    item['FirstName'] = first_name
    item['LastName'] = last_name
    item['Email'] = email
    item['UserID'] = email
    item['Password'] = password
    item['PhoneNumber'] = phone
    r = ddb_table.put_item(
        Item=item
    )
    return {'email': item['Email']}

def retrieve_user(email: str) -> dict:
    '''Get user item in DDB'''
    print(DDB_TABLE_NAME)

    r = ddb_table.get_item(
        Key={
            'PK': 'USER#{}'.format(email),
            'SK':  '#METADATA#{}'.format(email)
        }
    )
    item = r.get('Item', {})

    return item

# def retrieve_users(email: str) -> dict:
#     '''Get user item in DDB'''
#     r = ddb_table.get_item(
#         Key={
#             'UserID': email,
#         }
#     )
#     item = r.get('Item', {})

#     return item

def update_user(email: str, item: dict) -> dict:
    item = request.get_json(force=True)
    attribute_updates = {}
    for key in item.keys():
        attribute_updates[key] = {'Action': 'PUT', 'Value': item.get(key)}

    r = ddb_table.update_item(
        Key={
            'PK': 'USER#{}'.format(email),
            'SK':  'ACCOUNT#{account_type}#{account_name}'.format(account_type = account_type, account_name=account_name)
        },
        AttributeUpdates=attribute_updates
    )
    return r 

def delete_user(email: str) -> dict:
    # email = get_jwt_identity()
    '''Delete item in DDB'''
    r = ddb_table.delete_item(
        Key={
            'PK': 'USER#{}'.format(email),
            'SK':  '#METADATA#{}'.format(email)
        },
    )
    return r
