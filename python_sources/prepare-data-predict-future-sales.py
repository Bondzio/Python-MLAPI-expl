#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import numpy.random as nr
import math

get_ipython().run_line_magic('matplotlib', 'inline')
data = pd.read_csv('../input/sales_train.csv')
print(data.head(3))
data.info()


# # Remove item_cnt_day outliers ?

# In[ ]:


# Check for negative item_cnt_day (could be a return ?, invalid values, I don't think so)
data[data['item_cnt_day']<0]['item_cnt_day'].value_counts()


# In[ ]:


plt.plot(data[data['item_cnt_day']<0]['item_id'].value_counts().sort_index())


# In[ ]:


data_filtered=data.loc[data['item_cnt_day']>0]
data_filtered.info()
data=data_filtered


# In[ ]:


item_categories = pd.read_csv('../input/items.csv')
item_categories.head(3)


# # Merge based on item_id

# In[ ]:


dt=pd.merge(data, item_categories, how='inner')
dt.sort_values(by=['date'], inplace=True)
dt.head(3)


# # Drop unused columns

# In[ ]:


## Drop column 
columns=['date','item_price','item_name']
for c in columns:
    if c in dt:
        dt.drop(c, axis = 1, inplace = True)
dt[(dt['item_cnt_day']>0)].head(3)


# # Group by 'date_block_num', 'shop_id','item_id'  and sum the item count per day to get the sum for each month (or date_block_num)

# In[ ]:


dtf=dt.groupby(['date_block_num', 'shop_id','item_id'])[["item_cnt_day"]].sum().reset_index()


# In[ ]:


print(data.size)
print(dtf.size)


# In[ ]:


dtf.hist(figsize=(15,20))
plt.figure()


# In[ ]:


pd.plotting.scatter_matrix(dtf[['item_cnt_day','item_id','shop_id','date_block_num']],figsize=(10,10))
plt.figure()


# In[ ]:


dtf[(dtf['item_id']==2929) & (dtf['shop_id']==0)]


# In[ ]:


dt[(dt['item_id']==2929) & (dt['shop_id']==0)]


# In[ ]:


test_shop_id=dt.groupby(['shop_id'])[["item_cnt_day"]].sum().reset_index()
test_shop_id.head()
plt.bar(test_shop_id['shop_id'],test_shop_id ["item_cnt_day"])


# # Analyze item_id outliers

# In[ ]:


test_item_id=dt.groupby(['item_id'])[["item_cnt_day"]].sum().reset_index()
plt.plot(test_item_id[(test_item_id['item_id']!=20949)]['item_id'],test_item_id[(test_item_id['item_id']!=20949)] ["item_cnt_day"])
plt.plot(test_item_id[(test_item_id['item_cnt_day']<=10000)]['item_id'],test_item_id[(test_item_id['item_cnt_day']<=10000)]["item_cnt_day"])

print(test_item_id[(test_item_id['item_id']!=20949)]['item_id'].describe())
print(test_item_id[(test_item_id['item_cnt_day']>12000)]['item_id'].value_counts())


# In[ ]:


test_item_id=dt.groupby(['item_category_id'])[["item_cnt_day"]].sum().reset_index()
plt.plot(test_item_id['item_category_id'],test_item_id["item_cnt_day"])


# # Try to remove outliers (december months ...)

# In[ ]:


plt.plot(dt.groupby(['date_block_num'])[["item_cnt_day"]].sum())
dt_filtered=dt.loc[(dt['date_block_num'] ==9) | (dt['date_block_num'] ==10) | (dt['date_block_num'] ==21)| (dt['date_block_num'] ==22) | (dt['date_block_num'] ==33)]
print(dt_filtered.size)


# In[ ]:


dt_filtered['date_block_num'].value_counts()


# In[ ]:


pd.options.mode.chained_assignment = None  # default='warn'

idx=dt_filtered.loc[(dt_filtered['date_block_num'] ==9)].index.values
dt_filtered.at[idx,'date_block_num']=0
dt_filtered.at[idx,'year']=1

idx=dt_filtered.loc[(dt_filtered['date_block_num'] ==10)].index.values
dt_filtered.at[idx,'date_block_num']=1
dt_filtered.at[idx,'year']=1

idx=dt_filtered.loc[(dt_filtered['date_block_num'] ==21)].index.values
dt_filtered.at[idx,'date_block_num']=0
dt_filtered.at[idx,'year']=2

idx=dt_filtered.loc[(dt_filtered['date_block_num'] ==22)].index.values
dt_filtered.at[idx,'date_block_num']=1
dt_filtered.at[idx,'year']=2

idx=dt_filtered.loc[(dt_filtered['date_block_num'] ==33)].index.values
dt_filtered.at[idx,'date_block_num']=0
dt_filtered.at[idx,'year']=3
print(dt_filtered['date_block_num'].value_counts())
print(dt_filtered['year'].value_counts())


# In[ ]:


plt.plot(dt_filtered.groupby(['date_block_num'])[["item_cnt_day"]].sum())
print(dt_filtered.head())


# In[ ]:


dt_filtered.to_csv('sales_train_trans_filtered.csv', sep=',',index=False)


# In[ ]:


dt.to_csv('sales_train_trans.csv', sep=',',index=False)


# # Prepare test data : adding category column

# In[ ]:


sales_test = pd.read_csv('../input/test.csv')
sales_test.head(3)


# In[ ]:


sales_test1=pd.merge(sales_test, item_categories, how='inner')
sales_test1.sort_values(by=['ID'], inplace=True)
sales_test1.head(3)


# In[ ]:


sales_test1['shop_id'].value_counts()


# In[ ]:


sales_test1.info()


# In[ ]:


sales_test1.isnull().sum()


# In[ ]:


sales_test1['item_id'].value_counts().count()


# In[ ]:


sales_test1['item_category_id'].value_counts().count()


# In[ ]:


dt['item_category_id'].value_counts().count()


# # Item_category_id that can be removed

# In[ ]:


#pd.concat([pd.unique(sales_test1['item_category_id']),pd.unique(sales_test1['item_category_id'])]).drop_duplicates(keep=False)
#print("sales_test1['item_category_id']-->",pd.unique(sales_test1['item_category_id']))
#print("dt['item_category_id']-->",pd.unique(dt['item_category_id']))
#print("concatenate-->", np.concatenate((pd.unique(sales_test1['item_category_id']),pd.unique(dt['item_category_id'])),axis=0))
np.unique(np.concatenate((pd.unique(sales_test1['item_category_id']),pd.unique(dt['item_category_id'])),axis=0))

a=set(pd.unique(dt['item_category_id']));
b=set(pd.unique(sales_test1['item_category_id']));

list(a-b)


# In[ ]:


sales_test1.drop('item_name', axis = 1, inplace = True)
sales_test1.to_csv('sales_test1.csv', sep=',',index=False)

