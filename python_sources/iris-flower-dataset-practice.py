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

from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from xgboost import XGBRegressor, XGBClassifier
from sklearn.metrics import mean_absolute_error, accuracy_score
from sklearn.preprocessing import LabelEncoder


# In[ ]:


df = pd.read_csv("../input/IRIS.csv")
df.shape


# In[ ]:


df.head()


# In[ ]:


df.info()


# No missing values. One categorical variable.

# In[ ]:


label_encoder = LabelEncoder()
df['species'] = label_encoder.fit_transform(df['species'])
df.tail()


# In[ ]:


df.corr()


# In[ ]:


y = df.species
features = ['petal_length','petal_width','sepal_length','sepal_width']
X = df[features].copy()

X_train, X_valid, y_train, y_valid = train_test_split(X,y, train_size=0.8, test_size=0.2, random_state=0)


# Using XGBRegressor to check the MAE for different features combinations.

# In[ ]:


model = XGBRegressor(n_estimators=1000, learning_rate=0.05)
model.fit(X_train,y_train)
preds = model.predict(X_valid)
print("MAE: " + str(mean_absolute_error(preds, y_valid)))


# Removing sepal_width (least corr() value) - MAE increased by 0.01
# 
# Removing petal_width (highest corr() value) - MAE increased by 0.07!

# Now let's check the MAE after scaling.

# In[ ]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler().fit(X)
rescaledX = scaler.transform(X)

X_train, X_valid, y_train, y_valid = train_test_split(rescaledX,y, train_size=0.8, test_size=0.2, random_state=0)

model = XGBRegressor(n_estimators=1000, learning_rate=0.05)
model.fit(X_train,y_train)
preds = model.predict(X_valid)
print("MAE: " + str(mean_absolute_error(preds, y_valid)))


# MAE decreased by 0.002. Meh. Maybe the difference would be bigger on a bigger dataset.

# In[ ]:


model = XGBClassifier(n_estimators=1000, learning_rate=0.05)
model.fit(X_train,y_train)
preds = model.predict(X_valid)
print("Accuracy Score: " + str(accuracy_score(preds, y_valid)))


# In[ ]:


print(preds)


# Cool. :)
