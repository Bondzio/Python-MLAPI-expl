#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from matplotlib import pyplot as plt
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


heart = pd.read_csv("../input/heart.csv")


# Attribute Information: 
# > 1. age 
# > 2. sex 
# > 3. chest pain type (4 values) 
# > 4. resting blood pressure 
# > 5. serum cholestoral in mg/dl 
# > 6. fasting blood sugar > 120 mg/dl
# > 7. resting electrocardiographic results (values 0,1,2)
# > 8. maximum heart rate achieved 
# > 9. exercise induced angina 
# > 10. oldpeak = ST depression induced by exercise relative to rest 
# > 11. the slope of the peak exercise ST segment 
# > 12. number of major vessels (0-3) colored by flourosopy 
# > 13. thal: 3 = normal; 6 = fixed defect; 7 = reversable defect

# In[ ]:


heart.info()


# In[ ]:


heart.describe()


# In[ ]:


heart.head()


# In[ ]:


y=heart.sex.values
x=heart.drop(["sex"],axis=1)


# In[ ]:


x = (x - np.min(x))/(np.max(x)-np.min(x)).values # normalizition


# In[ ]:


#train_and_test_data
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)


# In[ ]:


x_train=x_train.T
y_train=y_train.T
x_test=x_test.T
y_test=y_test.T


# In[ ]:


#initializing parameters and sigmoid function
def initialize_weights_and_bias(dimension):
    w=np.full((dimension,1),0.01)
    b=0.0
    return w,b

def sigmoid(z):
    y_head=1/(1+np.exp(-z))
    return y_head


# In[ ]:


#forward and backward propogation
def forward_backward_propogation(w,b,x_train,y_train):
    #forward
    z=np.dot(w.T,x_train)+b
    y_head=sigmoid(z)
    loss=y_train*np.log(y_head)-(1-y_train)*np.log(1-y_head)
    cost=(np.sum(loss))/x_train.shape[1]
    #backward
    derivative_weight=(np.dot(x_train,((y_head-y_train).T)))/x_train.shape[1]
    derivative_bias=np.sum(y_head-y_train)/x_train.shape[1]
    gradients={"derivative_weight": derivative_weight, "derivative_bias": derivative_bias}
    return cost, gradients


# In[ ]:


#update parameters
def update(w,b,x_train,y_train,learning_rate,number_of_iteration):
    cost_list=[]
    cost_list2=[]
    index=[]
    #updating(learning) parameters is number of iteration times
    for i in range(number_of_iteration):
        #make forward and backward propogation and find cost,gradients
        cost,gradients=forward_backward_propogation(w,b,x_train,y_train)
        cost_list.append(cost)
        w=w-learning_rate*gradients["derivative_weight"]
        b=b-learning_rate*gradients["derivative_bias"]
        if i%10==0:
            cost_list2.append(cost)
            index.append(i)
            print("cost after iteration %i : %f" %(i,cost))
    parameters={"weight":w,"bias":b}        
    plt.plot(index,cost_list2)
    plt.xticks(index,rotation="vertical")
    plt.xlabel("Number of Iteration")
    plt.ylabel("Cost")
    plt.show()
    return parameters,gradients,cost_list


# In[ ]:


#parameters
def predict(w,b,x_test):
    #x_test is a input for forward propogation
    z=sigmoid(np.dot(w.T,x_test)+b)
    y_prediction=np.zeros((1,x_test.shape[1]))
    #if z>0.5, our prediction is one
    #if z<0.5, our prediction is zero
    for i in range(z.shape[1]):
        if z[0,i]<=0.5 :
            y_prediction[0,i]=0
        else:
            y_prediction[0,i]=1
    return y_prediction


# In[ ]:


#implementing logistic regression
def logistic_regression(x_train,y_train,x_test,y_test,learning_rate,number_of_iteration):
    #initialize
    dimension=x_train.shape[0]
    w,b= initialize_weights_and_bias(dimension)
    parameters,gradients,cost_list=update(w,b,x_train,y_train,learning_rate,number_of_iteration)
    y_prediction_test=predict(parameters["weight"],parameters["bias"],x_test)
    y_prediction_train=predict(parameters["weight"],parameters["bias"],x_train)
    print("train accuracy: {} %".format(100-np.mean(np.abs(y_prediction_train-y_train))*100))
    print("test accuracy: {} %".format(100-np.mean(np.abs(y_prediction_test-y_test))*100))
    


# In[ ]:


logistic_regression(x_train,y_train,x_test,y_test,learning_rate=0.1,number_of_iteration=10000)


# In[ ]:


from sklearn.linear_model import LogisticRegression
lr=LogisticRegression()
lr.fit(x_train.T,y_train.T)


# In[ ]:


lr.score(x_test.T,y_test.T)


# In[ ]:


lr.score(x_train.T,y_train.T)


# 
# You can make them all or you can just write it
# And Then I know this accuarcy is very low.But it does not matter.Because this is a exercise.

# In[ ]:


from sklearn import linear_model
logreg = linear_model.LogisticRegression(random_state = 42,max_iter= 10000)
print("test accuracy: {} ".format(logreg.fit(x_train.T, y_train.T).score(x_test.T, y_test.T)))
print("train accuracy: {} ".format(logreg.fit(x_train.T, y_train.T).score(x_train.T, y_train.T)))

#this section is a summary of the above work

