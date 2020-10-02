#!/usr/bin/env python
# coding: utf-8

# data source : https://www.kaggle.com/sammy123/lower-back-pain-symptoms-dataset/data#

# In[ ]:




import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # data visualization


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


data = pd.read_csv("/kaggle/input/lower-back-pain-symptoms-dataset/Dataset_spine.csv")
print(data.info())


# As you can see my labels are ordered -normal= 1, abnormal= 0-. 

# In[ ]:


data.dropna(how="any", inplace = True)  # Delete useless raw
data.drop(["Unnamed: 13"], axis = 1, inplace = True)
data.Class_att = [1 if each == "Normal" else 0 for each in data.Class_att]


result = data.Class_att.values
features_data = data.drop(["Class_att"], axis = 1)
features_data


# # **NORMALIZATION**
# Formula = (x -min(x))/(max(x)-min(x)

# In[ ]:


features = (features_data - np.min(features_data))/(np.max(features_data)-np.min(features_data)).values
features


# # **TRAIN-TEST SPLIT**
# Train Test Split data==> 80% of data set for Train, 20% of data set for Test

# In[ ]:


from sklearn.model_selection import train_test_split
features_train, features_test, result_train, result_test = train_test_split(features, result, test_size = 2, random_state = 42)


features_train = features_train.T
features_test = features_test.T
result_train = result_train.T
result_test = result_test.T

print("Changed of Features and Values place.")


print("features_train: ", features_train.shape)
print("features_test ", features_test.shape)
print("result_train: ", result_train.shape)
print("result_test: ", result_test.shape)


# # **PARAMETER INITALIZE AND SIGMOID FUNCTION**
# Time to start defining functions.First of all I need to initialize my weights and bias, then I will need a sigmoid function.
# 
# Sigmoid Function : f(x) = 1 / ( 1 + (e ^ -x) Initialize weight = 0.01 for each data Initialize bias = 0

# In[ ]:


def initialize_weights_bias(dimension): # dimension = 12
    weights = np.full((dimension,1), 0.01)
    bias = 0.0
    return weights, bias

def sigmoid(z):
    result_head = 1/(1+np.exp(-z))
    return result_head

print(sigmoid(0)) #test sigmoid(z)


# # **FORWARD AND BACKWARD PROPAGATION FUNCTION**
# z = bias + px1w1 + px2w2 + ... + pxn*wn loss function = -(1 - y) log(1- y_head) - y log(y_head) cost function = sum(loss value) / train dataset sample count

# In[ ]:


def forward_backward_propagation(weights, bias, features_train, result_train):
    #forward
    z = np.dot(weights.T,features_train) + bias
    result_head = sigmoid(z)
    
    loss = -result_train*np.log(result_head) - (1-result_train)*np.log(1-result_head)
    cost = (np.sum(loss))/features_train.shape[1]
    
    #backward
    derivative_weights = (np.dot(features_train,((result_head-result_train).T)))/features_train.shape[1]
    derivative_bias = np.sum(result_head-result_train)/features_train.shape[1]
    gradients = {"derivative_weights" : derivative_weights, "derivative_bias" : derivative_bias}
    return cost,gradients


# # **UPDATE**
# Update weights and bias with backward-forward propagation.

# In[ ]:


def update(weights, bias, features_train, result_train, learning_rate , number_of_iterations):
    cost_list = []
    cost_list2 = []
    index = []
    
    for i in range(number_of_iterations):
        cost,gradients = forward_backward_propagation(weights, bias, features_train, result_train)
        cost_list.append(cost)
        
        weights = weights - learning_rate*gradients["derivative_weights"]
        bias = bias - learning_rate*gradients["derivative_bias"]
        
        if i % 5 == 0:
            cost_list2.append(cost)
            index.append(i)
            print("Cost after iteration %i : %f" %(i,cost))
            
    parameters = {"weights" : weights,"bias" : bias}
    plt.plot(index,cost_list2)
    plt.xticks(index,rotation="vertical")
    plt.xlabel("Number Of Iterations")
    plt.ylabel("Cost")
    plt.show()
    return parameters, gradients, cost_list


# # **PREDICT**
# Predict function for testing purposes

# In[ ]:


def predict(weights,bias,features_test):
    z = sigmoid(np.dot(weights.T,features_test)+bias)
    result_prediction = np.zeros((1,features_test.shape[1]))
    
    for i in range(z.shape[1]):
        if z[0,i] <= 0.5:
            result_prediction[0,i] = 0
        else:
            result_prediction[0,i] = 1
            
    return result_prediction


# # **LOGISTIC REGRESSION**
# Main part. Put it all together.

# In[ ]:


def logistic_regression(features_train, result_train, features_test, result_test, learning_rate, number_of_iterations):
    
    dimension = features_train.shape[0]
    weights, bias = initialize_weights_bias(dimension)
    
    parameters, gradients, cost_list = update(weights, bias, features_train, result_train, learning_rate, number_of_iterations) 
    
    result_prediction_test = predict(parameters["weights"], parameters["bias"], features_test)
    
    print("Test accuracy: {}%".format(100-np.mean(np.abs(result_prediction_test - result_test))*100))

logistic_regression(features_train, result_train, features_test, result_test, learning_rate = 1, number_of_iterations = 100)  

