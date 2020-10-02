#!/usr/bin/env python
# coding: utf-8

# ###  Importing libraries and data

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import os
import random
import json
import cv2
import warnings
warnings.filterwarnings('ignore')

from PIL import Image
from keras.applications.vgg16 import VGG16 
from keras.preprocessing import image
from keras.models import Sequential,Model
from keras.optimizers import Adam,SGD
from keras.layers import Dense, Flatten, GlobalAveragePooling2D, Conv2D, Input, Dropout
from keras.utils import np_utils
from keras import backend as K


# In[ ]:


path = '../input/aerial-cactus-identification/'
train = pd.read_csv(path + 'train.csv')
sample_sub = pd.read_csv(path + 'sample_submission.csv')


# In[ ]:


train.head()


# ### Simple EDA

# In[ ]:


train['has_cactus'].value_counts().plot(kind='bar')


# Data is imbalanced, but as this is a playground competition, we can ignore this.

# In[ ]:


plt.subplots(figsize=(10,10))
for i in range(5):
    img_name = train['id'][i]
    img = Image.open(path + 'train/train/' + img_name)
    plt.imshow(np.asarray(img))
    plt.show()


# In[ ]:


images = []
labels = []
for i in os.listdir(path + 'train/train/'):
    img = image.load_img(path + 'train/train/' + i, target_size=(32,32))
    img = image.img_to_array(img)
    labels.append(train[train['id'] == i]['has_cactus'].values[0])
    images.append(img)


# creating lists of images and labels.

# In[ ]:


combined = list(zip(images,labels))
random.shuffle(combined)
images[:],labels[:] = zip(*combined) 


# In[ ]:


X_train = np.asarray(images)
X_train = X_train.astype('float32')
X_train /= 255
y_train = np.array(labels)


# Rescaling the pixel values and converting to arrays.

# In[ ]:


vgg16 = VGG16(include_top=False, weights='imagenet', input_shape=(32,32,3))


# In[ ]:


vgg16.summary()


# In[ ]:


avg = Flatten()(vgg16.output)
fc1 = Dense(256, activation='relu')(avg)
fc = Dropout(0.5)(fc1)
fc2 = Dense(1, activation='sigmoid')(fc)

model = Model(inputs=vgg16.inputs, outputs=fc2)
model.summary()


# In[ ]:


for i in model.layers:
    print(i)


# In[ ]:


for i in range(15):
    model.layers[i].trainable = False


# In[ ]:


model.compile(loss='binary_crossentropy', optimizer=Adam(lr=1e-5), metrics=['accuracy'])


# In[ ]:


hist = model.fit(X_train,y_train,shuffle=True, validation_split=0.1, batch_size=32, epochs=25,verbose=1)


# In[ ]:


plt.figure(0)
plt.plot(hist.history['acc'],'r')
plt.plot(hist.history['val_acc'],'b')

plt.figure(1)
plt.plot(hist.history['loss'],'r')
plt.plot(hist.history['val_loss'],'b')

plt.show()


# In[ ]:


test_images_ids = []
test_images = []
for i in os.listdir(path + 'test/test/'):
    img = image.load_img(path + 'test/test/' + i)
    img = image.img_to_array(img)
    test_images.append(img)
    test_images_ids.append(i)


# In[ ]:


X_test = np.asarray(test_images)
X_test = X_test.astype('float32')
X_test /= 255


# In[ ]:


predictions = model.predict(X_test)


# In[ ]:


predictions[:5]


# In[ ]:


submit = pd.DataFrame(predictions, columns=['has_cactus'])


# In[ ]:


submit['id'] = test_images_ids
submit['has_cactus'] = submit['has_cactus'].apply(lambda x: 1 if x > 0.75 else 0)
submit.to_csv('submission.csv', index=False)


# I am a beginner in Computer Vision. If there are any mistakes or improvements, please let me know.

# ## References
# 
# 1. A simple yet wonderful kernel :  https://www.kaggle.com/ateplyuk/keras-transfer-vgg16
# 2. How CNNs work : https://brohrer.github.io/how_convolutional_neural_networks_work.html
