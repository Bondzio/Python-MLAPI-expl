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


df = pd.read_csv("../input/bike_share.csv")


# In[ ]:


df.head()


# In[ ]:


df.describe().T


# In[ ]:


df.info()


# In[ ]:


df.corr()['count']


# In[ ]:


df.isna().sum()


# In[ ]:


df.duplicated().sum()


# In[ ]:


df = df.drop_duplicates()
df.duplicated().sum()


# In[ ]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# In[ ]:


sns.regplot(x=df["count"],y=df["registered"])


# In[ ]:


sns.scatterplot(x=df["count"],y=df["casual"],hue=df["temp"])


# In[ ]:


df.columns


# In[ ]:


df["season"].value_counts()


# In[ ]:


df["holiday"].value_counts()


# In[ ]:


df["workingday"].value_counts()


# In[ ]:


df["weather"].value_counts()


# In[ ]:


df["temp"].value_counts()


# In[ ]:


df["atemp"].value_counts()


# In[ ]:


df["humidity"].value_counts()


# In[ ]:


df["windspeed"].value_counts()


# In[ ]:


df["casual"].value_counts()


# In[ ]:


df["registered"].value_counts()


# In[ ]:


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# In[ ]:


y = df["count"]


# In[ ]:


x = df[["season","holiday","workingday","weather","temp","humidity","windspeed"]]


# In[ ]:


train_x, test_x, train_y, test_y = train_test_split(x,y,test_size=0.3,random_state=3)


# In[ ]:


model = LinearRegression()


# In[ ]:


model.fit(train_x,train_y)


# In[ ]:


print(model.intercept_)


# In[ ]:


print(model.coef_)


# In[ ]:


print("Predicting train data")
train_predict = model.predict(train_x)
print("Predicting test data")
test_predict = model.predict(test_x)
print(" ")
print("MAE")
print("Train data: ",mean_absolute_error(train_y,train_predict))
print("Test data: ",mean_absolute_error(test_y,test_predict))
print(" ")
print("MSE")
print("Train data: ",mean_squared_error(train_y,train_predict))
print("Test data: ",mean_squared_error(test_y,test_predict))
print(" ")
print("RMSE")
print("Train data: ",np.sqrt(mean_squared_error(train_y,train_predict)))
print("Test data: ",np.sqrt(mean_squared_error(test_y,test_predict)))
print(" ")
print("R^2")
print("Train data: ",r2_score(train_y,train_predict))
print("Test data: ",r2_score(test_y,test_predict))

