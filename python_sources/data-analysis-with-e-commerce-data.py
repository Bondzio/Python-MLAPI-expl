#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt #data visualizations
import seaborn as sns #data visualizations

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:





# In[ ]:


data = pd.read_csv('../input/ecommerce-data/data.csv',encoding='unicode_escape')


# Upload data and look at the top 5

# In[ ]:


data.head()


# In[ ]:


#look the data types
data.dtypes


# In[ ]:


data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
data.dtypes


# We convert the 'InvoiceDate' column from object to datetime so that you can use it in subsequent calculations.

# In[ ]:


data_new = data.copy()


# In[ ]:


data_new = data_new[(data_new['UnitPrice'] > 0) & (data_new['Quantity'] > 0)]
data_new[data_new['UnitPrice'] == 0]


# Discounted prices, dirty data etc. can. To get rid of this, we take orders with a **price and quantity greater than 0:**
# Here we have filtered out 'UnitPrice' to 0 for control.

# In[ ]:


#That look the numeric data
plt.subplots(figsize =(12,6))
sns.boxplot(data_new.UnitPrice);


# looking at dense places and ends

# In[ ]:


data_new.columns


# In[ ]:


data_new.groupby(by=['CustomerID','Country'])['InvoiceNo'].count().head()


# Here is how many orders a customer places on a country basis:

# In[ ]:


data_new['TotalPrice']=data_new['UnitPrice'] * data_new['Quantity']
data_new.head()


# To find the total price paid for a product in an order, we multiply the columns of 'UnitPrice' and 'Quantity'.
# 

# In[ ]:


data_new.groupby(by=['CustomerID'], as_index=False)['TotalPrice'].sum().head()


# To find the total spend of a customer

# In[ ]:


#Review by date
data_new['purch_month'] = data_new.InvoiceDate.dt.to_period('M').astype(str)
order_per_month = data_new.groupby(by='purch_month', as_index=False).TotalPrice.sum()
plt.figure(figsize = (12,5))
ax = sns.lineplot(x="purch_month", y = "TotalPrice", data=order_per_month)
ax.set_title('Orders per month');


# * Total turnover on a monthly basis
# * We create a year-month-based column, then visualize it:

# In[ ]:


data_new_2= data_new.groupby('Country')['InvoiceNo'].count().sort_values(ascending= False)


# In[ ]:


data_new_2.head()


# Most orders come from the United Kingdom,

# In[ ]:


sns.set(font_scale=1.4)
data_new_2.plot(kind='barh', figsize=(7, 10), rot=0)
plt.xlabel("Orders", labelpad=14)
plt.ylabel("Country", labelpad=14)
plt.title("OrdersperCountry", y=1.02);


# In[ ]:


data_grouped =  data_new.groupby(by=['Country','purch_month'], as_index=False)['TotalPrice'].sum()
data_grouped['percentage'] = data_grouped['TotalPrice']/data_grouped['TotalPrice'].sum()
data_per =  data_grouped.groupby(by=['Country'], as_index=False)['percentage'].sum().sort_values('percentage',ascending=False)
data_per.head()


# We look at the share that countries receive based on their total spending.

# In[ ]:


df = data_grouped[data_grouped['Country'].isin(['United Kingdom','Netherlands'])]
plt.figure(figsize=(16,6))
d=np.arange(1,13)
sns.lineplot(data = df, x='purch_month', y='TotalPrice',err_style='bars', hue= 'Country');


# We filter the first 2 countries that have the highest share in sales and look at the train on monthly sales:

# # ***Finally***
# **In England, the effect of 'Black Friday' or 'Halloween' is higher than the effect on sales in the Netherlands.**
