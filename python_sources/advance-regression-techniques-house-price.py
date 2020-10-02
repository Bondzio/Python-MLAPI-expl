#!/usr/bin/env python
# coding: utf-8

# # Problem Statement:
# We have given several parameter which may affect the Price of house. A regression model has to build which can predict the price of house with a least error. 

# # Steps to build the model.
# These are the steps that you will see in this particular notebook required to build a regression model:
# 1. Import the required libraries.
# 2. Analyse the data and remove Outliers.
# 3. Check the distribution of the target variable (make the distribution normal if it is not normal).
# 4. Handle missing values.
# 5. Handle features which contains year values.
# 6. Drop features with high correlation (Use Heatmap).
# 7. Convert categorical features into Dummy Variables.
# 8. Train the model.
# 9. Make Prediction of Prices of House

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


# ### Import Libraries

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
from scipy import stats
from scipy.stats import norm, skew
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import r2_score


# ### Import Train and Test data

# In[ ]:


train = pd.read_csv('/kaggle/input/house-prices-advanced-regression-techniques/train.csv')
test = pd.read_csv('/kaggle/input/house-prices-advanced-regression-techniques/test.csv')


# In[ ]:


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


# In[ ]:


train.head()


# In[ ]:


# Save the Id 
train_id = train['Id']
test_id = test['Id']


# # Data Processing
# ### Analyse the Data and remove Outliers

# In[ ]:


sns.jointplot(x='LotFrontage', y='SalePrice', data=train, kind='reg', )
plt.grid(True)


# In[ ]:


train = train.drop(train[(train['LotFrontage']>250) & (train['SalePrice']<400000)].index)
sns.jointplot(x='LotFrontage', y='SalePrice', data=train, kind='reg', )
plt.grid(True)


# In[ ]:


sns.jointplot(x='LotArea', y='SalePrice', data=train, kind='reg' )


# In[ ]:


train = train.drop(train[(train['LotArea']>150000) & (train['SalePrice']<300000)].index)
sns.jointplot(x='LotArea', y='SalePrice', data=train, kind='reg' )
plt.grid(True)


# In[ ]:


sns.jointplot(x='BsmtFinSF1', y='SalePrice', data=train, kind='reg', )
plt.grid(True)


# In[ ]:


train = train.drop(train[(train['BsmtFinSF1']>1000) & (train['SalePrice']>600000)].index)
sns.jointplot(x='BsmtFinSF1', y='SalePrice', data=train, kind='reg')
plt.grid(True)


# In[ ]:


sns.jointplot(x='WoodDeckSF', y='SalePrice', data=train, kind='reg')
plt.grid(True)


# In[ ]:


train = train.drop(train[(train['WoodDeckSF']>0) & (train['SalePrice']>500000)].index)
sns.jointplot(x='WoodDeckSF', y='SalePrice', data=train, kind='reg')
plt.grid(True)


# In[ ]:


sns.jointplot(x='OpenPorchSF', y='SalePrice', data=train, kind='reg')
plt.grid(True)


# In[ ]:


train = train.drop(train[((train['OpenPorchSF']>500) & (train['SalePrice']<300000)) | ((train['OpenPorchSF']<100) 
              & (train['SalePrice']>500000))].index)
sns.jointplot(x='OpenPorchSF', y='SalePrice', data=train, kind='reg')
plt.grid(True)


# ### Check the distribusion of Prices

# In[ ]:


sns.distplot(train['SalePrice'], fit=norm)
# Get the fitted parameters used by the function
(mu, sigma) = norm.fit(train['SalePrice'])

print('\n mean is {:.2f} and sigma is {:.2f} \n'.format(mu, sigma))

plt.legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(mu, sigma)],
            loc='best')
plt.ylabel('Frequency')
plt.title('SalePrice distribution')


# ### Make the Distribution Normal

# In[ ]:


train['SalePrice'] = np.log1p(train['SalePrice'])

sns.distplot(train['SalePrice'], fit=norm)
# Get the fitted parameters used by the function
(mu, sigma) = norm.fit(train['SalePrice'])

print('\n mean is {:.2f} and sigma is {:.2f} \n'.format(mu, sigma))

plt.legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(mu, sigma)],
            loc='best')
plt.ylabel('Frequency')
plt.title('SalePrice distribution')


# # Feature Engineering

# In[ ]:


# Set 'Id' as Index for the Sake if Simplicity
train = train.set_index('Id')
test = test.set_index('Id')


# In[ ]:


train_num = train.shape[0]
test_num = test.shape[0]


# In[ ]:


df = pd.concat([train, test], axis=0)
df.head()


# ### Transforming some Numerical Features into Categorical Featured

# In[ ]:


df['MSSubClass'] = df['MSSubClass'].astype('str')


# ### Let's check the missing values 

# In[ ]:


plt.figure(figsize=(10,6))
sns.heatmap(df.isnull())


# In[ ]:


df.isnull().sum()


# ### Dropping features with more than 50% Missing Values

# In[ ]:


