#!/usr/bin/env python
# coding: utf-8

#  **Using Desnsnet201 with Tranfser Learning on MIT Indoor 67** dataset

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from keras.preprocessing import image
from keras.models import Sequential
from keras.models import Model
from keras.utils import Sequence
from keras.layers import Dense, GlobalAveragePooling2D, Dropout, Input, Flatten
from keras.preprocessing.image import ImageDataGenerator

from keras import backend as K
K.set_image_dim_ordering('tf')

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory



# Any results you write to the current directory are saved as output.


# 

# In[2]:


#import os
import os
print(os.listdir("../input"))
print (os.listdir("../input/test/test"))

train_data_dir ='../input/train/train'
validation_data_dir = '../input/test/test'


# **Preparing Data Using Data Augmentation**
# 

# In[3]:


#Inception input size and input image target size
batch_size = 32
img_width, img_height = 224, 224

# prepare data augmentation configuration
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

test_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')


# **Importing DenseNet201**
# - Using pretrained imagenet weight and setting top to false
# - We can call the .summary( ) function on the model we downloaded to see its architecture and number of parameters. 

# In[4]:


from keras.applications.densenet import DenseNet201
pretrained_model = DenseNet201(weights='imagenet', include_top=False, input_shape=(224,224,3))
pretrained_model.summary()


# In[5]:



from keras import layers
from keras import models

top_model = models.Sequential()
top_model.add(Flatten(input_shape=pretrained_model.output_shape[1:]))
# model.add(pretrained_model)
#top_model.add(layers.Flatten())
top_model.add(layers.Dense(512, activation='relu'))
top_model.add(Dropout(0.5))
top_model.add(layers.Dense(256, activation='relu'))
top_model.add(Dropout(0.5))
top_model.add(layers.Dense(67, activation='softmax'))
model = Model(input= pretrained_model.input, output= top_model(pretrained_model.output))
model.summary()


# In[7]:


from keras import optimizers
model.compile(optimizer=optimizers.SGD(lr=0.00002, momentum=0.9), loss='categorical_crossentropy', metrics=['accuracy'], )
#model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'], )

epochs = 120
batch_size =128
nb_train_samples = 5361
nb_validation_samples = 1340


# fine-tune the model
model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=test_generator,
    validation_steps=nb_validation_samples // batch_size)


# In[8]:


for i, layer in enumerate(pretrained_model.layers):
  print(i, layer.name)
#freeze the first 704 layers and unfreeze the rest:
for layer in model.layers[:704]:
   layer.trainable = False
for layer in model.layers[704:]:
   layer.trainable = True


# In[ ]:


from keras import optimizers
# model.compile(optimizer=optimizers.RMSprop(lr=0.0001), loss='categorical_crossentropy', metrics=['accuracy'], )

model.compile(optimizer=optimizers.SGD(lr=0.00005, momentum=0.9), loss='categorical_crossentropy', metrics=['accuracy'], )


epochs = 30
batch_size = 128
nb_train_samples = 5361 
nb_validation_samples = 1340

# fine-tune the model
model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=test_generator,
    validation_steps=nb_validation_samples // batch_size)

