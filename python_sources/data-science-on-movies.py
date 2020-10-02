#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns  # visualization tool

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


df = pd.read_csv("../input/movies_metadata.csv")


# In[ ]:


df.info()


# In[ ]:


# View the top 5 rows
df.head()


# In[ ]:


# View the bottom rows
df.tail()


# In[ ]:


df.describe()


# In[ ]:


df.columns.values


# In[ ]:


# size of the dataframe : rows and columns
df.shape


# In[ ]:


# How many null objects in the datasets
df.isnull().sum()


# In[ ]:


# Filtering on the list of Movie Titles
df.title


# In[ ]:


#lang = df[df.original_language=='tr'].original_title
#df[['original_language', 'original_title']]
#lang.head()
# ----------------------------------------------------------
lang = df.loc[df.original_language=='tr', 'original_title']
lang.head()
# -----------------------------------------
#dil = pd.read_csv("../input/movies_metadata.csv", index_col='original_language')
#dil = df.loc[df.original_language=='tr', 'original_title']
#dil.head()


# In[ ]:


df.corr()


# In[ ]:


#correlation map
f,ax = plt.subplots(figsize=(8, 8))
sns.heatmap(df.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
plt.show()

