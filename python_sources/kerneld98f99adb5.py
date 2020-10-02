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


df=pd.read_csv('/kaggle/input/AAPL.csv')
df.rename(columns={'Unnamed: 0' : 'Index'},inplace='True')
df['Ticker']='Apple'
df.head()


# In[ ]:


df_1=pd.read_csv('/kaggle/input/AMZN.csv')
df_1.rename(columns={'Unnamed: 0' : 'Index'},inplace='True')
df_1['Ticker']='Amazon'
df_1.head()


# ****Performe Join Operation on two data frames****

# In[ ]:


inner_df=pd.merge(df,df_1,on ='Index',how='inner', suffixes=['_Apple','_Amazon'])
inner_df.head()

