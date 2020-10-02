#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from pandas import read_csv
import seaborn as sns

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# Reading Datasets

# In[ ]:


item_categories=pd.read_csv('/kaggle/input/competitive-data-science-predict-future-sales/item_categories.csv')
items=pd.read_csv('/kaggle/input/competitive-data-science-predict-future-sales/items.csv')
sales_train=pd.read_csv('/kaggle/input/competitive-data-science-predict-future-sales/sales_train.csv')
sample_submission=pd.read_csv('/kaggle/input/competitive-data-science-predict-future-sales/sample_submission.csv')
shops=pd.read_csv('/kaggle/input/competitive-data-science-predict-future-sales/shops.csv')
test=pd.read_csv('/kaggle/input/competitive-data-science-predict-future-sales/test.csv')


# schema of all the dataframes 

# In[ ]:


item_categories.info()


# In[ ]:


items.info()


# In[ ]:


sales_train.info()


# In[ ]:


sample_submission.info()


# In[ ]:


shops.info()


# In[ ]:


test.info()


# merging items,item_categories and shops datasets

# In[ ]:


train_full = pd.merge(sales_train, items, how='left', on=['item_id','item_id'])
train_full = pd.merge(train_full, item_categories, how='left', on=['item_category_id','item_category_id'])
train_full = pd.merge(train_full, shops, how='left', on=['shop_id','shop_id'])
train_full.head()


# In[ ]:


train_full['date'] = pd.to_datetime(train_full['date'], format='%d.%m.%Y')
train_full['month'] = train_full['date'].dt.month
train_full['year'] = train_full['date'].dt.year
train_full.head()


# In[ ]:



#calculation total Price
train_full['total_price']=train_full['item_price']*train_full['item_cnt_day']
train_full.head()


# date_block_num means "a consecutive month number, used for convenience. January 2013 is 0, February 2013 is 1, ..., October 2015 is 33"

# In[ ]:


plt.figure(figsize=(35,10))
sns.countplot(x='date_block_num', data=train_full);
plt.show()


# In[ ]:


plt.figure(figsize=(35,10))
sns.countplot(x='shop_id', data=sales_train)
plt.show()


# In[ ]:


plt.figure(figsize=(35,10))
sns.countplot(x='item_category_id', data=train_full)
plt.xlabel('Months')
plt.ylabel('item Count a day')
plt.title('item Count a day According to Months')
plt.show()


# ranking chart by monthly sales quantity

# In[ ]:


monthly_sales = pd.DataFrame(train_full.groupby(['date_block_num'])['item_cnt_day'].sum().reset_index())
plt.figure(figsize=(35,10))
sns.barplot(x="date_block_num", y="item_cnt_day", data=monthly_sales , order=monthly_sales['date_block_num'])
plt.xlabel('Months')
plt.ylabel('item Count a day')
plt.title('item Count a day According to Months')
plt.show()


# 

# In[ ]:


train_full_vs_monthly_total_price = pd.DataFrame(train_full.groupby(['date_block_num'])['total_price'].sum().reset_index())
plt.figure(figsize=(35,10))
sns.barplot(x="date_block_num", y="total_price", data=train_full_vs_monthly_total_price, order=train_full_vs_monthly_total_price['date_block_num'])
plt.xlabel('Months')
plt.ylabel('Total Price')
plt.title('Total Price According to Months')
plt.show()


# 
# which shop was sold how much

# In[ ]:


sales_total_price = pd.DataFrame(train_full.groupby(['shop_id'])['total_price'].sum().reset_index())
plt.figure(figsize=(35,10))
sns.barplot(x="shop_id", y="total_price", data=sales_total_price , order=sales_total_price['shop_id'])
plt.xlabel('Shop ID')
plt.ylabel('Total Price')
plt.title('Total Price According to Shops')
plt.show()


# In[ ]:


train_full.head()


# In[ ]:


sales_total_price.head()


# In[ ]:


sales_total_price = pd.DataFrame(train_full.groupby(['year'])['total_price'].sum().reset_index())
plt.figure(figsize=(35,10))
sns.barplot(x="year", y="total_price", data=sales_total_price , order=sales_total_price['year'])
plt.xlabel('years')
plt.ylabel('Total Price')
plt.title('Total sales quantity According to years')
plt.show()

