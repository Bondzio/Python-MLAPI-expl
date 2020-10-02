#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin, clone
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# ## Loading Data

# In[ ]:


train = pd.read_csv('/kaggle/input/cat-in-the-dat/train.csv')
sample = pd.read_csv('/kaggle/input/cat-in-the-dat/sample_submission.csv')
test = pd.read_csv('/kaggle/input/cat-in-the-dat/test.csv')


# In[ ]:


train_id=train['id']
test_id = test['id']
target = train['target']

df1 = train.drop(['target','id'],axis=1)
df2 = test.drop('id',axis=1)


# In[ ]:


data = pd.concat([df1, df2], ignore_index=True)


# In[ ]:


train.shape


# In[ ]:


test.shape


# In[ ]:


data.shape


# ## Checking and counting unique features

# In[ ]:


unq = train.columns.tolist()
for item in unq:
    print("Unique Features {}: ".format(item))
    print(train[item].unique(), "\n")


# In[ ]:


for item in unq:
    print("{}: ".format(item),train[item].nunique())


# In[ ]:


train["target"] = np.log1p(train["target"])


# ## Encoding

# In[ ]:


categorical_feature_mask = data.dtypes==object
# filter categorical columns using mask and turn it into a list
categorical_cols = data.columns[categorical_feature_mask].tolist()


# In[ ]:


le = LabelEncoder()

data[categorical_cols] = data[categorical_cols].apply(lambda col: le.fit_transform(col))
data[categorical_cols].head(10)


# In[ ]:


df_train = data[:300000]
df_test = data[300000:]


# In[ ]:


df_test.head()


# ## Model

# In[ ]:


XGBoost = XGBClassifier(learning_rate=0.05,n_estimators=1000,reg_alpha=5,eval_metric='auc')
XGBoost.fit(df_train,target)


# In[ ]:


finalModel = (np.expm1(XGBoost.predict_proba(df_test)[:,1]))
submission = pd.DataFrame()
submission['id'] = test_id
submission['target'] = finalModel
submission.to_csv('submission.csv',index=False)

