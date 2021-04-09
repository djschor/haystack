import pandas as pd
import numpy as np 
pd.options.mode.chained_assignment = None  # default='warn'
from datetime import datetime
import time
import json
from decimal import Decimal

# def handle_dynamo_types(row):
def decimal_from_value(value):
    if isinstance(value, float):
        return str(value)

# def float_check(ser):

'''
1. clean transactions 
 - input: dict of transactions 
'''
def input_transactions_to_df(transactions, source):
  if source == 'plaid':
    if isinstance(transactions, str):  
      t_obj = json.loads(transactions)
      transactions_df = pd.json_normalize(transactions)
      print('String case \n')
      return transactions_df #transactions_df[keep_cols]
    else: 
      transactions_df = pd.json_normalize(transactions)
      return transactions_df
  if source == 'statement-tcf': 
    tcf = pd.read_csv('../../statements/TCF.csv')
    return tcf
  if source == 'statement-amex': 
    amex = pd.read_csv('../../statements/AMEX.csv')
    return amex
  if source == 'statement-paypal': 
    paypal = pd.read_csv('../../statements/PAYPAL.csv')
    return paypal   
    # add other input sources, credit card, 


  '''
  Clean Transactions: 
  Driver function for cleaning a single account clean.py 
  input- transaction dataframe for single account ###account transaction data from dynamo
  output - dataframe 

  1. input kwargs expense accounts
  2. iterate through each, turn into dataframe
  3. filter for expenditures 
  4. combine dfs 
  5. return combined df
  '''
def clean_transactions(transact_df, source: str): 
    #eliminated by changing input from json to dataframe transact_df = input_transactions_to_df(transactions, source)
    #transact_df['amount'] = transact_df['amount'].apply(decimal_from_value)
    classified_transactions_df = classify_transaction_types(transact_df, source)
    classified_transactions_df.astype(str)
    expenses_df = classified_transactions_df[classified_transactions_df['transaction_type'] == 'Expense']
    income_df = classified_transactions_df[classified_transactions_df['transaction_type'] == 'Income']
    transfer_df = classified_transactions_df[classified_transactions_df['transaction_type'] == 'Account Transfer']
    secondary_classified_expense_df = categorize_secondary_expenses(expenses_df, source)
    primary_classified_expense_df = assign_primary_categories(secondary_classified_expense_df)
    
    #convert floats to decimal
    primary_classified_expense_df['amount'] = primary_classified_expense_df['amount'].apply(decimal_from_value)
    income_df['amount'] = income_df['amount'].apply(decimal_from_value)
    transfer_df['amount'] = transfer_df['amount'].apply(decimal_from_value)
    
    # convert dict floats to decimal
    #expense_dict = primary_classified_expense_df.to_dict(orient=)
    #['amount'] = primary_classified_expense_df['amount'].apply(decimal_from_value)
    # income_df['amount'] = income_df['amount'].apply(decimal_from_value)
    # transfer_df['amount'] = transfer_df['amount'].apply(decimal_from_value)
    
    transactions_item = {'Expenses': primary_classified_expense_df.to_dict(), 'Income': income_df.to_dict(), 'Account_Transfer': transfer_df.to_dict()}
    #transactions_item = {'Expenses': primary_classified_expense_df.to_json(orient='records'), 'Income': income_df.to_json(orient='records'), 'Account_Transfer': transfer_df.to_json(orient='records')}
    #trans_json = json.loads(json.dumps(transactions_item), parse_float=Decimal)
    return transactions_item

def handle_accounts(transactions_item: dict, source: str):
    if source == 'plaid': 
        transact_df = input_transactions_to_df(transactions_item, source)
    pass
def classify_transaction_types(transactions_df, source): 
    accounts_list = ['Paypal', 'Robinhood']
    # Create 'type' category  
    #if not 'transaction_type' in transactions_df.columns:
    transactions_df['transaction_type'] = transactions_df['name'].apply(assign_account_transfers)
    

    #transactions_df['transaction_type'] = [lambda x : 'Account Transfer' for x in transactions_df['name'] if x ]
    #transactions_df.loc[transactions_df['name'].str.contains(account, case=False), 'transaction_type'] = 'Account Transfer'
    if source == 'plaid': 
        # create primary secondary and tertiary from plaid
        transactions_df['plaid_category1'] = [x[0] for x in transactions_df['category'].values.tolist()]
        transactions_df['plaid_category2'] = [x[-1] if len(x) == 2 else "" for x in transactions_df['category'].values.tolist()]
        transactions_df['plaid_category3'] = [x[-1] if len(x) > 2 else "" for x in transactions_df['category'].values.tolist()]

        # assign types (transfer - credit card, expense, income)
        transactions_df['transaction_type'] = transactions_df.apply(plaid_conditions, axis=1)
        transactions_df = transactions_df.rename(columns={'name':'transaction_description'})

        transactions_df = transactions_df[['account_id', 'amount', 'date', 'merchant_name', 'transaction_description', 'transaction_id', 'transaction_type', 'plaid_category1', 'plaid_category2', 'plaid_category3']]
        print('src dtime: ', type(transactions_df.iloc[0]['date']))
        return transactions_df

    if source == 'statement-tcf': 
        transactions_df.loc[transactions_df['Credit'].notnull(), 'transaction_type'] = 'Income'
        transactions_df.loc[transactions_df['Debit'].notnull(), 'transaction_type'] = 'Expense'
        transactions_df.loc[transactions_df['Category'].notnull(), 'Financial Services'] = 'Account Transfer'

        income_df = transactions_df[transactions_df['Credit'].notnull()]
        income_df = income_df.rename(columns={'Credit':'Amount'})
        income_df  = income_df.drop(columns=['Debit', 'Account', 'Check'])

        expenseses_df = tcf[tcf['Debit'].notnull()]

        expenseses_df= expenseses_df.drop(columns=['Credit', 'Account', 'Check'])
        expenseses_df = expenseses_df.rename(columns={'Debit':'Amount'})

        expenseses_df = expenseses_df[(expenseses_df['Category']!= 'Transfer Between Accounts : Credit Card Payment') & (tcf_income['Category']!= 'Transfer Between Accounts')] # removing rows in TCF that are AMEX payments or transfers to savings account
        expenseses_df['Amount'] = expenseses_df['Amount'].apply(lambda x : x * -1)
        #expense_df['Account'] = 'TCF'
        
        expenseses_df.drop(tcf_debit_from_amex.index, inplace=True)
        combined_df = income_df.append(expenseses_df)
        combined_df = combined_df.rename(columns={'Description':'transaction_description'})
        transactions_df.columns = transactions_df.columns.str.lower()
        return combined_df 
    
    if source == 'statement-amex': 
        # Create Amex CSV, create secondary category
        transactions_df = transactions_df[transactions_df['Description'] != 'ONLINE PAYMENT - THANK YOU'] 
        transactions_df['date'] = transactions_df['Date'].apply(lambda x : x[:-2] + '20' + x[-2:])
        #transactions_df['Account'] = 'AMEX'
        transactions_df= combined_df.rename(columns={'Description':'transaction_description'})
        transactions_df.columns = transactions_df.columns.str.lower()
        return transactions_df

    if source == 'statement-paypal': 
        # Create AMEX csv and secondary categories
        transactions_df = transactions_df[(transactions_df['Type'] == 'PreApproved Payment Bill User Payment') | (paypal['Type'] == 'Express Checkout Payment')]
        transactions_df = transactions_df[['Date', 'Name', 'Type', 'Amount']]
        #paypal['Date'] = pd.to_datetime(paypal.Date)
        transactions_df['Category'] = np.zeros([len(transactions_df)])
        transactions_df = transactions_df.rename(columns={'Name':'Description'})
        transactions_df = payplaid_dfpal.drop(columns=['Type'])
        transactions_df['Amount'] = transactions_df['Amount'].apply(lambda x : x * -1)
        #transactions_df['Account'] = 'Paypal'
        transactions_df.columns = transactions_df.columns.str.lower()
        return transactions_df

def categorize_secondary_expenses(expense_df, source: str): 
  # grab 
  expense_df['primary_category'] = ''
  expense_df['secondary_category'] = ''

  if source == 'plaid':
      # Food and Drink
      expense_df.loc[expense_df['plaid_category1']  == 'Restaurants', 'secondary_category'] = 'Restaurants'
      expense_df.loc[expense_df['plaid_category2']  == 'Supermarkets and Groceries', 'secondary_category'] = 'Groceries'
      expense_df.loc[expense_df['plaid_category2']  == 'Convenience Stores', 'secondary_category'] = 'Convenience Stores'
      expense_df.loc[expense_df['plaid_category3']  == 'Coffee Shop', 'secondary_category'] = 'Coffee'
      expense_df.loc[expense_df['plaid_category3']  == 'Food and Beverage Store', 'secondary_category'] = 'Food and Beverage Store'

      # Health
      expense_df.loc[expense_df['plaid_category2']  == 'Pharmacies', 'secondary_category'] = 'Pharmacies'
      expense_df.loc[expense_df['plaid_category2']  == 'Financial Planning and Investments', 'secondary_category'] = 'Investment' 
      # Entertainment
      # Transportation
      expense_df.loc[expense_df['plaid_category2']  == 'Rail', 'secondary_category'] = 'Rail' 

      # Travel
      # Living 
      expense_df.loc[expense_df['plaid_category2']  == 'Rent', 'secondary_category'] = 'Rent'
      expense_df.loc[expense_df['plaid_category2']  == 'Telecommunication Services', 'secondary_category'] = 'Phone Bill' 
      expense_df.loc[expense_df['plaid_category3']  == 'Loans and Mortgages', 'secondary_category'] = 'Loans and Mortgages' 
	
      # Education
      expense_df.loc[expense_df['plaid_category2']  == 'Bookstores', 'secondary_category'] = 'Bookstore'

      # Other
      expense_df.loc[expense_df['plaid_category3']  == 'ATM', 'secondary_category'] = 'ATM Withdrawal' # ATM change, will need two logical conditionos to separate withdrawal and fees
      expense_df.loc[expense_df['plaid_category2']  == 'ATM', 'secondary_category'] = 'ATM Fee' # ATM change, will need two logical conditionos to separate withdrawal and fees
      expense_df.loc[expense_df['plaid_category2']  == 'ATM', 'secondary_category'] = 'Bank Fees' # ATM change, will need two logical conditionos to separate withdrawal and fees

      return expense_df
  
  source_bucket = ['statement-tcf', 'statement-paypal', 'statement-amex']
  
  # legacy secondary category rule system: 
  if source.isin(source_bucket): 
    ## Rule System for prepping the TCF Dataset secondary categories
    expense_df.loc[expense_df['transaction_description']  == 'PAYPAL              INST XFER', 'secondary_category'] = 'Paypal'
    expense_df.loc[expense_df['transaction_description']  == 'VENMO               PAYMENT', 'secondary_category'] = 'Venmo'
    expense_df.loc[expense_df['transaction_description']  == 'HAPPY CLEANERS', 'secondary_category'] = 'Dry Cleaning'
    expense_df.loc[expense_df['transaction_description']  == 'Coeval              WEB PMTS', 'secondary_category'] = 'Rent'
    expense_df.loc[expense_df['transaction_description']  == 'LAKESHORE SPORT &', 'secondary_category'] = 'Gym Membership'
    expense_df.loc[expense_df['transaction_description']  == 'ATT                 Payment', 'secondary_category'] = 'Phone Bill'
    expense_df.loc[expense_df['transaction_description']  == 'ROBINHOOD           Funds', 'secondary_category'] = 'Investment'
    expense_df.loc[expense_df['transaction_description']  == 'IHA CENTRAL BILLIN', 'secondary_category'] = 'Health Bill'
    expense_df.loc[expense_df['transaction_description']  == 'MARKET THYME.', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'SQ *ROOSROAST COFF', 'secondary_category'] = 'Coffee'
    expense_df.loc[expense_df['transaction_description']  == 'VENMO PAYMENT', 'secondary_category'] = 'Venmo'
    expense_df.loc[expense_df['transaction_description']  == 'SQ *FRITA BATIDOS', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'BESTBUYCOM80567329', 'secondary_category'] = 'Online Shopping '
    expense_df.loc[expense_df['transaction_description']  == 'EMAGINE SALINE', 'secondary_category'] = 'Movie'
    expense_df.loc[expense_df['transaction_description']  == 'MUSIC BOX THEATRE', 'secondary_category'] = 'Movie'
    expense_df.loc[expense_df['transaction_description']  == 'THE RAVENS CLUB', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'GOOGLE *YouTube T', 'secondary_category'] = 'Youtube TV'
    expense_df.loc[expense_df['transaction_description']  == 'TB12', 'secondary_category'] = 'Gift'
    expense_df.loc[expense_df['transaction_description']  == 'THE BLUE LEPRECHAU', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'BENCHMARK', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'SESSION ROOM', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'SAINT LOU S ASSEMB', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'THE CHICAGO FIREHO', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'MICHIGAN THEATER F', 'secondary_category'] = 'Movie'
    expense_df.loc[expense_df['transaction_description']  == 'RAVE 1097', 'secondary_category'] = 'Movie'
    expense_df.loc[expense_df['transaction_description']  == 'CITY MUSEUM', 'secondary_category'] = 'Museum'
    expense_df.loc[expense_df['transaction_description']  == 'SCIENCE MUSEUM OF', 'secondary_category'] = 'Museum'
    expense_df.loc[expense_df['transaction_description']  == 'Smoke Daddy', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'OLD CROW SMOKEHOUS', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'SQ *PAPPY S SMOKEH', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'BIRD APP', 'secondary_category'] = 'Scooter'
    expense_df.loc[expense_df['transaction_description']  == 'RICK S AMERICAN CA', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'CAMPUS CORNER', 'secondary_category'] = 'Grocery'
    expense_df.loc[expense_df['transaction_description']  == 'CHECK', 'secondary_category'] = 'Check'
    expense_df.loc[expense_df['transaction_description']  == 'POS 10310 CHICAGO N.MICHIG', 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description']  == 'BLT*Hyperice Inc', 'secondary_category'] = 'Shopping'
    expense_df.loc[expense_df['transaction_description']  == 'STATE OF MI IIT', 'secondary_category'] = 'Taxes'
    expense_df.loc[expense_df['transaction_description']  == 'TM *FLEETWOOD MAC', 'secondary_category'] = 'Concert'
    expense_df.loc[expense_df['transaction_description']  == 'Half Sour', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'HOWL AT THE MOON', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'FREMONT', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'GIORDANOS', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("STARBUCKS"), 'secondary_category'] = 'Coffee'
    expense_df.loc[expense_df['transaction_description'].str.contains("WALGREENS"), 'secondary_category'] = 'Grocery'
    expense_df.loc[expense_df['transaction_description'].str.contains("CVS/PHARM"), 'secondary_category'] = 'Prescription'
    expense_df.loc[expense_df['transaction_description'].str.contains("Amazon"), 'secondary_category'] = 'Amazon'
    expense_df.loc[expense_df['transaction_description'].str.contains("AMZN"), 'secondary_category'] = 'Amazon'
    expense_df.loc[expense_df['transaction_description'].str.contains("AMAZON"), 'secondary_category'] = 'Amazon'
    expense_df.loc[expense_df['transaction_description'].str.contains("TARGET"), 'secondary_category'] = 'Grocery'
    expense_df.loc[expense_df['transaction_description'].str.contains("GOODWILL"), 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description'].str.contains("GIFT"), 'secondary_category'] = 'Gift'
    expense_df.loc[expense_df['transaction_description'].str.contains("ASOS"), 'secondary_category'] = 'Online Shopping'
    expense_df.loc[expense_df['transaction_description'].str.contains("BANGGOOD"), 'secondary_category'] = 'Online Shopping'
    expense_df.loc[expense_df['transaction_description'].str.contains("UBER"), 'secondary_category'] = 'Uber'
    expense_df.loc[expense_df['transaction_description'].str.contains("PAYPAL"), 'secondary_category'] = 'Paypal'
    expense_df.loc[expense_df['transaction_description'].str.contains("AMTRAK"), 'secondary_category'] = 'Amtrak'
    expense_df.loc[expense_df['transaction_description'].str.contains("SPIRIT"), 'secondary_category'] = 'Airline'
    expense_df.loc[expense_df['transaction_description'].str.contains("AETNA"), 'secondary_category'] = 'Healthcare'
    expense_df.loc[expense_df['transaction_description'].str.contains("UNIQLO"), 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description'].str.contains("THE SCOUT"), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("FURIOUS SPOON"), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("FATPOUR"), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("BESTBUY"), 'secondary_category'] = 'Online Shopping'
    expense_df.loc[expense_df['transaction_description'].str.contains("GIFTS"), 'secondary_category'] = 'Gift'
    expense_df.loc[expense_df['transaction_description'].str.contains("jordan gonen", case=False), 'secondary_category'] = 'Education'
    expense_df.loc[expense_df['transaction_description'].str.contains("ClickBank", case=False), 'secondary_category'] = 'Other'
    expense_df.loc[expense_df['transaction_description'].str.contains("WOOD-24030OP", case=False), 'secondary_category'] = 'Rent'
    expense_df.loc[expense_df['transaction_description']  == 'Uber Technologies, Inc', 'secondary_category'] = 'Uber'
    expense_df.loc[expense_df['transaction_description']  == 'Microsoft Corporation', 'secondary_category'] = 'Xbox'
    expense_df.loc[expense_df['transaction_description']  == 'A24 Merch LLC', 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description']  == 'iTunes and App Store', 'secondary_category'] = 'Apple Storage Bill'
    expense_df.loc[expense_df['transaction_description']  == 'IPVanish.com', 'secondary_category'] = 'VPN'
    expense_df.loc[expense_df['transaction_description']  == 'Google', 'secondary_category'] = 'Google'
    expense_df.loc[expense_df['transaction_description']  == 'Thrift Books LLC', 'secondary_category'] = 'Books'
    expense_df.loc[expense_df['transaction_description']  == 'Lyft', 'secondary_category'] = 'Lyft'
    expense_df.loc[expense_df['transaction_description']  == 'DIVISION STREET LIQUORS', 'secondary_category'] = 'Liquor Store'
    expense_df.loc[expense_df['transaction_description']  == 'MURPHY\'S BLEACHERS', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'DELTA AIR LINES DELTA.COM', 'secondary_category'] = 'Airline'
    expense_df.loc[expense_df['transaction_description']  == 'Jewel-Osco', 'secondary_category'] = 'Grocery'
    expense_df.loc[expense_df['transaction_description']  == 'TOWNHOUSE RESTAURANT & WINE BAR', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'OFF COLOR BREWING', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'TST* PIZZERIA BEBU', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'ASOS.COM', 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description']  == 'RAPHLAUREN.COM', 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description']  == 'LYFT', 'secondary_category'] = 'Lyft'
    expense_df.loc[expense_df['transaction_description']  == 'LUCKY STRIKE SOCIAL AT WRIGLEYVILLE', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'ANN ARBOR DISTRICT LIBRARY', 'secondary_category'] = 'Misc'
    expense_df.loc[expense_df['transaction_description']  == 'WEATHER MARK TAVERN', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'Dunkin\' Donuts', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'FLOYDS 99 BARBERSHOP', 'secondary_category'] = 'Haircut'
    expense_df.loc[expense_df['transaction_description']  == 'REMEDY - AON', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'Panda Express', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'EB *LOTUS           SAN FRANCISCO       CA', 'secondary_category'] = 'Concert'
    expense_df.loc[expense_df['transaction_description']  == 'Culver\'s', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'WOLVERINE STATE BREWING CO', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'AMTRAK-MIDWEST CAFE', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'Shake Shack', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'Trader Joe\'s', 'secondary_category'] = 'Grocery'
    expense_df.loc[expense_df['transaction_description']  == 'BASEBALL MONKEY.COM', 'secondary_category'] = 'Online Shopping'
    expense_df.loc[expense_df['transaction_description']  == 'SHEFFIELD\'S BEER & WINE', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'Subway', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'THE CHICAGO FIREHOUSE RESTAURANT', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'FLOWERSHOPPING COM', 'secondary_category'] = 'Gift'
    expense_df.loc[expense_df['transaction_description']  == 'SWEETWATER TAVERN & GRILLE', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'GOOD TIME CHARLEY\'S', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'SCOREKEEPERS', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'McDonald\'s', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'POPEYES', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'GALWAY BAY', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'HAPPY`S', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'BENIHANA', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'PARK WEST', 'secondary_category'] = 'Gift'
    expense_df.loc[expense_df['transaction_description']  == 'PAYPAL *CARLYLEGRIL', 'secondary_category'] = 'Gift'
    expense_df.loc[expense_df['transaction_description']  == 'ART INST CHGO-ONLINE', 'secondary_category'] = 'Gift'
    expense_df.loc[expense_df['transaction_description']  == 'SHAW\'S CRAB HOUSE', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'TERZO PIANO', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'BACKCOUNTRYCOM', 'secondary_category'] = 'Gift'
    expense_df.loc[expense_df['transaction_description']  == 'THE CHOP SHOP', 'secondary_category'] = 'Concert'
    expense_df.loc[expense_df['transaction_description']  == 'PALMER HOUSE HILTON F&B', 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description']  == 'OLD CROW SMOKEHOUSE', 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description']  == 'Uber Eats', 'secondary_category'] = 'Uber Eats'
    expense_df.loc[expense_df['transaction_description'].str.contains("Nike", case=False), 'secondary_category'] = 'Online Shopping'
    expense_df.loc[expense_df['transaction_description'].str.contains("GO GROCER", case=False), 'secondary_category'] = 'Grocery'
    expense_df.loc[expense_df['transaction_description'].str.contains("AMAZON", case=False), 'secondary_category'] = 'Amazon'
    expense_df.loc[expense_df['transaction_description'].str.contains("PRIME VIDEO", case=False), 'secondary_category'] = 'Amazon'
    expense_df.loc[expense_df['transaction_description'].str.contains("RESTAURANT", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("Retail", case=False), 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description'].str.contains("Uber", case=False), 'secondary_category'] = 'Uber'
    expense_df.loc[expense_df['transaction_description'].str.contains("SWEETWATERS", case=False), 'secondary_category'] = 'Coffee'
    expense_df.loc[expense_df['transaction_description'].str.contains("AT&T", case=False), 'secondary_category'] = 'Phone Bill'
    expense_df.loc[expense_df['transaction_description'].str.contains("VENTRA", case=False), 'secondary_category'] = 'Ventra'
    expense_df.loc[expense_df['transaction_description'].str.contains("JETS PIZZA", case=False), 'secondary_category'] = 'Pizza'
    expense_df.loc[expense_df['transaction_description'].str.contains("VEND", case=False), 'secondary_category'] = 'Vending'
    expense_df.loc[expense_df['transaction_description'].str.contains("DEVIL DAWGS", case=False), 'secondary_category'] = 'Vending'
    expense_df.loc[expense_df['transaction_description'].str.contains("BAR", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("SHOWPLACE 16", case=False), 'secondary_category'] = 'Movie'
    expense_df.loc[expense_df['transaction_description'].str.contains("CHEESIE", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("RAMEN", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("WILMOT MOUNTAIN", case=False), 'secondary_category'] = 'Skiing'
    expense_df.loc[expense_df['transaction_description'].str.contains("VELVET TACO", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("KIMERA", case=False), 'secondary_category'] = 'Coffee'
    expense_df.loc[expense_df['transaction_description'].str.contains("QVC", case=False), 'secondary_category'] = 'Online Shopping'
    expense_df.loc[expense_df['transaction_description'].str.contains("LOU MALNATIS", case=False), 'secondary_category'] = 'Pizza'
    expense_df.loc[expense_df['transaction_description'].str.contains("Panera", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("TILE", case=False), 'secondary_category'] = 'Gift'
    expense_df.loc[expense_df['transaction_description'].str.contains("CAFFE ROM", case=False), 'secondary_category'] = 'Coffee'
    expense_df.loc[expense_df['transaction_description'].str.contains("Target", case=False), 'secondary_category'] = 'Target'
    expense_df.loc[expense_df['transaction_description'].str.contains("Weights", case=False), 'secondary_category'] = 'Gym Equipment'
    expense_df.loc[expense_df['transaction_description'].str.contains("PEP", case=False), 'secondary_category'] = 'Gym Equipment'
    expense_df.loc[expense_df['transaction_description'].str.contains("BP", case=False), 'secondary_category'] = 'Gas Station'
    expense_df.loc[expense_df['transaction_description'].str.contains("Coffee", case=False), 'secondary_category'] = 'Coffee'
    expense_df.loc[expense_df['transaction_description'].str.contains("Little Caesars", case=False), 'secondary_category'] = 'Pizza'
    expense_df.loc[expense_df['transaction_description'].str.contains("EBAY", case=False), 'secondary_category'] = 'Ebay'
    expense_df.loc[expense_df['transaction_description'].str.contains("EVERYTHING", case=False), 'secondary_category'] = 'Education'
    expense_df.loc[expense_df['transaction_description'].str.contains("SJV B.V.", case=False), 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description'].str.contains("LLBEAN", case=False), 'secondary_category'] = 'Online Shopping'
    expense_df.loc[expense_df['transaction_description'].str.contains("RUNNING WAREHOUSE", case=False), 'secondary_category'] = 'Athletic Equipment'
    expense_df.loc[expense_df['transaction_description'].str.contains("MANTASLEEP.COM", case=False), 'secondary_category'] = 'Online Shopping'
    expense_df.loc[expense_df['transaction_description'].str.contains("MACK WELDON", case=False), 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description'].str.contains("SHELL OIL", case=False), 'secondary_category'] = 'Gas Station'
    expense_df.loc[expense_df['transaction_description'].str.contains("BEARBOTTOM CLOTHING", case=False), 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description'].str.contains("A BICYCLE SHARE", case=False), 'secondary_category'] = 'Divvy'
    expense_df.loc[expense_df['transaction_description'].str.contains("HEARST MAGAZINES-DIGITAL", case=False), 'secondary_category'] = 'Online Shopping'
    expense_df.loc[expense_df['transaction_description'].str.contains("INTUIT", case=False), 'secondary_category'] = 'Taxes'
    expense_df.loc[expense_df['transaction_description'].str.contains("MCMILLAN RUNNING", case=False), 'secondary_category'] = 'Gym Equipment'
    expense_df.loc[expense_df['transaction_description'].str.contains("NORTHWESTERN MYCHART", case=False), 'secondary_category'] = 'Doctor Appointment'
    expense_df.loc[expense_df['transaction_description'].str.contains("REI", case=False), 'secondary_category'] = 'Online Shopping'
    expense_df.loc[expense_df['transaction_description'].str.contains("DELTA", case=False), 'secondary_category'] = 'Airline'
    expense_df.loc[expense_df['transaction_description'].str.contains("SHEFFIELD'S BEER & WINE GARDEN", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("DIZA HOSPITALITY GROUP", case=False), 'secondary_category'] = 'Misc'
    expense_df.loc[expense_df['transaction_description'].str.contains("U-GO'S MCHGAN", case=False), 'secondary_category'] = 'Grocery'
    expense_df.loc[expense_df['transaction_description'].str.contains("CENEX", case=False), 'secondary_category'] = 'Gas Station'
    expense_df.loc[expense_df['transaction_description'].str.contains("FORD FIELD", case=False), 'secondary_category'] = 'Entertainment'
    expense_df.loc[expense_df['transaction_description'].str.contains("WEST ACRES FSU", case=False), 'secondary_category'] = 'Fast Food'
    expense_df.loc[expense_df['transaction_description'].str.contains("Bodybuilding", case=False), 'secondary_category'] = 'Gym Equipment'
    expense_df.loc[expense_df['transaction_description'].str.contains("Finish Line", case=False), 'secondary_category'] = 'Shoes'
    expense_df.loc[expense_df['transaction_description'].str.contains("StockX LLC", case=False), 'secondary_category'] = 'Shoes'
    expense_df.loc[expense_df['transaction_description'].str.contains("Vivid Seats", case=False), 'secondary_category'] = 'Concert'
    expense_df.loc[expense_df['transaction_description'].str.contains("Ray-Ban", case=False), 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description'].str.contains("Stubhub", case=False), 'secondary_category'] = 'Concert'
    expense_df.loc[expense_df['transaction_description'].str.contains("Wayfair", case=False), 'secondary_category'] = 'Furniture'
    expense_df.loc[expense_df['transaction_description'].str.contains("Eastbay", case=False), 'secondary_category'] = 'Athletic Equipment'
    expense_df.loc[expense_df['transaction_description'].str.contains("LIFX", case=False), 'secondary_category'] = 'Furniture'
    expense_df.loc[expense_df['transaction_description'].str.contains("comcast", case=False), 'secondary_category'] = 'Internet Bill'
    expense_df.loc[expense_df['transaction_description'].str.contains("hampton social", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("7-ELEVEN", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("lowes", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("h&m", case=False), 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description'].str.contains("OVERSTOCK.COM", case=False), 'secondary_category'] = 'Online Shopping'
    expense_df.loc[expense_df['transaction_description'].str.contains("TASKRABBIT", case=False), 'secondary_category'] = 'Home Improvement'
    expense_df.loc[expense_df['transaction_description'].str.contains("Grill", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("HALF SOUR", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("SAFEGUARD", case=False), 'secondary_category'] = 'Home Improvement'
    expense_df.loc[expense_df['transaction_description'].str.contains("U-haul", case=False), 'secondary_category'] = 'Home Improvement'
    expense_df.loc[expense_df['transaction_description'].str.contains("HARBOR", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("insurance", case=False), 'secondary_category'] = 'Insurance'
    expense_df.loc[expense_df['transaction_description'].str.contains("HARBOR", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("TACO BELL", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("TEMPTATIONS OF GRAND HAVEN", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("VICTORY TAP", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("ASIAN OUTPOST", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("CHICAGO COMMUNITY BOND FUND", case=False), 'secondary_category'] = 'Charity'
    expense_df.loc[expense_df['transaction_description'].str.contains("omaze", case=False), 'secondary_category'] = 'Charity'
    expense_df.loc[expense_df['transaction_description'].str.contains("Roastery", case=False), 'secondary_category'] = 'Coffee'
    expense_df.loc[expense_df['transaction_description'].str.contains("DETROIT JUSTICE CENTER", case=False), 'secondary_category'] = 'Charity'
    expense_df.loc[expense_df['transaction_description'].str.contains("CHICAGO TORTURE JUSTICE CENTER", case=False), 'secondary_category'] = 'Charity'
    expense_df.loc[expense_df['transaction_description'].str.contains("SOUTH LOOP MARKET", case=False), 'secondary_category'] = 'Grocery'
    expense_df.loc[expense_df['transaction_description'].str.contains("ALTA GRAND CENTRAL", case=False), 'secondary_category'] = 'Rent'
    expense_df.loc[expense_df['transaction_description'].str.contains("PIZZERIA", case=False), 'secondary_category'] = 'Pizza'
    expense_df.loc[expense_df['transaction_description'].str.contains("CHICK-FIL-A", case=False), 'secondary_category'] = 'Fast Food'
    expense_df.loc[expense_df['transaction_description'].str.contains("adidas", case=False), 'secondary_category'] = 'Athletic Equipment'
    expense_df.loc[expense_df['transaction_description'].str.contains("Chris Albon", case=False), 'secondary_category'] = 'Education'
    expense_df.loc[expense_df['transaction_description'].str.contains("AllPosters", case=False), 'secondary_category'] = 'Home Improvement'
    expense_df.loc[expense_df['transaction_description'].str.contains("Alphalete", case=False), 'secondary_category'] = 'Athletic Equipment'
    expense_df.loc[expense_df['transaction_description'].str.contains("Birthright", case=False), 'secondary_category'] = 'Travel'
    expense_df.loc[expense_df['transaction_description'].str.contains("banggood", case=False), 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description'].str.contains("Lily's Garden", case=False), 'secondary_category'] = 'Gift'
    expense_df.loc[expense_df['transaction_description'].str.contains("APPLE.COM/BILL", case=False), 'secondary_category'] = 'Bill'
    expense_df.loc[expense_df['transaction_description'].str.contains("SECRETS", case=False), 'secondary_category'] = 'Party'
    expense_df.loc[expense_df['transaction_description'].str.contains("Pipes & stuff", case=False), 'secondary_category'] = 'Gift'
    expense_df.loc[expense_df['transaction_description'].str.contains("ASHWORTH AND PARKER LIMITED", case=False), 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description'].str.contains("University Tees", case=False), 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description'].str.contains("Statement Credit", case=False), 'secondary_category'] = 'Other'
    expense_df.loc[expense_df['transaction_description'].str.contains("OOZE", case=False), 'secondary_category'] = 'Entertainment'
    expense_df.loc[expense_df['transaction_description'].str.contains("CESARS ON BROA", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("SOPRAFFINA", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("MAGNOLIA BAKE", case=False), 'secondary_category'] = 'Food'
    expense_df.loc[expense_df['transaction_description'].str.contains("CHICAGO CONCES", case=False), 'secondary_category'] = 'Food'

    expense_df.loc[expense_df['transaction_description'].str.contains("DEBONAIR", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("UC CONCE", case=False), 'secondary_category'] = 'Food'
    expense_df.loc[expense_df['transaction_description'].str.contains("DAVIDSTEA", case=False), 'secondary_category'] = 'Food'
    expense_df.loc[expense_df['transaction_description'].str.contains("PEETS", case=False), 'secondary_category'] = 'Coffee'
    expense_df.loc[expense_df['transaction_description'].str.contains("LITTLE VICTORIES", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("DIVISION STREET LI", case=False), 'secondary_category'] = 'Liquor Store'
    expense_df.loc[expense_df['transaction_description'].str.contains("THE BEAUMONT", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("MAGNOLIA BAKE", case=False), 'secondary_category'] = 'Food'
    expense_df.loc[expense_df['transaction_description'].str.contains("AUBONPA", case=False), 'secondary_category'] = 'Food'
    expense_df.loc[expense_df['transaction_description'].str.contains("HOWL AT THE MOON", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("KALIFLOWER", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("BUDLONG", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("HOUSE OF BLUES", case=False), 'secondary_category'] = 'Concert'
    expense_df.loc[expense_df['transaction_description'].str.contains("GRASS CITY", case=False), 'secondary_category'] = 'Entertainment'
    expense_df.loc[expense_df['transaction_description'].str.contains("THE DARLING", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("BROWN JUG", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("TABOSUSHIPHOND", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("GIORDANO", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("EL HEFE", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("FRESHII", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("ROTI MEDITERRANEAN", case=False), 'secondary_category'] = 'Food'
    expense_df.loc[expense_df['transaction_description'].str.contains("DESIGNER PERFUME", case=False), 'secondary_category'] = 'Shopping'

    expense_df.loc[expense_df['transaction_description'].str.contains("RITUAL", case=False), 'secondary_category'] = 'Food'
    expense_df.loc[expense_df['transaction_description'].str.contains("BOTTLED BLONDE", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("Vig", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("PARLAY AT JOY", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("BOTTOM LOUNGE", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("DIVVY", case=False), 'secondary_category'] = 'Transportation'
    expense_df.loc[expense_df['transaction_description'].str.contains("LIQUEURS", case=False), 'secondary_category'] = 'Liquor Store'
    expense_df.loc[expense_df['transaction_description'].str.contains("CENTURY CENTRE CIN", case=False), 'secondary_category'] = 'Movie'
    expense_df.loc[expense_df['transaction_description'].str.contains("BIERGARTEN", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("KITCHEN", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("GAI - MIDTOWN", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("METROCARD", case=False), 'secondary_category'] = 'Train'
    expense_df.loc[expense_df['transaction_description'].str.contains("CLINTON HALL 51ST", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("CURRY", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("KATI ROLL COMP", case=False), 'secondary_category'] = 'Food'
    expense_df.loc[expense_df['transaction_description'].str.contains("BAO", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("BLACKWOOD", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("RJ GRUNTS", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("Broken English Tac", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("CRISP", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("RICCARDO TRAT", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("AON", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("INAMORATA", case=False), 'secondary_category'] = 'Gift'
    expense_df.loc[expense_df['transaction_description'].str.contains("THE ORIGINAL MOTHE", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("HOOK & LADDER", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("BLACKHAWKS", case=False), 'secondary_category'] = 'Sports'
    expense_df.loc[expense_df['transaction_description'].str.contains("IRISH SHANNONS", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("CHILLERS", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("SHOWPLACE ICON", case=False), 'secondary_category'] = 'Movie'
    expense_df.loc[expense_df['transaction_description'].str.contains("EGGSPERIENCE", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("SHUGA RECORDS", case=False), 'secondary_category'] = 'Music'
    expense_df.loc[expense_df['transaction_description'].str.contains("BUSCEMI", case=False), 'secondary_category'] = 'Liquor Store'
    expense_df.loc[expense_df['transaction_description'].str.contains("CONEY", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("GASTRO", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("AROMA ELL", case=False), 'secondary_category'] = 'Coffee'
    expense_df.loc[expense_df['transaction_description'].str.contains("CRUNCHYROLL", case=False), 'secondary_category'] = 'Entertainment'
    expense_df.loc[expense_df['transaction_description'].str.contains("TAXI", case=False), 'secondary_category'] = 'Transportation'
    expense_df.loc[expense_df['transaction_description'].str.contains("BIVOUAC", case=False), 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description'].str.contains("Restaur", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("CAMPUS CORNER", case=False), 'secondary_category'] = 'Liquor Store'
    expense_df.loc[expense_df['transaction_description'].str.contains("ISALITA CANTI", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("SALADS", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("LAST WORD", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("HOPCAT", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("GOOD TIME CHA", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("SADAKO JAPANESE", case=False), 'secondary_category'] = 'Restaurant'

    expense_df.loc[expense_df['transaction_description'].str.contains("DOMINICKS", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("LIQUO", case=False), 'secondary_category'] = 'Liquor Store'
    expense_df.loc[expense_df['transaction_description'].str.contains("Bellecour", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("COPPER COW", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("HUNGRY MOOSE", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("FRESH PRINTS", case=False), 'secondary_category'] = 'Clothing'
    expense_df.loc[expense_df['transaction_description'].str.contains("MAGERS AND QUINN", case=False), 'secondary_category'] = 'Books'
    expense_df.loc[expense_df['transaction_description'].str.contains("kitchen", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("UNITED CENTER CONC", case=False), 'secondary_category'] = 'Food'
    expense_df.loc[expense_df['transaction_description'].str.contains("BABS UNDERGROUND", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("MASH", case=False), 'secondary_category'] = 'Bar'
    expense_df.loc[expense_df['transaction_description'].str.contains("MEGABUS.COM", case=False), 'secondary_category'] = 'Bus'
    expense_df.loc[expense_df['transaction_description'].str.contains("Terzo", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("DICK S SPORTING", case=False), 'secondary_category'] = 'Athletic Equipment'
    expense_df.loc[expense_df['transaction_description'].str.contains("GALANTIS", case=False), 'secondary_category'] = 'Concert'
    expense_df.loc[expense_df['transaction_description'].str.contains("JIM BRADYS", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("LAUGH FACTORY CHIC", case=False), 'secondary_category'] = 'Concert'
    expense_df.loc[expense_df['transaction_description'].str.contains("MIGHTY GOOD CO", case=False), 'secondary_category'] = 'Coffee'
    expense_df.loc[expense_df['transaction_description'].str.contains("BLIND PIG", case=False), 'secondary_category'] = 'Concert'
    expense_df.loc[expense_df['transaction_description'].str.contains("MASONIC TEMPLE", case=False), 'secondary_category'] = 'Concert'
    expense_df.loc[expense_df['transaction_description'].str.contains("Lollapalooza", case=False), 'secondary_category'] = 'Concert'
    expense_df.loc[expense_df['transaction_description'].str.contains("Duty Free", case=False), 'secondary_category'] = 'Shopping'
    expense_df.loc[expense_df['transaction_description'].str.contains("Taco", case=False), 'secondary_category'] = 'Restaurant'
    expense_df.loc[expense_df['transaction_description'].str.contains("SPRINT *WIRELESS", case=False), 'secondary_category'] = 'Phone Bill'
    expense_df.loc[expense_df['transaction_description'].str.contains("fedex", case=False), 'secondary_category'] = 'Mail'
    expense_df.loc[expense_df['transaction_description'].str.contains("BMO Harris Payment", case=False), 'secondary_category'] = 'Other'
    return expense_df 

def assign_primary_categories(expenses_df):
    #Food and Drink (Grocert, Restaurants, Food Delivery) 
    expenses_df.loc[expenses_df['secondary_category']  == 'Food : Dining Out', 'primary_category'] = 'Food and Drink'
    expenses_df.loc[expenses_df['secondary_category']  == 'Food : Dining Out', 'Category'] = 'Restaurant'
    expenses_df.loc[expenses_df['secondary_category']  == 'Coffee', 'primary_category'] = 'Food and Drink'
    expenses_df.loc[expenses_df['secondary_category']  == 'Restaurant', 'primary_category'] = 'Food and Drink'
    expenses_df.loc[expenses_df['secondary_category']  == 'Food : Groceries', 'Category'] = 'Groceries'
    expenses_df.loc[expenses_df['secondary_category']  == 'Grocery', 'primary_category'] = 'Food and Drink'
    expenses_df.loc[expenses_df['secondary_category']  == 'Groceries', 'primary_category'] = 'Food and Drink'
    expenses_df.loc[expenses_df['secondary_category']  == 'Food', 'primary_category'] = 'Food and Drink'
    expenses_df.loc[expenses_df['secondary_category']  == 'Pizza', 'primary_category'] = 'Food and Drink'
    expenses_df.loc[expenses_df['secondary_category']  == 'Vending', 'primary_category'] = 'Food and Drink'
    expenses_df.loc[expenses_df['secondary_category']  == 'Uber Eats', 'primary_category'] = 'Food and Drink'
    expenses_df.loc[expenses_df['secondary_category']  == 'Fast Food', 'primary_category'] = 'Food and Drink'
    expenses_df.loc[expenses_df['secondary_category']  == 'Convenience Stores', 'primary_category'] = 'Food and Drink'
    expenses_df.loc[expenses_df['secondary_category']  == 'Food and Beverage Store', 'primary_category'] = 'Food and Drink'


    # Transportation (Commuting costs, Ubers, Taxis)
    expenses_df.loc[expenses_df['secondary_category']  == 'Transportation : Fuel', 'primary_category'] = 'Transportation'
    expenses_df.loc[expenses_df['secondary_category']  == 'Transportation', 'primary_category'] = 'Transportation'
    expenses_df.loc[expenses_df['secondary_category']  == 'Uber', 'primary_category'] = 'Transportation'
    expenses_df.loc[expenses_df['secondary_category']  == 'Lyft', 'primary_category'] = 'Transportation'
    expenses_df.loc[expenses_df['secondary_category']  == 'Scooter', 'primary_category'] = 'Transportation'
    expenses_df.loc[expenses_df['secondary_category']  == 'Ventra', 'primary_category'] = 'Transportation'
    expenses_df.loc[expenses_df['secondary_category']  == 'Divvy', 'primary_category'] = 'Transportation'

    # Travel (Vacation Expenses, Flights, Hotels)
    expenses_df.loc[expenses_df['secondary_category']  == 'Personal Travel/Vacation', 'primary_category'] = 'Travel'
    expenses_df.loc[expenses_df['secondary_category']  == 'Personal Travel/Vacation : Airline', 'Category'] = 'Airline'
    expenses_df.loc[expenses_df['secondary_category']  == 'Airline', 'primary_category'] = 'Travel'
    expenses_df.loc[expenses_df['secondary_category']  == 'Amtrak', 'primary_category'] = 'Travel'
    expenses_df.loc[expenses_df['secondary_category']  == 'Rail', 'primary_category'] = 'Travel'
    expenses_df.loc[expenses_df['secondary_category']  == 'Personal Travel/Vacation : Hotel', 'Category'] = 'Hotel'
    expenses_df.loc[expenses_df['secondary_category']  == 'Hotel', 'primary_category'] = 'Travel'
    expenses_df.loc[expenses_df['secondary_category']  == 'Travel', 'primary_category'] = 'Travel'

    # Entertainment (Movies, Concerts, Sporting Events, Bars) 
    expenses_df.loc[expenses_df['secondary_category']  == 'Movie', 'primary_category'] = 'Entertainment'
    expenses_df.loc[expenses_df['secondary_category']  == 'Museum', 'primary_category'] = 'Entertainment'
    expenses_df.loc[expenses_df['secondary_category']  == 'Entertainment', 'primary_category'] = 'Entertainment'
    expenses_df.loc[expenses_df['secondary_category']  == 'Youtube TV', 'primary_category'] = 'Entertainment'
    expenses_df.loc[expenses_df['secondary_category']  == 'Bar', 'primary_category'] = 'Entertainment'
    expenses_df.loc[expenses_df['secondary_category']  == 'Concert', 'primary_category'] = 'Entertainment'
    expenses_df.loc[expenses_df['secondary_category']  == 'Xbox', 'primary_category'] = 'Entertainment'
    expenses_df.loc[expenses_df['secondary_category']  == 'Books', 'primary_category'] = 'Entertainment'
    expenses_df.loc[expenses_df['secondary_category']  == 'Skiing', 'primary_category'] = 'Entertainment'
    expenses_df.loc[expenses_df['secondary_category']  == 'Liquor Store', 'primary_category'] = 'Entertainment'
    expenses_df.loc[expenses_df['secondary_category']  == 'Education', 'primary_category'] = 'Entertainment'
    expenses_df.loc[expenses_df['secondary_category']  == 'Party', 'primary_category'] = 'Entertainment'
    expenses_df.loc[expenses_df['secondary_category']  == 'Sports', 'primary_category'] = 'Entertainment'
    expenses_df.loc[expenses_df['secondary_category']  == 'Music', 'primary_category'] = 'Entertainment'

    # Education (Books, School, Online Courses, Educational Content) 
    expenses_df.loc[expenses_df['secondary_category']  == 'Bookstores', 'primary_category'] = 'Education'


    # Shopping 
    expenses_df.loc[expenses_df['secondary_category']  == 'Amazon', 'primary_category'] = 'Shopping'
    expenses_df.loc[expenses_df['secondary_category']  == 'Shopping', 'Category'] = 'Online Shopping'
    expenses_df.loc[expenses_df['secondary_category']  == 'Online Shopping', 'primary_category'] = 'Shopping'
    expenses_df.loc[expenses_df['secondary_category']  == 'Clothing', 'primary_category'] = 'Shopping'
    expenses_df.loc[expenses_df['secondary_category']  == 'Housing : Furnishings', 'primary_category'] = 'Shopping'
    expenses_df.loc[expenses_df['secondary_category']  == 'Housing : Supplies', 'primary_category'] = 'Shopping'
    expenses_df.loc[expenses_df['secondary_category']  == 'Publications', 'primary_category'] = 'Shopping'
    expenses_df.loc[expenses_df['secondary_category']  == 'Housing : Home Repair', 'primary_category'] = 'Shopping'
    expenses_df.loc[expenses_df['secondary_category']  == 'Online Shopping', 'primary_category'] = 'Shopping'
    expenses_df.loc[expenses_df['secondary_category']  == 'Target', 'primary_category'] = 'Shopping'
    expenses_df.loc[expenses_df['secondary_category']  == 'Ebay', 'primary_category'] = 'Shopping'
    expenses_df.loc[expenses_df['secondary_category']  == 'Athletic Equipment', 'primary_category'] = 'Shopping'
    expenses_df.loc[expenses_df['secondary_category']  == 'Shoes', 'primary_category'] = 'Shopping'

    # Health (Insurance, healthcare, gym membership)
    expenses_df.loc[expenses_df['secondary_category']  == 'Gym Membership', 'primary_category'] = 'Health'
    expenses_df.loc[expenses_df['secondary_category']  == 'Health Bill', 'primary_category'] = 'Health'
    expenses_df.loc[expenses_df['secondary_category']  == 'Healthcare - HSA Spending Account : Prescriptions', 'Category'] = 'Prescription'
    expenses_df.loc[expenses_df['secondary_category']  == 'Prescription', 'primary_category'] = 'Health'
    expenses_df.loc[expenses_df['secondary_category']  == 'Personal Care', 'primary_category'] = 'Health'
    expenses_df.loc[expenses_df['secondary_category']  == 'Healthcare - HSA Spending Account : Copays', 'Category'] = 'Copay'
    expenses_df.loc[expenses_df['secondary_category']  == 'Copay', 'primary_category'] = 'Health'
    expenses_df.loc[expenses_df['secondary_category']  == 'Healthcare - HSA Spending Account', 'primary_category'] = 'Health'
    expenses_df.loc[expenses_df['secondary_category']  == 'Healthcare', 'primary_category'] = 'Health'
    expenses_df.loc[expenses_df['secondary_category']  == 'Gym Equipment', 'primary_category'] = 'Health'
    expenses_df.loc[expenses_df['secondary_category']  == 'Doctor Appointment', 'primary_category'] = 'Health'
    expenses_df.loc[expenses_df['secondary_category']  == 'Pharmacies', 'primary_category'] = 'Health'

    # Housing and Living | (bills, insurance, rent) 
    expenses_df.loc[expenses_df['secondary_category']  == 'Rent', 'primary_category'] = 'Housing'
    expenses_df.loc[expenses_df['secondary_category']  == 'Furniture', 'primary_category'] = 'Housing'
    expenses_df.loc[expenses_df['secondary_category']  == 'Home Improvement', 'primary_category'] = 'Housing'
    expenses_df.loc[expenses_df['secondary_category']  == 'Bill', 'primary_category'] = 'Housing'
    expenses_df.loc[expenses_df['secondary_category']  == 'Internet Bill', 'primary_category'] = 'Housing'
    expenses_df.loc[expenses_df['secondary_category']  == 'Phone Bill', 'primary_category'] = 'Housing'
    expenses_df.loc[expenses_df['secondary_category']  == 'Insurance', 'primary_category'] = 'Housing'
    expenses_df.loc[expenses_df['secondary_category']  == 'Loans and Mortgages', 'primary_category'] = 'Housing'

    # Other
    expenses_df.loc[expenses_df['secondary_category']  == 'Venmo', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Paypal', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Dry Cleaning', 'primary_category'] = 'Other'

    expenses_df.loc[expenses_df['secondary_category']  == 'Investment', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Business', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Contributions', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Utilities : Phone', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Transfer Between Accounts', 'Category'] = 'Savings'
    expenses_df.loc[expenses_df['secondary_category']  == 'Savings', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Financial Services : ATM', 'Category'] = 'ATM Withdrawal'
    expenses_df.loc[expenses_df['secondary_category']  == 'ATM Withdrawal', 'Category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Gift', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Financial Services : Fees', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Check', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Taxes', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Uncategorized Expense', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Other', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Hobby', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Education', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Apple Storage Bill', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'VPN', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Google', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Misc', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Transportation : Fuel', 'Category'] = 'Gas Station'
    expenses_df.loc[expenses_df['secondary_category']  == 'Gas Station', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Charity', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Mail', 'primary_category'] = 'Other'
    expenses_df.loc[expenses_df['secondary_category']  == 'Bank Fees', 'primary_category'] = 'Other'

    expenses_df = expenses_df.rename(columns={'Debit':'Amount'}) #, 'primary_category':'primaryCategory'
    #expenses_df['date'] = expenses_df['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d')) #turning all Date strings into Datetime objects (to use for logical comparisons)
    expenses_df = expenses_df.sort_values(by = ['date'], ascending=False)
    return expenses_df

def assign_account_transfers(s): 
  accounts_list = ['Paypal', 'Robinhood']
  for acc in accounts_list:
      if acc.lower() in s.lower():
          return 'Account Transfer'

def plaid_conditions(s):
    accounts_list = ['Paypal', 'Robinhood']
    conditions = { 
          "income": [
          # income 
            (s['plaid_category1'] == 'Transfer') & (s['plaid_category2'] == 'Credit') & ('kpmg' in s['name'].lower()),
            (s['plaid_category1'] == 'Transfer') & (s['plaid_category3'] == 'Payroll'),
            (s['amount'] < 0)
          ],
          "account transfer": [
            # account transfer
            (s['plaid_category1'] == 'Transfer') & (s['plaid_category3'] in accounts_list), #,
            (s['plaid_category1'] == 'Payment') & ((s['plaid_category3'] == 'Credit Card') | (s['plaid_category2'] == 'Credit Card') ) #,
          ],
        }
    for x in conditions["income"]:
        if x: 
            return "Income"
    for y in conditions["account transfer"]:
        if y: 
            return "Account Transfer"
    for z in accounts_list: 
        if z.lower() in s['name'].lower():
            return 'Account Transfer'
    return "Expense"
