#!/usr/bin/env python
# coding: utf-8

# ## 1. Import libraries

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split


# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


# Importing tensorflow and keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Flatten, Dense, Softmax
from tensorflow.keras import optimizers


# In[ ]:


# Checking the tensorflow libraries  
print(tf.__version__)


# # 2. Data exploration

# In[ ]:


#Loading the dataset

housing_df=pd.read_csv("/kaggle/input/california-housing-prices/housing.csv")


# In[ ]:


housing_df.shape


# In[ ]:


# Displaying the data 

housing_df.head()


# In[ ]:


# Checking for the null values 

housing_df.isna().any()


# In[ ]:


#Count of the null values in each columns

housing_df.isna().sum()


# In[ ]:


# We can drop the null values as their count is less than 5 %

housing_df.dropna(inplace=True)


# In[ ]:


housing_df.isna().sum()


# In[ ]:


housing_df.shape


# In[ ]:


# Dividing the dataset into independant and dependant variables 
X=pd.DataFrame(columns=['longitude','latitude','housing_median_age','total_rooms','total_bedrooms','population','households','median_income','ocean_proximity'],data=housing_df)
y=pd.DataFrame(columns=['median_house_value'],data=housing_df)


# In[ ]:


X.head()


# In[ ]:


y.head()


# In[ ]:


#Creating the dummy values for ocean_proximity

X = pd.get_dummies(data = X, columns = ['ocean_proximity'] , prefix = ['ocean_proximity'] , drop_first = True)


# In[ ]:


X.head()


# # 3. Feature Scaling and test train split

# In[ ]:


#Dividing the training data into test and train 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)


# In[ ]:


X_train.shape


# In[ ]:


#Feature Standardization

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# In[ ]:


X_train


# # ANN

# In[ ]:


model = Sequential()

#Input Layer
model.add(Dense(X.shape[1], activation='relu', input_dim = X.shape[1]))

#Hidden Layer
model.add(Dense(512,kernel_initializer='normal', activation='relu'))
model.add(Dense(512,kernel_initializer='normal', activation='relu'))
model.add(Dense(256,kernel_initializer='normal', activation='relu'))
model.add(Dense(128,kernel_initializer='normal', activation='relu'))
model.add(Dense(64,kernel_initializer='normal', activation='relu'))
model.add(Dense(32,kernel_initializer='normal', activation='relu'))
#Output Layer
model.add(Dense(1,kernel_initializer='normal', activation = 'relu'))


# In[ ]:


X.shape[1]


# In[ ]:


#Compile the network 

model.compile(loss='mse', optimizer='adam', metrics=['mse','mae'])
model.summary()


# In[ ]:


history = model.fit(X_train, y_train.to_numpy(), batch_size = 10, epochs = 10, verbose = 1)


# In[ ]:


y_pred = model.predict(X_test)


# In[ ]:


y_pred


# In[ ]:


y_test


# In[ ]:


model.evaluate(X_test, y_test)

