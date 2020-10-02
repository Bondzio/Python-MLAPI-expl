#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

test = pd.read_csv('../input/mnist-in-csv/mnist_test.csv')
train = pd.read_csv('../input/mnist-in-csv/mnist_train.csv')


# In[ ]:


import matplotlib.pyplot as plt
import matplotlib.image as img
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


np.random.seed(2)
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import itertools


# In[ ]:


from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense,Dropout,Flatten,Conv2D,MaxPool2D
from keras.optimizers import RMSprop
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau


# In[ ]:


sns.set(style='white', context='notebook', palette='deep')


# In[ ]:


Y_train =  train["label"]                                        # 
X_train =  train.drop(labels=["label"],axis = 1)                 #
g = sns.countplot(Y_train)
Y_train.value_counts()


# In[ ]:


X_train.isnull().any().describe()


# In[ ]:


test.isnull().any().describe()


# In[ ]:


X_train = X_train/255.0


# In[ ]:


test = test/255.0


# In[ ]:


X_train = X_train.reshape(28,28,1)


# In[ ]:


test = test.values.reshape(-1,28,28,1)

