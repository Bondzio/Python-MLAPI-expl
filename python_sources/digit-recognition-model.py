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


import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split


# In[ ]:


train = pd.read_csv('/kaggle/input/digit-recognizer/train.csv')
test = pd.read_csv('/kaggle/input/digit-recognizer/test.csv')


# In[ ]:


class_names = ['0','1', '2','3','4','5','6','7','8','9']


# In[ ]:


train_image = (train.iloc[:,1:].values).astype('float32')
train_label = (train.iloc[:,0].values).astype('int32')
test_image = test.values.astype('float32')


# In[ ]:


train_image[0]


# In[ ]:


x_train,x_test,y_train, y_test = train_test_split(train_image, train_label, test_size = 0.2, random_state = 0)


# In[ ]:


model = keras.Sequential(
    [keras.layers.Flatten(input_shape = (28,28)),
    keras.layers.Dense(128, activation = "relu"),
    keras.layers.Dense(10, activation = "softmax") ]   
)
    


# In[ ]:


model.compile(optimizer = "adam", loss = "sparse_categorical_crossentropy", metrics = ["accuracy"])


# In[ ]:


model.fit(train_image,train_label, epochs=25)


# In[ ]:


predictions = model.predict(test)
print(class_names[np.argmax(predictions[0])])


# In[ ]:


results=[]
for i in range(28000):
    results.append(class_names[np.argmax(predictions[i])])
results=pd.Series(results,name="Label")


# In[ ]:


submission=pd.concat([pd.Series(range(1,28001),name="ImageId"),results],axis=1)


# In[ ]:


submission


# In[ ]:


submission.to_csv('My_submissions3',index=False)


# In[ ]:


my_submission=pd.read_csv('My_submissions3')


# In[ ]:


my_submission.head()


# In[ ]:




