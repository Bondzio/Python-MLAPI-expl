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


# In[ ]:


d1=pd.read_csv('../input/heart.csv')
d1


# In[ ]:


d1.describe()


# In[ ]:


from sklearn.model_selection import train_test_split
X=d1.drop('target',axis=1)
y=d1['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)


# In[ ]:


from sklearn.linear_model import LinearRegression
lr=LinearRegression()
lr.fit(X_train,y_train)


# In[ ]:


lr.score(X_train,y_train)


# In[ ]:


from sklearn.svm import LinearSVC

clf_svc = LinearSVC(penalty='l1',dual=False,tol=1e-3)
clf_svc.fit(X_train, y_train)


# In[ ]:


clf_svc.score(X_train,y_train)


# In[ ]:


from sklearn.linear_model import LogisticRegression
model = LogisticRegression()


# In[ ]:


model.fit(X_train, y_train)


# In[ ]:


X_test


# In[ ]:


model.score(X_test,y_test)


# In[ ]:




