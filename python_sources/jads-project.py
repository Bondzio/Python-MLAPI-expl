#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()

get_ipython().run_line_magic('matplotlib', 'inline')

pd.options.mode.chained_assignment = None
pd.options.display.max_columns = 999

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

import sys 
print(sys.version)


# I am importing the datasets bitcoin_price, ethereum_classic_price and ethereum_price

# In[ ]:


bitcoin = pd.read_csv('../input/bitcoin_price.csv', parse_dates= ['Date'])
ethereum = pd.read_csv('../input/ethereum_price.csv', parse_dates= ['Date'])
ethereum_classic = pd.read_csv('../input/ethereum_classic_price.csv', parse_dates= ['Date'])


# ![](http://)I am just testing the datasets inported, and having a first look on the data

# In[ ]:


bitcoin.columns


# In[ ]:


bitcoin[['Date','Close','Volume','Market Cap']].head()


# In[ ]:


ethereum[['Date','Close','Volume','Market Cap']].head()


# In[ ]:


ethereum_classic[['Date','Close','Volume','Market Cap']].head()


# selection of raws and columns, and also first approach on data extracted

# In[ ]:


bitcoin[(bitcoin['Date'] >= 'oct 01, 2016') & (bitcoin['Date'] <= 'feb 01, 2017')].head()


# In[ ]:


x = bitcoin[['Close',]][(bitcoin['Date'] == 'Sep 17, 2017')]
x


# I sorted the data sets based on the Close attribute, highest resoult 

# In[ ]:


print('*** Bitcoin ***' , '\n', bitcoin[['Date', 'Close']].sort_values('Close', ascending = False).head(1), '\n')
print('*** Ethereum ***' , '\n',ethereum[['Date', 'Close']].sort_values('Close', ascending = False).head(1), '\n')
print('*** Ethereum_classic ****', '\n', ethereum_classic[['Date', 'Close']].sort_values('Close', ascending = False).head(1))


# I sorted the data sets based on the Close attribute, lowest resoult 

# In[ ]:


print('*** Bitcoin ***' , '\n', bitcoin[['Date', 'Close']].sort_values('Close', ascending = False).tail(1), '\n')
print('*** Ethereum ***' , '\n',ethereum[['Date', 'Close']].sort_values('Close', ascending = False).tail(1), '\n')
print('*** Ethereum_classic ****', '\n', ethereum_classic[['Date', 'Close']].sort_values('Close', ascending = False).tail(1))


# First training day for bitcoin_price, ethereum_classic_price and ethereum_price

# In[ ]:


print('*** Bitcoin ***' , '\n', bitcoin[['Date', 'Close']].tail(1), '\n')
print('*** Ethereum ***' , '\n',ethereum[['Date', 'Close']].tail(1), '\n')
print('*** Ethereum_classic ****', '\n', ethereum_classic[['Date', 'Close']].tail(1))


# **BITCOIN**

# In[ ]:


import matplotlib.dates as mdates
bitcoin['Date_mpl'] = bitcoin['Date'].apply(lambda x: mdates.date2num(x))
fig, ax = plt.subplots(figsize=(12,6))
sns.tsplot(bitcoin.Close.values, time=bitcoin.Date_mpl.values, alpha=0.8, color=color[3], ax=ax)
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m.%d'))
fig.autofmt_xdate()
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price in USD', fontsize=12)
plt.title("Closing price distribution of Bitcoin", fontsize=15)
plt.show()


# Candlestick chart for Bitcoin [28 -4- 2013 to 2017-09-01]

# In[ ]:


import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc

fig = plt.figure(figsize=(12,8))
ax1 = plt.subplot2grid((1,1), (0,0))

temp_df = bitcoin[bitcoin['Date']>'2013-04-28']
ohlc = []
for ind, row in temp_df.iterrows():
    ol = [row['Date_mpl'],row['Open'], row['High'], row['Low'], row['Close'], row['Volume']]
    ohlc.append(ol)
    
candlestick_ohlc(ax1, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))

plt.xlabel("Date", fontsize=12)
plt.ylabel("Price in USD", fontsize=12)
plt.title("Candlestick chart for Bitcoin", fontsize=15)
plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
plt.show()


# **ETHEREUM**

# In[ ]:


import matplotlib.dates as mdates
ethereum['Date_mpl'] = ethereum['Date'].apply(lambda x: mdates.date2num(x))
fig, ax = plt.subplots(figsize=(12,8))
sns.tsplot(ethereum.Close.values, time=ethereum.Date_mpl.values, alpha=0.8, color=color[3], ax=ax)
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m.%d'))
fig.autofmt_xdate()
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price in USD', fontsize=12)
plt.title("Closing price distribution of Ethereum", fontsize=15)
plt.show()


# In[ ]:


import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc

fig = plt.figure(figsize=(12,8))
ax1 = plt.subplot2grid((1,1), (0,0))

temp_df = ethereum[(ethereum['Date']> '2017-01-01' )] 
ohlc = []
for ind, row in temp_df.iterrows():
    ol = [row['Date_mpl'],row['Open'], row['High'], row['Low'], row['Close'], row['Volume']]
    ohlc.append(ol)
    
candlestick_ohlc(ax1, ohlc, width=0.4, colorup='#77d879', colordown='#db3f3f')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))

plt.xlabel("Date", fontsize=12)
plt.ylabel("Price in USD", fontsize=12)
plt.title("Candlestick chart for Ethereum from 01-01-2017", fontsize=15)
plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
plt.show()


# **Ethereum Classic**

# In[ ]:


import matplotlib.dates as mdates
ethereum_classic['Date_mpl'] = ethereum_classic['Date'].apply(lambda x: mdates.date2num(x))
fig, ax = plt.subplots(figsize=(12,8))
sns.tsplot(ethereum_classic.Close.values, time=ethereum_classic.Date_mpl.values, alpha=0.8, color=color[3], ax=ax)
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m.%d'))
fig.autofmt_xdate()
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price in USD', fontsize=12)
plt.title("Closing price distribution of Ethereum Classic", fontsize=15)
plt.show()


# Let's now focus on the **variance of Bitcoin**

# In[ ]:


percent_change = []
change = []
Sevendays_change = []
price_7days_before = bitcoin['Open'][0]
for ind,row in bitcoin.iterrows():
    if ind > 7:
        price_7days_before = bitcoin['Open'][ind-7]
    change.append(row['Close'] - row['Open'])
    percent_change.append((row['Close'] - row['Open'])/row['Open'])
    Sevendays_change.append((row['Close'] - price_7days_before)/price_7days_before)
bitcoin['Change'] = change
bitcoin['percent_change'] = percent_change
bitcoin['Sevendays_change'] = Sevendays_change
bitcoin.head()


# **Change distribution of bitcoin**

# In[ ]:


#change graph
import matplotlib.dates as mdates
import seaborn as sns
import matplotlib.pyplot as plt
color = sns.color_palette()
bitcoin['Date_mpl'] = bitcoin['Date'].apply(lambda x: mdates.date2num(x))
fig, ax = plt.subplots(figsize=(12,8))
sns.tsplot(bitcoin.percent_change.values, time=bitcoin.Date_mpl.values, alpha=0.8, color=color[3], ax=ax)
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m.%d'))
fig.autofmt_xdate()
plt.xlabel('Date', fontsize=12)
plt.ylabel('Percent change', fontsize=12)
plt.title("Change distribution of bitcoin", fontsize=15)
plt.show()


# **This map describes the correlation between price of different currencies change with respect to each other.**
# 
# In the case below I choose; bitcoin_price.csv, ethereum_price.csv, neo_price.csv, stratis_price.csv and dash_price.csv but you can choose as many as you want

# In[ ]:


files_to_use = ["bitcoin_price.csv", "ethereum_price.csv", "neo_price.csv","stratis_price.csv","dash_price.csv"]

cols_to_use = []
for ind, file_name in enumerate(files_to_use):
    currency_name = file_name.split("_")[0]
    if ind == 0:
        df = pd.read_csv("../input/"+file_name, usecols=["Date", "Close"], parse_dates=["Date"])
        df.columns = ["Date", currency_name]
    else:
        temp_df = pd.read_csv("../input/"+file_name, usecols=["Date", "Close"], parse_dates=["Date"])
        temp_df.columns = ["Date", currency_name]
        df = pd.merge(df, temp_df, on="Date")
    cols_to_use.append(currency_name)
df.head()
        
temp_df = df[cols_to_use]
corrmat = temp_df.corr(method='spearman')
fig, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(corrmat, vmax=1., square=True)
plt.title("Cryptocurrency correlation map", fontsize=15)
plt.show()


# In[ ]:


INPUT_FILE = "bitcoin_price.csv"

from fbprophet import Prophet
# df is the data set with only date and close
df = pd.read_csv("../input/" + INPUT_FILE, parse_dates=['Date'], usecols=["Date", "Close"])
df.columns = ["ds", "y"]

m = Prophet()
m.fit(df);
future = m.make_future_dataframe(periods=30)
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()


# In[ ]:


len(forecast.yhat[:-30]), len(df.y)


# In[ ]:


forecast[['ds', 'yhat']].tail(10)


# In[ ]:


df.head(10)


# In[ ]:


merge = pd.merge(forecast.yhat[:-30], df.y, on = 'ds')


# In[ ]:


m.plot(forecast)

