from flask import Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
import boto3
import os
from datetime import datetime
from uuid import uuid4
import requests
import datetime 
#import models
from hayback.models.stockModel import get_stock
from hayback.processing.addAttributes import scan_bluechip
import logging
import json
DDB_TABLE_NAME = 'Bluechip'
ddb_res = boto3.resource('dynamodb')
ddb_table = ddb_res.Table(DDB_TABLE_NAME)
fmp_tok = 'a00e11fa00ba561eb0559a9040a0ca5d'

class StockApi(Resource):
    # def __init__(self):
    #     self.reqparse = reqparse.RequestParser()
    #     self.current_user = get_jwt_identity()
        # self.reqparse.add_argument('symbol', type = str, required = True,
        #     help = 'No symbol provided', location = 'json')

    # @jwt_required
    def get(self, symbol): # remember to add inputs from the response
        try:
            print('\nSymbol', symbol)
            return_stock = get_stock(symbol)['Items'][0]
            print('return stock\n', return_stock)
            return_stock['profile'] = json.loads(return_stock['profile'])
            return_stock['key_metrics'] = json.loads(return_stock['key_metrics'])
            return_stock['attributes'] = json.loads(return_stock['attributes'])
            return_stock['dcf'] = json.loads(return_stock['dcf'])
            return_stock['growth'] = json.loads(return_stock['growth'])
            return_stock['targets'] = json.loads(return_stock['targets'])
            return_stock['ratios'] = json.loads(return_stock['ratios'])
            return_stock['ratings'] = json.loads(return_stock['ratings'])
            return_stock['news'] = json.loads(return_stock['news'])
            print('hayback query for {} successful'.format(symbol))
            status_code = 200
            print('profile: \n', return_stock)

            return [return_stock]

        except:
          print('Unsuccessful query for {} stock')
          status_code = 400
          return 'Unsuccessful query for {} stock', status_code
   
class StocksApi(Resource):
    # @jwt_required
    def get(self): # remember to add inputs from the response
        try:
            return_stocks = scan_bluechip()
            print('hayback query for all {} stocks successful'.format(len(return_stocks)))
            status_code = 200
            return return_stocks, status_code

        except:
            print('Unsuccessful query for all stocks')
            status_code = 400
            return 'Unsuccessful query for all stocks', status_code
   
class HistoricalPricing(Resource):
    def get(self, symbol):
        print(symbol)
        quer = 'https://financialmodelingprep.com/api/v3/historical-price-full/{}?serietype=line&apikey={}'.format(symbol, fmp_tok)
        # try:
        r = requests.get(quer).json()
        #return_list = [[x['date'], x['close']] for x in r['historical']]
        print('loopdoop queried historical pricing for {}'.format(symbol))
        print('historical: \n', type(r))
        return [r]

class TimeSchema(Resource):
    def get(self):
        schema = [{
            "name": "Time",
            "type": "date",
            "format": "%-m/%-d/%Y"
        }, {
            "name": "Close",
            "type": "number"
        }]
        return schema

class TimeDataHistorical(Resource):
    def get(self, symbol):
        print(symbol)
        quer = 'https://financialmodelingprep.com/api/v3/historical-price-full/{}?serietype=line&apikey={}'.format(symbol, fmp_tok)
        r = requests.get(quer).json()
        print('histo format test: ', r['historical'])
        return r['historical']

class OneMinutePricing(Resource):
    def get(self, symbol):
        print(symbol)
        quer = 'https://financialmodelingprep.com/api/v3/historical-chart/1min/{}?apikey={}'.format(symbol, fmp_tok)
        try:
            r = requests.get(quer).json()
            print('queried historical pricing for {}'.format(symbol))
            status_code = 200
            return_list = [[datetime.datetime.strftime(datetime.datetime.strptime((x['date']), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d'), x['open'], x['low'], x['high'], x['close'], x['volume']] for x in r]
            return return_list

        except:
            print('Unsuccessful query for 1m pricing')
            status_code = 400
            return 'Unsuccessful query for 1m pricing', status_code

class FiveMinutePricing(Resource):
    def get(self, symbol):
        print(symbol)
        quer = 'https://financialmodelingprep.com/api/v3/historical-chart/5min/{}?apikey={}'.format(symbol, fmp_tok)
        try:
            r = requests.get(quer).json()
            print('queried historical pricing for {}'.format(symbol))
            return_list = [[datetime.datetime.strftime(datetime.datetime.strptime((x['date']), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d'), x['open'], x['low'], x['high'], x['close'], x['volume']] for x in r]
            return return_list

        except:
            print('Unsuccessful query for 5min pricing')
            status_code = 400
            return 'Unsuccessful query for 5min pricing', status_code


class FifteenMinutePricing(Resource):
    def get(self, symbol):
        print(symbol)
        quer = 'https://financialmodelingprep.com/api/v3/historical-chart/15min/{}?apikey={}'.format(symbol, fmp_tok)
        try:
            r = requests.get(quer).json()
            print('queried 15min pricing for {}'.format(symbol))
            return_list = [[datetime.datetime.strftime(datetime.datetime.strptime((x['date']), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d'), x['open'], x['low'], x['high'], x['close'], x['volume']] for x in r]
            return r

        except:
            print('Unsuccessful query for 15min pricing')
            status_code = 400
            return 'Unsuccessful query for 15min pricing', status_code


class ThirtyMinutePricing(Resource):
    def get(self, symbol): # remember to add inputs from the response
        quer = 'https://financialmodelingprep.com/api/v3/historical-chart/30min/{}?apikey={}'.format(symbol, fmp_tok)
        try:
            r = requests.get(quer).json()
            print('queried 30min pricing for {}'.format(symbol))
            return_list = [[datetime.datetime.strftime(datetime.datetime.strptime((x['date']), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d'), x['open'], x['low'], x['high'], x['close'], x['volume']] for x in r]
            return return_list

        except:
            print('Unsuccessful query for 30min pricing')
            status_code = 400
            return 'Unsuccessful query for 30min pricing', status_code

class HourPricing(Resource):
    def get(self, symbol): # remember to add inputs from the response
        print(symbol)
        quer = 'https://financialmodelingprep.com/api/v3/historical-chart/1hour/{}?apikey={}'.format(symbol, fmp_tok)
        try:
            r = requests.get(quer).json()
            print('queried 1hr pricing for {}'.format(symbol))
            return_list = [[datetime.datetime.strftime(datetime.datetime.strptime((x['date']), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d'), x['open'], x['low'], x['high'], x['close'], x['volume']] for x in r]
            return return_list

        except:
            print('Unsuccessful query for 1hr pricing')
            status_code = 400
            return 'Unsuccessful query for 1hr pricing', status_code

class FourHourPricing(Resource):
    def get(self, symbol): # remember to add inputs from the response
        quer = 'https://financialmodelingprep.com/api/v3/historical-chart/4hour/{}?apikey={}'.format(symbol, fmp_tok)
        try:
            r = requests.get(quer).json()
            print('queried 4hr for {}'.format(symbol))
            return_list = [[datetime.datetime.strftime(datetime.datetime.strptime((x['date']), '%Y-%m-%d %H:%M:%S'),'%Y-%m-%d'), x['open'], x['low'], x['high'], x['close'], x['volume']] for x in r]
            return return_list

        except:
            print('Unsuccessful query for 4hr pricing')
            status_code = 400
            return 'Unsuccessful query for 4hr pricing', status_code
