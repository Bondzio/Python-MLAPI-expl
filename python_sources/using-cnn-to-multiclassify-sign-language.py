#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[ ]:


import os
import zipfile
import numpy as np
import pandas as pd
import random
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split


# # Load data

# In[ ]:


train_df = pd.read_csv('../input/sign-language-mnist/sign_mnist_train.csv')
train_df.head()


# In[ ]:


test_df = pd.read_csv('../input/sign-language-mnist/sign_mnist_test.csv')
test_df.head()


# In[ ]:


labels = train_df['label'].values


# In[ ]:


train_df.drop('label', axis=1, inplace=True)


# In[ ]:


images = train_df.values.reshape(-1, 28, 28, 1)


# # Visualize some images in training set

# In[ ]:


import matplotlib
from matplotlib import pyplot as plt

index = 24 # change this index to see other images
plt.imshow(images[index].reshape(28,28))


# # Split train - validation set

# In[ ]:


x_train, x_valid, y_train, y_valid = train_test_split(images, labels, test_size=0.3, random_state=42)


# In[ ]:


print('Training set size: ' + str(x_train.shape[0]))
print('Validation set size: ' + str(x_valid.shape[0]))


# In[ ]:


np.unique(labels) # label 9 missing, cannot use to_categorical() in keras to one hot encode


# In[ ]:


from sklearn import preprocessing
lb = preprocessing.LabelBinarizer()
y_train_onehot = lb.fit_transform(y_train)
y_valid_onehot = lb.transform(y_valid)


# # Build CNN model

# In[ ]:


batch_size = 128
epochs = 50
num_classes = len(np.unique(labels)) # 24 classes


# In[ ]:


# Normalize train-validation data
x_train = x_train/255
x_valid = x_valid/255


# In[ ]:


from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, Activation, BatchNormalization
from keras.optimizers import RMSprop

model = Sequential()

model.add(Conv2D(64, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

#model.add(Conv2D(64, (3, 3), activation='relu'))
#model.add(BatchNormalization())
#model.add(MaxPooling2D(pool_size=(2, 2)))
#model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax')) 

model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.001), metrics=['accuracy'])

model.summary()


# # Fit model

# In[ ]:


history = model.fit(x_train, y_train_onehot, validation_data = (x_valid, y_valid_onehot), epochs = epochs, batch_size = batch_size)


# # Plot training - validation accuracy & loss

# In[ ]:


# Retrieve a list of list results on training and test data sets for each training epoch
acc      = history.history[     'acc' ]
val_acc  = history.history[ 'val_acc' ]
loss     = history.history[    'loss' ]
val_loss = history.history['val_loss' ]

plt.plot(range(epochs), acc, 'r', label='Training accuracy')
plt.plot(range(epochs), val_acc, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend()

plt.show()


# # Evaluate model on test set

# In[ ]:


y_test = test_df['label']
y_test_onehot = lb.transform(y_test)


# In[ ]:


test_df.drop('label', axis=1, inplace=True)


# In[ ]:


x_test = test_df.values.reshape(-1,28,28,1)/255


# In[ ]:


model.evaluate(x_test, y_test_onehot, batch_size = batch_size)


# In[ ]:




