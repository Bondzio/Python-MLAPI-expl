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


df=pd.read_csv('/kaggle/input/telco-paging-a-interface/Paging_Analysis_A_interface.csv')
df.head()


# In[ ]:


df1=df[['Success_Rate','Response','Failures']]
import seaborn as sns
sns.pairplot(df1)


# In[ ]:


X=df[['Response','Failures']]
X.head()


# In[ ]:


y=df[['Success_Rate']]
y.head()


# In[ ]:


from sklearn.preprocessing import StandardScaler
scale=StandardScaler()
X_trans=scale.fit_transform(X)
print(X_trans.shape)
print(X_trans.mean())
print(X_trans.std())


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test= train_test_split(X_trans,y,test_size=0.2, random_state=42)
print(X_train.shape)
print(y_test.shape)


# In[ ]:


from sklearn.linear_model import Ridge
model_r=Ridge().fit(X_train, y_train)
y_pred=model_r.predict(X_test)
y_pred


# In[ ]:


print('In Sample Score: ', model_r.score(X_train, y_train))
print('Out Sample Score: ', model_r.score(X_test, y_test))


# **Very bad model indeed, but no worry as we can explore always!**

# Now Let's improve our model by including polynomial feature

# In[ ]:


from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
X_poly_train=PolynomialFeatures(3).fit_transform(X_train)
X_poly_test=PolynomialFeatures(3).fit_transform(X_test)
model_lr=LinearRegression().fit(X_poly_train, y_train)
print('In Sample Score: ', model_lr.score(X_poly_train, y_train))
print('Out Sample Score: ', model_lr.score(X_poly_test, y_test))


# Congratulations! our model improved a lot & having no bias/variance problem as in sample and out sample r^2 score close to each other.
