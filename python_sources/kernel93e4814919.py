#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


train_data = pd.read_csv('../input/train.csv')
print(train_data.shape)
train_data.head()


# In[ ]:


sns.boxplot(train_data.GrLivArea)


# In[ ]:


train_data = train_data[train_data.GrLivArea < 4000]


# In[ ]:


train_data.shape


# In[ ]:


sns.scatterplot(train_data.LotArea,train_data.SalePrice)


# In[ ]:


sns.boxplot(train_data.LotArea)


# In[ ]:


train_data = train_data[train_data.LotArea <= 50000]
print(train_data.shape)


# In[ ]:


sns.scatterplot(train_data.TotalBsmtSF,train_data.SalePrice)


# In[ ]:


sns.boxplot(train_data.TotalBsmtSF)


# In[ ]:


train_data = train_data[train_data.TotalBsmtSF <= 2500]
print(train_data.shape)


# In[ ]:


sns.scatterplot(train_data.LotFrontage,train_data.SalePrice)


# In[ ]:


print(train_data.shape)


# In[ ]:


train_data.head()


# In[ ]:


test_data = pd.read_csv('../input/test.csv')
test_data.head()


# In[ ]:


_id = test_data['Id'].values


# In[ ]:


target = train_data['SalePrice'].values
train_data = train_data.drop('SalePrice',1)


# In[ ]:


print(train_data.shape)
print(test_data.shape)


# In[ ]:


train_data.columns


# In[ ]:


test_data.columns


# In[ ]:


total_data = pd.concat([train_data,test_data],0)


# In[ ]:


total_data.shape


# In[ ]:


total_data.head()


# In[ ]:


total_data.Id = total_data.Id.values.astype('int')


# In[ ]:


total_data.head()


# In[ ]:


# total_data.MSSubClass = total_data.MSSubClass.fillna(0)
# total_data.MSZoning = total_data.MSZoning.fillna('None')
# total_data.LotFrontage = total_data.LotFrontage.fillna(list(total_data.LotFrontage.median())[0])
# total_data.LotArea = total_data.LotArea.fillna(list(total_data.LotArea.median())[0])
# total_data.Street = total_data.Street.fillna('None')
# total_data.Alley = total_data.Alley.fillna("None")
# total_data.LotShape = total_data.LotShape.fillna('None')
# total_data.LandContour = total_data.LandContour.fillna('None')
# total_data.Utilities = total_data.Utilities.fillna('None')


# In[ ]:


cat_var = ['MSZoning', 'Street', 'Alley', 'LotShape', 'LandContour', 'Utilities',
       'LotConfig', 'LandSlope', 'Neighborhood', 'Condition1', 'Condition2',
       'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl', 'Exterior1st',
       'Exterior2nd', 'MasVnrType', 'ExterQual', 'ExterCond', 'Foundation',
       'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2',
       'Heating', 'HeatingQC', 'CentralAir', 'Electrical', 'KitchenQual',
       'Functional', 'FireplaceQu', 'GarageType', 'GarageFinish', 'GarageQual',
       'GarageCond', 'PavedDrive', 'PoolQC', 'Fence', 'MiscFeature',
       'SaleType', 'SaleCondition','YearBuilt','YearRemodAdd','GarageYrBlt','YrSold']


# In[ ]:


for i in cat_var:
    total_data[i] = total_data[i].fillna('None')


# In[ ]:


total_data.MSSubClass = total_data.MSSubClass.fillna(0)
total_data.OverallQual = total_data.OverallQual.fillna(0)
total_data.OverallCond = total_data.OverallCond.fillna(0)


# In[ ]:


num_var = ['LotFrontage', 'LotArea','MasVnrArea','BsmtFinSF1',
       'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF','1stFlrSF', '2ndFlrSF', 'LowQualFinSF',
       'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath', 'HalfBath',
       'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd','Fireplaces',
       'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch',
       'ScreenPorch', 'PoolArea', 'MiscVal',
       'MoSold']


# In[ ]:


for i in num_var:
    print(i)
    total_data[i] = total_data[i].fillna(total_data[i].median())


# In[ ]:


total_data.head()


# In[ ]:


total_data.shape


# In[ ]:


cat_features = total_data.drop(['MSSubClass', 'LotFrontage', 'LotArea',
       'OverallQual', 'OverallCond','MasVnrArea','BsmtFinSF1',
       'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF','1stFlrSF', '2ndFlrSF', 'LowQualFinSF',
       'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath', 'HalfBath',
       'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd','Fireplaces',
       'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch',
       'ScreenPorch', 'PoolArea', 'MiscVal',
       'MoSold'],1)


# In[ ]:


cat_features.head()


# In[ ]:


num_features = total_data[['MSSubClass', 'LotFrontage', 'LotArea',
       'OverallQual', 'OverallCond','MasVnrArea','BsmtFinSF1',
       'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF','1stFlrSF', '2ndFlrSF', 'LowQualFinSF',
       'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath', 'HalfBath',
       'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd','Fireplaces',
       'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch',
       'ScreenPorch', 'PoolArea', 'MiscVal',
       'MoSold']]


# In[ ]:


print(cat_features.shape)
print(num_features.shape)


# In[ ]:


cat_features.head()


# In[ ]:


num_features.head()


# In[ ]:


date_features = cat_features[['YearBuilt','YearRemodAdd','GarageYrBlt','YrSold']]
cat_features = cat_features.drop(['YearBuilt','YearRemodAdd','GarageYrBlt','YrSold'],1)


# In[ ]:


date_features = pd.get_dummies(date_features, columns=['YearBuilt','YearRemodAdd','GarageYrBlt','YrSold'])
date_features.head()


# In[ ]:


cat_features.columns


# In[ ]:


cat_features = pd.get_dummies(cat_features, columns=['MSZoning', 'Street', 'Alley', 'LotShape', 'LandContour', 'Utilities',
       'LotConfig', 'LandSlope', 'Neighborhood', 'Condition1', 'Condition2',
       'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl', 'Exterior1st',
       'Exterior2nd', 'MasVnrType', 'ExterQual', 'ExterCond', 'Foundation',
       'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2',
       'Heating', 'HeatingQC', 'CentralAir', 'Electrical', 'KitchenQual',
       'Functional', 'FireplaceQu', 'GarageType', 'GarageFinish', 'GarageQual',
       'GarageCond', 'PavedDrive', 'PoolQC', 'Fence', 'MiscFeature',
       'SaleType', 'SaleCondition'])
cat_features.head()


# In[ ]:


print(date_features.shape)
print(cat_features.shape)


# In[ ]:


from sklearn.preprocessing import MinMaxScaler
scalar_var = MinMaxScaler()


# In[ ]:


num_features = scalar_var.fit_transform(num_features)
print(num_features.shape)


# In[ ]:


num_features = pd.DataFrame(num_features)
num_features.head()


# In[ ]:


temp = pd.concat([cat_features,date_features],1)


# In[ ]:


print(temp.shape)
temp.head()


# In[ ]:


print(num_features.shape)
num_features.head()


# In[ ]:


np_temp = temp.values
np_num = num_features.values
print(np_temp.shape)
print(np_num.shape)


# In[ ]:


final_data = np.concatenate((np_temp,np_num),axis=1)


# In[ ]:


final_data = pd.DataFrame(final_data)


# In[ ]:


final_data.head()


# In[ ]:


final_data[final_data.columns[0]] = final_data[final_data.columns[0]].values.astype('int')


# In[ ]:


final_data.head()


# In[ ]:


final_data.shape


# In[ ]:


X_train = final_data.iloc[:1441]
X_test = final_data[1441:]
print(X_train.shape)
print(X_test.shape)


# In[ ]:


X_test.head()


# In[ ]:


X_train = X_train.drop(X_train.columns[0],1)
X_test = X_test.drop(X_test.columns[0],1)


# In[ ]:


X_train.shape


# In[ ]:


target = target.reshape(-1,1)


# In[ ]:


import xgboost as xgb


# In[ ]:


# reg_xgb = xgb.XGBRegressor(colsample_bytree=0.4603, gamma=0.0468, 
#                              learning_rate=0.05, max_depth=3, 
#                              min_child_weight=1.7817, n_estimators=2200,
#                              reg_alpha=0.4640, reg_lambda=0.8571,
#                              subsample=0.5213, silent=1,
#                              random_state =7, nthread = -1)


# In[ ]:


# reg.fit(X_train,target)


# In[ ]:


import lightgbm as lgb
reg_lgb = lgb.LGBMRegressor(objective='regression',num_leaves=5,
                              learning_rate=0.05, n_estimators=720,
                              max_bin = 55, bagging_fraction = 0.8,
                              bagging_freq = 5, feature_fraction = 0.2319,
                              feature_fraction_seed=9, bagging_seed=9,
                              min_data_in_leaf =6, min_sum_hessian_in_leaf = 11)


# In[ ]:


target = pd.DataFrame(target.reshape(-1,1))


# In[ ]:


target.head()


# In[ ]:


reg_lgb.fit(X_train,target)


# In[ ]:


# from sklearn.ensemble import GradientBoostingRegressor, ExtraTreesRegressor
# reg_gb = GradientBoostingRegressor(n_estimators=3000, learning_rate=0.05,
#                                    max_depth=4, max_features='sqrt',
#                                    min_samples_leaf=15, min_samples_split=10, 
#                                    loss='huber', random_state =5)


# In[ ]:


# reg_ext = ExtraTreesRegressor(n_estimators=3000)


# In[ ]:


# from mlxtend.regressor import StackingRegressor


# In[ ]:


# stregr = StackingRegressor(regressors=[reg_xgb, reg_lgb, reg_gb], 
#                            meta_regressor=reg_ext)


# In[ ]:


# stregr.fit(X_train,target)
# reg_ext.fit(X_train, target)


# In[ ]:


# pred = stregr.predict(X_test)
pred = reg_lgb.predict(X_test)


# In[ ]:


pred = pred.reshape(-1,1)
print(pred.shape)


# In[ ]:


test_data.head()


# In[ ]:


_id = test_data.Id.values.reshape(-1,1)


# In[ ]:


_id.shape


# In[ ]:


type(_id[0])


# In[ ]:


output = np.array(np.concatenate((_id, pred), 1))


# In[ ]:


output = pd.DataFrame(output,columns = ["Id","SalePrice"])


# In[ ]:


output.head()


# In[ ]:


output.Id = output.Id.astype('Int64')


# In[ ]:


output.head()


# In[ ]:


output.to_csv('submission.csv',index = False)


# In[ ]:




