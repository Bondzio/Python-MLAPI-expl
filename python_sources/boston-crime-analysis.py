#!/usr/bin/env python
# coding: utf-8

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


# In[2]:


import matplotlib.pyplot as plt 
import seaborn as sns


# In[3]:


os.chdir("../input")
os.listdir()


# In[4]:


df = pd.read_csv("../input/crime.csv",  encoding = "ISO-8859-1")


# In[5]:


df.shape
df.head(10)


# In[6]:


df.columns.values


# In[7]:


df.dtypes


# In[8]:


# Top 10 crime reported streets

streets = df.groupby([df['STREET'].fillna('NO STREET NAME')])['REPORTING_AREA'].aggregate(np.size).reset_index().sort_values('REPORTING_AREA',ascending = False).head(10)
streets


# In[9]:


sns.barplot(x="STREET", y="REPORTING_AREA", data = streets)


# In[10]:


ax = sns.barplot(x="STREET", y="REPORTING_AREA", data = streets)
ax.set(xlabel='Crime Street', ylabel='# of Crimes reported')
ax.set_xticklabels(streets['STREET'],rotation=90)

plt.show()


# In[34]:


# Top 10 Offense types

streets = df.groupby([df['OFFENSE_CODE_GROUP']])['STREET'].aggregate(np.size).reset_index().sort_values('STREET', ascending = False).head(10)
streets


# In[23]:


# Year wise percentage rate
yrlbl = df['YEAR'].astype('category').cat.categories.tolist()
yrlbl


# In[24]:


yrwisecount = df['YEAR'].value_counts()
yrwisecount


# In[33]:


sizes = [yrwisecount[year] for year in yrlbl]
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=yrlbl,  autopct='%1.1f%%',shadow=True) 
ax1.axis('equal')
ax1.set_title("Year wise crime %")
plt.show()


# In[38]:


# Day of the week crime %
dayofwkcount = df['DAY_OF_WEEK'].value_counts()
dayofwkcount

dayofwk = df['DAY_OF_WEEK'].astype('category').cat.categories.tolist()
dayofwk

sizes = [dayofwkcount[dow] for dow in dayofwk]
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=dayofwk,  autopct='%1.1f%%',shadow=True) 
ax1.axis('equal')
ax1.set_title("Day of week crime %")
plt.show()


# In[48]:


# Count of crimes - reporting district wise

crimedistrict = df.groupby([df['DISTRICT']])['STREET'].aggregate(np.size).reset_index().sort_values('STREET',ascending = False)

sns.barplot(x="DISTRICT", y="STREET", data = crimedistrict)

