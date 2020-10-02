#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization
from keras.utils import np_utils

import os
print(os.listdir("../input"))


# # Load train and test datasets

# **Load train dataset**

# In[ ]:


# load data
train = pd.read_csv("../input/train.csv")
print("train dataset shape is", train.shape)
train.head(5)


# **Load test dataset**

# In[ ]:


# load data
test = pd.read_csv("../input/test.csv")
print("test dataset shape is", test.shape)
test.head(5)


# # Split dataset into X and y

# ** split train dataset into X**

# In[ ]:


X_train = train.drop("label", axis=1)
X_train = X_train.values.astype("float32")


# **split train dataset into y**

# In[ ]:


y_train = train['label']
y_train = y_train.values.astype("int32")


# **split test dataset into X**

# In[ ]:


X_test = test.values.astype("float32")


# # Preprocess the data

# In[ ]:


# Normalize the data
X_train = X_train / 255
X_test = X_test / 255

# Reshape the data
X_train = X_train.reshape(-1, 28, 28, 1)
X_test = X_test.reshape(-1, 28, 28, 1)

# One hot encoding
y_train = np_utils.to_categorical(y_train, 10)

# Check the data shape
print("X_train shape is ", X_train.shape, "y_train shape is", y_train.shape)


# # Build the model

# In[ ]:


model = Sequential()

# Must define the input shape in the first layer of the neural network
model.add(Conv2D(filters=32, kernel_size=3, padding='same', activation='relu', input_shape=(28,28,1))) 
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.3))

model.add(Conv2D(filters=64, kernel_size=3, padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.3))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

# Take a look at the model summary
model.summary()


# **Compile the model**

# In[ ]:


model.compile(loss="categorical_crossentropy", optimizer="Adam", metrics=['accuracy'])


# **Fit the model**

# In[ ]:


model.fit(X_train, y_train, batch_size=64, epochs=5)


# In[ ]:


predictions = model.predict_classes(X_test, verbose=0)

submissions=pd.DataFrame({"ImageId": list(range(1,len(predictions)+1)),
                         "Label": predictions})
submissions.to_csv("mnist_keras.csv", index=False, header=True)


# In[ ]:




