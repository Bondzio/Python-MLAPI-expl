#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np 
import pandas as pd 

import os
print(os.listdir("../input"))


# In[ ]:


import tensorflow as tf


# In[ ]:


print(5)


# In[ ]:


(x_train, y_train)=tf.keras.datasets.mnist.load_data()


# In[ ]:


import numpy as np
import pandas as pd


# In[ ]:


import h5py


# In[ ]:


from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten, Dropout, MaxPool2D
from keras.optimizers import Adam, RMSprop
from keras.initializers import RandomNormal
import matplotlib.pyplot as plt
import seaborn as sns
import os
print(os.listdir("../input"))


# In[ ]:


trainFile = h5py.File('../input/train_happy.h5')
testFile = h5py.File('../input/test_happy.h5')


# In[ ]:


train_x=np.array(trainFile['train_set_x'][:])
train_y=np.array(trainFile['train_set_y'][:])

test_x=np.array(testFile['test_set_x'][:])
test_y=np.array(testFile['test_set_y'][:])


# In[ ]:


print(train_x.shape)
print(train_y.shape)
print(test_x.shape)
print(test_y.shape)


# In[ ]:


train_y=train_y.reshape(1,train_y.shape[0])
test_y=test_y.reshape(1,test_y.shape[0])


# In[ ]:


print(train_y.shape)
print(test_y.shape)


# In[ ]:


plt.imshow(train_x[0])


# In[ ]:


x_train=train_x/255
x_test=test_x/255

y_train = train_y.T
y_test = test_y.T


# In[ ]:


print(train_x)


# In[ ]:


print(x_train)


# In[ ]:


print(train_y)


# In[ ]:


print(test_y)


# In[ ]:


model=Sequential()

model.add(Conv2D(filters=32, kernel_size=(3,3), activation='relu', padding='Same', input_shape=(64,64,3)))
model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='Same'))

model.add(MaxPool2D(pool_size=(2,2)))

model.add(Conv2D(filters=128, kernel_size=(3,3), activation='relu', padding='Same'))

model.add(MaxPool2D(pool_size=(2,2)))

model.add(Flatten())

model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))


# In[ ]:



model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])


# In[ ]:


epochs = 30
batch_size = 30


# In[ ]:


history = model.fit(x=x_train, y=y_train, epochs=epochs, verbose=2,batch_size=batch_size)


# In[ ]:


test_score = model.evaluate(x_test, y_test, verbose=1)


# In[ ]:


print('test loss:', test_score[0])
print('test accuracy:', test_score[1])


# In[ ]:


training_accuracy = history.history['acc']
training_loss = history.history['loss']

E = range(len(training_accuracy))
plt.plot(E, training_accuracy, color='red', label='Training accuracy')
plt.title('epochs vs Training accuracy')
plt.legend()

plt.figure()
plt.plot(E, training_loss, color='red', label='Training Loss')
plt.title('epochs vs Training Loss')
plt.legend()


# In[ ]:




