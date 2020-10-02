#!/usr/bin/env python
# coding: utf-8

# As i am still in the learning phase i do not have that much sode after the training datase

# The code in this note book has been successfully run on my machine and then uploaded

# In[ ]:


from sklearn import linear_model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


# In[ ]:


dataset=pd.read_csv("insurance.csv")
dataset.head()


# In[ ]:


dataset['sex']=dataset['sex'].replace('female',0)
dataset['sex']=dataset['sex'].replace('male',1)
dataset['smoker']=dataset['smoker'].replace('yes',1)
dataset['smoker']=dataset['smoker'].replace('no',0)
dataset['region'].unique()


# In[ ]:


dataset.head()


# In[ ]:


dataset['region']=dataset['region'].replace('southwest',0)
dataset['region']=dataset['region'].replace('southeast',1)
dataset['region']=dataset['region'].replace('northwest',2)
dataset['region']=dataset['region'].replace('northeast',3)


# In[ ]:


dataset.head()


# In[ ]:


x=dataset.drop('charges',axis=1)
y=dataset['charges']
x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=10)
x_train.head()


# In[ ]:


reg=linear_model.LinearRegression()
reg.fit(x_train,y_train)
reg.score(x_test,y_test)
y_predict=reg.predict(x_test)
print(y_test.head())
print(y_predict)
reg.coef_
reg.intercept_


# In[ ]:


# plotting the plots on basis of few colums
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(x_test['age'],y_test,'r')
ax2.plot(x_test['age'],y_predict,'b')
plt.show()

