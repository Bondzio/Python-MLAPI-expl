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


# ## Load your data using pandas

# In[ ]:


train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')


# In[ ]:


train.head()


# In[ ]:


test.head()


# ## Import Your Classifier

# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
clf = LogisticRegression()


# In[ ]:


X = train.drop(['id', 'is_team1_won'], axis=1).values
y = train['is_team1_won'].values


# ## Split your data for validation

# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)


# In[ ]:


clf.fit(X_train, y_train)


# ## Measure Accuracy

# In[ ]:


# Performance on train set
clf.score(X_train, y_train)


# In[ ]:


# Performance on test set
clf.score(X_test, y_test)


# ## Start Predicting

# In[ ]:


clf.fit(X, y)


# In[ ]:


prediction = clf.predict(test.drop(['id'], axis=1).values)


# ## Making Submission

# In[ ]:


pd.DataFrame({
    'id' : test['id'],
    'is_team1_won': prediction
}).to_csv('mysubmission.csv', index=False)

