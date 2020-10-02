#!/usr/bin/env python
# coding: utf-8

# # **1. CNN from scratch**
# # **2. VGG16**
# # **3. Mobile Net**
# # **4. Xception**

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import keras
from keras import layers
from keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D
from keras.models import Model

        
import keras.backend as K
K.set_image_data_format('channels_last')

from matplotlib.pyplot import imshow
from keras.preprocessing import image
from keras import applications
from keras.models import Sequential
import os,sys
import warnings
warnings.simplefilter("ignore")

import cv2
from keras.preprocessing.image import ImageDataGenerator


# In[ ]:


img = cv2.imread('../input/training/training/n9/n919.jpg')
print(img.shape)
img1 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
plt.imshow(img1)


# In[ ]:


train_dir = '../input/training/training/'
valid_dir = '../input/validation/validation/'


# In[ ]:


# Training generator
train_datagen = ImageDataGenerator( 
    width_shift_range=0.1,  # randomly shift images horizontally (10% of total width)
    height_shift_range=0.1,  # randomly shift images vertically (10% of total height)
    rotation_range=40,
    zoom_range = 0.1,
    rescale=1./255)
train_generator = train_datagen.flow_from_directory(
    directory=train_dir,
    target_size=(224, 224),
    color_mode="rgb",
    batch_size=64,
    class_mode="categorical",
    shuffle=True,
    seed=42
)

# Valid generator

valid_datagen = ImageDataGenerator(rescale=1./255)
valid_generator = valid_datagen.flow_from_directory(
    directory=valid_dir,
    target_size=(224, 224),
    color_mode="rgb",
    batch_size=32,
    class_mode="categorical",
    shuffle=True,
    seed=42
)


# # **1. Create our own CNN from scratch**

# In[ ]:


model = Sequential()
model.add(BatchNormalization(input_shape=(224, 224, 3)))
model.add(Conv2D(filters=16, kernel_size=3, activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(BatchNormalization())

model.add(Conv2D(filters=32, kernel_size=3, activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(BatchNormalization())

model.add(Conv2D(filters=64, kernel_size=3, activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(BatchNormalization())

model.add(Conv2D(filters=128, kernel_size=3, activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(BatchNormalization())

model.add(Conv2D(filters=256, kernel_size=3, activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(BatchNormalization())

model.add(GlobalAveragePooling2D())

model.add(Dense(10, activation='softmax'))

model.summary()


# In[ ]:


from keras import optimizers
from keras.callbacks import ReduceLROnPlateau

optimizer = optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0)


# In[ ]:


model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])


# In[ ]:


learning_rate_reduction = ReduceLROnPlateau(monitor='val_acc', 
                                            patience=2, 
                                            verbose=1, 
                                            factor=0.5, 
                                            min_lr=0.00001)


# In[ ]:


STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size
STEP_SIZE_VALID=valid_generator.n//valid_generator.batch_size


# In[ ]:


model.fit_generator(generator=train_generator,
                    steps_per_epoch=STEP_SIZE_TRAIN,
                    validation_data=valid_generator,
                    validation_steps=STEP_SIZE_VALID,
                    epochs=10,
                    verbose=1,
                    callbacks=[learning_rate_reduction]
)


# # **2. VGG 16**

# In[ ]:


from keras.applications import vgg16


# In[ ]:


vgg16_model = vgg16.VGG16(weights='imagenet')


# In[ ]:


vgg16_model.summary()


# In[ ]:


model2 = Sequential()
for layer in vgg16_model.layers[:-1]:
    model2.add(layer)


# In[ ]:


for layer in model2.layers:
    layer.trainable = False


# In[ ]:


model2.add(Dense(10, activation='softmax'))


# In[ ]:


model2.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


# In[ ]:


model2.fit_generator(generator=train_generator,
                    steps_per_epoch=STEP_SIZE_TRAIN,
                    validation_data=valid_generator,
                    validation_steps=STEP_SIZE_VALID,
                    epochs=10,
                    verbose=1,
                    callbacks=[learning_rate_reduction]
)


# # **3. Mobile Net**

# In[ ]:


mobile = keras.applications.mobilenet.MobileNet()


# In[ ]:


mobile.summary()


# In[ ]:


mobile_tune = Sequential()
for layer in mobile.layers:
    mobile_tune.add(layer)


# In[ ]:


mobile_tune.add(Dense(10, activation='softmax'))


# In[ ]:


for layer in mobile_tune.layers[:-5]:
    layer.trainable = False


# In[ ]:


mobile_tune.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])


# In[ ]:


mobile_tune.fit_generator(generator=train_generator,
                    steps_per_epoch=STEP_SIZE_TRAIN,
                    validation_data=valid_generator,
                    validation_steps=STEP_SIZE_VALID,
                    epochs=10,
                    verbose=1,
                    callbacks=[learning_rate_reduction]
)


# # **5. Xception**

# In[ ]:


from keras.applications.xception import Xception


# In[ ]:


base_model = Xception(weights='imagenet', include_top=False)
base_model.summary()


# In[ ]:


# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(1024, activation='relu')(x)
# and a logistic layer -- let's say we have 200 classes
predictions = Dense(10, activation='softmax')(x)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = False
    
# this is the model we will train
xception = Model(inputs=base_model.input, outputs=predictions)


# In[ ]:


xception.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])


# In[ ]:


xception.fit_generator(generator=train_generator,
                    steps_per_epoch=STEP_SIZE_TRAIN,
                    validation_data=valid_generator,
                    validation_steps=STEP_SIZE_VALID,
                    epochs=10,
                    verbose=1,
                    callbacks=[learning_rate_reduction]
)

