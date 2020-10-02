#!/usr/bin/env python
# coding: utf-8

# # Digit Recognizer solution using CNN's

# Welcome everybody! This Notebook summarizes the work I have done in the Digit recognizer competition, as I wanted to get started with Convolutional Neural Networks (CCN). It has the minimum necessary information to get a good result in the competition while being simple and easy to understand. I'm sorry if it doesn't include more plots or EDA, because I think the problem is quite simple.
# 
# If any of you don't really understand CNN's and want to take a little course about it I strongly recommend the Kaggle's course about it (https://www.kaggle.com/learn/deep-learning), which is not very long but very informative. Most of the work of this notebook has been extracted from there.

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

from tensorflow.python import keras
from keras.models import Sequential
from keras.layers import Dense , Dropout , Lambda, Flatten, Conv2D, BatchNormalization, MaxPooling2D
from keras.optimizers import Adam ,RMSprop
from sklearn.model_selection import train_test_split
from keras import  backend as K
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.np_utils import to_categorical
from keras.callbacks import ReduceLROnPlateau


# In[ ]:


train = pd.read_csv("../input/digit-recognizer/train.csv")
test= pd.read_csv("../input/digit-recognizer/test.csv")


# In[ ]:


X_train = (train.iloc[:,1:].values).astype('float32')
y_train = train.iloc[:,0].values.astype('int32')
X_test = test.values.astype('float32')


# # Preprocessing images

# ## **Reshaping images**

# Reshape pictures to 3D arrays: height = 28px, width = 28px, canal = 1 (BW images)

# In[ ]:


img_rows, img_cols = 28, 28 # As explained in the competition's data description

X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols,1)
X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols,1)


# ## **Feature Standardization**

# In[ ]:


mean_px = X_train.mean().astype(np.float32)
std_px = X_train.std().astype(np.float32)

def standardize(x): 
    return (x-mean_px)/std_px

X_train = standardize(X_train)
X_test = standardize(X_test)


# ## **One Hot encoding the labels**

# In[ ]:


y_train = to_categorical(y_train)
num_classes = y_train.shape[1]


# In[ ]:


# An example image (randomly chosen)
plt.imshow(X_train[np.random.randint(low=0, high=len(X_train))][:,:,0], cmap='gray')


# ## **Data Augmentation**

# In[ ]:


gen = ImageDataGenerator(rotation_range = 10,
                         zoom_range = 0.1,
                         width_shift_range = 0.1,
                         height_shift_range = 0.1,
                         shear_range = 0.1)


# In[ ]:


X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.10, random_state=4)

batches = gen.flow(X_train, y_train, batch_size=64)
val_batches=gen.flow(X_val, y_val, batch_size=64)


# # Model generation

# ## Define model

# In[ ]:



model = Sequential()

model.add(Conv2D(64, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(img_rows, img_cols, 1)))
model.add(BatchNormalization())

model.add(Conv2D(64, kernel_size=(3, 3), strides=1, activation='relu'))
model.add(BatchNormalization())

model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))

model.add(Conv2D(64, kernel_size=(3, 3), strides=1, activation='relu'))
model.add(BatchNormalization())

model.add(Conv2D(64, kernel_size=(3, 3), strides=1, activation='relu'))
model.add(BatchNormalization())

model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(num_classes, activation='softmax'))


# ## Compile model

# In[ ]:


model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer='adam',
              metrics=['accuracy'])


# ## Model fitting

# In[ ]:


# Audjusting learning rate
learning_rate_reduction = ReduceLROnPlateau(monitor='val_accuracy', 
                                            patience=3, 
                                            verbose=1, 
                                            factor=0.5, 
                                            min_lr=0.00001)

history=model.fit_generator(generator=batches,
                            steps_per_epoch=batches.n,
                            epochs=3,
                            validation_data=val_batches,
                            validation_steps=val_batches.n,
                            callbacks=[learning_rate_reduction])


# ## Plot loss and accuracy curves

# In[ ]:


# Draw the loss and accuracy curves of the training set and the validation set.

fig, ax = plt.subplots(2,1)
ax[0].plot(history.history['loss'], color='b', label="Training loss")
ax[0].plot(history.history['val_loss'], color='r', label="validation loss",axes =ax[0])
legend = ax[0].legend(loc='best', shadow=True)

ax[1].plot(history.history['accuracy'], color='b', label="Training accuracy")
ax[1].plot(history.history['val_accuracy'], color='r',label="Validation accuracy")
legend = ax[1].legend(loc='best', shadow=True)


# ## **Submitting Predictions**

# In[ ]:


predictions = model.predict_classes(X_test, verbose=0)

submissions=pd.DataFrame({"ImageId": list(range(1,len(predictions)+1)),
                         "Label": predictions})
submissions.to_csv("submission.csv", index=False, header=True)