df.drop(['Alley', 'PoolQC', 'Fence', 'MiscFeature'], axis=1, inplace=True)


# ### Separate Numerical and Categorical Features

# In[ ]:


num_feat = df.select_dtypes(exclude='object').columns
cat_feat = df.select_dtypes(include='object').columns
num_feat = num_feat[:-1]


# In[ ]:


num_feat


# ### Inputing Missing Values

# In[ ]:


# Input mean value in Numerical Features
for col in num_feat:
    df[col] = df[col].fillna(df[col].mean())
    
# Input mode value in Categorical Features
for col in cat_feat:
    df[col] = df[col].fillna(df[col].mode()[0])


# In[ ]:


# Handle Features contains year values

df['YrSold_YearBuilt'] = df['YrSold'] - df['YearBuilt']
df['GarageYrBlt'] = df['GarageYrBlt'].astype('str')
df['YearRemodAdd'] = df['YearRemodAdd'].astype('str')
df.drop(['YrSold', 'YearBuilt'], axis=1, inplace=True)


# In[ ]:


train = df.iloc[:train_num, :]
test = df.iloc[train_num:, :]


# ### Feature Correlation

# In[ ]:


# Plotting Heatmap 
corrmat = train.corr()
plt.figure(figsize=(10,6))
sns.heatmap(corrmat, vmin=0, vmax=1, cmap='coolwarm')


# ### Let's check features with high correlation only

# In[ ]:


#saleprice correlation matrix
k = 15 
cols = corrmat.nlargest(k, 'SalePrice')['SalePrice'].index
cf = np.corrcoef(train[cols].values.T)
sns.set(font_scale=1.25)
plt.figure(figsize=(16,10))
hm = sns.heatmap(cf, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values,
                 cmap='coolwarm', xticklabels=cols.values)


# ### Drop features with with correlation value (more than 0.65)

# In[ ]:


train.drop(['GrLivArea', '1stFlrSF', 'OverallQual', 'GarageCars'], axis=1, inplace=True)
test.drop(['GrLivArea', '1stFlrSF', 'OverallQual', 'GarageCars'], axis=1, inplace=True)


# In[ ]:


df = pd.concat([train, test], axis=0)
df.head()


# In[ ]:


cat_feat = df.select_dtypes(include='object').columns
cat_feat


# ### Convert Categorical features into Dummy Variables

# In[ ]:


df_dummy = pd.get_dummies(df, columns=cat_feat, drop_first=True)


# In[ ]:


# Separate train and test set
train = df_dummy.iloc[:train_num, :]
test = df_dummy.iloc[train_num:, :]
test.drop('SalePrice', axis=1, inplace=True)


# ## Train Model 1

# In[ ]:


X = train.drop('SalePrice', axis=1)
y = train['SalePrice']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=51)


# In[ ]:


model1 = xgb.XGBRegressor()
model1.fit(X_train, y_train)


# In[ ]:


xgb_pred = model1.predict(X_test)
r2_score(y_test, xgb_pred)


# 
# ## Model Parameters tuning with RandomizedSearchCV

# In[ ]:


# Input Parameter values: 

param = {'max_depth': [3,5,6,8],
        'learning_rate': [0.05, 0.1, 0.15, 0.25, 0.3],
        'n_estimators': [100,200,300,500],
        'gamma': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
        'min_child_weight': [1,3,5,7]}


# In[ ]:


# Instantiate model
regressor = xgb.XGBRegressor()
random_search = RandomizedSearchCV(regressor, param_distributions=param, n_iter =5, scoring = 'neg_mean_squared_error',
                                   n_jobs=-1, cv=5, verbose=2)


# In[ ]:


random_search.fit(X_train, y_train)


# ### Find out the best parameter values:

# In[ ]:


random_search.best_estimator_


# ### Fit these best estimators into the model

# In[ ]:


model2 = xgb.XGBRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
             colsample_bynode=1, colsample_bytree=1, gamma=0.1, gpu_id=-1,
             importance_type='gain', interaction_constraints='',
             learning_rate=0.05, max_delta_step=0, max_depth=3,
             min_child_weight=3, monotone_constraints='()',
             n_estimators=300, n_jobs=0, num_parallel_tree=1, random_state=0,
             reg_alpha=0, reg_lambda=1, scale_pos_weight=1, subsample=1,
             tree_method='exact', validate_parameters=1, verbosity=None)


# In[ ]:


model2.fit(X, y)


# ### Predict SalePrices

# In[ ]:


test_pred = model2.predict(test)
test_pred = np.expm1(test_pred)


# ### Convert into Dataframe for final submission

# In[ ]:


test_pred_df = pd.DataFrame(test_pred, columns=['SalePrice'])
test_id_df = pd.DataFrame(test_id, columns=['Id'])


# In[ ]:


submission = pd.concat([test_id_df, test_pred_df], axis=1)
submission.head()


# In[ ]:


# Save the predictions
submission.to_csv(r'submission.csv', index=False)


# # Now it's your turn
# # Give it a try :)

# ## Upvote this notebook if you like my work.
