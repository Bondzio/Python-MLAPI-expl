#!/usr/bin/env python
# coding: utf-8

# ## Notebook Intro
# In this notebook, cancer type has been classified and predicted as **malignant or benign** based on Logistic Regression NN model.
# #### Dataset: [breastcancer](https://www.kaggle.com/jiuzhang/ninechapter-breastcancer)
# 
# 

# In[56]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
import os
#print(os.listdir("../input"))

path = "../input/breastCancer.csv"
df = pd.read_csv(path)
print(df.describe(),df.head(), df.columns)


# In[59]:


# diagnosis column is an object, we simply transform it to integer in order to make categorical datatype
df.info()


# In[57]:


df.drop(["id","Unnamed: 32"], axis=1, inplace = True)


# In[122]:


df.head(5)


# In[60]:


df.diagnosis = [1 if x == "M" else 0  for x in df.diagnosis]
print(df.info())


# In[61]:


#define x and y values
y = df.diagnosis.values
x_data = df.drop(["diagnosis"],axis=1) #unnormalized data

x_data.head()


# In[62]:


#normalization of values of features
x = (x_data - np.min(x_data))/(np.max(x_data)-np.min(x_data)).values
x.head()


# In[63]:


from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=42)


# In[64]:


x_train = x_train.T
x_test = x_test.T
y_train = y_train.T
y_test = y_test.T


# In[65]:


print("x_train: ",x_train.shape)
print("x_test: ",x_test.shape)
print("y_train: ",y_train.shape)
print("y_test: ",y_test.shape)


# In[105]:


# parameter initialize
# e.g. dimension = 30

def initialize_weights_and_bias(dimension):
    w = np.full((dimension,1),0.01)
    b = 0.0
    return w,b

# sigmoid function
def sigmoid(z):
    y_head = 1/(1+np.exp(-z))
    return y_head

# forward & back propagation
def forward_backward_propagation(w,b,x_train,y_train):
    # forward propagation
    z = np.dot(w.T,x_train) + b
    y_head = sigmoid(z)
    loss = -y_train*np.log(y_head)-(1-y_train)*np.log(1-y_head)
    cost = (np.sum(loss))/x_train.shape[1]      # x_train.shape[1]  is for scaling
    
    # backward propagation
    derivative_weight = (np.dot(x_train,((y_head-y_train).T)))/x_train.shape[1] # x_train.shape[1]  is for scaling
    derivative_bias = np.sum(y_head-y_train)/x_train.shape[1]                 # x_train.shape[1]  is for scaling
    gradients = {"derivative_weight": derivative_weight, "derivative_bias": derivative_bias}
    
    return cost,gradients

# Updating(learning) parameters
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
    plt.xlabel("Number of Iterarion")
    plt.ylabel("Cost")
    plt.show()
    return parameters, gradients, cost_list


# prediction
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

# logistic_regression
def logistic_regression(x_train, y_train, x_test, y_test, learning_rate ,  num_iterations):
    # initialize
    dimension =  x_train.shape[0]  # that is 30
    w,b = initialize_weights_and_bias(dimension)
    # do not change learning rate
    parameters, gradients, cost_list = update(w, b, x_train, y_train, learning_rate,num_iterations)
    
    y_prediction_test = predict(parameters["weight"],parameters["bias"],x_test)

    # Print test Errors
    print("test accuracy: {} %".format(100 - np.mean(np.abs(y_prediction_test - y_test)) * 100))


# In[120]:


logistic_regression(x_train, y_train, x_test, y_test,learning_rate = 4, num_iterations = 250)


# In[121]:


# sklearn with LR
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(x_train.T,y_train.T)
print("test accuracy {}".format(lr.score(x_test.T,y_test.T)))


# ## Conclusion
#  As a result, the forward & back propagation applied and sigmoid function used as an activation function on logistic regression classifier. Within appropriate learning rate and iteration, **about 97% accuracy level** can be seen on test data.
