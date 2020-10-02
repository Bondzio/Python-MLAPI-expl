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


#Importing required packages.
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


wine = pd.read_csv('../input/red-wine-quality-cortez-et-al-2009/winequality-red.csv')


# In[ ]:


wine.head()


# In[ ]:


wine.info()


# **Study and Analysis of Data with respect to dependent variable**

# In[ ]:


#Here we see that fixed acidity does not give any specification to classify the quality.
fig = plt.figure(figsize = (10,5))
sns.barplot(x = 'quality', y = 'fixed acidity', data = wine)


# In[ ]:


#Here we see that its quite a downing trend in the volatile acidity as we go higher the quality 
fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'volatile acidity', data = wine)


# In[ ]:


#Composition of citric acid go higher as we go higher in the quality of the wine
fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'citric acid', data = wine)


# In[ ]:


#Residual sugar doesn't have such important info on quality
fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'residual sugar', data = wine)


# In[ ]:


#Composition of chloride also go down as we go higher in the quality of the wine
fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'chlorides', data = wine)


# In[ ]:


#No important info can be be figured out from here 
fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'free sulfur dioxide', data = wine)


# In[ ]:


fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'total sulfur dioxide', data = wine)


# In[ ]:


#Sulphates level goes higher with the quality of wine
fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'sulphates', data = wine)


# In[ ]:


#Alcohol level also goes higher as te quality of wine increases
fig = plt.figure(figsize = (10,6))
sns.barplot(x = 'quality', y = 'alcohol', data = wine)


# Preprocessing Data

# In[ ]:


#Making binary classificaion for the response variable.
#Dividing wine as good and bad by giving the limit for the quality
bins = (2, 6.5, 8)
group_names = ['bad', 'good']
wine['quality'] = pd.cut(wine['quality'], bins = bins, labels = group_names)


# In[ ]:


#Now lets assign a labels to our quality variable
label_quality = LabelEncoder()


# In[ ]:


#Bad becomes 0 and good becomes 1 
wine['quality'] = label_quality.fit_transform(wine['quality'])


# In[ ]:


wine['quality'].value_counts()


# In[ ]:


sns.countplot(wine['quality'])


# In[ ]:


#Now seperate the dataset as response variable and feature variabes
X = wine.drop('quality', axis = 1)
y = wine['quality']


# In[ ]:


#Train and Test splitting of data 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)


# In[ ]:


#Applying Standard scaling to get optimized result
sc = StandardScaler()


# In[ ]:


X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)


# Machine learning algorithm

# Random Forest Classifier

# In[ ]:


rfc = RandomForestClassifier(n_estimators=200)
rfc.fit(X_train, y_train)
pred_rfc = rfc.predict(X_test)


# In[ ]:


#Let's see how our model performed
print(classification_report(y_test, pred_rfc))


# Random forest gives the accuracy of 87%

# In[ ]:


#Confusion matrix for the random forest classification
print(confusion_matrix(y_test, pred_rfc))


# Stochastic Gradient Decent Classifier

# In[ ]:


sgd = SGDClassifier(penalty=None)
sgd.fit(X_train, y_train)
pred_sgd = sgd.predict(X_test)


# In[ ]:


print(classification_report(y_test, pred_sgd))


# 84% accuracy using stochastic gradient descent classifier

# In[ ]:


print(confusion_matrix(y_test, pred_sgd))


# Support Vector Classifier

# In[ ]:


svc = SVC()
svc.fit(X_train, y_train)
pred_svc = svc.predict(X_test)


# In[ ]:


print(classification_report(y_test, pred_svc))


# Support vector classifier gets 86%

# Cross Validation to increase Accuracy

# Grid Search CV

# In[ ]:


#Finding best parameters for our SVC model
param = {
    'C': [0.1,0.8,0.9,1,1.1,1.2,1.3,1.4],
    'kernel':['linear', 'rbf'],
    'gamma' :[0.1,0.8,0.9,1,1.1,1.2,1.3,1.4]
}
grid_svc = GridSearchCV(svc, param_grid=param, scoring='accuracy', cv=10)


# In[ ]:


grid_svc.fit(X_train, y_train)


# In[ ]:


#Best parameters for our svc model
grid_svc.best_params_


# In[ ]:


#Let's run our SVC again with the best parameters.
svc2 = SVC(C = 1.2, gamma =  0.9, kernel= 'rbf')
svc2.fit(X_train, y_train)
pred_svc2 = svc2.predict(X_test)
print(classification_report(y_test, pred_svc2))


# SVC improves from 86% to 90% using Grid Search CV

# Cross Validation Score for random forest and SGD

# In[ ]:


#Now lets try to do some evaluation for random forest model using cross validation.
rfc_eval = cross_val_score(estimator = rfc, X = X_train, y = y_train, cv = 10)
rfc_eval.mean()


# Random forest accuracy increases from 87% to 91 % using cross validation score

# In[ ]:




