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


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


# In[ ]:


import tensorflow as tf


# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


np.random.seed(3)
tf.random.set_seed(3)


# In[ ]:


Data_set = np.loadtxt("/kaggle/input/ThoraricSurgery.csv", delimiter= ",")


# In[ ]:


X = Data_set [:, 0:17]
Y = Data_set [:, 17]


# In[ ]:


model = Sequential()
model.add(Dense(30, input_dim=17, activation='relu'))
model.add(Dense(1, activation='sigmoid'))


# In[ ]:


model.compile(loss='mean_squared_error', optimizer = 'adam', metrics=['accuracy'])
model.fit(X, Y, epochs=100, batch_size = 10)


# In[ ]:




