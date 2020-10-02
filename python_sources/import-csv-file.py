#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


#  Firslty import pandas library


# In[ ]:


import pandas as pd


# In[ ]:


# Import the Marks.csv in pd in data1


# In[ ]:


data1=pd.read_csv("../input/Marks1.csv")


# In[ ]:


print(data1)


# In[ ]:


# For first 5 rows


# In[ ]:


print(data1.head(5))


# In[ ]:


#For last 5 rows


# In[ ]:


print(data1.tail(5))


# In[ ]:





# In[ ]:


type(data1)


# In[ ]:




