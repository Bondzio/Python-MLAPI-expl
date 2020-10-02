#!/usr/bin/env python
# coding: utf-8

# # PIMA Dataset Prediction Modelling with KERAS (~80%)
# ---
# 
# Implement a Deep Neural Network with KERAS on the Pima Indians Diabetes Database (https://www.kaggle.com/uciml/pima-indians-diabetes-database)

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from __future__ import print_function
import tensorflow as tf
from six.moves import range
import numpy as np
import os
import sys

from IPython.display import display, Image
import matplotlib.pyplot as plt
# Config the matlotlib backend as plotting inline in IPython
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix,classification_report

from tensorflow.contrib import keras
from keras import models, layers, losses, optimizers, metrics

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# ## Data Preprocessing

# In[ ]:


df = pd.read_csv('../input/diabetes.csv')


# In[ ]:


df.head()


# In[ ]:


# Splitting into training and testing datasets

X = df.drop(['Outcome'], axis=1)
Y = df['Outcome']

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=101)


# ---

# ## Data Visualization

# *I have used the following kernel as reference for Data Visualizations - ML From Scratch-Part 2 by I, Coder *

# We first plot a 'histogram' of all data as-is.

# In[ ]:


X.hist(figsize=(16,9), edgecolor="black", bins=20)


# Now, we plot the histogram of the Diabetic Outcomes

# In[ ]:


# Diabetic Outcomes
x_aff = df[df['Outcome']==1]
x_aff.hist(figsize=(16,9), edgecolor="black", bins=20)


# Next, we plot the Pair Plots - A plot of all variables against the each other to get an idea about the distribution of diabetic and non-diabetic trend.

# In[ ]:


sns.pairplot(df, hue='Outcome', markers=['o', 'x'], diag_kind='kde')


# ---

# ## Data Scaling
# 
# We scale the data so as to increase the model accuracy.

# In[ ]:


scaler = MinMaxScaler()

scaled_x_train = scaler.fit_transform(X_train)
scaled_x_test = scaler.transform(X_test)


# ---

# ## KERAS DATA MODEL

# We will use the following parameters in our implementation -
# 
# * Hidden Layers - 3 , each consisiting of 8 neurons.
# * Activation - RELU for hidden, SOFTMAX for output layer.
# * Optimizer - SGD
# * Learning Rate Decay - 0.01
# * L2 Regularization
# 

# In[ ]:


# Create Keras DNN Model

model = models.Sequential()

# Hyperparameters
hold_prob = 0.01
beta = 1e-8
alpha = 0.05
lr_decay = 0.01
iterations = 400
validation_split = 0.5
opt_momentum = 0.9 # (Use only for SGD)
batch_size = 32

# Optimizer
opt = optimizers.SGD(lr=alpha, decay=lr_decay, momentum=opt_momentum, nesterov=True)

# First Layer
model.add(layers.Dense(input_dim=8, units=8, activation='relu'))

# Hidden Layers
model.add(layers.Dense(units=8, activation='relu', kernel_regularizer=keras.regularizers.l2(beta)))
model.add(layers.Dropout(hold_prob))

model.add(layers.Dense(units=8, activation='relu', kernel_regularizer=keras.regularizers.l2(beta)))
model.add(layers.Dropout(hold_prob))

model.add(layers.Dense(units=8, activation='relu', kernel_regularizer=keras.regularizers.l2(beta)))
model.add(layers.Dropout(hold_prob))

# Output Layer
model.add(layers.Dense(units=2, activation='softmax'))

# Compiling the Model
model.compile(optimizer=opt, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train
model.fit(x=scaled_x_train, y=y_train, epochs=iterations, validation_split=validation_split, batch_size=batch_size)


# **Training Accuracy ~ 80%**
# 
# **Validation Accuracy ~ 74%**
# 
# ---

# Let's check how our model performs on new data.

# In[ ]:


predictions = model.predict_classes(scaled_x_test)
print(classification_report(y_test, predictions))


# ### Conclusion
# 
# Thus, with considerable hyperparameter tuning, we can achieve an accuracy of ~76-79% with KERAS, which is a decent accuracy level.
