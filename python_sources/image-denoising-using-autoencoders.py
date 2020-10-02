#!/usr/bin/env python
# coding: utf-8

# # OVERVIEW

# #### Autoencoders are a type of artificial neural networks that are used to perform a task of data encoding (representation learning).
# #### We will feed in noisy images from the mnist-fashion dataset as input.
# #### The output will be clean (denoised) image
# 

# # IMPORT LIBRARIES AND DATASET

# In[ ]:


import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random


# In[ ]:


# Load dataset 
(x_train, y_train), (x_test,y_test) = tf.keras.datasets.fashion_mnist.load_data()


# In[ ]:


# Visualize a sample image
plt.imshow(x_train[0], cmap='gray')


# In[ ]:


# check out the shape of the training data
x_train.shape


# In[ ]:


# check out the shape of the testing data
x_test.shape


# # DATA VISUALIZATION

# - 0 = T-shirt/top
# - 1 = Trouser
# - 2 = Pullover
# - 3 = Dress
# - 4 = Coat
# - 5 = Sandal
# - 6 = Shirt
# - 7 = Sneaker
# - 8 = Bag
# - 9 = Ankle boot

# In[ ]:


# Let's view some images!
i = random.randint(1,60000)
plt.imshow(x_train[i], cmap='gray')


# In[ ]:


label = y_train[i]
label


# In[ ]:


# view more images in a grid format
# Define the dimensions of the plot grid 
W_grid = 15
L_grid = 15


fig, axes = plt.subplots(L_grid, W_grid, figsize = (17,17))

axes = axes.ravel() # flaten the 15 x 15 matrix into 225 array

n_training = len(x_train) # get the length of the training dataset

# Select a random number from 0 to n_training
for i in np.arange(0, W_grid*L_grid):
    index = np.random.randint(0, n_training)
    axes[i].imshow(x_train[index])
    axes[i].set_title(y_train[index], fontsize=8)
    axes[i].axis('off')


# # DATA PREPROCESSING

# In[ ]:


# normalize data
x_train = x_train/255
x_test = x_test/255


# In[ ]:


# add some noise
noise_factor = 0.3
noise_dataset = []

for img in x_train:
    noisy_image = img + noise_factor* np.random.randn(*img.shape)
    noisy_image = np.clip(noisy_image, 0, 1)
    noise_dataset.append(noisy_image)


# In[ ]:


noise_dataset = np.array(noise_dataset)


# In[ ]:


plt.imshow(noise_dataset[20], cmap='gray')


# In[ ]:


# add noise to testing dataset
noise_factor = 0.2
noise_test_dataset = []

for img in x_test:
    noisy_image = img + noise_factor* np.random.randn(*img.shape)
    noisy_image = np.clip(noisy_image, 0, 1)
    noise_test_dataset.append(noisy_image)


# In[ ]:


noise_test_dataset = np.array(noise_test_dataset)


# # BUILD AND TRAIN AUTOENCODER MODEL

# In[ ]:


from tensorflow.keras.layers import Conv2D, MaxPooling2D, UpSampling2D, Input
from tensorflow.keras import Model

def make_convolutional_autoencoder():
    # encoding
    inputs = Input(shape=(28, 28, 1))
    x = Conv2D(16, 3, activation='relu', padding='same')(inputs)
    x = MaxPooling2D(padding='same')(x)
    x = Conv2D( 8, 3, activation='relu', padding='same')(x)
    x = MaxPooling2D(padding='same')(x)
    x = Conv2D( 8, 3, activation='relu', padding='same')(x)
    encoded = MaxPooling2D(padding='same')(x)    
    
    # decoding
    x = Conv2D( 8, 3, activation='relu', padding='same')(encoded)
    x = UpSampling2D()(x)
    x = Conv2D( 8, 3, activation='relu', padding='same')(x)
    x = UpSampling2D()(x)
    x = Conv2D(16, 3, activation='relu')(x) # <= padding='valid'!
    x = UpSampling2D()(x)
    decoded = Conv2D(1, 3, activation='sigmoid', padding='same')(x)
    
    # autoencoder
    autoencoder = Model(inputs, decoded)
    autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
    return autoencoder

# create a convolutional autoencoder
autoencoder = make_convolutional_autoencoder()


# In[ ]:


autoencoder.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(lr=0.001))
autoencoder.summary()


# In[ ]:


autoencoder.fit(noise_dataset.reshape(-1, 28, 28, 1),
               x_train.reshape(-1, 28, 28, 1),
               epochs = 50,
               batch_size = 128,
               validation_data = (noise_test_dataset.reshape(-1, 28, 28, 1), x_test.reshape(-1, 28, 28, 1)))


# # EVALUATE TRAINED MODEL PERFORMANCE

# In[ ]:


predicted = autoencoder.predict(noise_test_dataset[:10].reshape(-1,28,28,1))


# In[ ]:


fig, axes = plt.subplots(nrows=2, ncols=10, sharex=True, sharey=True, figsize=(20,4))
for images, row in zip([noise_test_dataset[:10], predicted], axes):
    for img, ax in zip(images, row):
        ax.imshow(img.reshape((28, 28)), cmap='Greys_r')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)


# In[ ]:




