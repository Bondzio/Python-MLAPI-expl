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


pd.read_csv('/kaggle/input/random-numbers/random_numbers_1000.csv').describe()


# In[ ]:


pd.read_csv('/kaggle/input/random-numbers/random_numbers_10000.csv').describe()


# In[ ]:


pd.read_csv('/kaggle/input/random-numbers/random_numbers_100000.csv').describe()


# In[ ]:


pd.read_csv('/kaggle/input/random-numbers/random_numbers_1000000.csv').describe()


# In[ ]:


pd.read_csv('/kaggle/input/random-numbers/random_numbers_10000000.csv').describe()


# Hmmm, looks like the more numbers we generate, the closer the quantiles are to the expected values. What a surpise!
