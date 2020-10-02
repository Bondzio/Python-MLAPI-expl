#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import os
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt 
import seaborn as sns 
from sklearn.model_selection import cross_val_score, train_test_split
train = pd.read_csv("../input/train.csv")


# In[2]:


train.head()


# In[3]:


train.describe()


# In[4]:


X_train = train[["MSSubClass","LotArea","LotFrontage","OverallQual","OverallCond","YearBuilt","YearRemodAdd","MasVnrArea","BsmtFinSF1", "1stFlrSF","GarageCars"]]
y_train = train[["SalePrice"]]
X_train = X_train.replace([np.inf, -np.inf], np.nan)
X_train = X_train.fillna(0)
y_train = y_train.fillna(0)


# In[5]:


plt.figure(figsize=(15,8))
sns.heatmap(X_train.corr(),annot=True,cmap='coolwarm')
plt.show()


# In[6]:


plt.figure(figsize=(12,8))
sns.distplot(train['SalePrice'], color='r')
plt.title('Distribution of Sales Price', fontsize=18)
print("Skewness: %f" % train['SalePrice'].skew())
print("Kurtosis: %f" % train['SalePrice'].kurt())
plt.show()


# In[7]:


X_train = train[["MSSubClass","LotArea","LotFrontage","OverallQual","OverallCond","YearBuilt","YearRemodAdd","MasVnrArea","BsmtFinSF1", "1stFlrSF","GarageCars"]]
y_train = train[["SalePrice"]]
X_train = X_train.replace([np.inf, -np.inf], np.nan)
X_train = X_train.fillna(0)
y_train = y_train.fillna(0)

X_train,X_test,y_train,y_test = train_test_split(X_train,y_train,test_size = 0.3,random_state= 0)
reg = LinearRegression().fit(X_train, y_train)
preds = reg.predict(X_test)
reg.score(X_test, y_test)


# In[8]:


print ('RMSE: ', mean_squared_error(y_test, preds))


# In[9]:


train['SalePrice_Log'] = np.log(train['SalePrice'])
plt.figure(figsize=(12,8))
sns.distplot(train['SalePrice_Log'], color='r')
plt.title('Distribution of Sales Price after Log', fontsize=18)
print("Skewness: %f" % train['SalePrice_Log'].skew())
print("Kurtosis: %f" % train['SalePrice_Log'].kurt())
plt.show()


# In[10]:


X_train = train[["MSSubClass","LotArea","LotFrontage","OverallQual","OverallCond","YearBuilt","YearRemodAdd","MasVnrArea","BsmtFinSF1", "1stFlrSF","GarageCars"]]
y_train = train[["SalePrice_Log"]]
X_train.dtypes


# In[11]:


X_train = X_train.replace([np.inf, -np.inf], np.nan)
X_train = X_train.fillna(0)
y_train = y_train.fillna(0)

X_train,X_test,y_train,y_test = train_test_split(X_train,y_train,test_size = 0.3,random_state= 0)


# In[12]:


reg = LinearRegression().fit(X_train, y_train)


# In[13]:


reg.score(X_test, y_test)


# In[14]:


preds = reg.predict(X_test)
print ('RMSE: ', mean_squared_error(y_test, preds))


# In[15]:


test = pd.read_csv("../input/test.csv")
X_test = test[["MSSubClass","LotArea","LotFrontage","OverallQual","OverallCond","YearBuilt","YearRemodAdd","MasVnrArea","BsmtFinSF1", "1stFlrSF","GarageCars"]]
X_test = X_test.replace([np.inf, -np.inf], np.nan)
X_test = X_test.fillna(0)
predicted_prices = reg.predict(X_test)
predicted_prices_list = []
for predict in predicted_prices:
    predicted_prices_list.append(predict[0])
print(predicted_prices_list)


# In[16]:


submission = pd.DataFrame({"Id": test.Id, 'SalePrice': predicted_prices_list})


# In[17]:


submission.to_csv('submission.csv', index=False)


# In[ ]:




