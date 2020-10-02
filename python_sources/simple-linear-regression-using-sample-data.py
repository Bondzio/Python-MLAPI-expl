#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import pandas as pd
import pylab as pl
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


#Importing the dataset
df = pd.read_csv("../input/sample.csv")
df


# In[ ]:


plt.scatter(df["X"],df["Y"],color='red')


# In[ ]:


msk=np.random.rand(len(df))<0.8
train=df[msk]
test=df[~msk]


# In[ ]:


plt.scatter(train["X"],train["Y"],color='red')


# In[ ]:


from sklearn import linear_model
regr=linear_model.LinearRegression()
train_x=np.asanyarray(train[["X"]])
train_y=np.asanyarray(train[["Y"]])
regr.fit(train_x,train_y)

print("Coefficient: ",regr.coef_)
print("Intercept: ",regr.intercept_)


# In[ ]:


plt.scatter(train["X"],train["Y"],color='red')
plt.plot(train_x, regr.coef_[0][0]*train_x + regr.intercept_[0],'-b')


# In[ ]:


plt.scatter(test["X"],test["Y"],color='red')
plt.plot(train_x, regr.coef_[0][0]*train_x + regr.intercept_[0],'-b')


# In[ ]:


from sklearn.metrics import r2_score
test_x=np.asanyarray(test[["X"]])
test_y=np.asanyarray(test[["Y"]])

y_pred=regr.predict(test_x)

print("R2_score:%.2f" %r2_score(test_y,y_pred))
print("Mean absolute error: %.2f" % np.mean(np.absolute(y_pred- test_y)))


# 

# **Improving the model by gradient descent**

# In[ ]:


x=df["X"]
y=df["Y"]


# In[ ]:


m=0
c=0

L=0.0001      #The Learning Rate
epochs=1000   #The number of iterations to perform gradient descent

n=float(len(x))   #Number of elements in x

#Performing Gradient Desecent
for i in range(epochs):
    y_pred = m*x + c    #The current predicted value of y
    D_m=(-2/n) * sum(x*(y-y_pred))  #Derivative wrt m
    D_c=(-2/n) * sum(y-y_pred)      #Derivative wrt c
    m=m-L*D_m   #Update m
    c=c-L*D_c   #Update c
print(m,c)    


# In[ ]:


#Making Prediction
y_pred=m*x + c
plt.scatter(x,y)
plt.plot([min(x),max(x)],[min(y_pred),max(y_pred)],color='red')  #show
plt.show() 


# In[ ]:


print("r2_score:%.2f" %r2_score(y,y_pred))


# In[ ]:




