#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import pandas as pd
gdp = pd.read_csv("/kaggle/input/us-gdp-growth-rate/GDP.csv",index_col = "DATE",parse_dates = True)


# In[ ]:


gdp


# In[ ]:


gdp.tail()


# In[ ]:


gdp.head()


# In[ ]:


gdp.describe()


# In[ ]:


gdp.GDP.dtype


# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(20,10))
sns.lineplot(data = gdp['GDP'],label = "GDP of USA over time")
plt.xlabel("Time in years")
plt.ylabel("Change in GDP rate")


# In[ ]:


plt.figure(figsize=(20,10))
plt.title("Changes in GDP of USA from 1947 to 2020")
sns.barplot(x= gdp.index,y = gdp['GDP'])
plt.xlabel("Time in years")
plt.ylabel("Change in GDP over time")


# In[ ]:


plt.figure(figsize=(14,7))
sns.heatmap(data = gdp,annot=True)


# In[ ]:


plt.figure(figsize=(20,10))
plt.title("Changes in GDP of USA from 1947 to 2020")
sns.scatterplot(x= gdp.index,y = gdp['GDP'])
plt.xlabel("Arbitrary time in years")
plt.ylabel("Change in GDP over time")


# In[ ]:



# Color-coded scatter plot w/ regression lines
sns.swarmplot(y = gdp["GDP"],data=gdp)


# In[ ]:


sns.distplot(a=gdp['GDP'],kde=True) 


# In[ ]:


sns.kdeplot(data=gdp['GDP'],label="GDP Growth over time",shade=True)


# In[ ]:


sns.pairplot(gdp)


# In[ ]:


gdp["DATE"] = gdp.iloc[0:,0].astype(str)


# In[ ]:


gdp["DATE"] = gdp.iloc[0:,0].astype(int)


# In[ ]:


gdp.DATE.dtype


# In[ ]:


plt.figure(figsize=(20,10))
plt.title("Changes in GDP of USA from 1947 to 2020")
sns.scatterplot(x= gdp.index,y = gdp['GDP'])
plt.xlabel("Arbitrary time in years")
plt.ylabel("Change in GDP over time")


# In[ ]:


plt.figure(figsize=(20,10))
plt.title("Changes in GDP of USA from 1947 to 2020")
sns.lineplot(x= gdp.index,y = gdp['GDP'])
plt.xlabel("Time in years")
plt.ylabel("Change in GDP over time")


# In[ ]:




