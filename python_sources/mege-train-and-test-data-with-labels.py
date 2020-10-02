#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


train = pd.read_csv('../input/train.csv')


# In[4]:


test = pd.read_csv('../input/test.csv')


# In[6]:


test_label = pd.read_csv('../input/test_labels.csv')


# In[14]:


test = pd.merge(test,test_label,on='id')


# In[16]:


test = test.loc[test['toxic']!=-1]


# In[18]:


train.append(test).to_csv('train.csv')


# In[ ]:




