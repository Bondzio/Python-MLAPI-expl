#!/usr/bin/env python
# coding: utf-8

# **Predict House Price**

# **1. Importing Packages**

# In[ ]:


import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import warnings
from sklearn import metrics
from scipy.stats import skew
from scipy import stats
from collections import Counter
warnings.filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from scipy.stats import norm
from scipy import stats
from scipy.stats import skew

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input/house-prices-advanced-regression-techniques/'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        

# Any results you write to the current directory are saved as output.


# In[ ]:


train=pd.read_csv("/kaggle/input/house-prices-advanced-regression-techniques/train.csv")
test=pd.read_csv("/kaggle/input/house-prices-advanced-regression-techniques/test.csv")
# Check the numbers of samples and features
print("The train data size before dropping Id feature is : {} ".format(train.shape))
print("The test data size before dropping Id feature is : {} ".format(test.shape))

# Save the 'Id' column
train_ID = train['Id']
test_ID = test['Id']

# Now drop the 'Id' column since it's unnecessary for the prediction process.
train.drop("Id", axis = 1, inplace = True)
test.drop("Id", axis = 1, inplace = True)

# Check data size after dropping the 'Id' variable
print("\nThe train data size after dropping Id feature is : {} ".format(train.shape)) 
print("The test data size after dropping Id feature is : {} ".format(test.shape))


# In[ ]:


train=pd.read_csv("/kaggle/input/house-prices-advanced-regression-techniques/train.csv")
test=pd.read_csv("/kaggle/input/house-prices-advanced-regression-techniques/test.csv")
train.head()


# In[ ]:


train.describe()


# In[ ]:


###importing necesary libraries...
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


null_columns=train.columns[train.isnull().any()]
train[null_columns].isnull().sum()


# In[ ]:


train[null_columns].head()


# In[ ]:


null_columnst=test.columns[test.isnull().any()]
test[null_columnst].isnull().sum()


# In[ ]:


test[null_columns].head()


# In[ ]:


# Checking Categorical Data
train.select_dtypes(include=['object']).columns


# In[ ]:


# Checking Categorical Data
test.select_dtypes(include=['object']).columns


# In[ ]:


# Checking Numerical Data
train.select_dtypes(include=['int64','float64']).columns


# In[ ]:


cat = len(train.select_dtypes(include=['object']).columns)
num = len(train.select_dtypes(include=['int64','float64']).columns)
print('Total Features: ', cat, 'categorical', '+',
      num, 'numerical', '=', cat+num, 'features')


# In[ ]:


# Checking Numerical Data
test.select_dtypes(include=['int64','float64']).columns


# In[ ]:


cat = len(test.select_dtypes(include=['object']).columns)
num = len(test.select_dtypes(include=['int64','float64']).columns)
print('Total Features: ', cat, 'categorical', '+',
      num, 'numerical', '=', cat+num, 'features')


# **2.Correlation data**

# In[ ]:


# Correlation Matrix Heatmap
corrmat = train.corr()
f, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corrmat, vmax=.8, square=True);


# In[ ]:


# Top 10 Heatmap
k = 10 #number of variables for heatmap
cols = corrmat.nlargest(k, 'SalePrice')['SalePrice'].index
cm = np.corrcoef(train[cols].values.T)
sns.set(font_scale=1.25)
hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
plt.show()


# In[ ]:


most_corr = pd.DataFrame(cols)
most_corr.columns = ['Most Correlated Features']
most_corr


# In[ ]:


# Overall Quality vs Sale Price
var = 'OverallQual'
data = pd.concat([train['SalePrice'], train[var]], axis=1)
f, ax = plt.subplots(figsize=(8, 6))
fig = sns.boxplot(x=var, y="SalePrice", data=data)
fig.axis(ymin=0, ymax=800000);


# In[ ]:


# Living Area vs Sale Price
sns.jointplot(x=train['GrLivArea'], y=train['SalePrice'], kind='reg')


# In[ ]:


# Removing outliers manually (Two points in the bottom right)
train = train.drop(train[(train['GrLivArea']>4000) 
                         & (train['SalePrice']<300000)].index).reset_index(drop=True)


# In[ ]:


# Living Area vs Sale Price
sns.jointplot(x=train['GrLivArea'], y=train['SalePrice'], kind='reg')


# In[ ]:


# Garage Cars Area vs Sale Price
sns.boxplot(x=train['GarageCars'], y=train['SalePrice'])


# In[ ]:


# Removing outliers manually (More than 4-cars, less than $300k)
train = train.drop(train[(train['GarageCars']>3) 
                         & (train['SalePrice']<300000)].index).reset_index(drop=True)


# In[ ]:


# Garage Area vs Sale Price
sns.boxplot(x=train['GarageCars'], y=train['SalePrice'])


# In[ ]:


# Garage Area vs Sale Price
sns.jointplot(x=train['GarageArea'], y=train['SalePrice'], kind='reg')


# In[ ]:


# Removing outliers manually (More than 1000 sqft, less than $300k)
train = train.drop(train[(train['GarageArea']>1000) 
                         & (train['SalePrice']<300000)].index).reset_index(drop=True)


# In[ ]:


# Garage Area vs Sale Price
sns.jointplot(x=train['GarageArea'], y=train['SalePrice'], kind='reg')


# In[ ]:


# Basement Area vs Sale Price
sns.jointplot(x=train['TotalBsmtSF'], y=train['SalePrice'], kind='reg')


# In[ ]:


# First Floor Area vs Sale Price
sns.jointplot(x=train['1stFlrSF'], y=train['SalePrice'], kind='reg')


# In[ ]:


# Total Rooms vs Sale Price
sns.boxplot(x=train['TotRmsAbvGrd'], y=train['SalePrice'])


# In[ ]:


# Total Rooms vs Sale Price
var = 'YearBuilt'
data = pd.concat([train['SalePrice'], train[var]], axis=1)
f, ax = plt.subplots(figsize=(16, 8))
fig = sns.boxplot(x=var, y="SalePrice", data=data)
fig.axis(ymin=0, ymax=800000);
plt.xticks(rotation=90);


# **3.Imputing Null values and places where Null means something**

# In[ ]:


training_null = pd.isnull(train).sum()
testing_null = pd.isnull(test).sum()

null = pd.concat([training_null, testing_null], axis=1, keys=["Train", "Test"])


# In[ ]:


null_many = null[null.sum(axis=1) > 200]  #a lot of missing values
null_few = null[(null.sum(axis=1) > 0) & (null.sum(axis=1) < 200)]  #not as much missing values


# In[ ]:


null_many


# In[ ]:


null_few


# In[ ]:


null_has_meaning = ["Alley", "BsmtQual", "BsmtCond", "BsmtExposure", "BsmtFinType1", "BsmtFinType2", "FireplaceQu", "GarageType", "GarageFinish", "GarageQual", "GarageCond", "PoolQC", "Fence", "MiscFeature"]


# In[ ]:


for i in null_has_meaning:
    train[i].fillna("None", inplace=True)
    test[i].fillna("None", inplace=True)


# In[ ]:


null_columns=train.columns[train.isnull().any()]
train[null_columns].isnull().sum()


# **Imputing "Real" Null Values**

# In[ ]:


import numpy as np
from sklearn.impute import SimpleImputer

SimpleImputer = SimpleImputer(strategy="median")


# In[ ]:


training_null = pd.isnull(train).sum()
testing_null = pd.isnull(test).sum()

null = pd.concat([training_null, testing_null], axis=1, keys=["Train", "Test"])


# In[ ]:


null_many = null[null.sum(axis=1) > 200]  #a lot of missing values
null_few = null[(null.sum(axis=1) > 0) & (null.sum(axis=1) < 200)]  #few missing values


# In[ ]:


null_many


# In[ ]:


train.drop("LotFrontage", axis=1, inplace=True)
test.drop("LotFrontage", axis=1, inplace=True)


# In[ ]:


null_columns=train.columns[train.isnull().any()]
train[null_columns].isnull().sum()


# In[ ]:


null_few


# In[ ]:


train["GarageYrBlt"].fillna(train["GarageYrBlt"].median(), inplace=True)
test["GarageYrBlt"].fillna(test["GarageYrBlt"].median(), inplace=True)
train["MasVnrArea"].fillna(train["MasVnrArea"].median(), inplace=True)
test["MasVnrArea"].fillna(test["MasVnrArea"].median(), inplace=True)
train["MasVnrType"].fillna("None", inplace=True)
test["MasVnrType"].fillna("None", inplace=True)


# Now, the features with a lot of missing values have been taken care of! Let's move on to the features with fewer missing values.

# In[ ]:


types_train = train.dtypes #type of each feature in data: int, float, object
num_train = types_train[(types_train == int) | (types_train == float)] #numerical values are either type int or float
cat_train = types_train[types_train == object] #categorical values are type object

#we do the same for the test set
types_test = test.dtypes
num_test = types_test[(types_test == int) | (types_test == float)]
cat_test = types_test[types_test == object]


# **Numerical Imputing**

# In[ ]:


#we should convert num_train and num_test to a list to make it easier to work with
numerical_values_train = list(num_train.index)
numerical_values_test = list(num_test.index)


# In[ ]:


print(numerical_values_train)


# These are all the numerical features in our data.

# In[ ]:


fill_num = []

for i in numerical_values_train:
    if i in list(null_few.index):
        fill_num.append(i)


# In[ ]:


print(fill_num)


# In[ ]:


for i in fill_num:
    train[i].fillna(train[i].median(), inplace=True)
    test[i].fillna(test[i].median(), inplace=True)


# **Categorical Imputing**

# In[ ]:


categorical_values_train = list(cat_train.index)
categorical_values_test = list(cat_test.index)


# In[ ]:


print(categorical_values_train)


# These are all the categorical features in our data

# In[ ]:


fill_cat = []

for i in categorical_values_train:
    if i in list(null_few.index):
        fill_cat.append(i)


# In[ ]:


print(fill_cat)


# These are the categorical features in the data that have missing values in them. We'll impute with the most common term below.

# In[ ]:


def most_common_term(lst):
    lst = list(lst)
    return max(set(lst), key=lst.count)
#most_common_term finds the most common term in a series

most_common = ["Electrical", "Exterior1st", "Exterior2nd", "Functional", "KitchenQual", "MSZoning", "SaleType", "Utilities", "MasVnrType"]

counter = 0
for i in fill_cat:
    most_common[counter] = most_common_term(train[i])
    counter += 1


# In[ ]:


most_common_dictionary = {fill_cat[0]: [most_common[0]], fill_cat[1]: [most_common[1]], fill_cat[2]: [most_common[2]], fill_cat[3]: [most_common[3]],
                          fill_cat[4]: [most_common[4]], fill_cat[5]: [most_common[5]], fill_cat[6]: [most_common[6]], fill_cat[7]: [most_common[7]],
                          fill_cat[8]: [most_common[8]]}
most_common_dictionary


# In[ ]:


counter = 0
for i in fill_cat:  
    train[i].fillna(most_common[counter], inplace=True)
    test[i].fillna(most_common[counter], inplace=True)
    counter += 1


# In[ ]:


training_null = pd.isnull(train).sum()
testing_null = pd.isnull(test).sum()

null = pd.concat([training_null, testing_null], axis=1, keys=["Training", "Testing"])
null[null.sum(axis=1) > 0]


# **4.Feature Engineering**

# In[ ]:


sns.distplot(train["SalePrice"])


# In[ ]:


sns.distplot(np.log(train["SalePrice"]))


# In[ ]:


train["TransformedPrice"] = np.log(train["SalePrice"])


# In[ ]:


categorical_values_train = list(cat_train.index)
categorical_values_test = list(cat_test.index)


# In[ ]:


print(categorical_values_train)


# In[ ]:


train.head()


# In[ ]:


for i in categorical_values_train:
    feature_set = set(train[i])
    for j in feature_set:
        feature_list = list(feature_set)
        train.loc[train[i] == j, i] = feature_list.index(j)

for i in categorical_values_test:
    feature_set2 = set(test[i])
    for j in feature_set2:
        feature_list2 = list(feature_set2)
        test.loc[test[i] == j, i] = feature_list2.index(j)


# In[ ]:


train.head()


# In[ ]:


test.head()


# Great! It seems like we have changed all the categorical strings into a representative number. We are ready to build our models!

# **5.Creating, Training, Evaluating, Validating, and Testing ML Models**

# In[ ]:


from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge


# **Defining Training/Test Sets**

# In[ ]:


X_training = train.drop(["Id", "SalePrice", "TransformedPrice"], axis=1).values
y_training = train["TransformedPrice"].values
X_test = test.drop("Id", axis=1).values


# **Splitting into Validation**
# 
# It is always good to split our training data again into validation sets. This will help us evaluate our model performance as well as avoid overfitting our model.

# In[ ]:


from sklearn.model_selection import train_test_split #to create validation data set

