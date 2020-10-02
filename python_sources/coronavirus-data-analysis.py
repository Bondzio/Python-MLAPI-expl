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


Cdata_df = pd.read_csv('/kaggle/input/novel-corona-virus-2019-dataset/2019_nCoV_data.csv')
Cdata_df.head()


# In[ ]:


Cdata_df.info()


# 1.**Total cases confirmed  **

# In[ ]:


print("Total cases confirmed : "+"{}".format(Cdata_df['Confirmed'].sum()))


# 1. Total death cases

# In[ ]:


print("Total cases confirmed : "+"{}".format(Cdata_df['Deaths'].sum()))


# 1. **Maxinum confirmed cases by county**

# In[ ]:


print("Total cases confirmed : "+"{}".format(Cdata_df['Confirmed'].max()))

country_confirmed = Cdata_df[['Confirmed','Country']].groupby(['Confirmed']).max()
print(country_confirmed)


# In[ ]:


#pd.to_datetime(df.DOB)
Cdata_df['Date'] = pd.to_datetime(Cdata_df['Date']).dt.strftime('%Y-%d-%m')


# . **The total number of confirmed case**

# 
# 2. **Province/State**
# 3. **The stats may vary**

# In[ ]:


from datetime import datetime
df_date = Cdata_df.groupby('Date')['Confirmed'].sum().reset_index()
df_date.columns = ['Date','Confirmed']
print(df_date)   


# In[ ]:


import seaborn as sns
plt.figure(figsize = (16,9))
sns.barplot('Date','Confirmed', data = df_date)
plt.xlabel('Date', fontsize = 16)
plt.ylabel('Numbers of Infected', fontsize = 16)
plt.title('Total Numbers of Infected every Passing Day', fontsize = 20)
plt.show()


# In[ ]:


print(Cdata_df['Confirmed'].sum())
print(country_confirmed)


# In[ ]:


df_country_confirmed = country_confirmed.groupby('Confirmed')['Country'].sum().reset_index().sort_values('Confirmed',ascending=False)

