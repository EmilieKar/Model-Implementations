import numpy as np
import copy
import pandas as pd 
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

# For each model in input calculate cumulative return and total profit
def analyze(data_df, model_names, model_res):
    df = copy.copy(data_df)
    open_values = df['Open'].values

    for model_idx in range(len(model_names)):
        df[model_names[model_idx]] = model_res[model_idx]
        nmb_owned_stocks = model_res[model_idx]
        df[f'daily_val: {model_names[model_idx]}'] = df['Open'] * df[model_names[model_idx]]
        daily_values = df[f'daily_val: {model_names[model_idx]}'].values

        cumulative_ret = [0]
        cumulative_gain = [0]
        tot_return = 1
        tot_gain = 0

        for i in range(1, len(daily_values)):
            # If we currently do not have any invested money
            if daily_values[i-1] == 0:
                pass

            # If we've changed investment (bought or sold)
            elif nmb_owned_stocks[i] != nmb_owned_stocks[i-1]:
                tot_return *= (nmb_owned_stocks[i-1]*open_values[i])/ daily_values[i-1]
                tot_gain += (nmb_owned_stocks[i-1]*open_values[i]) - daily_values[i-1]

            else:
                tot_return *= (daily_values[i]/daily_values[i-1])
                tot_gain += daily_values[i] - daily_values[i-1]

            cumulative_ret.append(tot_return - 1)
            cumulative_gain.append(tot_gain)

        df[f'cum_ret: {model_names[model_idx]}'] = cumulative_ret
        df[f'tot_prof: {model_names[model_idx]}'] = cumulative_gain
    return df

# Everything again but different
def multi_analyze(stock_dfs, stock_names, model_names, model_res):
    df = pd.DataFrame()
    ret_df = copy.copy(stock_dfs[0])

    # Add open values of all stocks to df
    for stock_idx in range(len(stock_names)):
        df[f'open:{stock_names[stock_idx]}'] = stock_dfs[stock_idx].Open
    
    for model_idx in range(len(model_names)):
        model = model_names[model_idx]

        for stock_idx in range(len(stock_dfs)):
            stock = stock_names[stock_idx]

            open_values = df[f'open:{stock}'].values
            df[f'{model}:{stock}'] = model_res[model_idx][stock_idx]
            nmb_owned_stocks = model_res[model_idx][stock_idx]
            df[f'daily_val: {model}:{stock}'] = df[f'open:{stock}'] * df[f'{model}:{stock}']
            daily_values = df[f'daily_val: {model}:{stock}'].values
            
            ret = [0]
            cumulative_profit = [0]
            tot_return = 1
            tot_profit = 0

            for i in range(1, len(daily_values)):
                # If we currently do not have any invested money
                if daily_values[i-1] == 0:
                    pass

                # If we've changed investment (bought or sold)
                elif nmb_owned_stocks[i] != nmb_owned_stocks[i-1]:
                    tot_return = (nmb_owned_stocks[i-1]*open_values[i])/ daily_values[i-1]
                    tot_profit += (nmb_owned_stocks[i-1]*open_values[i]) - daily_values[i-1]

                else:
                    tot_return = (daily_values[i]/daily_values[i-1])
                    tot_profit += daily_values[i] - daily_values[i-1]

                ret.append(tot_return)
                cumulative_profit.append(tot_profit)

            df[f'ret: {stock}, {model}'] = ret
            df[f'tot_prof: {stock}, {model}'] = cumulative_profit
        
        df['Portfolio value'] = [0 for _ in range(len(df.index))]
        for stock in stock_names:
            df['Portfolio value'] = df['Portfolio value'] + df[f'daily_val: {model}:{stock}']

        
        df[f'ret: {model}'] = [0 for _ in range(len(df.index))]
        ret_df[f'tot_prof: {model}'] = [0 for _ in range(len(df.index))]

        for stock in stock_names: 
            df[f'ret: {model}'] = df[f'ret: {model}'] + df[f'ret: {stock}, {model}'] * (df[f'daily_val: {model}:{stock}'] / df['Portfolio value']) 
            ret_df[f'tot_prof: {model}'] = ret_df[f'tot_prof: {model}'] + df[f'tot_prof: {stock}, {model}'].values
                 
        daily_ret = df[f'ret: {model}'].values
        cumulative_ret = [0]
        cum_ret = 1
        for i in range(1, len(df.index)):
            cum_ret *= daily_ret[i]
            cumulative_ret.append(cum_ret -1)

        ret_df[f'cum_ret: {model}'] = cumulative_ret

    return ret_df

# Plot a linechart of cumulative return for all models in model names 
def plot_cum_ret(df, model_names):
    plot_df = pd.DataFrame()
    for model in model_names:
        plot_df[model] = df[f'cum_ret: {model}']

    sns.set(rc={"figure.figsize":(16, 6)})
    sns.lineplot(data=plot_df)
    plt.ylabel("Factor")
    plt.title("Cumulative return")
    plt.show()

# Plot a linechart of total profit for all models in model names 
def plot_tot_prof(df, model_names):
    plot_df = pd.DataFrame()
    for model in model_names:
        plot_df[model] = df[f'tot_prof: {model}']

    sns.set(rc={"figure.figsize":(16, 6)})
    sns.lineplot(data=plot_df)
    plt.ylabel("USD")
    plt.title("Total profit")
    plt.show()

# Model an input by 10 days open price and if set1 got higher % profit next day then y = 1, if set2 got higher % profit next day y = 0
# Also adds few more spans e.g. 5 days to today into the vector
# X is (set1%up/set2%up) -1 daily for 10 days and a few larger intervalls.
# This represents how much better set 1 has done compared to set 2 in %.
def getXandYVectorExtra(set1,set2):
    X = []
    y = []
    for i in range(len(set1)-11):
        # x will be % up or down compared to yesterday.
        x = [((set1[i+1]/set1[i])/(set2[i+1]/set2[i]))-1 , ((set1[i+2]/set1[i+1])/(set2[i+2]/set2[i+1]))-1 , ((set1[i+3]/set1[i+2])/(set2[i+3]/set2[i+2]))-1 , ((set1[i+4]/set1[i+3])/(set2[i+4]/set2[i+3]))-1 , ((set1[i+5]/set1[i+4])/(set2[i+5]/set2[i+4]))-1 , ((set1[i+6]/set1[i+5])/(set2[i+6]/set2[i+5]))-1 , ((set1[i+7]/set1[i+6])/(set2[i+7]/set2[i+6]))-1 , ((set1[i+8]/set1[i+7])/(set2[i+8]/set2[i+7]))-1 , ((set1[i+9]/set1[i+8])/(set2[i+9]/set2[i+8]))-1 , ((set1[i+10]/set1[i+9])/(set2[i+10]/set2[i+9]))-1 , ((set1[i+10]/set1[i+2])/(set2[i+10]/set2[i+2]))-1 , ((set1[i+10]/set1[i+5])/(set2[i+10]/set2[i+5]))-1 , ((set1[i+10]/set1[i+7])/(set2[i+10]/set2[i+7]))-1]
        X.append(x)
        if set1[i+11]/set1[i+10] > set2[i+11]/set2[i+10]:
            y.append(1)
        else:
            y.append(0)
    X = np.array(X)
    y = np.array(y)
    return X,y

# Model an input by 10 days open price and if set1 got higher % profit next day then y = 1, if set2 got higher % profit next day y = 0
# X is (set1%up/set2%up) -1 daily for 10 days and a few larger intervalls.
# This represents how much better set 1 has done compared to set 2 in %.
def getXandYVector(set1,set2):
    X = []
    y = []
    for i in range(len(set1)-11):
        # x will be % up or down compared to yesterday.
        x = [((set1[i+1]/set1[i])/(set2[i+1]/set2[i]))-1 , ((set1[i+2]/set1[i+1])/(set2[i+2]/set2[i+1]))-1 , ((set1[i+3]/set1[i+2])/(set2[i+3]/set2[i+2]))-1 , ((set1[i+4]/set1[i+3])/(set2[i+4]/set2[i+3]))-1 , ((set1[i+5]/set1[i+4])/(set2[i+5]/set2[i+4]))-1 , ((set1[i+6]/set1[i+5])/(set2[i+6]/set2[i+5]))-1 , ((set1[i+7]/set1[i+6])/(set2[i+7]/set2[i+6]))-1 , ((set1[i+8]/set1[i+7])/(set2[i+8]/set2[i+7]))-1 , ((set1[i+9]/set1[i+8])/(set2[i+9]/set2[i+8]))-1 , ((set1[i+10]/set1[i+9])/(set2[i+10]/set2[i+9]))-1]
        X.append(x)
        if set1[i+11]/set1[i+10] > set2[i+11]/set2[i+10]:
            y.append(1)
        else:
            y.append(0)
    X = np.array(X)
    y = np.array(y)
    return X,y


# Create new lists with only open price and removed missing data that does not exist in both data sets
# Given frames should have open price on index 0,
# AND must be sorted earlier -> later time.
def nonMatchRemoveToVector(set1, set2):
    matched1 = []
    matched2 = []
    i = 0
    j = 0
    while(i < len(set1)-1 and j < len(set2)-1):
        if set1.iloc[i].name == set2.iloc[j].name: # if time is same add data (open price)
            matched1.append(set1.iloc[i,0])
            matched2.append(set2.iloc[j,0])
            i = i+1
            j = j+1
        if set2.iloc[j].name > set1.iloc[i].name: # if set2 ahead set1 needs to catch up
            i = i+1
        if set2.iloc[j].name < set1.iloc[i].name: # if set1 ahead set2 needs to catch up
            j = j+1
    return matched1, matched2

# Removes missing data that does not exist in both data sets
# Given frames should have open price on index 0,
# AND must be sorted earlier -> later time.

def nonMatchRemoveDF(set1, set2):
    i = 0
    while(i < len(set1)-1 and i < len(set2)-1):
        if set1.iloc[i].name == set2.iloc[i].name: # if time is same add data (open price)
            i = i+1
        if set2.iloc[i].name > set1.iloc[i].name: # if set2 ahead set1 needs to catch up
            set1 = set1.drop(set1.iloc[i].name, axis=0)
            
        if set2.iloc[i].name < set1.iloc[i].name: # if set1 ahead set2 needs to catch up
            set2 = set2.drop(set2.iloc[i].name, axis=0)
    return set1, set2
"""
def nonMatchRemoveDF(set1, set2):
    i = 0
    df_1 = copy.copy(set1)
    df_2 = copy.copy(set2)
    df_1.reset_index(inplace = True)
    df_2.reset_index(inplace = True)
    date_idx = df_1.columns.get_loc('Date')

    while(i < len(df_1)-1 and i < len(df_2)-1):
        
        if df_1.iloc[i, date_idx] == df_2.iloc[i, date_idx]: # if time is same add data (open price)
            i = i+1
        if df_2.iloc[i, date_idx] > df_1.iloc[i, date_idx]: # if set2 ahead set1 needs to catch up
            df_1.drop(index = i, axis=0, inplace = True)
            
        if df_2.iloc[i, date_idx] < df_1.iloc[i, date_idx]: # if set1 ahead set2 needs to catch up
            df_2.drop(index = i, axis=0, inplace = True)

    df_1.set_index('Date', inplace = True)
    df_2.set_index('Date', inplace = True)
    return df_1, df_2
"""

def getXandY4Sets(set1,set2, set3, set4):
    X = []
    y = []
    for i in range(len(set1)-31):
        # x will be % up or down compared to yesterday.
        x = [
            [(set1[i+1]/set1[i])-1 , (set2[i+1]/set2[i])-1, (set3[i+1]/set3[i])-1 , (set4[i+1]/set4[i])-1],
            [(set1[i+2]/set1[i+1])-1 , (set2[i+2]/set2[i+1])-1 , (set3[i+2]/set3[i+1])-1 , (set4[i+2]/set4[i+1])-1],
            [(set1[i+3]/set1[i+2])-1 , (set2[i+3]/set2[i+2])-1 , (set3[i+3]/set3[i+2])-1 , (set4[i+3]/set4[i+2])-1],
            [(set1[i+4]/set1[i+3])-1 , (set2[i+4]/set2[i+3])-1 , (set3[i+4]/set3[i+3])-1 , (set4[i+4]/set4[i+3])-1],
            [(set1[i+5]/set1[i+4])-1 , (set2[i+5]/set2[i+4])-1 , (set3[i+5]/set3[i+4])-1 , (set4[i+5]/set4[i+4])-1],
            [(set1[i+6]/set1[i+5])-1 , (set2[i+6]/set2[i+5])-1 , (set3[i+6]/set3[i+5])-1 , (set4[i+6]/set4[i+5])-1],
            [(set1[i+7]/set1[i+6])-1 , (set2[i+7]/set2[i+6])-1 , (set3[i+7]/set3[i+6])-1 , (set4[i+7]/set4[i+6])-1],
            [(set1[i+8]/set1[i+7])-1 , (set2[i+8]/set2[i+7])-1 , (set3[i+8]/set3[i+7])-1 , (set4[i+8]/set4[i+7])-1],
            [(set1[i+9]/set1[i+8])-1 , (set2[i+9]/set2[i+8])-1 , (set3[i+9]/set3[i+8])-1 , (set4[i+9]/set4[i+8])-1],
            [(set1[i+10]/set1[i+9])-1 , (set2[i+10]/set2[i+9])-1, (set3[i+10]/set3[i+9])-1 , (set4[i+10]/set4[i+9])-1],
            [(set1[i+11]/set1[i+10])-1 , (set2[i+11]/set2[i+10])-1, (set3[i+11]/set3[i+10])-1 , (set4[i+11]/set4[i+10])-1],
            [(set1[i+12]/set1[i+11])-1 , (set2[i+12]/set2[i+11])-1, (set3[i+12]/set3[i+11])-1 , (set4[i+12]/set4[i+11])-1],
            [(set1[i+13]/set1[i+12])-1 , (set2[i+13]/set2[i+12])-1, (set3[i+13]/set3[i+12])-1 , (set4[i+13]/set4[i+12])-1],
            [(set1[i+14]/set1[i+13])-1 , (set2[i+14]/set2[i+13])-1, (set3[i+14]/set3[i+13])-1 , (set4[i+14]/set4[i+13])-1],
            [(set1[i+15]/set1[i+14])-1 , (set2[i+15]/set2[i+14])-1, (set3[i+15]/set3[i+14])-1 , (set4[i+15]/set4[i+14])-1],
            [(set1[i+16]/set1[i+15])-1 , (set2[i+16]/set2[i+15])-1, (set3[i+16]/set3[i+15])-1 , (set4[i+16]/set4[i+15])-1],
            [(set1[i+17]/set1[i+16])-1 , (set2[i+17]/set2[i+16])-1, (set3[i+17]/set3[i+16])-1 , (set4[i+17]/set4[i+16])-1],
            [(set1[i+18]/set1[i+17])-1 , (set2[i+18]/set2[i+17])-1, (set3[i+18]/set3[i+17])-1 , (set4[i+18]/set4[i+17])-1],
            [(set1[i+19]/set1[i+18])-1 , (set2[i+19]/set2[i+18])-1, (set3[i+19]/set3[i+18])-1 , (set4[i+19]/set4[i+18])-1],
            [(set1[i+20]/set1[i+19])-1 , (set2[i+20]/set2[i+19])-1, (set3[i+20]/set3[i+19])-1 , (set4[i+20]/set4[i+19])-1],
            [(set1[i+21]/set1[i+20])-1 , (set2[i+21]/set2[i+20])-1, (set3[i+21]/set3[i+20])-1 , (set4[i+21]/set4[i+20])-1],
            [(set1[i+22]/set1[i+21])-1 , (set2[i+22]/set2[i+21])-1, (set3[i+22]/set3[i+21])-1 , (set4[i+22]/set4[i+21])-1],
            [(set1[i+23]/set1[i+22])-1 , (set2[i+23]/set2[i+22])-1, (set3[i+23]/set3[i+22])-1 , (set4[i+23]/set4[i+22])-1],
            [(set1[i+24]/set1[i+23])-1 , (set2[i+24]/set2[i+23])-1, (set3[i+24]/set3[i+23])-1 , (set4[i+24]/set4[i+23])-1],
            [(set1[i+25]/set1[i+24])-1 , (set2[i+25]/set2[i+24])-1, (set3[i+25]/set3[i+24])-1 , (set4[i+25]/set4[i+24])-1],
            [(set1[i+26]/set1[i+25])-1 , (set2[i+26]/set2[i+25])-1, (set3[i+26]/set3[i+25])-1 , (set4[i+26]/set4[i+25])-1],
            [(set1[i+27]/set1[i+26])-1 , (set2[i+27]/set2[i+26])-1, (set3[i+27]/set3[i+26])-1 , (set4[i+27]/set4[i+26])-1],
            [(set1[i+28]/set1[i+27])-1 , (set2[i+28]/set2[i+27])-1, (set3[i+28]/set3[i+27])-1 , (set4[i+28]/set4[i+27])-1],
            [(set1[i+29]/set1[i+28])-1 , (set2[i+29]/set2[i+28])-1, (set3[i+29]/set3[i+28])-1 , (set4[i+29]/set4[i+28])-1],
            [(set1[i+30]/set1[i+29])-1 , (set2[i+30]/set2[i+29])-1, (set3[i+30]/set3[i+29])-1, (set4[i+30]/set4[i+29])-1]
            ]
        X.append(x)
        nextValues = [set1[i+31]/set1[i+30], set2[i+31]/set2[i+30], set3[i+31]/set3[i+30], set4[i+31]/set4[i+30]]
        idxMax = max(range(len(nextValues)), key = nextValues.__getitem__)
        new = [0,0,0,0]
        new[idxMax] = 1
        y.append(idxMax)
    X = np.array(X)
    y = np.array(y)
    return X,y