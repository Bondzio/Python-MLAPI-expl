#!/usr/bin/env python
# coding: utf-8

# # Setup Environment

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

import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

# Any results you write to the current directory are saved as output.


# # Load Dataset

# In[ ]:


train_df = pd.read_csv("../input/home-data-for-ml-course/train.csv",index_col='Id')
test_df = pd.read_csv("../input/home-data-for-ml-course/test.csv",index_col='Id')
train_df.head()


# # Preprocessing Phase
# ## drop categorical features which have more than 10 unique variables (too many features if (get_dummies) later)

# In[ ]:


cat_cols = [col for col in train_df if train_df[col].dtype == 'object' and train_df[col].nunique()>10]
train_df.drop(cat_cols,axis=1,inplace=True)
test_df.drop(cat_cols,axis=1,inplace=True)
train_df


# ## drop features more than 100 NaN entries

# In[ ]:


train_df.drop([col for col in train_df if train_df[col].isnull().sum()>100],axis=1,inplace=True)
test_df.drop([col for col in test_df if test_df[col].isnull().sum()>100],axis=1,inplace=True)
train_df


# ## extract SalePrice from train dataset and assign it to variable target

# In[ ]:


target = train_df.SalePrice
train_df.drop('SalePrice',axis=1,inplace=True)


# ## fill remaining NaN value with mode value

# In[ ]:


train_df.fillna(train_df.mode(),inplace=True)
test_df.fillna(test_df.mode(),inplace=True)
train_df


# ## one-hot encoding using pd.get_dummies

# In[ ]:


train_df = pd.get_dummies(train_df)
test_df = pd.get_dummies(test_df)
train_df


# In[ ]:


train_df.drop([col for col in train_df if train_df[col].isnull().any()],axis=1,inplace=True)
test_df.drop([col for col in test_df if test_df[col].isnull().any()],axis=1,inplace=True)


# ## split into train and test subsets

# In[ ]:


from sklearn.model_selection import train_test_split

X_train,X_valid,y_train,y_valid = train_test_split(train_df,target,test_size = 0.2,random_state = 20,shuffle=True)
display(X_train,y_train)


# ## standard scalar

# In[ ]:


from sklearn.preprocessing import StandardScaler

ss = StandardScaler()
ss.fit(X_train)
X_train = ss.transform(X_train)
X_valid = ss.transform(X_valid)


# # Model training & evaluation
# ## XGBRegressor model and MAE for evaluation

# In[ ]:


from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

model = XGBRegressor(n_estimators=500,learning_rate=0.05,random_state=0)

model.fit(X_train,y_train)
preds = model.predict(X_valid)
scores = mean_absolute_error(preds,y_valid)
scores


# In[ ]:


# submission_preds = model.predict(test_df)
# output = pd.read_csv("../input/home-data-for-ml-course/sample_submission.csv")
# ouptut.SalePrice = submission_preds
# output.to_csv('submission.csv',index=False)


# In[ ]:




