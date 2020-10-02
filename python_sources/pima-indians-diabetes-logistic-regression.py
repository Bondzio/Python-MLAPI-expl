#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# # Introduction
# * Our aim is to predict whether a patient is diabetes or not, using the dataset. 

# In[ ]:


data = pd.read_csv("/kaggle/input/pima-indians-diabetes-database/diabetes.csv")
data.info()


# * Above, we can see 8 features(pregnancies, glucose, blood pressure, skin thickness, insulin, BMI, diabetes pedigree function, age) and the outcome which indicates patient's situation.

# In[ ]:


data.head()


# In[ ]:


y = data["Outcome"].values


# In[ ]:


# Preparing the dataset
x_data = data.drop(["Outcome"], axis = 1)
x_data.head()


# In[ ]:


# Normalization of dataset
x = (x_data - np.min(x_data)) / (np.max(x_data) - np.min(x_data))
x.head()


# # Train - Test Split
# * 80% of data set will be used for train, 20% is for test.

# In[ ]:


from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=42)

# For mathematical operations, transpose is applied.
x_train = x_train.T
x_test = x_test.T
y_train = y_train.T
y_test = y_test.T

print("x_train: ",x_train.shape)
print("x_test: ",x_test.shape)
print("y_train: ",y_train.shape)
print("y_test: ",y_test.shape)


# # Parameter Initializing and Sigmoid Function
# * We have 8 features, so we have dimension = 8
# * Sigmoid function = 1 / ( 1 + (e ^ -x)
# * Initial weights = 0.01, initial bias = 0

# In[ ]:


def initialize_weights_and_bias(dimension):
    
    w = np.full((dimension,1),0.01)
    b = 0.
    return w,b

def sigmoid(z):
    
    y_head = 1/(1 + np.exp(-z))
    return y_head


# # Forward and Backward Propagation
# ## Forward:
# * z = bias + px1w1 + px2w2 + ... + pxn*wn 
# * Calculate y_head = sigmoid(z)
# * Calculate loss function = -(1 - y) log(1- y_head) - y log(y_head)
# * Find cost function = sum(loss value) / train dataset sample count
# 
# ## Backward:
# * Take derivative of cost function with respect to weight and bias. 
# * Then multiply it with learning rate 
# * Update the weight and bias.

# In[ ]:


def forward_backward_propagation(w,b,x_train,y_train):
    # forward propagation
    z = np.dot(w.T, x_train) + b
    y_head = sigmoid(z)
    loss = -y_train*np.log(y_head)-(1-y_train)*np.log(1-y_head)
    cost = (np.sum(loss))/x_train.shape[1] # x_train.shape[1] is for scaling
        
    # backward propagation
    derivative_weight = (np.dot(x_train,((y_head - y_train).T)))/x_train.shape[1] # x_train.shape[1] is for scaling 
    derivative_bias = np.sum(y_head - y_train)/x_train.shape[1] # x_train.shape[1] is for scaling
    gradients = {"derivative_weight": derivative_weight, "derivative_bias": derivative_bias}
        
    return cost,gradients


# # Updating Parameters
# * Using the gradients, we update the weight and bias values. We can do that process as much as which is determined as number of iterations.

# In[ ]:


def update(w, b, x_train, y_train, learning_rate,number_of_iteration):
    cost_list = []
    cost_list2 = []
    index = []
    
    # updating(learning) parameters is number_of_iteration times
    for i in range(number_of_iteration):
        # make forward and backward propagation and find cost and gradients
        cost,gradients = forward_backward_propagation(w,b,x_train,y_train)
        cost_list.append(cost)
        # lets update
        w = w - learning_rate * gradients["derivative_weight"]
        b = b - learning_rate * gradients["derivative_bias"]
        if i % 10 == 0:
            cost_list2.append(cost)
            index.append(i)
            print ("Cost after iteration %i: %f" %(i, cost))
    # we update(learn) parameters weights and bias
    parameters = {"weight": w,"bias": b}
    plt.plot(index,cost_list2)
    plt.xticks(index,rotation='vertical')
    plt.xlabel("Number of Iteration")
    plt.ylabel("Cost")
    plt.show()
    return parameters, gradients, cost_list


# # Prediction

# In[ ]:


def predict(w,b,x_test):
    # x_test is a input for forward propagation
    z = sigmoid(np.dot(w.T,x_test)+b)
    Y_prediction = np.zeros((1,x_test.shape[1]))
    # if z is bigger than 0.5, our prediction is sign one (y_head=1),
    # if z is smaller than 0.5, our prediction is sign zero (y_head=0),
    for i in range(z.shape[1]):
        if z[0,i]<= 0.5:
            Y_prediction[0,i] = 0
        else:
            Y_prediction[0,i] = 1

    return Y_prediction


# # Logistic Regression
# * Let's test and find our accuracy.

# In[ ]:


def logistic_regression(x_train, y_train, x_test, y_test, learning_rate , num_iterations):
    # initialize
    dimension =  x_train.shape[0]  # that is 30
    w,b = initialize_weights_and_bias(dimension)
    # do not change learning rate
    parameters, gradients, cost_list = update(w, b, x_train, y_train, learning_rate, num_iterations)
    
    y_prediction_test = predict(parameters["weight"],parameters["bias"],x_test)

    # Print Test Errors
    print("test accuracy: {} %".format(100 - np.mean(np.abs(y_prediction_test - y_test)) * 100))
    
logistic_regression(x_train, y_train, x_test, y_test, learning_rate = 1, num_iterations = 300)


# # Logistic Regression with Sklearn

# In[ ]:


from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(solver = 'lbfgs')
lr.fit(x_train.T,y_train.T)
print("Test accuracy {}".format(lr.score(x_test.T,y_test.T)))

