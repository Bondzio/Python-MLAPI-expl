#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


train = pd.read_csv('/kaggle/input/fashionmnist/fashion-mnist_train.csv')
test = pd.read_csv('/kaggle/input/fashionmnist/fashion-mnist_test.csv')


# In[ ]:


train.shape , test.shape


# In[ ]:


xtrain = train.drop('label', axis=1)


# In[ ]:


ytrain = train['label']


# In[ ]:


xtrain.shape, ytrain.shape


# In[ ]:


xtrain = xtrain.values
ytrain = ytrain.values


# In[ ]:


xtrain = xtrain/255
xtrain[0]


# In[ ]:


xtrain
set(ytrain)


# In[ ]:


import keras as kr
ytrain = kr.utils.to_categorical(ytrain)


# In[ ]:


ytrain


# In[ ]:


ytrain.shape


# In[ ]:


model = kr.models.Sequential()
model.add(kr.layers.Dense(512 , activation="sigmoid" , input_shape=(784,)))
model.add(kr.layers.Dense(512, activation="sigmoid" ))
model.add(kr.layers.Dense(10,activation="softmax"))


# In[ ]:


model.summary()


# In[ ]:


model.compile(optimizer="adam" ,loss="categorical_crossentropy",metrics=["accuracy"])


# In[ ]:


hist = model.fit(xtrain, ytrain , epochs = 13 , batch_size= 100 , validation_split=0.2 , shuffle=True)


# **CNN**

# In[ ]:





# In[ ]:


import matplotlib.pyplot as plt
#plt.figure(figsize=(10,6))
fig, (ax1, ax2) = plt.subplots(2)

ax1.plot(hist.history["accuracy"], c="red")
ax1.plot(hist.history["val_accuracy"])

ax2.plot(hist.history["loss"], c="red")
ax2.plot(hist.history["val_loss"])

plt.show()


# In[ ]:


train = pd.read_csv('/kaggle/input/fashionmnist/fashion-mnist_train.csv')
test = pd.read_csv('/kaggle/input/fashionmnist/fashion-mnist_test.csv')


# In[ ]:


train.shape , test.shape


# In[ ]:


xtrain = train.drop('label', axis=1)


# In[ ]:


ytrain = train['label']


# In[ ]:


xtrain.shape, ytrain.shape


# In[ ]:


xtrain = xtrain.values
ytrain = ytrain.values


# In[ ]:


xtrain = xtrain/255


# In[ ]:


xtrain[0]


# In[ ]:


xtrain = xtrain.reshape((-1,28,28,1))


# In[ ]:


xtrain.shape


# In[ ]:


xtrain.shape


# In[ ]:


import keras as kr
ytrain = kr.utils.to_categorical(ytrain)


# In[ ]:


ytrain.shape


# In[ ]:


import matplotlib.pyplot as plt
for i in range(10):
  plt.imshow(xtrain[i].reshape(28,28), cmap='gray')
  plt.show()


# In[ ]:


model = kr.models.Sequential()
model.add(kr.layers.Convolution2D(32 , (3,3) , activation="relu" , input_shape=(28,28,1)))
model.add(kr.layers.Convolution2D(64,(3,3) , activation="relu"))
model.add(kr.layers.Dropout(0.25))
model.add(kr.layers.MaxPooling2D(2,2))

model.add(kr.layers.Convolution2D(32 , (3,3) , activation="relu" ))
model.add(kr.layers.Convolution2D(8,(3,3) , activation="relu"))
model.add(kr.layers.Dropout(0.25))

model.add(kr.layers.Convolution2D(32 , (3,3) , activation="relu" ))
model.add(kr.layers.Convolution2D(8,(3,3) , activation="relu"))
model.add(kr.layers.Dropout(0.25))

model.add(kr.layers.Flatten())
model.add(kr.layers.Dense(100, activation='softmax'))
model.add(kr.layers.Dense(10, activation="softmax"))
model.summary()


# In[ ]:


model.compile(optimizer="adam" ,loss="categorical_crossentropy",metrics=["accuracy"])
hist = model.fit(xtrain,  ytrain , epochs=30  ,shuffle=True , batch_size=256 , validation_split=0.25)


# In[ ]:


import matplotlib.pyplot as plt
#plt.figure(figsize=(10,6))
fig, (ax1, ax2) = plt.subplots(2)

ax1.plot(hist.history["accuracy"], c="red")
ax1.plot(hist.history["val_accuracy"])

ax2.plot(hist.history["loss"], c="red")
ax2.plot(hist.history["val_loss"])

plt.show()

