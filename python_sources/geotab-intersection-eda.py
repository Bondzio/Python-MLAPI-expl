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


# Load Data

train = pd.read_csv("../input/bigquery-geotab-intersection-congestion/train.csv")
test = pd.read_csv("../input/bigquery-geotab-intersection-congestion/test.csv")


# In[ ]:


# We will create one hot encoding for entry , exit direction fields for train, test set

dfen = pd.get_dummies(train["EntryHeading"],prefix = 'en')
dfex = pd.get_dummies(train["ExitHeading"],prefix = 'ex')
train = pd.concat([train,dfen],axis=1)
train = pd.concat([train,dfex],axis=1)


# In[ ]:


dfent = pd.get_dummies(test["EntryHeading"],prefix = 'en')
dfext = pd.get_dummies(test["ExitHeading"],prefix = 'ex')
test = pd.concat([test,dfent],axis=1)
test = pd.concat([test,dfext],axis=1)


# In[ ]:


train.shape,test.shape


# In[ ]:


test.head()


# In[ ]:


train.columns


#  ### Approach: We will make 6 predictions based on features - IntersectionId , Hour , Weekend , Month , entry & exit directions .Target variables will be TotalTimeStopped_p20 ,TotalTimeStopped_p50,TotalTimeStopped_p80,DistanceToFirstStop_p20,DistanceToFirstStop_p50,DistanceToFirstStop_p80 .

# In[ ]:


X = train[["IntersectionId","Hour","Weekend","Month",'en_E',
       'en_N', 'en_NE', 'en_NW', 'en_S', 'en_SE', 'en_SW', 'en_W', 'ex_E',
       'ex_N', 'ex_NE', 'ex_NW', 'ex_S', 'ex_SE', 'ex_SW', 'ex_W']]
y1 = train["TotalTimeStopped_p20"]
y2 = train["TotalTimeStopped_p50"]
y3 = train["TotalTimeStopped_p80"]
y4 = train["DistanceToFirstStop_p20"]
y5 = train["DistanceToFirstStop_p50"]
y6 = train["DistanceToFirstStop_p80"]





# In[ ]:


testX = test[["IntersectionId","Hour","Weekend","Month",'en_E',
       'en_N', 'en_NE', 'en_NW', 'en_S', 'en_SE', 'en_SW', 'en_W', 'ex_E',
       'ex_N', 'ex_NE', 'ex_NW', 'ex_S', 'ex_SE', 'ex_SW', 'ex_W']]


# In[ ]:


from sklearn.linear_model import LinearRegression


# In[ ]:


lr = LinearRegression()


# In[ ]:


lr.fit(X,y1)
pred1 = lr.predict(testX)
lr.fit(X,y2)
pred2 = lr.predict(testX)
lr.fit(X,y3)
pred3 = lr.predict(testX)
lr.fit(X,y4)
pred4 = lr.predict(testX)
lr.fit(X,y5)
pred5 = lr.predict(testX)
lr.fit(X,y6)
pred6 = lr.predict(testX)


# In[ ]:


# Appending all predictions
all_preds = []
for i in range(len(pred1)):
    for j in [pred1,pred2,pred3,pred4,pred5,pred6]:
        all_preds.append(j[i])
        


# In[ ]:


len(all_preds)


# In[ ]:


sub  = pd.read_csv("../input/bigquery-geotab-intersection-congestion/sample_submission.csv")


# In[ ]:


sub["Target"] = all_preds


# In[ ]:


sub.to_csv("benchmark_beat_lr.csv",index = False)


# In[ ]:




