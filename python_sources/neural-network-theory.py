#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# ## Neural Network Example
# 
# ![image.png](attachment:image.png)

# ## Perceptron Review
# 
# ![image.png](attachment:image.png)

# ### Expression 1
# 
# ![image.png](attachment:image.png)

# ## A Perceptron Specifying Bias
# 
# ![image.png](attachment:image.png)

# ## Expression 2
# 
# ![image.png](attachment:image.png)

# ## Activation Function
# 
# a = b + $w_{1}x_{1}$ + $w_{2}x_{2}$
# 
# y = h(a)
# 
# ![image.png](attachment:image.png)

# ## Step Function

# In[ ]:


# Numpy array cannot be added as an argument.
def step_function(x):
    if x > 0:
        return 1
    else:
        return 0


# In[ ]:


# Numpy array can be added as an argument.
def step_function(x):
    y = x > 0 
    return y.astype(np.int)


# In[ ]:


# Specifically
import numpy as np
x = np.array([-2.0, 1.0, 2.0])
print(x)

y = x > 0
print(y) # bool array

y = y.astype(np.int) # bool to int
print(y)


# In[ ]:


# Step Function graph
import numpy as np
import matplotlib.pyplot as plt

def step_function(x):
    return np.array(x > 0, dtype=np.int)

x = np.arange(-6.0, 6.0, 0.1)
y = step_function(x)
plt.plot(x, y)
plt.ylim(-0.1, 1.1)
plt.show()


# ## Sigmoid Function
# 
# ![image.png](attachment:image.png)

# In[ ]:


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Handle numpy array properly 
x = np.array([-2.0, 1.0, 3.0])
print(sigmoid(x))


# In[ ]:


# Sigmoid function graph
x = np.arange(-6.0, 6.0, 0.1)
y = sigmoid(x)
plt.plot(x, y)
plt.ylim(-0.1, 1.1)
plt.show()


# ## ReLu Function
# 
# ![image.png](attachment:image.png)

# In[ ]:


def relu(x):
    return np.maximum(0, x)


# In[ ]:


# Relu function graph
x = np.arange(-6.0, 6.0, 0.5)
y = relu(x)
plt.plot(x, y)
plt.ylim(-1, 6)
plt.show()


# ## Dot Product of A Matrix
# 
# ![image.png](attachment:image.png)

# In[ ]:


A = np.array([[1,2], [3,4]])
print(A.shape)

B = np.array([[5,6], [7,8]])
print(B.shape)

print(np.dot(A, B))


# ![image.png](attachment:image.png)

# In[ ]:


A = np.array([[2,3], [3,4], [5,6]])
print(A.shape)

B = np.array([8,9])
print(B.shape)

print(np.dot(A, B))


# ![image.png](attachment:image.png)

# ## Perform Neural Network Calculation with Product of Matrices
# 
# ![image.png](attachment:image.png)

# In[ ]:


X = np.array([2,3])
print(X.shape)

W = np.array([[1,3,5], [2,4,6]])
print(W)
print(W.shape)

Y = np.dot(X, W)
print(Y)


# ## 3-Layer Neural Network
# 
# ![image.png](attachment:image.png)

# ### Signal Transmission from Input Layer to One Layer
# 
# ![image.png](attachment:image.png)

# $a_{1}^{1} = w_{11}^{1}x_{1} + w_{12}^{1}x_{2} + b_{1}^{1}$
# 
# $\mathbf{A}^{(1)} = \mathbf{X}\mathbf{W}^{(1)} + \mathbf{B}^{(1)}$
# 
# $\mathbf{A}^{(1)} = (a_{1}^{(1)}, a_{2}^{(1)}, a_{3}^{(1)})$
# 
# $\mathbf{X} = (x_{1}, x_{2})$
# 
# $\mathbf{B}^{(1)} = (b_{1}^{1}, b_{2}^{1}, b_{3}^{1})$
# 
# $\mathbf{W}^{(1)} = \begin{pmatrix}
# w_{11}^{(1)} & w_{21}^{(1)} & w_{31}^{(1)}\\ 
# w_{12}^{(1)} & w_{22}^{(1)} & w_{32}^{(1)}
# \end{pmatrix}$

# In[ ]:


X = np.array([2.0, 2.5])
W1 = np.array([[0.2, 0.4, 0.6], [0.3, 0.6, 0.8]])
B1 = np.array([-.2, 0.3, 0.4])

print(W1.shape)
print(X.shape)
print(B1.shape)

A1 = np.dot(X, W1) + B1
print(A1)


# ![image.png](attachment:image.png)

# In[ ]:


Z1 = sigmoid(A1)

print(A1)
print(Z1)


# ## Signaling from the 1 Layer to the 2 Layer
# 
# ![image.png](attachment:image.png)

# In[ ]:


W2 = np.array([[0.2, 0.4], [0.3, 0.5], [0.4, 0.7]])
B2 = np.array([0.2, 0.3])

print(Z1.shape)
print(W2.shape)
print(B2.shape)

A2 = np.dot(Z1, W2) + B2
Z2 = sigmoid(A2)


# ## Signal Transfer from the 2 Layer to the Output Layer
# 
# ![image.png](attachment:image.png)

# In[ ]:


def identity_function(x):
    return x

W3 = np.array([[0.2, 0.4], [0.3, 0.6]])
B3 = np.array([0.3,0.6])

A3 = np.dot(Z2, W3) + B3
Y = identity_function(A3) # Y = A3


# In[ ]:


# Organization
def init_network():
    network = {}
    network['W1'] = np.array([[0.1, 0.3, 0.5], [0.2, 0.4, 0.6]])
    network['b1'] = np.array([0.1, 0.2, 0.3])
    network['W2'] = np.array([[0.1, 0.4], [0.2, 0.5], [0.3, 0.6]])
    network['b2'] = np.array([0.1, 0.2])
    network['W3'] = np.array([[0.1, 0.3], [0.2, 0.4]])
    network['b3'] = np.array([0.1, 0.2])
    
    return network

def forward(network, x):
    W1, W2, W3 = network['W1'], network['W2'], network['W3']
    b1, b2, b3 = network['b1'], network['b2'], network['b3']
    
    a1 = np.dot(x, W1) + b1
    z1 = sigmoid(a1)
    a2 = np.dot(z1, W2) + b2
    z2 = sigmoid(a2)
    a3 = np.dot(z2, W3) + b3
    y = identity_function(a3)
    
    return y

network = init_network()
x = np.array([1.0, 0.5])
y = forward(network, x)
print(y)
    


# ## Identity Function
# 
# ![image.png](attachment:image.png)

# ## Softmax Function
# 
# ![image.png](attachment:image.png)

# ![image.png](attachment:image.png)

# In[ ]:


a = np.array([0.4, 3.0, 4.5])
exp_a = np.exp(a)
print(exp_a)

sum_exp_a = np.sum(exp_a)
print(sum_exp_a)

y = exp_a / sum_exp_a
print(y)


# In[ ]:


def softmax(a):
    exp_a = np.exp(a)
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a

    return y


# ## Softmax Function Overflow Solution
# 
# ![image.png](attachment:image.png)

# In[ ]:


a = np.array([2000, 1900, 800])
print(np.exp(a) / np.sum(np.exp(a)))

c = np.max(a) # Maximum value of input signal
print(a - c)

print(np.exp(a - c) / np.sum(np.exp(a - c)))


# In[ ]:


def softmax(a):
    c = np.max(a)
    exp_a = np.exp(a - c) # Overflow Countermeasures
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a

    return y


# In[ ]:


# You can interpret the output of a Softmax function as a probability
a = np.array([0.5, 3.0, 4.5])
y = softmax(a)
print(y)
print(np.sum(y))

