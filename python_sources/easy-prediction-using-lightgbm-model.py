#!/usr/bin/env python
# coding: utf-8

# # **SalePrice prediction :**

# Some basic setup :

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm, skew #for some statistics

# importing alll the necessary packages to use the various classification algorithms
from sklearn.linear_model import LogisticRegression  # for Logistic Regression algorithm
from sklearn.model_selection import train_test_split #to split the dataset for training and testing
from sklearn.neighbors import KNeighborsClassifier  # for K nearest neighbours
from sklearn import svm  #for Support Vector Machine (SVM) Algorithm
from sklearn import metrics #for checking the model accuracy
from sklearn.metrics import mean_squared_error #for checking the model accuracy
from sklearn.tree import DecisionTreeClassifier #for using Decision Tree Algoithm
from sklearn.linear_model import ElasticNet, Lasso,  BayesianRidge, LassoLarsIC
from sklearn.ensemble import RandomForestRegressor,  GradientBoostingRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin, clone
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import lightgbm as lgb


# Input data :

# In[ ]:


train_data = pd.read_csv("../input/train.csv")
test_data = pd.read_csv("../input/test.csv")
train_data.head(5)


# **Remove Outliers :**

# I picked some of the features that seem to be most affected to the salePrice,
# and then plot the pictures:

# In[ ]:


fig, axarr = plt.subplots(2, 2, figsize = (12, 8))
train_data.plot.scatter(
    x="GrLivArea", 
    y="SalePrice", 
    ax=axarr[0][0]
)
train_data.plot.scatter(
    x="BsmtFinSF1", 
    y="SalePrice", 
    ax=axarr[0][1]
)
train_data.plot.scatter(
    x="LotArea", 
    y="SalePrice", 
    ax=axarr[1][0]
)
train_data.plot.scatter(
    x="GarageArea", 
    y="SalePrice", 
    ax=axarr[1][1]
)


# As we can see, some of the data is terribly strange, thus I remove them.
# But sometimes it'll be worse if we done this too much, like 'yearBuilt', I thought the two dots at the top would be outliers, but it turns out that removing them just makes the result worse.

# In[ ]:


# drop outliers
train_data = train_data.drop(train_data[(train_data['GrLivArea']>4000) & (train_data['SalePrice']<300000)].index)
# train_data = train_data.drop(train_data[(train_data['BsmtFinSF1']>3000)].index)
train_data = train_data.drop(train_data[(train_data['LotArea']>150000)].index)
train_data = train_data.drop(train_data[(train_data['GarageArea']>1200) & (train_data['SalePrice']<300000)].index)
fig, axarr = plt.subplots(2, 2, figsize = (12, 8))
train_data.plot.scatter(
    x="GrLivArea", 
    y="SalePrice", 
    ax=axarr[0][0]
)
train_data.plot.scatter(
    x="BsmtFinSF1", 
    y="SalePrice", 
    ax=axarr[0][1]
)
train_data.plot.scatter(
    x="LotArea", 
    y="SalePrice", 
    ax=axarr[1][0]
)
train_data.plot.scatter(
    x="GarageArea", 
    y="SalePrice", 
    ax=axarr[1][1]
)


# saleprice :

# In[ ]:


sns.distplot(train_data['SalePrice']);


# Apply **Log transfomation** to SalePrice:

# By simply adding a log transformation, my place in competition jumed almost 2000 forward!

# In[ ]:


train_data['SalePrice'] = np.log1p(train_data['SalePrice'])
sns.distplot(train_data['SalePrice']);


# Now let's concat train data and test data, and save a copy of SalePrice and Id :

# In[ ]:


# data preprocessing
Id = test_data['Id']
train_y = train_data.SalePrice.values
# print(train_y)
all_data = pd.concat((train_data, test_data), sort=False).reset_index(drop=True)
all_data.drop(['SalePrice'], axis=1, inplace=True)
print("all_data size is : {}".format(all_data.shape))
all_data.head(5)


# **Handling missing value :**

# 1. drop columns that missing percent is too high or unnecessary :

# In[ ]:


# drop id
all_data = all_data.drop('Id', axis=1)

# drop NAN that missing ratio is above a certain threshold
missing_data = all_data.isnull().sum()
missing_data = missing_data.drop(missing_data[missing_data == 0].index)
missing_ratio = missing_data / len(all_data) * 100
# print(missing_ratio)
all_data = all_data.drop(missing_ratio[missing_ratio.values > 20].index, axis=1)
# all_data = all_data.drop(missing_data[missing_data.iloc[:] > 0].index, axis=1)
all_data.head(5)


# 2. deal with the rest of the missing value :

# In[ ]:


missing_data = all_data.isnull().sum()
missing_data = missing_data.drop(missing_data[missing_data == 0].index)
missing_ratio = missing_data / len(all_data) * 100
print(missing_ratio)
all_data[missing_ratio.index].head(5)


# In[ ]:


# LotFrontage has more missing value, thus we consider it more delicately
all_data["LotFrontage"] = all_data.groupby("Neighborhood")["LotFrontage"].transform(lambda x: x.fillna(x.median()))

# These features are useless, drop them
all_data['Utilities'] = all_data['Utilities'].fillna(all_data['Utilities'].mode()[0])

# These features, we just fill them with common case
all_data['MSZoning'] = all_data['MSZoning'].fillna(all_data['MSZoning'].mode()[0])
all_data['Utilities'] = all_data['Utilities'].fillna(all_data['Utilities'].mode()[0])
all_data['Exterior1st'] = all_data['Exterior1st'].fillna(all_data['Exterior1st'].mode()[0])
all_data['Exterior2nd'] = all_data['Exterior2nd'].fillna(all_data['Exterior2nd'].mode()[0])
all_data['MasVnrType'] = all_data['MasVnrType'].fillna(all_data['MasVnrType'].mode()[0])
all_data['Electrical'] = all_data['Electrical'].fillna(all_data['Electrical'].mode()[0])
all_data['KitchenQual'] = all_data['KitchenQual'].fillna(all_data['KitchenQual'].mode()[0])
all_data['Functional'] = all_data['Functional'].fillna(all_data['Functional'].mode()[0])
all_data['SaleType'] = all_data['SaleType'].fillna(all_data['SaleType'].mode()[0])

#in these features, NAN means none
all_data['BsmtQual'] = all_data['BsmtQual'].fillna('None')
all_data['BsmtCond'] = all_data['BsmtCond'].fillna('None')
all_data['BsmtExposure'] = all_data['BsmtExposure'].fillna('None')
all_data['BsmtFinType1'] = all_data['BsmtFinType1'].fillna('None')
all_data['BsmtFinType2'] = all_data['BsmtFinType2'].fillna('None')
all_data['GarageType'] = all_data['GarageType'].fillna('None')
all_data['GarageFinish'] = all_data['GarageFinish'].fillna('None')
all_data['GarageQual'] = all_data['GarageQual'].fillna('None')
all_data['GarageCond'] = all_data['GarageCond'].fillna('None')

#in these features, NAN means 0
all_data['BsmtFinSF1'] = all_data['BsmtFinSF1'].fillna(0)
all_data['BsmtFinSF2'] = all_data['BsmtFinSF2'].fillna(0)
all_data['BsmtUnfSF'] = all_data['BsmtUnfSF'].fillna(0)
all_data['TotalBsmtSF'] = all_data['TotalBsmtSF'].fillna(0)
all_data['BsmtFullBath'] = all_data['BsmtFullBath'].fillna(0)
all_data['BsmtHalfBath'] = all_data['BsmtHalfBath'].fillna(0)
all_data['MasVnrArea'] = all_data['MasVnrArea'].fillna(0)
all_data['GarageYrBlt'] = all_data['GarageYrBlt'].fillna(0)
all_data['GarageCars'] = all_data['GarageCars'].fillna(0)
all_data['GarageArea'] = all_data['GarageArea'].fillna(0)

# all_data = all_data.drop(missing_ratio[missing_ratio.values > 0].index, axis=1)
# missing_data = all_data.isnull().sum()
# missing_data = missing_data.drop(missing_data[missing_data == 0].index)
# missing_ratio = missing_data / len(all_data) * 100
# print(missing_ratio)
# all_data[missing_ratio.index].head(5)


# At my first attempt, I dropped all the columns that contain missing value. That's one way.
# The next attemt I tried to simply fill them with either some common value, or 0, or None. That's improves my placement in competition by another 1000! 

# In[ ]:


all_data = pd.get_dummies(all_data)
all_data.head(5)


# **Split to train and test data :**

# In[ ]:


ntrain = train_data.shape[0]
ntest = test_data.shape[0]
# train, test = train_test_split(all_data, test_size=0.4998)
train = all_data[:ntrain]
test = all_data[ntrain:]
train_x = train
print(train_x.shape[0], train_y.shape[0])
# train_y


# **Cross validation :**

# In[ ]:


#Validation function
n_folds = 5

def rmsle_cv(model):
    kf = KFold(n_folds, shuffle=True, random_state=42).get_n_splits(train.values)
    rmse= np.sqrt(-cross_val_score(model, train.values, train_y, scoring="neg_mean_squared_error", cv = kf))
    return(rmse)


# **Select an algorithm :**

# In[ ]:


model = lgb.LGBMRegressor(objective='regression',num_leaves=5,
                              learning_rate=0.05, n_estimators=720,
                              max_bin = 55, bagging_fraction = 0.8,
                              bagging_freq = 5, feature_fraction = 0.2319,
                              feature_fraction_seed=9, bagging_seed=9,
                              min_data_in_leaf =6, min_sum_hessian_in_leaf = 11)
score = rmsle_cv(model)
print("LGBM score: {:.4f} ({:.4f})\n" .format(score.mean(), score.std()))


# **Mean square error validation :**

# In[ ]:


def rmsle(y, y_pred):
    return np.sqrt(mean_squared_error(y, y_pred))


# **Train the selected model :**

# In[ ]:


model.fit(train_x, train_y)
train_prediction = model.predict(train)
prediction = np.expm1(model.predict(test.values))
print(rmsle(train_y, train_prediction))
# print(prediction)


# Done. Submit the answer.

# In[ ]:


submission = pd.DataFrame({'Id': Id, 'SalePrice': prediction})
submission.to_csv('submission.csv', index=False)

