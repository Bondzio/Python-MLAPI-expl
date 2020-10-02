#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas  # data processing, CSV file I/O (e.g. pd.read_csv)
import pandas_profiling
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


Bce_data=pandas.read_csv('/kaggle/input/border-crossing-entry-data/Border_Crossing_Entry_Data.csv')


# In[ ]:


Bce_data.head()


# In[ ]:


# Generating the profilling report

pandas_profiling.ProfileReport(Bce_data)

