#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from learntools.core import *

iowa_file_path = '../input/train.csv'
iowa_test_file_path = '../input/test.csv'
train_data = pd.read_csv(iowa_file_path)
test_data = pd.read_csv(iowa_test_file_path)

y = train_data.SalePrice
train_features = train_data.drop(['Id', 'SalePrice'], axis = 1)
test_data_no_id = test_data.drop(['Id'], axis = 1)


# # Missing and categorical values

# In[ ]:


# fill in missing numeric values
from sklearn.impute import SimpleImputer

# impute
train_data_num = train_features.select_dtypes(exclude=['object'])
test_data_num = test_data_no_id.select_dtypes(exclude=['object'])
imputer = SimpleImputer()
train_num_cleaned = imputer.fit_transform(train_data_num)
test_num_cleaned = imputer.transform(test_data_num)

# columns rename after imputing
train_num_cleaned = pd.DataFrame(train_num_cleaned)
test_num_cleaned = pd.DataFrame(test_num_cleaned)
train_num_cleaned.columns = train_data_num.columns
test_num_cleaned.columns = test_data_num.columns


# In[ ]:


# string columns: transform to dummies
train_data_str = train_data.select_dtypes(include=['object'])
test_data_str = test_data_no_id.select_dtypes(include=['object'])
train_str_dummy = pd.get_dummies(train_data_str)
test_str_dummy = pd.get_dummies(test_data_str)
train_dummy, test_dummy = train_str_dummy.align(test_str_dummy, 
                                                join = 'left', 
                                                axis = 1)


# In[ ]:


# convert numpy dummy tables to pandas DataFrame
train_num_cleaned = pd.DataFrame(train_num_cleaned)
test_num_cleaned = pd.DataFrame(test_num_cleaned)


# In[ ]:


# joining numeric (after imputing) and string (converted to dummy) data
train_all_clean = pd.concat([train_num_cleaned, train_dummy], axis = 1)
test_all_clean = pd.concat([test_num_cleaned, test_dummy], axis = 1)


# In[ ]:


# detect NaN in already cleaned test data 
# (there could be completely empty columns in test data)
cols_with_missing = [col for col in test_all_clean.columns
                                if test_all_clean[col].isnull().any()]
for col in cols_with_missing:
    print(col, test_all_clean[col].isnull().any())


# In[ ]:


# since there are empty columns in test we need to drop them in train and test data
train_all_clean_no_nan = train_all_clean.drop(cols_with_missing, axis = 1)
test_all_clean_no_nan = test_all_clean.drop(cols_with_missing, axis = 1)


# # XGBoost training and validation

# In[ ]:


train_X, val_X, train_y, val_y = train_test_split(train_all_clean_no_nan, y, random_state=1)

# default XGBoost
xgb_model = XGBRegressor(random_state = 1)
xgb_model.fit(train_X, train_y, verbose = False)
xgb_predictions = xgb_model.predict(val_X)
xgb_mae = mean_absolute_error(val_y, xgb_predictions)
print("XGBoost MAE default: {:,.0f}".format(xgb_mae))

# fine tuned XGBoost
xgb_model = XGBRegressor(n_estimators = 1000, learning_rate=0.05, random_state = 1)
xgb_model.fit(train_X, train_y, early_stopping_rounds = 25, eval_set = [(val_X, val_y)], verbose = False)
# with verbose = True we have the best iteration on step 757 => n_estimators = 757


# In[ ]:


xgb_predictions = xgb_model.predict(val_X)
xgb_mae = mean_absolute_error(val_y, xgb_predictions)
print("XGBoost MAE default: {:,.0f}".format(xgb_mae))


# # XGBoost Model (on all training data)

# In[ ]:


# To improve accuracy, create a new Random Forest model which you will train on all training data
xgb_model_on_full_data = xgb_model = XGBRegressor(n_estimators = 757, learning_rate=0.05)
xgb_model_on_full_data.fit(train_all_clean_no_nan, y)


# # Partial dependencies plots

# In[ ]:


from xgboost import plot_importance

plot_importance(xgb_model_on_full_data, max_num_features = 20)


# # Make Predictions

# In[ ]:


test_X = test_all_clean_no_nan
test_preds = xgb_model_on_full_data.predict(test_X)


# In[ ]:


output = pd.DataFrame({'Id': test_data.Id,
                       'SalePrice': test_preds})
output.to_csv('submission.csv', index=False)

