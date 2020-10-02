#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os

df = pd.read_csv("../input/Iris.csv")


# In[4]:


df.head()


# In[6]:


df.info()


# In[8]:


df.PetalWidthCm.value_counts(normalize=True)


# In[9]:


df.describe()


# In[13]:


df.Species.value_counts()
df['Species'] = df['Species'].map( {'Iris-virginica': 0, 'Iris-versicolor': 1, 'Iris-setosa': 2} ).astype(int)


# In[24]:


X = df[['SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm']]
y = df['Species']


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2,random_state = 1)


# In[25]:


from sklearn.tree import DecisionTreeRegressor
iris_model = DecisionTreeRegressor(random_state=1)
iris_model.fit(X_train,y_train)


# In[26]:


prediciton = iris_model.predict(X_test)
from sklearn.metrics import accuracy_score
print(accuracy_score(prediciton,y_test))


# In[ ]:




