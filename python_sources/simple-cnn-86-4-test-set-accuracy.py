#!/usr/bin/env python
# coding: utf-8

# # CNN for Image Classification

# **Hey Kagglers,
# Classification is done by Convutional Neural Network
# First we are importing the libraries**

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory


# Any results you write to the current directory are saved as output.


# In[ ]:


import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import matplotlib.image as mig


# # Setting Path for Datasets

# In[ ]:


import pathlib
PATH = '../input/intel-image-classification/seg_train/seg_train'
data_dir = pathlib.Path(PATH)
test_path = '../input/intel-image-classification/seg_test/seg_test'
test_data_dir = pathlib.Path(test_path)


# # Classes
# **Defining Class Names from folder names **
# In the dataset each folder contains images of a particular class 
# and folder name is same as class name so we extract classname from folder name 

# In[ ]:


CLASS_NAMES = np.array([item.name for item in data_dir.glob('*') if item.name != "LICENSE.txt"])
CLASS_NAMES


# # Train Data and Augmenting Train Data
# Augmenting Training Data for more distorted images to get more variety 
# this augmentation is done by ImageDataGenerator and its method flow_from_directory
# Here augmented images are produced and replaces original Image
# flow_from_directory produces a object which contains images and label batches
# In ImageDataGenerator we also split data into train data and validaton Data

# In[ ]:


from tensorflow.keras.preprocessing.image import ImageDataGenerator
IDG = ImageDataGenerator(rescale = 1./255, validation_split=0.2,
                         rotation_range=10,
    zoom_range = 0.1,
    width_shift_range=0.1,
    height_shift_range=0.1,)

train_data = IDG.flow_from_directory(PATH,target_size=(150,150),batch_size=64,classes = list(CLASS_NAMES),subset='training')
validation_data = IDG.flow_from_directory(PATH,target_size=(150,150),batch_size=64,classes = list(CLASS_NAMES),subset='validation')


# **Producing test data without augmenting**

# In[ ]:


from tensorflow.keras.preprocessing.image import ImageDataGenerator
IDG_test = ImageDataGenerator(rescale = 1./255)
test_data = IDG_test.flow_from_directory(test_path,target_size=(150,150),batch_size=64,classes = list(CLASS_NAMES))


#  **Function for Ploting a batch of image along with its label**

# In[ ]:


def show_batch(image_batch, label_batch):
  plt.figure(figsize=(10,10))
  for n in range(25):
      ax = plt.subplot(5,5,n+1)
      plt.imshow(image_batch[n])
      plt.title(CLASS_NAMES[label_batch[n].argmax()])
      plt.axis('off')
     


# In[ ]:


image_batch, label_batch = next(train_data)
show_batch(image_batch, label_batch)


# # **Convutional Neural Network Architecture**

# In[ ]:


from keras.models import Sequential
from keras import layers
from keras.layers import BatchNormalization
from keras import regularizers
model = Sequential()
##Convutional Layers
model.add(layers.Conv2D(32, (3, 3),input_shape=(150,150,3)))

model.add(layers.Activation('relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))

model.add(layers.Conv2D(32, (3, 3)))

model.add(layers.Activation('relu'))

model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(64, (3, 3)))

model.add(layers.Activation('relu'))

model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(128, (3, 3)))

model.add(layers.Activation('relu'))

model.add(layers.MaxPooling2D(pool_size=(2, 2)))

##Fully Conneted Layers

model.add(layers.Flatten())
model.add(layers.Dense(256,activation='relu'))
model.add(layers.Dropout(.5))
model.add(layers.Dense(100,activation='relu'))
model.add(layers.Dropout(.5))
model.add(layers.Dense(len(CLASS_NAMES),activation='softmax'))


# In[ ]:


model.summary()


# # COMPILING AND TRAINING
# Training is done by adam optimizer with 25 epochs

# In[ ]:


model.compile(optimizer='adam', loss=tf.keras.losses.categorical_crossentropy, metrics=['accuracy'])
history = model.fit_generator(train_data, epochs=25, steps_per_epoch = train_data.samples//64, validation_data=validation_data, validation_steps = validation_data.samples//64)


# # Learning Curves
# **Loss and Accuracy curve for train and validation data**

# In[ ]:


plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()


# # Predicting Images

# In[ ]:


plt.figure(figsize=(20,20))
#for _ in range(3):
sam_x,sam_y = next(test_data) 
pred_ = model.predict(sam_x)
for i in range(15):
    pred,y = pred_[i].argmax(), sam_y[i].argmax()
    plt.subplot(4,4,i+1)
    plt.imshow(sam_x[i])
    title_ = 'Predict:' + str(CLASS_NAMES[pred])+ ';   Label:' + str(CLASS_NAMES[y])
    plt.title(title_,size=11)
plt.show()


# # Testing using test data

# In[ ]:


model.evaluate(test_data)


# # Saving Model

# In[ ]:


model.save_weights("model.h5")

