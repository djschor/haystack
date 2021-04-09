import pandas as pd
import numpy as np 
pd.options.mode.chained_assignment = None  # default='warn'
from datetime import datetime
import time


'''
Average spending per Year (does not include current year in calculation)
'''
def average_yearly_spend(expenses): 
    current_year = str(datetime.now().year)
    exp = expenses
    exp['Year'] = exp['Date'].apply(lambda x : str(x.year))
    exp = exp[exp['Year'] != current_year]
    year_grouped = exp.groupby(['Year']).sum()
    mean_year = year_grouped['Amount'].mean()
    return mean_year