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


# # introduction
# 
# #### A heart attack occurs when an artery supplying your heart with blood and oxygen becomes blocked. Fatty deposits build up over time, forming plaques in your heart's arteries. If a plaque ruptures, a blood clot can form and block your arteries, causing a heart attack.

# In[ ]:


## import the packages 
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix


# In[ ]:


## load the data
data = pd.read_csv("../input/health-care-data-set-on-heart-attack-possibility/heart.csv")


# In[ ]:


## check the data
data.head()


# # EDA

# In[ ]:


## check the info of the data
data.info()


# In[ ]:


## check for missing values
data.isnull().sum()


# In[ ]:


## the columns
data.columns


# In[ ]:


## plot the age feature 
sns.distplot(data["age"])


# In[ ]:


## plot the target variable
sns.countplot(data["target"])


# In[ ]:


## plot the heat map
g = data.corr()
df_ = g.index
g = sns.heatmap(data[df_].corr())


# # Modelling and Predicting

# In[ ]:


## select dependent and independent features 
X = data.drop("target", axis=1)
y = data["target"]


# In[ ]:


## split the dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)


# In[ ]:


## import the model
## we'll be using the random forest classidier 

random_forest = RandomForestClassifier(n_estimators=100)
random_forest.fit(X_train, y_train)

Y_prediction = random_forest.predict(X_test)

random_forest.score(X_train, y_train)


# In[ ]:


print(classification_report(y_test, Y_prediction))


# In[ ]:


print(confusion_matrix(y_test, Y_prediction))


# In[ ]:


## plot the confusion matrix in a heat map
sns.heatmap(confusion_matrix(y_test, Y_prediction), annot=True, cmap="mako")


# In[ ]:


## feature importance
feat_importances = pd.Series(random_forest.feature_importances_, index=X.columns)
feat_importances.nlargest(13).plot(kind='barh')


# ### Suggestions and corrections are welcomed :)
