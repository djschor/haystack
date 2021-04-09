import pandas as pd
import numpy as np 
pd.options.mode.chained_assignment = None  # default='warn'
from datetime import datetime
import time
from .plaid import Balance, Transactions

'''
Returns number of days in the month
'''
def get_month_end_day(month_int): 
    last_day = 0
    three_one = [1, 3, 5, 7, 8, 10, 12]
    three_zero = [4, 6, 9, 11]
    two_eight = [2]
    if month_int in three_one: 
        last_day = 31
    elif month_int in three_zero: 
        last_day = 30
    else: 
        last_day = 28
    return last_day

def number_of_years_of_data(expenses): 
    expenses['Year'] = expenses['Date'].apply(lambda x : x.year)
    return expenses.Year.unique().tolist()