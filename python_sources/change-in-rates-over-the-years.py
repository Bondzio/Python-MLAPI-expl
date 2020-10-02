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


# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv('/kaggle/input/russian-demography/russian_demography.csv')


# In[ ]:


data.head()


# In[ ]:


data.info()


# In[ ]:


# we can see there are some empty rows
data.isnull().sum()


# In[ ]:


# let's drop any row with empty column
data.dropna(inplace=True)


# In[ ]:


data.isnull().sum()


# In[ ]:


data.head()


# In[ ]:


# checking how the data is
data[data['region'] == 'Tula Oblast']


# So the data is grouped for each region

# In[ ]:


data['region'].unique()


# In[ ]:


# natural popluation growth of all regions
data.groupby('region').agg({'npg': 'mean'}).plot.bar(figsize=(15,8))
plt.title('Natural population growth of regions over the years')


# In[ ]:


# Population difference for moscow over the years
plt.figure(figsize=(15,8))
sns.lineplot(data.groupby('region').get_group('Moscow')['year'], data.groupby('region').get_group('Moscow')['population'])
plt.title('Population difference for moscow over the years')


# In[ ]:


regions_w_highest_population = data.groupby('region').agg({'population': 'sum'}).sort_values(by="population",ascending=False)[:10].index.values
plt.figure(figsize=(15,8))
for x in regions_w_highest_population:
    sns.lineplot(data.groupby('region').get_group(x)['year'], data.groupby('region').get_group(x)['population'], label=x)
plt.title('Population difference for top 10 regions with most population')


# As, we can see there was a sudden dip in the population near 2005 and then it again began to increase 7 years later

# In[ ]:


highest_death_regions = data.groupby('region').agg({'death_rate': 'sum'}).sort_values(by="death_rate",ascending=False)[:10].index.values
plt.figure(figsize=(15,8))
for x in highest_death_regions:
    sns.lineplot(data.groupby('region').get_group(x)['year'], data.groupby('region').get_group(x)['population'], label=x)
plt.title('Death rate change for top 10 regions with most death rate')


# Looks like kursk Oblast had the highest death rate, let's look at its other attributes

# In[ ]:


kursk_oblast_viz = data.groupby('region').get_group('Kursk Oblast')
plt.figure(figsize=(15,8))
sns.lineplot(kursk_oblast_viz['year'], kursk_oblast_viz['npg'], label="natural popuplation growth")
sns.lineplot(kursk_oblast_viz['year'], kursk_oblast_viz['birth_rate'], label="birth rate")
sns.lineplot(kursk_oblast_viz['year'], kursk_oblast_viz['death_rate'], label="death rate")
sns.lineplot(kursk_oblast_viz['year'], kursk_oblast_viz['migratory_growth'], label="migratory growth")
plt.title('Kursk Oblast change over the years')


# In[ ]:


moscow_viz = data.groupby('region').get_group('Moscow')
plt.figure(figsize=(15,8))
sns.lineplot(moscow_viz['year'], moscow_viz['npg'], label="natural popuplation growth")
sns.lineplot(moscow_viz['year'], moscow_viz['birth_rate'], label="birth rate")
sns.lineplot(moscow_viz['year'], moscow_viz['death_rate'], label="death rate")
sns.lineplot(moscow_viz['year'], moscow_viz['migratory_growth'], label="migratory growth")
plt.title('Moscow change over the years')


# In[ ]:




