#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# Import necessary modules
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


train = pd.read_csv("/kaggle/input/digit-recognizer/train.csv")
test = pd.read_csv("/kaggle/input/digit-recognizer/test.csv")
train.head(1)


# - label is the target variable
# - pixel0 to pixel783 are the input variables.

# In[ ]:


test.head(1)


# In[ ]:


X = train.drop('label', axis = 1)
y = train[['label']]


# In[ ]:


X = X / 255.0
X = np.array(X).reshape(-1, 28, 28, 1)


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3, stratify = y)


# In[ ]:


import seaborn as sns
print(len(train['label'].unique()))
sns.countplot(train['label'])


# In[ ]:


model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D(2, 2),
    
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation = tf.nn.relu),
    tf.keras.layers.Dense(10, activation = tf.nn.softmax) # Note 10 is the number of unique layers
])

For classification, it is recommended to use ADAM optimizer and sparse_categorical_crossentropy as loss function.
# In[ ]:


model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


# ## Image Augumentation with Rotation

# In[ ]:


image_gen = ImageDataGenerator(rotation_range=90, horizontal_flip=False, vertical_flip=False)
image_gen.fit(X_train)


# In[ ]:


model.fit(X_train, y_train, epochs = 5, steps_per_epoch = 50)


# In[ ]:


test_loss, test_accuracy = model.evaluate(X_test, y_test, steps = 100)
print('Loss on test dataset : ', test_loss)
print('Accuracy on test dataset : ', test_accuracy)


# 98 % acuracy is better that human detection. But still a lot of improvement is required to make the model more accurate. 

# Note : This is for beginners only. Checkout more resources to improve your model accuracy.

# In[ ]:


result_dataset = test / 255.0
result_dataset = np.array(result_dataset).reshape(-1,28,28,1)


# In[ ]:


predictions = model.predict(result_dataset)

prediction_labels = []
for index, p in enumerate(predictions):
    prediction_labels.append(np.argmax(p))

print(prediction_labels)


# ## Please upvote the kernel if you liked it. 

# In[ ]:




