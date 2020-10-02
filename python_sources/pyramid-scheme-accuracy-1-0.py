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


# In[ ]:


data=pd.read_csv("../input/pyramid_scheme.csv",sep=",")


# In[ ]:


display(data)


# In[ ]:


data.drop(data.columns[0],axis=1,inplace=True)


# In[ ]:


display(data)


# In[ ]:


data.rename(columns={data.columns[2]:"profit"},inplace=True)


# In[ ]:


display(data)


# In[ ]:


data.drop(data.columns[0],axis=1,inplace=True)


# In[ ]:


display(data)


# In[ ]:


data.drop(data.columns[2],axis=1,inplace=True)


# In[ ]:


display(data)


# In[ ]:


x=data.iloc[:,[0,1]].values
y=data.profit.values


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)


# In[ ]:


from sklearn.linear_model import LinearRegression
mul_lin_Regr=LinearRegression()
mul_lin_Regr.fit(x_train,y_train)
accuracy=mul_lin_Regr.score(x_test,y_test)


# In[ ]:


print("b0:",mul_lin_Regr.intercept_)
print("b1,b2:",mul_lin_Regr.coef_)
print("accuracy:",accuracy)


# In[ ]:


mul_lin_Regr.predict(np.array([[5,15],[2,13]]))

