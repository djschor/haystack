import pandas as pd
import numpy as np 
pd.options.mode.chained_assignment = None  # default='warn'
from datetime import datetime
import time

##############################
#########  STATS  ############
##############################
'''
Average of all monthly spending to this day in the month
'''
def average_monthly_spent_to_point(expenses): 
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_day = datetime.now().day
    unique_current_md = str(datetime.now().month) + " " + str(datetime.now().year)
    exp = expenses
    exp['Unique_month_year'] = exp['Date'].apply(lambda x : str(x.month) + " " + str(x.year))
    exp = exp[exp['Unique_month_year'] != unique_current_md]
    month_grouped = exp.groupby(['Unique_month_year'])
    beg_to_current_df = pd.DataFrame(columns = exp.columns)
    for name, group in month_grouped:
        group_month = name.split(" ")[0]
        group_year = name.split(" ")[1]
        late = datetime.strptime(group_month + '/' + str(current_day) + '/' + group_year, '%m/%d/%Y')
        filtered_dates_df = group[group['Date'] < late]
        beg_to_current_df = pd.concat([filtered_dates_df, beg_to_current_df])

    filtered_grouped_sum = beg_to_current_df.groupby(['Unique_month_year']).sum()
    mean_month_to_point = filtered_grouped_sum['Amount'].mean()
    return mean_month_to_point

'''
Average spending per month (does not include current month in calculation)
'''
def average_monthly_spend(expenses, dis_month=datetime.now().month, dis_year=datetime.now().year, is_current=True): 
    unique_current_md = str(datetime.now().month) + str(datetime.now().year)
    unique_md_dis = str(dis_month) + str(dis_year)
    exp = expenses
    print(exp['Date'])
    exp['Unique_month_year'] = exp['Date'].apply(lambda x : str(x.month) + str(x.year))
    if is_current == True:
        exp = exp[exp['Unique_month_year'] != unique_current_md]
    else: 
        exp = exp[(exp['Unique_month_year'] != unique_current_md) & (exp['Unique_month_year'] != unique_md_dis)]
        month_grouped = exp.groupby(['Unique_month_year']).sum()
        mean_months = month_grouped['Amount'].mean()
        return mean_months

'''
Total difference of money spent this month compared to average monthly spend to point in percent increase of decrease
'''
def monthly_change_percent(expenses, month_int=datetime.now().month,  year_int = datetime.now().year, is_current=True):
    month_int = int(month_int)
    year_int = int(year_int)
    total_spent_month = total_spent_any_month(expenses, month_int, year_int, is_current)
    if is_current == True:    
        avg_monthly_spend_to_pt = average_monthly_spent_to_point(expenses)
        change = total_spent_month - avg_monthly_spend_to_pt 
        percent_delta = change / (avg_monthly_spend_to_pt) * 100
        return percent_delta

    else: 
        avg_monthly_spent = average_monthly_spend(expenses, month_int, year_int, is_current)
        change = total_spent_month - avg_monthly_spent 
        percent_delta = change / (avg_monthly_spent) * 100
        return percent_delta

'''
Difference of money spent this month compared to average monthly spent to point. 
If the number is positive, you've spent that amount more this month than normally. 
If negative, you've spent that amount less than normal
'''
def monthly_change_total(expenses, month_int = datetime.now().month, year_int = datetime.now().year, is_current=False): 
    month_int = int(month_int)
    year_int = int(year_int)
    if is_current == True: 
        total_spent_month_base = total_spent_any_month(expenses, is_current=True)
        avg_monthly_spend_to_pt = average_monthly_spent_to_point(expenses)
        change = total_spent_month_base - avg_monthly_spend_to_pt 
        return change
    else: 
        total_spent_month_base = total_spent_any_month(expenses, month_int, year_int, is_current)
        avg_monthly_spend = average_monthly_spend(expenses, month_int, year_int, is_current)
        change = total_spent_month_base - avg_monthly_spend 
        return change

##############################
#########  GRAPHS  ###########
##############################

'''
Total spent in any specific month
Arguments: Expenses dataframe, month, year
imp
'''
def total_spent_any_month(expenses, month_int = datetime.now().month, year_int = datetime.now().year, is_current=False): 
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_day =  datetime.now().day
    month_end_day = get_month_end_day(month_int)
    first_day = datetime.strptime(str(month_int) + '/' + str(1) + '/' + str(year_int), '%m/%d/%Y')
    if is_current == False: 
        last_day = datetime.strptime(str(month_int) + '/' + str(month_end_day) + '/' + str(year_int), '%m/%d/%Y')
    else: 
        last_day = datetime.strptime(str(month_int) + '/' + str(current_day) + '/' + str(year_int), '%m/%d/%Y')
    
    month_transactions = expenses[(expenses['Date'] > first_day) & (expenses['Date'] < last_day)]
    total_spent = round(month_transactions['Amount'].sum(), 2)
    return total_spent


'''
Total amount of money spent in current month for each primary category in any month
Arguments: expenses df, month, int
'''
def month_prim_cat_totals(expenses, month_int = datetime.now().month, year_int = datetime.now().year, is_current=False): 
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_day =  datetime.now().day
    month_end_day = get_month_end_day(month_int)
    first_day = datetime.strptime(str(month_int) + '/' + str(1) + '/' + str(year_int), '%m/%d/%Y')
    if is_current == False: 
        last_day = datetime.strptime(str(month_int) + '/' + str(month_end_day) + '/' + str(year_int), '%m/%d/%Y')
    else: 
        last_day = datetime.strptime(str(month_int) + '/' + str(current_day) + '/' + str(year_int), '%m/%d/%Y')
    
    month_transactions = expenses[(expenses['Date'] > first_day) & (expenses['Date'] < last_day)]
    prim_categories_month = month_transactions.groupby('primaryCategory')['Amount'].sum()
    categories = prim_categories_month.index.values.tolist()
    values = prim_categories_month.values.tolist()
    values = [ round(x, 2) for x in values ] 


    #print(type(categories))
    backgroundColor = ["#AF9C00", "#629628", "#00884c", "#007568", "#006075", "#00496F", "#003258"]
    hoverBackgroundColor = ["#CCC05C", "#8CB262", "#17925C", "#2E8E83", "#73A8B3", "#456985", "#738FA3"]
    monthly_cats_json = {"datasets": {"data": values, "backgroundColor": backgroundColor, "hoverBackgroundColor": hoverBackgroundColor}, "labels": categories, "option": {}}
    return monthly_cats_json

def stacked_area_income_outcome_year_per_month(expenses, income_df, year_int = datetime.now().year): 
    first_day = datetime.strptime(str(1) + '/' + str(1) + '/' + str(year_int), '%m/%d/%Y')
    last_day = datetime.strptime(str(12) + '/' + str(31) + '/' + str(year_int), '%m/%d/%Y')

    ## get expenses df sum of month spend 
    # get transactions in the year
    year_expense_transactions = expenses[(expenses['Date'] > first_day) & (expenses['Date'] < last_day)]

    # create month column 
    year_expense_transactions['Month'] = year_expense_transactions['Date'].apply(lambda x: x.month)

    # groupby month
    expense_sum_df = year_expense_transactions.groupby('Month')['Amount'].sum().reset_index()
    expense_sum_df['Type'] = 'Expenditure'

    ## get incomes df sum of month spend 
    income_df.rename(columns = {'Credit': 'Amount'}, inplace=True)
    year_income_transactions = income_df[(income_df['Date'] > first_day) & (income_df['Date'] < last_day)]
    year_income_transactions['Month'] = year_income_transactions['Date'].apply(lambda x: x.month)
    income_sum_df = year_income_transactions.groupby('Month')['Amount'].sum().reset_index()
    income_sum_df['Type'] = 'Income'

    merged_year_per_mo_df = expense_sum_df.append(income_sum_df).reset_index()
    merged_year_per_mo_df = merged_year_per_mo_df.drop(columns = ['index'])
    merged_year_per_mo_df['Amount'] = merged_year_per_mo_df['Amount'].apply(lambda x: round(x, 2))
    return merged_year_per_mo_df.to_dict('records')   
     

def line_total_any_month_per_day(expenses, month_int = datetime.now().month, year_int = datetime.now().year, is_current=False): 
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_day =  datetime.now().day
    month_end_day = get_month_end_day(month_int)
    first_day = datetime.strptime(str(month_int) + '/' + str(1) + '/' + str(year_int), '%m/%d/%Y')
    if is_current == False: 
        last_day = datetime.strptime(str(month_int) + '/' + str(month_end_day) + '/' + str(year_int), '%m/%d/%Y')
    else: 
        last_day = datetime.strptime(str(month_int) + '/' + str(current_day) + '/' + str(year_int), '%m/%d/%Y')
    
    month_transactions = expenses[(expenses['Date'] > first_day) & (expenses['Date'] < last_day)]

    #get total spending for the month for each day
    prim_categories_mo = month_transactions.groupby('Date')['Amount'].sum()
    cat_totals_per_day = month_transactions.groupby(['Date','primaryCategory'], as_index=False)['Amount'].sum()
    prim_cats = pd.Series(['Other', 'Health', 'Shopping', 'Food', 'Transportation',
           'Entertainment', 'Travel'])

    #get total spending for each category
    cat_totals_regrouped = cat_totals_per_day.groupby(['Date'])
    for x, y in cat_totals_regrouped: # x is datetime index, y is dataframe
        day_prim_cats = y['primaryCategory'] #this is a series of all the primary categories used in the day
        missing_cats = prim_cats[~prim_cats.isin(day_prim_cats)].tolist() # series of all categories not in day_prim_cats
        amounts = []
        cat_name = [] 
        date = []
        for cat in missing_cats: 
            amounts.append(0)
            cat_name.append(cat)
            date.append(x)
        data = {"Date": date, "primaryCategory": cat_name, "Amount": amounts}
        missing_vals_df = pd.DataFrame(data)
        cat_totals_per_day = pd.concat([cat_totals_per_day, missing_vals_df])
        
    cat_totals_per_day = cat_totals_per_day.sort_values(by=['Date'])
    
    # Creating dfs for each primary category
    transportation = cat_totals_per_day[cat_totals_per_day['primaryCategory'] == 'Transportation']
    other = cat_totals_per_day[cat_totals_per_day['primaryCategory'] == 'Other']
    health =  cat_totals_per_day[cat_totals_per_day['primaryCategory'] == 'Health']
    food =  cat_totals_per_day[cat_totals_per_day['primaryCategory'] == 'Food']
    shopping = cat_totals_per_day[cat_totals_per_day['primaryCategory'] == 'Shopping']
    travel = cat_totals_per_day[cat_totals_per_day['primaryCategory'] == 'Travel']
    entertainment = cat_totals_per_day[cat_totals_per_day['primaryCategory'] == 'Entertainment']
        
    #OTHER
    other['Day'] = other['Date'].apply(lambda x : str(x.day))
    if is_current == False:
        days = range(1,month_end_day + 1)
    else: 
        days = range(1, current_day + 1)
        
    for x in days: 
        if str(x) not in other['Day'].values:
            date = datetime.strptime(str(month_int) + '/' + str(x) + '/' + str(year_int), '%m/%d/%Y')
            cat = 'Other'
            amount = 0
            day = x
            zero_row = pd.Series([date, cat, amount, day], index = other.columns)
            other = other.append(zero_row, ignore_index=True)
            other = other.sort_values(by='Date')
    values = [ round(x, 2) for x in other['Amount'].tolist() ] 
    other_data = {"label": "Other", "borderColor":"#AF9C00", "data": values}    

    # TRANSPORTATION
    transportation['Day'] = transportation['Date'].apply(lambda x : str(x.day))
    for x in days: 
        if str(x) not in transportation['Day'].values:
            date = datetime.strptime(str(month_int) + '/' + str(x) + '/' + str(year_int), '%m/%d/%Y')
            cat = 'Transportation'
            amount = 0
            day = x
            zero_row = pd.Series([date, cat, amount, day], index = transportation.columns)
            transportation = transportation.append(zero_row, ignore_index=True)
            transportation = transportation.sort_values(by='Date')
    values = [ round(x, 2) for x in transportation['Amount'].tolist() ] 
    transportation_data = {"label": "Transportation", "borderColor":"#629628", "data": values}    

    # Food
    food['Day'] = food['Date'].apply(lambda x : str(x.day))
    for x in days: 
        if str(x) not in food['Day'].values:
            date = datetime.strptime(str(month_int) + '/' + str(x) + '/' + str(year_int), '%m/%d/%Y')
            cat = 'Food'
            amount = 0
            day = x
            zero_row = pd.Series([date, cat, amount, day], index = food.columns)
            food = food.append(zero_row, ignore_index=True)
            food = food.sort_values(by='Date')
    values = [ round(x, 2) for x in food['Amount'].tolist() ]
    food_data = {"label": "Food", "borderColor":"#00884C", "data": values}    

    # Health
    health['Day'] = health['Date'].apply(lambda x : str(x.day))
    for x in days: 
        if str(x) not in health['Day'].values:
            date = datetime.strptime(str(month_int) + '/' + str(x) + '/' + str(year_int), '%m/%d/%Y')
            cat = 'Health'
            amount = 0
            day = x
            zero_row = pd.Series([date, cat, amount, day], index = health.columns)
            health = health.append(zero_row, ignore_index=True)
            health = health.sort_values(by='Date')
    values = [ round(x, 2) for x in health['Amount'].tolist() ]
    health_data = {"label": "Health", "borderColor":"#007568", "data": values}    

    # Entertainment
    entertainment['Day'] = entertainment['Date'].apply(lambda x : str(x.day))
    for x in days: 
        if str(x) not in entertainment['Day'].values:
            date = datetime.strptime(str(month_int) + '/' + str(x) + '/' + str(year_int), '%m/%d/%Y')
            cat = 'Entertainment'
            amount = 0
            day = x
            zero_row = pd.Series([date, cat, amount, day], index = entertainment.columns)
            entertainment = entertainment.append(zero_row, ignore_index=True)
            entertainment = entertainment.sort_values(by='Date')
    values = [ round(x, 2) for x in entertainment['Amount'].tolist() ]
    entertainment_data = {"label": "Entertainment", "borderColor":"#006075", "data": values}    
    # SHOPPING
    shopping['Day'] = shopping['Date'].apply(lambda x : str(x.day))
    for x in days: 
        if str(x) not in shopping['Day'].values:
            date = datetime.strptime(str(month_int) + '/' + str(x) + '/' + str(year_int), '%m/%d/%Y')
            cat = 'Shopping'
            amount = 0
            day = x
            zero_row = pd.Series([date, cat, amount, day], index = shopping.columns)
            shopping = shopping.append(zero_row, ignore_index=True)
            shopping = shopping.sort_values(by='Date')
    values = [ round(x, 2) for x in shopping['Amount'].tolist() ]
    shopping_data = {"label": "Shopping", "borderColor":"#00496F", "data": values}    

    # TRAVEL
    travel['Day'] = travel['Date'].apply(lambda x : str(x.day))
    for x in days: 
        if str(x) not in travel['Day'].values:
            date = datetime.strptime(str(month_int) + '/' + str(x) + '/' + str(year_int), '%m/%d/%Y')
            cat = 'Travel'
            amount = 0
            day = x
            zero_row = pd.Series([date, cat, amount, day], index = travel.columns)
            travel = travel.append(zero_row, ignore_index=True)
            travel = travel.sort_values(by='Date')
    values = [ round(x, 2) for x in travel['Amount'].tolist() ]
    travel_data = {"label": "Travel", "borderColor":"#003258", "data": values}    

    # TOTAL 
    totals = prim_categories_mo.to_frame()
    totals['Date'] = totals.index
    totals['Day'] = totals['Date'].apply(lambda x : str(x.day))
    for x in days: 
        if str(x) not in totals['Day'].values:
            date = datetime.strptime(str(month_int) + '/' + str(x) + '/' + str(year_int), '%m/%d/%Y')
            amount = 0
            day = x
            zero_row = pd.Series([amount, date, day], index = totals.columns)
            totals = totals.append(zero_row, ignore_index=True)
            totals = totals.sort_values(by='Date')
    values = [ round(x, 2) for x in totals['Amount'].tolist() ]
    total_data = {"label": "Total Spend", "borderColor":"#3E0D49", "data": values}    
    
    # creating label data for days (x-axis) 
    labels = []
    for day in days: 
        date = str(month_int) + '/' + str(day) + '/' + str(year_int)
        labels.append(date)
    all_data = {"data": { "labels": labels, "datasets": [total_data, other_data, transportation_data, food_data, health_data, entertainment_data, shopping_data, travel_data]}, "options": { "responsive": True, "title": {"display": True, "text": "$ Spent Each Day in " + str(month_int) + "/" + str(year_int)}, "tooltips": {"mode": "index", "intersect":False}, "hover": {"mode":"nearest", "intersect": True}, "scales": {"x": {"display":True, "scaleLabel": {"display": True, "labelString": 'Day'}}, "y": { "display":True, "scaleLabel": {"display": True, "labelString": 'Amount Spent'}}}}}
    return all_data

