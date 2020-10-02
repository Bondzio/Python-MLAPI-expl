#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


df=pd.read_csv('/kaggle/input/videogamesales/vgsales.csv')


# In[ ]:


df.head() #check exp default 5


# In[ ]:


df.corr() #show chart 


# Let us visualize for a better understanding.
# 

# In[ ]:


f,ax=plt.subplots(figsize=(12,12))
sns.heatmap(df.corr(),annot=True,linewidth=.5,fmt='.2f',ax=ax) #annot =numbered notation,fmt=digit


#  NA_Sales and EU_Sales have big corr

# In[ ]:


df.columns


# In[ ]:


df['NA_Sales'].plot(kind='line',figsize = (12,6),color='yellow',label='NA',linewidth=1,alpha = 0.5,grid = True,linestyle = ':',fontsize='12')
df['EU_Sales'].plot(kind='line',figsize = (12,6),color='black',label='EU',linewidth=1,alpha = 0.5,grid = True,linestyle = '-.',fontsize='12')
plt.legend(loc='upper right') 
plt.xlabel('x axis')              # label = name of label
plt.ylabel('y axis')
plt.title('Line Plot')            # title = title of plot
plt.show()


# In[ ]:


df.plot(kind='scatter', x='NA_Sales', y='EU_Sales',alpha = 0.5,color = 'red',figsize = (5,5))
plt.xlabel('NA_Sales')              # label = name of label
plt.ylabel('EU_Sales')
plt.title('NA EU Sales - Scatter Plot') 


# >We understood the intensity better.

# In[ ]:


df['NA_Sales'].plot(kind = 'hist',bins = 50,figsize = (5,5))
plt.show()


# In[ ]:


df['EU_Sales'].plot(kind = 'hist',bins = 50,figsize = (5,5))
plt.show()


# >Same in two histograms

# In[ ]:


df[(df['NA_Sales']>40) & (df['EU_Sales']<40)]


# The graphs show that the relationship is high, but there are some exceptions.
