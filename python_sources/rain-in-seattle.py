#!/usr/bin/env python
# coding: utf-8

# 1. [Data Load and Check](#1)
# 2. [Supervised Learning](#2)
#    * [KNN](#3)
#    * [SVM](#4)
#    * [Naive Bayes](#5)
#    * [Decision Tree](#6)
#    * [Random Forest](#7)
# 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from collections import Counter
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# <a id ="1" >
# # Data Load and Check

# In[ ]:


data = pd.read_csv("/kaggle/input/did-it-rain-in-seattle-19482017/seattleWeather_1948-2017.csv")


# In[ ]:


data.head(20)


# In[ ]:


data.info()


# In[ ]:


index_nan = list(data["PRCP"][data["PRCP"].isnull()].index)
data.drop(index_nan,inplace=True)


# In[ ]:


date = data.DATE


# In[ ]:


T = data[data["RAIN"] == True]
F = data[data["RAIN"] == False]


# In[ ]:


data["RAIN"] = [1 if i==True else 0 for i in data["RAIN"] ]


# In[ ]:


data.head()


# In[ ]:


y = data.RAIN.values


# In[ ]:


x_data = data.drop(["RAIN"],axis=1,inplace=True)
x_data = data.drop(["DATE"],axis=1)


# In[ ]:


x = ((x_data - np.min(x_data) )/(np.max(x_data)-np.min(x_data)))


# In[ ]:


from sklearn.model_selection import train_test_split
x_train , x_test, y_train, y_test = train_test_split(x,y,test_size=0.3,random_state=2)


# <a id ="2">
#     
# # SUPERVISED LEARNING

# <a id="3" >
# ## KNN

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors = 3)
knn.fit(x_train,y_train)
y_predictknn = knn.predict(x_test)
print("acc = ", knn.score(x_test,y_test))

supervised =["KNN"]
score=[knn.score(x_test,y_test)]


# In[ ]:


from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test,y_predictknn)
import seaborn as sns
f , ax = plt.subplots(figsize=(5,5))

sns.heatmap(cm,annot = True,linewidths =0.5,linecolor ="Red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.show()


# <a id="4" >
# ## SVM

# In[ ]:


from sklearn.svm import SVC

svm = SVC(random_state=2)
svm.fit(x_train,y_train)
y_predictsvm = svm.predict(x_test)
print("acc = ", svm.score(x_test,y_test))

supervised =supervised+["SVM"]
score=score+[svm.score(x_test,y_test)]


# In[ ]:


cm = confusion_matrix(y_test,y_predictsvm)
f , ax = plt.subplots(figsize=(5,5))

sns.heatmap(cm,annot = True,linewidths =0.5,linecolor ="Red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.show()


# <a id="5" >
# ## Naive Bayes
#  

# In[ ]:


from sklearn.naive_bayes import GaussianNB
nb=GaussianNB()

nb.fit(x_train,y_train)
y_predictnb=nb.predict(x_test)
print("acc = ", nb.score(x_test,y_test))
supervised =supervised+["NB"]
score=score+[nb.score(x_test,y_test)]


# In[ ]:


cm = confusion_matrix(y_test,y_predictnb)
f , ax = plt.subplots(figsize=(5,5))

sns.heatmap(cm,annot = True,linewidths =0.5,linecolor ="Red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.show()


# <a id="6" >
# ## Decision Tree Class

# In[ ]:


from sklearn.tree import DecisionTreeClassifier

dt = DecisionTreeClassifier()

dt.fit(x_train,y_train)
y_predictdt=dt.predict(x_test)

print("acc = ", dt.score(x_test,y_test))
supervised =supervised+["Dt"]
score=score+[dt.score(x_test,y_test)]


# In[ ]:


cm = confusion_matrix(y_test,y_predictdt)
f , ax = plt.subplots(figsize=(5,5))

sns.heatmap(cm,annot = True,linewidths =0.5,linecolor ="Red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.show()


# <a id="7" >
# ## Random Forest 

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)

rf.fit(x_train,y_train)
y_predictrf=rf.predict(x_test)

print("acc = ", rf.score(x_test,y_test))
supervised =supervised+["Rf"]
score=score+[rf.score(x_test,y_test)]


# In[ ]:


cm = confusion_matrix(y_test,y_predictrf)
f , ax = plt.subplots(figsize=(5,5))

sns.heatmap(cm,annot = True,linewidths =0.5,linecolor ="Red",fmt=".0f",ax=ax)
plt.xlabel("y_pred")
plt.ylabel("y_true")
plt.show()


# In[ ]:


plt.plot(supervised,score)
plt.show()

