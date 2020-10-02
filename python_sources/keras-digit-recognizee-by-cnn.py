#!/usr/bin/env python
# coding: utf-8

# ### HI!! It is my first keras kernel
# ### I happy to receive your comment and suggestion

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

from keras.models import Sequential
from keras.utils import np_utils
from keras.layers import Dense, Dropout,Activation,Conv2D,MaxPooling2D,Flatten
from keras.optimizers import Adam

from sklearn.model_selection import train_test_split

import os
print(os.listdir("../input"))


# In[3]:


train = pd.read_csv('../input/train.csv').values.astype('int32')
test = pd.read_csv('../input/test.csv').values.astype('int32')


# In[4]:


x_train, x_test, y_train, y_test= train_test_split(train[:,1:],train[:,0],test_size=0.2)


# In[5]:


x_train.shape,x_test.shape


# In[6]:


plt.imshow(x_train[0].reshape(28,28),cmap='Greys')


# In[7]:


x_train = x_train.reshape(-1,28,28,1)
x_test = x_test.reshape(-1,28,28,1)


# In[8]:


scale = np.max(x_train)
x_train = x_train.astype('float32') /scale
x_test = x_test.astype('float32') /scale


# In[9]:


y_train = np_utils.to_categorical(y_train,10)
y_test = np_utils.to_categorical(y_test,10)


# In[10]:


y_train.shape,y_test.shape


# In[11]:


model = Sequential()
model.add(Conv2D(32,(3,3),padding='same',activation='relu',input_shape=(28,28,1)))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.15))

model.add(Conv2D(64,(3,3),padding='same',activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.15))

model.add(Flatten())

model.add(Dense(200,activation='relu'))
model.add(Dropout(0.15))
model.add(Dense(400,activation='relu'))
model.add(Dropout(0.30))

model.add(Dense(10,activation='softmax'))


# In[12]:


model.compile(loss='categorical_crossentropy',optimizer=Adam(lr=1e-4),metrics=['accuracy'])


# In[13]:


model.fit(x_train,y_train,epochs=10,batch_size=16,validation_split=0.1,verbose=2)


# In[14]:


loss,accuracy = model.evaluate(x_test,y_test,verbose=0)
print('loss score:{0:.4f}, final score:{1:.4f}'.format(loss,accuracy))


# In[15]:


pick = np.random.randint(1,8400,5)
for i in range(5):
    plt.subplot(1,5,i+1)
    plt.imshow(x_test[pick[i]].reshape(28,28),cmap='Greys')
    plt.axis('off')


# In[16]:


X_test = test.astype('float32')
X_test = X_test.reshape(-1,28,28,1)/255.
predict = model.predict_classes(X_test)


# In[17]:


model_json = model.to_json()
open('digit_recognizer_model_cnn.json','w').write(model_json)
model.save_weights('digit_recognizer_weights_model_cnn.h5')


# In[18]:


def write_predict(predict,name):
    pd.DataFrame({'ImageId':list(range(1,len(predict)+1)),'label':predict}).to_csv(name,index=False,header=True)
    
write_predict(predict,'keras_digit_recognizer_by_cnn.csv')


# In[ ]:




