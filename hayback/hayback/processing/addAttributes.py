import pandas as pd
import urllib.request as ur
import requests
# from iexfinance.stocks import Stock
# from iexfinance.stocks import get_historical_data
from datetime import datetime
import os
import pickle
from urllib.request import urlopen
import boto3
import os
from datetime import datetime
from uuid import uuid4
import json
from boto3.dynamodb.conditions import Key
import pprint

fmp_tok = 'a00e11fa00ba561eb0559a9040a0ca5d'
iex_tok = 'pk_4b21399bbfe944e6b1981e70e97d66ea'
symbol = 'AAPL'
DDB_TABLE_NAME = 'Bluechip'
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table(DDB_TABLE_NAME)

'''
scan_bluechip
-scans dynamo db for all stocks, returns list of dicts
'''
def scan_bluechip():
    def print_stocks(stocks):
        for sto in stocks:
    #         print(sto.keys())
            print(f"\n{sto['symbol']}")
    
    scan_kwargs = {
        'FilterExpression': Key('pk').begins_with('STOCK#') & Key('sk').begins_with('IND#') 
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

def calculate_features(stocks_df, price_df):
    stock_price_df = stocks_df[['symbol', 'priceTargetAverage', 'dcf']].merge(price_df, on='symbol', how='outer')
  # calculate features
    stock_price_df['price_target_to_share_price'] = stock_price_df['priceTargetAverage'] / stock_price_df['price']
    stock_price_df["dcf_to_share_price"] = stock_price_df['dcf'] / stock_price_df['price']
    return stocks_df.merge(stock_price_df[['symbol', 'price_target_to_share_price', 'dcf_to_share_price']], on='symbol', how='outer')

'''
calculate_percentiles
- calculates percentiles and ranks for all quantitative features in Stock
    :stocks - output from scan_bluechip() function, scan output from Dynamo DB all stocks
'''
def calculate_percentiles(stocks_df):
    qual_list = ['symbol','name','industry','pk','sk','website','description','ceo','sector','country','fullTimeEmployees','currency','exchange','address','city','state','zip','price', 'image', 'ipoDate', 'updatedDate', 'numberOfAnalysts', 'stockPrice']
    quant_list = [x for x in stocks_df.columns if x not in qual_list]
    low_score_list = ['priceToBookRatioTTM',  'debtToEquity', 'debtToAssets', 'peRatioTTM', 'pegRatioTTM', 'longTermDebtToCapitalizationTTM', 'debtRatioTTM', 'debtEquityRatioTTM', 'debtGrowth']
    for qcol in quant_list:
        if qcol in low_score_list:
            print('low score: {}'.format(qcol))
            stocks_df['{}_rank'.format(qcol)] = stocks_df[qcol].rank(method='max', ascending=True)
            stocks_df['{}_pct'.format(qcol)] = stocks_df[qcol].rank(pct=True, ascending=False)
        else:
            print(qcol)
            if ('{}_rank'.format(qcol) not in stocks_df.columns) or ('{}_pct'.format(qcol) not in stocks_df.columns):
                stocks_df['{}_rank'.format(qcol)] = stocks_df[qcol].rank(method='min', ascending=False)
                stocks_df['{}_pct'.format(qcol)] = stocks_df[qcol].rank(pct=True)
    return stocks_df

'''
get_batch_price
- returns the real time pricing df for all symbols included in input dataframe
  :stocks_df - dataframe containing a column 'symbol' which contains symbols that will get the price queried 
'''
def get_batch_price(stocks_df):
    # sort sectors
    stocks_df.loc[(stocks_df.sector == 'Industrial Goods'),'sector']='N/A'
    stocks_df.loc[(stocks_df.sector == 'Consumer Goods'),'sector']='N/A'
    stocks_df.loc[(stocks_df.sector == 'Conglomerates'),'sector']='N/A'
    stocks_df.loc[(stocks_df.sector == 'Financial'),'sector']='Financial Services'
    stocks_df.loc[(stocks_df.sector == ''),'sector']='N/A'
    
    # get unique sectors
    sectors = stocks_df['sector'].unique()
    sector_df_list = []
    
    # query prices for each sector
    for sector in sectors: 
        split_df = stocks_df[stocks_df.sector == sector]
        print(sector, len(split_df))
        if sector in('Financial Services', 'Technology', 'Healthcare'):
            df1 = split_df[:round(len(split_df)/2)]
            df2 = split_df[round(len(split_df)/2):]
            print('df1-df1 lens: ', len(df1), len(df2))
            for spl in [df1, df2]:
                quer_prices = 'https://financialmodelingprep.com/api/v3/quote/{}?apikey={}'.format(",".join(spl['symbol']), fmp_tok)
                r_prices = requests.get(quer_prices).json()
                sector_df_list.append(pd.DataFrame(r_prices))
        else:
            quer_prices = 'https://financialmodelingprep.com/api/v3/quote/{}?apikey={}'.format(",".join(split_df['symbol']), fmp_tok)
            r_prices = requests.get(quer_prices).json()
            sector_df_list.append(pd.DataFrame(r_prices))
    sector_df = pd.concat(sector_df_list)
    return sector_df

'''
process_stocks_dynoscan
- flattens stocks response object from dyno and returns df of all stocks
    :stocks - stocks resp object from dyno, var from scan_bluechip()
'''
def process_stocks_dynoscan(stocks):
    def flatten_stock(stock):
        new_dict = {}
        for x in stock.keys():
            #print(x)
            if x in ('pk', 'sk', 'symbol'):
                new_dict[x] = stock[x]
            else: 
                loaded = json.loads(stock[x])
                if isinstance(loaded, dict):
                    for i in loaded.keys():
                        new_dict[i] = loaded[i]
        dfe = pd.DataFrame([new_dict.values()], columns=new_dict.keys() )
        qual_list = ['symbol','name','industry','pk','sk','website','description','ceo','sector','country','fullTimeEmployees']
        quant_list = [x for x in dfe.columns if x not in qual_list]
        order_list = qual_list + quant_list
        dfe = dfe[order_list]
        return dfe
    df = pd.json_normalize(stocks, sep='_')
    flat = df.to_dict(orient='records')
    dff = pd.concat([flatten_stock(x) for x in flat]) # flatten and order stocks
    return dff

'''
format_attribute_object
- formats each symbol's row from percentiles_df into object to save to dyno db 
- saves new data back to dynamo db
'''
def save_attribute_object(stocks_df, price_df):
    def growth_attributes(stocks_df):
        growth_df = stocks_df[['price_target_to_share_price', 'price_target_to_share_price_pct', 'price_target_to_share_price_rank',
                              'ebitgrowth', 'ebitgrowth_pct', 'ebitgrowth_rank',
                              'epsgrowth', 'epsgrowth_pct', 'epsgrowth_rank',
                              'revenueGrowth', 'revenueGrowth_pct', 'revenueGrowth_rank']]
        
        return growth_df.to_dict('records')
    
    def value_attributes(stocks_df, price_df):
        value_df_stocks = stocks_df[['symbol', 'dcf_to_share_price', 'price_target_to_share_price_pct', 'price_target_to_share_price_rank',
                                'peRatioTTM_pct', 'peRatioTTM_rank', 
                                'pegRatioTTM', 'pegRatioTTM_pct', 'pegRatioTTM_rank',
                                'priceToBookRatioTTM', 'priceToBookRatioTTM_pct', 'priceToBookRatioTTM_rank']]
        
        value_df_price = price_df[['symbol', 'pe']]
        value_df = value_df_stocks.merge(value_df_price, on='symbol', how='outer')
        value_df = value_df.rename(columns={'pe':'pe_ratio'})
        value_df.drop(columns=['symbol'])
        return value_df.to_dict('records')
    
    def capef_attributes(stocks_df):
        capef_df = stocks_df[['returnOnAssetsTTM', 'returnOnAssetsTTM_pct', 'returnOnAssetsTTM_rank',
                               'returnOnEquityTTM', 'returnOnEquityTTM_pct', 'returnOnEquityTTM_rank']]      
        return capef_df.to_dict('records')
    
    def debt_attributes(stocks_df):
        value_df = stocks_df[['debtEquityRatioTTM', 'debtEquityRatioTTM_pct', 'debtEquityRatioTTM_rank',
                              'longTermDebtToCapitalizationTTM', 'longTermDebtToCapitalizationTTM_pct', 'longTermDebtToCapitalizationTTM_rank',
                              'debtGrowth', 'debtGrowth_pct', 'debtGrowth_rank',
                              'debtToAssets', 'debtToAssets_pct', 'debtToAssets_rank']]
        return value_df.to_dict('records')
                              
    def div_attributes(stocks_df):
        div_df = stocks_df[['dividendsperShareGrowth', 'dividendsperShareGrowth_pct', 'dividendsperShareGrowth_rank',
                              'dividendYielPercentageTTM', 'dividendYielPercentageTTM_pct', 'dividendYielPercentageTTM_rank']]
        return div_df.to_dict('records')
    
    def update_stock_attributes_dyno(pk, sk, attribute_dict):
        # dynamoDB config
        dynamo_client = boto3.client('dynamodb')
        DDB_TABLE_NAME = 'Bluechip'
        ddb_res = boto3.resource('dynamodb')
        ddb_table = ddb_res.Table(DDB_TABLE_NAME)
        r = ddb_table.update_item(
            Key={
                'pk': pk,
                'sk': sk
            },
            UpdateExpression="set attributes = :r",
            ExpressionAttributeValues={
                ':r': json.dumps(attribute_dict),
            },
            ReturnValues="UPDATED_NEW"
        )
#         print(r['ResponseMetadata'])
        try:
            if r['ResponseMetadata']['HTTPStatusCode'] == 200:
                print('{} successfully updated to DynamoDB'.format(pk))
        except:
            print('Error getting response data for Dynamo save')
            return r
        return {'Stock Created': pk, 'Response': r}
    
    attributes = {}
    attributes['growth'] = growth_attributes(stocks_df)
    attributes['value'] = value_attributes(stocks_df, price_df)
    attributes['capef'] = capef_attributes(stocks_df)
    attributes['debt'] = debt_attributes(stocks_df)
    attributes['div'] = div_attributes(stocks_df)
    return update_stock_attributes_dyno(stocks_df['pk'].item(), stocks_df['sk'].item(), attributes)

'''
drive_attribute_update
- driver function for attribute, runs save_attribute_object() on all stocks in percentiles_df
  :percentiles_df - df containing percentages and rankings columns
  :price_df - queried price df
'''
def drive_attribute_update(percentiles_df, price_df):
    for stock in percentiles_df.symbol:
        save_attribute_object(percentiles_df[percentiles_df.symbol == stock], price_df[price_df.symbol == stock])
    return 'Successfully updated attribute objects'
       

'''
drive_attribution
- driver function for attributes, percentiles, rankings of stocks
- order of operations: 
     1. scan_bluechip()
     2. process_stocks_dynoscan(scan_bluechip)
     3. get_batch_price(process_stocks_dynoscan)
     4. calculate_features(process_stocks_dynoscan, get_batch_price)
     5. calculate_percentiles(calculate_features)
     6. calculate_attributes(process_stocks_dynoscan, get_batch_price)
     7. save_attributes
'''
def drive_attribution():
    stocks = scan_bluechip()
    stocks_scan_df = process_stocks_dynoscan(stocks)
    price_df = get_batch_price(stocks_scan_df)
    stocks_calculated_features = calculate_features(stocks_scan_df, price_df)
    percentiles_df = calculate_percentiles(stocks_calculated_features)
    save_updates = drive_attribute_update(percentiles_df, price_df)
    return save_updates