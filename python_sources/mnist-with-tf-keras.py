#!/usr/bin/env python
# coding: utf-8

# MNIST is the "Hello World" of computer vision. 
# In this notebook, let's classify the MNIST digits with deap learning CNN, with tf.Keras part of the TensorFlow core API.

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


# Import TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Print TensorFlow version
print(tf.__version__)


# # Load train and test datasets

# **Load train dataset**

# In[ ]:


train = pd.read_csv("../input/train.csv")
print("train dataset shape is ", train.shape)
train.head()


# **Train dataset **- split into image pixel data and labels

# In[ ]:


# All pixel values - all rows and column 1 (pixel0) to column 785 (pixel 783)
x_train = (train.iloc[:,1:].values).astype('float32') 
# Take a look at x_train
x_train


# In[ ]:


# Labels - all rows and column 0
y_train = (train.iloc[:,0].values).astype('int32') 

# Take a look at y_train
y_train


# In[ ]:





# **Load test dataset**

# In[ ]:


test = pd.read_csv("../input/test.csv")
print("test dataset shape is ", test.shape)
test.head()


# In[ ]:


x_test = test.values.astype('float32')


# In[ ]:


x_test


# ### Preprocess data

# In[ ]:


num_classes = 10

# Normalize the input data
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

# Reshape input data from (28, 28) to (28, 28, 1)
w, h = 28, 28
x_train = x_train.reshape(x_train.shape[0], w, h, 1)
x_test = x_test.reshape(x_test.shape[0], w, h, 1)

# One-hot encode the labels
y_train = keras.utils.to_categorical(y_train, num_classes)

# Take a look at the dataset shape after conversion with keras.utils.to_categorical
print("x_train shape:", x_train.shape, "y_train shape:", y_train.shape)


# ### Define the model architecture

# In[ ]:


model = keras.Sequential()

# Must define the input shape in the first layer of the neural network
model.add(keras.layers.Conv2D(filters=32, kernel_size=3, padding='same', activation='relu', input_shape=(28,28,1))) 
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.MaxPooling2D(pool_size=2))
model.add(keras.layers.Dropout(0.3))

model.add(keras.layers.Conv2D(filters=64, kernel_size=3, padding='same', activation='relu'))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.MaxPooling2D(pool_size=2))
model.add(keras.layers.Dropout(0.3))

model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(128, activation='relu'))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Dense(10, activation='softmax'))

# Take a look at the model summary
model.summary()


# In[ ]:


model.compile(loss=keras.losses.categorical_crossentropy,
             optimizer=keras.optimizers.Adam(),
             metrics=['accuracy'])


# In[ ]:


model.fit(x_train,
         y_train,
         batch_size=64,
         epochs=5)


# In[ ]:


predictions = model.predict_classes(x_test, verbose=0)

submissions=pd.DataFrame({"ImageId": list(range(1,len(predictions)+1)),
                         "Label": predictions})
submissions.to_csv("mnist_tfkeras.csv", index=False, header=True)


# In[ ]:


print(os.listdir(".."))

