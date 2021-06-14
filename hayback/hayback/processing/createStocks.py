import pandas as pd
import urllib.request as ur
import requests
from datetime import datetime
import os
import pickle
from urllib.request import urlopen
import boto3
import os
from datetime import datetime
from uuid import uuid4
import json

fmp_tok = 'a00e11fa00ba561eb0559a9040a0ca5d'
iex_tok = 'pk_4b21399bbfe944e6b1981e70e97d66ea'

class Stock:
    def __init__(self, symbol, fmp_tok, iex_tok):
        self.symbol = symbol
        self.fmp_tok = fmp_tok
        self.pk = 'STOCK#{}'.format(symbol)
        self.iex_tok = iex_tok

    def get_company_profile(self, symbol, fmp_tok):
        quer_profile = 'https://financialmodelingprep.com/api/v3/profile/{}?apikey={}'.format(symbol, fmp_tok)
        self.profile = {}
        try: 
            print('  -Querying Company Outlook . . . ')
            r_profile = requests.get(quer_profile).json()
            self.profile['name'] = r_profile[0]['companyName']
            self.profile['currency'] = r_profile[0]['currency']
            self.profile['exchange'] = r_profile[0]['exchangeShortName']
            self.profile['industry'] = r_profile[0]['industry']
            self.sk = "IND#{}".format(r_profile[0]['industry'])
            self.profile['website'] = r_profile[0]['website']
            self.profile['description'] = r_profile[0]['description']
            self.profile['ceo'] = r_profile[0]['ceo']
            self.profile['sector'] = r_profile[0]['sector']
            self.profile['country'] = r_profile[0]['country']
            self.profile['fullTimeEmployees'] = r_profile[0]['fullTimeEmployees']
            self.profile['address'] = r_profile[0]['address']
            self.profile['city'] = r_profile[0]['city']
            self.profile['state'] = r_profile[0]['state']
            self.profile['zip'] = r_profile[0]['zip']
            self.profile['price'] = r_profile[0]['zip']
            self.profile['dcf']  = r_profile[0]['dcf']
            self.profile['image']  = r_profile[0]['image']
            self.profile['ipoDate']  = r_profile[0]['ipoDate']
            print('    Successful\n    Added Profile Info for {}'.format(symbol))
        except:
            print(requests.get(quer_profile).text)
            self.profile = None
            
    def get_dcf(self, symbol, fmp_tok):
        quer_dcf = 'https://financialmodelingprep.com/api/v3/company/discounted-cash-flow/{}?apikey={}'.format(symbol, fmp_tok)
        self.dcf = {}
        try: 
            print('  -Querying DCF . . . ')
            r_dcf = requests.get(quer_dcf).json()
            self.dcf['date'] = r_dcf['date']
            self.dcf['dcf'] = r_dcf['dcf']
            self.dcf['stockPrice'] = r_dcf['Stock Price']
            print('    Successful\n    Added DCF for {}'.format(symbol))
        except:
            print(requests.get(quer_dcf).text)
            self.dcf = None
        
    

    def get_key_metrics(self, symbol, fmp_tok):
        quer_ckm = 'https://financialmodelingprep.com/api/v3/key-metrics/{}?limit=1&apikey={}'.format(symbol, fmp_tok)
        self.key_metrics = {}
        try: 
            print('  -Querying Company Key Metrics . . . ')
#             if not isinstance(self.financials, dict): 
            r_ckm = requests.get(quer_ckm).json()[0]
            self.key_metrics['revenuePerShare'] = r_ckm['revenuePerShare']
            self.key_metrics['netIncomePerShare'] = r_ckm['netIncomePerShare']
            self.key_metrics['operatingCashFlowPerShare'] = r_ckm['operatingCashFlowPerShare']
            self.key_metrics['cashPerShare'] = r_ckm['cashPerShare']
            self.key_metrics['bookValuePerShare'] = r_ckm['bookValuePerShare']
            self.key_metrics['marketCap'] = r_ckm['marketCap']
            self.key_metrics['enterpriseValue'] = r_ckm['enterpriseValue']
            self.key_metrics['peRatio'] = r_ckm['peRatio']
            self.key_metrics['debtToEquity'] = r_ckm['debtToEquity']
            self.key_metrics['debtToAssets'] = r_ckm['debtToAssets']
            self.key_metrics['dividendYield'] = r_ckm['dividendYield']
            self.key_metrics['roe'] = r_ckm['roe']
            print('    Successful\n    Added key metrics  to {}'.format(symbol))
        except:
            print('ERROR KEY METRICS!\n', requests.get(quer_ckm).text)
            self.key_metrics = None
            
    def get_company_growth(self, symbol, fmp_tok):
        quer_growth = 'https://financialmodelingprep.com/api/v3/financial-growth/{}?apikey={}'.format(symbol, fmp_tok)
        self.growth = {}
        try: 
            print('  -Querying Company Growth . . . ')
            r_growth = requests.get(quer_growth).json()[0]
            self.growth['ebitgrowth'] = r_growth['ebitgrowth']
            self.growth['revenueGrowth'] = r_growth['revenueGrowth']
            self.growth['epsgrowth'] = r_growth['epsgrowth']
            self.growth['debtGrowth'] = r_growth['debtGrowth']
            self.growth['dividendsperShareGrowth'] = r_growth['dividendsperShareGrowth']
            print('    Successful\n    Added growth features to {}'.format(symbol))
        except:
            print(requests.get(quer_growth).text)
            self.growth = None
                
    def get_financial_ratios(self, symbol, fmp_tok):
        quer_ratios = 'https://financialmodelingprep.com/api/v3/ratios-ttm/{}?apikey={}'.format(symbol, fmp_tok)
        self.ratios = {}
        try:
            print('  -Querying Financial Ratios . . . ')
            r_ratios = requests.get(quer_ratios).json()[0]
            self.ratios['dividendYielPercentageTTM'] = r_ratios['dividendYielPercentageTTM']
            self.ratios['peRatioTTM'] = r_ratios['peRatioTTM']
            self.ratios['pegRatioTTM'] = r_ratios['pegRatioTTM'] #!
            self.ratios['returnOnAssetsTTM'] = r_ratios['returnOnAssetsTTM']
            self.ratios['returnOnEquityTTM'] = r_ratios['returnOnEquityTTM']
            self.ratios['priceToBookRatioTTM'] = r_ratios['priceToBookRatioTTM']
            self.ratios['debtRatioTTM'] = r_ratios['debtRatioTTM']
            self.ratios['debtEquityRatioTTM'] = r_ratios['debtEquityRatioTTM']
            self.ratios['longTermDebtToCapitalizationTTM'] = r_ratios['longTermDebtToCapitalizationTTM']
            print('    Successful\n    Added Financial Ratios to {}'.format(symbol))
        except:
            print('error: ', requests.get(quer_ratios).text)
            self.ratios = None
            
    def get_company_ratings(self, symbol, fmp_tok):
        quer_rat = 'https://financialmodelingprep.com/api/v3/rating/{}?apikey={}'.format(symbol, fmp_tok)
        self.ratings = {}
        try:
            print('  -Querying Company Ratings . . . ')
            r_rat = requests.get(quer_rat).json()[0]
            self.ratings['date'] = r_rat['date']
            self.ratings['ratingScore'] = r_rat['ratingScore']
            self.ratings['ratingDetailsDCFScore'] = r_rat['ratingDetailsROEScore']
            self.ratings['ratingDetailsROAScore'] = r_rat['ratingDetailsROAScore']
            self.ratings['ratingDetailsDEScore'] = r_rat['ratingDetailsDEScore']
            self.ratings['ratingDetailsPEScore'] = r_rat['ratingDetailsPEScore']
            self.ratings['ratingDetailsPBScore'] = r_rat['ratingDetailsPBScore']
            print('    Successful\n    Added Company Ratings for {}'.format(symbol))
        except:
            print('error: ', requests.get(quer_rat).text)
            self.ratings = None
    def get_price_targets(self, symbol, tok):
        quer_targ = 'https://cloud.iexapis.com/stable/stock/{}/price-target?token={}'.format(symbol, tok)
        self.targets = {}
        try:
            print('  -Querying Price Targets . . . ')
            r_targ = requests.get(quer_targ).json()
            self.targets = r_targ
            print('    Successful\n    Added Price Targets for {}'.format(symbol))
        except:
            print('error: ', requests.get(quer_targ).text)
            self.targets = None
            
    def get_stock_news(self, symbol, fmp_tok):
        quer_news = 'https://financialmodelingprep.com/api/v3/stock_news?tickers={}&limit=50&apikey={}'.format(symbol, fmp_tok)
        try:
            print('  -Querying Financial Ratios . . . ')
            r_news = requests.get(quer_news).json()
            self.news = r_news
            print('    Successful\n    Added 50 latest news articles for {}'.format(symbol))
        except:
            print('error: ', requests.get(quer_news).text)
            self.news = None
            
    def check_data(self):
        print('  -Checking None values . . . ')
        self_list = [self.targets,
                    self.ratings,
                    self.ratios,
                    self.growth,
                    self.dcf,
                    self.key_metrics,
                    self.profile]
        nones = 0
        for d in self_list:
            if d is None:
                nones += 1
        print('      {} Nones'.format(nones))
        if nones >= 3:
            return False
        else:
            return True

    def save_stock_dyno(self):
        # dynamoDB config
        dynamo_client = boto3.client('dynamodb')
        DDB_TABLE_NAME = 'Bluechip'
        ddb_res = boto3.resource('dynamodb')
        ddb_table = ddb_res.Table(DDB_TABLE_NAME)
        item = {}
        item['pk'] = self.pk
        item['sk'] = self.sk
        item['symbol'] = self.symbol
        item['profile'] = json.dumps(self.profile)
        item['key_metrics'] = json.dumps(self.key_metrics)
        item['growth'] = json.dumps(self.growth)
        item['dcf'] = json.dumps(self.dcf)
        item['ratios'] = json.dumps(self.ratios)
        item['ratings'] = json.dumps(self.ratings)
        item['targets'] = json.dumps(self.targets)
        item['news'] = json.dumps(self.news)
        r = ddb_table.put_item(Item=item)
        try:
            if r['ResponseMetadata']['HTTPStatusCode'] == 200:
                print('{} successfully added to DynamoDB'.format(self.symbol))
        except:
            print('Error getting response data for Dynamo save')
        return {'Stock Created': item['sk'], 'Response': r}
    
    
    def drive(self):
        print('\n\nStarting engine for {}'.format(self.symbol))
        self.get_company_profile(self.symbol, self.fmp_tok)
        self.get_dcf(self.symbol, self.fmp_tok)
        self.get_key_metrics(self.symbol, self.fmp_tok)
        self.get_company_growth(self.symbol, self.fmp_tok)
        self.get_financial_ratios(self.symbol, self.fmp_tok)
        self.get_company_ratings(self.symbol, self.fmp_tok)
        self.get_price_targets(self.symbol, self.iex_tok)
        self.get_stock_news(self.symbol, self.fmp_tok)
        none_bool = self.check_data()
        print('none bool:', none_bool)
        if none_bool == True: 
            return self.save_stock_dyno()
        else: 
            print('{} Failed Data Check'.format(self.symbol))
            
if __name__ == "__main__":
  symbols_df = pd.read_pickle('../../pickles/symbols_fmp.pkl')
  stock_symbols = [x for x in symbols_df.symbol]
  stocks_init = [Stock(x, fmp_tok, iex_tok) for x in stock_symbols]
  [x.drive() for x in stocks_init]