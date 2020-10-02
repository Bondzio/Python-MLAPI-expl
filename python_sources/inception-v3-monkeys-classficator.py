#!/usr/bin/env python
# coding: utf-8

# # About
# This is a deep learning kernel to use Inception v3 pretrained model to train the classificators for monkeys. 
# - keras
# - tensorflow
# - inception v3
# 
# It is also my assignment for machine learning paper at uni.
# 
# 
# 

# # Preparation
# 

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


train_dir = '../input/10-monkey-species/training/training/'
val_dir = '../input/10-monkey-species/validation/validation/'


# In[ ]:




labels = pd.read_csv("../input/10-monkey-species/monkey_labels.txt")
num_classes = labels['Label'].size
labels


# In[ ]:


# for display images in notebook
from IPython.display import Image, display

from os import listdir
get_ipython().run_line_magic('matplotlib', 'inline')


# # Data Augmetation

# In[ ]:


IMAGE_WIDTH = 150
IMAGE_HEIGHT = 150
BATCH_SIZE = 24


# In[ ]:


from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.applications.inception_v3 import preprocess_input


## use inception's own preprocess function
train_data_gen_aug=ImageDataGenerator(
                              preprocessing_function=preprocess_input,
                              rotation_range=20,
                              width_shift_range=0.2,
                              height_shift_range=0.2,
#                               shear_range=0.2,
#                               horizontal_flip=True,
#                               fill_mode='nearest' # default is nearest
                             )

validation_data_gen=ImageDataGenerator(
                                       preprocessing_function=preprocess_input
                                      )


# In[ ]:


train_gen=train_data_gen_aug.flow_from_directory(train_dir,
                                            target_size=(IMAGE_WIDTH,
                                                       IMAGE_HEIGHT),
                                            batch_size=BATCH_SIZE,
                                            shuffle=True,
                                            class_mode="categorical")
val_gen = validation_data_gen.flow_from_directory(val_dir, 
                                                    target_size=(IMAGE_WIDTH, IMAGE_HEIGHT), 
                                                    batch_size = BATCH_SIZE, 
                                                    class_mode="categorical")


# In[ ]:


train_count=1097
val_count=272
steps_per_epoch=train_count//BATCH_SIZE
steps_per_epoch


# ## Set up Model

# In[ ]:


from keras.applications import InceptionV3
from keras.models import Sequential
from keras.layers import Dense, GlobalAveragePooling2D, Dropout

# set  up the model
model=Sequential()
# add inception pretrained model, the wieghts 80Mb
model.add(InceptionV3(include_top=False, 
                      pooling='avg', 
                      weights='../input/inceptionv3/inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5'
                     ))
# use relu as activation function "vanishing gradiends" :)
# model.add(Dense(2048, activation="relu"))  
# # add drop out to avoid overfitting
# model.add(Dropout(0.25))
model.add(Dense(num_classes, activation="softmax"))


# In[ ]:


# we should keep trainable layers as less than possible to speed up
# for layer in model.layers[0].layers:
#     layer.trainable= False
       
    
model.layers[0].trainable=False


# In[ ]:


# for layer in model.layers[0].layers:
#     print(layer, layer.trainable)


# In[ ]:


model.summary()


# # Compile then Fit the model

# In[ ]:



from keras import optimizers
adam = optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.00001)
# use adam to avoid overfitting

model.compile(loss="categorical_crossentropy",
              optimizer=adam,
              metrics=["accuracy"])


# In[ ]:


model_history = model.fit_generator(train_gen,
                                    steps_per_epoch=steps_per_epoch,
                                    epochs=48,
                                    validation_data=val_gen,
                                    validation_steps=val_count // BATCH_SIZE
                                   )


# In[ ]:


model.save('incept_adv.h5') 


# # Show the results

# In[ ]:


import pandas as pd
history = pd.DataFrame()
history["acc"] = model_history.history["acc"]
history["val_acc"] = model_history.history["val_acc"]
history.plot(figsize=(12, 6))


# In[ ]:


acc = model_history.history['acc']
val_acc = model_history.history['val_acc']
loss = model_history.history['loss']
val_loss = model_history.history['val_loss']
epochs = range(1, len(acc) + 1)

import matplotlib.pyplot as plt

plt.title('Training and validation accuracy')
plt.plot(epochs, acc, 'red', label='Training acc')
plt.plot(epochs, val_acc, 'blue', label='Validation acc')
plt.legend()

plt.figure()
plt.title('Training and validation loss')
plt.plot(epochs, loss, 'red', label='Training loss')
plt.plot(epochs, val_loss, 'blue', label='Validation loss')

plt.legend()

plt.show()


# **Credits:**
# 1. Dan Becker https://www.kaggle.com/learn
# 2. Juan https://www.kaggle.com/moriano/monkey-species-transfer-learning-95-6-accuracy
# 3. Dan Rusei https://www.kaggle.com/danrusei/10-monkey-keras-transfer-learning-resnet50
