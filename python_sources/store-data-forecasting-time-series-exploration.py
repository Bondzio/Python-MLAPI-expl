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
get_ipython().run_line_magic('matplotlib', 'inline')

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


from sklearn.model_selection import train_test_split
from matplotlib import style
style.use('ggplot')


# In[ ]:


train = pd.read_csv('../input/train.csv', parse_dates=['date'])
test = pd.read_csv('../input/test.csv', parse_dates=['date'])
sub = pd.read_csv('../input/sample_submission.csv')


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


print("Test Shape: ", test.shape)
print("Train Shape: ", train.shape)


# In[ ]:


train.info()


# In[ ]:


test.info()


# In[ ]:


print("End Date: ", train.date.max())
print("Start Date: ", train.date.min())


# In[ ]:


train.columns


# In[ ]:


test.columns


# >### OUR **TRAIN AND TEST** DATAFRAMES HAS 3 COMMON AND 1 DIFFERENT COLUMNS **

# In[ ]:


# Make Sure to add the type to later identify the kind of data while separating
train['Type'] = 'Train'
test['Type'] = 'Test'


# In[ ]:


df = pd.concat([train, test])


# In[ ]:


df.shape


# In[ ]:


df.date = pd.to_datetime(df.date, format='%Y-%m-%d')


# In[ ]:


df.head()


# In[ ]:


df['dayofmonth'] = df.date.dt.day
df['dayofyear'] = df.date.dt.dayofyear
df['dayofweek'] = df.date.dt.dayofweek
df['month'] = df.date.dt.month
df['year'] = df.date.dt.year
df['weekofyear'] = df.date.dt.weekofyear
df['is_month_start'] = (df.date.dt.is_month_start).astype(int)
df['is_month_end'] = (df.date.dt.is_month_end).astype(int)


# In[ ]:


df.head()


# In[ ]:


temp_df = df.set_index('date')


# In[ ]:


from matplotlib.pyplot import figure


# ### BoxPlot Distribution separated by Months

# In[ ]:


figure(num=None, figsize=(12, 5), dpi=80, facecolor='w', edgecolor='k')
sns.boxplot(x='month', y='sales', data=df)


# ### Store by Sales BoxPlot

# In[ ]:


figure(num=None, figsize=(12, 5), dpi=80, facecolor='w', edgecolor='k')
sns.boxplot(x='store', y='sales', data=df)


# ### Sales v/s DayofWeek BoxPlot
# #### It seems that week day #6 appears to have the maximum sale and the highest median sales.

# In[ ]:


figure(num=None, figsize=(12, 5), dpi=80, facecolor='w', edgecolor='k')
sns.boxplot(x='dayofweek', y='sales', data=df)
plt.xlabel('Day of Week')


# In[ ]:


figure(num=None, figsize=(12, 5), dpi=80, facecolor='w', edgecolor='k')
plt.scatter(df.groupby('store')['sales'].mean().index, df.groupby('store')['sales'].mean().values)
plt.xticks([1,2,3,4,5,6,7,8,9,10])
plt.xlabel("Store Number")
plt.ylabel("Average Sale")


# In[ ]:


train_temp = train.set_index('date')
test_temp = test.set_index('date')


# In[ ]:


train_temp.plot(figsize=(20,10), linewidth=5, fontsize=20)
plt.xlabel('Year', fontsize=20);


# In[ ]:


new_train = df.loc[~df.sales.isna()]
print("new train",new_train.shape)
new_test = df.loc[df.sales.isna()]
print("new test",new_test.shape)


# In[ ]:


new_train.columns


# In[ ]:


new_test.columns


# In[ ]:


train_x, train_cv, y, y_cv = train_test_split(new_train.drop('sales', axis=1),new_train['sales'], test_size=0.15, random_state=101)


# In[ ]:


print(train_x.shape)
print(train_cv.shape)
print(y.shape)
print(y_cv.shape)

