#!/usr/bin/env python
# coding: utf-8

# ## Classification of Flower image
# 
# This dataset contain image of different type of flower , there are five type flowers.
# * Sunflower
# * Tulip
# * Daisy
# * Rose
# * Dandelion
# 
# Here to to solve this Classification problem we will create a CNN model and train it with given image dataset, then we will take some image from dataset and try to predict its accuracy.

# In[ ]:


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from PIL import  Image
get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('fivethirtyeight')

from PIL import Image
# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from tensorflow.contrib.keras.api.keras.callbacks import Callback
from tensorflow.contrib.keras.api.keras.preprocessing.image import ImageDataGenerator
from tensorflow.contrib.keras import backend
from keras.optimizers import Adam

import os

print(os.listdir("../input/flowers/flowers/"))


# In[ ]:



script_dir = os.path.dirname(".")
training_set_path = os.path.join(script_dir, '../input/flowers/flowers/')
test_set_path = os.path.join(script_dir, '../input/flowers/flowers/')


# # Initialising the CNN
# 

# In[ ]:


classifier = Sequential()


# # Step 1 - Convolution

# In[ ]:


input_size = (256, 256)
classifier.add(Conv2D(32, (3, 3), input_shape=(256,256,3), activation='relu'))


# # Step 2 - Pooling

# In[ ]:


classifier.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))


# # Adding a second convolutional layer
# 

# In[ ]:


classifier.add(Conv2D(32, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))


# # Adding a third convolutional layer
# 

# In[ ]:


classifier.add(Conv2D(64, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))


# # Step 3 - Flattening
# 

# In[ ]:


classifier.add(Flatten())


# # Step 4 - Full connection
# 

# In[ ]:


classifier.add(Dense(units=64, activation='relu'))
classifier.add(Dropout(0.5))
classifier.add(Dense(units=5, activation='softmax'))


# # Compiling the CNN
# 

# In[ ]:


opt = Adam(lr=1e-3, decay=1e-6)
classifier.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])


# # Data preprocessing
# Read  image data and split it in two part training and test.
# 
# 

# In[ ]:


batch_size = 32

train_datagen = ImageDataGenerator(rescale=1. / 255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255, validation_split=0.33)

training_set = train_datagen.flow_from_directory(training_set_path,
                                                 target_size=input_size,
                                                 batch_size=batch_size,
                                                 subset="training",
                                                 class_mode='categorical')



test_set = test_datagen.flow_from_directory(test_set_path,
                                            target_size=input_size,
                                            batch_size=batch_size,
                                            subset="validation",
                                            class_mode='categorical')


# # Summary
# 

# In[ ]:



classifier.summary()


# 
# # Part 2 - Fitting the CNN to the images

# In[ ]:




model_info = classifier.fit_generator(training_set,
                         steps_per_epoch=1000/batch_size,
                         epochs=90,
                         validation_data=test_set,
                         validation_steps=100/batch_size,
                         workers=12)


# 
# 

# ##  Accuracy or Loss as a Function of Number of Epoch
# 

# In[ ]:


def plot_model_history(model_history):
    fig, axs = plt.subplots(1,2,figsize=(15,5))
    # summarize history for accuracy
    axs[0].plot(range(1,len(model_history.history['acc'])+1),model_history.history['acc'])
    axs[0].plot(range(1,len(model_history.history['val_acc'])+1),model_history.history['val_acc'])
    axs[0].set_title('Model Accuracy')
    axs[0].set_ylabel('Accuracy')
    axs[0].set_xlabel('Epoch')
    axs[0].set_xticks(np.arange(1,len(model_history.history['acc'])+1),len(model_history.history['acc'])/10)
    axs[0].legend(['train', 'val'], loc='best')
    # summarize history for loss
    axs[1].plot(range(1,len(model_history.history['loss'])+1),model_history.history['loss'])
    axs[1].plot(range(1,len(model_history.history['val_loss'])+1),model_history.history['val_loss'])
    axs[1].set_title('Model Loss')
    axs[1].set_ylabel('Loss')
    axs[1].set_xlabel('Epoch')
    axs[1].set_xticks(np.arange(1,len(model_history.history['loss'])+1),len(model_history.history['loss'])/10)
    axs[1].legend(['train', 'val'], loc='best')
    plt.show()


# In[ ]:


plot_model_history(model_info)


# That's all i have. I hope you enjoyed this.  if you find this kernel helpful, please upvote.

# In[ ]:




