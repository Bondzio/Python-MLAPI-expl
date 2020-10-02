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


import numpy as np
import pandas as pd 
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.feature_selection import RFE
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt


# In[ ]:


train = pd.read_csv("/kaggle/input/walmart/train.csv")
test = pd.read_csv("/kaggle/input/walmart/test.csv")
store = pd.read_csv("/kaggle/input/walmart/stores.csv")
features = pd.read_csv("/kaggle/input/walmart/features.csv")


# In[ ]:


train.head()


# In[ ]:


store.head()


# In[ ]:


features= features.drop(columns= ['IsHoliday'])
features.head()


# In[ ]:


train= train.merge(store, how='left', on= 'Store')
test= test.merge(store, how='left', on= 'Store')


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


train= train.merge(features,how = 'inner', on=['Store','Date'])
test= test.merge(features,how = 'inner', on=['Store','Date'])


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


print(train.isnull().sum()*100/len(train))
print(test.isnull().sum()*100/len(test))


# In[ ]:


train = train.drop(columns= ['MarkDown2', 'Date'], axis= 1)
test= test.drop(columns= ['MarkDown2', 'Date'], axis= 1)


# In[ ]:


train= train.fillna(0)
test= test.fillna(0)


# In[ ]:


catagorical = ['IsHoliday','Type']
for col in catagorical:
    lbl = preprocessing.LabelEncoder()
    lbl.fit(train[col].values.astype('str'))
    train[col] = lbl.transform(train[col].values.astype('str'))


# In[ ]:


for col in catagorical:
    lbl = preprocessing.LabelEncoder()
    lbl.fit(test[col].values.astype('str'))
    test[col] = lbl.transform(test[col].values.astype('str'))


# In[ ]:





# In[ ]:


test.head()


# In[ ]:


train.describe()


# In[ ]:


fig = plt.figure(figsize=(10, 10))
corr= train.corr()
sns.heatmap(corr, cbar = True,  square = True, cmap= 'coolwarm')
plt.show()


# In[ ]:


sns.pairplot(train, x_vars= ['Store', 'IsHoliday', 'Size', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment'], 
             y_vars= ['Weekly_Sales'], kind= 'reg')


# In[ ]:


x_train= train.drop(['Weekly_Sales'], axis= 1)
y_train= train['Weekly_Sales']
x_test= test


# In[ ]:


lm = LinearRegression()
model = lm.fit(x_train,y_train)


# In[ ]:


pred_y = lm.predict(x_test)
pred_y

