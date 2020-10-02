#!/usr/bin/env python
# coding: utf-8

# In this notebook, we will be using quantitative analysis and technical analysis techniques often used in finance to visualize trend strength and volatility. Though, in this notebook, I am simply plotting the techniques, I hope this will inspire some creative feature engineering.

# In[ ]:


#data manipulation packages
import pandas as pd
import numpy as np
import scipy
import re

#visualization tools
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import matplotlib.pyplot as plt
from itertools import cycle

import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_rows', 300)


# In[ ]:


sales = pd.read_csv('/kaggle/input/m5-forecasting-accuracy/sales_train_validation.csv')
cal = pd.read_csv('/kaggle/input/m5-forecasting-accuracy/calendar.csv')
prices = pd.read_csv('/kaggle/input/m5-forecasting-accuracy/sell_prices.csv')


# For the sake of simplicity, we will choose a random item to demonstrate how the different quantitative and TA graphs play out.

# In[ ]:


item = 'FOODS_3_090_CA_3_validation'
d_cols = [col for col in sales.columns if 'd_' in col]


# ### 2-STD Bollinger Bands

# One way to detect outliers, or unexpected volatility, is through the use of bollinger bands - bands two standard deviations above and below the item's window mean. Those that are outside the bands will be deamed outliers.

# In[ ]:


def plot_bollinger_bands(item):
    '''bollinger bands around the 50-day rolling mean items sold per day for specified item.
    Args:
        item(str): id of the item we are wanting to plot.
    
    Returns:
        line plot of item sale history as well as 50-day rolling standard deviation of the time series (2):
    '''
    item_df = sales.loc[sales['id'] == item][d_cols].T
    item_df = item_df.rename(columns={sales.index[sales['id']==item].to_list()[0]:item}) # Name it correctly
    item_df = item_df.reset_index().rename(columns={'index': 'd'}) # make the index "d"
    item_df['mean'] = item_df[item].rolling(window=50).mean()
    item_df['std'] = item_df[item].rolling(window=50).std()
    item_df['upper_band'] = item_df['mean'] + (item_df['std'] * 2)
    item_df['lower_band'] = item_df['mean'] - (item_df['std'] * 2)
    
    item_df[[item, 'mean', 'upper_band', 'lower_band']].plot(figsize=(15,8))
    plt.grid(linestyle='-', linewidth='1')
    plt.title('30 Day Bollinger Band for {}'.format(item))
    plt.ylabel('Number of Times the Item is Sold')
    plt.xlabel('Day')
    plt.show()


# In[ ]:


plot_bollinger_bands(item)


# We can see tha there are many instances in which the actual sales is outside of the bands.

# ## Relative Rotation

# To get really familiar with the item's strength - relative to it's category - , we can plot a Relative Rotation Graph. This locates the an item's relative strength and momentum from one period to another, and is compared to those properties of the benchmark (item's category aggregated stats). The direction of the property is important; each quadrant illustrates if the item's selling history is leading, lagging, weakening, or improving. The ideal formation is that the item's relative strength and momentum are both above 100, and is heading in the direction of the leading quadrant. The graph created below should help clarify.

# In[ ]:


def plot_RRG(item_cat, window):
    '''Relative Rotation Graph (RRG) of a sample of items and its categories. RRGs are made 
    of an item's/category's relative strength and momentum.
    
    Args:
        item(str): id of the item we are wanting to plot.
        window(int): window to to roll over.
    
    Returns:
        RRG of item nad it's category. This RRG takes advantage of a simple moving average.
    '''
    colors = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])
    
    category = sales.loc[sales['id']==item_cat]['cat_id']
    benchmark = sales.loc[sales['cat_id'].isin(category)][d_cols].mean(axis=0).T
    benchmark = pd.DataFrame({'mean_values':benchmark.values})
    
    
    # Get the difference in price from previous step
    benchmark_delta = benchmark.diff().dropna()
    # Get rid of the first row, which is NaN since it did not have a previous 
    # row to calculate the differences  
    benchmark_delta = benchmark_delta[1:]
    # Make the positive gains (up) and negative gains (down) Series
    b_up, b_down = benchmark_delta.copy(), benchmark_delta.copy()
    b_up[b_up < 0] = 0
    b_down[b_down > 0] = 0
    
    #Calculate SMA
    b_roll_up2 = b_up.rolling(window).mean()
    b_roll_down2 = b_down.abs().rolling(window).mean()  

    b_RS2 = b_roll_up2 / b_roll_down2
#     b_RSI2 = 100.0 - (100.0 / (1.0 + b_RS2))
    benchmark['jdk_rs'] = 100 + ((b_RS2 - b_RS2.mean()) / b_RS2.std() + 1)
    
    b_mom = benchmark.iloc[:,0].diff(periods = window)
    benchmark['jdk_mom'] = 100 + ((b_mom - b_mom.mean()) / b_mom.std() + 1)
    
    
    #Repeat steps for a sample of items in that category
#     series_sample = sales.loc[sales['cat_id'].isin(category)]['id'].sample(sample)#grab sample of items
    
    series = sales.loc[sales['id'] == item][d_cols].T

    # Get the difference in price from previous step
    item_delta = series.diff().dropna()

    item_delta = item_delta[1:] 

    # Make the positive gains (up) and negative gains (down) Series
    i_up, i_down = item_delta.copy(), item_delta.copy()
    i_up[i_up < 0] = 0
    i_down[i_down > 0] = 0

    # Calculate the EWMA
#     roll_up1 = up.ewm(span=window).mean()
#     roll_down1 = down.abs().ewm(span=window).mean()

#     # Calculate the RSI based on EWMA
#     RS1 = roll_up1 / roll_down1
#     RSI1 = 100.0 - (100.0 / (1.0 + RS1))

    # Calculate the SMA
    i_roll_up2 = i_up.rolling(window).mean()
    i_roll_down2 = i_down.abs().rolling(window).mean()

    # Calculate the RSI based on SMA
    i_RS2 = i_roll_up2 / i_roll_down2
#     i_RSI2 = 100.0 - (100.0 / (1.0 + i_RS2))
    series['jdk_rs'] = 100 + ((i_RS2 - i_RS2.mean()) / i_RS2.std() + 1)

    i_mom = series.iloc[:,0].diff(periods = window)

    series['jdk_mom'] = 100 + ((i_mom - i_mom.mean()) / i_mom.std() + 1)
    
    from scipy.interpolate import interp1d
    from matplotlib.patches import ConnectionPatch, FancyArrowPatch
    
    ix = series.iloc[::220]['jdk_rs'].values
    iy = series.iloc[::220]["jdk_mom"].values
    
    bx = benchmark.iloc[::150, benchmark.columns.get_loc("jdk_rs")].values
    by = benchmark.iloc[::150, benchmark.columns.get_loc("jdk_mom")].values
    
    improving_lagging = np.linspace(94,       
                     100, 
                     1000)
    leading_weaking = np.linspace(100,       
                     106, 
                     1000)

    
    b_origin=(bx[-2],by[-2])
    bxy =(bx[-1],by[-1])
    
    i_origin=(ix[-2],iy[-2])
    ixy =(ix[-1],iy[-1])
    

    #plotting RRG in steps of 150 days
    fig, axes = plt.subplots(1,1, figsize=(25,10), dpi=100)
    plt.scatter(bx,by, marker='o', label='Benchmark', color='red')
    plt.scatter(ix,iy, marker='o', label = 'Item', color=next(colors))
    axes.set_axisbelow(True)
    axes.grid(linestyle='-', linewidth='2.0')
    plt.xlim(95,105)
    plt.ylim(95,105)
    plt.axhline(100, linewidth=4, color='b')  #horizontal line
    plt.axvline(100, linewidth=4, color='b')
    plt.gca().fill_between(improving_lagging, 
                           100, 
                           106.5, 
                           alpha=0.1, color='b', zorder=3, label='Improving')
    plt.gca().fill_between(leading_weaking, 
                           100, 
                           106.5, 
                           alpha=0.1, color='g', zorder=4, label='Leading')
    plt.gca().fill_between(leading_weaking, 
                           94, 
                           100, 
                           alpha=0.1, color='y', zorder=5, label='Weakening')
    plt.gca().fill_between(improving_lagging, 
                           94, 
                           100, 
                           alpha=0.1, color='r', zorder=6, label='Lagging')
    plt.quiver(b_origin[0], b_origin[1], bxy[0]-b_origin[0], bxy[1]-b_origin[1],
               scale_units='xy', angles='xy',alpha=.9, scale=1, pivot='tip', width=.0025, headlength = 4.5, headwidth=3, color='maroon')
    plt.quiver(i_origin[0], i_origin[1], ixy[0]-i_origin[0], ixy[1]-i_origin[1],
               scale_units='xy', angles='xy',alpha=.9, scale=1, pivot='tip', width=.0025, headlength = 4.5, headwidth=3, color='royalblue')
    plt.xlabel('JDK Relative Strength', fontsize=14)
    plt.ylabel('JDK Momentum', fontsize=14)
    plt.legend(fontsize='xx-large')
    plt.title('Relative Rotation Graph for Item Category', fontsize=25)


# In[ ]:


plot_RRG('FOODS_3_090_CA_3_validation', 350)


# In the above example, we can see that this particular item start out in the middle of the graph, but gradually moves to the leading quadrant, which signals progressing sales momentum and strength. The item's benchmark (average of all food items) is also leading quandrant. Since the benchmark is further from the middle, it looks the average food item is performing better than this particular item.
# 
# The vectors represent the direction the item and benchmark are heading compared to the last period the RRG was calculated. The item is heading further in the leading quadrant (which is promising) while the benchmark is regressing closer to the middle (not a good sign).

# ## Average True Range

# Below we will add an Average True Range (ATR) plot. This feature measures the trendiness of the data; the higher the ATR value, the more the item sales are trending in either direction.

# In[ ]:


#Volatility measure
def wwma(values, window):
    """
     J. Welles Wilder's EMA 
    """
    return values.ewm(alpha=1/window, adjust=False).mean()

def ATR(item, window):
    
    item_df = sales.loc[sales['id'] == item][d_cols].T
    item_wwma = item_df.ewm(alpha=1/window, adjust=False).mean() #Wilder's EMA
        
    high = item_df.rolling(window).max()
    low = item_df.rolling(window).min()
    close = item_df.rolling(window).mean()
    item_df['tr0'] = abs(high - low)
    item_df['tr1'] = abs(high - close.shift())
    item_df['tr2'] = abs(low - close.shift())
    tr = item_df[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = wwma(tr, window)
    return atr



item = 'HOBBIES_1_004_CA_1_validation'

item_atr = ATR(item, 60)

fig, axes = plt.subplots(1,1, figsize=(15,8), dpi=100)
item_atr.plot()
axes.grid(linestyle='-', linewidth='1.0')
plt.xlabel('Day')
plt.ylabel('True Range')
plt.title('%s Average True Range (ATR)'% item)


# We can see that near d_1000 that the item sales begins to trend before tailing off at the end. This matches the upwards trend we observe when we just simply plot item sales over time or category sales (all items in the category averaged) over time.

# ## Relative Strength Index

# Another metric we can plot out is the item's relative strength, which shows how well the item is selling within its window. Relative strength is the percentage of days that experienced higher selling than the previous day to the percentage of that experience lower selling than the previous day.

# In[ ]:


def plot_RSI(item, window, category=False):
    '''Relative strength of specified item compared to the average relative strength of all items in its category.
    
    Args:
        item(str): id of the item we are wanting to plot.
        window(int): number of days we want to average over.
        category(bool): whether or not we are finding the RS of an item or a category.
    
    Returns:
        Relative strength of item or category.
    '''
    if category == True:
        category = sales.loc[sales['id']==item]['cat_id']
        series = sales.loc[sales['cat_id'].isin(category)][d_cols].mean(axis=0).T
    else:
        series = sales.loc[sales['id'] == item][d_cols].T
    
    # Get the difference in price from previous step
    delta = series.diff().dropna()
    # Get rid of the first row, which is NaN since it did not have a previous 
    # row to calculate the differences
    delta = delta[1:] 

    # Make the positive gains (up) and negative gains (down) Series
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    # Calculate the EWMA
    roll_up1 = up.ewm(span=window).mean()
    roll_down1 = down.abs().ewm(span=window).mean()

    # Calculate the RSI based on EWMA
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))

    # Calculate the SMA
    roll_up2 = up.rolling(window).mean()
    roll_down2 = down.abs().rolling(window).mean()

    # Calculate the RSI based on SMA
    RS2 = roll_up2 / roll_down2
    RSI2 = 100.0 - (100.0 / (1.0 + RS2))

    # Compare graphically
    fig, axes = plt.subplots(1, 1, figsize=(15, 6), dpi=100)
    RSI1.plot(ax=axes, label='EWMA of Item Sold', alpha=0.8).set_ylabel('RS Index', fontsize=14)
    RSI2.plot(ax=axes, label='SMA of Item Sold', alpha=0.8).set_ylabel('RSI Index', fontsize=14)
    axes.set_title('Relative Strength (using EWMA and SMA) of Item', fontsize=16);
    axes.grid(linestyle='-', linewidth='1')
    axes.legend(['RSI via EWMA', 'RSI via SMA'])


# In[ ]:


plot_RSI(item, 20, category=True)


# Based on the graph, we can see that both the simple moving average and the exponentially weighted moving avg hover around the 50 mark - give or take 10. This suggest that, throughout the time period, the item's sales experience consistent fluctuations of up days (# of the item sales is higher than the day before) and down days (# of the item sales is lower than the day before).

# ## Annualized Volatility

# Annualized volatility - a popular metric used in finance that presents item sales volatility in annualized terms; we multiply our daily standard deviation by sq root of 365 days.

# In[ ]:


def annualized_volatility(item, window):
    "Return the annualized standard deviation of daily log returns of item."
    
    item_df = sales.loc[sales['id'] == item][d_cols].T
    ann_vol = item_df.diff().rolling(window).std()*(365**0.5)
    return ann_vol

item_ann = annualized_volatility(item, 30)

fig, axes = plt.subplots(1,1, figsize=(15,8), dpi=100)
item_ann.plot(ax=axes)
axes.grid(linestyle='-', linewidth='1.0')
plt.xlabel('Day')
plt.ylabel('Volatility')
plt.title('%s Annualized Volatility'% item)
plt.legend(item)
plt.show()


# Based on the graph above, we can see that the annualized volatility increases over time as the item experiences more and more sales.

# ## Semivariance

# Lastly, we will consider an item's semivariance. This is the item's downside sales volatililty. It is a risk measurement, so it isolates the variance of sales below the item's sales mean.

# In[ ]:


series = sales.loc[sales['id']==item][d_cols].T
series = series.rename(columns={sales.index[sales['id']==item].to_list()[0]:item})
series['mean'] = series[item].rolling(30).mean().fillna(series[item].mean())
series.fillna(method='ffill', inplace=True)
series.loc[series[item]<series['mean'], 'semivariance'] = series[item].rolling(30).var()
series.semivariance.isna().sum()


# In[ ]:


def semivariance(item, w1, w2):
    '''
    Semivariance records the variance of sales that fall below the sales average of a period of time.
    '''
    
    series = sales.loc[sales['id']==item][d_cols].T
    series = series.rename(columns={sales.index[sales['id']==item].to_list()[0]:item})
    series['mean'] = series[item].rolling(w1).mean().fillna(series[item].mean())
    series.loc[series[item]<series['mean'], 'semivariance'] = series[item].rolling(w2).var()
    series.fillna(method='ffill', inplace=True)
    return series['semivariance']

item_semi = semivariance(item, 30, 30)

fig, axes = plt.subplots(1,1, figsize=(15,8), dpi=100)
item_semi.plot(ax=axes)
axes.grid(linestyle='-', linewidth='1.0')
plt.xlabel('Day')
plt.ylabel('Volatility')
plt.title('%s Annualized Volatility'% item)
plt.legend(item)
plt.show()


# I hope these metrics give you some idea of how to incororate strength and volatility in your feature engineering.
# 
# Other quantitative analysis ideas could be item-to-benchmark beta, triple exp. moving average (TEMA), relative volatility (comparing volatility of item sales over two different moving avg windows), or even entropy.
