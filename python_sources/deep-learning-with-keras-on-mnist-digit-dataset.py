#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import keras


# In[ ]:


from keras.datasets import mnist

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()


# In[ ]:


train_images.shape


# In[ ]:


len(train_labels)


# In[ ]:


train_labels


# In[ ]:


test_images.shape


# In[ ]:


len(test_labels)


# In[ ]:


test_labels


# In[ ]:


from keras import models
from keras import layers

model = models.Sequential()
model.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
model.add(layers.Dense(10, activation='softmax'))
print(model.summary())


# In[ ]:


model.compile(optimizer='rmsprop',
                loss='categorical_crossentropy',
                metrics=['accuracy'])


# In[ ]:


# reshaping from 28,28 numpy array to 28*28 image and normalising pixel between 0-1 by dividing 255 
train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype('float32') / 255


# In[ ]:


# turning labeles into catagories
from keras.utils import to_categorical

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)


# In[ ]:


model.fit(train_images, train_labels, epochs=5, batch_size=128)


# In[ ]:


test_loss, test_acc = model.evaluate(test_images, test_labels)


# In[ ]:


print('test_acc:', test_acc)

