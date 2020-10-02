#!/usr/bin/env python
# coding: utf-8

# 

# Import Libraries

# In[ ]:


import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
def ignore_warn(*args, **kwargs):
    pass
warnings.warn = ignore_warn


# Read the test and train data

# In[ ]:


train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')

Observe the first 5 rows of the training set
# In[ ]:


train.head(5)


# Save the labels in one set, and remove it from another set, keeping only the pixel values. Convert the values into integers and floats, respectively.

# In[ ]:


Y_train = train["label"].values.astype('int32')
X_train = train.drop(labels = ["label"],axis = 1).values.astype('float32')
X_test = test.values.astype('float32')


# Normalize the data

# In[ ]:


X_train = X_train/255.0
X_test = X_test/255.0


# Reshape the datasets to conform to Keras's expectations

# In[ ]:


X_train = X_train.reshape(X_train.shape[0], 28, 28,1)
X_test = X_test.reshape(X_test.shape[0], 28, 28,1)


# Convert the class vectors to binary class matrices

# In[ ]:


from keras.utils.np_utils import to_categorical
Y_train = to_categorical(Y_train, num_classes = 10)


# Split into training and validation data

# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size = 0.1, random_state=123)


# Construct the model

# In[ ]:


import keras
from keras.models import Sequential  
from keras.layers import Dense, Dropout, Flatten, BatchNormalization, Activation  
from keras.layers.convolutional import Conv2D, MaxPooling2D  
from keras.constraints import maxnorm  
from keras.utils import np_utils 

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=X_train.shape[1:], padding='same'))  
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3), input_shape=(3, 32, 32), activation='relu', padding='same'))  
model.add(Dropout(0.2))
model.add(BatchNormalization())
model.add(Conv2D(64, (3, 3), padding='same'))  
model.add(Activation('relu'))  
model.add(MaxPooling2D(pool_size=(2, 2)))  
model.add(Dropout(0.2))  
model.add(BatchNormalization())
model.add(Conv2D(64, (3, 3), padding='same'))  
model.add(Activation('relu'))  
model.add(MaxPooling2D(pool_size=(2, 2)))  
model.add(Dropout(0.2))  
model.add(BatchNormalization())
model.add(Conv2D(128, (3, 3), padding='same'))  
model.add(Activation('relu'))  
model.add(Dropout(0.2))  
model.add(BatchNormalization())
model.add(Flatten())  
model.add(Dropout(0.2))
model.add(Dense(256, kernel_constraint=maxnorm(3)))  
model.add(Activation('relu'))  
model.add(Dropout(0.2))  
model.add(BatchNormalization())
model.add(Dense(128, kernel_constraint=maxnorm(3)))  
model.add(Activation('relu'))  
model.add(Dropout(0.2))  
model.add(BatchNormalization())
model.add(Dense(10))  
model.add(Activation('softmax'))  

model.compile(loss=keras.losses.categorical_crossentropy,  optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])


# Fit and run the model and subsequently see the accuracy

# In[ ]:


model.fit(X_train, Y_train, batch_size=128, epochs=7, verbose=1, validation_data=(X_val, Y_val))
accuracy = model.evaluate(X_val, Y_val, verbose=0)
print('Test accuracy:', accuracy[1])


# Submit the predictions

# In[ ]:


pred = model.predict(X_test)
Y_classes = pred.argmax(axis=-1)
res = pd.DataFrame()
res['ImageId'] = list(range(1,28001))
res['Label'] = Y_classes
res.to_csv("DigitsNN.csv", index = False)

