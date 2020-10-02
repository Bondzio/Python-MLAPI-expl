#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# # Football Stats
# 
# 
# * Cluster football players based on the following features
#     - tackles +won
#     - duels + won
#     - passes + won
#     - interception
#     - 
#     
# * Find outliers
#     - goalkeepers!
#     - 

# In[ ]:


# load data from url
url = "https://datafaculty.s3.us-east-2.amazonaws.com/Indore/song_football-class13.csv"

df = pd.read_csv(url, encoding="latin1")
df.head()


# In[ ]:


df.columns


# In[ ]:


# rename columns
df = df.rename(columns={'Player Id': 'pid', 'Tackles': 'tackles', 'Last_Name': 'lname', 'First_Name': 'fname'})
df.columns


# ### Data description
# 
# * pid *(Player Id) - id of the player
# * tackles - total number of tackles
# * wontackles - number of tackles won by the player 
# * duels - total number of duels
# * wonduels - number of duels won by the player
# * passes - total number of passes
# * wonpasses - 
# * interception - number of interceptions
# * Last_name
# * First_name
# 
# ### Indicators
# 
# * Ratio of wontackles to tackles - ideal is 1
# * Ratio of wonduels to duels - ideal is 1
# * Ratio of wonpasses to passes - ideal is 1
# * More the number of interceptions better the player
# 

# In[ ]:


df['name'] = df['fname'] + ' ' + df['lname']

df.drop(['fname', 'lname'], axis=1, inplace=True)


# In[ ]:


df.describe(include='all')


# ## Identify Goalkeepers!

# In[ ]:


df.loc[(df.interception <= 10) & (df.tackles <= 10) & (df.duels <= 10)]


# In[ ]:


sns.boxplot(x=df['tackles'])


# In[ ]:


sns.boxplot(x=df['duels'])


# In[ ]:





# ## Exploratory Data Analysis

# In[ ]:


# number of rows
len(df)


# In[ ]:


# NaN check
df.isna().sum()


# In[ ]:


# null check
df.isnull().sum()


# In[ ]:


# create the list of players
players = df['name'].values
players[:5]


# In[ ]:


numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
numeric_cols


# In[ ]:


numeric_cols.remove('pid')
numeric_cols


# In[ ]:


feature_cols = ['tackles', 'duels', 'passes', 'interception']
ratio_cols = ['wontackles', 'wonduels', 'wonpasses',]


# In[ ]:


numeric_data = df[numeric_cols]
numeric_data.sample(7)


# In[ ]:


sns.set()
plt.legend(ncol=2, loc='upper right');


# In[ ]:


for col in feature_cols:
    plt.hist(df[col], alpha=0.5)


# In[ ]:


for col in feature_cols:
    sns.kdeplot(df[col], shade=True)


# In[ ]:


for col in ratio_cols:
    sns.kdeplot(df[col], shade=True)


# In[ ]:


for col in ratio_cols:
    plt.hist(df[col], alpha=0.5)


# In[ ]:


sns.kdeplot(numeric_data[feature_cols])


# In[ ]:


sns.kdeplot(numeric_data[ratio_cols])


# In[ ]:


with sns.axes_style('white'):
    sns.jointplot('wontackles', 'wonduels', df, kind='kde')


# In[ ]:


with sns.axes_style('white'):
    sns.jointplot('wontackles', 'wonpasses', df, kind='kde')


# In[ ]:


g = sns.PairGrid(numeric_data, vars=feature_cols, palette='RdBu_r')
g.map(plt.scatter, alpha=0.8)
g.add_legend()


# In[ ]:


sns.scatterplot(x='tackles', y='wontackles', hue='pid', palette="Set2", data=df)


# ## Cluster

# In[ ]:


from sklearn.cluster import KMeans


# In[ ]:


X = df[numeric_cols].values


# In[ ]:


kmeans = KMeans(n_clusters=4)
kmeans


# In[ ]:


kmeans.fit(X)


# In[ ]:


y_kmeans = kmeans.predict(X)
y_kmeans


# In[ ]:


plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)


# In[ ]:


# cluster columns
def cluster_cols(df, l, n):
    
    X = df[l].values
    kmeans = KMeans(n_clusters=n)

    kmeans.fit(X)
    
    y_kmeans = kmeans.predict(X)
    
    plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
    
    return y_kmeans


# In[ ]:


tackles = ['tackles', 'wontackles']

cluster_cols(df, tackles, 6)


# In[ ]:


df.pid.unique()[:5]


# In[ ]:


numeric_data.head()


# In[ ]:


numeric_data['cluster'] = cluster_cols(df, numeric_cols, 8)


# In[ ]:


numeric_data.head()


# In[ ]:


g = sns.PairGrid(numeric_data, vars=feature_cols, hue='cluster', palette='RdBu_r')
g.map(plt.scatter, alpha=0.8)
g.add_legend()


# In[ ]:


df['cluster'] = numeric_data['cluster']
df.head()


# In[ ]:


sns.scatterplot(x='tackles', y='wontackles', hue='cluster', palette="Set2", data=df)


# In[ ]:


df['cluster'].value_counts()


# In[ ]:


df['name'].loc[df.cluster == 3].unique()


# In[ ]:


df['name'].loc[df.cluster == 4].unique()


# In[ ]:


df.loc[df.cluster == 4]


# In[ ]:


df.loc[df.cluster == 7]


# In[ ]:




