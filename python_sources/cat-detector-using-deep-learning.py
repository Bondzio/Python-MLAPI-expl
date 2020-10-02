#!/usr/bin/env python
# coding: utf-8

# The objective of this kernel is to build a cat detector by training a multilayer Neural Network on the dataset of 209 images. The validation set contains 50 images. The resolution of images is 64 by 64 RGB pixels which make a total of 12,288 input features.

# In[ ]:


import time
import numpy as np
import h5py
import matplotlib.pyplot as plt
import scipy
from PIL import Image
from scipy import ndimage
import skimage
np.random.seed(1)


# Fetching the traing and the test datasets...

# In[ ]:


def load_data():
    train_dataset = h5py.File('/kaggle/input/cat-images-dataset/train_catvnoncat.h5', "r")
    train_set_x_orig = np.array(train_dataset["train_set_x"][:]) 
    train_set_y_orig = np.array(train_dataset["train_set_y"][:]) 

    test_dataset = h5py.File('/kaggle/input/cat-images-dataset/test_catvnoncat.h5', "r")
    test_set_x_orig = np.array(test_dataset["test_set_x"][:]) 
    test_set_y_orig = np.array(test_dataset["test_set_y"][:]) 

    classes = np.array(test_dataset["list_classes"][:]) 
    
    train_set_y_orig = train_set_y_orig.reshape((1, train_set_y_orig.shape[0]))
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))
    
    return train_set_x_orig, train_set_y_orig, test_set_x_orig, test_set_y_orig, classes

x_train,y_train,x_test,y_test,classes = load_data()


# Some example of classes...

# In[ ]:


index = 19
plt.imshow(x_train[index])
print ("y = " + str(y_train[:,index]) + ", it's a '" + classes[np.squeeze(y_train[:,index])].decode("utf-8") +  "' picture.")


# In[ ]:


index = 21
plt.imshow(x_train[index])
print ("y = " + str(y_train[:,index]) + ", it's a '" + classes[np.squeeze(y_train[:,index])].decode("utf-8") +  "' picture.")


# Vectorizing and standardizing the datasets...

# In[ ]:


x_train = x_train.reshape(x_train.shape[0], -1).T
x_train = x_train / 255
x_test = x_test.reshape(x_test.shape[0], -1).T
x_test = x_test / 255
print('No. of features: ', x_train.shape[0] ,'\nNo. of training instances:' , x_train.shape[1])


# Initializing and forward propagation...

# In[ ]:


def initialize_parameters_deep(layer_dims):
    np.random.seed(1)
    parameters={}
    L=len(layer_dims)
    for l in range(1,L):
        parameters['W'+str(l)]=np.random.randn(layer_dims[l],layer_dims[l-1])/np.sqrt(layer_dims[l-1])
        parameters['b'+str(l)]=np.zeros((layer_dims[l],1))
    return parameters

def linear_forward(A,W,b):
    Z=W.dot(A)+b
    cache=(A,W,b)
    return Z,cache

def sigmoid(Z):
    A=1/(1+np.exp(-Z))
    cache=Z
    return A,cache

def relu(Z):
    A=np.maximum(0,Z)
    cache=Z
    return A,cache

def linear_activation_forward(A_prev,W,b,activation):
    if(activation=="sigmoid"):
        Z,linear_cache=linear_forward(A_prev,W,b)
        A,activation_cache=sigmoid(Z)
    elif(activation=="relu"):
        Z,linear_cache=linear_forward(A_prev,W,b)
        A,activation_cache=relu(Z)
    cache=(linear_cache,activation_cache)
    return A,cache

def L_model_forward(X,parameters):
    L=len(parameters)//2
    caches=[]
    A=X
    for l in range(1,L):
        A_prev=A
        A,cache=linear_activation_forward(A_prev,parameters['W'+str(l)],parameters['b'+str(l)],activation="relu")
        caches.append(cache)
    AL,cache=linear_activation_forward(A,parameters['W'+str(L)],parameters['b'+str(L)],activation="sigmoid")
    caches.append(cache)
    return AL,caches

def compute_cost(AL,Y):
    m=Y.shape[1]
    cost = (1./m) * (-np.dot(Y,np.log(AL).T) - np.dot(1-Y, np.log(1-AL).T))
    cost=np.squeeze(cost)
    return cost


# Calculating gradients and updating parameters...

# In[ ]:


def linear_backward(dZ,cache):
    A_prev,W,b=cache
    m=A_prev.shape[1]
    dW = 1./m * np.dot(dZ,A_prev.T)
    db = 1./m * np.sum(dZ, axis = 1, keepdims = True)
    dA_prev = np.dot(W.T,dZ)
    return dA_prev,dW,db

def relu_backward(dA, cache):
    Z = cache
    dZ = np.array(dA, copy=True)    
    dZ[Z <= 0] = 0
    assert (dZ.shape == Z.shape)
    return dZ

def sigmoid_backward(dA, cache):
    Z = cache
    s = 1/(1+np.exp(-Z))
    dZ = dA * s * (1-s)
    assert (dZ.shape == Z.shape)
    return dZ

def linear_activation_backward(dA,cache,activation):
    linear_cache, activation_cache = cache
    if activation == "relu":
        dZ = relu_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)
    elif activation == "sigmoid":
        dZ = sigmoid_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)
    return dA_prev, dW, db

def L_model_backward(AL, Y, caches):
    grads = {}
    L = len(caches) 
    m = AL.shape[1]
    Y = Y.reshape(AL.shape)
    dAL = - (np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))
    current_cache = caches[L-1]
    grads["dA" + str(L)], grads["dW" + str(L)], grads["db" + str(L)] = linear_activation_backward(dAL, current_cache, activation = "sigmoid")
    for l in reversed(range(L-1)):
        current_cache = caches[l]
        dA_prev_temp, dW_temp, db_temp = linear_activation_backward(grads["dA" + str(l + 2)], current_cache, activation = "relu")
        grads["dA" + str(l + 1)] = dA_prev_temp
        grads["dW" + str(l + 1)] = dW_temp
        grads["db" + str(l + 1)] = db_temp
    return grads

def update_parameters(parameters, grads, learning_rate):
    L = len(parameters) //2
    for l in range(L):
        parameters["W" + str(l+1)] = parameters["W" + str(l+1)] - learning_rate * grads["dW" + str(l+1)]
        parameters["b" + str(l+1)] = parameters["b" + str(l+1)] - learning_rate * grads["db" + str(l+1)]
    return parameters


# Building the optimization function...

# In[ ]:


def L_layer_model(X, Y, layers_dims, learning_rate = 0.0075, num_iterations = 3000, print_cost=False):#lr was 0.009
    np.random.seed(1)
    costs = []              
    parameters = initialize_parameters_deep(layers_dims)
    for i in range(0, num_iterations):
        AL, caches = L_model_forward(X, parameters)
        cost = compute_cost(AL, Y)
        grads = L_model_backward(AL, Y, caches)
        parameters = update_parameters(parameters, grads, learning_rate=learning_rate)
        if print_cost and i % 100 == 0:
            print ("Cost after %i iterations: %f" %(i, cost))
        if print_cost and i % 100 == 0:
            costs.append(cost)
    plt.plot(np.squeeze(costs))
    plt.ylabel('cost')
    plt.xlabel('iterations (per tens)')
    plt.title("Learning rate =" + str(learning_rate))
    plt.show()
    return parameters


# Defining the model's architecture, training the data, and plotting the learning curve...

# In[ ]:


layers_dims = [12288, 20, 7, 5, 1]
parameters = L_layer_model(x_train, y_train, layers_dims, num_iterations = 2500, print_cost = True)


# Making predictions and computing the accuracy on the training and the test datasets:

# In[ ]:


def predict(X, y, parameters):
    m = X.shape[1]
    n = len(parameters) // 2
    p = np.zeros((1,m))
    probas, caches = L_model_forward(X, parameters)
    for i in range(0, probas.shape[1]):
        if probas[0,i] > 0.5:
            p[0,i] = 1
        else:
            p[0,i] = 0
    print("Accuracy: "  + str(np.sum((p == y)/m)))
    return p

pred_train = predict(x_train, y_train, parameters)
pred_test = predict(x_test,y_test, parameters)

