#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from xgboost.sklearn import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer, mean_squared_error
from scipy import stats
import warnings
from math import sqrt
warnings.filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))
print(os.listdir("."))

# Any results you write to the current directory are saved as output.


# In[2]:


random_state = 32
folds = 3


# In[3]:


def rmse(actual, predict):
    return sqrt(mean_squared_error(actual, predict))

scoring = make_scorer(rmse, greater_is_better = False)


# In[4]:


train = pd.read_csv('../input/preprocess/train.csv')
train.columns


# In[5]:


y_train = train['SalePrice']
predictor_cols = ['GrLivArea', 'OverallQual', 'YearBuilt', 'GarageArea', 'TotalBsmtSF', 'LotArea', 'YearRemodAdd', 'Fireplaces', 'BsmtFinSF1', 'WoodDeckSF', 'HalfBath',
                  'BedroomAbvGr', 'Neighborhood', 'HeatingQC', 'CentralAir', 'MSZoning', 'MSSubClass', 'Functional', '1stFlrSF']
x_train = train[predictor_cols]
model = XGBRegressor(n_estimators = 200, learning_rate = 0.1, subsample = 0.75, colsample_bytree = 0.75, gamma = 0.01, reg_alpha = 1, reg_lambda = 0, random_state = random_state)
pipe = Pipeline([('model', model)])
param_grid = {
    'model__max_depth': [3, 6]
}
cv = GridSearchCV(pipe, cv=folds, param_grid=param_grid, scoring=scoring)
cv.fit(x_train, y_train)
print('best_params_={}\nbest_score_={}'.format(repr(cv.best_params_), repr(cv.best_score_)))


# best_score_=-0.1266783350636276

# In[6]:


# Read the test data
test = pd.read_csv('../input/preprocess/test.csv')
# Treat the test data in the same way as training data. In this case, pull same columns.
x_test = test[predictor_cols]
# Use the model to make predictions
preds = cv.predict(x_test)
preds = [np.exp(y) - 1 for y in preds]
# We will look at the predicted prices to ensure we have something sensible.
submission = pd.DataFrame({'Id': test['Id'], 'SalePrice': preds})
submission.head()


# In[7]:


submission.to_csv('submission.csv', index=False)
print(os.listdir("."))

