#!/usr/bin/env python
# coding: utf-8

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


# In[ ]:


# load important packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


# data loading
data = pd.read_csv('/kaggle/input/datasets_383055_741735_CarPrice_Assignment.csv')
data.head()


# In[ ]:


# data info
data.info()


# In[ ]:


# checking for null values
data.isna().sum()


# In[ ]:


# getting all columns
data.columns


# In[ ]:


def get_unique_values(dataset):
    """ this function will return unique values from a dataset attribute wise"""
    df = dataset.select_dtypes(include = np.object)
    cols = list(df.columns)
    for i in cols:
        print('{}: {}'.format(i,df[i].unique()), '\n')


# In[ ]:


get_unique_values(data)


# In[ ]:


# drop unnecessary attributes from data
data_clean = data.copy(deep= True)
data_clean.drop(columns = ['car_ID','CarName'], axis = 1, inplace = True)
data_clean.columns


# In[ ]:


# select float datatype data
data_clean.select_dtypes(include= [np.float, np.int64]).head()


# In[ ]:


# select category data
data_clean.select_dtypes(include= np.object).head()


# In[ ]:


df_numeric = data_clean.select_dtypes(include= [np.float, np.int64])
df_cat = data_clean.select_dtypes(include= np.object)


# In[ ]:


# pairplot for better understanding of data
sns.pairplot(df_numeric)
plt.show()


# In[ ]:


df_cat.columns


# In[ ]:


# barplots for target variable importance on input attributes
for i in list(df_cat.columns):
    plt.style.use('seaborn')
    sns.barplot(x = i, y = 'price', data = data_clean,estimator= sum )
    plt.show()


# In[ ]:


data_clean.groupby('fueltype')['price'].sum().sort_values(ascending = False)


# In[ ]:


# more pandas way to see the data group wise
for i in list(df_cat.columns):
    print(pd.DataFrame(data_clean.groupby(i)['price'].sum().sort_values(ascending = False)), '\n')


# In[ ]:


# boxplots for outliers
for i in list(df_numeric.columns):
    plt.boxplot(i, data = df_numeric)
    plt.title(i)
    plt.show()


# In[ ]:


data_clean.head()


# In[ ]:


# create a final data with dummies
final_data = pd.get_dummies(data_clean, columns= list(df_cat.columns),drop_first= True)
final_data.columns


# In[ ]:



print('original data shape : {}'.format(data.shape))
print('final data shape : {}'.format(final_data.shape))


# In[ ]:


# scaling
from sklearn.preprocessing import MinMaxScaler
ms = MinMaxScaler()
final_data[list(df_numeric.columns)[:-1]] = ms.fit_transform(final_data[list(df_numeric.columns)[:-1]])


# In[ ]:


X_data = final_data.drop(columns= 'price')
y_data = final_data['price']


# In[ ]:


# array of input and target variable
X = X_data.iloc[:].values
y = y_data.iloc[:].values


# In[ ]:


# divide the data into train and test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)


# In[ ]:


# import all machine learning packages from sklearn
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb


# In[ ]:


# build models
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
dt_model = DecisionTreeRegressor()
dt_model.fit(X_train, y_train)
rf_model = RandomForestRegressor()
rf_model.fit(X_train,y_train)
xg_model = xgb.XGBRegressor()
xg_model.fit(X_train,y_train)


# In[ ]:


# train model evaluation
print('linear model score: {}'.format(lr_model.score(X_train, y_train)))
print('decison model score: {}'.format(dt_model.score(X_train, y_train)))
print('rf model score: {}'.format(rf_model.score(X_train, y_train)))
print('xg boost model score: {}'.format(xg_model.score(X_train, y_train)))


# In[ ]:


# test model evaluation
print('linear model score: {}'.format(lr_model.score(X_test, y_test)))
print('decison model score: {}'.format(dt_model.score(X_test, y_test)))
print('rf model score: {}'.format(rf_model.score(X_test, y_test)))
print('xg boost model score: {}'.format(xg_model.score(X_test, y_test)))


# In[ ]:


# getting predictions on all models 
y_pred_lr = lr_model.predict(X_test)
y_pred_dt = dt_model.predict(X_test)
y_pred_rf = rf_model.predict(X_test)
y_pred_xg = xg_model.predict(X_test)


# In[ ]:


# error metrics for all models
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
print('linear reg metrics', '\n')
print('mae score : {}'.format(mean_absolute_error(y_test, y_pred_lr)))
print('mse score : {}'.format(mean_squared_error(y_test, y_pred_lr)))
print('rmse score : {}'.format(np.sqrt(mean_squared_error(y_test, y_pred_lr))))
print('R2 score : {}'.format(r2_score(y_test, y_pred_lr)))


# In[ ]:


from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
print('decision tree metrics', '\n')
print('mae score : {}'.format(mean_absolute_error(y_test, y_pred_dt)))
print('mse score : {}'.format(mean_squared_error(y_test, y_pred_dt)))
print('rmse score : {}'.format(np.sqrt(mean_squared_error(y_test, y_pred_dt))))
print('R2 score : {}'.format(r2_score(y_test, y_pred_dt)))


# In[ ]:



from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
print('randomforest metrics', '\n')
print('mae score : {}'.format(mean_absolute_error(y_test, y_pred_rf)))
print('mse score : {}'.format(mean_squared_error(y_test, y_pred_rf)))
print('rmse score : {}'.format(np.sqrt(mean_squared_error(y_test, y_pred_rf))))
print('R2 score : {}'.format(r2_score(y_test, y_pred_rf)))


# In[ ]:


from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
print('xgboost metrics', '\n')
print('mae score : {}'.format(mean_absolute_error(y_test, y_pred_xg)))
print('mse score : {}'.format(mean_squared_error(y_test, y_pred_xg)))
print('rmse score : {}'.format(np.sqrt(mean_squared_error(y_test, y_pred_xg))))
print('R2 score : {}'.format(r2_score(y_test, y_pred_xg)))


# In[ ]:


#plot graph of feature importances for better visualization
feat_importances = pd.Series(dt_model.feature_importances_, index=X_data.columns)
feat_importances.nlargest(10).plot(kind='barh')
plt.show()


# In[ ]:


feat_importances = pd.Series(rf_model.feature_importances_, index=X_data.columns)
feat_importances.nlargest(10).plot(kind='barh')
plt.show()


# In[ ]:


feat_importances = pd.Series(xg_model.feature_importances_, index=X_data.columns)
feat_importances.nlargest(10).plot(kind='barh')
plt.show()


# ### Note: The idea of feature importance and PCA was to give you an idea about it

# In[ ]:


# Applying PCA (diamentionality reduction technique)
# 95% of variance
from sklearn.decomposition import PCA
pca = PCA(n_components = 0.95)
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)
explained_variance = pca.explained_variance_ratio_


# In[ ]:


pca.explained_variance_


# In[ ]:


X_train.shape


# In[ ]:


# Applying PCA
# 99% of variance
from sklearn.decomposition import PCA
pca = PCA(n_components = 0.99)
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)
explained_variance = pca.explained_variance_ratio_


# In[ ]:


X_train.shape


# ### Note: we saw diamentionality reduction from original training set after applying PCA

# In[ ]:




