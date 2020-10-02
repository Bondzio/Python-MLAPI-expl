#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


data = pd.read_csv('/kaggle/input/iris/Iris.csv')
data.head(5)


# In[ ]:


data.columns


# In[ ]:


unsupervised_data = data.copy()
unsupervised_data.drop('Species',axis=1,inplace=True)
unsupervised_data.head()


# In[ ]:


X = unsupervised_data[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]


# In[ ]:


import scipy.cluster.hierarchy as shc

plt.figure(figsize=(10, 7))
plt.title("Iris Dataset")
dend = shc.dendrogram(shc.linkage(X, method='ward'))


# In[ ]:


from sklearn.cluster import AgglomerativeClustering

cluster = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')
clusters = cluster.fit_predict(X)


# In[ ]:


unsupervised_data['Clusters']=clusters
unsupervised_data['Cluster_name'] = unsupervised_data['Clusters'].map({0:'Cluster 1',1:'Cluster 2',2:'Cluster 3'})
unsupervised_data.head()


# In[ ]:


data.head(5)


# In[ ]:


for value in data['Species'].unique():
    print(value)


# In[ ]:


f, axes = plt.subplots(1,4,figsize=(15,5))
f.suptitle("Original data")
y = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']
hue = 'Species'
ax = 0
for y in y:
    sns.scatterplot(x = 'Id', y = y, hue = hue, data = data, ax = axes[ax])
    ax = ax + 1
    
f, axes = plt.subplots(1,4,figsize=(15,5))
f.suptitle("Cluster on data without labels")
y = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']
hue = 'Cluster_name'
ax = 0
for y in y:
    sns.scatterplot(x = 'Id', y = y, hue = hue, data = unsupervised_data, ax = axes[ax])
    ax = ax + 1

