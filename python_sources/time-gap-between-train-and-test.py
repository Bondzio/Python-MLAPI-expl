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


# In[ ]:


dtypes = {
        'ip':'uint32',
        'app': 'uint16',
        'device': 'uint16',
        'os': 'uint16',
        'channel': 'uint16',
        'is_attributed': 'uint8'
        }
train_df  = pd.read_csv('../input/train.csv', dtype=dtypes)
test_df  = pd.read_csv('../input/test.csv', dtype=dtypes)


# ## There is a big max Train click_time and min test click_time

# In[ ]:


print(train_df['click_time'].max())
print(test_df['click_time'].min())


# > be carefull about that, I am not sure why there is a gap between training set and test set too. But it is a big challange
