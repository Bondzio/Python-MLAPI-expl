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


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


IceCream=pd.read_csv('../input/IceCreamData.csv')


# In[ ]:


IceCream


# In[ ]:


IceCream.head(5) #first 5 rows


# In[ ]:


IceCream.tail(5) #last 5 rows


# In[ ]:


IceCream.describe()


# In[ ]:


IceCream.info()


# In[ ]:


sns.jointplot(x='Temperature',y='Revenue',data=IceCream,color='gray')


# In[ ]:


#exp
sns.jointplot(x='Revenue',y='Temperature',data=IceCream,color='blue')


# In[ ]:


sns.pairplot(IceCream)


# In[ ]:


sns.lmplot(x='Revenue',y='Temperature',data=IceCream)


# In[ ]:


X =IceCream[['Temperature']]
y = IceCream['Revenue']


# In[ ]:


learning_rate = 0.05
max_itr = 100
precision = 0.001 
converged = False 
n = len(X) 


# In[ ]:


theta=[]
J = 1.0 / n * ((theta[0] + theta[1] * X - y) ** 2).sum()
itr = 0
while not converged:
    prediction = theta[0] + theta[1] * X
    
    grad0 = 1.0 / n * (prediction - y).sum()
    grad1 = 1.0 / n * ((prediction - y) * x).sum()
    
    theta[0] = theta[0] - learning_rate * grad0
    theta[1] = theta[1] - learning_rate * grad1
    
    error = 1.0 / n * ((theta[0] + theta[1] * x - y) ** 2).sum()
    plt.scatter(itr, error)
    if abs(J - error) < precision:
        converged = True
    if itr == max_itr:
        converged = True
    itr += 1
    J = error
    
    
plt.show()


# In[ ]:


prediction = T[0] + T[1] * X
plt.scatter(X,y)
plt.plot(X, prediction, 'r')
plt.show()


# In[ ]:


from sklearn.linear_model import LinearRegression
regressor =LinearRegression(fit_intercept=True)
regressor.fit(X_train,y_train)


# In[ ]:


print('Linear Model Coeff (m) =' , regressor.coef_)
print('Linear Model Coeff (b) =' , regressor.intercept_)


# In[ ]:


y_predict=regressor.predict(X_test)


# In[ ]:


y_predict


# In[ ]:


plt.scatter(X_train,y_train,color='blue')
plt.plot(X_train,regressor.predict(X_train),color='red')
plt.ylabel('Revenue [$]')
plt.xlabel('Temperatur [degC]')
plt.title('Revenue Generated vs. Temperature @Ice Cream Stand (Training)')


# In[ ]:


plt.scatter(X_test,y_test,color='blue')
plt.plot(X_test,regressor.predict(X_test),color='red')
plt.ylabel('Revenue [$]')
plt.xlabel('Temperatur [degC]')
plt.title('Revenue Generated vs. Temperature @Ice Cream Stand (Training)')


# In[ ]:


#Challenge
print('---------0---------')
Temp = -0
Revenue = regressor.predict(Temp)
print(Revenue)
print('--------35----------')
Temp = 35
Revenue = regressor.predict(Temp)
print(Revenue)
print('--------55----------')
Temp = 55
Revenue = regressor.predict(Temp)
print(Revenue)

