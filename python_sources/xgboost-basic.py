#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


import xgboost as xgb
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


# In[3]:


train = pd.read_csv('../input/train/train.csv')
test = pd.read_csv('../input/test/test.csv')
sample_submission = pd.read_csv('../input/test/sample_submission.csv')


# In[4]:


test.shape


# In[5]:


train.drop(['Name', 'RescuerID', 'Description', 'PetID'], axis=1, inplace=True)


# In[6]:


test.drop(['Name', 'RescuerID', 'Description', 'PetID'], axis=1, inplace=True)


# In[7]:


train.shape


# In[8]:


X, y = train.iloc[:,:-1],train.iloc[:,-1]


# In[9]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)


# In[10]:


train.head()


# In[11]:


xg_clf = xgb.XGBClassifier(objective ='reg:linear', colsample_bytree = 0.3, learning_rate = 0.1,
                max_depth = 5, alpha = 10, n_estimators = 10)


# In[12]:


xg_clf.fit(X_train,y_train)


# In[13]:


preds = xg_clf.predict(test)


# In[14]:


preds.shape


# In[15]:


test = pd.read_csv('../input/test/test.csv')


# In[16]:


submission = pd.DataFrame({'PetID': test['PetID'].values, 'AdoptionSpeed': preds})
submission.to_csv('submission.csv', index=False)


# In[17]:


submission.shape


# In[ ]:




