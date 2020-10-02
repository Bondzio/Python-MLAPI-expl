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





# In[ ]:


import pandas as pd
DataCoSupplyChainDataset = pd.read_csv("../input/dataco-smart-supply-chain-for-big-data-analysis/DataCoSupplyChainDataset.csv", header= 0,encoding= 'unicode_escape')
DescriptionDataCoSupplyChain = pd.read_csv("../input/dataco-smart-supply-chain-for-big-data-analysis/DescriptionDataCoSupplyChain.csv")
tokenized_access_logs = pd.read_csv("../input/dataco-smart-supply-chain-for-big-data-analysis/tokenized_access_logs.csv")


# In[ ]:


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


train=DataCoSupplyChainDataset


# In[ ]:


train.head()


# In[ ]:


train.shape


# In[ ]:


train.info()


# In[ ]:


train.columns[train.isnull().any()]


# In[ ]:


train['Order Item Discount Rate'].unique()


# In[ ]:


train['Order Item Id'].unique()


# In[ ]:


train[(train['Customer Id']==19491)]


# In[ ]:


train['Market'].unique()


# In[ ]:


train.head(10)


# In[ ]:


train.drop(columns=['Late_delivery_risk','Category Name','Customer City','Customer Email','Customer Fname','Customer Lname','Customer Password','Customer State','Customer Street','Customer Zipcode',
                      'Department Name','Latitude','Longitude','Order City','Product Description','Product Image','Product Status','Order Zipcode'],inplace=True)


# In[ ]:


train.info()


# In[ ]:


train.head()


# In[ ]:


train['Type'].unique()


# In[ ]:


train.loc[(train['Type'] == 'DEBIT') ,'Type'] =1
train.loc[(train['Type'] == 'TRANSFER') ,'Type'] =2
train.loc[(train['Type'] == 'CASH') ,'Type'] =3
train.loc[(train['Type'] == 'PAYMENT') ,'Type'] =4


# In[ ]:


train['Type'].unique()


# In[ ]:


train['Delivery Status'].unique()


# In[ ]:


train.loc[(train['Delivery Status'] == 'Shipping canceled') ,'Delivery Status'] =0
train.loc[(train['Delivery Status'] == 'Late delivery') ,'Delivery Status'] =1
train.loc[(train['Delivery Status'] == 'Shipping on time') ,'Delivery Status'] =2
train.loc[(train['Delivery Status'] == 'Advance shipping') ,'Delivery Status'] =3


# In[ ]:


train['Customer Segment'].unique()


# In[ ]:


train.loc[(train['Customer Segment'] == 'Consumer') ,'Customer Segment'] =1
train.loc[(train['Customer Segment'] == 'Home Office') ,'Customer Segment'] =2
train.loc[(train['Customer Segment'] == 'Corporate') ,'Customer Segment'] =3


# In[ ]:


train['Market'].unique()


# In[ ]:


train.loc[(train['Market'] == 'Pacific Asia') ,'Market'] =1
train.loc[(train['Market'] == 'USCA') ,'Market'] =2
train.loc[(train['Market'] == 'Africa') ,'Market'] =3
train.loc[(train['Market'] == 'Europe') ,'Market'] =4
train.loc[(train['Market'] == 'LATAM') ,'Market'] =5


# In[ ]:


train['Order Status'].unique()


# In[ ]:


train.loc[(train['Order Status'] == 'COMPLETE') ,'Order Status'] =0
train.loc[(train['Order Status'] == 'PENDING') ,'Order Status'] =1
train.loc[(train['Order Status'] == 'CLOSED') ,'Order Status'] =2
train.loc[(train['Order Status'] == 'PENDING_PAYMENT') ,'Order Status'] =3
train.loc[(train['Order Status'] == 'CANCELED') ,'Order Status'] =4
train.loc[(train['Order Status'] == 'PROCESSING') ,'Order Status'] =5
train.loc[(train['Order Status'] == 'SUSPECTED_FRAUD') ,'Order Status'] =6
train.loc[(train['Order Status'] == 'ON_HOLD') ,'Order Status'] =7
train.loc[(train['Order Status'] == 'PAYMENT_REVIEW') ,'Order Status'] =8


# In[ ]:


train['Shipping Mode'].unique()


# In[ ]:


train.loc[(train['Shipping Mode'] == 'Standard Class') ,'Shipping Mode'] =1
train.loc[(train['Shipping Mode'] == 'First Class') ,'Shipping Mode'] =2
train.loc[(train['Shipping Mode'] == 'Second Class') ,'Shipping Mode'] =3
train.loc[(train['Shipping Mode'] == 'Same Day') ,'Shipping Mode'] =0


# In[ ]:


train.drop(columns=['Customer Country','Order Country','order date (DateOrders)','Order Region','Order State','Product Name','shipping date (DateOrders)'],inplace=True)


# In[ ]:


train.shape


# In[ ]:


train.info()


# In[ ]:


train.columns[train.isnull().any()]


# In[ ]:


train['Department Id'].unique()


# In[ ]:


train.head()


# In[ ]:


numeric_cols = ['Days for shipping (real)','Days for shipment (scheduled)','Benefit per order','Sales per customer','Category Id','Customer Id',
                'Order Customer Id','Order Id','Order Item Cardprod Id','Order Item Discount','Order Item Id','Order Item Product Price','Order Item Profit Ratio',
                'Order Item Quantity','Order Item Total','Sales','Order Item Total','Order Profit Per Order','Product Card Id','Product Category Id',
                'Product Price','Order Item Discount Rate']


# In[ ]:


categorical_cols = ['Type','Delivery Status','Customer Segment','Market','Department Id','Order Status','Shipping Mode']


# In[ ]:


f = pd.melt(train, value_vars=numeric_cols)
g = sns.FacetGrid(f, col="variable",  col_wrap=3, sharex=False, sharey=False, height = 5)
g = g.map(sns.distplot, "value")


# In[ ]:


train.corr()


# In[ ]:


targets = train['Product Price']
train.drop(columns=['Product Price'], inplace=True)


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(train, targets, test_size=0.3, random_state=9)
print(X_train.shape)
print(X_test.shape)


# In[ ]:


#import xgboost 


# In[ ]:


from sklearn.ensemble import RandomForestRegressor


# In[ ]:


regressor = RandomForestRegressor(n_estimators=70, random_state=0)
regressor.fit(X_train, y_train)


# In[ ]:


from sklearn.metrics import mean_squared_error
train_pred = regressor.predict(X_train)
mean_squared_error(y_train, train_pred)


# In[ ]:


from sklearn.metrics import mean_squared_error

y_pred = regressor.predict(X_test)
mean_squared_error(y_test, y_pred)


# In[ ]:



#xgb = xgboost.XGBRegressor(n_estimators=30, learning_rate=0.08, gamma=0, subsample=0.75,
                           #colsample_bytree=1, max_depth=7)
#xgb_model.fit(X_train, y_train)

