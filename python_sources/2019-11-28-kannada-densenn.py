#!/usr/bin/env python
# coding: utf-8

# ### Setup & Imports

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


path = '../input/Kannada-MNIST/'


# In[ ]:


import matplotlib.pyplot as plt
from PIL import Image


# In[ ]:


from keras.utils import to_categorical

from keras.models import Sequential
from keras.layers import Dense

from keras.callbacks import EarlyStopping


# ### Data loading & inspection

# ##### helper functions

# In[ ]:


"""
helper function to show a number of randomly selected images 
belonging either to a specified label or selected across all labels
"""

def show_random_images(images, num=10, label=None):

    # generating images' subsample if label specified
    if label is not None:
        images = images[images.label == label]
    
    fig, axs = plt.subplots(num, figsize=(1.25, num * 2.5))
    
    for i in range(num):
    
        rnd = np.random.randint(len(images))
    
        # getting image data and splitting between label and pixels' vector
        img_data = np.array(images.iloc[rnd], dtype='uint8')    
        img_label = img_data[0]
        img_pixels = img_data[1:]
        
        # reshaping image to 2D array
        img_shape = (int(np.sqrt(img_pixels.shape[0])), int(np.sqrt(img_pixels.shape[0])))
        img_array = img_pixels.reshape(img_shape)
        
        title = 'Image {} / labelled {}'.format(rnd, img_label)
        
        axs[i].imshow(img_array, alpha=0.66, cmap='gray')
        axs[i].set_title(title)


# #### "train.csv"

# In[ ]:


train_data = pd.read_csv(path + 'train.csv')
train_data


# In[ ]:


# checking labels distribution

train_data.label.value_counts()


# In[ ]:


show_random_images(train_data, num=5, label=5)


# #### "Dig-MNIST.csv"

# In[ ]:


dig_data = pd.read_csv(path + 'Dig-MNIST.csv')
dig_data


# In[ ]:


# checking labels distribution

dig_data.label.value_counts()


# In[ ]:


show_random_images(dig_data, num=5, label=5)


# ### Data preparation

# ##### Helper functions

# In[ ]:


# helper function to show randomly selected image from 2D images array

def show_random_image(imgset):
    
    rnd = np.random.randint(imgset.shape[0])
    imgarray = imgset[rnd]
    plt.figure(figsize=(1.5, 1.5))
    plt.imshow(imgarray, cmap='gray')


# #### Preparing "train" images

# In[ ]:


# preparing train image labels using 'one-hot' encoding

train_labels = to_categorical(train_data.label)
train_labels


# In[ ]:


train_labels.shape


# In[ ]:


# preparing train images array ('flat' image vectors)

train_images = np.array(train_data.drop(columns='label'))
train_images.shape


# In[ ]:


# preparing 2D train images array (reshaping original 'flat' image vectors array)

n_images = train_images.shape[0]
dim = int(np.sqrt(train_images.shape[1]))

train_images_2D = train_images.reshape(n_images, dim, dim)
train_images_2D.shape


# In[ ]:


show_random_image(train_images_2D)


# In[ ]:


# normalizing "train" images

train_images = train_images / 255


# #### Preparing "Dig-MNIST" images

# In[ ]:


# preparing dig-mnist image labels using 'one-hot' encoding

dig_labels = to_categorical(dig_data.label)
dig_labels


# In[ ]:


dig_labels.shape


# In[ ]:


# preparing train images array ('flat' image vectors)

dig_images = np.array(dig_data.drop(columns='label'))
dig_images.shape


# In[ ]:


# preparing 2D dig-mnist images array (reshaping original 'flat' image vectors array)

n_images = dig_images.shape[0]
dim = int(np.sqrt(dig_images.shape[1]))

dig_images_2D = dig_images.reshape(n_images, dim, dim)
dig_images_2D.shape


# In[ ]:


show_random_image(dig_images_2D)


# In[ ]:


# normalizing "Dig-MNIST" images

dig_images = dig_images / 255


# ### Modelling

# #### Loading test images and sample submission

# In[ ]:


test_data = pd.read_csv(path + 'test.csv', index_col='id')
test_data


# In[ ]:


submission = pd.read_csv(path + 'sample_submission.csv', index_col='id')
submission


# #### Preparing test images

# In[ ]:


# preparing test images array ('flat' image vectors)

test_images = np.array(test_data)
test_images.shape


# In[ ]:


# normalizing "test" images

test_images = test_images / 255


# #### Setting (hyper)parameters

# In[ ]:


# setting input dimensionality - "flat" image vectors
input_dim = train_images.shape[1]


# In[ ]:


# setting optimization parameters
optimizer = 'rmsprop'
loss = 'categorical_crossentropy'
metrics = ['accuracy']


# In[ ]:


# setting training parameters
epochs = 100
batch_size = 1024

early_stop = EarlyStopping(monitor='val_loss', 
                           min_delta=0, 
                           patience=3, 
                           verbose=True, 
                           mode='auto', 
                           baseline=None, 
                           restore_best_weights=False)

callbacks = [early_stop]


# In[ ]:


model = Sequential()
model.add(Dense(128, activation='relu', input_shape=(input_dim,)))
model.add(Dense(16, activation='relu'))
model.add(Dense(10, activation='softmax'))


# In[ ]:


model.compile(optimizer=optimizer, loss=loss, metrics=metrics)


# In[ ]:


model.summary()


# In[ ]:


model.fit(train_images, train_labels, 
          batch_size=batch_size, epochs=epochs, 
          verbose=True, 
          callbacks=callbacks, 
          validation_split=0.1)


# #### Model evaluation

# In[ ]:


# showing history of 'accuracy'

plt.figure()
plt.plot(model.history.history['accuracy'], label='TRAIN ACC')
plt.plot(model.history.history['val_accuracy'], label='VAL ACC')
plt.legend()
plt.show()


# In[ ]:


# showing history of 'loss'

plt.figure()
plt.plot(model.history.history['loss'], label='TRAIN LOSS')
plt.plot(model.history.history['val_loss'], label='VAL LOSS')
plt.legend()
plt.show()


# In[ ]:


# making predictions for "train" data (in-sample check)

pred_train = model.predict_classes(train_images)
pred_train.shape


# In[ ]:


hits = (pred_train == train_data.label)
print('Hits: {}, i.e. {:.2f}%'.format(hits.sum(), hits.sum() / pred_train.shape[0] * 100))


# In[ ]:


miss = (pred_train != train_data.label)
print('Misses: {}, i.e. {:.2f}%'.format(miss.sum(), miss.sum() / pred_train.shape[0] * 100))


# In[ ]:


# evaluating model on "train" data

eval_metrics = model.evaluate(x=train_images, y=train_labels, 
                              batch_size=batch_size, verbose=True, callbacks=callbacks)
pd.DataFrame(eval_metrics, index=model.metrics_names, columns=['metric'])


# In[ ]:


# evaluating model on "Dig-MNIST" data

eval_metrics = model.evaluate(x=dig_images, y=dig_labels, 
                              batch_size=batch_size, verbose=True, callbacks=callbacks)
pd.DataFrame(eval_metrics, index=model.metrics_names, columns=['metric'])


# #### Making predictions

# In[ ]:


# setting the optimal number of epochs
epochs = 8

# re-training the model on full train dataset
model.fit(train_images, train_labels, 
          batch_size=batch_size, epochs=epochs, 
          verbose=True)


# In[ ]:


# making predictions on "test" data

pred_test = model.predict_classes(test_images)


# In[ ]:


submission.label = pred_test
submission.to_csv('submission.csv')

