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


data = pd.read_csv("/kaggle/input/heart-disease-uci/heart.csv")


# In[ ]:


data.head()


# In[ ]:


## Variable Identification


# In[ ]:


# Category variables === > sex , cp , trestbps , fbs , restecg , exang , slope , thal
# Continuous variables === > age , trestbps , chol , thalach , oldpeak


# In[ ]:


data.describe()


# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


sns.heatmap(data.corr(), annot=True)


# In[ ]:


sns.countplot(data.target)


# In[ ]:


sns.distplot(data.age)


# In[ ]:


data.hist()


# In[ ]:


data.isnull().sum()  # no missing values


# In[ ]:


data_clean = pd.get_dummies(data,columns=['sex' , 'cp' , 'fbs' , 'restecg' , 'exang' , 'slope' , 'thal'],drop_first=True)


# In[ ]:


data_clean.head()


# In[ ]:


from sklearn.preprocessing import StandardScaler

stdScaler = StandardScaler()
cols_ToScale = [ 'age' , 'trestbps' , 'chol' , 'thalach' , 'oldpeak']
data_clean[cols_ToScale] = stdScaler.fit_transform(data_clean[cols_ToScale])


# In[ ]:


data_clean.head()


# In[ ]:


X = data_clean.drop('target',axis=1)
y = data_clean['target']


# In[ ]:


# split the data

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y)


# In[ ]:


X_test.head()
accuracies = {}


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV


# In[ ]:


knn_params = {'n_neighbors':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]}
knn= KNeighborsClassifier()
grid_knn = GridSearchCV(knn,knn_params,scoring='accuracy',cv=10)
grid_knn.fit(X_train,y_train)


# In[ ]:


print(grid_knn.best_score_  , grid_knn.best_params_)


# In[ ]:


#y_pred = grid_knn.predict(X_test)
knn = KNeighborsClassifier(n_neighbors=8)
knn.fit(X_train,y_train)
y_pred_knn = knn.predict(X_test)


# In[ ]:


from sklearn.metrics import accuracy_score
knn_score = accuracy_score(y_test,y_pred_knn)
accuracies["KNN"] = knn_score
knn_score


# In[ ]:


from sklearn.tree import DecisionTreeClassifier


# In[ ]:


decision_tree = DecisionTreeClassifier()
decision_tree_params = {'criterion':['gini','entropy'],'max_depth':[4,5,6,7,8]}
grid_tree = GridSearchCV(decision_tree,decision_tree_params,cv=10,refit=True)
grid_tree.fit(X_train,y_train)


# In[ ]:


print(grid_tree.best_score_ , grid_tree.best_params_)


# In[ ]:


dt = DecisionTreeClassifier(criterion='entropy',max_depth=4)
dt.fit(X_train,y_train)
y_pred_dtree = dt.predict(X_test)


# In[ ]:


y_pred = grid_tree.predict(X_test)
decision_tree_score = accuracy_score(y_test,y_pred_dtree)
accuracies["DecisionTree"]=decision_tree_score
decision_tree_score


# In[ ]:


from sklearn.ensemble import RandomForestClassifier


# In[ ]:


random_forest = RandomForestClassifier()
random_forest_grid_prams = {'criterion':['gini','entropy'],'n_estimators':[100,500],'max_features':range(3,5)}
random_forest_grid = GridSearchCV(random_forest , random_forest_grid_prams,cv=10)
random_forest_grid.fit(X_train,y_train)


# In[ ]:


print(random_forest_grid.best_score_ , random_forest_grid.best_params_)
rf = RandomForestClassifier(criterion='entropy',max_features=3,n_estimators=100)
rf.fit(X_train,y_train)
y_pred_Randomforest=rf.predict(X_test)


# In[ ]:


rf_score = accuracy_score(y_test,y_pred_Randomforest)
accuracies["RandomForest"]= rf_score
rf_score


# In[ ]:


from sklearn.naive_bayes import GaussianNB
nb = GaussianNB()
nb.fit(X_train,y_train)
y_pred_nb = nb.predict(X_test)
nb_score = accuracy_score(y_test,y_pred_nb)
accuracies["GaussianNB"] = nb_score
nb_score


# In[ ]:


sns.set_style('whitegrid')
plt.figure(figsize=(16,5))
sns.barplot(x=list(accuracies.keys()),y=list(accuracies.values()))


# In[ ]:


from sklearn.metrics import confusion_matrix

knn_cm = confusion_matrix(y_test,y_pred_knn)
dt_cm = confusion_matrix(y_test,y_pred_dtree)
rf_cm = confusion_matrix(y_test,y_pred_Randomforest)
nb_cm = confusion_matrix(y_test,y_pred_nb)


# In[ ]:




