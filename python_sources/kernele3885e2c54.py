#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# 

# Titatic Data Analytics - what factor made people more likely to survive the shinking of the Titanic? What ever the amount passerger paid is right or wrong? what is the chances to survive for worker.
# 
# **LOAD DATA TO DATAFRAME**

# 

# In[60]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split,cross_val_score
import re


# In[61]:


trn = pd.read_csv('../input/train.csv')
trn.head()


# In[62]:


test = pd.read_csv('../input/test.csv')
test.head()


# In[64]:


trn.nunique()


# In[65]:


trn.isnull().sum()


# In[66]:


trn.Cabin = trn.Cabin.str[0]
trn.Age = trn.fillna(trn.Age.mean())
trn.Sex = pd.Categorical(trn.Sex).codes
trn.Embarked = pd.Categorical(trn.Embarked).codes
trn['Title'] = trn.Name.apply(lambda x: re.search(' ([A-Z][a-z]+)\.', x).group(1))
trn.Title = pd.Categorical(trn.Title).codes
trn.head()


# In[67]:


X = trn.drop(['PassengerId','Name','Ticket','Cabin','Survived'], axis=1)
y = trn.Survived
X.head()


# In[71]:


tst = test.copy()
tst.Cabin = tst.Cabin.str[0]
tst.Age = tst.fillna(tst.Age.mean())
tst.Fare = tst.fillna(tst.Fare.mean())
tst.Sex = pd.Categorical(tst.Sex).codes
tst.Embarked = pd.Categorical(tst.Embarked).codes
tst['Title'] = tst.Name.apply(lambda x: re.search(' ([A-Z][a-z]+)\.', x).group(1))
tst.Title = pd.Categorical(tst.Title).codes
X_test = tst.drop(['PassengerId','Name','Ticket','Cabin',], axis=1)


# In[72]:


X_test.head()


# In[73]:


from sklearn.base import TransformerMixin
class DataFrameImputer(TransformerMixin):
    def fit(self, X, y=None):
        self.fill = pd.Series([X[c].value_counts().index[0]
            if X[c].dtype == np.dtype('O') else X[c].median() for c in X],
            index=X.columns)
        return self
    def transform(self, X, y=None):
        return X.fillna(self.fill)


# In[74]:


X = DataFrameImputer().fit_transform(X)
X_test = DataFrameImputer().fit_transform(X_test)


# In[76]:


import xgboost as xgb

gbm = xgb.XGBClassifier().fit(X, y)


# ## Final Prediction ##

# In[79]:


Y_predict = gbm.predict(X_test)
Y_predict.shape


# In[80]:


submission = pd.DataFrame({ 'PassengerId': test['PassengerId'],
                            'Survived': Y_predict })
submission.to_csv("submission.csv", index=False)
submission.head()

