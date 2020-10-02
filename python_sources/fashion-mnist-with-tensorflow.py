#!/usr/bin/env python
# coding: utf-8

# In[29]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[30]:


train = pd.read_csv('../input/fashion-mnist_train.csv')
train_data, val_data = train_test_split(train, test_size=0.2)
train_label = train_data['label']
train_image = train_data.iloc[:, 1:]
val_label = val_data['label']
val_image = val_data.iloc[:, 1:]


# In[43]:


model = keras.models.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation = 'relu', input_shape = (28, 28 ,1)),
#     keras.layers.MaxPool2D(2, 2),
#     keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPool2D(2, 2),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])


# In[44]:


model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


# In[33]:


train_image = train_image.values
val_image = val_image.values


# In[34]:


train_image = train_image / 255.0
val_image = val_image / 255.0


# In[35]:


train_image = train_image.reshape(48000, 28, 28, 1)
val_image = val_image.reshape(12000, 28, 28, 1)


# In[45]:


model.fit(train_image, train_label, epochs=5)


# In[37]:


model.summary()


# In[46]:


model.evaluate(val_image, val_label)


# In[47]:


model.fit(val_image, val_label)


# In[54]:


test_data = pd.read_csv('../input/fashion-mnist_test.csv')


# In[58]:


test_label = test_data['label']
test_image = test_data.iloc[:, 1:]
test_image = test_image.values.reshape(10000, 28, 28, 1) / 255.0


# In[59]:


model.evaluate(test_image, test_label)

