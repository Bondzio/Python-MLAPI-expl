#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


#We import the necessary libraries
from mlxtend.frequent_patterns import apriori, association_rules


# In[ ]:


#We read data set
df = pd.read_csv('/kaggle/input/satislar.csv',sep=';',low_memory=False, header=None)
df.head()


# In[ ]:


#We change the variable names
df.columns = ['BranchId', 'PosId', 'InvoiceDate', 'InvoiceNo','StockCode','Line','Quantity','CategoryCode','CategoryName']
df.head()


# In[ ]:


df.shape


# In[ ]:


df.info()


# In[ ]:


#We check for missing data
df.isnull().sum()


# In[ ]:


#We check for missing data in CategoryCode
df[df["CategoryCode"].isnull()]


# In[ ]:


#We can delete the CategoryId because CategoryName doesn't make sense.
df.dropna(subset= ["CategoryCode"],inplace= True)
df.shape


# In[ ]:


#How many unique values do I have
df.nunique()


# In[ ]:


df.describe().T


# In[ ]:


# Stripping extra spaces in the description 
df['CategoryName'] = df['CategoryName'].str.strip(',')
df.head()


# In[ ]:


pd.DataFrame(df["CategoryName"].value_counts(normalize=True)).head(100)


# In[ ]:


#We change Quantity int
df["Quantity"] = df["Quantity"].astype("str")
df['Quantity'] = [x.replace(',', '.') for x in df['Quantity']]
df["Quantity"] = df["Quantity"].astype("float")
df["Quantity"] = df["Quantity"].astype("int")
df.info()


# In[ ]:


branch_order = (df
          .groupby(['InvoiceNo', 'CategoryName'])['Quantity'] 
          .sum().unstack().reset_index().fillna(0) 
          .set_index('InvoiceNo')) 


# In[ ]:


branch_order.head(20)


# In[ ]:


# Encoding the datasets 
branch_encoded = branch_order.applymap(lambda x: 0 if x<=0 else 1) 
basket_branch = branch_encoded 


# In[ ]:


frq_items = apriori(basket_branch, min_support = 0.01, use_colnames = True)
frq_items


# In[ ]:


rules = association_rules(frq_items, metric ="confidence", min_threshold = 0.20) 
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False]) 
rules.head(20) 

