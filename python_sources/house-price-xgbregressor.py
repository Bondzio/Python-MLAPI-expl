#!/usr/bin/env python
# coding: utf-8

# Importing libraries:

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import seaborn as sns
import os


# In[ ]:


test_data = pd.read_csv('../input/test.csv')
train_data = pd.read_csv('../input//train.csv')

# sizes of each doc
print(test_data.shape)
print(train_data.shape)


# In[ ]:


train_data.head()


# In[ ]:


df_train = pd.DataFrame(train_data)
df_test = pd.DataFrame(test_data)


# In[ ]:


df_train.describe(include='all')


# Checking all the count of NaN per each column:

# In[ ]:


cols_missed_train = df_train.isnull().sum()
cols_missed_valid = df_test.isnull().sum()

print('Columns with NaN in df_train: ', len(cols_missed_train[cols_missed_train > 0]))
print(cols_missed_train[cols_missed_train > 0].sort_values(ascending = False))

print('Columns with NaN in df_test: ', len(cols_missed_valid[cols_missed_valid > 0]))
print(cols_missed_valid[cols_missed_valid > 0].sort_values(ascending = False))


# In[ ]:


# Getting rid of all the NaNs
df_train['PoolQC'] = df_train['PoolQC'].fillna('None')
df_train['MiscFeature'] = df_train['MiscFeature'].fillna('None')
df_train['Alley'] = df_train['Alley'].fillna('None')
df_train['Fence'] = df_train['Fence'].fillna('None')
df_train['FireplaceQu'] = df_train['FireplaceQu'].fillna('None')
df_train['LotFrontage'] = df_train['LotFrontage'].fillna(df_train['LotFrontage'].mode()[0])
for col in ('GarageYrBlt', 'GarageCars', 'GarageArea'):
	df_train[col] = df_train['GarageYrBlt'].fillna(0)
for col in ('GarageType', 'GarageQual', 'GarageCond', 'GarageFinish'):
	df_train[col] = df_train[col].fillna('None')
for col in ('BsmtFinType2', 'BsmtFinType1', 'BsmtExposure', 'BsmtCond', 'BsmtQual'):
	df_train[col] = df_train[col].fillna('None')
df_train['MasVnrArea'] = df_train['MasVnrArea'].fillna(df_train['MasVnrArea'].mode()[0])
df_train['MasVnrType'] = df_train['MasVnrType'].fillna('None')
df_train['Electrical'] = df_train['Electrical'].fillna('None')
df_train['MSZoning'] = df_train['MSZoning'].fillna(df_train['MSZoning'].mode()[0])

df_train['Functional'] = df_train['Functional'].fillna(df_train['Functional'].mode()[0])
for col in ('BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF','TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath'):
    df_train[col] = df_train[col].fillna(0)
df_train['SaleType'] = df_train['SaleType'].fillna(df_train['SaleType'].mode()[0])
df_train['Utilities'] = df_train['Utilities'].fillna(df_train['Utilities'].mode()[0])
df_train['Exterior1st'] = df_train['Exterior1st'].fillna(df_train['Exterior1st'].mode()[0])
df_train['Exterior2nd'] = df_train['Exterior2nd'].fillna(df_train['Exterior2nd'].mode()[0])
df_train['KitchenQual'] = df_train['KitchenQual'].fillna(df_train['KitchenQual'].mode()[0])

# Checking nulls to be sure they are gone in df_train
print('Missed data in df_train: ', df_train.isnull().sum().sum())


# Replacing missing data in df_test
df_test['PoolQC'] = df_test['PoolQC'].fillna('None')
df_test['MiscFeature'] = df_test['MiscFeature'].fillna('None')
df_test['Alley'] = df_test['Alley'].fillna('None')
df_test['Fence'] = df_test['Fence'].fillna('None')
df_test['FireplaceQu'] = df_test['FireplaceQu'].fillna('None')
df_test['LotFrontage'] = df_test['LotFrontage'].fillna(df_test['LotFrontage'].mode()[0])
for col in ('GarageYrBlt', 'GarageCars', 'GarageArea'):
	df_test[col] = df_test['GarageYrBlt'].fillna(0)
for col in ('GarageType', 'GarageQual', 'GarageCond', 'GarageFinish'):
	df_test[col] = df_test[col].fillna('None')
for col in ('BsmtFinType2', 'BsmtFinType1', 'BsmtExposure', 'BsmtCond', 'BsmtQual'):
	df_test[col] = df_test[col].fillna('None')
df_test['MasVnrArea'] = df_test['MasVnrArea'].fillna(df_test['MasVnrArea'].mode()[0])
df_test['MasVnrType'] = df_test['MasVnrType'].fillna('None')
df_test['Electrical'] = df_test['Electrical'].fillna('None')
df_test['MSZoning'] = df_test['MSZoning'].fillna(df_test['MSZoning'].mode()[0])
df_test['Functional'] = df_test['Functional'].fillna(df_test['Functional'].mode()[0])
for col in ('BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF','TotalBsmtSF', 'BsmtFullBath', 'BsmtHalfBath'):
    df_test[col] = df_test[col].fillna(0)
df_test['SaleType'] = df_test['SaleType'].fillna(df_test['SaleType'].mode()[0])
df_test['Utilities'] = df_test['Utilities'].fillna(df_test['Utilities'].mode()[0])
df_test['Exterior1st'] = df_test['Exterior1st'].fillna(df_test['Exterior1st'].mode()[0])
df_test['Exterior2nd'] = df_test['Exterior2nd'].fillna(df_test['Exterior2nd'].mode()[0])
df_test['KitchenQual'] = df_test['KitchenQual'].fillna(df_test['KitchenQual'].mode()[0])

# Checking nulls to be sure they are gone in df_train
print('Missed data in df_test: ', df_test.isnull().sum().sum())


# In[ ]:


df_train.dtypes.value_counts()


# In[ ]:


# We need to copy df_train_full and df_test_full in case something will go wrong

df_train_full = df_train.copy()
df_test_full = df_test.copy()


# In[ ]:


#Excluding object types of data to be able to get some information from histograms
train_num = df_train_full.select_dtypes(exclude = ['object'])
test_num = df_test_full.select_dtypes(exclude = ['object'])


# In[ ]:


# Histogram for SalePrice
train_num['SalePrice'].hist(color='purple')
plt.title('SalePrice distribution 1')


# In[ ]:


sns.distplot(train_num['SalePrice'], color='DarkOrange')
plt.title('SalePrice distribution 2')


# In[ ]:


# Let's take logarithm for more comfortable understandin our data
np.log(train_num['SalePrice']).hist(bins=50, density=1, color='DarkCyan')
plt.title('SalePrice distribution 3')
# As we can see we have outliers. We will get rid of them a bit later


# In[ ]:


# Histogram of SalePrice depending on MSZoning (normalized)
df_train_full.groupby('MSZoning')['SalePrice'].plot.hist(density=1, alpha=0.6)
plt.title('Distribution by MSZoning 1')
plt.legend()


# But it is not that informative, so we need something else:

# In[ ]:


# MSZoning
var = 'MSZoning'
data = pd.concat([df_train_full['SalePrice'], df_train_full[var]], axis=1)
fig = sns.boxplot(x=var, y="SalePrice", data=data)
fig.axis(ymin=0, ymax=700000);


# In[ ]:


# YearBuilt boxplot
var = 'YearBuilt'
data = pd.concat([df_train_full['SalePrice'], df_train_full[var]], axis=1)
f, ax = plt.subplots(figsize=(26, 12))
fig = sns.boxplot(x=var, y="SalePrice", data=data)
fig.axis(ymin=0, ymax=1000000);


# In[ ]:


#Removing outliers (choosing data between first and third quartiles)
first_q = df_train_full['SalePrice'].describe()['25%']
third_q = df_train_full['SalePrice'].describe()['75%']
diff = third_q - first_q

cols_train = df_train_full[(df_train_full['SalePrice'] > (first_q - 3 * diff))&
                     (df_train_full['SalePrice'] < (third_q + 3 * diff))]
print('Removed outliers: ' + str(len(df_train_full) - len(cols_train)))


# In[ ]:


cols_train.head()


# In[ ]:


test_id = df_test['Id']


# In[ ]:


# Removing IDs (to get more accurate outputs)
cols_train.drop(columns=['Id'], axis=1, inplace=True)
df_test_full.drop(columns=['Id'], axis=1, inplace=True)


# In[ ]:


# Building correlation matrix for understanding how the characteristics influence to each other
n_df = cols_train.copy()
corr_matrix = n_df.corr()

#Mask and cmap
mask = np.zeros_like(corr_matrix, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
colormap = sns.diverging_palette(220, 10, as_cmap=True)

f, ax = plt.subplots(figsize=(16, 12))
plt.title('Correlation Matrix',fontsize=22)
sns.heatmap(corr_matrix, mask=mask, square=True, cmap=colormap, vmax=1, center=0, annot=True, fmt='.1f')


# In[ ]:


cols_train['SalePrice'] = np.log(cols_train['SalePrice'])


# In[ ]:


cols_train['SalePrice'].head()


# In[ ]:


SalePrice = cols_train['SalePrice']


# In[ ]:


new_cols_train = cols_train.drop('SalePrice', axis=1)
new_cols_train.head()


# In[ ]:


y = SalePrice
X = new_cols_train

# Split dataset to train and valid for training and testing
train_X, valid_X, train_y, valid_y = train_test_split(X, y, random_state=1)

print(train_X.shape)
print(valid_X.shape)


# In[ ]:


s = (train_X.dtypes == 'object')
categor_cols = list(s[s].index)

label_train_X = train_X.copy()
label_valid_X = valid_X.copy()

OHE = OneHotEncoder(handle_unknown='ignore', sparse=False)
OHE_train_X = pd.DataFrame(OHE.fit_transform(label_train_X[categor_cols]))
OHE_valid_X = pd.DataFrame(OHE.transform(label_valid_X[categor_cols]))

OHE_train_X.index = label_train_X.index
OHE_valid_X.index = label_valid_X.index

num_train_X = label_train_X.drop(categor_cols, axis=1)
num_valid_X = label_valid_X.drop(categor_cols, axis=1)

OHE_train = pd.concat([num_train_X, OHE_train_X], axis=1)
OHE_valid = pd.concat([num_valid_X, OHE_valid_X], axis=1)


# In[ ]:


xgb = XGBRegressor(n_estimator=500, learning_rate=0.1, n_jobs=4)
xgb.fit(OHE_train, train_y,
        early_stopping_rounds=5,
        eval_set=[(OHE_valid, valid_y)],
        verbose=False)

val_pred = xgb.predict(OHE_valid)

rmse = np.sqrt(mean_squared_error(valid_y, val_pred))
rmse


# In[ ]:


u = (df_test_full.dtypes == 'object')
categor_cols_test = list(u[u].index)
categor_cols_test

OHE_test = pd.DataFrame(OHE.transform(df_test_full[categor_cols_test]))
OHE_test.index = df_test_full.index
num_test = df_test_full.drop(categor_cols_test, axis=1)

OHE_test_final = pd.concat([num_test, OHE_test], axis=1)


# In[ ]:


final_pred = xgb.predict(OHE_test_final)
final_pred = np.exp(final_pred)


# In[ ]:


df_pred = pd.DataFrame({"id":test_id, "SalePrice":final_pred})
df_pred.SalePrice = df_pred.SalePrice.round(0)
df_pred.to_csv('submission.csv', sep=',', encoding='utf-8', index=False)


# In[ ]:


df_pred.head()

