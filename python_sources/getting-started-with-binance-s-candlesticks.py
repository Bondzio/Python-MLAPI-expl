#!/usr/bin/env python
# coding: utf-8

# # Libraries and configuration

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = 30, 10


# # Cleaning
# This quick cleaning function converts the columns to their most useful datatype.

# In[ ]:


def quick_clean(df):
    """convert all columns to their proper dtype"""

    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df = df.set_index('open_time', drop=True)

    df = df.astype(dtype={
        'open': 'float64',
        'high': 'float64',
        'low': 'float64',
        'close': 'float64',
        'volume': 'float64',
        'close_time': 'datetime64[ms]',
        'quote_asset_volume': 'float64',
        'number_of_trades': 'int64',
        'taker_buy_base_asset_volume': 'float64',
        'taker_buy_quote_asset_volume': 'float64',
        'ignore': 'float64'
    })
    
    return df


# In[ ]:


df = quick_clean(pd.read_csv('/kaggle/input/binance-full-history/ETH-BTC.csv'))


# In[ ]:


df


# # Indicators and Plot
# Let's add some technical indicators and plot them together with the opening price.

# In[ ]:


# window of minutes times hours times days
window = 60 * 24 * 50
df['moving_average'] = df['open'].rolling(window).mean()


# In[ ]:


df[['open', 'moving_average']].plot(title='ETH BTC', color=['black', 'red', 'green'])


# In[ ]:


ax = df['volume'].plot(title='ETH BTC', color='black', legend=True)
df['number_of_trades'].plot(title='ETH BTC', color='gold', legend=True, ax=ax)

