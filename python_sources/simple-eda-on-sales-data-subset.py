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


# The following is a Simple Exploration of Sales Data. The exploration is performed on a subset of the entire dataset.
# Objective: To understand the data and find possible patterns and seasonality in the data.


# In[ ]:


from matplotlib import pyplot as plt


# In[ ]:


import pandas as pd
sales_train = pd.read_csv("../input/competitive-data-science-predict-future-sales/sales_train.csv")


# In[ ]:


sales = sales_train
sales.head(5) #Top 5 rows


# In[ ]:


print(sales.dtypes) #Data type for every column


# In[ ]:


sales['year'] = sales.date.apply(lambda x: x[-4:])  #Adding Year Column
sales.head()


# In[ ]:


sales['month'] = sales.date.apply(lambda x:x[-7:-5:1]) #Adding month Column
sales.head()


# In[ ]:


sales['day'] = sales.date.apply(lambda x:x[0:2:1]) #Adding day column
sales.head()


# In[ ]:


sales['total'] = sales['item_price'] * sales['item_cnt_day'] #Total amount in dollars sale


# In[ ]:


#Number of Products sold per year
df1 = sales.groupby('year')['item_cnt_day'].sum().reset_index()
df1.head()


# In[ ]:


df1.plot(x='year',y='item_cnt_day',kind='bar')
plt.show()


# In[ ]:


df2 = sales.groupby('year')['total'].sum().reset_index()


# In[ ]:


df2.plot(x='year',y='total',kind='bar')
plt.ticklabel_format(style='plain', axis='y')
plt.show()


# In[ ]:


#observation:
# The sale in dollar amounts for year 2014 is the highest
# The sale in dollar amounts for year 2014 is highest inspite of 2013 having higghest number of itmems sold
#It can be inferred more costly items were sold in 2014.


# In[ ]:


df3 = sales.groupby('month')['total'].agg(sum).reset_index()


# In[ ]:


df3.plot(x='month', y='total',kind="bar")
plt.ticklabel_format(style='plain', axis='y')

plt.show()


# In[ ]:


df4 = sales.groupby('month')['total'].mean().reset_index()
df4.plot(x='month', y='total',kind="bar")
plt.ticklabel_format(style='plain', axis='y')

plt.show()


# In[ ]:


df5 = sales.groupby('month')['item_cnt_day'].sum().reset_index()


# In[ ]:


df5.plot(x='month', y='item_cnt_day',kind="bar")
plt.ticklabel_format(style='plain', axis='y')

plt.show()


# In[ ]:


#The months of November and December have greater number of items sold than the rest of the months


# In[ ]:


sales['int_month'] = sales['month'].astype(int)
def f(row):
    if row['int_month'] >=3 and  row['int_month'] <=5:
        s='spring'
    elif row['int_month'] >=6 and row['int_month'] <=8:
        s='summer'
    elif row['int_month'] >='9' and row['int_month'] <=11:
        s='autumn'
    else:
        s='winter'
    return s


# In[ ]:


sales['int_date'] = pd.to_datetime(sales['date'],format="%d.%m.%Y")


# In[ ]:


sales['WEEKDAY'] = ((pd.DatetimeIndex(sales['int_date']).dayofweek) // 5 == 1).astype(float)


# In[ ]:


df6 = sales.groupby('WEEKDAY')['total'].sum().reset_index()
df6.plot(x='WEEKDAY', y='total',kind="bar")
plt.ticklabel_format(style='plain', axis='y')

plt.show()


# In[ ]:


##### Total amount of sales in dollars is more than double for weekdays 


# In[ ]:


#Analysis on Shops
df7 = sales.groupby('shop_id')['item_cnt_day'].sum().reset_index()
df7.head()


# In[ ]:


from matplotlib.pyplot import figure
figure(figsize=(14, 5))
df7.plot(x='shop_id', y='item_cnt_day',kind="bar")
plt.ticklabel_format(style='plain', axis='y')
plt.gcf().set_size_inches(20, 10)

plt.show()


# In[ ]:


df8 = sales.groupby(['shop_id','year'])['item_cnt_day'].sum().reset_index()


# In[ ]:


df8_1 = df8[df8.shop_id <30].reset_index()
df8_2 = df8[df8.shop_id >=30].reset_index()

#df8_1 = df8['shop_id'] < 30  #First 30 shops
#df8_2 = df8['shop_id']>=30    #Next 30 shops
df8_1['shop_id'] = df8_1['shop_id'].apply(str) 
df8_2['shop_id'] = df8_2['shop_id'].apply(str) 
df8_1['shopyear'] = df8_1['shop_id'] + df8_1['year']
df8_2['shopyear'] = df8_2['shop_id'] + df8_2['year']
#figure(figsize=(14, 5))
df8_1.plot(x='shopyear', y='item_cnt_day',kind="bar")
plt.gcf().set_size_inches(20, 10)

plt.ticklabel_format(style='plain', axis='y')

plt.show()


# In[ ]:


##### Item sales per Shop over the years(For shops 0-29)


# In[ ]:



#plt.figure(figsize=(20,10)) 
df8_2.plot(x='shopyear', y='item_cnt_day',kind="bar")
plt.gcf().set_size_inches(20, 10)
plt.ticklabel_format(style='plain', axis='y')
plt.show()


# In[ ]:


## The sales per shop over the year is declining 


# In[ ]:


#### Most popular shop is Shop 31 interms of amount of sale


# In[ ]:




