#!/usr/bin/env python
# coding: utf-8

# Hello, here is a basic example of a kmeans algorithm using the elbow technique to find the value of k. 
# A certain number of values will be randomly generated and the algorithm will be used to find the most 
# efficients way to regroup them.

# <h3>IMPORT</h3>

# In[ ]:


import numpy as np
import pandas as pd
import math
from matplotlib import pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler


# <h3>creation of random coordinates to add data to our dataframe</h3>

# In[ ]:


random_int = np.random.randint(1,200)
max_samples = 300
rand_center = np.random.randint(1,30)
rand_box = np.random.randint(8,20)

X, y = make_blobs(n_samples=max_samples, 
                  centers=rand_center, 
                  cluster_std=1,
                  center_box=(-(rand_box),rand_box),
                  random_state=random_int)

plt.scatter(X[:,0], X[:,1])
print(X.shape)
print(y.shape)


# <h3>model training and data curve printing</h3>

# In[ ]:


wcss = []
max_iteration = 300
df = pd.DataFrame(X)
max_range = 15
K = range(1, max_range)

points = []
for i in K: 
    kmeans = KMeans(n_clusters=i, 
                    init='k-means++', 
                    max_iter=max_iteration,
                    n_init=10, 
                    random_state=random_int)
    kmeans.fit(df)
    wcss.append(kmeans.inertia_)
    point = {'x': i, 'y': kmeans.inertia_}
    points.append(point)
    
    
plt.plot(K, wcss,'bx-')
plt.title('TRAINING MODEL')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')

plt.show()


# <h3>Searching for the bend in the curve to evaluate the optimal number of points needed to cover each area equitably</h3>

# In[ ]:


plt.plot(K, wcss,'bx-')
first_to_last = [points[0],points[max_range-2]]
df_ftl = pd.DataFrame(first_to_last)
plt.plot([K[0],K[13]],[wcss[0],wcss[13]], 'ro-')
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')


# In[ ]:


#thank you https://www.youtube.com/watch?v=IEBsrUQ4eMc for the help
def calc_distance_from_line(x1,y1,a,b,c):
    distance = abs((a*x1+b*y1+c)) / (math.sqrt(a*a+b*b))
    return distance


# In[ ]:


a = wcss[0] - wcss[max_range-2]
b = K[max_range-2] - K[0]
c1 = K[0] * wcss[max_range-2]
c2 = K[max_range-2] * wcss[0]
c = c1-c2

a,b,c


# <h3>calculates the distance between each point on the curve and the line separating the first and the last point </h3>

# In[ ]:


distance_from_line = []
for k in range(max_range-1):
    distance_from_line.append(
        calc_distance_from_line(K[k],wcss[k],a,b,c))

plt.title('Elbow Method reverse curve')
plt.xlabel('Number of clusters')
plt.ylabel('Distance')
plt.plot(K,distance_from_line)


# <h3>Prints a graph of the distances between each point and the line and finds its vertex.</h3>

# In[ ]:


plt.plot(K,distance_from_line)

num_cluster = distance_from_line.index(max(distance_from_line))+1

plt.title('Elbow Method reverse curve')
plt.xlabel('Number of clusters')
plt.ylabel('Distance')
plt.plot([num_cluster,num_cluster],[distance_from_line[0],max(distance_from_line)], 'ro-')


# <h3>uses pattern prediction to separate the group by that number of points and assigns a different color for each subgroup</h3>

# In[ ]:


num_cluster = distance_from_line.index(max(distance_from_line))+1
max_iteration = 300
kmeans = KMeans(n_clusters=num_cluster, 
                init='k-means++',
                max_iter=max_iteration, 
                n_init=10, 
                random_state=random_int)

pred_y = kmeans.fit_predict(X)
categories = np.array([1,2,3,4])
plt.scatter(X[:,0], X[:,1], s=20, c=pred_y)
plt.scatter(kmeans.cluster_centers_[:, 0], 
            kmeans.cluster_centers_[:, 1], s=300, c='red')
plt.show()


# You can see the different groupings by color in the graphic. The k central points are represented by the red dots in the graphic.
