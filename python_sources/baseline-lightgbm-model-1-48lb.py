#!/usr/bin/env python
# coding: utf-8

# In[16]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
print(os.listdir("../input"))

import lightgbm as lgb
import time
from sklearn.cross_validation import KFold
# this kernel use code from https://www.kaggle.com/tunguz/bow-meta-text-and-dense-features-lb-0-2241


# In[17]:


train = pd.read_csv('../input/train.csv')
print("Train shape: ", train.shape)
test = pd.read_csv('../input/test.csv')
print(test.shape[0], " rows in test")


# In[18]:


train.head()


# In[19]:


test.head()


# In[20]:


train.dtypes


# In[21]:


train.shape


# In[22]:


train[train.columns[train.dtypes=='float64']].describe()


# ## Let's try some basic row-wise features 
# * Count nans, count zeros , other variables (e.g. mode - may indicate other missings imputations)

# In[23]:


# No NaNs! 
train.isnull().sum(axis=1).sum()


# In[24]:


## Count zeroes:
def num_count(df,num=0):
    return((df == num).astype(int).sum(axis=1))


# In[25]:


train["row_zeros"] = num_count(train)
test["row_zeros"] = num_count(test)


# In[26]:


train["row_zeros"].describe()


# ## Basic model

# In[27]:


Y = np.log(train.target+1)

train.drop(['target'], axis=1, inplace=True)


# In[28]:


test_ID = test.ID
test.drop(['ID'], axis=1, inplace=True)

train_ID = train.ID
train.drop(['ID'], axis=1, inplace=True)


# In[29]:


train[train.columns[train.dtypes=='int64']].describe()


# In[30]:


lgbm_params =  {
    'task': 'train',
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': 'rmse',
    'max_depth': 8,
    'num_leaves': 32,  # 63, 127, 255
    'feature_fraction': 0.8, # 0.1, 0.01
    'bagging_fraction': 0.8,
    'learning_rate': 0.01, #0.00625,#125,#0.025,#05,
    'verbose': 1
}


# In[31]:


Y_target = []
for fold_id,(train_idx, val_idx) in enumerate(KFold(n=train.shape[0], n_folds=10, random_state=1)):
    print('FOLD:',fold_id)
    X_train = train.values[train_idx]
    y_train = Y.values[train_idx]
    X_valid = train.values[val_idx]
    y_valid =  Y.values[val_idx]
    
    
    lgtrain = lgb.Dataset(X_train, y_train,
                feature_name=train.columns.tolist(),
#                 categorical_feature = categorical # No point to do naively, wihtout defining categoricals based on cardinality
                         )

    lgvalid = lgb.Dataset(X_valid, y_valid,
                feature_name=train.columns.tolist(),
#                 categorical_feature = categorical # No point to do naively, wihtout defining categoricals based on cardinality
                         )

    modelstart = time.time()
    lgb_clf = lgb.train(
        lgbm_params,
        lgtrain,
        num_boost_round=30000,
        valid_sets=[lgtrain, lgvalid],
        valid_names=['train','valid'],
        early_stopping_rounds=80,
        verbose_eval=100
    )
    
    test_pred = lgb_clf.predict(test.values)
    Y_target.append(np.exp(test_pred)-1)
    print('fold finish after', time.time()-modelstart)


# In[32]:


Y_target = np.array(Y_target)


# In[33]:


#submit
sub = pd.read_csv('../input/sample_submission.csv')
sub['target'] = Y_target.mean(axis=0)
sub.to_csv('sub_lgb_baseline.csv', index=False)

