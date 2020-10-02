#!/usr/bin/env python
# coding: utf-8

# In[15]:


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


# Using the Pandas library, we can load a DataFrame from a CSV file or many other formats.
# 
# For reference, see the documation at https://pandas.pydata.org/pandas-docs/stable/

# In[16]:


df = pd.read_csv('../input/FAO.csv', encoding='latin-1')


# The [DataFrame.head()](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.head.html#pandas.DataFrame.head) method allows you to peek at the first few rows of a DataFrame.

# In[20]:


df.head()


# In[26]:


# Where are the top maize producers in the year 2000?
maize_df = df[df['Item'] == 'Maize and products'].sort_values('Y2000', ascending=False)
maize_df.head(n=10).plot.bar(x='Area', y='Y2000', figsize=(15, 7), fontsize=20)


# In[ ]:




