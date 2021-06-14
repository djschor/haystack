import boto3
from boto3.dynamodb.conditions import Key
import os
from datetime import datetime
from uuid import uuid4
import json
# DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table('Bluechip')

'''
process_save_accounts
- Queries to plaid endpoints hit an institution and return results by account. 
  This function creates an account and saves for dynamo db for unique accounts in each input
    :email - user email
    :holdings_obj - result from get_holdings, investment account holdings query
    :transactions_obj - result from get_transactions, investment account transactions query
'''
def process_save_accounts(email, holdings_obj, transactions_obj):
    print('\nprocessing_save_accounts: ')
    account_sum_list = []
    account_create_list = []
    accounts = holdings_obj['accounts']
    transactions = transactions_obj['investment_transactions']
    holdings = holdings_obj['holdings']
    for acc in accounts: 
        account_item = {'account_id': acc['account_id'],
                        'balances': json.dumps(acc['balances']),
                        'name': acc['name'],
                        'official_name': acc['official_name'],
                        'type': acc['type'],
                        'subtype': acc['subtype']
                    }
        account_transactions = [x for x in transactions if x['account_id'] == acc['account_id']]
        account_holdings = [x for x in holdings if x['account_id'] == acc['account_id']]
        account_item['investment_transactions'] = json.dumps(account_transactions)
        account_item['holdings'] = json.dumps(account_holdings)
        account_sum_list.append(account_item)
        try:
            r = create_account(email, account_item)
            account_create_list.append(r)
            print('    -Successfully created account {}'.format(account_item['name']))
        except:
            print('   -Error creating account {}'.format(account_item['name']))
            print(create_account(email, account_item))
            return account_item
    print('  Successfully created {} accounts'.format(len(account_sum_list)))

    return account_create_list

def create_account(email, item) -> dict:
    '''Transform item to put into DDB'''
    dt = datetime.utcnow()
    item['pk'] = 'USER#{}'.format(email)
    item['sk'] = 'ACC#{}'.format(item['account_id'])
    item['date_added'] = dt.strftime("%m/%d/%Y")
    r = ddb_table.put_item(
        Item=item
    )
    return {'Account Created': item['sk'], 'Response': r}


# def create_account(email, account_id, account_name, account_type, account_subtype, holdings=None, transactions=None) -> dict:
#     '''Transform item to put into DDB'''
#     dt = datetime.utcnow()
#     item = {}
#     item['pk'] = 'USER#{}'.format(email)
#     item['sk'] = 'ACC#{}'.format(account_id)
#     item['account_id'] = account_id
#     item['name'] = account_name
#     item['type'] = account_type
#     item['subtype'] = account_subtype
#     if not isinstance(holdings, None):
#         item['holdings'] = holdings
#     if not isinstance(transactions, None):
#         item['transactions'] = json.dumps(transactions)
#     item['date_added'] = dt.strftime("%m/%d/%Y")
#     import pickle
#     #pickle.dump(item, open( "createaccountobj_infunct2.p", "wb" ) )

#     #print('ITEM: \n', item, '\\n END ITEM') 
#     r = ddb_table.put_item(
#         Item=item
#     )
#     return {'Account Created': item['sk'], 'Response': r}


def retrieve_account(email: str, account_id: str) -> dict:
    '''Get user ITEM in DDB'''
    r = ddb_table.get_item(
        Key={
            'pk': 'USER#{}'.format(email),
            'sk': 'ACC#{}'.format(account_id)        
        }
    )
    item = r.get('Item', {})
    return item

# returns all accounts in 'expense' category
# might not be avle to do this with current sk structure
def retrieve_user_accounts(email: str):
    response = ddb_table.query(
        KeyConditionExpression=Key('pk').eq('USER#{}'.format(email)) &  Key('sk').begins_with('ACC#') 
    )
    return response

def update_account(email: str, account_id: str, item) -> dict:
    #item = request.get_json(force=True)
    attribute_updates = {}
    for key in item.keys():
        attribute_updates[key] = {'Action': 'PUT', 'Value': item.get(key)}

    r = ddb_table.update_item(
        Key={
            'pk': 'USER#{}'.format(email),
            'sk':  'ACC#{}'.format(account_id)
        },
        AttributeUpdates=attribute_updates
    )
    return r 

def update_transactions(email: str, account_id: str, transactions) -> dict:
    dt = datetime.utcnow()
    trans_dict = {'investment_transactions': {'transactions': json.dumps(transactions), 'date_added': dt.strftime("%m/%d/%Y")}}
    attribute_updates = {}
    for key in trans_dict.keys():
        attribute_updates[key] = {'Action': 'PUT', 'Value': attribute_updates.get(key)}

    r = ddb_table.update_item(
        Key={
            'pk': 'USER#{}'.format(email),
            'sk':  'ACC#{}'.format(account_id)
        },
        AttributeUpdates=attribute_updates
    )
    return r 

def update_holdings(email: str, account_id: str, holdings) -> dict:
    dt = datetime.utcnow()
    hold_dict = {'holdings': json.dumps(holdings), 'date_added': dt.strftime("%m/%d/%Y")}
    attribute_updates = {}
    for key in hold_dict.keys():
        attribute_updates[key] = {'Action': 'PUT', 'Value': hold_dict.get(key)}

    r = ddb_table.update_item(
        Key={
            'pk': 'USER#{}'.format(email),
            'sk':  'ACC#{}'.format(account_id)
        },
        AttributeUpdates=attribute_updates
    )
    return r 

def delete_account(email: str, account_id):
    r = ddb_table.delete_item(
        Key={
            'pk': 'USER#{}'.format(email),
            'sk':  'ACC#{}'.format(account_id)
        },
    )
    return r

