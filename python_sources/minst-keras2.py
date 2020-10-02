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
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


train_df=pd.read_csv('../input/train.csv')
test_df=pd.read_csv('../input/test.csv')


# In[ ]:


from keras.models import Sequential
from keras.layers import  Dense, Flatten, Dropout
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.models import load_model
from keras.optimizers import Adam

from keras.preprocessing.image import img_to_array, array_to_img


# In[ ]:


train_data = np.array(train_df, dtype='float32')
test_data = np.array(test_df, dtype='float32')


# In[ ]:


X_train = train_data[:, 1:] / 255
Y_train = train_data[:, 0]
X_test = test_data[:, :] / 255


# In[ ]:





# In[ ]:


im_rows = 28
im_cols = 28
batch_size = 512
im_shape = (im_rows, im_cols, 1)


# In[ ]:


X_train = X_train.reshape(-1, *im_shape)
X_train.shape


# In[ ]:


X_test = X_test.reshape(-1, *im_shape)
X_test.shape


# In[ ]:


Y_train=Y_train.reshape(-1,1)


# In[ ]:


#x_train, x_validate, y_train, y_validate = train_test_split(
    #X_train, Y_train, test_size=0.2, random_state=42,
#)


# In[ ]:


model=Sequential()
model.add(Flatten(input_shape=im_shape))
model.add(Dense(512,activation='relu'))
model.add(Dropout(.2))
model.add(Dense(512,activation='relu'))
model.add(Dropout(.2))
model.add(Dense(10,activation='softmax'))

           


# In[ ]:


model.summary()


# In[ ]:


X_train = X_train.reshape(-1, *im_shape)


# In[ ]:


model.compile(loss='sparse_categorical_crossentropy',
    optimizer=Adam(lr=0.01),
    metrics=['accuracy'])


# In[ ]:





# In[ ]:


score=model.evaluate(x_validate,y_validate,verbose=0)


# In[ ]:


accursy=100*score[1]
accursy


# In[ ]:


#from keras.callbacks import ModelCheckpoint


# In[ ]:


model.fit(X_train, Y_train,batch_size=128,epochs=20,validation_split=.2,verbose=1)


# In[ ]:


model.save('model1.h5')
model.save_weights('model_weigh1t.h5')


# In[ ]:


new_model1=load_model('model1.h5')


# In[ ]:


y_pred = new_model1.predict(X_test)


# In[ ]:


y_pred


# In[ ]:


test_pred1 = pd.DataFrame(new_model1.predict(X_test, batch_size=100))
test_pred1 = pd.DataFrame(test_pred1.idxmax(axis = 1))
test_pred1.index.name = 'ImageId'
test_pred1 = test_pred1.rename(columns = {0: 'Label'}).reset_index()
test_pred1['ImageId'] = test_pred1['ImageId'] + 1


# In[ ]:


test_pred1.to_csv('mnist_submission1.csv', index = False)


# In[ ]:




