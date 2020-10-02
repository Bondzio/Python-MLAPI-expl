#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from sklearn.preprocessing import LabelEncoder, OneHotEncoder   # handling categorical data 
from sklearn.model_selection import train_test_split            # split the data into taring and testing set
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report # check accuracy of predicted result

import warnings
warnings.filterwarnings('ignore')
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv('/kaggle/input/mushroom-classification/mushrooms.csv')


# In[ ]:


data.head()


# In[ ]:


data.shape


# In[ ]:


# our dataset contains 8124 rows and 23 columns


# In[ ]:


# lets check if there any missing values
data.info()


# In[ ]:


data.describe()


# In[ ]:


# lets divide the data into features and label


# In[ ]:


# beacause data contains so many categorical features we only take some features for our model


# In[ ]:


X = data.iloc[:, 1 : 6].values      # Features
y = data.iloc[:, 0].values          # label


# # Handling categorical features

# In[ ]:


le = LabelEncoder()
ohe = OneHotEncoder(categorical_features = 'all')


# In[ ]:


X[:, 0] = le.fit_transform(X[:, 0])
X[:, 1] = le.fit_transform(X[:, 1])
X[:, 2] = le.fit_transform(X[:, 2])
X[:, 3] = le.fit_transform(X[:, 3])
X[:, 4] = le.fit_transform(X[:, 4])


# In[ ]:


X = ohe.fit_transform(X).toarray()


# In[ ]:


# removing dummy variable trap
X = X[:, [1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 23, 24, 25, 26, 27, 28, 29, 30]]


# ## Split the data into training and testing set

# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42)


# # RandomForestClassifier

# In[ ]:


# train the model 
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier()
classifier.fit(X_train, y_train)


# In[ ]:


# Predicting the results of our model
y_pred = classifier.predict(X_test)


# In[ ]:


# create confusion matrix
confusion_matrix(y_test, y_pred)


# In[ ]:


# check accuracy
accuracy_score(y_test, y_pred)


# In[ ]:


# check f1score
print(classification_report(y_test, y_pred))


# In[ ]:


# hope you guys liked it 


# In[ ]:


# thankyou for visit

