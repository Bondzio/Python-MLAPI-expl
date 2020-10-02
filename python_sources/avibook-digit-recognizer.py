#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2


# In[ ]:


# reading the training and testing dataset from csv files
train = pd.read_csv("../input/train.csv")
test = pd.read_csv("../input/test.csv")


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


# labels of training features
train_y = train["label"]


# In[ ]:


train_y.head()


# In[ ]:


# finding the training freature
train_x = train.iloc[:,1:785]


# In[ ]:


train_x.head()


# In[ ]:


# Explore the dataset
m_train = train.shape[0]
num_px = test.shape[1]
m_test = test.shape[0]
print("Number of training examples: " + str(m_train))
print("Number of testing examples: "+ str(m_test))
print("Size of each image: ("+ str(int(np.sqrt(num_px))) + ", " + str(int(np.sqrt(num_px)))+")")
print("Shape of training features: " + str(train.shape))
print("Shape of testing features: " + str(test.shape))
print("Shape of labels of tarining features: " + str(train_y.shape))


# In[ ]:


# Examples of digits
index = 100
plt.figure(1)
plt.imshow(train_x.iloc[index,:].reshape(28,28), cmap = 'gray')
print("Corresponding label = " + str(train_y[index]))


# In[ ]:


# Standardize data to have feature values between 0 and 1
tarin_x = train_x/255
test_x = test/255

print("train_x's shape: "+str(train_x.shape))
print("test_x's shape: "+str(test_x.shape))


# In[ ]:


# initialize parameters
def initialize_parameters(n_x,n_h,n_y):
    """
    inputs:
    n_x -- size of input layer
    n_h -- size of hidden layer
    n_y -- size of output layer
    
    outputs:
    parameters
    """
    # W1 : weight of matrix of shape (n_h,n_x)
    W1 = np.random.randn(n_h,n_x) * 0.01
    # b1 : bias vector of shape (n_h,1)
    b1 = np.zeros((n_h,1))
    # W2 : weight of matrix of shape (n_y,n_h)
    W2 = np.random.randn(n_y,n_h) * 0.01
    # b2 : bias vector of shape (n_y,1)
    b2 = np.zeros((n_y,1))
    
    parameters = {"W1" : W1,
                 "b1" : b1,
                 "W2" : W2,
                 "b2" : b2}
    
    return parameters


# In[ ]:


# initial parameters
parametrs = initialize_parameters(2,2,1)
print("W1 = "+str(parametrs["W1"]))
print("b1 = "+str(parametrs["b1"]))
print("W2 = "+str(parametrs["W2"]))
print("b2 = "+str(parametrs["b2"]))


# In[ ]:


def initialize_parameters_deep(layer_dims):
    """
    inputs:
    layer_dims: list of the dimention of each layer
    
    outputs:
    parameters: containing the weight and bias parameters of deep neural networks
    Wl : weight matrix of shape (layer_dims[l],layer_dims[l-1])
    bl : bias vector of shape (layer_dims[l],1)
    """
    parameters = {}
    # number of layers in the network
    L = len(layer_dims)
    
    for l in range(1,L):
        parameters["W" + str(l)] = np.random.randn(layer_dims[l],layer_dims[l-1]) * 0.001
        parameters["b" + str(l)] = np.zeros((layer_dims[l],1))
        
    return parameters   


# In[ ]:


# initial parameters of deep neural nets
parametrs = initialize_parameters_deep([6,4,3])
print("W1 = "+str(parametrs["W1"]))
print("b1 = "+str(parametrs["b1"]))
print("W2 = "+str(parametrs["W2"]))
print("b2 = "+str(parametrs["b2"]))


# In[ ]:


# forward propagation Module
# building the linear part of NN
def linear_forward(A,W,b):
    '''
    inputs:
    A --- Activation from previous layer
    W,b --- parameters of NN
    
    outputs:
    Z --- linear equation or input for the activation layer
    cache --- stored A, W and b
    '''
    Z = np.matmul(W,A) + b
    cache = (A, W, b)
    return Z, cache


# In[ ]:


# sigmoid function 
def sigmoid(Z):
    '''
    Z : input value, vector or matrix
    
    A : sigmoid of Z
    '''
    A = 1/(1+np.exp(-Z))
    cache = Z
    return A, cache


# In[ ]:


# derivative of sigmoid function
def sigmoid_backward(dA, activation_cache):
    #print("dA: "+str(dA))
    Z = activation_cache
    #print("Z: "+str(Z))
    A,cache = sigmoid(Z)
    dSig = np.multiply(A, (1-A))
    #print("dSig: "+str(dSig))
    dZ = np.multiply(dA,dSig)
    #print("dZ: "+str(dZ))
    return dZ


# def softmax(Z):
#     exps = np.exp(Z)
#     A = exps/np.sum(exps)
#     cache = Z
#     return A, cache

# def softmax_backward(dA, activation_cache):
#     Z = activation_cache
#     A,cache = softmax(Z)
#     dSoft = np.multiply(A,(1-A))
#     dZ = np.multiply(dA,dSoft)
#     return dZ

# In[ ]:


# ReLU function
def relu(Z):
    A = Z * (Z>0)
    cache = Z
    return A, cache


# In[ ]:


# Derivative of ReLU function
def relu_backward(dA, activation_cache):
    Z = activation_cache
    dRelu = (Z > 0)
    dRelu = dRelu.astype(float)
    dZ = np.multiply(dA,dRelu)
    return dZ


# In[ ]:


# linear activation function
def linear_activation_forward(A_prev, W, b, activation):
    '''
    inputs: 
    A_prev, W, b --- As defined in the linear_forward function
    activation  --- activation to be used
    
    outputs:
    A -- output of the activation function
    cache -- containing linear cache and activation cache which will use in backpropagation 
            calulation         
   '''
    if activation == "sigmoid":
        Z, linear_cache = linear_forward(A_prev,W,b)
        #print("Z: "+str(Z))
        A, activation_cache = sigmoid(Z)
    
    elif activation == "relu":
        Z, linear_cache = linear_forward(A_prev,W,b)
        A, activation_cache = relu(Z)
        
    cache = (linear_cache, activation_cache)
    
    return A, cache


# In[ ]:


# L-layer linear activation function
def L_model_forward(X, parameters):
    '''
    X --- data
    parameters --- output of initialize_parameters_deep()
    
    AL -- last post activation value
    '''
    caches = []
    A = X
    L = len(parameters)//2
    # implimentation of [Linear ---> RELU * (L-1)]
    for l in range(1,L):
        A_prev = A
        A, cache = linear_activation_forward(A_prev, parameters["W" + str(l)], parameters["b" + str(l)],"relu")
        caches.append(cache)
    # implimentation of Linear ---> sigmoid
    AL, cache = linear_activation_forward(A, parameters["W" + str(L)], parameters["b" + str(L)], "sigmoid")
    caches.append(cache)
    
    return AL, caches
    


# In[ ]:


def one_hot_matrix(Y, n_y):
    Y = np.vstack(Y)
    Y_ = np.zeros((Y.shape[0],n_y))
    Y_[np.arange(Y.shape[0]),Y.T] = 1
    Y_ = Y_.T
    return Y_
    


# In[ ]:


Y = one_hot_matrix(train_y,10)


# # computing the cost function
# def compute_cost1(AL, Y):
#     '''
#     AL --- probability vector corresponding to label prediction
#     Y --- correct label vector
#     
#     cost --- entropy cost
#     '''
#     m = Y.shape[0]
#     #print(AL[1,:])
#     cost = 0
#     for i in range(0,10):
#         cost = cost-np.sum(np.multiply(np.log(AL[i,:]),(Y==i)) + np.multiply(np.log(1-AL[i,:]),(1-(Y==i))))/m
#     cost = np.squeeze(cost)
#     return cost

# In[ ]:


def compute_cost(AL, Y):
    m = Y.shape[1]
    cost = -np.sum(np.multiply(np.log(AL),Y)+np.multiply(np.log(1-AL),(1-Y)))/m
    return cost


# In[ ]:


# Backward propagation module
# Implimentation of backward propagation for single layer
def linear_backward(dZ, cache):
    A_prev, W, b = cache
    m = A_prev.shape[1]
    dW = np.matmul(dZ,A_prev.T)/m
    db = np.sum(dZ, axis=1,keepdims = True)/m
    dA_prev = np.matmul(W.T,dZ)
    return dA_prev, dW, db
    


# In[ ]:


# linear activation backward
def linear_activation_backward(dA, cache, activation):
    linear_cache, activation_cache = cache
    if activation == "relu":
        dZ = relu_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)
        
    if activation == "sigmoid":
        dZ = sigmoid_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)
    
    return dA_prev, dW, db


# In[ ]:


#implimentation of L layer backward activation function
def L_model_backward(AL, Y, caches):
    grads = {}
    L = len(caches)
    m = AL.shape[1]
    Y = Y.reshape(AL.shape)
    dAL = -(np.divide(Y,AL)-np.divide(1-Y,1-AL))
    current_cache = caches[L-1]
    grads["dA"+str(L)], grads["dW"+str(L)],grads["db"+str(L)] = linear_activation_backward(dAL, current_cache, "sigmoid")
    
    for l in reversed(range(L-1)):
        current_cache = caches[l]
        dA_prev_temp, dW_temp, db_temp = linear_activation_backward(grads["dA"+str(l+2)],current_cache,"relu")
        grads["dA"+str(l+1)] = dA_prev_temp
        grads["dW" + str(l+1)] = dW_temp
        grads["db" + str(l+1)] = db_temp
    return grads


# In[ ]:


# implimentation for parameter updation
def update_parameters(parameters, grads, learning_rate):
    L = len(parameters)//2
    for l in range(L):
        parameters["W"+str(l+1)] = parameters["W"+str(l+1)] - learning_rate * grads["dW"+str(l+1)]
        parameters["b"+str(l+1)] = parameters["b"+str(l+1)] - learning_rate * grads["db"+str(l+1)]
    return parameters


# # Two layer model
# def two_layer_model(X, Y, layers_dims, learning_rate = 0.0001, num_iteration = 3000):
#     costs = []
#     grads = {}
#     m = X.shape[0]
#     (n_x,n_h,n_y) = layers_dims
#     parameters = initialize_parameters(n_x, n_h, n_y)
#     W1 = parameters["W1"]
#     b1 = parameters["b1"]
#     W2 = parameters["W2"]
#     b2 = parameters["b2"]
#     Y_ = Y
#     Y = one_hot_matrix(Y,n_y)
#     
#     for i in range(0,num_iteration):
#         A1, cache1 = linear_activation_forward(X, W1, b1, "relu")
#         A2, cache2 = linear_activation_forward(A1, W2, b2, "sigmoid")
#         cost = compute_cost(A2, Y)
#         #Y = one_hot_matrix(Y_,n_y)
#         #cost1 = compute_cost1(A2,Y_)
#         #print(cost1,cost)
#         # initializing backward propagation
#         #print("cost1: "+str(cost1))
#         #print("cost: "+str(cost))
#         #print("A1: "+str(A1))
#         #print("A2: "+str(A2))
#         #print(cost1)
#         dA2 = -(np.divide(Y,A2) - np.divide((1-Y),(1-A2)))
#         #dA2 = A2 - Y
#         #print("dA2: "+str(dA2))
#         #print("cache2 : "+str(cache2))
#         dA1, dW2, db2 = linear_activation_backward(dA2, cache2, "sigmoid")
#         dA0, dW1, db1 = linear_activation_backward(dA1, cache1, "relu")
#         
#         grads["dW1"] = dW1
#         grads["db1"] = db1
#         grads["dW2"] = dW2
#         grads["db2"] = db2
#         parameters = update_parameters(parameters, grads, learning_rate)
#         
#         W1 = parameters["W1"]
#         b1 = parameters["b1"]
#         W2 = parameters["W2"]
#         b2 = parameters["b2"]
#         if i % 100 == 0:
#             print("Cost after iteration {}: {}".format(i,np.squeeze(cost)))
#         if i%100 == 0:
#             costs.append(cost)
#             
#     # plot the cost
#     plt.figure(6)
#     plt.plot(np.squeeze(costs))
#     plt.ylabel('cost')
#     plt.xlabel('iterations (per tens)')
#     plt.title("Learning rate = "+str(learning_rate))
#     plt.show()
#     return parameters

# In[ ]:


# implementation of L layer model
def L_layer_model(X, Y, layers_dims, learning_rate, num_iterations, print_cost):
    costs = []
    # parameters initialization
    parameters = initialize_parameters_deep(layers_dims)
    # one hot matrix conversion
    Y = one_hot_matrix(Y,layers_dims[-1])
    # gradient descent
    for i in range(0, num_iterations):
        # forward propagation
        AL, caches = L_model_forward(X, parameters)
        # cost computation
        cost = compute_cost(AL, Y)
        # backward propagation
        grads = L_model_backward(AL, Y, caches)
        # parameter updation
        parameters = update_parameters(parameters, grads, learning_rate)
        # print the cost every 100 iterations
        if print_cost and i%100 == 0:
            print("cost after iteration %i: %f" %(i,cost))
        if print_cost and i%100 == 0:
            costs.append(cost)
            
   # plot the cost 
    plt.figure(7)
    plt.plot(np.squeeze(costs))
    plt.ylabel('cost')
    plt.xlabel('iterations (per tens)')
    plt.title("Learning rate = "+str(learning_rate))
    plt.show()
    return parameters


# # Constant for the two layer model
# n_x = 784 ; # number of pixels of each image
# n_h = 30
# n_y = 10; # number of possible digits
# #layers_dims = (n_x, n_h, n_y)
# #train_y = np.array(train_y)
# #parameters = two_layer_model(train_x.T,train_y,layers_dims)

# In[ ]:


# Constant for the L layer model
X = train_x.T
Y = np.array(train_y)
layers_dims = [784, 128, 64, 10]
learning_rate = 0.005
num_iterations = 3000
print_cost = True
parameters = L_layer_model(X, Y, layers_dims, learning_rate, num_iterations, print_cost)


# In[ ]:


print(parameters)


# def predict(X, y, parameters):
#     m = X.shape[1]
#     
#     W1 = parameters["W1"]
#     b1 = parameters["b1"]
#     W2 = parameters["W2"]
#     b2 = parameters["b2"]
#     
#     y = one_hot_matrix(y,b2.shape[0])
#     y_prediction = np.zeros(y.shape)
#     A1, cache1 = linear_activation_forward(X, W1, b1, "relu")
#     A2, cache2 = linear_activation_forward(A1, W2, b2, "sigmoid")
#     y_prediction = A2 > 0.5
#     y_prediction = y_prediction.astype(float)
#     accuracy = 100 - np.mean(np.abs(y_prediction -y))
#     return accuracy

# In[ ]:


def L_model_predict(X, Y, parameters):
    n_y = np.max(Y)+1
    Y = one_hot_matrix(Y, n_y)
    L = len(parameters)//2
    A = X
    for l in range(1,L):
        A_prev = A
        A, cache = linear_activation_forward(A_prev, parameters["W" + str(l)], parameters["b" + str(l)],"relu")
    AL, cache = linear_activation_forward(A, parameters["W" + str(L)], parameters["b" + str(L)], "sigmoid")
    y_prediction = AL > 0.5
    y_prediction = y_prediction.astype(float)
    accuracy = 100 - np.mean(np.abs(y_prediction - Y))
    return accuracy


# In[ ]:


train_accuracy = L_model_predict(train_x.T, train_y, parameters)
print("train accuracy: "+str(train_accuracy)+"%")


# In[ ]:


def decode_one_hot_matrix(mat):
    vec = np.argmax(mat, axis = 0)
    return vec


# def predicted_digit(X,parameters):
#     W1 = parameters["W1"]
#     b1 = parameters["b1"]
#     W2 = parameters["W2"]
#     b2 = parameters["b2"]
#     y_prediction = np.zeros((b2.shape[0],X.shape[1]),np.float)
#     A1, cache1 = linear_activation_forward(X, W1, b1, "relu")
#     A2, cache2 = linear_activation_forward(A1, W2, b2, "sigmoid")
#     y_prediction = A2 > 0.5
#     y_prediction = y_prediction.astype(float)
#     y_prediction = decode_one_hot_matrix(y_prediction)
#     return y_prediction

# In[ ]:


def L_model_predicted_digit(X, parameters):
    L = len(parameters)//2
    A = X
    for l in range(1,L):
        A_prev = A
        A, cache = linear_activation_forward(A_prev, parameters["W" + str(l)], parameters["b" + str(l)],"relu")
    AL, cache = linear_activation_forward(A, parameters["W" + str(L)], parameters["b" + str(L)], "sigmoid")
    y_prediction = np.zeros((parameters["b"+str(L)].shape[0],X.shape[1]),np.float)
    y_prediction = AL > 0.5
    y_prediction = y_prediction.astype(float)
    y_prediction = decode_one_hot_matrix(y_prediction)
    return y_prediction


# In[ ]:


test_y =L_model_predicted_digit(test.T,parameters)
pd.DataFrame(test_y)


# In[ ]:


ImageId = np.array(list(range(test_y.shape[0])))
ImageId = ImageId + 1
submission = pd.DataFrame({
        "ImageId": ImageId,
        "Label": test_y
    })
submission.to_csv("output3.csv", index=False)
outputFile = pd.read_csv("output3.csv")
outputFile.head()


# In[ ]:


index = 25000
plt.figure(7)
plt.imshow(test.iloc[index,:].reshape(28,28), cmap = "gray")
print("Corresponding label = " + str(test_y[index]))

