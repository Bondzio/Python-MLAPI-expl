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

import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


train = pd.read_csv('../input/train.csv', index_col='ID_code')
train.head()


# In[ ]:


x = 0
def plot():
    global x
    sns.distplot(train.iloc[:, x])
    x += 1


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()


# In[ ]:


plot()

