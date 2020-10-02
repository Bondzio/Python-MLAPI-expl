#!/usr/bin/env python
# coding: utf-8

# # Unsupervised Clustering-Kmeans Analysis

# ### Importing libraries

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score,silhouette_samples
from sklearn.decomposition import PCA
import matplotlib.cm as cm
get_ipython().run_line_magic('matplotlib', 'inline')


# ### Reading data from csv

# In[ ]:


df=pd.read_csv('../input/mushrooms.csv')


# ### Exploratory Data Analysis:

# In[ ]:


df.head()


# ### Function to map categorical features to integral values

# In[ ]:


def Encoder(val):
    if val in category:
        return category[val]
    else:
        category[val]=len(category)
    return category[val]


# In[ ]:


df.info()


# ### no missing values

# In[ ]:


df.shape


# #### Encoder at work

# In[ ]:


for i in range(df.shape[1]):
    category={}
    df.iloc[:,i]=df.iloc[:,i].apply(Encoder)


# In[ ]:


df.head()


# ### Now since we are doing unsupervised clustering analysis here thus, dropping class column

# In[ ]:


X=df.drop('class',axis=1)


# In[ ]:


X.head()


# #### Converting all the features and extracting just 2 principle components for scatter plot analysis

# In[ ]:


pca = PCA(n_components=2).fit(X)


# In[ ]:


pca_2d = pca.transform(X)


# ## Trying different values of K and plotting Total within-cluster sum of squares and Average silhouette score for each value of K
# ### To find appropriate value of K

# In[ ]:


twss=[]
sa=[]


# In[ ]:


for i in range(1,10):
    kmeans = KMeans(n_clusters=i, init= 'k-means++')
    kmeans.fit(X)
    Ypreds=kmeans.predict(X)
    twss.append(kmeans.inertia_)
    if i>1:
        sa.append(silhouette_score(X, Ypreds))


# In[ ]:


plt.plot(range(1,10),twss)
plt.title('The Elbow Method')
plt.xlabel('Number of Clusters')
plt.ylabel('Total within-cluster sum of squares')


# In[ ]:


plt.plot(range(2,10),sa)
plt.title('silhouette analysis')
plt.xlabel('Number of Clusters')
plt.ylabel('Average silhouette score')


# ### *Above observations suggest k=3 but since we already know that there are only two clusters here edible and poisonous mushrooms then why the above results say otherwise?*

# ## By plotting silhouettes this problem can be solved : 
# ### Because we don't choose the k with just the highest silhouette score , silhouette samples should be uniform as well 

# In[ ]:


for n_clusters in range(2,7):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(18,7)

    ax1.set_xlim([-0.1, 1])
    ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])
    clusterer = KMeans(n_clusters=n_clusters, random_state=10)
    cluster_labels = clusterer.fit_predict(X)
    silhouette_avg = silhouette_score(X, cluster_labels)
    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)
    sample_silhouette_values = silhouette_samples(X, cluster_labels)
    y_lower = 10
    for i in range(n_clusters):
        ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
        y_lower = y_upper + 10
    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")
    ax1.set_yticks([])
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    
    colors = cm.spectral(cluster_labels.astype(float) / n_clusters)
    ax2.scatter(pca_2d[:, 0], pca_2d[:, 1], marker='.', s=30, lw=0, alpha=0.7, c=colors, edgecolor='k')
    centers = clusterer.cluster_centers_
    ax2.scatter(centers[:, 0], centers[:, 1], marker='o',c="white", alpha=1, s=200, edgecolor='k')
    for i, c in enumerate(centers):
        ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1,
                    s=50, edgecolor='k')

    ax2.set_title("Clusters")
    ax2.set_xlabel("feature 1 by pca")
    ax2.set_ylabel("feature 2 by pca")

    plt.suptitle(("Silhouette analysis for KMeans clustering "
                  "with n_clusters = %d" % n_clusters),
                 fontsize=14, fontweight='bold')

    plt.show()


# # As we can see although k=2 has the second highest avg silhouette score but it's samples are more uniform and thus, the appropriate value for k should indeed be 2 (edible , posionous)

# In[ ]:


kmeans = KMeans(n_clusters=2, init= 'k-means++')


# In[ ]:


kmeans.fit(X)


# In[ ]:


Ypreds=kmeans.predict(X)


# In[ ]:


plt.scatter(pca_2d[Ypreds == 0, 0], pca_2d[Ypreds == 0, 1], s = 100, c = 'red', label = 'edible')
plt.scatter(pca_2d[Ypreds == 1, 0], pca_2d[Ypreds == 1, 1], s = 100, c = 'blue', label = 'poisonous')
plt.legend()

