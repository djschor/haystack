import pandas as pd
import numpy as np 
pd.options.mode.chained_assignment = None  # default='warn'
from datetime import datetime
import time


##############################
#########  STATS  ############
##############################

'''
Average spending per Day (does not include outliers above 95th percentile)
'''
def average_daily_spend(expenses): 
    exp = expenses
    day_grouped = exp.groupby(['Date']).sum()
    y=day_grouped['Amount']
    removed_outliers = day_grouped[y.between(y.quantile(.00), y.quantile(.95))]
    mean_day = removed_outliers['Amount'].mean()
    return mean_day


##############################
#########  GRAPHS  ###########
##############################
