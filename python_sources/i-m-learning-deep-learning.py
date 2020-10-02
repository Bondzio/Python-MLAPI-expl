#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


train=pd.read_csv("/kaggle/input/digit-recognizer/train.csv")
print(train.shape)
train.head()


# In[ ]:


test=pd.read_csv("/kaggle/input/digit-recognizer/test.csv")
print(test.shape)
test.head()


# In[ ]:


Y_train=train["label"]
X_train=train.drop(labels=["label"],axis=1)


# In[ ]:


plt.figure(figsize=(15,7))
g=sns.countplot(Y_train,palette="icefire")
plt.title("Number of digit classes")
Y_train.value_counts()


# In[ ]:


img=X_train.iloc[5].as_matrix()
img=img.reshape((28,28))
plt.imshow(img,cmap='gray')
plt.title(train.iloc[0,0])
plt.axis("off")
plt.show()


# In[ ]:


img = X_train.iloc[13].as_matrix()
img = img.reshape((28,28))
plt.imshow(img,cmap='gray')
plt.title(train.iloc[3,0])
plt.axis("off")
plt.show()


# In[ ]:


#Normalization
X_train=X_train/255.0
test=test/255.0
print("x_train shape: ",X_train.shape)
print("test shape: ",test.shape)


# In[ ]:


X_train=X_train.values.reshape(-1,28,28,1)
test=test.values.reshape(-1,28,28,1)
print("x_train shape: ",X_train.shape)
print("test shape: ",test.shape)


# In[ ]:


#Label Encoding
from keras.utils.np_utils import to_categorical
Y_train=to_categorical(Y_train,num_classes=10)


# **Train Test Split**

# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_val,Y_train,Y_val=train_test_split(X_train,Y_train,test_size=0.1,random_state=29)
print("x_train shape",X_train.shape)
print("x_test shape",X_val.shape)
print("y_train shape",Y_train.shape)
print("y_test shape",Y_val.shape)


# In[ ]:


plt.imshow(X_train[13][:,:,0],cmap='gray')
plt.show()


# In[ ]:


from sklearn.metrics import confusion_matrix
import itertools

from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D,MaxPool2D
from keras.optimizers import RMSprop,Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau

model=Sequential()

model.add(Conv2D(filters=16,kernel_size=(5,5),padding='Same',
                activation='relu',input_shape=(28,28,1)))
model.add(MaxPool2D(pool_size=(2,2)))
model.add(Dropout(0.2))
#
model.add(Conv2D(filters=32,kernel_size=(3,3),padding='Same',
                activation='relu'))
model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
model.add(Dropout(0.2))

#Fully Connected
model.add(Flatten())
model.add(Dense(256,activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(10,activation='softmax'))


# In[ ]:


optimizer=Adam(lr=0.001,beta_1=0.9,beta_2=0.999)


# In[ ]:


model.compile(optimizer,loss="categorical_crossentropy",metrics=['accuracy'])


# In[ ]:


epochs=30
batch_size=300


# In[ ]:


datagen=ImageDataGenerator(
featurewise_center=False,
samplewise_center=False,
featurewise_std_normalization=False,
samplewise_std_normalization=False,
zca_whitening=False,
rotation_range=0.5,
zoom_range=0.5,
width_shift_range=0.5,
height_shift_range=0.5,
horizontal_flip=0.5,
vertical_flip=0.5)
datagen.fit(X_train)


# In[ ]:


history=model.fit_generator(datagen.flow(X_train,Y_train,batch_size=batch_size),
                           epochs=epochs,validation_data=(X_val,Y_val),steps_per_epoch=X_train.shape[0]//batch_size)


# In[ ]:


plt.plot(history.history['val_loss'],color='b',label='validation loss')
plt.title("Test Loss")
plt.xlabel("Number of epoch")
plt.ylabel("Loss")
plt.show()


# In[ ]:


import seaborn as sns
# Predict the values from the validation dataset
Y_pred = model.predict(X_val)
# Convert predictions classes to one hot vectors 
Y_pred_classes = np.argmax(Y_pred,axis = 1) 
# Convert validation observations to one hot vectors
Y_true = np.argmax(Y_val,axis = 1) 
# compute the confusion matrix
confusion_mtx = confusion_matrix(Y_true, Y_pred_classes) 
# plot the confusion matrix
f,ax = plt.subplots(figsize=(8, 8))
sns.heatmap(confusion_mtx, annot=True, linewidths=0.01,cmap="Greens",linecolor="gray", fmt= '.1f',ax=ax)
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix")
plt.show()


# In[ ]:




