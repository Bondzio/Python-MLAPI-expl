#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# In[ ]:


train = pd.read_csv("../input/digit-recognizer/train.csv")
test = pd.read_csv("../input/digit-recognizer/test.csv")
train.shape


# In[ ]:


test.shape


# In[ ]:


Y_train = train["label"]
X_train = train.drop(labels = ["label"],axis = 1) 


# In[ ]:


X_train.isnull().any().describe()


# In[ ]:


X_train.info()


# In[ ]:


test.isnull().any().describe()


# In[ ]:


X_train = X_train / 255.0
test = test / 255.0


# In[ ]:


X_train = X_train.values.reshape(-1,28,28,1)
test = test.values.reshape(-1,28,28,1)


# In[ ]:


from keras.utils.np_utils import to_categorical


# In[ ]:


Y_train = to_categorical(Y_train, num_classes = 10)


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size = 0.1, random_state=10)


# In[ ]:


g = plt.imshow(X_train[0][:,:,0])


# In[ ]:


from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.optimizers import RMSprop
import tensorflow as tf


# In[ ]:


model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(28, 28, 1),padding='same'),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(28, 28, 1),padding='same'),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu', input_shape=(28, 28, 1),padding='same'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu',padding='same'),
    tf.keras.layers.Conv2D(192, (3, 3), activation='relu',padding='same'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(192, (3, 3), activation='relu',padding='same'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])


# In[ ]:


model.compile(optimizer = keras.optimizers.RMSprop(learning_rate=0.001, rho=0.9) , loss = "categorical_crossentropy", metrics=["accuracy"])


# In[ ]:


model.fit(X_train, Y_train, batch_size = 86, epochs =50, validation_data = (X_val, Y_val), verbose = 1)


# In[ ]:


results = model.predict(test)
results = np.argmax(results,axis = 1)
results = pd.Series(results,name="Label")
submission = pd.concat([pd.Series(range(1,28001),name = "ImageId"),results],axis = 1)
submission.to_csv("cnn_fourth.csv",index=False)


# In[ ]:




