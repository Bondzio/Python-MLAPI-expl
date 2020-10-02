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


import pandas as pd

df = pd.read_csv('/kaggle/input/scl-dummy/Dummy data.csv')
print(df.head())
df


# In[ ]:


# x = range(101)

# for n in x:
#   print(n)
no = [[n, n+2] for n in range(101)]
df = pd.DataFrame(np.array(no), columns = ['id', 'new_number'])
df = df.set_index('id')
df


# In[ ]:


df.to_csv('submission.csv') # also can use df.to_csv('submission.csv', header= True, index= False) with out set_index()


# In[ ]:




