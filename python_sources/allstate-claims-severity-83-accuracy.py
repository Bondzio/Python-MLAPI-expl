#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


sample=pd.read_csv("/kaggle/input/allstate-claims-severity/sample_submission.csv")
sample.head()


# In[ ]:


train=pd.read_csv("/kaggle/input/allstate-claims-severity/train.csv")
train.head()


# In[ ]:


from sklearn.preprocessing import LabelEncoder
la=LabelEncoder()
for i in train:
    if 'cat' in i:
        train[i]=la.fit_transform(train[i])


# In[ ]:


train.head()


# In[ ]:


train.info()


# In[ ]:


import matplotlib.pyplot as plt
plt.figure(figsize=(15,15))
import seaborn as sns
sns.heatmap(train.corr(),annot=True,cmap="Blues")


# In[ ]:


x=train.drop(["id","loss"],axis=1)
y=train["loss"]


# In[ ]:


from sklearn.model_selection import train_test_split,KFold,cross_val_score
xr,xt,yr,yt=train_test_split(x,y)


# In[ ]:


from sklearn.ensemble import GradientBoostingClassifier,RandomForestClassifier,RandomForestRegressor,GradientBoostingRegressor
from xgboost import XGBClassifier,XGBRFRegressor,XGBRegressor
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression,LinearRegression,SGDRegressor
from sklearn.svm import SVC,SVR
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB
from lightgbm import LGBMRegressor


# In[ ]:


model=XGBRegressor(n_estimators=1000)
model.fit(x,y)
print(model)


# In[ ]:


yp=model.predict(xt)


# In[ ]:


from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
print(r2_score(yt,yp))
print(mean_absolute_error(yt,yp))
print(mean_squared_error(yt,yp))


# # TEST

# In[ ]:


test=pd.read_csv("/kaggle/input/allstate-claims-severity/test.csv")
test.head()


# In[ ]:


for i in test:
    if 'cat' in i:
        test[i]=la.fit_transform(test[i])


# In[ ]:


pred=test.drop('id',axis=1)
yp=model.predict(x)
y1=pd.DataFrame(yp)


# In[ ]:


test=pd.concat([test,y1],axis=1)


# In[ ]:


test.head()


# In[ ]:


test.columns


# In[ ]:


test.to_csv("sub.csv",index=False,columns=['id',0])

