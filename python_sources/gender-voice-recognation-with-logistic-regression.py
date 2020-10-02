#!/usr/bin/env python
# coding: utf-8

# # Introduction to Gender Voice Recognation with Logistic Regression
# 
# ## Index of Contents
# 
# * [Read Data and Check Features](#1)
# * [Adjustment of Label values (male = 1, female = 0)](#2)
# * [Data Normalization](#3)
# * [Split Operation for Train and Test Data](#4)
# * [Matrix creation function for initial weight values](#5)
# * [Sigmoid function declaration](#6)
# * [Forward and Backward Propogation](#7)
# * [Updating Parameters](#8)
# * [Prediction with Test Data](#9)
# * [Logistic Regression Implementation](#10)
# * [Logistic Regression with sklearn](#11)

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# <a id="1"></a> 
# **Read Data and Check Features**

# In[ ]:


data = pd.read_csv("../input/voice.csv")


# In[ ]:


data.head(10)


# In[ ]:


# Get some information about our data
data.info()


# <a id="2"></a> 
# ***Adjustment of Label values (male = 1, female = 0***
# * After getting information about data we'll call male as 1 and female as 0***

# In[ ]:


data.label = [1 if each == "male" else 0 for each in data.label]


# In[ ]:


data.info() # now we have label as integer


# <a id="3"></a> 
# ***Data Normalization***

# In[ ]:


y = data.label.values # main results male or female
x_data = data.drop(["label"], axis = 1) # prediction components


# In[ ]:


x = (x_data - np.min(x_data))/(np.max(x_data)-np.min(x_data)).values # all data evaluated from 1 to 0


# <a id="4"></a>
# ***Split Operation for Train and Test Data***
# * Data is splitted for training and testing operations. We'll have %20 of data for test and %80 of data for train after split operation.

# In[ ]:


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)


# In[ ]:


# Data Shapes
print("x_train.shape : ", x_train.shape)
print("x_test.shape : ", x_test.shape)
print("y_train.shape : ", y_train.shape)
print("y_test.shape : ", y_test.shape)


# In[ ]:


# Transform features to rows (Transpose)
x_train = x_train.T
x_test = x_test.T
y_train = y_train.T
y_test = y_test.T


# <a id="5"></a> 
# ***Matrix creation function for initial weight values***

# In[ ]:


def initializeWeightsAndBias(dimension): # according to our data dimension will be 20
    w = np.full((dimension, 1), 0.01) 
    b = 0.0
    return w,b


# <a id="6"></a> 
# ***Sigmoid function declaration***

# In[ ]:


def sigmoid(z):
    y_head = (1 / (1 + np.exp(-z)))
    return y_head


# <a id="7"></a> 
# ***Forward and Backward Propogation***
# * Get z values from sigmoid function and calculate loss and cost. 

# In[ ]:


x_train.shape[1]


# In[ ]:


def forward_backward_propogation(w, b, x_train, y_train):
    
    #forward propogation
    z = np.dot(w.T, x_train) + b
    y_head = sigmoid(z)
    loss = -y_train * np.log(y_head) - (1 - y_train) * np.log(1 - y_head)
    cost = (np.sum(loss)) / x_train.shape[1] # x_train.shape[1] is for scaling
    
    #backward propogation
    derivative_weight = (np.dot(x_train, ((y_head - y_train).T))) / x_train.shape[1] # x_train.shape[1] is for scaling
    derivative_bias = np.sum(y_head - y_train) / x_train.shape[1] # x_train.shape[1] is for scaling
    gradients = {"derivative_weight" : derivative_weight, "derivative_bias" : derivative_bias}
    
    return cost, gradients


# <a id="8"></a> 
# ***Updating parameters***
# * Our purpose is find to optimum weight and bias values using derivative of these values.

# In[ ]:


def update(w, b, x_train, y_train, learningRate, numberOfIteration):
    cost_list = []
    cost_list2 = []
    index = []
    
    # updating(learning) parameters is number_of_iteration times
    for i in range(numberOfIteration):
        # make forward and backward propogation and find costs and gradients
        cost,gradients = forward_backward_propogation(w, b, x_train, y_train)
        cost_list.append(cost)
        #lets update
        w = w - learningRate * gradients["derivative_weight"]
        b = b - learningRate * gradients["derivative_bias"]
        if i % 10 == 0:
            cost_list2.append(cost)
            index.append(i)
            print("Cost after iteration %i: %f" %(i, cost))
            
    # we update(learn) paramters weights and bias
    parameters = {"weight" : w, "bias" : b}
    plt.plot(index, cost_list2)
    plt.xticks(index, rotation = 'vertical')
    plt.xlabel("Number of Iteration")
    plt.ylabel("Cost")
    plt.show()
    return parameters, gradients, cost_list


# <a id="9"></a> 
# ***Prediction with Test Data***
# * Prediction using test data which is splitted first.

# In[ ]:


def predict(w,b, x_test):
    # x_test is an input for forward propogation
    z = sigmoid(np.dot(w.T, x_test) + b)
    Y_prediction = np.zeros((1, x_test.shape[1]))
    # if z is bigger than 0.5, our prediction is Male (y_head = 1)
    # if z is smaller than 0.5, our prediction is Female (y_head = 0)
    for i in range(z.shape[1]):
        if z[0, i] <= 0.5:
            Y_prediction[0, i] = 0
        else:
            Y_prediction[0, i] = 1
    
    return Y_prediction


# <a id="10"></a> 
# ***Logistic Regression Implementation***

# In[ ]:


def logistic_regression(x_train, y_train, x_test, y_test, learningRate, numberOfIterations):
    dimension = x_train.shape[0] # that is 20 (feature count of data)
    w,b = initializeWeightsAndBias(dimension)
    parameters, gradients, cost_list = update(w, b, x_train, y_train, learningRate, numberOfIterations)
    y_prediction_test = predict(parameters["weight"], parameters["bias"], x_test)
    print("test accuracy : {} %.".format(100 - np.mean(np.abs(y_prediction_test - y_test)) * 100))


# In[ ]:


#Let's try our model and check costs and prediction results.
logistic_regression(x_train, y_train, x_test, y_test, learningRate = 1, numberOfIterations = 100)


# In[ ]:


logistic_regression(x_train, y_train, x_test, y_test, learningRate = 1, numberOfIterations = 1000)


# As you see above, when the iteration is increased, accuracy increasing too. 

# <a id="11"></a> 
# ***Logistic Regression with sklearn***
# * Logistic Regression Classification can be done with sklearn library. All codes which are written above correspond to the codes below.
# 

# In[ ]:


from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(x_train.T, y_train.T)
print("test accuracy {}".format(lr.score(x_test.T, y_test.T)))

