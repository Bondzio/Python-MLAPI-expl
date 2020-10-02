#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.linear_model import Lasso #gain access to the functions and variables to the module Lasso from sklearn library's linear_model feature
model = Lasso(alpha=0.1) #build the model with alpha = 0.3
X_train = [[-1],[0],[1]] #define training x 
Y_train = [-1,0,1] #define training y
model.fit(X_train,Y_train) #fit the lasso model of training x and training y
print(model.intercept_) #output is the intercept, which is the beta0 in the formula: y=beta1*x+beta0
print(model.coef_) #output is the coefficient, which is the beta1 in the formula: y=beta1*x+beta0
model.predict([[3]]) #testing x=3; output is prediction


# In[2]:


#Alternative way of calling the function

from sklearn import linear_model 
model = linear_model.Lasso(alpha=0.1) 
X_train = [[-1],[0],[1]]  
Y_train = [-1,0,1] 
model.fit(X_train, Y_train) 
print(model.intercept_) 
print(model.coef_) 
model.predict([[0]]) 


# In[3]:


import matplotlib.pyplot as plt
plt.scatter(X_train,Y_train)
plt.plot(X_train, model.coef_*X_train + model.intercept_, linestyle='--')


# In[4]:


#The following reiterates the first example, but adding a second feature.

from sklearn.linear_model import Lasso 
model = Lasso(alpha=0.1) 
X_train = [[3,-1],[0,0],[1,1]] 
Y_train = [-1,0,1] 
model.fit(X_train,Y_train) 
print(model.intercept_) 
print(model.coef_) 
model.predict([[0,1]]) 

