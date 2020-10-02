#!/usr/bin/env python
# coding: utf-8

# In[5]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Load Dataset 
credit_data=pd.read_csv('../input/creditcard.csv')

# List columns
list(credit_data)

# Any results you write to the current directory are saved as output.


# In[17]:


print(credit_data['Class'].value_counts())


# In[ ]:


list(credit_data)


# In[6]:


from sklearn.model_selection import train_test_split


# In[7]:


x=credit_data.iloc[:, :-1]
y=credit_data.iloc[:,-1]


# In[8]:


X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=.33,random_state =42)


# In[13]:


from sklearn.naive_bayes import GaussianNB
model = GaussianNB()


# In[15]:


model.fit(X_train,y_train)


# In[16]:


print(model.score(X_test,y_test))


# In[2]:


from sklearn.linear_model import LogisticRegression


# In[9]:


logreg = LogisticRegression()
logreg.fit(X_train, y_train)


# In[19]:


y_pred = logreg.predict(X_test)
print('Accuracy of logistic regression classifier on test set:',logreg.score(X_test, y_test))

