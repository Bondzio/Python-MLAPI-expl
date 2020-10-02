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





# In[ ]:


India=pd.read_csv('/kaggle/input/covid-19-india-12th-march-2020/COVID 19 India.csv')


# In[ ]:


India


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")


# In[ ]:


IndianN= sns.barplot(x="Total confirmed cases(Indian National)", y="Name of State/UT", data=India)
IndianN


# In[ ]:


ForeignN= sns.barplot(x="Total confirmed cases(Foreign National)", y="Name of State/UT", data=India)
ForeignN


# In[ ]:


India['IndiaTotalCase']=India['Total confirmed cases(Indian National)']+ India['Total confirmed cases(Foreign National)']


# In[ ]:


India


# In[ ]:


IndianCovidCases= sns.barplot(x="IndiaTotalCase", y="Name of State/UT", data=India)
IndianCovidCases


# In[ ]:


death=pd.read_csv('/kaggle/input/covid-19-india-12th-march-2020/death case age.csv')
death


# In[ ]:





# In[ ]:




