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


# **Importing all necessary libraries**
# 

# In[ ]:


import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import collections
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
from scipy import stats
from sklearn.preprocessing import StandardScaler
import seaborn as sns


# **Importing data**
# 

# In[ ]:


data= pd.read_csv("/kaggle/input/ccdata/CC GENERAL.csv")
print(data.shape)
data.head()


# **Customer ID is to be removed**
# (Customer ID is not required for clustering)

# In[ ]:


x=data.iloc[:,1:]
x.head()


# **Identifying Null Values**

# In[ ]:


missing = x.isnull().sum()
print(missing)


# **Handling missing values**

# In[ ]:


x['MINIMUM_PAYMENTS'].fillna((x['MINIMUM_PAYMENTS'].mean()), inplace=True)
x['CREDIT_LIMIT'].fillna((x['CREDIT_LIMIT'].mean()), inplace=True)
print(missing)


# **Dealing with outliers**

# In[ ]:


z_score = np.abs(stats.zscore(x))
print(z_score)


# **Data after removing outliers**

# In[ ]:


data_without_outlier = pd.DataFrame(x[(z_score < 3).all(axis=1)], columns = x.columns)


# **Shape of data without outliers**

# In[ ]:


data_without_outlier.shape


# Standardization for feature scaling
# 

# In[ ]:


scaler = StandardScaler()
X = scaler.fit_transform(data_without_outlier)


# **Applying principal component analysis (PCA) for dimensionality reduction **

# In[ ]:


pca = PCA(n_components = 2) 
X_principal = pca.fit_transform(X) 
X_principal = pd.DataFrame(X_principal) 
X_principal.columns = ['P1', 'P2'] 


# **Finding optimal number of clusters for K-MEANS**

# In[ ]:


#optimal no. of clusters
n_clusters=20
cost=[]
for i in range(1,n_clusters):
    kmean= KMeans(i)
    kmean.fit(X_principal)
    cost.append(kmean.inertia_)  
   
plt.plot(cost, 'bx-')


# **Comparing silhoutte scores for different no. of clusters **

# In[ ]:


silhouette_scores = [] 
for n_cluster in range(2, 8):
    silhouette_scores.append(   
        silhouette_score(X_principal, KMeans(n_clusters = n_cluster).fit_predict(X_principal))) 
    
k = [2, 3, 4, 5, 6,7] 
plt.bar(k, silhouette_scores) 
plt.xlabel('Number of clusters', fontsize = 10) 
plt.ylabel('Silhouette Score', fontsize = 10) 
plt.show()    


# **Applying K-Means with no. of clusters as 3 because it has maximum silhoutte score**

# In[ ]:


db_default = KMeans(n_clusters=3, init='k-means++').fit(X_principal) 
labels = db_default.labels_  


# **Visualization of clusters**

# In[ ]:


colours = {} 
colours[0] = 'r'
colours[1] = 'y'
colours[2] = 'g'
# Building the colour vector for each data point 
cvec = [colours[label] for label in labels] 
  
# For the construction of the legend of the plot 
#r = plt.scatter(X_principal['P1'], X_principal['P2'], color ='r'); 
#y = plt.scatter(X_principal['P1'], X_principal['P2'], color ='y'); 
#g = plt.scatter(X_principal['P1'], X_principal['P2'], color ='g');  
# Plotting P1 on the X-Axis and P2 on the Y-Axis  
# according to the colour vector defined 
plt.figure(figsize =(9, 9))  
plt.scatter(X_principal['P1'], X_principal['P2'], c = cvec) 
  
# Building the legend 
plt.legend((r, y, g), ('Label 0','Label 1','Label 2')) 
  
plt.show() 


# visualizing each feature in each cluster

# In[ ]:


clusters=pd.concat([x, pd.DataFrame({'cluster':labels})], axis=1)
clusters.head()

for cols in data_without_outlier:
    g = sns.FacetGrid(clusters, col = 'cluster')
    g.map(plt.hist, cols)


# **Cluster analysis**
# * Cluster 0 : Customers with more usage of credit card and makes more frequent purchases of product.
# * Cluster 1 : Customers with least usage of credit card.
# * Cluster 2 : Customers with moderate usage of credit card.
