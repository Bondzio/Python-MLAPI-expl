#!/usr/bin/env python
# coding: utf-8

# In[12]:


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


# In[13]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


df = pd.read_csv("../input/HR.csv")
df.head(5)


# In[14]:


#data analyzing
import seaborn as sns
sns.countplot(x='left', hue='time_spend_company', data=df)


# In[15]:


sns.countplot(x='left', hue='salary', data=df)


# In[16]:


#data wrangling
sal=pd.get_dummies(df['salary'],drop_first=True)
sal.head(5)


# In[17]:


df=pd.concat([df,sal],axis=1)
df.head(5)


# In[18]:


#dropping unwanted columns
df.drop(['Department','salary'],axis=1,inplace=True)
df.head(5)


# In[19]:


#assining values to dependent(y) and independent variables(x)
X=df.drop("left",axis=1)
y=df["left"]


# In[22]:


#training and testing the data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)


# In[23]:


from sklearn.linear_model import LogisticRegression
logmodel=LogisticRegression()
logmodel.fit(X_train,y_train)
predictions=logmodel.predict(X_test)


# In[24]:


from sklearn.metrics import confusion_matrix
confusion_matrix(y_test,predictions)


# In[25]:


from sklearn.metrics import accuracy_score
accuracy_score(y_test,predictions)