X_train, X_valid, y_train, y_valid = train_test_split(X_training, y_training, test_size=0.2, random_state=0) #X_valid and y_valid are the validation sets


# **Linear Regression Model**

# In[ ]:


linreg = LinearRegression()
linreg.fit(X_train, y_train)
lin_pred = linreg.predict(X_valid)
r2_lin = r2_score(y_valid, lin_pred)
rmse_lin = np.sqrt(mean_squared_error(y_valid, lin_pred))
print("R^2 Score: " + str(r2_lin))
print("RMSE Score: " + str(rmse_lin))


# In[ ]:


scores_lin = cross_val_score(linreg, X_train, y_train, cv=10, scoring="r2")
print("Cross Validation Score: " + str(np.mean(scores_lin)))


# **Decision Tree Regressor Model**

# In[ ]:


dtr = DecisionTreeRegressor()
dtr.fit(X_train, y_train)
dtr_pred = dtr.predict(X_valid)
r2_dtr = r2_score(y_valid, dtr_pred)
rmse_dtr = np.sqrt(mean_squared_error(y_valid, dtr_pred))
print("R^2 Score: " + str(r2_dtr))
print("RMSE Score: " + str(rmse_dtr))


# In[ ]:


scores_dtr = cross_val_score(dtr, X_train, y_train, cv=10, scoring="r2")
print("Cross Validation Score: " + str(np.mean(scores_dtr)))


# **Random Forest Regressor Model**

# In[ ]:


rf = RandomForestRegressor()
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_valid)
r2_rf = r2_score(y_valid, rf_pred)
rmse_rf = np.sqrt(mean_squared_error(y_valid, rf_pred))
print("R^2 Score: " + str(r2_rf))
print("RMSE Score: " + str(rmse_rf))


# In[ ]:


scores_rf = cross_val_score(rf, X_train, y_train, cv=10, scoring="r2")
print("Cross Validation Score: " + str(np.mean(scores_rf)))


# **Lasso Model**

# In[ ]:


lasso = Lasso()
lasso.fit(X_train, y_train)
lasso_pred = lasso.predict(X_valid)
r2_lasso = r2_score(y_valid, lasso_pred)
rmse_lasso = np.sqrt(mean_squared_error(y_valid, lasso_pred))
print("R^2 Score: " + str(r2_lasso))
print("RMSE Score: " + str(rmse_lasso))


# In[ ]:


scores_lasso = cross_val_score(lasso, X_train, y_train, cv=10, scoring="r2")
print("Cross Validation Score: " + str(np.mean(scores_lasso)))


# **Ridge**

# In[ ]:


ridge = Ridge()
ridge.fit(X_train, y_train)
ridge_pred = ridge.predict(X_valid)
r2_ridge = r2_score(y_valid, ridge_pred)
rmse_ridge = np.sqrt(mean_squared_error(y_valid, ridge_pred))
print("R^2 Score: " + str(r2_ridge))
print("RMSE Score: " + str(rmse_ridge))


# In[ ]:


scores_ridge = cross_val_score(ridge, X_train, y_train, cv=10, scoring="r2")
print("Cross Validation Score: " + str(np.mean(scores_ridge)))


# **6.Valuation Models**

# In[ ]:


model_performances = pd.DataFrame({
    "Model" : ["Linear Regression", "Decision Tree Regressor", "Random Forest Regressor","Ridge", "Lasso"],
    "R Squared" : [str(r2_lin)[0:5], str(r2_dtr)[0:5], str(r2_rf)[0:5], str(r2_ridge)[0:5], str(r2_lasso)[0:5]],
    "RMSE" : [str(rmse_lin)[0:8], str(rmse_dtr)[0:8], str(rmse_rf)[0:8], str(rmse_ridge)[0:8], str(rmse_lasso)[0:8]]
})
model_performances.round(4)


# In[ ]:


print("Sorted by R Squared:")
model_performances.sort_values(by="R Squared", ascending=False)


# In[ ]:


print("Sorted by RMSE:")
model_performances.sort_values(by="RMSE", ascending=True)


# In[ ]:


linreg.fit(X_training, y_training)


# **7.Submission**

# In[ ]:


submission_predictions = np.exp(linreg.predict(X_test))


# In[ ]:


submission = pd.DataFrame({
        "Id": test["Id"],
        "SalePrice": submission_predictions
    })

submission.to_csv("saleprice_3_group6.csv", index=False)
print(submission.shape)

