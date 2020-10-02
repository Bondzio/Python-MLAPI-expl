#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
import pandas_profiling

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


get_ipython().system('pip install pandas-profiling')


# In[ ]:


train = pd.read_csv('/kaggle/input/house-prices-advanced-regression-techniques/train.csv')
test = pd.read_csv('/kaggle/input/house-prices-advanced-regression-techniques/test.csv')
full = train.append(test, ignore_index=True)


# In[ ]:


train.drop('Id',axis=1,inplace=True)


# In[ ]:


train['SalePrice'].describe()


# In[ ]:


pandas_profiling.ProfileReport(train)


# In[ ]:


corrmat = train.corr()
f, ax = plt.subplots(figsize=(20, 9))
sns.heatmap(corrmat, vmax=0.8, square=True)


# In[ ]:


cols = ['OverallQual', 'GrLivArea', 'GarageCars', 'YearBuilt', 'GarageArea', 'FullBath',
       'YearRemodAdd', 'TotRmsAbvGrd', 'TotalBsmtSF', '1stFlrSF']
for col in cols:
    full[col].fillna(0, inplace=True)


# In[ ]:


full_X=pd.concat([full['OverallQual'],
                  full['GrLivArea'],
                  full['GarageCars'],
                  full['YearBuilt'],
                  full['GarageArea'],
                  full['FullBath'],
                  full['YearRemodAdd'],
                  full['TotRmsAbvGrd'],
                  full['TotalBsmtSF'],
                  full['1stFlrSF']],axis=1)


# In[ ]:


sourceRow=1460
data_X=full_X.loc[0:sourceRow-1,:]
data_y=full.loc[0:sourceRow-1,'SalePrice']
pred_X=full_X.loc[sourceRow:,:]


# In[ ]:


from sklearn.linear_model import LinearRegression
regressor=LinearRegression()
regressor.fit(data_X,data_y)


# In[ ]:


regressor.score(data_X,data_y)


# In[ ]:


pandas_profiling.ProfileReport(pred_X)


# In[ ]:


predicted_prices = regressor.predict(pred_X)


# In[ ]:


my_submission = pd.DataFrame({"Id":test["Id"],"SalePrice": predicted_prices})
my_submission.to_csv('submission.csv', index=False)

