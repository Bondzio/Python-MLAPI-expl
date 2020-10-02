#!/usr/bin/env python
# coding: utf-8

# In[3]:


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


# In[1]:


print("Hello notebook")


# In[4]:


data_train_file = "../input/fashion-mnist_train.csv"
data_test_file = "../input/fashion-mnist_test.csv"

df_train = pd.read_csv(data_train_file)
df_test = pd.read_csv(data_test_file)


# In[5]:


df_train.head()


# In[6]:


df_train.describe()


# In[9]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

for i in range(5000,5005):
    sample = np.reshape(df_test[df_test.columns[1:]].iloc[i].values/255,(28,28) )
    plt.figure()
    plt.title("labled class {}".format(df_test["label"].iloc[i]))
    plt.imshow(sample, 'gray')


# In[ ]:




