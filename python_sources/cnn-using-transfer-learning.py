#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input/cell-images-for-detecting-malaria/cell_images/cell_images"))

# Any results you write to the current directory are saved as output.


# #### Problem Statement
# 
# We have cell images , some of then have malaria parasite and other don't. <br> Its a simple classification problem with 2 labels. We will mark one with parasite as 1 and without as 0.<br> Instead of creating a CNN model from the scratch, we will use the pretrained model (transfer learning). For our current evaluation we will us RESNET.

# #### Steps 
# - Load the images of both the classes.
# - Evaluate the shape of the Images and try to reshape it , as all the images will not be of same shape.
# - Convert the image to the matrix (3 d matrix , with channel as 3).
# - Divide the datset in the training and validation set.
# - Use ImageDataGenerator to increase the number samples.
# - Use Pretrained RESNET model extend it and try to evalute the classification.

# In[ ]:


import os
import pandas as pd
import numpy as np
import cv2

from sklearn.utils import shuffle

from tensorflow.python.keras.applications import ResNet50
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras import optimizers


# In[ ]:





# ### Load And Transform Data

# In[ ]:


root_directory = '../input/cell-images-for-detecting-malaria/cell_images/cell_images/'
parasite_folder = 'Parasitized'
uninfected_folder = 'Uninfected'


# In[ ]:


WIDTH =  120
HEIGHT = 120

CHANNELS = 3


# In[ ]:


# r = root, d = directory, f = file
def load_data(path, label, data):
    for r,d,f in os.walk(path):
        for file in f:
            if not file.endswith('db'):
                complete_path = r + "/" + file
                img = cv2.imread(complete_path)
                converted_img = cv2.resize(img, (WIDTH, HEIGHT))
                row = [[img.shape[0], img.shape[1], img.shape[2], complete_path,label, converted_img]]
                temp = pd.DataFrame(row, columns=['width', 'height', 'channel', 'path', 'label', 'image'])
                data  = data.append(temp, ignore_index=True)
                
    return data  


# In[ ]:


data = pd.DataFrame(columns=['width', 'height', 'channel', 'path', 'label', 'image'])
data = load_data(root_directory + parasite_folder, 1, data)
data = load_data(root_directory + uninfected_folder, 0, data)


# In[ ]:


data.width = data.width.astype(int)
data.height = data.height.astype(int)
data.channel = data.channel.astype(int)
data.path = data.path.astype(str)
data.label = data.label.astype(int)


# In[ ]:


print('Data Type of all the Coloumns', data.dtypes)


# In[ ]:


data.head()


# In[ ]:


data.describe()


# In[ ]:


data.width.hist(bins = 7)


# In[ ]:


data.height.hist(bins = 7)


# #### Information Decided from metadata
# 
# - Since most of the width and height is btw 100-150 , we will reshape image around the same.
# - All the images are of same channel.
# - We have equal number of both the classes.
# - Data generated have to be shuffled.

# In[ ]:


def split_training_and_test(data_frame, training_percentage):
    training_number = data_frame.shape[0] * training_percentage / 100
    test_number = data_frame.shape[0] - training_number
    return data_frame.head(int(training_number)), data_frame.tail(int(test_number))


# In[ ]:


data = shuffle(data)
train, val = split_training_and_test(data, 85)


# In[ ]:


data = None


# In[ ]:



train_X = np.stack(train.image, axis=0) 
train_y = train.label

val_X = np.stack(val.image, axis=0)  
val_y = val.label


# In[ ]:


train = None
val = None


# In[ ]:





# In[ ]:


RESNET_WEIGHTS_PATH = '../input/resnet50/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5'
RESNET50_POOLING_AVERAGE = 'avg'
DENSE_LAYER_ACTIVATION = 'relu'
DENSE_LAYER_ACTIVATION_LAST = 'softmax'
OBJECTIVE_FUNCTION = 'sparse_categorical_crossentropy'
LOSS_METRICS = ['accuracy']


# In[ ]:


NUM_CLASSES = 2
NUM_EPOCHS = 10
BATCH_SIZE = 64
EARLY_STOP_PATIENCE = 3


# In[ ]:


model = Sequential()
model.add(ResNet50(include_top = False, pooling = RESNET50_POOLING_AVERAGE, weights = RESNET_WEIGHTS_PATH))
model.add(Dense(NUM_CLASSES, activation = DENSE_LAYER_ACTIVATION))
model
model.add(Dense(NUM_CLASSES, activation = DENSE_LAYER_ACTIVATION))

model.layers[0].trainable = False


# In[ ]:


model.summary()


# In[ ]:


sgd = optimizers.SGD(lr = 0.01, decay = 1e-6, momentum = 0.9, nesterov = True)
model.compile(optimizer = sgd, loss = OBJECTIVE_FUNCTION, metrics = LOSS_METRICS)


# In[ ]:


model.fit(train_X, train_y, 
          validation_data=(val_X, val_y), epochs=NUM_EPOCHS, batch_size = BATCH_SIZE, verbose =1)


# ### Things that can be extended in this kernel
# * Normalized the data before training.
# * Use ImageDataGenerator for improving accuracy.
# * Try early stopping using callback and save intermediate models.
