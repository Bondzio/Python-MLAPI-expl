#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

from warnings import filterwarnings
filterwarnings('ignore')
import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import scipy as sp
from sklearn.cluster import KMeans

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


# Assign sets important according to segmentations preparation. 
# Consuquently segmentation sets has to be controlled by experts


df = pd.read_csv("/kaggle/input/violent-crime-rates-by-us-state/US_violent_crime.csv").copy()
df.head()


# # Exploratory Data Analysis

# In[ ]:


# firstly lets do it index 'Unnamed: 0' value in observation units

df.index = df.iloc[:,0]
df.index


# In[ ]:


df.head()


# In[ ]:


# stil during 'Unnamed: 0' let's get out of the list

df = df.iloc[:,1:5]
df.head()


# In[ ]:


df.index.name = "Index"
df.head()


# In[ ]:


# Let's see if I have any missing observations

df.isnull().sum()


# In[ ]:


# here all of them have to be numerical values. Here we have made it this too

df.info()


# In[ ]:


df.describe().T


# In[ ]:


# here it is appropriate to visualize the data to try to understand it.
# For example, 3 Assault (Assault) histogram looks like 3 peaks or accumulation.

df.hist(figsize = (10,10));


# # K-MEANS Model and Visualizations

# In[ ]:


# The number of part sand (n_cluster) we need to determine per work can be the same as the number of variables we need to concentrate on.

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters = 4)
kmeans


# In[ ]:


# lets look model properties

#?kmeans


# In[ ]:


k_fit = kmeans.fit(df)


# In[ ]:


# Let's create the chunks of the model to be fit

k_fit.n_clusters


# In[ ]:


# create the centers of these sets

k_fit.cluster_centers_


# ## Visualizations

# In[ ]:


# If I want to visualize, now let's reduce the set numbers to 2
kmeans = KMeans(n_clusters = 2)
k_fit = kmeans.fit(df)              


# In[ ]:


sets = k_fit.labels_


# In[ ]:


# Let's visualize the data we reduced to 2 sets.

plt.scatter(df.iloc[:,0], df.iloc[:,1], c = sets, s = 50, cmap = "viridis")

centers = k_fit.cluster_centers_                                 # We want to create 2 centers and show them on the visual.

plt.scatter(centers[:,0], centers[:,1], c = "black", s = 200, alpha = 0.5);


# In[ ]:


# Let us import 3D visualization. Otherwise it is necessary to download

from mpl_toolkits.mplot3d import Axes3D


# Let's create our sets again, this time it will be 3 dimensional variable

kmeans = KMeans(n_clusters = 3)
k_fit = kmeans.fit(df)
sets = k_fit.labels_
centers = kmeans.cluster_centers_


# In[ ]:


plt.rcParams['figure.figsize'] = (16, 9)
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]);


# In[ ]:


# Let's look at the visualization of these sets and centers on the plot.

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2], c=sets)
ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2], 
           marker='*', 
           c='#050505', 
           s=1000);


# ## Sets and observation units

# In[ ]:


# To provide cluster numbers and information about which states (observations) these numbers belong to
# If we want, we can take the model with 2 variables or 3 variables above, let's take the 3 ones

kmeans = KMeans(n_clusters = 3)
k_fit = kmeans.fit(df)
sets = k_fit.labels_


# In[ ]:


# to see which set and index you have for the top 10 states

pd.DataFrame({"Provinces" : df.index, "Sets": sets})[0:15]


# In[ ]:


# to look at the set number that each belongs to

df["set_no"] = sets

df.head()


# In[ ]:


# eger kume no 0 dan basliyorsa biz 1 den baslamasini istiyorsak soyle yapabiliriz

df["set_no"] = df["set_no"] + 1

df.head()


# ## Determination of Optimum Set Number

# In[ ]:


# It is called one from 2 to 50. The number of sets should decrease, because we should approach zero, because we reduce the sands.
# When you have 10 thousand customers, you are not interested in 100 people. It is necessary to put the customers with high degrees or features into a segment(sets).
#!pip install yellowbrick
from yellowbrick.cluster import KElbowVisualizer
kmeans = KMeans()
visualizer = KElbowVisualizer(kmeans, k=(2,50))
visualizer.fit(df) 
visualizer.poof()  

# We understand the presentation from gorsel each point segment (set), ie, the set of elements with similar properties in it
# For example, when the customer enters our site, a presentation can be made about what the monthly income it brings to us.


# In[ ]:


# Let's take our model above again
# To provide cluster numbers and information about which states (observations) these numbers belong to
# If we want we can take the model with 2 variables or 3 variables above, let's take the 4 normal ones

kmeans = KMeans(n_clusters = 4)
k_fit = kmeans.fit(df)
sets = k_fit.labels_


# In[ ]:


# to see which set and index you have for the top 10 states

pd.DataFrame({"Provinces" : df.index, "Sets": sets})[0:10]


# # Hierarchical Clustering

# In[ ]:


df = pd.read_csv("/kaggle/input/violent-crime-rates-by-us-state/US_violent_crime.csv").copy()
df.index = df.iloc[:,0]
df = df.iloc[:,1:5]
#del df.index.name
df.index.name = "Index"
df.head()


# In[ ]:


from scipy.cluster.hierarchy import linkage

hc_complete = linkage(df, "complete")
hc_average = linkage(df, "average")
hc_single = linkage(df, "single")


# In[ ]:


# We can watch its features and see what it does

dir(hc_complete)


# In[ ]:


# We need to create Dendogram

from scipy.cluster.hierarchy import dendrogram

plt.figure(figsize=(15, 10))
plt.title('Hierarchical Clustering - Dendogram')
plt.xlabel('Indexs')
plt.ylabel('Distance')
dendrogram(
    hc_complete,
    leaf_font_size=10
);


# In[ ]:


# another form of representation and the number of elements below it

from scipy.cluster.hierarchy import dendrogram

plt.figure(figsize=(15, 10))
plt.title('Hierarchical Clustering - Dendogram')
plt.xlabel('Indexs')
plt.ylabel('Distance')
dendrogram(
    hc_complete,
    truncate_mode = "lastp",
    p = 4,
    show_contracted = True
);


# ## Optimum Set Number

# In[ ]:


from scipy.cluster.hierarchy import dendrogram

plt.figure(figsize=(15, 10))
plt.title('Hierarchical Clustering - Dendogram')
plt.xlabel('Indexs')
plt.ylabel('Distance')
den = dendrogram(
    hc_complete,
    leaf_font_size=10
);


# In[ ]:


#?den


# In[ ]:


#?dendrogram


# In[ ]:


# When we look at the dendogram, it will be logical to divide it into 4 large clusters. Then we say n_cluster = 4.

from sklearn.cluster import AgglomerativeClustering
cluster = AgglomerativeClustering(n_clusters = 4, 
                                  affinity = "euclidean", 
                                  linkage = "ward")

cluster.fit_predict(df)


# In[ ]:


# if we want to see which state is in which bank

pd.DataFrame({"Provinces" : df.index, "Sets": cluster.fit_predict(df)})[0:10]


# In[ ]:


df["set_no"] = cluster.fit_predict(df)
df.head()


# # Conclusion
# 
# 
# 
#     1. If this tutorial is not enough you can check also https://www.picostat.com/dataset/r-dataset-package-datasets-usarrests
# 
#     2. I used here K_Means and Hierarchical Clustering Model but you can try also PCA Model. Results of both models:
# 
#     3. After this tutorial, my aim is to prepare 'kernel' which is connected to Deep Learning 'not clear' data set.
#    
#  If you have any suggestions, please could you write for me? I wil be happy for comment and critics!
#  
#  
#  Thank you for your suggestion and votes ;)
# 
# 
