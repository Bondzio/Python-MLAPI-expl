#!/usr/bin/env python
# coding: utf-8

# Needless to say, the first thing to do is always importing the data.

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # plot drawing
from tensorflow import keras #import google tensorflow.keras, which we may use later
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


train = pd.read_csv("../input/digit-recognizer/train.csv")
test = pd.read_csv("../input/digit-recognizer/test.csv")
#deal with training data 
x=train.drop(["label"],axis=1)
x=x.iloc[:,:].values
x=x.reshape(42000,28,28,1)
#deal with test data
test=test.iloc[:,:].values
test=test.reshape(28000,28,28,1)
#normalize the data.
x, test= x/255.0,test/255.0
#Get the training labels
y=train.label.iloc[:].values


# # BatchNormalization
# 
# The procedure of neuro network(from my understanding, __pleas point out if I am wrong, it is really important for me__) is:
# 1. Select a batch, put them togethor in to the input layer;
# 2. Simultaneously play the BackPropagation through the network, and add the effect of them together to determine the next position of gradient descent.
# 3. Return to 1 until we finish our epoch.

# In[ ]:


#The whole "building" of neuronetwork
Sequential=keras.Sequential
#Now we choose "who will be moved into" each layer
#possible Candidates are:
#Use different filters to get different channels.
Conv2D=keras.layers.Conv2D
#Pooling, select Maximum value from a certain pool.
MaxPool2D=keras.layers.MaxPool2D
#a flat ANN layer
Dense=keras.layers.Dense
#as it suggests, flatten: \mathbb{R}^2 \to \mathbb{R}
Flatten=keras.layers.Flatten
#Randomly select a chosen percentage of neurons and remove them temporarily
Dropout=keras.layers.Dropout
#BarchNormalization, "Centralize" the batch.(randomly chose a noise on sigma is available)
BatchNormalization=keras.layers.BatchNormalization


# Build the architecture of two models, one is a batch normalized model and a non batch normalized model

# In[ ]:


def BN_model():
    model=Sequential()
    model.add(Conv2D(filters = 32, kernel_size = (3,3),padding = 'same', 
                 activation ='relu', input_shape = (28,28,1)))
    model.add(Conv2D(filters = 32, kernel_size = (3,3),padding = 'same', 
                 activation ='relu', input_shape = (28,28,1)))
    model.add(BatchNormalization())
    model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
    model.add(Dropout(0.3))
    model.add(Conv2D(filters = 64, kernel_size = (3,3),padding = 'same', 
                 activation ='relu', input_shape = (28,28,1)))
    model.add(Conv2D(filters = 64, kernel_size = (3,3),padding = 'same', 
                 activation ='relu', input_shape = (28,28,1)))
    model.add(BatchNormalization())
    model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
    model.add(Dropout(0.3))
    model.add(Conv2D(filters = 128, kernel_size = (3,3),padding = 'same', 
                 activation ='relu'))
    model.add(Conv2D(filters = 128, kernel_size = (3,3),padding = 'same', 
                 activation ='relu'))
    model.add(BatchNormalization())
    model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
    model.add(Dropout(0.3))
    model.add(Flatten())
    model.add(Dense(256, activation = "relu"))
    model.add(Dropout(0.3))
    model.add(Dense(10, activation = "softmax"))
    model.compile(keras.optimizers.Adam(0.0001), 
             loss="sparse_categorical_crossentropy",
              metrics=["accuracy"]
             )
    return model


# In[ ]:


def NBN_model():
    model=Sequential()
    model.add(Conv2D(filters = 32, kernel_size = (3,3),padding = 'same', 
                 activation ='relu', input_shape = (28,28,1)))
    model.add(Conv2D(filters = 32, kernel_size = (3,3),padding = 'same', 
                 activation ='relu', input_shape = (28,28,1)))
    model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
    model.add(Dropout(0.3))
    model.add(Conv2D(filters = 64, kernel_size = (3,3),padding = 'same', 
                 activation ='relu', input_shape = (28,28,1)))
    model.add(Conv2D(filters = 64, kernel_size = (3,3),padding = 'same', 
                 activation ='relu', input_shape = (28,28,1)))
    model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
    model.add(Dropout(0.3))
    model.add(Conv2D(filters = 128, kernel_size = (3,3),padding = 'same', 
                 activation ='relu'))
    model.add(Conv2D(filters = 128, kernel_size = (3,3),padding = 'same', 
                 activation ='relu'))
    model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
    model.add(Dropout(0.3))
    model.add(Flatten())
    model.add(Dense(256, activation = "relu"))
    model.add(Dropout(0.3))
    model.add(Dense(10, activation = "softmax"))
    model.compile(keras.optimizers.Adam(0.0001), 
             loss="sparse_categorical_crossentropy",
              metrics=["accuracy"]
             )
    return model


# In[ ]:


#Finish building up 2 model's architecture
Bmodel=BN_model()
Nmodel=NBN_model()


# In[ ]:


from tensorflow.keras.preprocessing.image import ImageDataGenerator
#Considering to do data augumentation
datagen = ImageDataGenerator(
        rotation_range=10,  
        zoom_range = 0.10,  
        width_shift_range=0.1, 
        height_shift_range=0.1)


# In[ ]:


from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.1)


# In[ ]:


history_B = Bmodel.fit_generator(datagen.flow(x_train,y_train, batch_size=20),
                                 epochs = 45, 
                                 validation_data=(x_test,y_test),
                                 validation_steps=210,
                                 verbose = 1, steps_per_epoch=x.shape[0] / 20)


# In[ ]:


history_N = Nmodel.fit_generator(datagen.flow(x_train,y_train, batch_size=20),
                                 epochs = 45, 
                                 validation_data=(x_test,y_test),
                                 validation_steps=210,
                                 verbose = 1, steps_per_epoch=x.shape[0] / 20)


# In[ ]:


# Plot training & validation accuracy values
plt.plot(history_B.history['acc'])
plt.plot(history_B.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history_B.history['loss'])
plt.plot(history_B.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()


# In[ ]:


# Plot training & validation accuracy values
plt.plot(history_N.history['acc'])
plt.plot(history_N.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history_N.history['loss'])
plt.plot(history_N.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()


# In[ ]:


predictionsB=Bmodel.predict_classes(test)
predictionsN=Nmodel.predict_classes(test)


# In[ ]:


ids=np.arange(28000)+1
output=pd.DataFrame({"ImageId":ids, "Label":predictionsB})
output.to_csv("submissionB.csv",index=False)
output=pd.DataFrame({"ImageId":ids, "Label":predictionsN})
output.to_csv("submissionN.csv",index=False)

