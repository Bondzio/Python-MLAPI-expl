#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


df = pd.read_csv("/kaggle/input/graduate-admissions/Admission_Predict_Ver1.1.csv")


# In[ ]:


df.head()


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
fig, ax = plt.subplots(figsize=(10,10))         
sns.heatmap(df.corr(), annot= True)
plt.show()


# In[ ]:


df.corr()


# In[ ]:


df.info()


# In[ ]:


df.columns


# In[ ]:


# Loading the  target values as Chance of Admit
df["Chance of Admit "].plot()


# In[ ]:


# Based of the above estimation
df.info()


# In[ ]:


# Creating the base line model using simple Linear regression
from sklearn.linear_model  import LinearRegression
linear = LinearRegression()
X = df.drop("Chance of Admit ", axis= 1)
y = df["Chance of Admit "]
print(X.shape)
print(y.shape)


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.8, random_state  = 1)
linear.fit(X_train, y_train)


# In[ ]:


linear.coef_


# In[ ]:


linear.intercept_


# In[ ]:


y_pred = linear.predict(X_test)


# In[ ]:


from sklearn.metrics import r2_score
print("Baseline R2 score is ", r2_score(y_test,y_pred))


# In[ ]:


# The baseline scrore is by using simple sklearn linear regression with 0.2 test set


# In[ ]:


# Again using the Linear model with more train size 
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.85, random_state  = 1)
linear.fit(X_train, y_train)


# In[ ]:


new_y_pred = linear.predict(X_test)


# In[ ]:


print("Revised Linear Regression Score  is ", r2_score(y_test,new_y_pred, ))


# In[ ]:




