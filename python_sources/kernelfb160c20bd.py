#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


#import required packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (10,6)
from sklearn import preprocessing

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


#load the data
train = pd.read_csv('..//input//train.csv')
test = pd.read_csv('../input//test.csv')


# In[ ]:


train.shape


# In[ ]:


test.shape


# In[ ]:


#overview ofthe data
train.head()


# In[ ]:


#stats of the predictor variable (saleprice)
train.SalePrice.describe().round(2)


# In[ ]:


#analysing the distribution of sale price
print('skew is', train.SalePrice.skew())   
plt.hist(train['SalePrice'], color= 'b')

plt.title('Distribution of sales price of houses', fontsize = 24)
plt.ylabel('observation', fontsize = 20)
plt.xlabel('sales price', fontsize = 20)

plt.show()


# In[ ]:


#log transforming sale price to transform it into gaussian distribution
target = np.log(train.SalePrice)


# In[ ]:


print('skew is', target.skew())
plt.hist(target, color= 'b')

plt.title('Distribution of sales price of houses', fontsize = 24)
plt.ylabel('observation', fontsize = 20)
plt.xlabel('sales price', fontsize = 20)

plt.show()


# In[ ]:


#seeking only the numeric features from the data
numeric_features = train.select_dtypes(include = [np.number])
numeric_features.dtypes


# In[ ]:


#features with the most correlation with the predictor variable
corr = numeric_features.corr()
print(corr['SalePrice'].sort_values(ascending = False)[:5], '\n')
print(corr['SalePrice'].sort_values(ascending = False)[-5:])


# In[ ]:


train.OverallQual.unique()


# In[ ]:


#pivot table of Overall Quality & Sale price
quality_pivot = train.pivot_table(index= 'OverallQual', values= 'SalePrice')


# In[ ]:


#plotting the pivot table
quality_pivot.plot(kind = 'bar', color = 'blue')

plt.xlabel('Overall Quality')
plt.ylabel('Median Sale Price')
plt.xticks(rotation = 0)
plt.show()


# In[ ]:


#Analysing the feature - ground living area 
plt.scatter(x = train['GrLivArea'], y = target)

plt.xlabel('Above grade (ground) living area square feet')
plt.ylabel('Sale Price')
plt.show()


# In[ ]:


#Analysing the feature - garage area
plt.scatter(x = train['GarageArea'], y = target)

plt.xlabel('Garage Area')
plt.ylabel('Sale Price')
plt.show()


# In[ ]:


#removing the outliers
train = train[train['GarageArea'] < 1200]


# In[ ]:


plt.scatter(x = train['GarageArea'], y = np.log(train.SalePrice))

plt.xlim(-200, 1600)
plt.xlabel('Garage Area')
plt.ylabel('Sale Price')
plt.show()


# In[ ]:


#checking the null values
nulls = pd.DataFrame(train.isnull().sum().sort_values(ascending = False)[:25])
nulls.columns = ['Null Count']
nulls.index.name = 'Feature'
nulls[:5]


# In[ ]:


print('Unique values are:', train.MiscFeature.unique())


# In[ ]:


#analysing the categorical data
categoricals = train.select_dtypes(exclude= [np.number])
categoricals.describe()


# In[ ]:


print ("Original: \n") 
print (train.Street.value_counts(), "\n")


# In[ ]:



#One-hot encoding to convert the categorical data into integer data
train['enc_street'] = pd.get_dummies(train.Street, drop_first= True)
test['enc_street'] = pd.get_dummies(test.Street, drop_first= True)


# In[ ]:


print('Encoded: \n')
print(train.enc_street.value_counts())


# In[ ]:


#Analysing the feature - Sale Condition
condition_pivot = train.pivot_table(index= 'SaleCondition', values= 'SalePrice', aggfunc= np.median)

condition_pivot.plot(kind= 'bar', color = 'blue')
plt.xlabel('Sale Condition')
plt.ylabel('Median Sale Price')
plt.xticks(rotation = 0)
plt.show()


# In[ ]:


def encode(x): 
    if x == 'Partial':
        return 1
    else:
        return 0


# In[ ]:


#Treating partial as one class and other all sale condition as other
train['enc_condition'] = train.SaleCondition.apply(encode)
test['enc_condition'] = test.SaleCondition.apply(encode)


# In[ ]:


condition_pivot = train.pivot_table(index= 'enc_condition', values= 'SalePrice', aggfunc= np.median)

condition_pivot.plot(kind= 'bar', color = 'blue')
plt.xlabel('Encoded Sale Condition')
plt.ylabel('Median Sale Price')
plt.xticks(rotation = 0)
plt.show()


# In[ ]:


#Handling the missing values by interpolation
data = train.select_dtypes(include= [np.number]).interpolate().dropna()


# In[ ]:


#Verifying missing values
sum(data.isnull().sum() != 0)


# In[ ]:



#log transforming the target variable to improve the linearity of the regression
y = np.log(train.SalePrice)
#dropping the target variable and the index from the training set
X = data.drop(['SalePrice', 'Id'], axis = 1)


# In[ ]:


#splitting the data into training and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 42, test_size = .33)


# In[ ]:


#Linear regression model
from sklearn import linear_model
lr = linear_model.LinearRegression()


# In[ ]:


#fitting linear regression on the data
model = lr.fit(X_train, y_train)


# In[ ]:


#R square value
print('R square is: {}'.format(model.score(X_test, y_test)))


# In[ ]:


#predicting on the test set
predictions = model.predict(X_test)


# In[ ]:


#evaluating the model on mean square error
from sklearn.metrics import mean_squared_error, accuracy_score
print('RMSE is {}'.format(mean_squared_error(y_test, predictions)))


# In[ ]:


actual_values = y_test
plt.scatter(predictions, actual_values, alpha= 0.75, color = 'b')

plt.xlabel('Predicted price')
plt.ylabel('Actual price')
plt.title('Linear Regression Model')
plt.show()


# In[ ]:


#Linear regression with L2 regularization
for i in range(-2, 3):
    alpha = 10**i
    rm = linear_model.Ridge(alpha = alpha)
    ridge_model = rm.fit(X_train, y_train)
    preds_ridge = ridge_model.predict(X_test)
    
    plt.scatter(preds_ridge, y_test, alpha= 0.75, c= 'b')
    plt.xlabel('Predicted price')
    plt.ylabel('Actual price')
    plt.title('Ridge redularization with alpha {}'.format(alpha))
    overlay = 'R square: {} \nRMSE: {}'.format(ridge_model.score(X_test, y_test), mean_squared_error(y_test, preds_ridge))
    plt.annotate(s = overlay, xy = (12.1, 10.6), size = 'x-large')
    plt.show()


# In[ ]:


#Gradient boosting regressor model
from sklearn.ensemble import GradientBoostingRegressor


# In[ ]:


est = GradientBoostingRegressor(n_estimators= 1000, max_depth= 2, learning_rate= .01)
est.fit(X_train, y_train)


# In[ ]:


y_train_predict = est.predict(X_train)


# In[ ]:


y_test_predict = est.predict(X_test)


# In[ ]:


est_train = mean_squared_error(y_train, y_train_predict)
print('Mean square error on the Train set is: {}'.format(est_train))


# In[ ]:


est_test = mean_squared_error(y_test, y_test_predict)
print('Mean square error on the Test set is: {}'.format(est_test))


# In[ ]:




