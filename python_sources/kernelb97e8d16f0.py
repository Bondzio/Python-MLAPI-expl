#!/usr/bin/env python
# coding: utf-8

# In[15]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from fbprophet import Prophet

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

all_cities = pd.read_csv("../input/temperature.csv")
chicago = pd.DataFrame({'ds': all_cities['datetime'], 'y': all_cities['Chicago']})
chicago.head()
# Any results you write to the current directory are saved as output.


# In[17]:


m = Prophet()
m.fit(chicago)


# In[18]:


future = m.make_future_dataframe(periods=365)
future.tail()


# In[19]:


forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()


# In[20]:


fig1 = m.plot(forecast)


# In[21]:


fig2 = m.plot_components(forecast)

