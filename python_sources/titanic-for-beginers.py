#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


# Check the first 5 rows of train.csv
df_train = pd.read_csv("../input/train.csv")
df_train.head()


# In[ ]:


# Check the first 5 rows of train.csv
df_test = pd.read_csv("../input/test.csv")
df_test.head()


# In[ ]:


# Check statistics information for df_train
df_train.info()

