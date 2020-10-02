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


from catboost import CatBoostClassifier, CatBoostRegressor, Pool, cv
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from sklearn import preprocessing, model_selection, neighbors, svm
from sklearn.preprocessing import StandardScaler, RobustScaler, MaxAbsScaler
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error, roc_auc_score, precision_score, recall_score


# Import Data

# In[ ]:


df=pd.read_csv('/kaggle/input/weight-height/weight-height.csv')


# In[ ]:


df.describe()


# In[ ]:


df.head()


# Define features and labels. I try to predict weight. So my label is weight, gender is a categorial feature and height is a numerical feature

# In[ ]:


X = df.drop(['Weight'], axis=1)
y = df['Weight']
print(X.shape, y.shape)


# Split data for validation and shuffle

# In[ ]:


X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2, shuffle=True)
print(X_train.shape, X_test.shape)


# Define catboost regression model. We have not much data so we could choose boosting type ordered, it is better.

# In[ ]:


model = CatBoostRegressor(iterations=100_000, 
                           verbose=1000,
                           #learning_rate=0.01,
                           early_stopping_rounds=2000,
                           #bootstrap_type='Poisson',
                           boosting_type='Ordered',
                           #loss_function='LogLoss', 
                           #custom_metric='Accuracy',
                           #grow_policy='Lossguide',
                           cat_features = ['Gender'],
                           task_type='GPU')


# In[ ]:


model.fit(X_train, y_train, ['Gender'], use_best_model=True, eval_set=(X_test, y_test))


# Predict

# In[ ]:


y_pred = model.predict(X)


# In[ ]:


y_pred


# In[ ]:


y.values


# Calculate Errors

# In[ ]:


print("MAE:", mean_absolute_error(y, y_pred))
print("MSE:", mean_squared_error(y, y_pred))


# Calculate me and my wife data (Conversion to kg -> lbs, cm->inces)

# In[ ]:


my_data = pd.DataFrame(columns=['Gender','Height'], data=[['Male', 167.0*0.3937007874], ['Female', 170.0*0.3937007874]])


# In[ ]:


my_pred = model.predict(my_data)


# In[ ]:


my_pred*0.45359237


# Seems right :), So in conculision catbooost can learn quickly a lineer data
