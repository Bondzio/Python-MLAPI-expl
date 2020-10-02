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


# In[ ]:


df = pd.read_csv('/kaggle/input/paysim1/PS_20174392719_1491204439457_log.csv')


# In[ ]:


df.head()


# In[ ]:


df.drop('step',axis=1,inplace=True)
df.drop('nameOrig',axis=1,inplace=True)
df.drop('nameDest',axis=1,inplace=True)


# In[ ]:


df.head()


# In[ ]:


df.info()


# In[ ]:


from sklearn.preprocessing import LabelEncoder,MinMaxScaler


# In[ ]:


lb = LabelEncoder()


# In[ ]:


df['type'] = lb.fit_transform(df['type'])


# In[ ]:


X = df.drop('isFraud',axis=1)
y = df['isFraud']


# In[ ]:


mx = MinMaxScaler()


# In[ ]:


X = mx.fit_transform(X)


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


# In[ ]:


import keras
from keras.layers import Dense
from keras.models import Sequential


# In[ ]:


model = Sequential()


# In[ ]:


X.shape


# In[ ]:


model.add(Dense(7,input_shape=(7,),activation='relu'))


# In[ ]:


model.add(Dense(4,activation='relu'))
model.add(Dense(4,activation='relu'))
model.add(Dense(1,activation='sigmoid'))


# In[ ]:


model.compile(optimizer='adam', metrics=['accuracy'], loss='binary_crossentropy')


# In[ ]:


model.fit(X_train,y_train,epochs=15,batch_size=36,validation_data=(X_test,y_test),shuffle=True)


# In[ ]:


model.save('99.96%.m5')


# In[ ]:




