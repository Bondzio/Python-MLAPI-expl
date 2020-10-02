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


# ## First 5 rows of the dataset

# In[ ]:


# loading libraries
import pandas as pd

# define column names
names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'Species']

# loading training data
df = pd.read_csv('../input/irisdata/iris.data', header=None, names=names)
df.head()


# 

# In[ ]:


df.describe()


# ## CHecking for correlation

# In[ ]:


import matplotlib.pyplot as plt 
import seaborn as sns
df.corr()


# ## Scatter plot between Sepal width and Sepal Length 

# In[ ]:


sns.scatterplot(x=df["sepal_width"],y=df["sepal_length"],hue=df["Species"])
plt.xlabel("Sepal width")
plt.ylabel("Sepal length")


# ## Scatter PLot between PEtal Width and Petal Length

# In[ ]:


sns.scatterplot(df["petal_width"],df["petal_length"],hue=df["Species"])
plt.xlabel("Petal width")
plt.ylabel("Petal length")


# In[ ]:





# In[ ]:


from sklearn.model_selection import train_test_split
x=df[["sepal_length"]]
y=df["Species"]


# In[ ]:


x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33,random_state=42)


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier


# In[ ]:


knn=KNeighborsClassifier(n_neighbors=3)
knn.fit(x_train,y_train)


# In[ ]:


pred=knn.predict(x_test)


# In[ ]:


neighbors = list(range(1,50,2))


# ## CHecking for optimal value of K

# In[ ]:


cv_scores=[]

import sklearn.model_selection
from sklearn.model_selection import cross_val_score


# In[ ]:


for k in neighbors:
    knn=KNeighborsClassifier(n_neighbors=k)
    scores= sklearn.model_selection.cross_val_score(knn,x_train,y_train,cv=10)
    cv_scores.append(scores.mean())


# In[ ]:


MSE=[1-x for x in cv_scores]
print("The minimum MSE is ",min(MSE))
optimal_k = neighbors[MSE.index(min(MSE))]
print ("The optimal number of neighbors is ",optimal_k)

# plot misclassification error vs k
plt.plot(neighbors, MSE)
plt.xlabel('Number of Neighbors K')
plt.ylabel('Misclassification Error')
plt.show()


# In[ ]:





# In[ ]:




