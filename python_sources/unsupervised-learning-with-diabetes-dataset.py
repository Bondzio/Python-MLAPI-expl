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

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# # INTRODUCTION
# Hello.  I'm trying to learn unsupervised learning and these are my execises. I hope it help to you. If you find some bugs, please tell me. Thank you.
# 
# 1. [Dataset Features](#1)
# 1. [KMeans Clustering](#2)
# 1. [Standarization](#3)
# 1. [Hierarchy](#4)
# 1. [Hierarchical Clustering](#5)
# 

# <a id = "1"> </a><br>
# # Dataset Features

# In[ ]:


data = pd.read_csv('../input/pima-indians-diabetes-database/diabetes.csv')
data.head(10)


# In[ ]:


data.info()


# In[ ]:


data.describe()


# <a id = "2"> </a><br>
# # KMeans Clustering

# In[ ]:


#data1 visualization
plt.scatter(data['Glucose'], data['Insulin'])
plt.xlabel('Glucose')
plt.ylabel('Insulin')
plt.show()


# In[ ]:


#data2 visualization
plt.scatter(data['Glucose'], data['BloodPressure'])
plt.xlabel('Glucose')
plt.ylabel('BloodPressure')
plt.show()


# In[ ]:


# data1 create
data1 = data.loc[:, ['Glucose', 'Insulin']]
# KMEANS 1
from sklearn.cluster import KMeans
kmeans1 = KMeans(n_clusters=2)
kmeans1.fit(data1)
labels1 = kmeans1.predict(data1)

# visualization
plt.scatter(data['Glucose'], data['Insulin'], c = labels1)
plt.xlabel('Glucose')
plt.ylabel('Insulin')
plt.show()


# In[ ]:


# data2 create
data2 = data.loc[:, ['Glucose', 'BloodPressure']]
# KMEANS 2
kmeans2 = KMeans(n_clusters=2)
kmeans2.fit(data2)
labels2 = kmeans2.predict(data2)

# visualization
plt.scatter(data['Glucose'], data['BloodPressure'], c = labels2)
plt.xlabel('Glucose')
plt.ylabel('BloodPressure')
plt.show()


# Now we try 2 different clustering. We will continue with data 2. Let's make cross table.

# In[ ]:


df = pd.DataFrame({'labels':labels2, 'Outcome':data['Outcome']})
crosstab = pd.crosstab(df['labels'],df['Outcome'])
crosstab


# This table shows us:
# * In Label 0 class We have 387 patients without diabetes and 103 patients with diabetes.
# * In Label 1 class We have 113 patients without diabetes and 165 patients with diabetes.

# Now We need to find optimum K value for better result.

# In[ ]:


iner_list = np.empty(10)
for i in range(1,10):
    kmeans2 = KMeans(n_clusters=i)
    kmeans2.fit(data2)
    iner_list[i] = kmeans2.inertia_

# iner_list = iner_list%100
# show the best number in graph
plt.plot(range(0,10), iner_list,'-')
plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")
plt.show()


# As a result of this chart, we can choose the K value of 4.

# <a id = "3"> </a><br>
# ## Standarization

# In[ ]:


data3 = data.drop('Outcome', axis = 1)
data3


# In[ ]:


from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

sscaler = StandardScaler()
kmeans2 = KMeans(n_clusters=4)
pipeline = make_pipeline(sscaler, kmeans2)
pipeline.fit(data3)

# cross table
labels = pipeline.predict(data3)
df = pd.DataFrame({'labels':labels, 'Outcome':data['Outcome']})
crosstab = pd.crosstab(df['labels'], df['Outcome'])
crosstab


# <a id = "4"> </a><br>
# ## Hierarchy

# In[ ]:


from scipy.cluster.hierarchy import linkage, dendrogram

merg = linkage(data3.iloc[200:220,:],method = 'single')
dendrogram(merg, leaf_rotation = 90, leaf_font_size = 6)
plt.show()


# <a id = "5"> </a><br>
# # Hierarchical Clustering

# In[ ]:


from sklearn.cluster import AgglomerativeClustering

hc = AgglomerativeClustering(n_clusters=2, affinity="euclidean",linkage="ward")
cluster = hc.fit_predict(data3)
data3['Label'] = cluster
data3


# In[ ]:


plt.scatter(data3['Glucose'], data3['BloodPressure'], c = cluster)
plt.xlabel('Glucose')
plt.ylabel('BloodPressure')
plt.show()


# In[ ]:


plt.scatter(data['Glucose'], data['BloodPressure'], c = data['Outcome'])
plt.xlabel('Glucose')
plt.ylabel('BloodPressure')
plt.show()


# In[ ]:


data3['Outcome'] = data['Outcome']
data3


# In[ ]:


# We compare our labels results with base data's result.
correct = []
for i in range(0,767):
    if data3['Label'][i] == data3['Outcome'][i]:
        correct.append(1)
    else:
        correct.append(0)
correct[0:10] # -> if we find correctly 1, if not 0


# In[ ]:


print("Hierarchical Clustering Accuracy : ", (correct.count(1)/data3['Label'].size)*100)


# In[ ]:




