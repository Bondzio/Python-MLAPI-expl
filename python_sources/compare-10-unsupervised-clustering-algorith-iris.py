#!/usr/bin/env python
# coding: utf-8

# # Compare various clustering algorithms on the iris dataset
# 
# * **k-Means and Mini Batch k-Means**
# accuracy: 0.89 ... 
# silhouette:  0.696
# 
# * **DBSCAN and Optics**
# accuracy: with 3 clusters there are 114 outliers with DBSCAN and similar w OPTICS (?!)
# 
# * **Affinity Propagation**
# accuracy: 0.90 ... 
# silhouette:  0.696
# 
# * **Mean Shift**
# accuracy: 0.79 ... 
# silhouette:  0.635
# 
# * **Spectral Clustering**
# accuracy: 0.84 ... 
# silhouette:  0.661
# 
# * **Agglomerative Clustering**
# accuracy: 0.89 ... 
# silhouette:  0.688
# 
# * **Gaussian Mixture Clustering**
# accuracy: 0.97 ... 
# silhouette:  0.606
# 
# * **Birch**
# finds only 2 clusters
# 
# 
# * Based on https://scikit-learn.org/stable/modules/clustering.html
# 

# In[ ]:


import numpy as np  
import pandas as pd 
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans, DBSCAN, AffinityPropagation, MeanShift, estimate_bandwidth, SpectralClustering
from sklearn.cluster import AgglomerativeClustering, OPTICS, cluster_optics_dbscan, Birch, MiniBatchKMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn import metrics
from sklearn.mixture import GaussianMixture

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


# Read dataset

df = pd.read_csv("../input/iris-flower-dataset/IRIS.csv")
df.shape


# In[ ]:


df.sample(5)


# In[ ]:


df.groupby('species').size().plot.bar()
plt.show()


# In[ ]:


X = df.copy()
X = X.drop('species', axis=1)
X.describe()


# In[ ]:


# Normalize X

mms = MinMaxScaler()
mms.fit(X)
Xnorm = mms.transform(X)
Xnorm.shape


# # ELBOW method for finding the optimal # of clusters k

# In[ ]:


# Not knowing the number of clusters (3) we try a range such 1,10
# For the ELBOW method check with and without init='k-means++'

Sum_of_squared_distances = []
for k in range(1,10):
    km = KMeans(n_clusters=k, init='k-means++')
    km = km.fit(Xnorm)
    Sum_of_squared_distances.append(km.inertia_)


# In[ ]:


plt.plot(range(1,10), Sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k')
plt.show()


# In[ ]:


# Knowing from the ELBOW method that k=3 ...

kmeans3 = KMeans(n_clusters=3, init='k-means++').fit(Xnorm) 

KM_clustered = Xnorm.copy()
KM_clustered = pd.DataFrame(KM_clustered)
KM_clustered.loc[:,'Cluster'] = kmeans3.labels_ # append labels to points

frames = [df['species'], KM_clustered['Cluster']]
result = pd.concat(frames, axis = 1)
print(result.shape)
result.sample(5)


# # Assigning a label to each cluster
# * As there's no relation between a cluster number and the true label we need to map a cluster to the one label which appears most in that cluster
# 
# * These corrected predicted labels are needed below to calculate model performance vs the the true labels

# In[ ]:


for ClusterNum in range(3):

    OneCluster = pd.DataFrame(result[result['Cluster'] == ClusterNum].groupby('species').size())
    OneCluster.columns=['Size']
    
    NewDigit = OneCluster.index[OneCluster['Size'] == OneCluster['Size'].max()].tolist()
    NewDigit[0]

    rowIndex = result.index[result['Cluster'] == ClusterNum]
    result.loc[rowIndex, 'TransLabel'] = NewDigit[0]
    
    print(ClusterNum, NewDigit[0])


# In[ ]:


# Check performance of classification to 3 clusters

print('K-Means performance')
print('-'*60)

Correct = (df['species'] == result['TransLabel']).sum()
Accuracy = round(Correct/df.shape[0],3)
print('Accuracy ', Accuracy)

# METRICS for clustering algorithms

print('silhouette: ', round(metrics.silhouette_score(Xnorm, result['TransLabel'],metric='sqeuclidean'),3))
print('homogeneity_score: ', round(metrics.homogeneity_score(df['species'], result['TransLabel']),3))
print('completeness_score: ', round(metrics.completeness_score(df['species'], result['TransLabel']),3))
print('v_measure_score: ', round(metrics.v_measure_score(df['species'], result['TransLabel']),3))
print('adjusted_rand_score: ', round(metrics.adjusted_rand_score(df['species'], result['TransLabel']),3))
print('adjusted_mutual_info_score: ', round(metrics.adjusted_mutual_info_score(df['species'], result['TransLabel']),3))


# # DBSCAN

# In[ ]:


# Compute DBSCAN
# played with eps and min samples ... till I got num clustrers = 3 and lowest number of noise (114 ?!?)

db = DBSCAN(eps=0.078).fit(Xnorm)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)

print('Estimated number of clusters: %d' % n_clusters_)
print('Estimated number of noise points: %d' % n_noise_)


# # Affinity Propagation

# In[ ]:


af = AffinityPropagation(preference=-3).fit(Xnorm)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

n_clusters_ = len(cluster_centers_indices)

print('Estimated number of clusters: %d' % n_clusters_)

Clustered = Xnorm.copy()
Clustered = pd.DataFrame(Clustered)
Clustered.loc[:,'Cluster'] = af.labels_ # append labels to points
frames = [df['species'], Clustered['Cluster']]
result = pd.concat(frames, axis = 1)
for ClusterNum in range(3):

    OneCluster = pd.DataFrame(result[result['Cluster'] == ClusterNum].groupby('species').size())
    OneCluster.columns=['Size']
    
    NewDigit = OneCluster.index[OneCluster['Size'] == OneCluster['Size'].max()].tolist()
    NewDigit[0]

    rowIndex = result.index[result['Cluster'] == ClusterNum]
    result.loc[rowIndex, 'TransLabel'] = NewDigit[0]
    
    print(ClusterNum, NewDigit[0])


# In[ ]:


# Check performance of classification to 3 clusters

print('Affinity propagation performance')
print('-'*60)

Correct = (df['species'] == result['TransLabel']).sum()
Accuracy = round(Correct/df.shape[0],3)
print('Accuracy ', Accuracy)

# METRICS for clustering algorithms

print('silhouette: ', round(metrics.silhouette_score(Xnorm, result['TransLabel'],metric='sqeuclidean'),3))
print('homogeneity_score: ', round(metrics.homogeneity_score(df['species'], result['TransLabel']),3))
print('completeness_score: ', round(metrics.completeness_score(df['species'], result['TransLabel']),3))
print('v_measure_score: ', round(metrics.v_measure_score(df['species'], result['TransLabel']),3))
print('adjusted_rand_score: ', round(metrics.adjusted_rand_score(df['species'], result['TransLabel']),3))
print('adjusted_mutual_info_score: ', round(metrics.adjusted_mutual_info_score(df['species'], result['TransLabel']),3))


# # Mean Shift

# In[ ]:


# Compute clustering with MeanShift

# The following bandwidth can be automatically detected using
bandwidth = estimate_bandwidth(Xnorm, quantile=0.2) # Manually set the quantile to get num clusters = 3

ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(Xnorm)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)
print("number of estimated clusters : %d" % n_clusters_)

Clustered = Xnorm.copy()
Clustered = pd.DataFrame(Clustered)
Clustered.loc[:,'Cluster'] = ms.labels_ # append labels to points
frames = [df['species'], Clustered['Cluster']]
result = pd.concat(frames, axis = 1)


# In[ ]:


for ClusterNum in range(3):

    OneCluster = pd.DataFrame(result[result['Cluster'] == ClusterNum].groupby('species').size())
    OneCluster.columns=['Size']
    
    NewDigit = OneCluster.index[OneCluster['Size'] == OneCluster['Size'].max()].tolist()
    NewDigit[0]

    rowIndex = result.index[result['Cluster'] == ClusterNum]
    result.loc[rowIndex, 'TransLabel'] = NewDigit[0]
    
    print(ClusterNum, NewDigit[0])


# In[ ]:


# Check performance of classification to 3 clusters

print('Mean shift performance')
print('-'*60)

Correct = (df['species'] == result['TransLabel']).sum()
Accuracy = round(Correct/df.shape[0],3)
print('Accuracy ', Accuracy)

# METRICS for clustering algorithms

print('silhouette: ', round(metrics.silhouette_score(Xnorm, result['TransLabel'],metric='sqeuclidean'),3))
print('homogeneity_score: ', round(metrics.homogeneity_score(df['species'], result['TransLabel']),3))
print('completeness_score: ', round(metrics.completeness_score(df['species'], result['TransLabel']),3))
print('v_measure_score: ', round(metrics.v_measure_score(df['species'], result['TransLabel']),3))
print('adjusted_rand_score: ', round(metrics.adjusted_rand_score(df['species'], result['TransLabel']),3))
print('adjusted_mutual_info_score: ', round(metrics.adjusted_mutual_info_score(df['species'], result['TransLabel']),3))


# # Spectral Clustering

# In[ ]:


# Compute clustering with SpectralClustering

sc = SpectralClustering(n_clusters = 3)
sc.fit(Xnorm)
labels = ms.labels_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)
print("number of estimated clusters : %d" % n_clusters_)

Clustered = Xnorm.copy()
Clustered = pd.DataFrame(Clustered)
Clustered.loc[:,'Cluster'] = sc.labels_ # append labels to points
#Clustered.sample(5)

frames = [df['species'], Clustered['Cluster']]
result = pd.concat(frames, axis = 1)
#print(result.shape)
#result.sample(5)
for ClusterNum in range(3):

    OneCluster = pd.DataFrame(result[result['Cluster'] == ClusterNum].groupby('species').size())
    OneCluster.columns=['Size']
    
    NewDigit = OneCluster.index[OneCluster['Size'] == OneCluster['Size'].max()].tolist()
    NewDigit[0]

    rowIndex = result.index[result['Cluster'] == ClusterNum]
    result.loc[rowIndex, 'TransLabel'] = NewDigit[0]
    
    print(ClusterNum, NewDigit[0])


# In[ ]:


# Check performance of classification to 3 clusters

print('Spectral clustering performance')
print('-'*60)

Correct = (df['species'] == result['TransLabel']).sum()
Accuracy = round(Correct/df.shape[0],3)
print('Accuracy ', Accuracy)

# METRICS for clustering algorithms

print('silhouette: ', round(metrics.silhouette_score(Xnorm, result['TransLabel'],metric='sqeuclidean'),3))
print('homogeneity_score: ', round(metrics.homogeneity_score(df['species'], result['TransLabel']),3))
print('completeness_score: ', round(metrics.completeness_score(df['species'], result['TransLabel']),3))
print('v_measure_score: ', round(metrics.v_measure_score(df['species'], result['TransLabel']),3))
print('adjusted_rand_score: ', round(metrics.adjusted_rand_score(df['species'], result['TransLabel']),3))
print('adjusted_mutual_info_score: ', round(metrics.adjusted_mutual_info_score(df['species'], result['TransLabel']),3))


# In[ ]:


# Agglomerative Clustering

sc = AgglomerativeClustering(n_clusters = 3)
sc.fit(Xnorm)
labels = sc.labels_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)
print("number of estimated clusters : %d" % n_clusters_)

Clustered = Xnorm.copy()
Clustered = pd.DataFrame(Clustered)
Clustered.loc[:,'Cluster'] = sc.labels_ # append labels to points
#Clustered.sample(5)

frames = [df['species'], Clustered['Cluster']]
result = pd.concat(frames, axis = 1)
#print(result.shape)
#result.sample(5)
for ClusterNum in range(3):

    OneCluster = pd.DataFrame(result[result['Cluster'] == ClusterNum].groupby('species').size())
    OneCluster.columns=['Size']
    
    NewDigit = OneCluster.index[OneCluster['Size'] == OneCluster['Size'].max()].tolist()
    NewDigit[0]

    rowIndex = result.index[result['Cluster'] == ClusterNum]
    result.loc[rowIndex, 'TransLabel'] = NewDigit[0]
    
    print(ClusterNum, NewDigit[0])


# In[ ]:


# Check performance of classification to 3 clusters

print('Agglomerative clustering performance')
print('-'*60)

Correct = (df['species'] == result['TransLabel']).sum()
Accuracy = round(Correct/df.shape[0],3)
print('Accuracy ', Accuracy)

# METRICS for clustering algorithms

print('silhouette: ', round(metrics.silhouette_score(Xnorm, result['TransLabel'],metric='sqeuclidean'),3))
print('homogeneity_score: ', round(metrics.homogeneity_score(df['species'], result['TransLabel']),3))
print('completeness_score: ', round(metrics.completeness_score(df['species'], result['TransLabel']),3))
print('v_measure_score: ', round(metrics.v_measure_score(df['species'], result['TransLabel']),3))
print('adjusted_rand_score: ', round(metrics.adjusted_rand_score(df['species'], result['TransLabel']),3))
print('adjusted_mutual_info_score: ', round(metrics.adjusted_mutual_info_score(df['species'], result['TransLabel']),3))


# # Gaussian mixture
# 
# * Tried w covariance_type='tied' acc = 0.9, 'full' DEFAULT acc = 0.97,  'diag' acc = 0.93,  'spherical' acc = 0.89

# In[ ]:


# Gaussian Mixture clustering

sc = GaussianMixture(n_components=3, covariance_type='full')
y_pred = sc.fit_predict(Xnorm)
print("number of estimated clusters : %d" % len(set(y_pred)))

Clustered = Xnorm.copy()
Clustered = pd.DataFrame(Clustered)
Clustered.loc[:,'Cluster'] = y_pred # append labels to points
#Clustered.sample(5)

frames = [df['species'], Clustered['Cluster']]
result = pd.concat(frames, axis = 1)
#print(result.shape)
#result.sample(5)
for ClusterNum in range(3):

    OneCluster = pd.DataFrame(result[result['Cluster'] == ClusterNum].groupby('species').size())
    OneCluster.columns=['Size']
    
    NewDigit = OneCluster.index[OneCluster['Size'] == OneCluster['Size'].max()].tolist()
    NewDigit[0]

    rowIndex = result.index[result['Cluster'] == ClusterNum]
    result.loc[rowIndex, 'TransLabel'] = NewDigit[0]
    
    print(ClusterNum, NewDigit[0])


# In[ ]:


# Check performance of classification to 3 clusters

print('Gaussian mixture clustering performance')
print('-'*60)

Correct = (df['species'] == result['TransLabel']).sum()
Accuracy = round(Correct/df.shape[0],3)
print('Accuracy ', Accuracy)

# METRICS for clustering algorithms

print('silhouette: ', round(metrics.silhouette_score(Xnorm, result['TransLabel'],metric='sqeuclidean'),3))
print('homogeneity_score: ', round(metrics.homogeneity_score(df['species'], result['TransLabel']),3))
print('completeness_score: ', round(metrics.completeness_score(df['species'], result['TransLabel']),3))
print('v_measure_score: ', round(metrics.v_measure_score(df['species'], result['TransLabel']),3))
print('adjusted_rand_score: ', round(metrics.adjusted_rand_score(df['species'], result['TransLabel']),3))
print('adjusted_mutual_info_score: ', round(metrics.adjusted_mutual_info_score(df['species'], result['TransLabel']),3))


# # Birch

# In[ ]:


sc = Birch(n_clusters = 3)
sc.fit(Xnorm)
labels = sc.labels_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)
print("number of estimated clusters : %d" % n_clusters_)


# # Mini Batch K-Means

# In[ ]:



# Mini Batch K-Means Clustering

sc = MiniBatchKMeans(n_clusters = 3)
sc.fit(Xnorm)
labels = sc.labels_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)
print("number of estimated clusters : %d" % n_clusters_)

Clustered = Xnorm.copy()
Clustered = pd.DataFrame(Clustered)
Clustered.loc[:,'Cluster'] = sc.labels_ # append labels to points
#Clustered.sample(5)

frames = [df['species'], Clustered['Cluster']]
result = pd.concat(frames, axis = 1)
#print(result.shape)
#result.sample(5)
for ClusterNum in range(3):

    OneCluster = pd.DataFrame(result[result['Cluster'] == ClusterNum].groupby('species').size())
    OneCluster.columns=['Size']
    
    NewDigit = OneCluster.index[OneCluster['Size'] == OneCluster['Size'].max()].tolist()
    NewDigit[0]

    rowIndex = result.index[result['Cluster'] == ClusterNum]
    result.loc[rowIndex, 'TransLabel'] = NewDigit[0]
    
    print(ClusterNum, NewDigit[0])


# In[ ]:


# Check performance of classification to 3 clusters

print('Mini Batch K-Means clustering performance')
print('-'*60)

Correct = (df['species'] == result['TransLabel']).sum()
Accuracy = round(Correct/df.shape[0],3)
print('Accuracy ', Accuracy)

# METRICS for clustering algorithms

print('silhouette: ', round(metrics.silhouette_score(Xnorm, result['TransLabel'],metric='sqeuclidean'),3))
print('homogeneity_score: ', round(metrics.homogeneity_score(df['species'], result['TransLabel']),3))
print('completeness_score: ', round(metrics.completeness_score(df['species'], result['TransLabel']),3))
print('v_measure_score: ', round(metrics.v_measure_score(df['species'], result['TransLabel']),3))
print('adjusted_rand_score: ', round(metrics.adjusted_rand_score(df['species'], result['TransLabel']),3))
print('adjusted_mutual_info_score: ', round(metrics.adjusted_mutual_info_score(df['species'], result['TransLabel']),3))

