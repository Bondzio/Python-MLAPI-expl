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


df=pd.read_csv('/kaggle/input/credit-card-risk-assessment/Credit_default_dataset.csv')
df.head(5)


# In[ ]:


df.drop(['ID'],axis=1,inplace=True)


# In[ ]:


df.head()


# In[ ]:


df.rename(columns={'PAY_0':'PAY_1'},inplace=True)


# In[ ]:


df['EDUCATION']=df['EDUCATION'].map({0:4,1:1,2:2,3:3,4:4,5:4,6:4,7:4})
df['MARRIAGE']=df['MARRIAGE'].map({0:3,1:1,2:2,3:3})


# In[ ]:


df['EDUCATION'].value_counts()


# **WE WILL BE SCALING OUR VALUES IN GIVEN DATASET AS IT CAN BE SEEN VALUES IN COLUMNS LIKE BILL_AMT PAY_AMT ARE VERY LARGE AND DISTINGUIVE IN COMPARISON TO OTHERS SO WE WILL BE SACLING THEM DOWN **

# REMEBER THE GOLDEN RULE:-
#         WHENEVER DISTANCE IS COMPUTED IN ANY ALGO STANDARD SCALING SHOULD BE DONE TO REVISE ITS MAGNITUDE
#         
#     we will be using XGBoost so distance is compiuted so we will be using standard scaling
#     

# 

# In[ ]:


from sklearn.preprocessing import StandardScaler
scale=StandardScaler()
X=df.drop(['default.payment.next.month'],axis=1)
X=scale.fit_transform(X)


# In[ ]:


y=df['default.payment.next.month']


# In[ ]:


params={'learning_rate':[0.05,0.1,0.15,0.2,0.25,0.3],
       'max_depth':[2,3,5,6,8,9],
       'min_child_weight':[1,2,3,5,7],
       'gamma':[0.1,0.2,0.3,0.4]}


# In[ ]:


from sklearn.model_selection import RandomizedSearchCV
import xgboost


# In[ ]:


classifier=xgboost.XGBClassifier()


# In[ ]:


random_search=RandomizedSearchCV(classifier,params,n_iter=5,scoring='roc_auc',n_jobs=-1,cv=5,verbose=3)


# In[ ]:


random_search.fit(X,y)


# In[ ]:


random_search.best_estimator_


# In[ ]:


classifier=xgboost.XGBClassifier(base_score=0.5, booster=None, colsample_bylevel=1,
              colsample_bynode=1, colsample_bytree=1, gamma=0.4, gpu_id=-1,
              importance_type='gain', interaction_constraints=None,
              learning_rate=0.2, max_delta_step=0, max_depth=3,
              min_child_weight=3, missing=None, monotone_constraints=None,
              n_estimators=100, n_jobs=0, num_parallel_tree=1,
              objective='binary:logistic', random_state=0, reg_alpha=0,
              reg_lambda=1, scale_pos_weight=1, subsample=1, tree_method=None,
              validate_parameters=False, verbosity=None)


# In[ ]:


from sklearn.model_selection import cross_val_score
score=cross_val_score(classifier,X,y,cv=5)


# In[ ]:


score


# In[ ]:


score.mean()


# **IF YOU LIKE IT PLAESE UPVOTE IT**

# In[ ]:




