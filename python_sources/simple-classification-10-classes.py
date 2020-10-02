#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames[0:10]: # only ten samples
        print(os.path.join(dirname, filename))


# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
from tqdm import tqdm
from keras.preprocessing import image


# #### Read all the training images, store them in a list, and finally convert that list into a numpy array. Store the score into a label list.

# In[ ]:


train_image = []
labels = []
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in tqdm (filenames):
        img = image.load_img(os.path.join(dirname, filename), target_size = (160, 240 , 3), grayscale = False)
        img = image.img_to_array(img)
        img = img/255
        train_image.append(img)
        # append score
        score = int(filename[:2])
        
        score = score - 1 # this is because To categorical works from 0 to number of classes

        labels.append(score)


# In[ ]:



X = np.array(train_image)
y = np.array(labels)


# In[ ]:


import random
fig = plt.figure(figsize = (20,10))
for i in range(4):
    fig.add_subplot(1, 4, i + 1)
    plt.imshow(X[random.randint(0,2400)])
    
    fig.add_subplot(3, 4, i + 1)
    plt.imshow(X[random.randint(0,2400)])


# ### check shapes

# In[ ]:


print (X.shape)
print (y.shape)


# ### Simple classification

# In[ ]:


from keras.utils import to_categorical
y_cat= to_categorical(y, num_classes = 10)


# In[ ]:


y_cat.shape


# # Define the model structure

# In[ ]:


import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=(160,240,3)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

model.summary()


# ### Compile the model

# In[ ]:


model.compile(loss='categorical_crossentropy',optimizer='Adam',metrics=['accuracy'])


# # Training Test Split

# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y_cat, random_state=42, test_size=0.1)


# # Training the model

# In[ ]:


model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test))


# # Predictions

# In[ ]:


predictions =  model.predict(X_test)


# In[ ]:


y_pred = []
for pred in predictions:
    y_pred.append(np.argmax(pred))
y_true = []
for y in y_test:
    y_true.append(np.argmax(y))


# In[ ]:


from sklearn.metrics import classification_report
print(classification_report(y_true, y_pred, labels=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))


# In[ ]:




