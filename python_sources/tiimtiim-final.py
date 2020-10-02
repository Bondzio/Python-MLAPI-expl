#!/usr/bin/env python
# coding: utf-8

# Kaggle competition submission from TiimTiim. Started out from LGBM Baseline model https://www.kaggle.com/morituri/lgbm-baseline but is quite modified, with additional logic for missing values and 10 fold stratified models for each meter type.

# # Imports

# In[ ]:


import numpy as np
import pandas as pd
import gc
import matplotlib.pyplot as plt

import seaborn as sns
import matplotlib.patches as patches
pd.set_option('max_columns', 150)
from datetime import timedelta
import random

from sklearn.model_selection import train_test_split, KFold, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.experimental import enable_iterative_imputer 
from sklearn.impute import IterativeImputer


# # Training data

# Load the data reducing its size

# In[ ]:


metadata_dtype = {'site_id':"uint8",'building_id':'uint16','square_feet':'float32','year_built':'float32','floor_count':"float16"}
weather_dtype = {"site_id":"uint8",'air_temperature':"float16",'cloud_coverage':"float16",'dew_temperature':"float16",'precip_depth_1_hr':"float16",
                 'sea_level_pressure':"float32",'wind_direction':"float16",'wind_speed':"float16"}
train_dtype = {'meter':"uint8",'building_id':'uint16'}


# In[ ]:


get_ipython().run_cell_magic('time', '', '\nweather_train = pd.read_csv("../input/ashrae-energy-prediction/weather_train.csv", parse_dates=[\'timestamp\'], dtype=weather_dtype)\nmetadata = pd.read_csv("../input/ashrae-energy-prediction/building_metadata.csv", dtype=metadata_dtype)\ntrain = pd.read_csv("../input/ashrae-energy-prediction/train.csv", parse_dates=[\'timestamp\'], dtype=train_dtype)\n\nprint(\'Size of train_df data\', train.shape)\nprint(\'Size of weather_train_df data\', weather_train.shape)\nprint(\'Size of building_meta_df data\', metadata.shape)')


# Improve data readability

# In[ ]:


train['meter'].replace({0:"Electricity",1:"ChilledWater",2:"Steam",3:"HotWater"},inplace=True)


# ## Add missing measurements to weather

# There are some missing measurements alltogether as well. For example 2016.12.31 17:00. I simply interpolate between previous and next measurement. There are few days which have almost no weather data (2016.01.05 for example) and this will at the moment be left as is.

# In[ ]:


def add_missing_weather_times(df):
    first = df['timestamp'].iloc[0]
    last = df['timestamp'].iloc[-1]
    
    for site in df['site_id'].unique():
        site_data = df[df['site_id'] == site].sort_values('timestamp')
        site_timestamps = list(site_data['timestamp'])
        site_num = len(site_timestamps)
    
        i = 0
        while True:
            time = first + timedelta(hours=i)
            if time not in site_timestamps:
                dic = {'site_id': site, 'timestamp': time}
                    
                # Add new rows with NAs, because these will be taken care of later
                for col in ['air_temperature', 'cloud_coverage', 'dew_temperature', 'precip_depth_1_hr', 'sea_level_pressure', 'wind_direction', 'wind_speed']:
                        dic[col] = np.nan

                df.loc[df.index[-1] + 1] = dic

            if time == last:
                break

            i += 1

        del site_data, site_timestamps, site_num
        gc.collect()
                
    df.sort_values(['site_id', 'timestamp'], inplace=True)
    df.reset_index(inplace=True, drop=True)


# In[ ]:


print(len(weather_train))
add_missing_weather_times(weather_train)
print(len(weather_train))


# ## Engineer new features I
# 
# Day, Month, Hour, Weekend

# In[ ]:


def create_date_features(df):
    df['Month'] = df['timestamp'].dt.month.astype("uint8")
    df['DayOfMonth'] = df['timestamp'].dt.day.astype("uint8")
    df['DayOfWeek'] = df['timestamp'].dt.dayofweek.astype("uint8")
    df['Hour'] = df['timestamp'].dt.hour.astype("uint8")
    df['Weekend'] = ((df['DayOfWeek'] == 6) | (df['DayOfWeek'] == 5)).astype('uint8')


# In[ ]:


create_date_features(train)
create_date_features(weather_train) # I'll also add these features to weather, which should help imputer


# In[ ]:


weather_train.drop(['Weekend', 'DayOfWeek', 'DayOfMonth', 'precip_depth_1_hr'], axis=1, inplace=True)
weather_train


# ## Deal with NaNs

# If there is single NaN in weather data, it seems reasonable to linearly interpolate between previous and next measurement.

# In[ ]:


def replace_single_weather_nans(df):
    for column in ['air_temperature', 'cloud_coverage', 'dew_temperature', 'sea_level_pressure', 'wind_speed']:
        nan_index = df.index[df[column].isnull()]
        
        for i in range(0, len(nan_index)):
            index = nan_index[i]
            if index in [0, len(df)]:
                continue
            if  np.isfinite(df[column][index - 1]) and np.isfinite(df[column][index + 1]):
                if df['site_id'][index-1] == df['site_id'][index] == df['site_id'][index + 1]:
                    df[column][index] = (df[column][index-1] + df[column][index+1])/2


# In[ ]:


print(sum(weather_train.isna().sum()))
replace_single_weather_nans(weather_train)
print(sum(weather_train.isna().sum()))


# For other nan-s let's use sklearn's IterativeImputer with BayesianRidge estimator, to predict likely values for other nan-s.

# In[ ]:


imputer = IterativeImputer()
imputer.fit(weather_train.drop('timestamp', axis=1))


# In[ ]:


def replace_other_weather_nans(df):
    col_names = list(df.columns)
    col_names.remove('timestamp')
    # Must remove timestamp, since it doesn't work with imputer
    weather_temp = pd.DataFrame(imputer.transform(df[col_names]), columns=col_names)
    weather_temp.insert(1, 'timestamp', df['timestamp']) # Reinsert timestamps

    return weather_temp.drop(['Month', 'Hour'], axis=1)


# In[ ]:


weather_train = replace_other_weather_nans(weather_train)


# ## Map wind direction
# 

# In[ ]:


def map_wind_direction(df):
    N_idx = (0 < df['wind_direction']) & ((315 < df['wind_direction']) | (df['wind_direction'] <= 45))
    E_idx = (df['wind_direction'] > 45) & (df['wind_direction'] <= 135)
    S_idx = (df['wind_direction'] > 135) & (df['wind_direction'] <= 225)
    W_idx = (df['wind_direction'] > 225) & (df['wind_direction'] <= 315)
    
    df['wind_direction'][N_idx] = 1
    df['wind_direction'][E_idx] = 2
    df['wind_direction'][S_idx] = 3
    df['wind_direction'][W_idx] = 4
    
    df['wind_direction'].astype('uint8')


# In[ ]:


map_wind_direction(weather_train)


# ## Drop features

# Drop some columns based on EDA

# In[ ]:


# Dropping floor_count variable as it has 75% missing values
metadata.drop('floor_count',axis=1,inplace=True)
metadata.drop('year_built',axis=1,inplace=True)


# Convert target to log scale

# In[ ]:


train['meter_reading'] = np.log1p(train['meter_reading'])


# Preprocess metadata 
# 

# In[ ]:


metadata['primary_use'].replace({"Healthcare":"Other","Parking":"Other","Warehouse/storage":"Other","Manufacturing/industrial":"Other",
                                "Retail":"Other","Services":"Other","Technology/science":"Other","Food sales and service":"Other",
                                "Utility":"Other","Religious worship":"Other"},inplace=True)
metadata['square_feet'] = np.log1p(metadata['square_feet'])
metadata['square_feet'] = metadata['square_feet'].astype('float16') #Save space


#metadata['year_built'].fillna(-999, inplace=True)
#metadata['year_built'] = metadata['year_built'].astype('int16')


# ## Merge data

# In[ ]:


train = pd.merge(train,metadata,on='building_id',how='left')
print ("Training Data+Metadata Shape {}".format(train.shape))
gc.collect()


# In[ ]:


train = pd.merge(train,weather_train,on=['site_id','timestamp'],how='left')
print ("Training Data+Metadata+Weather Shape {}".format(train.shape))
gc.collect()


# In[ ]:


del weather_train
gc.collect()


# ## Drop some training data

# In[ ]:


# Drop nonsense entries
# As per the discussion in the following thread, https://www.kaggle.com/c/ashrae-energy-prediction/discussion/117083, there is some discrepancy in the meter_readings for different ste_id's and buildings. It makes sense to delete them
idx_to_drop = list((train[(train['site_id'] == 0) & (train['timestamp'] < "2016-05-21 00:00:00")]).index)
print (len(idx_to_drop))
train.drop(idx_to_drop,axis='rows',inplace=True)

# dropping all the electricity meter readings that are 0, after considering them as anomalies.
idx_to_drop = list(train[(train['meter'] == "Electricity") & (train['meter_reading'] == 0)].index)
print(len(idx_to_drop))
train.drop(idx_to_drop,axis='rows',inplace=True)

# Drop outliers from training data. Following https://www.kaggle.com/juanmah/ashrae-outliers
idx_to_drop = list(train[(train.building_id == 1099) | 
                         (train.building_id == 799) | 
                         (train.building_id == 1088) | 
                         (train.building_id == 778) | 
                         (train.building_id == 1168) | 
                         (train.building_id == 1021)].index)
print(len(idx_to_drop))
train.drop(idx_to_drop, axis='rows', inplace=True)


# ## Encode features

# In[ ]:


train.drop('timestamp',axis=1,inplace=True)

le = LabelEncoder()
train['meter']= le.fit_transform(train['meter']).astype("uint8")
train['primary_use']= le.fit_transform(train['primary_use']).astype("uint8")

print (train.shape)


# Drop correlated variables

# In[ ]:


get_ipython().run_cell_magic('time', '', '# Let\'s check the correlation between the variables and eliminate the one\'s that have high correlation\n# Threshold for removing correlated variables\nthreshold = 0.9\n\n# Absolute value correlation matrix\ncorr_matrix = train.corr().abs()\n# Upper triangle of correlations\nupper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))\n\n# Select columns with correlations above threshold\nto_drop = [column for column in upper.columns if any(upper[column] > threshold)]\n\ndel corr_matrix, upper\ngc.collect()\n\nprint(\'There are %d columns to remove.\' % (len(to_drop)))\nprint ("Following columns can be dropped {}".format(to_drop))\n\ndef drop_correlated_features(df):\n    df.drop(to_drop,axis=1,inplace=True)')


# In[ ]:


drop_correlated_features(train)


# In[ ]:


get_ipython().run_cell_magic('time', '', "y = train['meter_reading']\ntrain.drop('meter_reading',axis=1,inplace=True)")


# In[ ]:


get_ipython().run_cell_magic('time', '', "x_trains = {meter: train[train['meter'] == meter] for meter in [0, 1, 2, 3]}\ny_trains = {meter: y[train['meter'] == meter] for meter in [0, 1, 2, 3]}")


# In[ ]:


del y, train
gc.collect()


# # Model
# 
# I'm going to build lightGBM based model with separate model for each meter type and using 10 fold ensamble for each, in order to reduce overfitting.

# In[ ]:


import lightgbm as lgb


# ## Prediction function

# In[ ]:


def predict(X, step=1000000):
    results = {}
    for meter in [0, 1, 2, 3]:
        x = X[X.meter == meter]
        predictions = None
        for model in models[meter]:
            preds = []
            for i in range(0, len(x), step):
                preds.extend(model.predict(x.iloc[i: min(i+step, len(x)), :], num_iteration=model.best_iteration))

            # Average results
            if predictions is None:
                predictions = np.array(preds)/(len(models[meter]))
            else:
                predictions += np.array(preds)/(len(models[meter]))
 
            print('... ', end ='')
        predictions = np.expm1(predictions) # Back to kWh
        print()
        
        # Create DFs
        results[meter] = pd.DataFrame(x.index, columns=['row_id'])
        results[meter]['meter_reading'] = predictions
        results[meter]['meter_reading'].clip(lower=0,upper=None,inplace=True)
        
        del preds, predictions, x
        gc.collect()
        
    # Merge results
    result = pd.concat([*results.values()])
    result.sort_values('row_id', inplace=True)
    
    return result


# In[ ]:


common_params = {'objective': 'regression',
                'boosting_type': 'gbdt',
                'bagging_seed': 11,
                'metric': 'rmse',
                'verbosity': -1,
                'random_state': 47}

params = {0: {'feature_fraction': 0.75,
          'bagging_fraction': 0.8,
          'num_leaves': 300,
          'max_depth': 15,
          'learning_rate': 0.14,
          'min_child_weight': 10,
          'min_split_gain': 0.005,
          'reg_alpha': 12.5,
          'reg_lambda': 7.5,
          **common_params
         },
         1: {'feature_fraction': 0.725,
          'bagging_fraction': 0.75,
          'num_leaves': 250, 
          'max_depth': 20,
          'learning_rate': 0.17,
          'min_child_weight': 1,
          'min_split_gain': 0.005,
          'reg_alpha': 3.,
          'reg_lambda': 15.,
          **common_params
         },
         2: {'feature_fraction': 0.75,
          'bagging_fraction': 0.825,
          'num_leaves': 300,
          'max_depth': 25,
          'learning_rate': 0.17,
          'min_child_weight': 15,
          'min_split_gain': 0.005,
          'reg_alpha': 3.,
          'reg_lambda': 5.,
          **common_params
         },
         3: {'feature_fraction': 0.75,
          'bagging_fraction': 0.750,
          'num_leaves': 300,
          'max_depth': 15,
          'learning_rate': 0.16,
          'min_child_weight': 15,
          'min_split_gain': 0.01,
          'reg_alpha': 1.,
          'reg_lambda': 3.,
          **common_params
         }}


# ## KFold model

# In[ ]:


get_ipython().run_cell_magic('time', '', "categorical_cols = ['building_id','Month','meter','Hour','Weekend','primary_use','DayOfWeek','DayOfMonth', 'wind_direction']\n\nmodels = {0: [], 1: [], 2:[], 3:[]}\nfor meter in [0, 1, 2, 3]:\n    X = x_trains[meter]\n    y = y_trains[meter]\n    \n    X_np = np.array(X)\n    y_np = np.array(y)\n    \n    strats = np.array(pd.cut(y, 50, labels=list(range(50))))\n    \n    kf = StratifiedKFold(n_splits=10, random_state=200)\n    for train_i, test_i in kf.split(X_np, strats):\n        X_train_kf, X_test_kf = X.iloc[train_i], X.iloc[test_i]\n        y_train_kf, y_test_kf = y.iloc[train_i], y.iloc[test_i]\n\n        lgb_train = lgb.Dataset(X_train_kf, y_train_kf, categorical_feature=categorical_cols)\n        lgb_test = lgb.Dataset(X_test_kf, y_test_kf, categorical_feature=categorical_cols)\n\n        reg = lgb.train(params[meter], lgb_train, num_boost_round=500, valid_sets=[lgb_train, lgb_test], \n                    early_stopping_rounds=50, verbose_eval=500)\n        \n        print()\n        del X_train_kf, X_test_kf, y_train_kf, y_test_kf, lgb_train, lgb_test\n        gc.collect()\n    \n        models[meter].append(reg)\n    \n    del X, y, X_np\n    gc.collect()\n    \n    print('\\n------------------------\\n')")


# # Final predictions

# ## Read and modify test data

# In[ ]:


del x_trains, y_trains


# In[ ]:


test = pd.read_csv("../input/ashrae-energy-prediction/test.csv", parse_dates=['timestamp'], usecols=['building_id','meter','timestamp'], dtype=train_dtype)
weather_test = pd.read_csv("../input/ashrae-energy-prediction/weather_test.csv", parse_dates=['timestamp'], dtype=weather_dtype)

test['meter'].replace({0:"Electricity",1:"ChilledWater",2:"Steam",3:"HotWater"},inplace=True)


# In[ ]:


add_missing_weather_times(weather_test)
create_date_features(test)
create_date_features(weather_test)
weather_test.drop(['Weekend', 'DayOfWeek', 'DayOfMonth', 'precip_depth_1_hr'], axis=1, inplace=True)
replace_single_weather_nans(weather_test)
weather_test = replace_other_weather_nans(weather_test)
map_wind_direction(weather_test)


# In[ ]:


get_ipython().run_cell_magic('time', '', '# Merge data\ntest = pd.merge(test,metadata,on=\'building_id\',how=\'left\')\nprint ("Training Data+Metadata Shape {}".format(test.shape))\ngc.collect()\ntest = pd.merge(test,weather_test,on=[\'site_id\',\'timestamp\'],how=\'left\')\nprint ("Training Data+Metadata+Weather Shape {}".format(test.shape))\ngc.collect()')


# In[ ]:


del metadata, weather_test
gc.collect()


# In[ ]:


test.drop('timestamp',axis=1,inplace=True)
test['meter']= le.fit_transform(test['meter']).astype("uint8")
test['primary_use']= le.fit_transform(test['primary_use']).astype("uint8")


# In[ ]:


drop_correlated_features(test)


# In[ ]:


gc.collect()


# ## Predict

# In[ ]:


get_ipython().run_cell_magic('time', '', 'predictions = predict(test)')


# In[ ]:


predictions.to_csv("TiimTiim_submission_10.csv",index=None)


# In[ ]:




