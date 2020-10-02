#!/usr/bin/env python
# coding: utf-8

# In[ ]:



from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split


# In[ ]:


dataset=pd.read_csv("/kaggle/input/titanic/train_and_test2.csv")
dataset.head()


# In[ ]:


dataset=dataset.drop("Passengerid",axis=1)


# In[ ]:


dataset.info()


# In[ ]:


dataset.isnull().sum()


# In[ ]:


dataset=dataset.dropna()


# In[ ]:


dataset.isnull().sum()


# In[ ]:


dataset=dataset.drop(["zero","zero.1","zero.2","zero.3","zero.4","zero.5","zero.6"
                   ,"zero.7","zero.8","zero.9","zero.10","zero.11","zero.12",
                   "zero.13","zero.14","zero.15","zero.16","zero.17","zero.18"],axis=1)


# In[ ]:


dataset.info()


# In[ ]:


y=dataset["2urvived"]
x=dataset.drop("2urvived",axis=1)


# In[ ]:


import seaborn as sns
sns.pairplot(dataset)


# In[ ]:


# sns.pairplot(dataset,hue="2urvived")
# This ran perfectly in my pc but here it shows that one hot ncoding is required for this to run


# In[ ]:


x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.33)


# In[ ]:


reg=linear_model.LogisticRegression(C=0.5)
reg.fit(x_train,y_train)
y_predict=reg.predict(x_test)


# In[ ]:


print(y_predict)


# In[ ]:


accuracy_score(y_predict,y_test)


# In[ ]:


confusion_matrix(y_predict,y_test)

