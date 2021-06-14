import boto3
from boto3.dynamodb.conditions import Key
import os
from datetime import datetime
from uuid import uuid4
import json
from hayback.processing.createStocks import Stock
import pandas as pd

# DDB_TABLE_NAME = os.environ.get('DDB_TABLE_NAME')
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table('Bluechip')
fmp_tok = 'a00e11fa00ba561eb0559a9040a0ca5d'
iex_tok = 'pk_4b21399bbfe944e6b1981e70e97d66ea'

def process_create_all_stocks(stocks): 
    symbols_df = pd.read_pickle('../../pickles/symbols_fmp.pkl')
    stock_symbols = [x for x in symbols_df.symbol]
    stocks_init = [Stock(x, fmp_tok, iex_tok) for x in stock_symbols]
    [x.drive() for x in stocks_init]


def create_stock(stock) -> dict:
    item = {}
    item['pk'] = stock['pk']
    item['sk'] = stock['sk']
    item.update({k:json.dumps(v) for (k, v) in stock.items() if k not in ('pk', 'sk')})
    r = ddb_table.put_item(
        Item=item
    )
    return {'Stock Created': item['sk'], 'Response': r}
    
# returns all stocks in 'expense' category
def get_stock(symbol: str):
    response = ddb_table.query(
        KeyConditionExpression=Key('pk').eq('STOCK#{}'.format(symbol)) &  Key('sk').begins_with('IND#') 
    )
    return response