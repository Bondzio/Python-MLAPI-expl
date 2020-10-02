#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import tensorflow as tf

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# THIS NOTEBOOK FOLLOWS CHAPTER 13 OF Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow, 2nd Edition
# 

# In[ ]:


X = tf.range(10)
dataset = tf.data.Dataset.from_tensor_slices(X)
dataset


# In[ ]:


for item in dataset:
    print(item)


# In[ ]:


dataset = dataset.repeat(3).batch(7)
for item in dataset:
    print(item)


# In[ ]:


dataset = dataset.map(lambda x: x * 2)


# In[ ]:


dataset = dataset.apply(tf.data.experimental.unbatch())


# In[ ]:


dataset = dataset.filter(lambda x: x < 10)


# In[ ]:


for item in dataset.take(3):
    print(item)


# In[ ]:


dataset = tf.data.Dataset.range(10).repeat(3)
dataset = dataset.shuffle(buffer_size=5, seed=42).batch(7)
for item in dataset:
    print(item)


# In[ ]:


with tf.io.TFRecordWriter("my_data.tfrecord") as f:
    f.write(b"This is the first record")
    f.write(b"And this is the second record")


# In[ ]:


filepaths = ["my_data.tfrecord"]
dataset = tf.data.TFRecordDataset(filepaths)
for item in dataset:
    print(item)


# In[ ]:


options = tf.io.TFRecordOptions(compression_type="GZIP")
with tf.io.TFRecordWriter("my_compressed.tfrecord", options) as f:
    f.write(b"This is the first record")
    f.write(b"And this is the second record")


# In[ ]:


dataset = tf.data.TFRecordDataset(["my_compressed.tfrecord"],
                                  compression_type="GZIP")


# In[ ]:





# In[ ]:





# In[ ]:




