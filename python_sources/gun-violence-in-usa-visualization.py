#!/usr/bin/env python
# coding: utf-8

# #  Visualization for Gun violence cases in USA

# ### The peaks of the plot show which state has more such cases and the shaded region between killed and injured depicts how many of these cases lead to death of the victim. Lesser the space, more the deaths from Gun violence. 

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


# In[3]:


data = pd.read_csv('../input/gun-violence-data_01-2013_03-2018.csv')


# In[4]:


data.head()


# In[7]:


data = data.loc[:, ['state', 'n_killed', 'n_injured']]


# In[12]:


data = data.sort_values(by='state').groupby('state').aggregate({'n_killed': np.sum, 'n_injured': np.sum})


# In[13]:


data.head()


# In[14]:


import matplotlib.pyplot as plt


# In[46]:


plt.figure()
plt.plot(data.loc[:, 'n_killed'].values, 'r', label='Killed')
plt.plot(data.loc[:, 'n_injured'].values, 'b', label='Injured')
plt.legend(frameon=False)
N = len(data.index)
plt.xticks(np.arange(0, N), data.index, rotation='90')
plt.gca().margins(x=0)
plt.gcf().canvas.draw()
tl = plt.gca().get_xticklabels()
maxsize = max([t.get_window_extent().width for t in tl])
m = 0.5 # inch margin
s = maxsize / plt.gcf().dpi * N + 2 * m
margin = m / plt.gcf().get_size_inches()[0]

plt.gcf().subplots_adjust(left=margin, right=1.-margin)
plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)

plt.xlabel('State Name')
plt.ylabel('Number of Cases')

plt.gca().fill_between(range(0, N), data.loc[:, 'n_killed'], data.loc[:, 'n_injured'], facecolor='yellow', alpha=0.5)

