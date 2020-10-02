#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import linear_model
from sklearn.model_selection import train_test_split 
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV


# In[ ]:


df=pd.read_csv("/kaggle/input/eval-lab-1-f464-v2/train.csv")
df2=pd.read_csv("/kaggle/input/eval-lab-1-f464-v2/test.csv")


# In[ ]:


df.info()


# In[ ]:


df2.info()


# In[ ]:


df.head(n=10)


# In[ ]:


df.isnull().values.any()


# In[ ]:


df2.isnull().values.any()


# In[ ]:


null_columns_testSet=df2.columns[df2.isnull().any()] 
df2[null_columns_testSet].isnull().sum()


# In[ ]:


print(df2[df2.isnull().any(axis=1)][null_columns_testSet].head())


# In[ ]:


df2.fillna(value=df2.mean(),inplace=True)


# In[ ]:


null_columns_trainSetafterreplacement=df.columns[df.isnull().any()] 
df[null_columns_trainSetafterreplacement].isnull().sum()


# In[ ]:


null_columns_trainSet=df.columns[df.isnull().any()] 
df[null_columns_trainSet].isnull().sum()


# In[ ]:


print(df[df.isnull().any(axis=1)][null_columns_trainSet].head())
# df.isnull().head(5)


# In[ ]:


df.fillna(value=df.mean(),inplace=True)


# In[ ]:


null_columns=df.columns[df.isnull().any()] 
df[null_columns].isnull().sum()


# In[ ]:


high_corr=df.corr()
high_corr['rating']


# In[ ]:


Y=df['rating']
X= df.drop(['id','feature1','feature3','feature5','feature7','feature9','feature10','type','rating'],axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


# In[ ]:


# scaler = StandardScaler()
# scaler.fit(X_train)

# X_train = scaler.transform(X_train)
# X_test = scaler.transform(X_test)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier

rforest=RandomForestClassifier(n_estimators=1000, max_features= 'auto', max_depth= 110)
rforest.fit(X_train,y_train)
# from sklearn.ensemble import RandomForestClassifier
# rforest=RandomForestClassifier(bootstrap=True,n_estimators=100,max_depth=110,
#                                   max_features=3, min_samples_leaf=3, min_samples_split=8)
# rforest.fit(X_train,y_train)


# In[ ]:


from sklearn import metrics
rf_predictions = rforest.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, rf_predictions))


# In[ ]:


# rf_predictions


# In[ ]:


import math
print(math.sqrt(mean_squared_error(rf_predictions,y_test)))


# In[ ]:


ID=df2['id']
df2.drop(['id','feature1','feature3','feature5','feature7','feature9','feature10','type'],axis=1,inplace=True)


# In[ ]:


Y_dfpred=pd.DataFrame()
Y_dfpred['id']=ID
pred=rforest.predict(df2)
Y_dfpred['rating']=list(pred)


# In[ ]:


# Y_dfpred.to_csv('Output5.csv',index=False)


# In[ ]:


# param_grid = {
#     'bootstrap': [True],
#     'max_depth': [80, 90, 100, 110],
#     'max_features': [2, 3],
#     'min_samples_leaf': [3, 4, 5],
#     'min_samples_split': [8, 10, 12],
#     'n_estimators': [100, 200, 300, 1000]
# }
# grid_s=GridSearchCV(estimator = rforest, param_grid = param_grid, 
#                         cv = 3, n_jobs = -1, verbose = 2)


# In[ ]:


# grid_s.fit(X_train,y_train)
# grid_s.best_params_


# In[ ]:


# rforest=RandomForestClassifier(bootstrap=True,n_estimators=1000,max_depth=110,
#                                   max_features=2, min_samples_leaf=10, min_samples_split=10)
# rforest.fit(X_train,y_train)


# In[ ]:


# from sklearn import metrics
# rf_predictions = rforest.predict(X_test)
# print("Accuracy:",metrics.accuracy_score(y_test, rf_predictions))


# In[ ]:




