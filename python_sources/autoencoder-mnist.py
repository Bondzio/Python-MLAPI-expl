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


# **CHAPTER - 11 -- Hands-on On Deep Learning**

# In[ ]:


import warnings
warnings.filterwarnings('ignore')

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

import tensorflow as tf
#tf.logging.set_verbosity(tf.logging.ERROR)

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

from tensorflow.keras.datasets import mnist
import numpy as np


# In[ ]:


(x_train, _), (x_test, _) = mnist.load_data()


# In[ ]:


x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255


# In[ ]:


print(x_train.shape, x_test.shape)


# In[ ]:


x_train[0]


# In[ ]:


x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))


# In[ ]:


print(x_train.shape, x_test.shape)


# In[ ]:


print(len(x_train[0]))
print(x_train[0].shape)


# In[ ]:


encoding_dim = 32


# In[ ]:


input_image = Input(shape= (784,))


# In[ ]:


encoder = Dense(encoding_dim, activation = 'relu')(input_image)


# In[ ]:


decoder = Dense(784, activation = 'sigmoid')(encoder)


# In[ ]:


model = Model(inputs = input_image,outputs = decoder)


# In[ ]:


model.summary()


# In[ ]:


model.compile(optimizer = 'adadelta', loss = 'binary_crossentropy')


# In[ ]:


model.fit(x_train,x_train, epochs=200, batch_size = 256, shuffle = True, validation_data = (x_test, x_test))


# In[ ]:


reconstructed_images = model.predict(x_test)


# In[ ]:


n = 7
plt.figure(figsize=(20, 4))
for i in range(n):
    ax = plt.subplot(1, n, i+1)
    plt.imshow(x_test[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()


# In[ ]:


n = 7
plt.figure(figsize=(20, 4))
for i in range(n):
    ax = plt.subplot(2, n, i + n + 1)
    plt.imshow(reconstructed_images[i].reshape(28, 28))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

plt.show()


# In[ ]:




