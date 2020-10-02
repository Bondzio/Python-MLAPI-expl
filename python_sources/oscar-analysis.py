#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import matplotlib
import matplotlib.pyplot as plt 
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set()

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# ### Read the CSV into a pandas dataframe

# In[ ]:


oscar_df = pd.read_csv('../input/demographics-of-academy-awards-oscars-winners/Oscars-demographics-DFE.csv', encoding='latin')
oscar_df.head()


# ### Observe the columns of the oscar dataframe

# In[ ]:


oscar_df.columns


# ### Observe diversity in the Oscars

# In[ ]:


def plotdiversity(data,cat):
    l=data.groupby(cat).size()
    l=np.log(l)
    l=l.sort_values()
    fig=plt.figure(figsize=(35,7))
    plt.yticks(fontsize=8)
    l.plot(kind='bar',fontsize=12,color='r')
    plt.xlabel('')
    plt.ylabel('Number of reports',fontsize=10)

plotdiversity(oscar_df,'race_ethnicity')


# ### Observe religion

# In[ ]:


def plotreligion(data,cat):
    l=data.groupby(cat).size()
    l=np.log(l)
    l=l.sort_values()
    fig=plt.figure(figsize=(35,7))
    plt.yticks(fontsize=8)
    l.plot(kind='bar',fontsize=12,color='b')
    plt.xlabel('')
    plt.ylabel('Number of reports',fontsize=10)

plotreligion(oscar_df,'religion')


# ### Observe gender

# In[ ]:


def plotgender(data,cat):
    l=data.groupby(cat).size()
    l=np.log(l)
    l=l.sort_values()
    fig=plt.figure(figsize=(35,7))
    plt.yticks(fontsize=8)
    l.plot(kind='bar',fontsize=12,color='y')
    plt.xlabel('')
    plt.ylabel('Number of reports',fontsize=10)

plotgender(oscar_df,'sexual_orientation')


# ### Group by awards

# In[ ]:


def plotawards(data,cat):
    l=data.groupby(cat).size()
    l=np.log(l)
    l=l.sort_values()
    fig=plt.figure(figsize=(35,7))
    plt.yticks(fontsize=8)
    l.plot(kind='bar',fontsize=12,color='g')
    plt.xlabel('')
    plt.ylabel('Number of reports',fontsize=10)

plotawards(oscar_df,'award')


# In[ ]:




