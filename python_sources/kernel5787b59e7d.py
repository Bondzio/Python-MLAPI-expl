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


# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time


# In[ ]:


def sigmoid(X, weight):
    z = np.dot(X, weight)
    return 1 / (1 + np.exp(-z))

def loss(h, y):
    return (-y * np.log(h) - (1 - y) * np.log(1 - h)).mean()

def gradient_descent(X, h, y):
    return np.dot(X.T, (h - y)) / y.shape[0]

def update_weight_loss(weight, learning_rate, gradient):
    return weight - learning_rate * gradient

def log_likelihood(x, y, weights):
    z = np.dot(x, weights)
    ll = np.sum( y*z - np.log(1 + np.exp(z)) )
    return ll

def gradient_ascent(X, h, y):
    return np.dot(X.T, y - h)

def update_weight_mle(weight, learning_rate, gradient):
    return weight + learning_rate * gradient


# In[ ]:


data = pd.read_csv("../input/titanic/train_data.csv")
print("Dataset size")
print("Rows {} Columns {}".format(data.shape[0], data.shape[1]))


# In[ ]:


print("Columns and data types")
pd.DataFrame(data.dtypes).rename(columns = {0:'dtype'})


# In[ ]:


df = data.copy()


# In[ ]:


df['class'] = df['Survived'].apply(lambda x : 1 if x == "Yes" else 0)
# features will be saved as X and target will be saved as y
X = df[['Sex','Emb_3']].copy()
X2 = df[['Sex','Emb_3']].copy()
y = df['class'].copy()


# In[ ]:


start_time = time.time()

num_iter = 100000

intercept = np.ones((X.shape[0], 1)) 
X = np.concatenate((intercept, X), axis=1)
theta = np.zeros(X.shape[1])

for i in range(num_iter):
    h = sigmoid(X, theta)
    gradient = gradient_descent(X, h, y)
    theta = update_weight_loss(theta, 0.1, gradient)
    
print("Training time (Log Reg using Gradient descent):" + str(time.time() - start_time) + " seconds")
print("Learning rate: {}\nIteration: {}".format(0.1, num_iter))


# 

# In[ ]:


result = sigmoid(X, theta)
result

