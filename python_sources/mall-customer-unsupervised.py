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


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df = pd.read_csv('../input/mall-customers/Mall_Customers.csv')


# In[ ]:


df.columns  = ['id','gender','age','salary','score']


# In[ ]:


df.head()


# We have three columns of use age ,income ,score.

# In[ ]:


import seaborn as sns
sns.countplot(x = 'gender',data = df)


# In[ ]:


import plotly.express as px
px.box(df,y = 'score',x = 'gender',points = 'all')


# In[ ]:


px.box(df,y = 'age',x = 'gender',points = 'all')


# In[ ]:


sns.distplot(df['age'])


# In[ ]:


sns.distplot(df['score'])


# In[ ]:


plt.scatter(df['age'],df['score'], s=100, c='red')


# In[ ]:


def flip(x):
    if(x == 'Male'):
        return 0
    else:
        return 1
df['gender'] = df['gender'].apply(lambda x : flip(x))


# In[ ]:


df.head()


# In[ ]:


df.shape


# In[ ]:


df = df[['gender','age','salary','score']]
from sklearn.model_selection import train_test_split


# In[ ]:


from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=4)
y_hc = kmeans.fit_predict(df)


# In[ ]:


y_hc


# In[ ]:


print(kmeans.cluster_centers_.shape)


# In[ ]:


print(kmeans.cluster_centers_)


# In[ ]:


points = df


# In[ ]:


plt.scatter(points[y_hc ==0]['age'], points[y_hc ==0]['score'], s=100, c='red')
plt.scatter(points[y_hc ==1]['age'], points[y_hc ==1]['score'], s=100, c='black')
plt.scatter(points[y_hc ==2]['age'], points[y_hc ==2]['score'], s=100, c='blue')
plt.scatter(points[y_hc ==3]['age'], points[y_hc ==3]['score'], s=100, c='cyan')


# Implementing Agglomerative Hierarchical Clustering

# In[ ]:


import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering


# In[ ]:


# create dendrogram
dendrogram = sch.dendrogram(sch.linkage(df, method='ward'))
# create clusters
hc = AgglomerativeClustering(n_clusters=4, affinity = 'euclidean', linkage = 'ward')
# save clusters for chart
y_hc = hc.fit_predict(df)


# In[ ]:


from sklearn.mixture import GaussianMixture 
gmm_model = GaussianMixture(n_components = 4).fit(points)
y_hc = gmm_model.predict(points)


# In[ ]:


y_hc


# In[ ]:


plt.scatter(points[y_hc ==0]['age'], points[y_hc ==0]['score'], s=100, c='red')
plt.scatter(points[y_hc ==1]['age'], points[y_hc ==1]['score'], s=100, c='black')
plt.scatter(points[y_hc ==2]['age'], points[y_hc ==2]['score'], s=100, c='blue')
plt.scatter(points[y_hc ==3]['age'],
            points[y_hc ==3]['score'], s=100, c='cyan')


# In[ ]:


import scipy.spatial.distance
from sklearn.cluster import DBSCAN


# In[ ]:


can = DBSCAN(eps=7, min_samples=2).fit_predict(df)
#can = DBSCAN(eps=10, min_samples=2,metric= 'manhattan').fit_predict(df)
#can = DBSCAN(eps=7, min_samples=2,metric = 'l1').fit_predict(df
#can = DBSCAN(eps=1, min_samples=2,metric = 'dice').fit_predict(df)


# In[ ]:


len(list(set(can)))


# In[ ]:


can


# In[ ]:


#clustering for the first eight clusters , -1 means no cluster made for them uptil now.
plt.scatter(df[can ==0]['age'], df[can == 0]['score'], s=100, c='red')
plt.scatter(df[can ==-1]['age'], df[can == -1]['score'], s=100, c='black')
plt.scatter(df[can ==1]['age'], df[can == 2]['score'], s=100, c='blue')
plt.scatter(df[can ==3]['age'], df[can == 3]['score'], s=100, c='green')
plt.scatter(df[can ==4]['age'], df[can == 4]['score'], s=100, c='pink')
plt.scatter(df[can ==5]['age'], df[can == 5]['score'], s=100, c='orange')
plt.scatter(df[can ==6]['age'], df[can == 6]['score'], s=100, c='grey')
plt.scatter(df[can ==7]['age'], df[can == 7]['score'], s=100, c='violet')


# In[ ]:




