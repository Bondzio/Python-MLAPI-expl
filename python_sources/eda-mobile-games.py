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
get_ipython().run_line_magic('matplotlib', 'inline')

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# # Exploratory data Analysis

# In[ ]:


df = pd.read_csv('/kaggle/input/17k-apple-app-store-strategy-games/appstore_games.csv', parse_dates=['Original Release Date','Current Version Release Date'])


# In[ ]:


df.head()


# In[ ]:


df.info()


# In[ ]:


# analysing missing data
plt.figure(figsize=(8,6))
sns.heatmap(df.isnull(),cbar=False, cmap='viridis');


# In[ ]:


df.describe()


# In[ ]:


df.describe(include='O')


# In[ ]:


plt.figure(figsize=(12,4))
sns.countplot(x='Average User Rating', data=df).set_title("Average User Rating");


# In[ ]:


plt.figure(figsize=(12,4))
sns.countplot(x='Average User Rating', hue='Age Rating', data=df).set_title("Average User Rating x Age Rating");


# In[ ]:


plt.figure(figsize=(6,8))
sns.countplot(y='Primary Genre', data=df).set_title("Primary Genre");


# In[ ]:


Languages = pd.DataFrame(df['Languages'].str.split(',', expand=True).values.ravel(), columns=['Languages'])
sns.countplot(x='Languages', data=Languages, order=pd.value_counts(Languages['Languages']).iloc[:10].index).set_title("Top 10 Languages");


# In[ ]:


df.Genres.value_counts()


# In[ ]:


plt.figure(figsize=(6,8))
Genres = pd.DataFrame(df.Genres.str.split(',',expand=True).values.ravel(), columns=['Genre'])
sns.countplot(y='Genre', data=Genres, order=pd.value_counts(Genres['Genre']).iloc[:20].index).set_title("Top 20 Genre");


# In[ ]:


df.groupby(['Primary Genre'], sort=False).agg({'Price':[min,'mean','std',max,'count']})


# In[ ]:


def fast_df_plot(x):
    sns.set()
    df1 = pd.DataFrame(x.dt.year.value_counts()).reset_index()
    return sns.lineplot(x=df1.iloc[:,0], y=df1.iloc[:,1]).set_title("Original Release Date x Year")

fast_df_plot(df['Original Release Date']);


# In[ ]:


def fast_df_plot(x):
    sns.set()
    df1 = pd.DataFrame(x.dt.year.value_counts()).reset_index()
    return sns.lineplot(x=df1.iloc[:,0], y=df1.iloc[:,1]).set_title("Current Version Release Date")

fast_df_plot(df['Current Version Release Date']);


# In[ ]:


plt.figure(figsize=(12,8))
sns.lineplot(x='Original Release Date', y='Size', data=df).set_title("Original Release Date x Size");


# In[ ]:


plt.figure(figsize=(12,8))
sns.lineplot(x='Current Version Release Date', y='Size', data=df).set_title("Current Version Release Date x Size");


# In[ ]:


sns.scatterplot(x='Size', y='Average User Rating', data=df).set_title('Size x Average User Rating');


# In[ ]:


sns.scatterplot(x='Size', y='Price', data=df).set_title('Size x Price');


# In[ ]:


sns.scatterplot(x='Price', y='Average User Rating', data=df).set_title('Price x Average User Rating');

