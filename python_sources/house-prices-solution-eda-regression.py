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
import warnings
warnings.filterwarnings("ignore")
# Any results you write to the current directory are saved as output.


# In[ ]:


train=pd.read_csv("/kaggle/input/house-prices-advanced-regression-techniques/train.csv")
train.head()


# In[ ]:


#remove outliers
train=train.drop(index=[523,1298],axis=0)


# In[ ]:


test=pd.read_csv("/kaggle/input/house-prices-advanced-regression-techniques/test.csv")
test.head()


# In[ ]:


print('the train data has {} rows and {} features'.format(train.shape[0],train.shape[1]))
print('the test data has {} rows and {} features'.format(test.shape[0],test.shape[1]))


# We'll combine these two data sets using the concat attribute

# In[ ]:


data=pd.concat([train.iloc[:,:-1],test],axis=0)
print('the data has {} rows and {} features'.format(data.shape[0],data.shape[1]))


# In[ ]:


data.info()


# We'll divide the data into numerical and categorical data and verify their descriptive statistics

# In[ ]:


num_features=data.select_dtypes(include=['int64','float64'])
categorical_features=data.select_dtypes(include='object')


# In[ ]:


num_features.describe()


# In[ ]:


categorical_features.describe()


# In[ ]:


data.isnull().sum().sort_values(ascending=False)[:34]


# In[ ]:


data = data.drop(columns=['Id','Street','PoolQC','Utilities'],axis=1)


# In[ ]:


data['LotFrontage'] = data.groupby('Neighborhood')['LotFrontage'].transform(lambda x: x.fillna(x.median()))


# In[ ]:


data['LotFrontage'].isnull().sum()


# In[ ]:


#create a new class 'other'
features=['Electrical','KitchenQual','SaleType','Exterior2nd','Exterior1st','Alley','Fence', 'MiscFeature','FireplaceQu','GarageCond','GarageQual','GarageFinish','GarageType','BsmtCond','BsmtExposure','BsmtQual','BsmtFinType2','BsmtFinType1','MasVnrType']
for name in features:
    data[name].fillna('Other',inplace=True)


# In[ ]:


data[features].isnull().sum()


# In[ ]:


data['MSZoning'] = data.groupby('MSSubClass')['MSZoning'].transform(lambda x: x.fillna(x.mode()[0]))


# In[ ]:


data['Functional']=data['Functional'].fillna('typ')


# In[ ]:


zero=['GarageArea','GarageYrBlt','MasVnrArea','BsmtHalfBath','BsmtHalfBath','BsmtFullBath','BsmtFinSF1','BsmtFinSF2','BsmtUnfSF','TotalBsmtSF','GarageCars']
for name in zero:
    data[name].fillna(0,inplace=True)


# In[ ]:


data.isnull().sum()


# Our dataset has no missing values.
# 
# Another pre-processing step is to transform categorical features into numerical features

# In[ ]:


data.loc[data['MSSubClass']==60, 'MSSubClass']=0
data.loc[(data['MSSubClass']==20)|(data['MSSubClass']==120), 'MSSubClass']=1
data.loc[data['MSSubClass']==75, 'MSSubClass']=2
data.loc[(data['MSSubClass']==40)|(data['MSSubClass']==70)|(data['MSSubClass']==80), 'MSSubClass']=3
data.loc[(data['MSSubClass']==50)|(data['MSSubClass']==85)|(data['MSSubClass']==90)|(data['MSSubClass']==160)|(data['MSSubClass']==190), 'MSSubClass']=4
data.loc[(data['MSSubClass']==30)|(data['MSSubClass']==45)|(data['MSSubClass']==180), 'MSSubClass']=5
data.loc[(data['MSSubClass']==150), 'MSSubClass']=6


# In[ ]:


object_features = data.select_dtypes(include='object').columns
object_features


# In[ ]:


def dummies(d):
    dummies_df=pd.DataFrame()
    object_features = d.select_dtypes(include='object').columns
    for name in object_features:
        dummies = pd.get_dummies(d[name], drop_first=False)
        dummies = dummies.add_prefix("{}_".format(name))
        dummies_df=pd.concat([dummies_df,dummies],axis=1)
    return dummies_df


# In[ ]:


dummies_data=dummies(data)
dummies_data.shape


# In[ ]:


data=data.drop(columns=object_features,axis=1)
data.columns


# In[ ]:


final_data=pd.concat([data,dummies_data],axis=1)
final_data.shape


# In[ ]:


#Re-spliting the data into train and test datasets
train_data=final_data.iloc[:1458,:]
test_data=final_data.iloc[1458:,:]
print(train_data.shape)
test_data.shape


# In[ ]:


# X: independent variables and y: target variable
X=train_data
y=train.loc[:,'SalePrice']


# In[ ]:


from sklearn.linear_model import Ridge, RidgeCV, LassoCV, ElasticNet


# In[ ]:


model_las_cv = LassoCV(alphas=(0.0001, 0.0005, 0.001, 0.01, 0.05, 0.1, 0.3, 1, 3, 5, 10))
model_las_cv.fit(X,y)
las_cv_preds=model_las_cv.predict(test_data)


# In[ ]:


model_ridge_cv = RidgeCV(alphas=(0.01, 0.05, 0.1, 0.3, 1, 3, 5, 10))
model_ridge_cv.fit(X, y)
ridge_cv_preds=model_ridge_cv.predict(test_data)


# In[ ]:


model_ridge = Ridge(alpha=10, solver='auto')
model_ridge.fit(X, y)
ridge_preds=model_ridge.predict(test_data)


# In[ ]:


model_en = ElasticNet(random_state=1, alpha=0.00065, max_iter=3000)
model_en.fit(X, y)
en_preds=model_en.predict(test_data)


# In[ ]:


import xgboost as xgb


# In[ ]:


model_xgb = xgb.XGBRegressor(learning_rate=0.01,n_estimators=3460,
                                     max_depth=3, min_child_weight=0,
                                     gamma=0, subsample=0.7,
                                     colsample_bytree=0.7,
                                     objective='reg:linear', nthread=-1,
                                     scale_pos_weight=1, seed=27,
                                     reg_alpha=0.00006)
model_xgb.fit(X, y)
xgb_preds=model_xgb.predict(test_data)


# In[ ]:


from sklearn.ensemble import GradientBoostingRegressor


# In[ ]:


model_gbr = GradientBoostingRegressor(n_estimators=3000, 
                                learning_rate=0.05, 
                                max_depth=4, 
                                max_features='sqrt', 
                                min_samples_leaf=15, 
                                min_samples_split=10, 
                                loss='huber', 
                                random_state =42)
model_gbr.fit(X, y)
gbr_preds=model_gbr.predict(test_data)


# In[ ]:


from lightgbm import LGBMRegressor


# In[ ]:


model_lgbm = LGBMRegressor(objective='regression', 
                                       num_leaves=4,
                                       learning_rate=0.01, 
                                       n_estimators=5000,
                                       max_bin=200, 
                                       bagging_fraction=0.75,
                                       bagging_freq=5, 
                                       bagging_seed=7,
                                       feature_fraction=0.2,
                                       feature_fraction_seed=7,
                                       verbose=-1,
                                       #min_data_in_leaf=2,
                                       #min_sum_hessian_in_leaf=11
                                       )
model_lgbm.fit(X, y)
lgbm_preds=model_lgbm.predict(test_data)


# In[ ]:


final_predictions = 0.3 * lgbm_preds + 0.3 * gbr_preds + 0.1 * xgb_preds + 0.3 * ridge_cv_preds


# In[ ]:


#display the first 5 predictions of sale price
final_predictions[:5]


# In[ ]:


#make the submission data frame
submission = {
    'Id': test.Id.values,
    'SalePrice': final_predictions + 0.007 * final_predictions
}
solution = pd.DataFrame(submission)
solution.head()


# In[ ]:


#make the submission file
solution.to_csv('submission.csv',index=False)


# In[ ]:




