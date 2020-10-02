#!/usr/bin/env python
# coding: utf-8

# # Overview
# 
# I try to most simple visualization.
# 

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


df = pd.read_csv('/kaggle/input/death-due-to-air-pollution-19902017/death-rates-from-air-pollution.csv')
df


# In[ ]:


df.isnull().sum()


# Code only contains null values.  

# In[ ]:


null_code_df = df[df['Code'].isnull()]
null_code_df['Entity'].unique()


# Code means country code. So area consisting of multiple country or the region in the country don't have country code.

# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns

fig = sns.lineplot(x="Year", y="Air pollution (total) (deaths per 100,000)", data=df)
fig = sns.lineplot(x="Year", y="Indoor air pollution (deaths per 100,000)", data=df)
fig = sns.lineplot(x="Year", y="Outdoor particulate matter (deaths per 100,000)", data=df)
fig = sns.lineplot(x="Year", y="Outdoor ozone pollution (deaths per 100,000)", data=df)

plt.title("World wide death rates from air pollution")
plt.show()


# In[ ]:


entity_df = df.groupby('Code').mean().sort_values('Air pollution (total) (deaths per 100,000)', ascending=False)
entity_df['Code'] = entity_df.index
entity_df


# In[ ]:


sns.barplot(x="Code", y="Air pollution (total) (deaths per 100,000)", data=entity_df.head(10))
plt.title("Country ranking")
plt.show()


# # Future work
# 
# - Draw heatmap to the world map by using GeoPandas
# - Treat countries as groups by region
# - Clustering countries
# - Does the ratio of indoor and outdoor differ depending countries?
