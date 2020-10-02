#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd 

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


df_train = pd.read_csv('/kaggle/input/train.csv/train.csv')
df_test = pd.read_csv('/kaggle/input/test.csv/test.csv')


# In[ ]:


#df_train.shape
#df_train.head(10)
df_train.describe()


# In[ ]:


#df_test.shape
df_test.head(10)


# In[ ]:


df_train.info()


# In[ ]:


df_test.info()


# In[ ]:


#df_train.isnull().sum()
df_train.columns[df_train.isnull().sum()!=0].size


# In[ ]:


#df_test.isnull().sum()
df_test.columns[df_test.isnull().sum()!=0].size


# In[ ]:


df_train['target']


# In[ ]:


constantColumns = []
for i in df_train.columns:
    if i !='ID' and i!= 'target':
        if df_train[i].std()==0:
            constantColumns.append(i)


# In[ ]:


df_train.drop(constantColumns,axis = 1,inplace=True)
df_test.drop(constantColumns,axis = 1,inplace=True)

print("Total count of Constant Columns : '{}'".format(len(constantColumns)))
print(constantColumns)


# In[ ]:


get_ipython().run_cell_magic('time', '', 'def Duplicate_Columns(dataFrame):\n    groups = dataFrame.columns.to_series().groupby(dataFrame.dtypes).groups\n    duplicateValues = []\n    \n    for t,v in groups.items():\n        \n        colmn = dataFrame[v].columns\n        val = dataFrame[v]\n        lenColmn = len(colmn)\n        \n        for i in range(lenColmn):\n            iValue = val.iloc[:,i].values\n            for j in range(i+1,lenColmn):\n                jValue = val.iloc[:,j].values\n                if np.array_equal(iValue,jValue):\n                    duplicateValues.append(colmn[i])\n                    break \n    return duplicateValues\n\n\nDuplicateColumns = Duplicate_Columns(df_train)\nprint(DuplicateColumns)')


# In[ ]:


df_train.drop(DuplicateColumns,axis = 1,inplace=True)
df_test.drop(DuplicateColumns,axis=1,inplace=True)

print("Removed '{}' Duplicate Columns".format(len(DuplicateColumns)))
print(DuplicateColumns)


# In[ ]:


def Remove_Sparse(train,test):
    datalist = [x for x in train.columns if not x in ['ID','target']]
    for f in datalist:
        if len(np.unique(train[f]))<2:
            train.drop(f,axis=1,inplace=True)
            test.drop(f,axis=1,inplace=True)
    return train,test


# In[ ]:


get_ipython().run_cell_magic('time', '', 'df_train,df_test = Remove_Sparse(df_train,df_test)')


# In[ ]:


import gc


# In[ ]:


gc.collect()
print("New Train Data Size : {}".format(df_train.shape))
print("New Test Data Size : {}".format(df_test.shape))


# In[ ]:


#Test and Train
XTrain = df_train.drop(["ID","target"], axis=1)
YTrain = np.log1p(df_train["target"].values)

XTest = df_test.drop(["ID"],axis=1)


# In[ ]:


from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler


# In[ ]:


dev_X, val_X, dev_y, val_y = train_test_split(XTrain,YTrain,test_size=0.2,random_state =42 )


# In[ ]:


import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostRegressor


# In[ ]:


def _LightGBM_(XTrain,YTrain,val_X,val_Y,XTest):
    param = {"objective" : "regression", "metric" : "rmse", "num_leaves" : 40 , "learning_rate" : 0.004, "bagging_fraction" : 0.6,
             "feature_fraction" : 0.6, "bagging_frequency" : 6, "bagging_seed" : 42,"verbosity" : -1,"seed" : 42 }
    
    LGBtrain = lgb.Dataset(XTrain, label=YTrain)
    LGBtest = lgb.Dataset(val_X,label=val_Y)
    result = {}
    model = lgb.train(param,LGBtrain,5000,
                     valid_sets=[LGBtrain,LGBtest],
                     early_stopping_rounds=100,
                      verbose_eval= 150,
                      evals_result= result)
    pred_testY = np.expm1(model.predict(XTest,num_iteration = model.best_iteration))
    return pred_testY,model,result


# In[ ]:


pred_Test,model,result = _LightGBM_(dev_X,dev_y,val_X,val_y,XTest)
print("LightGBM Training Over")


# In[ ]:


gain = model.feature_importance('gain')
ftImp = pd.DataFrame({'feature' : model.feature_name(),
                     'split' : model.feature_importance('split'),
                     'gain': 100*gain / gain.sum()}).sort_values('gain',ascending=False)

print(ftImp[:25])
print("Feature Tuning Done.....")


# In[ ]:


#Practice XG Boost
def _XGBoost_(XTrain,YTrain,val_X,val_y,XTest):
    param={'objective' : 'reg:linear', 'eval_metric': 'rmse', 'eta' : 0.001, 'max_depth' : 10, 'subsample' : 0.6,
          'alpha': 0.001,'random_state': 42,'silent': True, 'colsample_bytree' : 0.6}
    
    train_data_xgb = xgb.DMatrix(XTrain,YTrain)
    test_data_xgb = xgb.DMatrix(val_X,val_y)
    
    watchlist = [(train_data_xgb,'train'),(test_data_xgb,'valid')]
    model_xgb = xgb.train(param,train_data_xgb,2000,watchlist,maximize = False,early_stopping_rounds=100,verbose_eval=100)
    dtest = xgb.DMatrix(XTest)
    xgb_pred_y = np.expm1(model_xgb.predict(dtest, ntree_limit=model_xgb.best_ntree_limit ) )
    return xgb_pred_y,model_xgb


# In[ ]:


pred_test_xgb, model_xgb = _XGBoost_(dev_X, dev_y, val_X, val_y, XTest)
print("XGB Training Completed...")


# In[ ]:


cb_model = CatBoostRegressor(iterations=500,
                             learning_rate=0.05,
                             depth=10,
                             eval_metric='RMSE',
                             random_seed = 42,
                             bagging_temperature = 0.2,
                             od_type='Iter',
                             metric_period = 50,
                             od_wait=20)


# In[ ]:


cb_model.fit(dev_X, dev_y,
             eval_set=(val_X, val_y),
             use_best_model=True,
             verbose=50)


# In[ ]:


pred_test_cat = np.expm1(cb_model.predict(XTest))


# In[ ]:


sub = pd.read_csv('/kaggle/input/sample_submission.csv/sample_submission.csv')


# In[ ]:


subLGB = pd.DataFrame()
subLGB["target"] = pred_Test

subXGB = pd.DataFrame()
subXGB["target"] =  pred_test_xgb

subCGB = pd.DataFrame()
subCGB["target"] =  pred_test_cat

sub['target'] = (subLGB["target"]*0.5+subXGB["target"]*3+subCGB["target"]*0.2)


# In[ ]:


sub.head()


# In[ ]:


import warnings
warnings.filterwarnings('ignore')
sub.to_csv('finalSample.csv',index=False)


# In[ ]:




