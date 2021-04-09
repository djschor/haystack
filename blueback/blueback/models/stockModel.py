import boto3
from boto3.dynamodb.conditions import Key
import os
from datetime import datetime
from uuid import uuid4
import json
# DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table('Cache')

def create_stock(stock) -> dict:
    item = {}
    item['pk'] = stock['pk']
    item['sk'] = stock['sk']
    item.update({k:json.dumps(v) for (k, v) in stock.items() if k not in ('pk', 'sk')})
    r = ddb_table.put_item(
        Item=item
    )
    return {'Stock Created': item['sk'], 'Response': r}

def create_industry(email, ins_name, ins_id, item_id, access_token) -> dict:
    '''Transform item to put into DDB'''
    dt = datetime.utcnow()
    item = {}
    item['PK'] = 'USER#{}'.format(email)
    item['SK'] = 'INS#{}'.format(ins_id)
    item['Name'] = ins_name
    item['Institution_Id'] = ins_id
    item['Item_Id'] = item_id
    item['Access_Token'] = access_token
    item['Date_Added'] = dt.strftime("%m/%d/%Y")
    item['Last_Updated'] = dt.strftime("%m/%d/%Y")
    # item['stocks'] = stocks

    r = ddb_table.put_item(
        Item=item
    )
    return {'Institution Created': item['SK'], 'Response': r}
    
# returns all stocks in 'expense' category
def retrieve_stocks_by_instution(email: str, ins_name):
    response = ddb_table.query(
        KeyConditionExpression=Key('PK').eq('USER#{}'.format(email)) &  Key('SK').begins_with('ACC#{}'.format(ins_name)) 
    )
    return response

def retrieve_stock(symbol: str, ins_name: str, stock_type: str, stock_id: str) -> dict:
    '''Get user ITEM in DDB'''
    r = ddb_table.get_item(
        Key={
            'PK': 'USER#{}'.format(email),
            'SK': 'ACC#{}#{}#{}'.format(ins_name, stock_type, stock_id)        
        }
    )
    item = r.get('Item', {})
    return item

def retrieve_institution(email: str, ins_id):
    r = ddb_table.get_item(
        Key={
            'PK': 'USER#{}'.format(email),
            'SK':  'INS#{}'.format(ins_id)
        }
    )
    item = r.get('Item', {})
    return item

def retrieve_instution_stocks_object(email: str, ins_id) -> dict:
    # get institution
    ins = retrieve_institution(email, ins_id)
    print('ins in obj: ', ins)
    accs = retrieve_stocks_by_instution(email, ins_id)
    print('accs in retrieve accs by inst: ', accs)
    ins['stocks'] = accs
    import pickle
    pickle.dump(ins, open( "retrieve_inst_accs_obj.p", "wb" ) )

    return ins

# returns all stocks in 'expense' category
def retrieve_stocks_by_instution(email: str, ins_name):
    response = ddb_table.query(
        KeyConditionExpression=Key('PK').eq('USER#{}'.format(email)) &  Key('SK').begins_with('ACC#{}'.format(ins_name)) 
    )
    return response

# returns all stocks in 'expense' category
# might not be avle to do this with current sk structure
def retrieve_stocks_by_type(email: str, stock_type):
    response = ddb_table.query(
        KeyConditionExpression=Key('PK').eq('USER#{}'.format(email)) &  Key('SK').begins_with('ACC#{}'.format(stock_type)) 
    )
    return response

def update_stock(email: str, stock_name: str, stock_type: str, item: dict) -> dict:
    #item = request.get_json(force=True)
    attribute_updates = {}
    for key in item.keys():
        attribute_updates[key] = {'Action': 'PUT', 'Value': item.get(key)}

    r = ddb_table.update_item(
        Key={
            'PK': 'USER#{}'.format(email),
            'SK':  'stock#{stock_type}#{stock_name}'.format(stock_type = stock_type, stock_name=stock_name)
        },
        AttributeUpdates=attribute_updates
    )
    return r 

def delete_stock(email: str) -> dict:
    email = get_jwt_identity()
    '''Delete item in DDB'''
    r = ddb_table.delete_item(
        Key={
            'PK': 'USER#{}'.format(email),
            'SK':  'stock#{stock_type}#{stock_name}'.format(stock_type = stock_type, stock_name=stock_name)
        },
    )
    return r
