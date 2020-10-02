#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv('/kaggle/input/international-football-results-from-1872-to-2017/results.csv')


# In[ ]:


data


# In[ ]:


from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
data["neutral"] = le.fit_transform(data["neutral"])
data["neutral"] = data["neutral"].astype("category") 

data["country"] = le.fit_transform(data["country"])
data["country"] = data["country"].astype("category") 

data["city"] = le.fit_transform(data["city"])
data["city"] = data["city"].astype("category") 

data["tournament"] = le.fit_transform(data["tournament"])
data["tournament"] = data["tournament"].astype("category") 

data["away_team"] = le.fit_transform(data["away_team"])
data["away_team"] = data["away_team"].astype("category") 

data["home_team"] = le.fit_transform(data["home_team"])
data["home_team"] = data["home_team"].astype("category") 

data["date"] = le.fit_transform(data["date"])
data["date"] = data["date"].astype("category") 


# In[ ]:


data


# In[ ]:


y = data["neutral"]
x = data.values[: ,0:8]


# In[ ]:


print(data.shape)
print(x.shape)


# In[ ]:


from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix

xtrain,xtest,ytrain,ytest = train_test_split(x, y,test_size=0.2)

clf = DecisionTreeClassifier()
# Train Decision Tree Classifer
clf = clf.fit(xtrain,ytrain)
#Predict the response for test dataset
y_pred = clf.predict(xtest)
acc1 = metrics.accuracy_score(ytest, y_pred)
matrix=confusion_matrix(ytest,y_pred)


# In[ ]:


acc1


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
#Create a Gaussian Classifier
clf=RandomForestClassifier()
#Train the model using the training sets y_pred=clf.predict(X_test)
clf.fit(xtrain,ytrain)
y_pred2=clf.predict(xtest)
acc2 = metrics.accuracy_score(ytest, y_pred2)
matrix2=confusion_matrix(ytest,y_pred2)


# In[ ]:


acc2


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors= 2)
knn.fit(xtrain, ytrain)
acc_knn_test=knn.score(xtest, ytest)
acc_knn_train = knn.score(xtrain , ytrain)
y_pred=knn.predict(xtest) 


# In[ ]:


acc_knn_test


# In[ ]:




