#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Use one-hot encoding for categorical variables
# Take the log on sales price
# Use decision Trees, and set parameters as 1
# only use columns 
# ['Id','LotArea', 'OverallQual','OverallCond','YearBuilt','TotRmsAbvGrd','GarageCars','WoodDeckSF',
# 'PoolArea','SalePrice']

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


columns_to_use = ['Id', 'LotArea', 'OverallQual','OverallCond','YearBuilt',
                  'TotRmsAbvGrd','GarageCars','WoodDeckSF','PoolArea','SalePrice']
columns_in_test = columns_to_use.copy()
columns_in_test.remove("SalePrice")
columns_in_test


# In[ ]:


# import pandas_profiling as pdp


# In[ ]:


df = pd.read_csv("../input/train.csv", usecols=columns_to_use)
df.set_index('Id', inplace=True)
pd.options.display.max_rows=5


# In[ ]:


df


# In[ ]:


# pdp.ProfileReport(df)


# In[ ]:


from sklearn.ensemble import RandomForestRegressor


# In[ ]:


# pull data into target (y) and predictors (X)
train_y = np.log(df.SalePrice)
# predictor_cols = ['LotArea', 'OverallQual', 'YearBuilt', 'TotRmsAbvGrd']


# In[ ]:


# Create training predictors data
# train_X = df[predictor_cols]


# In[ ]:


train_X = df.drop(['SalePrice'], 1)


# In[ ]:


import category_encoders as ce


# In[ ]:


encoder = ce.OneHotEncoder()


# In[ ]:


train_X.replace(np.nan, 0, inplace=True)


# In[ ]:


train_X = encoder.fit_transform(train_X)


# In[ ]:


from sklearn import tree


# In[ ]:


# DecisionTreeRegressor?


# In[ ]:


my_model = tree.DecisionTreeRegressor(random_state=42)


# In[ ]:


my_model.fit(train_X, train_y)


# In[ ]:


import graphviz 
dot_data = tree.export_graphviz(my_model, out_file=None) 
graph = graphviz.Source(dot_data) 
# graph
graph.render("housing")


# In[ ]:





# In[ ]:


test = pd.read_csv('../input/test.csv', usecols=columns_in_test)
test.set_index('Id', inplace=True)
# Treat the test data in the same way as training data. In this case, pull same columns.
test_X = test.replace(np.nan, 0)
test_X = encoder.transform(test_X)
# test_X = test.replace(np.nan, 0, inplace=True)
# test_X = test[predictor_cols]
# Use the model to make predictions
predicted_prices = my_model.predict(test_X)
# We will look at the predicted prices to ensure we have something sensible.
print(predicted_prices)


# In[ ]:


# Get the exponent of prices
# The current predicted prices are the log of the prices
predicted_prices = np.exp(predicted_prices)


# In[ ]:


my_submission = pd.DataFrame({'Id': test.index, 'SalePrice': predicted_prices})
# you could use any filename. We choose submission here
my_submission.to_csv('submission_1723.csv', index=False)


# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


df.SalePrice.hist()


# In[ ]:


np.log10(df.SalePrice).hist()


# In[ ]:




