#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import make_scorer, mean_squared_error
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBRegressor
from sklearn.ensemble import VotingRegressor

pd.set_option('display.max_columns', 5000)
pd.set_option('display.max_row', 500)
np.random.seed(51)


# In[ ]:


train = pd.read_csv('/kaggle/input/house-prices-advanced-regression-techniques/train.csv')
test = pd.read_csv('/kaggle/input/house-prices-advanced-regression-techniques/test.csv')

y_train = train['SalePrice']
X_train = train.drop(['Id','SalePrice'], axis=1)
X_test = test.drop(['Id'], axis=1)
print(X_train.shape, y_train.shape)


# In[ ]:


X_train.head()


# In[ ]:


X_train_corr = X_train.corrwith(y_train)
X_train_corr.sort_values(ascending=False).head(10)


# In[ ]:


plt.scatter(X_train['GrLivArea'], y_train)


# In[ ]:


outliers = X_train.loc[(X_train['GrLivArea']>4000.0) & (y_train<300000.0)].index
print(outliers)

X_train = X_train.drop(outliers)
y_train = y_train.drop(outliers)


# In[ ]:


train_samples = X_train.shape[0]
X = pd.concat((X_train, X_test), sort=False).reset_index(drop=True)


# From EDA we know that MSsubclass is categorical even if the values are integers

# In[ ]:


X['MSSubClass'] = X['MSSubClass'].astype('object')


# In[ ]:


X.isna().sum().sort_values(ascending=False).head(40)


# In[ ]:


fake_nans_cols = ['Alley', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'FireplaceQu', 
         'GarageType', 'GarageFinish', 'GarageQual', 'GarageCond', 'PoolQC', 'Fence', 'MiscFeature']
X[fake_nans_cols] = X[fake_nans_cols].fillna('None')


# In[ ]:


X['Utilities'].value_counts()


# In[ ]:


X = X.drop(['Utilities'], axis=1)


# In[ ]:


numerical = (X.dtypes != 'object')
categorical = (X.dtypes == 'object')


# Some columns have nans which mean instead that the there is none of the values. Imputing with mode doesn't make sense.

# In[ ]:


X.isna().sum().sort_values(ascending=False).head(10)


# In[ ]:


imputer = SimpleImputer(missing_values=np.nan)
X.loc[:, numerical] = imputer.fit_transform(X.loc[:, numerical])


# In[ ]:


imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
X.loc[:, categorical] = imputer.fit_transform(X.loc[:, categorical])


# In[ ]:


X.isna().sum().sort_values(ascending=False).head(10)


# In[ ]:


ord_encoder=OrdinalEncoder()
X.loc[:, categorical] = ord_encoder.fit_transform(X.loc[:, categorical])


# In[ ]:


sns.distplot(X['LotArea'])


# In[ ]:


X.loc[:, numerical].skew().sort_values(ascending=False).head(25)


# In[ ]:


skewed = X.loc[:, numerical].skew() > 10
X.loc[:, numerical & skewed] = np.log1p(X.loc[:, numerical & skewed])


# In[ ]:


sns.distplot(X['LotArea'])


# In[ ]:


X['TotalSF'] = X['TotalBsmtSF'] + X['1stFlrSF'] + X['2ndFlrSF']


# In[ ]:


numerical = (X.dtypes != 'object')
categorical = (X.dtypes == 'object')


# In[ ]:


X_train = X[:train_samples]
X_test  = X[train_samples:]
X_train.shape


# In[ ]:


cols = X_train.columns

scaler= RobustScaler()
X_train = np.hstack([X_train.loc[:, categorical], scaler.fit_transform(X_train.loc[:, numerical])])
X_test = np.hstack([X_test.loc[:, categorical], scaler.transform(X_test.loc[:, numerical])])

X_train = pd.DataFrame(X_train, columns=cols)
X_test = pd.DataFrame(X_test, columns=cols)
X_train


# In[ ]:


y_train = np.log1p(y_train)


# In[ ]:


lr = LinearRegression(fit_intercept=False)
MSEs=cross_val_score(lr, X_train, y_train, scoring='neg_mean_squared_error', cv=5)
meanMSE=np.mean(MSEs)
print('RMSE = '+str(np.sqrt(-meanMSE)))


# In[ ]:


lr = LinearRegression(fit_intercept=False)
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)
pd.DataFrame({'Id': test.Id, 'SalePrice': np.exp(y_pred)}).to_csv('lr_full_2019-11-20.csv', index =False)


# In[ ]:


xgb= XGBRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
             colsample_bynode=1, colsample_bytree=0.5, gamma=0,
             importance_type='gain', learning_rate=0.01, max_delta_step=0,
             max_depth=3, min_child_weight=0, missing=None, n_estimators=4000,
             n_jobs=1, nthread=None, objective='reg:squarederror', random_state=0,
             reg_alpha=0.0001, reg_lambda=0.01, scale_pos_weight=1, seed=None,
             silent=None, subsample=1, verbosity=1)
MSEs=cross_val_score(xgb, X_train, y_train, scoring='neg_mean_squared_error', cv=5)
meanMSE=np.mean(MSEs)
print('RMSE = '+str(np.sqrt(-meanMSE)))


# In[ ]:


vote_reg = VotingRegressor([('Linear', lr), ('XGBRegressor', xgb)])
MSEs=cross_val_score(vote_reg, X_train, y_train, scoring='neg_mean_squared_error', cv=5)
meanMSE=np.mean(MSEs)
print('RMSE = '+str(np.sqrt(-meanMSE)))


# In[ ]:


vote_reg = VotingRegressor([('Linear', lr), ('XGBRegressor', xgb)])
vote_reg.fit(X_train, y_train)
y_pred = vote_reg.predict(X_test)
pd.DataFrame({'Id': test.Id, 'SalePrice': np.exp(y_pred)}).to_csv('vote_reg_2019-11-21.csv', index =False)

