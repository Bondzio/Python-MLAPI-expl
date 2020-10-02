#!/usr/bin/env python
# coding: utf-8

# # CNN Stanford Cars using Keras Alexnet

# ## Table Content
# 
# * [Data Exploratory](#exploratory)
# * [Data Selection](#selection)
# * [Data Split](#split)
# * [Implementation](#implementation)
# * [Analyze](#analyze)
# * [Prediction](#prediction)
# * [Reference](#reference)

# # Goal
# 
# The goal of this notebook is simply to show the implementation of the AlexNet and train a model to predict certain types of Cars
# 
# ## Definition
# 
# AlexNet is the name of a convolutional neural network (CNN), designed by Alex Krizhevsky, and published with Ilya Sutskever and Krizhevsky's doctoral advisor Geoffrey Hinton.
# 
# AlexNet competed in the ImageNet Large Scale Visual Recognition Challenge on September 30, 2012. The network achieved a top-5 error of 15.3%, more than 10.8 percentage points lower than that of the runner up. The original paper's primary result was that the depth of the model was essential for its high performance, which was computationally expensive, but made feasible due to the utilization of graphics processing units (GPUs) during training.
# 
# https://en.wikipedia.org/wiki/AlexNet

# <a id='exploratory'></a>
# # Data Exploratory

# In[ ]:


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import glob
import cv2


# In[ ]:


import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Activation, MaxPool2D, BatchNormalization, Flatten, Dense, Dropout
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.optimizers import SGD


# In[ ]:


names = pd.read_csv('../input/stanford-car-dataset-images-in-224x224/stanford-car-dataset-by-classes-folder-224/names.csv')
names = names.values


# In[ ]:


np.random.shuffle(names)


# <a id='selection'></a>
# # Data Selection
# 
# Select only a limited amount of cars to train on just because Kaggle does not support to train on all data at the same time.

# In[ ]:


nr_cars = 10


# In[ ]:


idx_to_name = {x : names[x][0] for x in np.arange(nr_cars)}
name_to_idx = {x:i for i,x in enumerate(idx_to_name.values())}


# In[ ]:


idx_to_name


# In[ ]:


train_path = '../input/stanford-car-dataset-images-in-224x224/stanford-car-dataset-by-classes-folder-224/car_data/train/'
test_path = '../input/stanford-car-dataset-images-in-224x224/stanford-car-dataset-by-classes-folder-224/car_data/test/'


# In[ ]:


def get_data(path):
    train = []
    for i, name in enumerate(name_to_idx.keys()):
        new_path = path + name + "/"
        [train.append([i, cv2.resize(cv2.imread(img), (244,244), interpolation = cv2.INTER_AREA)]) for img in glob.glob(new_path + "*.jpg")]
    return np.array(train)


# In[ ]:


train = get_data(train_path)
test = get_data(test_path)


# <a id='split'></a>
# # Data split

# In[ ]:


X_train = np.concatenate(train[:,1], axis=0).reshape(len(train), 244, 244, 3)
X_train = X_train / 255.0
X_train = X_train.astype('float32')
y_train = train[:,0]
y_train = np.eye(len(idx_to_name))[list(y_train)]

X_test = np.concatenate(test[:,1], axis=0).reshape(len(test), 244, 244, 3)
X_test = X_test / 255.0
X_test = X_test.astype('float32')
y_test = test[:,0]
y_test = np.eye(len(idx_to_name))[list(y_test)]


# <a id='implementation'></a>
# # Implementation

# <img align=left src='https://dpzbhybb2pdcj.cloudfront.net/elgendy/v-8/Figures/05-06_img_0050.png'>

# In[ ]:


# Instantiate an empty sequential model
model = Sequential(name="Alexnet")
# 1st layer (conv + pool + batchnorm)
model.add(Conv2D(filters= 96, kernel_size= (11,11), strides=(4,4), padding='valid', kernel_regularizer=l2(0.0005),
input_shape = (227,227,3)))
model.add(Activation('relu'))  #<---- activation function can be added on its own layer or within the Conv2D function
model.add(MaxPool2D(pool_size=(3,3), strides= (2,2), padding='valid'))
model.add(BatchNormalization())
    
# 2nd layer (conv + pool + batchnorm)
model.add(Conv2D(filters=256, kernel_size=(5,5), strides=(1,1), padding='same', kernel_regularizer=l2(0.0005)))
model.add(Activation('relu'))
model.add(MaxPool2D(pool_size=(3,3), strides=(2,2), padding='valid'))
model.add(BatchNormalization())
            
# layer 3 (conv + batchnorm)      <--- note that the authors did not add a POOL layer here
model.add(Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), padding='same', kernel_regularizer=l2(0.0005)))
model.add(Activation('relu'))
model.add(BatchNormalization())
        
# layer 4 (conv + batchnorm)      <--- similar to layer 3
model.add(Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), padding='same', kernel_regularizer=l2(0.0005)))
model.add(Activation('relu'))
model.add(BatchNormalization())
            
# layer 5 (conv + batchnorm)  
model.add(Conv2D(filters=256, kernel_size=(3,3), strides=(1,1), padding='same', kernel_regularizer=l2(0.0005)))
model.add(Activation('relu'))
model.add(BatchNormalization())
model.add(MaxPool2D(pool_size=(3,3), strides=(2,2), padding='valid'))

# Flatten the CNN output to feed it with fully connected layers
model.add(Flatten())

# layer 6 (Dense layer + dropout)  
model.add(Dense(units = 4096, activation = 'relu'))
model.add(Dropout(0.5))

# layer 7 (Dense layers) 
model.add(Dense(units = 4096, activation = 'relu'))
model.add(Dropout(0.5))
                           
# layer 8 (softmax output layer) 
model.add(Dense(units = len(y_train[0]), activation = 'softmax'))

# print the model summary
model.summary()


# In[ ]:


# reduce learning rate by 0.1 when the validation error plateaus
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=np.sqrt(0.1))
 
# set the SGD optimizer with lr of 0.01 and momentum of 0.9
optimizer = SGD(lr = 0.01, momentum = 0.9)
 
# compile the model
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])


# In[ ]:


# train the model
# call the reduce_lr value using callbacks in the training method
with tf.device('/GPU:0'):
    history = model.fit(X_train, y_train, batch_size=32, epochs=100, validation_data=(X_test, y_test),
    verbose=0, callbacks=[reduce_lr])


# <a id='analyze'></a>
# # Analyze training history

# In[ ]:


plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()


# <a id='prediction'></a>
# # Prediction

# In[ ]:


def predict(img):
    to_predict = np.zeros(shape=X_train.shape)
    to_predict[0] = img
    
    return idx_to_name[np.argmax(model(to_predict)[0])]


# In[ ]:


predict(X_train[100])


# In[ ]:


plt.imshow(X_train[100])


# <a id='reference'></a>
# # Reference
# 
# AlexNet kaggle layers design and architecture image:<br>
# https://www.manning.com/books/deep-learning-for-vision-systems
