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
from scipy.stats import skew

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


train =  pd.read_excel('/kaggle/input/novahomeprice/Kaggle Training Data.xlsx')
train1 = train[train['Previous Close Price'].isnull() == False]
test = pd.read_excel('/kaggle/input/novahomeprice/Kaggle Test Data.xlsx')
sample = pd.read_csv('/kaggle/input/novahomeprice/Kaggle Sample Submission.csv')


# In[ ]:


train2 = train[train['Previous Close Price'].isnull() == True]


# In[ ]:


train2.shape


# In[ ]:


sample = pd.read_csv('/kaggle/input/novahomeprice/Kaggle Sample Submission.csv')


# In[ ]:


train.head()


# In[ ]:


train.head(40)


# In[ ]:


train.columns


# In[ ]:


train.shape


# In[ ]:


full_df = pd.concat([train,test])


# In[ ]:


full_df.shape


# In[ ]:


train1.shape


# In[ ]:


nullz = train.isnull().sum()
nullz[nullz < 33000].shape


# In[ ]:


for col in nullz[nullz < 34000].keys():
    if train[col].dtype != object:
        try:
            plt.figure(figsize = (15,5))
            plt.title('%s has %s nulls' %(col, nullz[col]))
            sns.kdeplot(train[col].dropna())
            sns.kdeplot(train1.rename(columns = {col:col + '_1'})[col + '_1'].dropna())
        except:
            df1 = train1[col].value_counts().sort_values(ascending = False).reset_index().rename(columns = {col:col+'_1'})
            df2 = train2[col].value_counts().sort_values(ascending = False).reset_index()
            df_lol = pd.concat([df1,df2], axis = 1)
            print (df_lol.head(10))


# In[ ]:





# In[ ]:


for col in train.columns:
    if train[col].dtype == object:
        df1 = train1[col].value_counts().sort_values(ascending = False).reset_index().rename(columns = {col:col+'_1'})
        df2 = train2[col].value_counts().sort_values(ascending = False).reset_index()
        df_lol = pd.concat([df1,df2], axis = 1)
        print (df_lol.head(10))


# In[ ]:


train.shape


# In[ ]:


train1.shape


# In[ ]:




