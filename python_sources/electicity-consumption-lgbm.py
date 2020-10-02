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


from fastai import *
from fastai.tabular import *


# In[ ]:


train = pd.read_csv('/kaggle/input/electrical-consumption/train_6BJx641.csv')
test =  pd.read_csv('/kaggle/input/electrical-consumption/test_pavJagI.csv')
print(train.shape)
print(test.shape)


# In[ ]:


comb = pd.concat([train,test])
print(comb.shape)


# In[ ]:


comb['datetime'] = pd.to_datetime(comb['datetime'])


# PRE-PROCESSING

# In[ ]:


comb.head()


# In[ ]:


from pykalman import KalmanFilter
def Kalman1D(observations,damping=1):
    # To return the smoothed time series data
    observation_covariance = damping
    initial_value_guess = observations[0]
    transition_matrix = 1
    transition_covariance = 0.1
    initial_value_guess
    kf = KalmanFilter(
            initial_state_mean=initial_value_guess,
            initial_state_covariance=observation_covariance,
            observation_covariance=observation_covariance,
            transition_covariance=transition_covariance,
            transition_matrices=transition_matrix
        )
    pred_state, state_cov = kf.smooth(observations)
    return pred_state

# Kalman Filter
observation_covariance = .0015
comb['temperature'] = Kalman1D(comb.temperature.values,observation_covariance)
comb['var1'] = Kalman1D(comb.var1.values,observation_covariance)
comb['pressure'] = Kalman1D(comb.pressure.values,observation_covariance)
comb['windspeed'] = Kalman1D(comb.windspeed.values,observation_covariance)
#test['signal'] = Kalman1D(test.signal.values,observation_covariance)


# WINDOWS=[3,5]
# def create_rolling_features(df):
#     for window in WINDOWS:
#         df["rolling_mean_temp_" + str(window)] = df['temperature'].rolling(window=window).mean()
#         df["rolling_std_temp_" + str(window)] = df['temperature'].rolling(window=window).std()
#         df["rolling_var_temp_" + str(window)] = df['temperature'].rolling(window=window).var()
#         df["rolling_min_temp_" + str(window)] = df['temperature'].rolling(window=window).min()
#         df["rolling_max_temp_" + str(window)] = df['temperature'].rolling(window=window).max()
#         df["rolling_min_max_ratio_temp_" + str(window)] = df["rolling_min_temp_" + str(window)] / df["rolling_max_temp_" + str(window)]
#         df["rolling_min_max_diff_temp_" + str(window)] = df["rolling_max_temp_" + str(window)] - df["rolling_min_temp_" + str(window)]
#         
#         df["rolling_mean_var1_" + str(window)] = df['var1'].rolling(window=window).mean()
#         df["rolling_std_var1_" + str(window)] = df['var1'].rolling(window=window).std()
#         df["rolling_var_var1_" + str(window)] = df['var1'].rolling(window=window).var()
#         df["rolling_min_var1_" + str(window)] = df['var1'].rolling(window=window).min()
#         df["rolling_max_var1_" + str(window)] = df['var1'].rolling(window=window).max()
#         df["rolling_min_max_ratio_var1_" + str(window)] = df["rolling_min_var1_" + str(window)] / df["rolling_max_var1_" + str(window)]
#         df["rolling_min_max_diff_var1_" + str(window)] = df["rolling_max_var1_" + str(window)] - df["rolling_min_var1_" + str(window)]
#         
#         df["rolling_mean_pressure_" + str(window)] = df['pressure'].rolling(window=window).mean()
#         df["rolling_std_pressure_" + str(window)] = df['pressure'].rolling(window=window).std()
#         df["rolling_var_pressure_" + str(window)] = df['pressure'].rolling(window=window).var()
#         df["rolling_min_pressure_" + str(window)] = df['pressure'].rolling(window=window).min()
#         df["rolling_max_pressure_" + str(window)] = df['pressure'].rolling(window=window).max()
#         df["rolling_min_max_ratio_pressure_" + str(window)] = df["rolling_min_pressure_" + str(window)] / df["rolling_max_pressure_" + str(window)]
#         df["rolling_min_max_diff_pressure_" + str(window)] = df["rolling_max_pressure_" + str(window)] - df["rolling_min_pressure_" + str(window)]
#         
#         df["rolling_mean_windspeed" + str(window)] = df['windspeed'].rolling(window=window).mean()
#         df["rolling_std_windspeed" + str(window)] = df['windspeed'].rolling(window=window).std()
#         df["rolling_var_windspeed" + str(window)] = df['windspeed'].rolling(window=window).var()
#         df["rolling_min_windspeed" + str(window)] = df['windspeed'].rolling(window=window).min()
#         df["rolling_max_windspeed" + str(window)] = df['windspeed'].rolling(window=window).max()
#         df["rolling_min_max_ratio_windspeed" + str(window)] = df["rolling_min_windspeed" + str(window)] / df["rolling_max_windspeed" + str(window)]
#         df["rolling_min_max_diff_windspeed" + str(window)] = df["rolling_max_windspeed" + str(window)] - df["rolling_min_windspeed" + str(window)]    
#     
#     
#     df = df.replace([np.inf, -np.inf], np.nan)    
#     df.fillna(0, inplace=True)
#     return df
# 
# comb = create_rolling_features(comb)
# #test = create_rolling_features(test)

# In[ ]:


def booleancon(x):
    if x == True:
        return 1
    else:
        return 0
    


def daypart(x):
    if x >= 0 and x<=4:
        return 101
    elif x>=5 and x<=8:
        return 102
    elif x>=9 and x<=12:
        return 103
    elif x>=13 and x<=16:
        return 104
    elif x>=17 and x<=19:
        return 105
    elif x>=20 and x<=23:
        return 106
    else:
        return 0
    
def seasons(x):
    if x>=3 and x<5:
        return 0
    elif x>=6 and x<=8:
        return 1
    elif x>=9 and x<=11:
        return 2
    elif x>=12 and x<=2:
        return 3
    else:
        return 0
    
def var2(x):
    if x=='A':
        return 1
    elif x=='B':
        return 2
    else:
        return 3

def time_pr(train):
    train = add_datepart(train,'datetime',drop=False,time=True)
    #train.drop(['datetimeIs_month_end', 'datetimeIs_quarter_end','datetimeIs_year_start','datetimeIs_year_end'], axis=1, inplace=True)
    train['datetimeIs_month_end'] = train['datetimeIs_month_end'].apply(booleancon)
    train['datetimeIs_month_start']   = train['datetimeIs_month_start'].apply(booleancon)
    train['datetimeIs_quarter_start'] = train['datetimeIs_quarter_start'].apply(booleancon)
    train['datetimeIs_quarter_end'] = train['datetimeIs_quarter_end'].apply(booleancon)
    train['datetimeIs_year_start'] = train['datetimeIs_quarter_start'].apply(booleancon)
    train['datetimeIs_year_end'] = train['datetimeIs_quarter_end'].apply(booleancon)
    train['var2'] = train['var2'].apply(var2)
    train['daypart'] = train['datetimeHour'].apply(daypart)
    train['season'] = train['datetimeMonth'].apply(seasons)
    train['year_month'] = train['datetimeYear'].astype(str)+'_'+train['datetimeMonth'].astype(str)
    train['MonthCat'] = 'M'+train['datetimeMonth'].astype(str)
    train['HourCat'] = 'H'+train['datetimeHour'].astype(str)
    for c in ['temperature','var1','pressure','datetimeElapsed']:
        d = {}
        d['mean'+c] = train.groupby(['year_month'])[c].mean()
        d['median'+c] = train.groupby(['year_month'])[c].median()
        d['max'+c] = train.groupby(['year_month'])[c].max()
        d['min'+c] = train.groupby(['year_month'])[c].min()
        d['std'+c] = train.groupby(['year_month'])[c].std()
        d['mean_abs_chg'+c] = train.groupby(['year_month'])[c].apply(lambda x: np.mean(np.abs(np.diff(x))))
        d['abs_max'+c] = train.groupby(['year_month'])[c].apply(lambda x: np.max(np.abs(x)))
        d['abs_min'+c] = train.groupby(['year_month'])[c].apply(lambda x: np.min(np.abs(x)))
        for v in d:
            train[v] = train['year_month'].map(d[v].to_dict())
        train['range'+c] = train['max'+c] - train['min'+c]
        train['maxtomin'+c] = train['max'+c] / train['min'+c]
        train['abs_avg'+c] = (train['abs_min'+c] + train['abs_max'+c]) / 2
    for c in ['temperature','var1','pressure','datetimeElapsed']:
        train['signal_shift_+1'+c] = train.groupby(['year_month'])[c].shift(1)
        train['signal_shift_-1'+c] = train.groupby(['year_month'])[c].shift(-1)
        train['signal_shift_+2'+c] = train.groupby(['year_month'])[c].shift(2)
        train['signal_shift_-2'+c] = train.groupby(['year_month'])[c].shift(-2)
        train['signal_shift_+3'+c] = train.groupby(['year_month'])[c].shift(3)
        train['signal_shift_-3'+c] = train.groupby(['year_month'])[c].shift(-3)
        train['signal_shift_+4'+c] = train.groupby(['year_month'])[c].shift(4)
        train['signal_shift_-4'+c] = train.groupby(['year_month'])[c].shift(-4)
        train['signal_shift_+5'+c] = train.groupby(['year_month'])[c].shift(5)
        train['signal_shift_-5'+c] = train.groupby(['year_month'])[c].shift(-5)
        
        train['signal_shift_+5'+c] = train.groupby(['year_month'])[c].shift(5)
        train['signal_shift_-5'+c] = train.groupby(['year_month'])[c].shift(-5)
    return train


# In[ ]:


pd.set_option('display.max_columns', 1000)  # or 1000
pd.set_option('display.max_rows', 1000)  # or 1000
pd.set_option('display.max_colwidth', 199)  # or 199
comb = time_pr(comb)


# In[ ]:


comb.head()


# Modeling

# In[ ]:


dummy_train = comb[comb['datetimeDay']<=16].fillna(method='bfill')
dummy_test = comb[(comb['datetimeDay']>16) & (comb['datetimeDay']<=23)].fillna(method='bfill')


# In[ ]:


col = []
for i in comb.columns:
    if i!= 'electricity_consumption' and i!='ID' and i!='datetime' and i!='year_month' and i!='MonthCat' and i!='HourCat':
        col.append(i)


# In[ ]:


actual_data = comb[comb['datetimeDay']<=23].fillna(method='bfill')


# In[ ]:


X = actual_data[col].values
Y = actual_data['electricity_consumption'].values


# In[ ]:


x_train = dummy_train[col].values
y_train = dummy_train['electricity_consumption'].values
x_test = dummy_test[col].values
y_test = dummy_test['electricity_consumption'].values


# LGBM

# In[ ]:


import lightgbm as lgb
d_train = lgb.Dataset(x_train, label=y_train)
d_test = lgb.Dataset(x_test, label=y_test)
params = {}
params['application']='root_mean_squared_error'
params['num_boost_round'] = 1000
params['learning_rate'] = 0.015
params['boosting_type'] = 'gbdt'
params['metric'] = 'rmse'
params['sub_feature'] = 0.833
params['num_leaves'] = 15
params['min_split_gain'] = 0.05
params['min_child_weight'] = 27
params['max_depth'] = -1
params['num_threads'] = 10
params['max_bin'] = 217
params['lambda_l2'] = 0.10
params['lambda_l1'] = 0.30
params['feature_fraction']= 0.833
params['bagging_fraction']= 0.979
params['seed']=42
clf = lgb.train(params, d_train, 2000,d_test,verbose_eval=200, early_stopping_rounds=200)


# In[ ]:


# 42  [995]	valid_0's rmse: 91.8676


# XGBOOST

# In[ ]:


from xgboost import XGBRegressor
p=XGBRegressor(n_estimators=30000,random_state=1729,learning_rate=0.017,max_depth=4,n_jobs=4)
# max_depth=5,0.018
p.fit(x_train,y_train,eval_set=[(x_test, y_test)],eval_metric='rmse',early_stopping_rounds=500,verbose=200)
#p.fit(X,Y)


# In[ ]:





# CatBoost

# In[ ]:


from catboost import CatBoostRegressor
cb_model = CatBoostRegressor(n_estimators = 1000,
    loss_function = 'RMSE',
    eval_metric = 'RMSE',random_state=1729)
cb_model.fit(x_train, y_train, use_best_model=True, eval_set=(x_test, y_test), early_stopping_rounds=50)


# In[ ]:


d_train = lgb.Dataset(X, label=Y)
params = {}
params['application']='root_mean_squared_error'
params['num_boost_round'] = 1000
params['learning_rate'] = 0.015
params['boosting_type'] = 'gbdt'
params['metric'] = 'rmse'
params['sub_feature'] = 0.833
params['num_leaves'] = 15
params['min_split_gain'] = 0.05
params['min_child_weight'] = 27
params['max_depth'] = -1
params['num_threads'] = 10
params['max_bin'] = 217
params['lambda_l2'] = 0.10
params['lambda_l1'] = 0.30
params['feature_fraction']= 0.833
params['bagging_fraction']= 0.979
params['seed']=42
clf = lgb.train(params, d_train, 2000)


# In[ ]:


# p=XGBRegressor(n_estimators=30000,random_state=1729,learning_rate=0.017,max_depth=4,n_jobs=4)
# # max_depth=5,0.018
# p.fit(X,Y)


# In[ ]:


test = comb[comb['datetimeDay']>23]
x_test = test[col].values
pred = clf.predict(x_test)
test['electricity_consumption'] =[round(i) for i in pred]
test[['ID','electricity_consumption']].to_csv('result.csv',header=True,index = None)


# In[ ]:


col_dict ={}
z=0
for i in col:
    col_dict[i]=z
    z=z+1
    


# In[ ]:


lgb.plot_importance(clf,importance_type='split', max_num_features=25)


# In[ ]:





# In[ ]:




