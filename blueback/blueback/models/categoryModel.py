import boto3
import os
from datetime import datetime
from uuid import uuid4

DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table(DDB_TABLE_NAME)

def add_category(user_id, cat_name: str, cat_type: str, color = '', icon = str, children = [], parents = [], members = []) -> dict:
    dt = datetime.utcnow()
    item['PK'] = 'USER#{}'.format(user_id)
    item['SK'] = 'CAT#{cat_type}#{cat_name}'.format(cat_type = cat_type, cat_name = cat_name)
    item['Name'] = cat_name
    item['Type'] = cat_type
    if color: 
      item['Color'] = color
    if icon: 
      item['Icon'] = icon
    if children: 
      item['Children'] = children
    if parents: 
      item['Parents'] = parents
    if members: 
      item['Members'] = members

    r = ddb_table.put_item(
        Item=item
    )
    return {'Category Added': item['SK']}

def retrieve_all_categories(user_id: str) -> dict:
    '''Get user item in DDB'''
    print(DDB_TABLE_NAME)
    pk = 'USER#{}'.format(user_id)
    r = ddb_table.query(
        KeyConditionExpression= Key('PK'.eq(pk) & Key('SK').begins_with('CAT'))
    )
    item = r.get('Item', {})

    return item

def retrieve_categories_by_type(user_id: str, cat_type: str) -> dict:
    '''Get user item in DDB'''
    print(DDB_TABLE_NAME)
    pk = 'USER#{}'.format(user_id)
    sk = 'CAT#{cat_type}'.format(cat_type = cat_type)
    r = ddb_table.query(
        KeyConditionExpression= Key('PK'.eq(pk) & Key('SK').begins_with(sk))
    )
    item = r.get('Item', {})

    return item

def update_category(user_id: str, cat_name: str, cat_type: str) -> dict:
    item = request.get_json(force=True)
    attribute_updates = {}
    for key in item.keys():
        attribute_updates[key] = {'Action': 'PUT', 'Value': item.get(key)}

    r = ddb_table.update_item(
        Key={
            'PK': 'USER#{}'.format(user_id),
            'SK':  'CAT#{cat_type}#{cat_name}'.format(cat_type = cat_type, cat_name = cat_name)
        },
        AttributeUpdates=attribute_updates
    )
    return r 

def delete_category(user_id: str, cat_name: str, cat_type: str) -> dict:
    user_id = get_jwt_identity()
    '''Delete item in DDB'''
    r = ddb_table.delete_item(
        Key={
            'PK': 'USER#{}'.format(user_id),
            'SK':  'CAT#{cat_type}#{cat_name}'.format(cat_type = cat_type, cat_name = cat_name)
        },
    )
    return r
