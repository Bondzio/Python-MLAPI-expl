#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np
import itertools
plt.style.use('fivethirtyeight')

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


df=pd.read_csv('../input/uncover/coders_against_covid/crowd-sourced-covid-19-testing-locations.csv')
df.head()


# In[ ]:


df.groupby(['is_verified'])
df


# In[ ]:


plt.clf()
df.groupby('is_verified').size().plot(kind='bar')
plt.show()


# In[ ]:


plt.clf()
df.groupby('is_hidden').size().plot(kind='bar')
plt.show()


# In[ ]:


plt.clf()
df.groupby('is_location_screening_patients').size().plot(kind='bar')
plt.show()


# In[ ]:


plt.clf()
df.groupby('is_location_collecting_specimens').size().plot(kind='bar')
plt.show()

