#!/usr/bin/env python
# coding: utf-8

# <p style='text-align:center;font-size:20px'> <b>Kaggle Competition<b/> </p>

# <p style='text-align:center;font-size:32px'> <b>Digit Recognizer<b/> </p>

# ### Data Loading & Preprocessing

# In[16]:


# importing libraries
from __future__ import print_function
import pandas as pd
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras import backend as K
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")


# In[17]:


# importing train dataset
train = pd.read_csv('../input/train.csv')
print('The dimensions of Train dataset are - ', train.shape)


# In[18]:


# importing test dataset
test = pd.read_csv('../input/test.csv')
print('The dimensions of Test dataset are - ', test.shape)


# In[19]:


# setting the model parameters
batch_size = 128
num_classes = 10
epochs = 10
img_rows, img_cols = 28, 28


# In[20]:


# dropping the label column from train dataset
X_train = train.drop(['label'], axis=1)
X_test = test

y_train = train['label']
# converting each value of y_train to binary vector of size=10
# for y=2 => [0,0,1,0,0,0,0,0,0,0]
y_train = keras.utils.to_categorical(y_train, num_classes)


# In[21]:


# converting the pandas dataframe to numpy array
X_train = np.array(X_train)
X_test = np.array(X_test)


# In[22]:


# resizing the train & test datasets
if K.image_data_format() == 'channels_first':
    X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
    X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
    X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)


# In[23]:


print('The dimensions of the resized Train dataset is', X_train.shape)
print('The dimensions of the resized Test dataset is', X_train.shape)


# In[24]:


# this function is used to update the plots for each epoch and error
def plt_dynamic(x, ty, ax, colors=['b']):
    ax.plot(x, ty, 'r', label="Train Loss")
    plt.legend()
    plt.grid()
    fig.canvas.draw()


# ### Applying CNN model

# **3 Convolution Layers + Kernel size=5 + Padding + Batch Norm. with Max Pooling**

# In[25]:


model = Sequential()
# layer 1
model.add(Conv2D(128, kernel_size=(5, 5),
                 kernel_initializer='he_normal',
                 activation='relu',
                 padding='same',
                 input_shape=input_shape))
model.add(BatchNormalization())

#layer 2
model.add(Conv2D(64, kernel_size=(5, 5),
                 kernel_initializer='he_normal',
                 padding='same',
                 activation='relu'
                 ))
model.add(BatchNormalization())

#layer 3
model.add(Conv2D(32, kernel_size=(5, 5),
                 kernel_initializer='he_normal',
                 padding='same',
                 activation='relu'))
model.add(BatchNormalization())

model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Flatten())

model.add(Dense(128, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(rate=0.5))

model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

history = model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1)


# In[26]:


# epoch vs loss plot
fig,ax = plt.subplots(1,1)
ax.set_xlabel('Epoch') 
ax.set_ylabel('Categorical Crossentropy Loss')

# list of epoch numbers
x = list(range(1,epochs+1))

ty = history.history['loss']
plt_dynamic(x, ty, ax)


# In[27]:


# predicting the class labels
y_pred = model.predict(X_test)

# converting the probabilities to class labels
y_classes = y_pred.argmax(axis=-1)


# In[28]:


# constructing the ID column for submission
Id = [x for x in range(1,28001)]


# In[29]:


output=pd.DataFrame({'ImageId':Id,'Label':y_classes})
output.to_csv('submission.csv', index=False)


# 1. **Result** - The model scored an accuracy of **99.27%** on Test dataset. 

# ## Conclusion

# - In this case study, I trained a 3-layered Convolutional Neural Network that achieved 99.27% accuracy on Test data.
# - The size of the kernel used was 5x5 along with Padding.
# - The activation function used was Adam. 
# - Techniques such as Batch Normalization, MaxPooling & Dropouts were used.
