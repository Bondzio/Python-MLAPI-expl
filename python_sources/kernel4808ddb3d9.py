#!/usr/bin/env python
# coding: utf-8

# In[39]:


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


# In[40]:


train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')
sample = pd.read_csv('../input/sample_submission.csv')


# In[41]:


train = train.iloc[:,0:31]
test = test.iloc[:,0:30]


# In[42]:


x = train.drop('diagnosis', axis =1)
y = train['diagnosis']


# In[43]:


from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25)


# In[44]:


print('shape x_train', x_train.shape)
print('shape x_test', x_test.shape)
print('shape y_train', y_train.shape)
print('shape y_test', y_test.shape)


# In[45]:


from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import accuracy_score


# In[46]:


classify = Sequential()
classify.add(Dense(units=8,activation='relu',kernel_initializer='normal',input_dim=len(x_train)))
classify.add(Dense(units=16,activation='relu',kernel_initializer='normal'))
classify.add(Dense(units=1,activation='sigmoid'))
classify.compile(optimizer='adam',loss="binary_crossentropy",metrics=['binary_accuracy'])
classify.fit(x_train,y_train,batch_size=10,epochs=300)
y_pred = classify.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)
print(accuracy)

