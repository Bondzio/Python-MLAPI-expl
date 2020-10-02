#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# In[ ]:


import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


tips=pd.read_csv('../input/tips.csv')


# In[ ]:


tips.head()


# In[ ]:


sns.lmplot(x='total_bill',y='tip',data=tips)


# In[ ]:


sns.lmplot(x='total_bill',y='tip',data=tips,hue='sex')


# In[ ]:


# http://matplotlib.org/api/markers_api.html
sns.lmplot(x='total_bill',y='tip',data=tips,hue='sex',palette='coolwarm',
           markers=['o','v'],scatter_kws={'s':100})


# In[ ]:


sns.lmplot(x='total_bill',y='tip',data=tips,col='sex')


# In[ ]:


sns.lmplot(x="total_bill", y="tip", row="sex", col="time",data=tips)


# In[ ]:


sns.lmplot(x='total_bill',y='tip',data=tips,col='day',hue='sex',palette='coolwarm')


# In[ ]:


sns.lmplot(x='total_bill',y='tip',data=tips,col='day',hue='sex',palette='coolwarm',
          aspect=0.6,size=8)


# In[ ]:




