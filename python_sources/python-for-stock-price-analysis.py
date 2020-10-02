#!/usr/bin/env python
# coding: utf-8

# **PYTHON FOR STOCK PRICE ANALYSIS**

# ![](https://4.bp.blogspot.com/-oLOn05EMPmw/V9SzHxHrnWI/AAAAAAAAOKA/8v-0dpR0Fec4tXkjcZLleD9YfsiHOPj2wCLcB/s640/frugal-finance-bootstrap-business-lean-startup-financial-responsibility-save-money-company-entrepreneur.jpg)

# The python ecosystem allows for useful retrieval and visualizations of a variety of data. In this notebook, I'll show you how to retrieve stock data nd produce some basic visualizations!

# In[ ]:


#Setting up local directoy
import os

#Importing dependcies
import datetime as dt
import numpy as np 
import pandas as pd 
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib import style

#Style used by ggplot, R library
style.use('ggplot')

#Setting date range
start = dt.datetime(2008,1,1)
end = dt.datetime.today()

#Retrieving stock dataframe
df = web.DataReader('GE', 'yahoo', start, end)


# In[ ]:


df.head()


# In[ ]:


df.tail()


# In[ ]:


#Plotting pricing data 
df[['Open', 'Close', 'High', 'Low']].plot(figsize=(10,7))


# In[ ]:


#Plotting Trading Volume
df[['Volume']].plot(figsize=(10,7))


# These graphs are nice, but aren't full of any technical indicators. One such useful indicator we can derive from the data is the moving average of the stock price.  In effect, a moving averagegives us a "smoother" image of price changes over time that are resistant to brief fluctuations. You can find more info on moving averages here: https://www.investopedia.com/terms/m/movingaverage.asp

# In[ ]:


#Creating a 50, 100, and 200 day moving average
df['100 MA'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
df['50 MA'] = df['Adj Close'].rolling(window=50, min_periods=0).mean()
df['200 MA'] = df['Adj Close'].rolling(window=200, min_periods=0).mean()


df[['Adj Close', '100 MA', '50 MA', '200 MA']].plot(figsize=(15,7))


# Let's revisit raw price changes. Candlesticks are a more useful visualization, so we'll reconstruct the price plot with the plotyl API

# In[ ]:


#Using the plotly API
import plotly
plotly.tools.set_credentials_file(username='jtcpca', api_key='JrYvdfddTawiS9eexi32')
import plotly.plotly as py
import plotly.graph_objs as go
#Resample data for 10-day increment data
df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_ohlc.reset_index(inplace=True)
df_volume = df['Adj Close'].resample('10D').sum()



trace = go.Ohlc(x=df_ohlc['Date'],
                open=df_ohlc['open'],
                high=df_ohlc['high'],
                low=df_ohlc['low'],
                close=df_ohlc['close'])
data = [trace]
py.iplot(data, filename='simple_candlestick')


# Alright, so we have some visualizations, but there all for one stock. Not very useful. For the next section, we'll use webscarping libraries, namely Beautiful Soup (bs4) and pickle, to scrape a wikipedia page for the tickers for all companies in the S&P 500. In the following section, we'll retrieve the tickers, get pricing data for the tickers, compile our data, and demonstrate how to plot any of the data we have.

# In[ ]:


import bs4 as bs
import pickle
import requests


# In[ ]:


#Retrive S&P 500 tickers from wikipedia
def sp500():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    #In order to be able to commit this notebook, I've set the index for table.findAll('tr') to [1:101].
    #If you want every company in the S&P 500, set the index to [1:] 
    for row in table.findAll('tr')[1:101]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
        
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers, f)
        
    print(tickers)
    
    return tickers


sp500()
    
    
    


# In[ ]:


#Use stock tickers to create file of all stocks' price data
def get_data(reload_sp500 = False):
    if reload_sp500:
        tickers=sp500()
    else:
        with open("sp500tickers.pickle","rb") as f:
            tickers = pickle.load(f)
            
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    
    start = dt.datetime(2008,1,1)
    end = dt.datetime(2018,12,14)

    for ticker in tickers:
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker.replace(".", "-"), 'yahoo', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

get_data()


# In[ ]:


#Compile data from files created
def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)
        
    main_df = pd.DataFrame()
    
    for count, ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace = True)
        df.rename(columns = {'Adj Close': ticker}, inplace = True)
        df.drop(['Open','High','Low','Close','Volume'], 1, inplace = True)
        
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how = 'outer')
            
        if count%100 == 0:
            print(count)
            
    print(main_df.head())
    main_df.to_csv('sp500_compile.csv')
    
compile_data()


# In[ ]:


#Function for plotting any number of tickers
def visualize(ticker_symbol, size):
    df = pd.read_csv('sp500_compile.csv')
    df[ticker_symbol].plot(figsize=size)


# In[ ]:


visualize(['AAPL', 'AMZN'], (10, 7))

