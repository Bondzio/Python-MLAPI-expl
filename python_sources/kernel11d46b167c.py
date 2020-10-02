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


df = pd.read_csv('../input/salary-data-simple-linear-regression/Salary_Data.csv')


# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


df.sample(5)


# In[ ]:


df.info()


# In[ ]:


X = df.iloc[:,:-1]   # X = df['YearsExperience']
y = df.iloc[:,-1]    # y = df['Salary']


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)


# In[ ]:


from sklearn.linear_model import LinearRegression


# In[ ]:


reg = LinearRegression()


# In[ ]:


reg.fit(X_train,y_train)


# In[ ]:


pred = reg.predict(X_test)


# In[ ]:


plt.scatter(X_train,y_train,color='red')
plt.plot(X_test,pred,color='green')
plt.show()


# In[ ]:




