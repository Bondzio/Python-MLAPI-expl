#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# # Importing necessary lib

# In[ ]:


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,BatchNormalization
from sklearn.model_selection import train_test_split
#from tensorflow.keras.callbacks import Callback
from tensorflow.keras.layers import Dropout
from tensorflow.keras import regularizers
from tensorflow.keras.models import Sequential
import sklearn
from tensorflow.keras.regularizers import l1
from tensorflow.keras.layers import Conv2D, Dense, Flatten, MaxPool2D, Dropout, SpatialDropout2D, BatchNormalization, LayerNormalization

from sklearn.model_selection import train_test_split


# # loading data

# In[ ]:


train=pd.read_csv('/kaggle/input/digit-recognizer/train.csv')
test=pd.read_csv('/kaggle/input/digit-recognizer/test.csv')
train.head()


# In[ ]:


test.head()


# In[ ]:


y=train['label']
y.head()


# In[ ]:


X=train.drop('label',axis=1)
X.head()


# ## for faster training

# In[ ]:


X=X/255
test=test/255


# ## since conv2d requires 3d input

# In[ ]:


X= X.values.reshape(-1,28,28,1)
test = test.values.reshape(-1,28,28,1)


# ## Splitting The Data

# In[ ]:


X_train,X_val,y_train,y_val=train_test_split(X,y,test_size=0.1)


# # Now lets build our model

# In[ ]:


model=Sequential([
    Conv2D(32,(3,3),input_shape=(28,28,1),activation='relu',padding='same'),
    BatchNormalization(),
    SpatialDropout2D(0.25),
    Conv2D(32,(3,3),activation='relu',padding='same'),
    BatchNormalization(),
    SpatialDropout2D(0.25),
    
    Conv2D(32,(3,3),activation='relu',padding='same'),
    BatchNormalization(),
    SpatialDropout2D(0.25),
    Conv2D(32,(5,5),strides=2,activation='relu',padding='same'),
    BatchNormalization(),
    SpatialDropout2D(0.25),
    
    Conv2D(64,(3,3),activation='relu',padding='same'),
    BatchNormalization(),
    SpatialDropout2D(0.25),
    Conv2D(32,(3,3),activation='relu',padding='same'),
    BatchNormalization(),
    SpatialDropout2D(0.25),
    
    
    Conv2D(64,(3,3),activation='relu',padding='same'),
    BatchNormalization(),
    SpatialDropout2D(0.25),
    Conv2D(64,(5,5),strides=2,activation='relu',padding='same'),
    BatchNormalization(),
    SpatialDropout2D(0.25),
    
    
    
    
    
    Conv2D(128,(4,4),activation='relu',kernel_regularizer=l1(5e-4),padding='same'),
    Conv2D(8,(3,3),activation='relu',padding='same'),
    BatchNormalization(),
    SpatialDropout2D(0.25),
    Flatten(),
    Dense(128,activation='relu'),
    Dense(10,activation='softmax')
])


# In[ ]:


model.summary()


# In[ ]:


from tensorflow.keras.optimizers import Adam,RMSprop
opt=RMSprop(
    learning_rate=0.002,
    rho=0.9,
    momentum=0,
    epsilon=1e-07,
    centered=False,
    name="RMSprop"
)
model.compile(loss='sparse_categorical_crossentropy',optimizer=opt,metrics=['accuracy'])


# In[ ]:


history=model.fit(X_train,y_train,verbose=1,epochs=12,batch_size=128,validation_data=(X_val,y_val))


# In[ ]:


test_labels=model.predict(test)
test_labels


# In[ ]:


def plotLearningCurve(history,epochs):
    epochRange = range(1,epochs+1)
    plt.plot(epochRange,history.history['accuracy'])
    plt.plot(epochRange,history.history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend(['Train','Validation'],loc='upper left')
    plt.show()

    plt.plot(epochRange,history.history['loss'])
    plt.plot(epochRange,history.history['val_loss'])
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(['Train','Validation'],loc='upper left')
    plt.show()


# In[ ]:


plotLearningCurve(history,12)


# In[ ]:


test_labels.shape


# In[ ]:


print(history)


# In[ ]:


results = np.argmax(test_labels,axis = 1)
results = pd.Series(results,name="Label")
submission = pd.concat([pd.Series(range(1,28001),name = "ImageId"),results],axis = 1)

#submission.to_csv("submission.csv",index=False)


# ### uncomment the last line to do your submission

# In[ ]:


results.head()


# ## Thankyou for Reading!!!

# In[ ]:




