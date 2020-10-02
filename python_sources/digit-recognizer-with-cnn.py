#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[3]:


train_data = pd.read_csv('../input/train.csv')
test_data = pd.read_csv('../input/test.csv')


# In[25]:


train_data.head()


# In[4]:


label = train_data['label']
train_data.drop(['label'], axis=1, inplace=True)


# In[31]:


import matplotlib.pyplot as plt

plt.imshow(train_data.iloc[222].values.reshape(28,28), cmap='Greys')


# In[5]:


train_data[train_data>0]=1
test_data[test_data>0]=1


# In[32]:


plt.imshow(train_data.iloc[222].values.reshape(28,28), cmap='Greys')


# In[6]:


img_data = train_data.values.reshape(-1,28,28,1)
test_img_data = test_data.values.reshape(-1,28,28,1)


# In[7]:


from sklearn.preprocessing import OneHotEncoder

one = OneHotEncoder(sparse=False, categories='auto')
hot_label = one.fit_transform(label.values.reshape(-1,1))
hot_label = hot_label.reshape(-1,10)


# In[33]:


print(hot_label)


# In[9]:


import tensorflow as tf
import tensorflow.keras as K


# In[10]:


model = tf.keras.Sequential()


# In[12]:


model.add(K.layers.Conv2D(filters=32, kernel_size=(3,3), padding='same',activation='relu'))
model.add(K.layers.Conv2D(filters=32, kernel_size=(3,3), padding='same',activation='relu'))
model.add(K.layers.MaxPool2D(pool_size=(2,2), ))
model.add(K.layers.Dropout(rate = 0.2))


# In[13]:


model.add(K.layers.Conv2D(filters=64, kernel_size=(3,3), padding='same',activation='relu'))
model.add(K.layers.Conv2D(filters=64, kernel_size=(3,3), padding='same',activation='relu'))
model.add(K.layers.MaxPool2D(pool_size=(2,2), strides=(2,2)))
model.add(K.layers.Dropout(rate = 0.2))


# In[14]:


model.add(K.layers.Flatten())
model.add(K.layers.Dense(256, activation='relu'))
model.add(K.layers.Dropout(rate = 0.4))
model.add(K.layers.Dense(10, activation='softmax'))


# In[15]:


model.compile(optimizer=K.optimizers.Adam(), loss=K.losses.categorical_crossentropy, metrics=['accuracy'])


# In[16]:


model.fit(x=img_data, y=hot_label, batch_size=64, epochs=30)


# In[17]:


model.summary()


# In[21]:


result = model.predict_classes(test_img_data)


# In[22]:


result


# In[24]:


results = pd.Series(result,name="Label")
submission = pd.concat([pd.Series(range(1,28001),name = "ImageId"),results],axis = 1)

submission.to_csv("results.csv",index=False)


# In[ ]:




