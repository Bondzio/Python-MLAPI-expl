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
print(os.listdir("../input/flowers/flowers/"))

# Any results you write to the current directory are saved as output.


# In[ ]:


from keras.applications.vgg16 import VGG16
from keras.layers import Dense
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator, img_to_array,load_img
import cv2


# In[ ]:


train_path='../input/flowers/flowers/'
labels=[]
for i in os.listdir(train_path):
    labels.append(i)
labels


# In[ ]:


vgg_model=VGG16(weights='imagenet')


# In[ ]:


vgg_model.summary()


# In[ ]:


model=Sequential()
for i in vgg_model.layers[:-1]:
    model.add(i)


# In[ ]:


model.summary()


# In[ ]:


for layer in model.layers:
    layer.trainable=False


# In[ ]:


model.add(Dense(5,activation='softmax'))
model.summary()


# In[ ]:


train_generator=ImageDataGenerator().flow_from_directory(train_path,target_size=(224,224),classes=labels,batch_size=32)


# In[ ]:


del vgg_model


# In[ ]:


model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])


# In[ ]:


model.fit_generator(train_generator,steps_per_epoch=100,epochs=5,verbose=1,shuffle=False)


# In[ ]:


image_path='../input/flowers/flowers/daisy/102841525_bd6628ae3c.jpg'
img=cv2.imread(image_path)
print(img.shape)
x=cv2.resize(img,(224,224))
print(x.shape)
x=np.expand_dims(x,axis=0)
prediction=model.predict_classes(x,verbose=1)
labels[int(prediction)]


# In[ ]:


#As simple as that.

