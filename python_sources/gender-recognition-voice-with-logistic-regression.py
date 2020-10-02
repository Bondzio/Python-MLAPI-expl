#!/usr/bin/env python
# coding: utf-8

# **INTRODUCTION**
# 1. Data adjustment
#     * Data Information
#     * Reading the Data
#     * Adjustment the Data
#     * Normalize the Data
# 2. Visualize the Data
# 3. Train and Test Data
# 4. Functions
#     * Functions that we write
#     * Sklearn Function
# 5. Conclusion
# 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns


# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# > **1. Data Adjustment**

# * **Data Information**

# * meanfreq: mean frequency (in kHz)
# * sd: standard deviation of frequency
# * median: median frequency (in kHz)
# * Q25: first quantile (in kHz)
# * Q75: third quantile (in kHz)
# * IQR: interquantile range (in kHz)
# * skew: skewness (see note in specprop description)
# * kurt: kurtosis (see note in specprop description)
# * sp.ent: spectral entropy
# * sfm: spectral flatness
# * mode: mode frequency
# * centroid: frequency centroid (see specprop)
# * peakf: peak frequency (frequency with highest energy)
# * meanfun: average of fundamental frequency measured across acoustic signal
# * minfun: minimum fundamental frequency measured across acoustic signal
# * maxfun: maximum fundamental frequency measured across acoustic signal
# * meandom: average of dominant frequency measured across acoustic signal
# * mindom: minimum of dominant frequency measured across acoustic signal
# * maxdom: maximum of dominant frequency measured across acoustic signal
# * dfrange: range of dominant frequency measured across acoustic signal
# * modindx: modulation index. Calculated as the accumulated absolute difference between adjacent measurements of fundamental frequencies divided by the frequency range
# * label: male or female
# 
# *Retrieved from https://www.kaggle.com/primaryobjects/voicegender*
# 
# 

# * **Reading the Data**

# In[ ]:


data = pd.read_csv("../input/voice.csv")


# * **Adjustment the Data**

# In[ ]:


data.label = [1 if each == "male" else 0 for each in data.label]


# In[ ]:


data.head(3)


# In[ ]:


data.tail(3)


# In[ ]:


x_data = data.drop(["label"],axis=1)
y = data.label.values


# * **Normalize the Data**

# In[ ]:


x = (x_data - np.min(x_data))/(np.max(x_data)-np.min(x_data)).values


# > **2. Visualize the Data**

# In[ ]:


f,ax = plt.subplots(figsize = (20,20))
plt.title("Heatmap of Human Voice", fontsize=20)
sns.set(font_scale=1.1)
sns.heatmap(x_data.corr(), linewidth = 5, linecolor = "white", annot = True, ax = ax)
plt.yticks(rotation='horizontal')
plt.show()


# There is a direct correlation between certain values

# > **3. Train and Test Data**

# In[ ]:


from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.2,random_state=42)


# In[ ]:


x_train=x_train.T
y_train=y_train.T
x_test=x_test.T
y_test=y_test.T


# > **4. Functions**

# * **Functions that we write**

# In[ ]:


def initialize_weights_and_bias(dimension):                                     # Initial values of Weights and Bias
    w = np.full((dimension,1),0.01)
    b = 0.0
    return w,b

def sigmoid(z):                                                                 # Sigmoid Functions
    y_head = 1/(1+ np.exp(-z))
    return y_head

def forward_backward_propagation(w,b,x_train,y_train):                         # Forward Backward Propagation
    # forward propagation
    z = np.dot(w.T,x_train) + b
    y_head = sigmoid(z)
    loss = -y_train*np.log(y_head)-(1-y_train)*np.log(1-y_head)
    cost = (np.sum(loss))/x_train.shape[1]                                      # x_train.shape[1]  is for scaling
    # backward propagation
    derivative_weight = (np.dot(x_train,((y_head-y_train).T)))/x_train.shape[1] # x_train.shape[1]  is for scaling
    derivative_bias = np.sum(y_head-y_train)/x_train.shape[1]                   # x_train.shape[1]  is for scaling
    gradients = {"derivative_weight": derivative_weight, "derivative_bias": derivative_bias}
    return cost,gradients

def update(w, b, x_train, y_train, learning_rate,number_of_iterarion):          # Update parameters
    cost_list = []
    cost_list2 = []
    index = []
    # updating(learning) parameters is number_of_iterarion times
    for i in range(number_of_iterarion):
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
    plt.subplots(figsize = (20,20))
    plt.plot(index,cost_list2)
    plt.xticks(index,rotation='vertical')
    plt.xlabel("Number of Iterarion")
    plt.ylabel("Cost")
    plt.show()
    return parameters, gradients, cost_list

def predict(w,b,x_test):                                                       # Value prediction
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

def logistic_regression(x_train, y_train, x_test, y_test, learning_rate ,  num_iterations):  # Logistic Regression Function
    # initialize
    dimension =  x_train.shape[0]  # that is 30
    w,b = initialize_weights_and_bias(dimension)
    # do not change learning rate
    parameters, gradients, cost_list = update(w, b, x_train, y_train, learning_rate,num_iterations)
    y_prediction_test = predict(parameters["weight"],parameters["bias"],x_test)
    # Print test Errors
    print("Functions that we write Test Accuracy: {} %".format(100 - np.mean(np.abs(y_prediction_test - y_test)) * 100))
  


# In[ ]:


logistic_regression(x_train, y_train, x_test, y_test,learning_rate = 1, num_iterations = 500)    


# * **Sklearn Function**

# In[ ]:


from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(x_train.T,y_train.T)
print("Sklearn Test Accuracy {} %".format(lr.score(x_test.T,y_test.T)))


# *To fix this error*

# In[ ]:


from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(solver='lbfgs') # Fix this error
lr.fit(x_train.T,y_train.T)
print("Sklearn Test Accuracy {} %".format(lr.score(x_test.T,y_test.T)))


# > **5. Conclusion**

# They became a very successful Logistic Regression System. Sklearn library was a bit more successful than our code.However, we can close this difference by increasing the number of iterations.
# 
# I published my first karnel. Sorry for my mistakes.
# 
# If you enjoy the content. Please don't forget to upvote.
