#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.arima_model import ARIMA
from pandas.tseries.offsets import DateOffset

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

# Suppress warnings 
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


df = pd.read_csv('../input/liver-transplant-waiting-list/transplant.csv')
df.head()


# In[ ]:


df1=df.groupby('sex').groups
df1


# In[ ]:


df1=df.groupby('abo').groups
df1


# In[ ]:


plt.clf()
df.groupby('sex').size().plot(kind='bar')
plt.show()


# In[ ]:


plt.clf()
df.groupby('event').size().plot(kind='bar')
plt.show()


# In[ ]:


plt.clf()
df.groupby('abo').size().plot(kind='bar')
plt.show()

