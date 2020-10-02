#!/usr/bin/env python
# coding: utf-8

# In[70]:


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


# In[71]:


train = pd.read_csv("../input/train.csv")


# In[72]:


train.head()


# In[73]:


test = pd.read_csv("../input/test.csv")


# In[74]:


test.head()


# In[75]:


train.dtypes


# In[76]:


test.dtypes


# In[77]:


test = pd.read_csv("../input/test.csv", parse_dates = ["datetime"])
train = pd.read_csv("../input/train.csv", parse_dates = ["datetime"])


# In[78]:


test.dtypes


# In[79]:


train.dtypes


# In[80]:


train["year"] = train["datetime"].dt.year
train["hour"] = train["datetime"].dt.hour
train["dayofweek"] = train["datetime"].dt.dayofweek

test["year"] = test["datetime"].dt.year
test["hour"] = test["datetime"].dt.hour
test["dayofweek"] = test["datetime"].dt.dayofweek


# In[81]:


train.head()


# In[82]:


test.head()


# In[83]:


y_train = train["count"]
y_train = np.log1p(y_train)


# In[84]:


train.drop(["datetime", "windspeed", "casual", "registered", "count"], 1, inplace=True)
test.drop(["datetime", "windspeed"], 1, inplace=True)


# In[85]:


train.head()


# In[86]:


test.head()


# In[87]:


from sklearn.ensemble import RandomForestRegressor


# In[88]:


rf = RandomForestRegressor(n_estimators=100)


# In[89]:


rf.fit(train,y_train)


# In[90]:


preds = rf.predict(test)


# In[91]:


submission=pd.read_csv("../input/sampleSubmission.csv")


# In[92]:


submission.head()


# In[93]:


submission["count"] = np.expm1(preds)


# In[94]:


submission.head()


# In[ ]:


submission.to_csv("allrf.csv", index=False)

