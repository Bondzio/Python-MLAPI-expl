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


df = pd.read_csv("../input/corona-virus-report/covid_19_clean_complete.csv")


# In[ ]:


df.head(25)


# In[ ]:


import seaborn as sns 
import matplotlib.pyplot as plt 


# In[ ]:


plt.figure(figsize=(40,25))
sns.scatterplot(x='Country/Region', y='Confirmed', data = df)


# In[ ]:


#WorldWideHueMap 
#Work in progress #STAY_SAFE
plt.figure(figsize=(10,8))
sns.scatterplot(x='Long', y= 'Lat', hue = "Deaths", data = df, alpha =0.2)


# In[ ]:




