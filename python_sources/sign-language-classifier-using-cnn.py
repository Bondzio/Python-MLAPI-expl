#!/usr/bin/env python
# coding: utf-8

# In[87]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input/Sign-language-digits-dataset/"))

# Any results you write to the current directory are saved as output.


# ## Loading the npy files using numpy to x and y

# In[88]:


x = np.load('../input/Sign-language-digits-dataset/X.npy')
y = np.load('../input/Sign-language-digits-dataset/Y.npy')

x = np.expand_dims(x, axis=3)
x.shape


# ## Visualizing the single image loaded

# In[89]:


import matplotlib.pyplot as plt
plt.imshow(x[100].reshape(64, 64), cmap='gray')
print(x[100].shape)
print(y[100].shape)


# In[90]:


from sklearn.model_selection import train_test_split
xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.1)


# ## Defining the model in model function

# In[135]:


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, BatchNormalization, Flatten, Dropout
from tensorflow.keras.optimizers import SGD

dropout = False
dropoutVal = 0.2


# In[189]:


def model():
    kernelSize = (4, 4)
    numClasses = 10
    activation = 'relu'
    model = Sequential()
    model.add(Conv2D(32, kernel_size=kernelSize, padding='same', input_shape=(64, 64, 1), activation=activation))
    model.add(Conv2D(32, kernel_size=kernelSize, padding='same', activation=activation))    
    model.add(Conv2D(32, kernel_size=kernelSize, padding='same', activation=activation))
    model.add(Conv2D(32, kernel_size=kernelSize, padding='same', activation=activation))
    model.add(MaxPooling2D(pool_size=4))

    model.add(BatchNormalization())
    model.add(Flatten())
    model.add(Dense(500, activation=activation))
    model.add(Dense(numClasses, activation='softmax'))
    model.summary()
    model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.0001), metrics=['accuracy'])
    return model


# In[190]:


model = model()


# In[191]:


history = model.fit(xTrain, yTrain, validation_data=(xTest, yTest), epochs=100)


# ## Let's try to visualize the layers

# In[192]:


output_layers = [layer.output for layer in model.layers]


# In[193]:


input_layer = model.input


# In[194]:


from tensorflow.keras.models import Model


# In[195]:


m = Model(inputs=input_layer, outputs=output_layers)


# In[196]:


activations = m.predict(xTrain[0].reshape(1, 64, 64, 1))


# In[197]:


def disp_activations(activations):
    rows = 1
    cols = len(activations) - 4 # 4 Subracted from this because last 3 layers are not CNN layers which can't be visualized
    fig, ax = plt.subplots(rows, cols, figsize=(15, 15))
    for i in range(cols):
        ax[i].imshow(activations[i][0, :, :, i], cmap='gray')


# In[198]:


disp_activations(activations)


# In[ ]:




