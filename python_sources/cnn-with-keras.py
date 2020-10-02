#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Activation, Conv2D, MaxPooling2D, Dropout, Flatten
import keras
from sklearn.model_selection import train_test_split
from numpy import argmax
from sklearn.metrics import accuracy_score


# In[ ]:


train = pd.read_csv("../input/train.csv")


# In[ ]:


y_train = train['label']
x_train = train.drop(labels = ['label'], axis = 1)

x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.1, random_state=42)


# In[ ]:


input_x = x_train.values.reshape(len(x_train),28,28,1)
input_y = keras.utils.to_categorical(y_train, num_classes=10)


# In[ ]:


model = Sequential()

model.add(Conv2D(filters = 32, kernel_size = (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(Conv2D(filters = 32, kernel_size = (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(input_x, input_y, validation_split = 0.1, epochs=5)


# In[ ]:


x_test = x_test.values.reshape(len(x_test),28,28,1)


# In[ ]:


predict = model.predict(x_test)


# In[ ]:


predict = argmax(predict, axis=1)


# In[ ]:


accuracy_score(predict,y_test)


# In[ ]:


submission = pd.read_csv("../input/test.csv")


# In[ ]:


submission = submission.values.reshape(len(submission),28,28,1)


# In[ ]:


predict_sub = model.predict(submission)


# In[ ]:


predict_sub = argmax(predict_sub, axis=1)


# In[ ]:


result = pd.read_csv("../input/sample_submission.csv")


# In[ ]:


result['Label'] = predict_sub


# In[ ]:


result


# In[ ]:


result.to_csv('./sample_submission.csv', index = False)


# In[ ]:




