#!/usr/bin/env python
# coding: utf-8

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


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# In[ ]:


#Reading training data
train_df = pd.read_csv("/kaggle/input/covid19-global-forecasting-week-1/train.csv")
train_df.head(60)


# In[ ]:


train_df.tail()


# In[ ]:


#size of dataframe
train_df.shape


# In[ ]:


train_df.info()


# In[ ]:


train_df[['ConfirmedCases','Fatalities']].describe()


# In[ ]:


# Filtering necessery columns
df = train_df[['Country/Region', 'ConfirmedCases','Fatalities']]
df


# In[ ]:


# Group BY Country/Region and adding ConfirmedCases and Fatalities
df = df.groupby(['Country/Region']).sum()
df


# In[ ]:


df.shape


# In[ ]:


df.head(10)


# In[ ]:


#Sorting based on ConfirmedCases
df = df.sort_values('ConfirmedCases', ascending=False)
df


# In[ ]:


#filtering countries with no fatalities

df = (df.loc[df['Fatalities']!=0])
df


# In[ ]:



#Percentage Fatalities with respect to ConfirmedCases
df['Perc_fat'] = (df['Fatalities'] / df['ConfirmedCases']) *100
df


# In[ ]:


#countries where fatel is more when comparing to confirmed cases

(df.loc[df['Perc_fat']>5])


# # 2. Italy insights

# In[ ]:


#italy insights
df_italy = train_df['Country/Region']== 'Italy'
df_italy = train_df[df_italy]
df_italy = df_italy[['Date','ConfirmedCases','Fatalities']]
df_italy.reset_index(drop=True, inplace=True)
df_italy


# In[ ]:


df_italy.shape


# In[ ]:


df_italy['Date'] = pd.to_datetime(df_italy['Date']) - pd.to_timedelta(7, unit='d')
df_italy = df_italy.groupby([pd.Grouper(key='Date', freq='W-MON')])[['ConfirmedCases','Fatalities']].sum().reset_index().sort_values('Date')
df_italy


# In[ ]:


import matplotlib.pyplot as plt
ax = df_italy[['ConfirmedCases','Fatalities']].plot(kind='bar', title ="Itally Insights", figsize=(15, 10), legend=True, fontsize=12)
ax.set_xlabel("Week", fontsize=12)
ax.set_ylabel("Covid19", fontsize=12)
plt.show()


# In[ ]:




