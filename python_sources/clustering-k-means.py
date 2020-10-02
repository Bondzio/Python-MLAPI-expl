#!/usr/bin/env python
# coding: utf-8

#  # <span style="font-family: Arial; font-weight:bold;font-size:1.5em;color:#ba2323;"> Centroid Clustering: K-Means

# ![](https://cdn.pixabay.com/photo/2016/03/28/09/39/shelf-1285186_960_720.jpg)

# In[ ]:


import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pylab as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('ggplot')

import sklearn
from sklearn.model_selection  import train_test_split
from sklearn import cluster

from scipy.stats import zscore


# In[ ]:


import pandas as pd
data_df = pd.read_csv("../input/technical-customer-support-data/technical_support_data.csv")


# In[ ]:


data_df.head(10)


# In[ ]:


#eleiminate the catagorical feature
data_df=data_df.iloc[:,1:]
data_df


# In[ ]:


from scipy.spatial.distance import cdist


# In[ ]:


no_of_clusters = range(1,10)

meanDistortions = []

for k in no_of_clusters:
    clsfmodel = cluster.KMeans(n_clusters=k)
    clsfmodel.fit(data_df)
    predict = clsfmodel.predict(data_df)
    meanDistortions.append(sum(np.min(cdist(data_df,clsfmodel.cluster_centers_,'euclidean'),axis=1)) / data_df.shape[0])
    print(clsfmodel.labels_)
    
#print(meanDistortions)
    


# In[ ]:


plt.plot(no_of_clusters, meanDistortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Average distortion')
plt.title('Selecting k with the Elbow Method')


# In[ ]:


# Let us first start with K = 3
model_cluster = cluster.KMeans(3)
model_cluster.fit(data_df)
predict = model_cluster.predict(data_df)

#Append the prediction 
data_df["Group"] = predict
data_df.mean()


# In[ ]:


inertia = []

for n in range(1,10):
    model = cluster.KMeans(n_clusters=n,init='k-means++',n_init = 10, max_iter=300,tol=0.001,random_state=2,algorithm='elkan')
    model.fit(data_df)
    inertia .append(model.inertia_)


# In[ ]:


plt.figure(1,figsize=(8,5))
plt.plot(np.arange(1,10),inertia,'o')
plt.plot(np.arange(1,10),inertia,'-')
plt.xlabel('Number of Clusters') ,
plt.ylabel('Inertia')
plt.show()


# # <span style="font-family: Arial; font-weight:bold;font-size:1.5em;color:#8a3ebe;"> Silhouette coefficient: find optimal number

# ![process of extrapolating information](https://cdn.pixabay.com/photo/2016/09/11/08/33/man-1660853__340.jpg)

# In[ ]:


silhouette_score  = list()
no_of_cluster = range(2,20)

for i in no_of_cluster:
    model = cluster.KMeans(i,init='k-means++',n_init=10,max_iter=100,tol=0.0001, verbose=0, random_state=None, copy_x=True)
    model.fit(data_df)
    predict = model.predict(data_df)
    sklearn.metrics.silhouette_score(data_df,predict,metric='euclidean')
    silhouette_score.append(sklearn.metrics.silhouette_score(data_df,predict,metric='euclidean'))
    


# In[ ]:


plt.plot(no_of_cluster,silhouette_score)
plt.title("Silhouette score vs Numbers of Clusters ")
plt.xlabel('Number of Cluster')
plt.ylabel('Silhouette Score')
plt.show()


# In[ ]:


Optimal_Number=no_of_cluster[silhouette_score.index(max(silhouette_score))]
print( "Optimal number :")
print(Optimal_Number)


# In[ ]:




