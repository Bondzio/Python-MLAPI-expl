#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

import warnings

warnings.filterwarnings('ignore')


# Loading dataset from sklearn datasets.Lets visualize our data set...

# In[ ]:


ds = load_digits()
print(ds.target.shape)
plt.figure(figsize=(8,7))
for i in range(16):
    plt.subplot(4, 4, i+1)
    plt.imshow(ds.data[i].reshape(8,8),cmap='Greys',interpolation = "nearest")
    plt.title("Digit: {}".format(ds.target[i]))
    plt.xticks([])
    plt.yticks([])
plt.show()


# Lets check the distribution of numbers.

# In[ ]:


plt.figure()
sns.set(style="darkgrid")
sns.countplot(ds.target)
plt.show()


# Manipulate dataset for builded training model.And split it for test and train sets.

# In[ ]:


onehot_target = pd.get_dummies(ds.target)
x_train, x_test, y_train, y_test = train_test_split(ds.data, onehot_target, test_size=0.1, random_state=10)
print("Train Set Shape : " , x_train.shape)
print("Train Set Label Shape : " , y_train.shape)
print("Test Set Shape : " , x_test.shape)
print("Test Set Label Shape : " , y_test.shape)


# Lets normalize our x_train and x_test

# In[ ]:


x_train = x_train/np.amax(x_train)
x_test = x_test/np.amax(x_test)


# Initialize parameters for the layers..We will have 2 hidden layer one input layers and the one output layers.

# In[ ]:


class ModelParams:
    def __init__ (self,x, y):
        self.x = x
        self.y = y
        neurons = 128       # neuron counts for hidden layers
        self.lr = 0.2       # learning rate
        self.epoch = 500   # epoch count
        ip_dim = x.shape[1] # input layer size
        op_dim = y.shape[1] # output layer size
        self.w1 = np.random.randn(ip_dim, neurons) # weights for first layer
        self.b1 = np.zeros((1, neurons))           # biases for first layer
        self.w2 = np.random.randn(neurons, neurons)
        self.b2 = np.zeros((1, neurons))
        self.w3 = np.random.randn(neurons, op_dim)
        self.b3 = np.zeros((1, op_dim))


# Lets write usefull functions (sigmoid and softmax).
# We will use softmax for the last layer..

# In[ ]:


def sigmoid(ts):
    return 1/(1 + np.exp(-ts))

def softmax(ts):
    exps = np.exp(ts - np.max(ts, axis=1, keepdims=True))
    return exps/np.sum(exps, axis=1, keepdims=True)


# Lets start with the forward propogation..

# In[ ]:


def forwardPropagation(param):
    z1 = np.dot(param.x, param.w1) + param.b1
    param.a1 = sigmoid(z1)
    z2 = np.dot(param.a1, param.w2) + param.b2
    param.a2 = sigmoid(z2)
    z3 = np.dot(param.a2, param.w3) + param.b3
    param.a3 = softmax(z3)


# For backwardpropagation we need derivative method of our Activation function..

# In[ ]:


def sigmoid_derv(x):
    return sigmoid(x) * (1 - sigmoid(x))


# One more step before the backward propagation.We have to define our cost and loss function.As a cost function i will use cross entropy.. For details please check [here](https://deepnotes.io/softmax-crossentropy)

# In[ ]:


def cross_entropy(pred, real):
    ns = real.shape[0]
    res = pred - real
    return res/ns

def error(pred, real):
    ns = real.shape[0]
    logp = - np.log(pred[np.arange(ns), real.argmax(axis=1)])
    loss = np.sum(logp)/ns
    return loss


# Now lets build our backward propagation method. For output layer i dont get derivative of softmax activation function. You can find the details in [here](https://deepnotes.io/softmax-crossentropy).

# In[ ]:


def backwardPropagation(param):
    loss = error(param.a3, param.y)
    a3d = cross_entropy(param.a3, param.y) # w3
    z2d = np.dot(a3d, param.w3.T)
    a2d = z2d * sigmoid_derv(param.a2) # w2
    z1d = np.dot(a2d, param.w2.T)
    a1d = z1d * sigmoid_derv(param.a1) # w1

    param.w3 -= param.lr * np.dot(param.a2.T, a3d)
    param.b3 -= param.lr * np.sum(a3d, axis=0, keepdims=True)
    param.w2 -= param.lr * np.dot(param.a1.T, a2d)
    param.b2 -= param.lr * np.sum(a2d, axis=0)
    param.w1 -= param.lr * np.dot(param.x.T, a1d)
    param.b1 -= param.lr * np.sum(a1d, axis=0)
    return loss;


# Create prediction depends on our model..

# In[ ]:


def predict(data,model):
    model.x = data
    forwardPropagation(model)
    return model.a3.argmax()


# Lets train our model

# In[ ]:


model = ModelParams(x_train,np.array(y_train))
errorList = []
for x in range(model.epoch):
    forwardPropagation(model)
    loss = backwardPropagation(model)
    errorList.append(loss)
    if(x % 10 == 0 or x+1 == model.epoch):
        print('%s.Iteration -> Loss : %s' % (x, loss))


# Lets visualize our training process

# In[ ]:


index_list = range(model.epoch)
plt.plot(index_list,errorList)
plt.xlabel("Number of Iterarion")
plt.ylabel("Cost")
plt.show()


# Lets Calculate Accuracy. When we increase the epoch count our accuracy will increase.

# In[ ]:


def calc_acc(x, y):
    acc = 0
    for x_s,y_s in zip(x, y):
        s = predict(x_s,model)
        if s == np.argmax(y_s):
            acc +=1
    return acc/len(x)*100

print("Training accuracy : ", calc_acc(x_train, np.array(y_train)))
print("Test accuracy : ", calc_acc(x_test, np.array(y_test)))


# Lets Try with some examples..

# In[ ]:


plt.figure(figsize=(8,7))
for i in range(16):
    plt.subplot(4, 4, i+1)
    plt.imshow(ds.data[i].reshape(8,8),cmap='Greys',interpolation = "nearest")
    plt.title("Digit: {}".format(predict(ds.data[i],model)))
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
plt.show()

