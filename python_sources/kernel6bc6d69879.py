#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
import xgboost as xgb

import numpy as np


# # Done in jupyter notebook

# In[ ]:


from sklearn.metrics import roc_auc_score


# # Reading data

# In[ ]:


df_train = pd.read_csv('TRAIN_DATA.csv')
df_test = pd.read_csv('TEST_DATA.csv')


# In[ ]:


test_index=df_test['Unnamed: 0']


# In[ ]:


train_X = df_train.loc[:, 'V1':'Class']
train_y = df_train.loc[:, 'Class']


# In[ ]:


test_X=df_test.loc[:,'V1':'V16']


# # Testing correlation

# In[ ]:


corr_matrix=df_train.corr()
corr_matrix['Class'].sort_values()


# In[ ]:





# # Trying to normalize

# In[ ]:


from sklearn import preprocessing
train_Xnorm=preprocessing.normalize([train_X['V6']], norm='l2',axis=1)


# In[ ]:


train_Xnorm=train_Xnorm.reshape(30000,1)


# In[ ]:


train_X['V17']=train_Xnorm


# In[ ]:


test_Xnorm=preprocessing.normalize([df_test['V6']], norm='l2',axis=1)


# In[ ]:


test_Xnorm=test_Xnorm.reshape(15210,1)


# In[ ]:


test_X['V17']=test_Xnorm


# In[ ]:


test_X=test_X.drop('V6',axis=1)


# In[ ]:


train_X=train_X.drop('V6',axis=1)


# In[ ]:


train_X=train_X.drop(['V5',],axis=1)


# In[ ]:


from sklearn import preprocessing
train_Xnorm=preprocessing.normalize([train_X['V12']], norm='l2',axis=1)
test_Xnorm=preprocessing.normalize([test_X['V12']], norm='l2',axis=1)


# In[ ]:


train_Xnorm=train_Xnorm.reshape(30000,1)
test_Xnorm=test_Xnorm.reshape(15210,1)


# In[ ]:


train_X['V18']=train_Xnorm
test_X['V18']=test_Xnorm


# In[ ]:


train_X=train_X.drop('V12',axis=1)
test_X=test_X.drop('V12',axis=1)


# In[ ]:


test_X=test_X.drop(['V5',],axis=1)


# In[ ]:


train_X=train_X.drop('Class',axis=1)


# In[ ]:


train_X.head()


# In[ ]:


train_X['V19']=train_X['V7']+train_X['V8']
test_X['V19']=test_X['V7']+test_X['V8']

train_X.head()
# In[ ]:


train_X.head()


# In[ ]:


train_X=train_X.drop(['V7','V8'],axis=1)


# In[ ]:


test_X=test_X.drop(['V7','V8'],axis=1)


# # Creating new features and dropping old features

# In[ ]:


train_X['V20']=train_X['V3']+train_X['V4']
test_X['V20']=test_X['V3']+test_X['V4']


# In[ ]:


train_X.describe()


# In[ ]:


from sklearn import preprocessing
train_Xnorm=preprocessing.normalize([train_X['V14']], norm='l2',axis=1)
test_Xnorm=preprocessing.normalize([test_X['V14']], norm='l2',axis=1)


# In[ ]:


train_Xnorm=train_Xnorm.reshape(30000,1)
test_Xnorm=test_Xnorm.reshape(15210,1)


# In[ ]:


train_X['V21']=train_Xnorm
test_X['V21']=test_Xnorm


# In[ ]:


train_X=train_X.drop('V14',axis=1)
test_X=test_X.drop('V14',axis=1)


# In[ ]:


train_X.describe()


# In[ ]:


train_X.columns


# In[ ]:


test_X.columns


# In[ ]:


train_X=train_X.drop(['V3','V4'],axis=1)
test_X=test_X.drop(['V3','V4'],axis=1)


# In[ ]:


train_X.columns


# In[ ]:


test_X.columns


# In[ ]:


train_X.describe()


# In[ ]:


test_X.describe()


# In[ ]:





# In[ ]:


train_X.describe()


# In[ ]:





# In[ ]:


train_X.describe()


# In[ ]:


train_X.columns


# In[ ]:


test_X.columns


# In[ ]:





# In[ ]:


train_X.describe()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


train_X.describe()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


train_X.describe()


# In[ ]:





# In[ ]:


train_X.describe()


# In[ ]:


train_X.columns


# In[ ]:


test_X.columns


# In[ ]:





# In[ ]:


train_X.describe()


# In[ ]:





# In[ ]:





# In[ ]:


train_X.describe()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # Using xgboost

# In[ ]:


data_dmatrix = xgb.DMatrix(data=train_X,label=train_y)


# # creating classifier

# In[ ]:


xg_reg = xgb.XGBRegressor(objective ='reg:logistic', colsample_bytree = 0.3, learning_rate = 0.03,
                max_depth =6 , alpha = 10, n_estimators =205,eval_metric='auc')


# In[ ]:





# used trial and error and grid search to calculate optimal hyperparameters

# # Fitting model

# In[ ]:


xg_reg.fit(train_X,train_y)


# # Predicting

# In[ ]:


pred = xg_reg.predict(test_X)
pred=pred*(pred>=0)
pred= (pred*(pred<=1))+ 1*(pred>1)


# In[ ]:


pred


# tested data using train test split by trial and error method
# 

# not able to show cross validation because it was done in another notebook (jupyter)

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # Output

# In[ ]:


result = pd.DataFrame()


# In[ ]:


result['Id'] = test_index


# In[ ]:





# In[ ]:


result['PredictedValue']=pred


# In[ ]:


result


# In[ ]:


result.to_csv('output.csv', index=False)


# In[ ]:





# In[ ]:




