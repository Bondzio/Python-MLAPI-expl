#!/usr/bin/env python
# coding: utf-8

# Here I have plotted some interesting observations using seaborn and matplotlib libraries.

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


df = pd.read_csv('../input/xAPI-Edu-Data.csv')
# Any results you write to the current directory are saved as output.
df.head()


# **Let us first get some visualisation of the data before moving onto Support Vector machine**

# In[ ]:


plt.figure(figsize=(11,7))
sns.countplot(x='PlaceofBirth',data=df,palette='muted')
plt.ylim(0,200)


# **We can see that student's place of birth are more in Kuwait and jordon while very few people are from Venzuela and morocco.**

# In[ ]:


x=[pd.Series(df['raisedhands']),pd.Series(df['Discussion'])]
y.head()
pda=pd.DataFrame(x).transpose()
pda.head()


# In[ ]:


plt.figure(figsize=(11,7))
sns.pairplot(data=pda)

