#!/usr/bin/env python
# coding: utf-8

# **Machine Learning for beginners, by beginner (Regression problem)**
# * This code is self explanatory and comments are written wherever necessary to understand code.

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


# Step 1: Loading Data

# In[ ]:


import pandas as pd
#loading data
train_df = pd.read_csv('../input/house-prices-advanced-regression-techniques/train.csv')
test_df = pd.read_csv('../input/house-prices-advanced-regression-techniques/test.csv')


# In[ ]:


train_df.info()
test_df.info()


# **Missing Data**
# * There are ordinal variables in the missing data where "Nan" is equivalent to zero.
# * Categorical Data : to be filled with most frequent.
# * Numerical Data: to be filled with mean/median.
# 

# **Strategy to be used to fill missing data**
# * 'LotFrontage': missing data to be filled with mean/ median
# * Utilities(in test data): Categorical most frequent
# * Alley  : filled with zero          
# * 'MasVnrType':Categorical most frequent
# * 'MasVnrArea': mean or median
# * 'Electrical': categorical
# * FireplaceQu : zero
# * GarageType  : zero
# * GarageYrBlt : median or most frequent
# * GarageFinish,GarageQual,GarageQual, GarageCond, PoolQC, Fence,MiscFeature: zero 
# * GarageQual   : zero
# * GarageCond   : zero  
# * PoolQC       : zero
# * Fence        : zero
# * MiscFeature  : zero
# **test data**
# * MSZoning     : Categorical most frequent
# * Exterior1st  : categorical   
# * Exterior2nd  : categorical 
# * MasVnrType   : categorical
# * MasVnrArea   : mean / meadian 
# * BsmtQual     : zero   
# * BsmtCond     : zero
# * BsmtExposure : zero
# * BsmtFinType1 : zero
# * BsmtFinSF1   :zero
# * BsmtFinType2 :zero
# * BsmtFinSF2   : zero
# * BsmtUnfSF    : mean or median  
# * TotalBsmtSF  : zero
# * BsmtFullBath : zero
# * BsmtHalfBath : zero
# * KitchenQual  : categorical
# * Functional   : categorical  
# * GarageArea   : zero     
# * GarageCars   : zero

# In[ ]:


#Dealing with the data to be filled with zero
cols_to_fill_zero = ['Alley','FireplaceQu','GarageType','GarageFinish',
                     'GarageQual','GarageCond','PoolQC' ,'Fence','MiscFeature',
                    'GarageFinish','GarageQual','GarageQual', 'GarageCond', 'PoolQC',
                     'Fence','MiscFeature','MasVnrArea','BsmtQual' ,'BsmtCond','BsmtExposure',
                     'BsmtFinType1','BsmtFinSF2' ,'TotalBsmtSF','BsmtFullBath','BsmtHalfBath',
                     'GarageArea','GarageCars']
train_df[cols_to_fill_zero] =  train_df[cols_to_fill_zero].fillna(0, inplace = True)
test_df[cols_to_fill_zero] = train_df[cols_to_fill_zero].fillna(0, inplace = True)


# In[ ]:


#fill missing data with mean/ median
cols_to_fill_mean = ['LotFrontage','GarageYrBlt','BsmtUnfSF']

train_df['LotFrontage'] = train_df['LotFrontage'].fillna(train_df['LotFrontage'].dropna().mean())
test_df['LotFrontage'] = test_df['LotFrontage'].fillna(train_df['LotFrontage'].dropna().mean())

train_df['GarageYrBlt'] = train_df['GarageYrBlt'].fillna(train_df['GarageYrBlt'].dropna().median())
test_df['GarageYrBlt'] = test_df['GarageYrBlt'].fillna(train_df['GarageYrBlt'].dropna().median())


train_df['BsmtUnfSF'] = train_df['BsmtUnfSF'].fillna(train_df['BsmtUnfSF'].dropna().mean())
test_df['BsmtUnfSF'] = test_df['BsmtUnfSF'].fillna(train_df['BsmtUnfSF'].dropna().mean())


# In[ ]:


train_df.isnull().sum()


# In[ ]:


#filling categorical data with most_frequent occurings
categorical_missing_cols = ['MasVnrType', 'BsmtFinType2', 'Electrical','MSZoning','Utilities',
                            'Exterior1st','Exterior2nd','MasVnrType','BsmtFinSF1','BsmtFinType2',
                            'KitchenQual','Functional','SaleType']


for col in categorical_missing_cols:
    most_frequent = train_df[col].dropna().value_counts().idxmax()
    train_df[col] = train_df[col].fillna(most_frequent)
    test_df[col] = train_df[col].fillna(most_frequent)



# In[ ]:


#dummy code to print the null values in training data
train_cols_with_null = []

for col in train_df.columns:
    if train_df[col].isnull().sum()>0:
        train_cols_with_null.append(col)

train_cols_with_null


# In[ ]:


#dummy code to print the columns with null values
test_cols_with_null = []

for col in test_df.columns:
    if test_df[col].isnull().sum()>0:
        test_cols_with_null.append(col)

test_cols_with_null


# Dealt with missing data.
# It's time to deal with **categorical** data.
# 
# We have some ordinal and nominal data
# 
# We will one hot encode nominal data nd level encode ordinal data.

# In[ ]:


#setting the dependent and independent variables
train_X =train_df.drop(['SalePrice'],axis=1)
test_X = test_df
y = train_df[['SalePrice']]


# In[ ]:


#storing object cols in a list
object_cols = train_X.select_dtypes(include=['object']).columns
len(object_cols)


# Columns to be one hot encoded:
# * ['MSZoning', 'Street', 'Alley','Utilities','LotConfig','Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl', 'MasVnrType', 'Foundation',  'Heating','CentralAir', 'Electrical','Functional', 'PavedDrive','SaleType','SaleCondition']
# 
# 
# 

# In[ ]:


#cols to one hot encode
nominal_vars= ['MSZoning', 'Street', 'Alley','Utilities','LotConfig'
                     ,'Condition1', 'Condition2', 'BldgType', 'HouseStyle'
                     , 'RoofStyle', 'RoofMatl', 'MasVnrType', 'Foundation'
                     ,  'Heating','CentralAir', 'Electrical','Functional'
                     , 'PavedDrive','SaleType','SaleCondition']

len(nominal_vars)


# In[ ]:


#columns to label encode
ordinal_vars = []
for col in object_cols:
    
    if col not in nominal_vars:
        ordinal_vars.append(col)
        
len(ordinal_vars)


# Note the columns "Neighbourhood', "Exterior1st", "Exterior2nd" are nominal variables but are label encoded since they have high number of unique values which would highly increase the column size (threshold usually preferred is 15 unique values)

# In[ ]:


#label encoding to all the categorical columns
#to-do: OneHotEncode nominal variables
from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()
label_encoded_train_X = train_X.copy()
label_encoded_test_X = test_X.copy()

for col in ordinal_vars:
    label_encoded_train_X[col] = pd.DataFrame(label_encoder.fit_transform(train_X[col]))
    label_encoded_test_X[col] = pd.DataFrame(label_encoder.transform(test_X[col]))


# In[ ]:


#replacing the object columns of data with label encoded data
train_X[ordinal_vars] = label_encoded_train_X[ordinal_vars]
test_X[ordinal_vars] = label_encoded_train_X[ordinal_vars]


# In[ ]:


train_X.shape
y.shape
test_X.shape


# In[ ]:


#one hot encoding
from sklearn.preprocessing import OneHotEncoder

OH_encoder = OneHotEncoder()

OH_encoded_train_X = pd.DataFrame(OH_encoder
                                  .fit_transform(train_X[nominal_vars])
                                  .toarray())
OH_encoded_test_X = pd.DataFrame(OH_encoder
                                 .transform(test_X[nominal_vars])
                                 .toarray())


# In[ ]:


#drop nominal variables, replace them with OH_encoded variables
train_X = train_X.drop(nominal_vars,axis = 1)
final_train_X = pd.concat([train_X,OH_encoded_train_X],axis = 1)

test_X = test_X.drop(nominal_vars,axis = 1)
final_test_X = pd.concat([test_X,OH_encoded_test_X],axis = 1)


# In[ ]:


train_X.isnull().sum()
test_X.info()


# In[ ]:


#splitting the training and validation data
from sklearn.model_selection import train_test_split

X_train, X_valid, y_train, y_valid = train_test_split(final_train_X, y,
                                                    train_size = 0.8,
                                                    test_size = 0.2, 
                                                    random_state = 0)


# In[ ]:


y_train.shape


# *Perfect. Now we are ready to test out models for predictions.*

# In[ ]:


from sklearn.tree import DecisionTreeRegressor

dt_model = DecisionTreeRegressor(random_state=0,max_leaf_nodes= 50)
dt_model.fit(X_train,y_train)
dt_predictions = dt_model.predict(X_valid)


# In[ ]:


#mean absolute error of the dt model
from sklearn.metrics import mean_absolute_error
dt_mae_score = mean_absolute_error(dt_predictions,y_valid)
print(dt_mae_score)


# In[ ]:


#function to fine tune RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor

def rf_score(n_estimators):
    rf_model = RandomForestRegressor(random_state=1
                                     ,n_estimators=n_estimators
                                     ,max_leaf_nodes=430)
    rf_model.fit(X_train,y_train.values.ravel())
    rf_predictions = rf_model.predict(X_valid)
    rf_mae_score = mean_absolute_error(rf_predictions,y_valid)
    
    return rf_mae_score


#calling the function iteratively for different values

n_estimators_value = [260,270,280,290,300,310,320,330,340]

# max_leaf_nodes_value = [360,370,380,390,400,410,420,430,440,450]

rf_score_list = []
for value in n_estimators_value:
    rf_score_list.append(rf_score(value))

print(rf_score_list)


# In[ ]:


#randomForestClassifier
from sklearn.ensemble import RandomForestRegressor
rf_model = RandomForestRegressor(random_state=1,n_estimators=300,max_leaf_nodes=380)
rf_model.fit(X_train,y_train.values.ravel())
rf_predictions = rf_model.predict(X_valid)


# In[ ]:


#mae score of random forest model
from sklearn.metrics import mean_absolute_error
rf_mae_score = mean_absolute_error(rf_predictions,y_valid)
print(rf_mae_score)


# In[ ]:


#XGboost
from xgboost import XGBRegressor
xgb_model = XGBRegressor(n_estimators = 5000
                         ,learning_rate = 0.1
                         ,n_jobs = 4)
xgb_model.fit(X_train, y_train.values.ravel()
              ,early_stopping_rounds = 5
              ,eval_set = [(X_valid, y_valid)]
              ,verbose= False)

xgb_predictions = xgb_model.predict(X_valid)


# In[ ]:


#mae_score of xgboost model
from sklearn.metrics import mean_absolute_error
xgb_mae_score = mean_absolute_error(xgb_predictions,y_valid)
print(xgb_mae_score)


# Alright, let's try submitting the output

# In[ ]:


#submission
xgb_model.fit(final_train_X,y.values.ravel())
xgb_predictions = xgb_model.predict(final_test_X)
ids = test_df['Id']
output = pd.DataFrame({'Id': ids,
                       'SalePrice': xgb_predictions})
output.to_csv('hr_submission_xgb_1.csv', index=False)

