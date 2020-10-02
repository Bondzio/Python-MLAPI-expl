#!/usr/bin/env python
# coding: utf-8

# # Sign Language Model Training for Numbers
# 
# In this kernel, I will show you how to use and train model for [Sign Language for Numbers Dataset](https://www.kaggle.com/muhammadkhalid/sign-language-for-numbers)

# ## Load Data

# In[ ]:


import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import cv2 
import os

DATADIR = "/kaggle/input/sign-language-for-numbers/Sign Language for Numbers/"
CATEGORIES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "unknown"]

for category in CATEGORIES:
    path = os.path.join(DATADIR,category)  # create path to categories
    for img in os.listdir(path):
      # iterate over each image
      # convert to array
      img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)  
      plt.imshow(img_array, cmap='gray')  # graph it
      plt.show()  # display!

      break  # we just want one for now so break
    break  #...and one more!


# ## Resize

# In[ ]:


IMG_SIZE = 64

new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
plt.imshow(new_array, cmap='gray')
plt.show() # Show resize image


# ## Ceate training data

# In[ ]:


training_data = []

def create_training_data():
    for category in CATEGORIES:  # do 0,1,2,3, .....

        path = os.path.join(DATADIR,category)  # create path to categories
        class_num = CATEGORIES.index(category)  # get the classification

        for img in tqdm(os.listdir(path)):  # iterate over each image
            try:
                img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)  # convert to array
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
                training_data.append([new_array, class_num])  # add this to our training_data
            except Exception as e:  # in the interest in keeping the output clean...
                pass
            
create_training_data() # call function


# ## Shuffle

# In[ ]:


import random
random.shuffle(training_data)

# Check
for sample in training_data[:10]:
    print(sample[1])


# ## Appending data into X and Y lists

# In[ ]:


X = []
Y = []

for features,label in training_data:
    X.append(features)
    Y.append(label)

print(X[0].reshape(-1, IMG_SIZE, IMG_SIZE, 1))

X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)


# ## Pickle

# In[ ]:


import pickle

pickle_out = open("/kaggle/working/X.pickle","wb")
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("/kaggle/working/Y.pickle","wb")
pickle.dump(Y, pickle_out)
pickle_out.close()


# ## Start Training

# In[ ]:


import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
import time

import pickle

NAME = "Numbers-CNN-Model-{}".format(str(time.ctime())) # Model Name

# Load pickel data
pickle_in = open("/kaggle/working/X.pickle","rb")
X = pickle.load(pickle_in)
X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

pickle_in = open("/kaggle/working/Y.pickle","rb")
Y = pickle.load(pickle_in)
Y = np.array(Y)

X = X/255.0

model = Sequential()

model.add(Conv2D(16, (2,2), input_shape=X.shape[1:], activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
model.add(Conv2D(32, (3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(3, 3), strides=(3, 3), padding='same'))
model.add(Conv2D(64, (5,5), activation='relu'))
model.add(MaxPooling2D(pool_size=(5, 5), strides=(5, 5), padding='same'))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(11, activation='softmax')) # size must be equal to number of classes i.e. 11

tensorboard = TensorBoard(log_dir="/kaggle/working/logs/{}".format(NAME))

model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(X, Y, batch_size=32, epochs=10, validation_split=0.2, callbacks=[tensorboard])


# ## Save Model

# In[ ]:


model.save("/kaggle/working/{}.model".format(NAME))


# # Done
