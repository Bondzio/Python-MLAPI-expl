#!/usr/bin/env python
# coding: utf-8

# Hello! This is my first attempt at data science in Kaggle. Please feel free to offer any suggestions as to how I can improve my methods, my style, or if there's anything missing that I should include! Thanks! 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns 
import datetime
get_ipython().run_line_magic('matplotlib', 'inline')
avo=pd.read_csv('/kaggle/input/avocado-prices/avocado.csv')
avo


# In[ ]:


plt.figure(figsize=(15,5))
avo['AveragePrice'].plot()


# In[ ]:


sns.pairplot(avo)


# In[ ]:


# In what month are Avocado prices highest? Lowest?

type(avo['Date'].iloc[0])

avo['Date']=pd.to_datetime(avo['Date'])

type(avo['Date'].iloc[0])


# In[ ]:


avo[avo['AveragePrice']==(avo['AveragePrice'].max())]['Date']


# In[ ]:


avo[avo['AveragePrice']==(avo['AveragePrice'].min())]['Date']


# In[ ]:


avo['Month']=avo['Date'].apply(lambda x: x.month)
avo.groupby('Month').mean()['AveragePrice'].sort_values(ascending=False).index[0]


# In[ ]:





# In[ ]:


# Which region buys the most avocados?

avo.drop(avo.loc[avo['region']=='TotalUS'].index, inplace=True)

avo.groupby('region').sum()['Total Volume']#.idxmax()


# In[ ]:


avo.groupby('region').sum()['Total Volume'].idxmax()


# In[ ]:


plt.figure(figsize=(12,5))
avo.drop(avo.loc[avo['region']=='TotalUS'].index, inplace=True)
avo.groupby('region').sum()['Total Volume'].sort_values().plot.bar()


# In[ ]:


# How much more/less revenue do Organic avocados bring in vs regular?

avo['Revenue']=avo['AveragePrice']*avo['Total Volume']
c=avo.groupby('type').sum()['Revenue']['conventional']
o=avo.groupby('type').sum()['Revenue']['organic']
o-c


# In[ ]:


# Which state cares most about buying organic? (higest ratio of organic to nonorganic)


a=pd.DataFrame(avo.groupby(['region','type']).sum()['Total Volume'].values.reshape((-1,2)))
a['ratio']=a[1]/a[0]

a['region']=avo['region'].unique()
a.set_index('region', inplace=True)
a


# In[ ]:


a['ratio'].idxmax()


# In[ ]:


plt.figure(figsize=(5,12))
a['ratio'].sort_values().plot.barh()


# In[ ]:


# Is there any correlation between length of state name and avg price of avocado?

newdf = avo[['region', 'AveragePrice']]
meandf = newdf.groupby('region').mean()
meandf.reset_index(inplace=True)
meandf['state_name_len']=meandf['region'].str.len()
plt.scatter(x=meandf['AveragePrice'], y=meandf['state_name_len'])


# In[ ]:




