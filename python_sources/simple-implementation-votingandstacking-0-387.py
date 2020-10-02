#!/usr/bin/env python
# coding: utf-8

# ## <center> Bike Sharing Demand - Prediction

# ### Ask:
# Predict the total count of bikes rented during each hour in test set.

# ### Data:
# <br>
# <li> Hourly rental data spanning two years.
# <li> Training set contains first 19 days of each month.
# <li> Test Set contains 20th to end of month.

# ### Features:
# <ol>
# <li> datetime - hourly date + timestamp  
# <li> season -  1 = spring, 2 = summer, 3 = fall, 4 = winter 
# <li> holiday - whether the day is considered a holiday
# <li> workingday - whether the day is neither a weekend nor holiday
# <li> weather - 1: Clear, Few clouds, Partly cloudy, Partly cloudy
# <li> weather - 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
# <li> weather - 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
# <li> weather - 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog 
# <li> temp - temperature in Celsius
# <li> atemp - "feels like" temperature in Celsius
# <li> humidity - relative humidity
# <li> windspeed - wind speed
# <li> casual - number of non-registered user rentals initiated
# <li> registered - number of registered user rentals initiated
# <li> count - number of total rentals
#     </ol>

# In[ ]:


#Import necessary packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sb
from datetime import datetime
import calendar

#Suppress warnings
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


#Read Dataset
df_train = pd.read_csv('/kaggle/input/bike-sharing-demand/train.csv')
df_test = pd.read_csv('/kaggle/input/bike-sharing-demand/test.csv')


# In[ ]:


#Review training set data
df_train.head()


# In[ ]:


#Review test set data
df_test.head()


# In[ ]:


df_train.shape, df_test.shape


# ### Backup data

# In[ ]:


df_train_copy = df_train.copy()
df_test_copy = df_test.copy()


# ---

# In[ ]:


#Reviewing datatypes
df_train.dtypes


# In[ ]:


df_test.dtypes


# In[ ]:


#Saving total number of rows in test and train
ntrain = df_train.shape[0]
ntest = df_test.shape[0]

ntrain, ntest


# In[ ]:


#Let's remove few columns from training set as they are not available in test set.
dcols = ['count', 'casual', 'registered']

#Let's backkup the data first
df_target = df_train[dcols]

#Let's remove them
df_train.drop(dcols, inplace=True, axis=1)


# In[ ]:


df_train.shape, df_test.shape


# In[ ]:


#Let's concatenate train and test data
df_alldata = pd.concat([df_train, df_test], axis=0).reset_index(drop=True)

df_alldata.head(3)


# In[ ]:


df_alldata.shape


# ## Exploratory Data Analysis

# In[ ]:


#Let start our EDA with datetime
df_alldata['datetime'] = pd.to_datetime(df_alldata['datetime'])


# In[ ]:


#New values extracted from datetime -> day, date, hour, month, year
df_alldata['day'] = df_alldata['datetime'].apply(lambda x: calendar.day_name[x.weekday()])
df_alldata['date'] = df_alldata['datetime'].apply(lambda x: x.day)
df_alldata['hour'] = df_alldata['datetime'].apply(lambda x: x.hour)
df_alldata['month'] = df_alldata['datetime'].apply(lambda x: calendar.month_name[x.month])
df_alldata['year'] = df_alldata['datetime'].apply(lambda x:x.year)

df_alldata.head(3)


# In[ ]:


#For simplicity of our model
df_alldata['year'] = df_alldata['year'].map({2011:0, 2012:1})


# In[ ]:


#Let's drop datetime column as we extracted information
df_alldata.drop('datetime', inplace=True, axis=1)


# In[ ]:


#Let's change few more cols as per their values
df_alldata['season'] = df_alldata['season'].map({1:'Spring', 2:'Summer', 3:'Fall', 4:'Winter'})


# In[ ]:


df_alldata['weather'] = df_alldata['weather'].map({1:'Clear-Cloudy', 2:'Misty-Cloudy', 3:'LightRain-Storm', 4:'Rain-Ice'})


# In[ ]:


#Let's check dataset datatypes
df_alldata.dtypes


# In[ ]:


#Let's get catg features
catg_feats = df_alldata.dtypes[df_alldata.dtypes == 'object'].index
catg_feats


# In[ ]:


#Let's onehot encode these categorical feats
for col in catg_feats:
    df_temp = pd.get_dummies(df_alldata[col], prefix=col)
    dcol = df_temp.columns[0]
    df_temp.drop(dcol, inplace=True, axis=1) #Dropping dummy variable trap col
    df_alldata.drop(col, inplace=True, axis=1) #Dropping original column
    df_alldata = pd.concat([df_alldata, df_temp], axis=1).reset_index(drop=True)


# In[ ]:


df_alldata.head(3)


# In[ ]:


df_alldata.dtypes


# ## Preprocessing for Modelling

# In[ ]:


#For submission dataframe saving timestamp
srs_timestamp = df_test['datetime']


# In[ ]:


#Let's split train and test set
df_train = df_alldata[:ntrain]
df_test = df_alldata[ntrain:]

df_train.shape, df_test.shape


# In[ ]:


## Setting up target variable
target = np.log1p(df_target['count'])

len(target)


# ## Defining Cross Validation and Error Function

# In[ ]:


from sklearn.model_selection import KFold

cross_val = KFold(n_splits=10, random_state=42, shuffle=True)


# In[ ]:


#Calculating RMSLE
def rmsle(y, y_pred):
    assert len(y) == len(y_pred), 'Error in actual and prediction length.'
    return np.sqrt(np.mean((np.log1p(y) - np.log1p(y_pred))**2))

#np.sqrt(mean_squared_log_error(y, y_pred))


# ## Model and Parameter Tuning

# In[ ]:


#List of models to try
import xgboost as xgb
from sklearn.linear_model import RidgeCV, Ridge, LassoCV, Lasso, ElasticNetCV, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import lightgbm as lgbm
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.metrics import mean_squared_log_error


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(df_train.values, target, test_size=0.3, random_state=42)


# In[ ]:


X_train.shape, X_test.shape


# In[ ]:


#Function to store model parameters and score

cols = ['Model', 'Parameters', 'Xtrain_RMSLE', 'Xtest_RMSLE', 'dftrain_RMSLE', 'exp_dftrain_RMSLE']
df_model_scores = pd.DataFrame(columns=cols)


def model_scores(model, df_model_scores = df_model_scores, X_train = X_train, y_train = y_train, X_test = X_test, 
                 y_test = y_test, df_train = df_train, target = target):
    #Fit with Xtrain
    model.fit(X_train, y_train)
    
    #Predict X_train
    pred = model.predict(X_train)
    
    #X_train RMSLE
    xtr_rmsle = rmsle(y_train, pred)
    
    #Predict X_test
    pred = model.predict(X_test)
    
    #X_test rmsle
    xts_rmsle = rmsle(y_test, pred)
    
    #Predict df_train
    model.fit(df_train.values, target)
    pred = model.predict(df_train.values)
    dftr_rmsle = rmsle(target, pred)
    expdftr_rmsle = rmsle(np.expm1(target), np.expm1(pred))
    
    #setting up values for data frame
    mdl = model.__class__.__name__
    param = str(model.get_params())
    
    data = {'Model':[mdl], 'Parameters':[param], 'Xtrain_RMSLE':[xtr_rmsle], 'Xtest_RMSLE':[xts_rmsle], 
                           'dftrain_RMSLE':[dftr_rmsle], 'exp_dftrain_RMSLE':[expdftr_rmsle]}
    
    df_temp = pd.DataFrame(data)
    
    df_model_scores = pd.concat([df_model_scores, df_temp]).reset_index(drop=True)
    
    return df_model_scores


# ### XGBoost Model

# In[ ]:


#Let's find optimum parameters for each model
model_xgb = xgb.XGBRegressor(n_estimators=1000, n_jobs=-1, objective='reg:squarederror', random_state=42)


# In[ ]:


xgb_param_grid={'max_depth':[5, 6],
               'learning_rate':[0.1],
               'booster':['gbtree','dart']}


# In[ ]:


#Implement Grid Search over XGBoost
gs_xgb_model = GridSearchCV(param_grid=xgb_param_grid, estimator=model_xgb, cv=cross_val, verbose=1, n_jobs=-1)
# gs_xgb_model.fit(X_train, y_train)#Training the Model
# print('Best Score:', gs_xgb_model.best_score_)
# print('Parameters:', gs_xgb_model.best_params_)


# In[ ]:


xgb_param_grid = {'booster':['gbtree', 'gblinear', 'dart']}


# In[ ]:


#Gathering model scores
model_xgb = xgb.XGBRegressor(n_estimators=1000, n_jobs=-1, objective='reg:squarederror', random_state=42, max_depth=5, 
                             booster='dart')
df_model_scores = model_scores(model_xgb, df_model_scores)
df_model_scores


# In[ ]:


#Model Training
model_xgb.fit(X_train, y_train)

#Model Prediction
pred=model_xgb.predict(df_test.values)

#Submission
pred = np.expm1(pred)

#Rounding prediction
sr_pred = pd.Series(data=pred, name='count')
sr_pred = sr_pred.apply(lambda x: round(x,0))

submission = pd.DataFrame({'datetime':srs_timestamp, 'count':sr_pred})
submission.head()


# In[ ]:


#Saving Submission
submission.to_csv('1119_xgb.csv', index=False)


# ### Submission Secured 0.40167

# ### Ridge

# In[ ]:


alphas_ridge = [14.5, 14.6, 14.7, 14.8, 14.9, 15, 15.1, 15.2, 15.3, 15.4, 15.5]
alphas_lasso = [5e-05, 0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008]
elastic_alphas = [0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007]
elastic_l1ratio = [0.8, 0.85, 0.9, 0.95, 0.99, 1]


# In[ ]:


#RidgeCV
rcv = RidgeCV(alphas=alphas_ridge, cv=10, scoring='neg_mean_squared_log_error')


# In[ ]:


rcv.fit(X_train, y_train)


# In[ ]:


rcv.alpha_


# In[ ]:


#Finding best alpha round 2
alphas_ridge = [0.1, 1, 5, 8, 10, 12, 14, 14.5]
rcv = RidgeCV(alphas_ridge, cv=10, scoring='neg_mean_squared_log_error')
rcv.fit(X_train, y_train)
rcv.alpha_


# In[ ]:


#Finding best alpha round 3
alphas_ridge = [0.1, 0.01, 0.5, 0.001, 0.3]
rcv = RidgeCV(alphas_ridge, cv=10, scoring='neg_mean_squared_log_error')
rcv.fit(X_train, y_train)
rcv.alpha_


# In[ ]:


#Finding best alpha round 4
alphas_ridge = [0.001, 0.005, 0.015, 0.003, 0.008]
rcv = RidgeCV(alphas_ridge, cv=10, scoring='neg_mean_squared_log_error')
rcv.fit(X_train, y_train)
rcv.alpha_


# In[ ]:


model_ridge = Ridge(alpha=0.001, max_iter=10000, random_state=42)


# In[ ]:


df_model_scores = model_scores(model_ridge, df_model_scores)
df_model_scores


# ### Lasso

# In[ ]:


lcv = LassoCV(alphas=alphas_lasso, max_iter=1000, cv=10, n_jobs=-1, selection='random', random_state=42, verbose=1)


# In[ ]:


lcv.fit(X_train, y_train)
lcv.alpha_


# In[ ]:


#Computing best alpha round 2
alphas = [0.0002, 0.0003, 0.00025, 0.0015]
lcv = LassoCV(alphas = alphas, max_iter=10000, cv=10, n_jobs=-1, selection='random', random_state=42, verbose=1)
lcv.fit(X_train, y_train)
lcv.alpha_


# In[ ]:


model_lasso = Lasso(alpha=0.0002, max_iter=10000, random_state=42, selection='cyclic')
df_model_scores = model_scores(model_lasso, df_model_scores)
df_model_scores


# ### Random Forest Regressor

# In[ ]:


model_rf = RandomForestRegressor(random_state=42)

grid_rf = {'max_depth':[2, 3, 5],
           'n_estimators':[200],
          'criterion':['mse','mae']}

GSearch = GridSearchCV(param_grid=grid_rf, estimator=model_rf, cv=10, n_jobs=-1, verbose=1)

GSearch.fit(X_train, y_train)

print('Best Score:', GSearch.best_score_)
print('Parameters:', GSearch.best_params_)


# In[ ]:


GSearch.best_params_


# In[ ]:


model_rf = RandomForestRegressor(n_estimators=200, random_state=42, max_depth=5, criterion='mse')


# In[ ]:


df_model_scores = model_scores(model_rf, df_model_scores)
df_model_scores


# ### Light GBM

# In[ ]:


model_lgbm = lgbm.LGBMRegressor(n_estimators=1000, objective='regression', random_state=42, n_jobs=-1)

grid_lgbm = {'learning_rate':[0.02, 0.05, 0.08]}

GSearch = GridSearchCV(param_grid=grid_lgbm, estimator=model_lgbm, cv=10, n_jobs=-1, verbose=1)

GSearch.fit(X_train,y_train)

print('Best Score:', GSearch.best_score_)
print('Parameters:', GSearch.best_params_)


# In[ ]:


model_lgbm = lgbm.LGBMRegressor(n_estimators=1000, objective='regression', random_state=42, n_jobs=-1, learning_rate=0.05)

df_model_scores = model_scores(model_lgbm, df_model_scores)

df_model_scores


# ### ElasticNet

# In[ ]:


#Round 2
elastic_alphas = [0.0003, 0.00035, 0.00028]
elastic_l1ratio = [0.7, 0.75, 0.8]
ecv = ElasticNetCV(alphas=elastic_alphas, l1_ratio=elastic_l1ratio, cv=10, n_jobs=-1, random_state=42, max_iter=10000)
ecv.fit(X_train, y_train)
ecv.alpha_, ecv.l1_ratio_


# In[ ]:


#Round 3
elastic_l1ratio = [0.6, 0.5, 0.7]
elastic_alphas = [0.0003]
ecv = ElasticNetCV(alphas = elastic_alphas, l1_ratio=elastic_l1ratio, cv=10, n_jobs=-1, random_state=42, max_iter=10000)
ecv.fit(X_train, y_train)
ecv.alpha_, ecv.l1_ratio_


# In[ ]:


#Round 4
elastic_l1ratio = [0.3, 0.2, 0.5]
elastic_alphas = [0.0003]
ecv = ElasticNetCV(alphas = elastic_alphas, l1_ratio=elastic_l1ratio, cv=10, n_jobs=-1, random_state=42, max_iter=10000)
ecv.fit(X_train, y_train)
ecv.alpha_, ecv.l1_ratio_


# In[ ]:


model_elastic = ElasticNet(alpha=0.0003, l1_ratio=0.5, random_state=42, max_iter=10000)
df_model_scores = model_scores(model_elastic, df_model_scores)
df_model_scores


# ### Gradient Boosting Model

# In[ ]:


model_GB = GradientBoostingRegressor(n_estimators=300, random_state=42)

GSearch_param = {'max_depth':[3,5],
             'learning_rate':[0.1, 0.01, 0.3],
                'alpha':[0.5, 0.1, 0.9]}

GSearch_GB = GridSearchCV(param_grid=GSearch_param, estimator=model_GB, cv=10, n_jobs=-1, verbose=2)

GSearch_GB.fit(X_train, y_train)

print('Best Score:', GSearch_GB.best_score_)
print('Best Param:', GSearch_GB.best_params_)


# In[ ]:


model_gb = GradientBoostingRegressor(n_estimators=300, random_state=42, max_depth=5, alpha=0.5)
df_model_scores = model_scores(model_gb, df_model_scores)
df_model_scores


# ### Voting Regressor

# In[ ]:


from sklearn.ensemble import VotingRegressor

model_vote = VotingRegressor([('XGBoost', model_xgb), ('LGBM', model_lgbm), ('GradientBoosting', model_gb)])
model_vote.fit(X_train, y_train)
pred = model_vote.predict(df_test.values)


# In[ ]:


df_model_scores = model_scores(model_vote, df_model_scores)
df_model_scores


# In[ ]:


#Model Training
model_vote.fit(X_train, y_train)

#Model Prediction
pred=model_vote.predict(df_test.values)

#Submission
pred = np.expm1(pred)

#Rounding prediction
sr_pred = pd.Series(data=pred, name='count')
sr_pred = sr_pred.apply(lambda x: round(x,0))

submission = pd.DataFrame({'datetime':srs_timestamp, 'count':sr_pred})
submission.head()


# In[ ]:


submission.to_csv('VotingModelResults.csv', index=False)


# ### Voting Model Secured 0.38715

# ### Stacking Regressor

# In[ ]:


from mlxtend.regressor import StackingRegressor

stack_reg = StackingRegressor(regressors=[model_gb, model_lgbm], meta_regressor=model_xgb, 
                              use_features_in_secondary=False)

df_model_scores = model_scores(stack_reg, df_model_scores)
df_model_scores


# In[ ]:


df_model_scores.to_csv('Kaggle_Bike_Sharing_Model.csv')


# In[ ]:


stack_reg.fit(X_train, y_train)
pred = stack_reg.predict(df_test.values)
x = pred[:5]
np.expm1(x)


# ---
