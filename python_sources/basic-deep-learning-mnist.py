#!/usr/bin/env python
# coding: utf-8

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


from keras.datasets import mnist

(train_images,train_labels),(test_images,test_labels) = mnist.load_data()


# In[ ]:


train_images = train_images.reshape(60000,28*28)
train_images = train_images.astype('float32')/255

test_images = test_images.reshape(10000,28*28)
test_images = test_images.astype('float32')/255

from keras.utils import to_categorical

train_labels = to_categorical(train_labels)
test_labels  = to_categorical(test_labels)


# In[ ]:


train_images.shape


# In[ ]:


train_labels.shape


# In[ ]:


from keras import models
from keras import layers

def build_model():
    network = models.Sequential()
    network.add(layers.Dense(512,activation='relu',input_shape=(28*28,)))
    network.add(layers.Dense(512,activation='relu'))
    network.add(layers.Dense(10,activation='softmax'))
    
    network.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])
    return network


# In[ ]:


network = build_model()


# In[ ]:


valid_images = train_images[:10000]
valid_labels = train_labels[:10000]

partial_train_images = train_images[10000:]
partial_train_labels = train_labels[10000:]


# In[ ]:


network_history = network.fit(partial_train_images,partial_train_labels,epochs=10,batch_size=128,
                              validation_data=(valid_images,valid_labels))


# In[ ]:


network_history.history.keys()


# In[ ]:


import matplotlib.pyplot as plt

train_loss = network_history.history['loss']
valid_loss = network_history.history['val_loss']

train_acc = network_history.history['acc']
valid_acc = network_history.history['val_acc']

epochs = range(1,len(train_acc)+1)

plt.plot(epochs,train_loss,'bo',label='Training_loss')
plt.plot(epochs,valid_loss,'b',label='Validation_loss')

plt.xlabel('Epochs')
plt.ylabel('Loss')

plt.legend()
plt.show()


# In[ ]:


import matplotlib.pyplot as plt

plt.plot(epochs,train_acc,'go',label='Training_accuracy')
plt.plot(epochs,valid_acc,'g',label='Validation_accuracy')

plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.show()


# In[ ]:


test_result = network.evaluate(test_images,test_labels)

print('Test_acc:{}'.format(test_result[1]))


# In[36]:


from keras.datasets import mnist

(train_images,train_labels),(test_images,test_labels) = mnist.load_data()


# In[37]:


train_images = train_images.reshape(train_images.shape[0],train_images.shape[1]*(train_images.shape[1]))
train_images = train_images.astype('float32')/255

test_images = test_images.reshape(test_images.shape[0],test_images.shape[1]*test_images.shape[1])
test_images = test_images.astype('float32')/255
                                    
                                                           


# In[38]:


train_images.shape


# In[39]:


test_images.shape


# In[40]:


from keras.utils import to_categorical

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)


# In[42]:


train_labels.shape
test_labels.shape


# In[43]:


valid_images = train_images[:10000]
valid_labels = train_labels[:10000]

partial_train_images = train_images[10000:]
partial_train_labels = train_labels[10000:]


# In[44]:


valid_images.shape
valid_labels.shape


# In[45]:


from keras import models
from keras import layers

def build_model():
    network = models.Sequential()
    network.add(layers.Dense(512,activation='relu',input_shape=(28*28,)))
    network.add(layers.Dense(512,activation='relu'))
    network.add(layers.Dense(10,activation='softmax'))
    
    network.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])
    return network


# In[46]:


from keras import regularizers

def build_L1_model():
    network = models.Sequential()
    network.add(layers.Dense(512,activation='relu',kernel_regularizer=regularizers.l1(0.001),input_shape=(28*28,)))
    network.add(layers.Dense(512,activation='relu',kernel_regularizer=regularizers.l1(0.001)))
    network.add(layers.Dense(10,activation='softmax'))
    
    network.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])
    return network


# In[47]:


def build_L2_model():
    network = models.Sequential()
    network.add(layers.Dense(512,activation='relu',kernel_regularizer=regularizers.l2(0.001),input_shape=(28*28,)))
    network.add(layers.Dense(512,activation='relu',kernel_regularizer=regularizers.l2(0.001)))
    network.add(layers.Dense(10,activation='softmax'))
    
    network.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])
    return network


# In[48]:


def build_L1_L2_model():
    network = models.Sequential()
    network.add(layers.Dense(512,activation='relu',kernel_regularizer=regularizers.l1_l2(0.001),input_shape=(28*28,)))
    network.add(layers.Dense(512,activation='relu',kernel_regularizer=regularizers.l1_l2(0.001)))
    network.add(layers.Dense(10,activation='softmax'))
    
    network.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])
    return network


# In[49]:


def build_Dropout_model():
    network = models.Sequential()
    network.add(layers.Dense(512,activation='relu',input_shape=(28*28,)))
    network.add(layers.Dropout(0.5))
    network.add(layers.Dense(512,activation='relu'))
    network.add(layers.Dropout(0.5))
    network.add(layers.Dense(10,activation='softmax'))
    
    network.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])
    return network


# In[50]:


normal_model=build_model()
L1_model=build_L1_model()
L2_model=build_L2_model()
L1_L2_model=build_L1_L2_model()
Dropout_model=build_Dropout_model()


# In[55]:


normal_model_history = normal_model.fit(partial_train_images,partial_train_labels,epochs=100,batch_size=128,
                                        validation_data=(valid_images,valid_labels))


# In[58]:


dropout_model_history = Dropout_model.fit(partial_train_images,partial_train_labels,epochs=100,batch_size=128,
                                        validation_data=(valid_images,valid_labels))


# In[59]:


dropout_model_history.history.keys()


# In[60]:


import matplotlib.pyplot as plt

valid_loss_nm = normal_model_history.history['val_loss']

valid_loss_dm = dropout_model_history.history['val_loss']

epochs = range(1,len(valid_loss)+1)

plt.plot(epochs,valid_loss_nm,'b',label='Normal_model')

plt.plot(epochs,valid_loss_dm,'g',label='Dropout_model')

plt.legend()

plt.show()


# In[61]:


test1 = normal_model.evaluate(test_images,test_labels)

print(test1[1])


# In[62]:


test1 = Dropout_model.evaluate(test_images,test_labels)

print(test1[1])


# In[ ]:




