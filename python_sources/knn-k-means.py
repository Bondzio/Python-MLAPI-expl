#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# # K Means Clustering

#  Objective : Defining a custom function for k-means clustering (Euclidean distance)

# ### Importing Libraries

# In[ ]:


import numpy as np
import pandas as pd
from copy import deepcopy


# In[ ]:


# Euclidean Distance Caculator
def dist(a, b, axis=1):
    return np.linalg.norm(a - b, axis=axis)


# ### Custom Function for K-means Clustering

# In[ ]:


def kmeans_custom(Data,k) :
    # Select k random datapoints as centroids
    Centroids = np.array(pd.DataFrame(Data).sample(n=k))
    # To store the value of centroids when it updates
    Centroids_old = np.zeros(Centroids.shape)
    # Cluster lables to be appended (Initialize with zeros)
    clusters = np.zeros(len(Data))
    # Loss function - Distance between new centroids and old centroids
    loss = dist(Centroids, Centroids_old, None)
    # Looping through all the points till the loss becomes zero
    while loss != 0:
        
        for i in range(len(Data)):
            distances = dist(Data[i], Centroids)
            cluster = np.argmin(distances)
            clusters[i] = cluster
        # Storing the old centroid values
        Centroids_old = deepcopy(Centroids)
        # Finding the new centroids by taking the average value
        for i in range(k):
            points = [Data[j] for j in range(len(Data)) if clusters[j] == i]
            Centroids[i] = np.mean(points, axis=0)
        loss = dist(Centroids, Centroids_old, None)
    new_DataFrame = pd.DataFrame(Data)
    # Appending clusters column to the original dataframe
    new_DataFrame['Cluster']= clusters
    return new_DataFrame


# #### Testing with a simple dataset

# In[ ]:


data = pd.read_csv('../input/insurance.csv')
data.head()


# In[ ]:


new_data = data.iloc[:500,[0,2]]
new_data.head()


# #### Normalizing the dataset

# In[ ]:


from sklearn import preprocessing
new_data2 = preprocessing.normalize(new_data)
new_data3 = pd.DataFrame(new_data2)
new_data3.head()


# Passing it through the custom function

# In[ ]:


result = kmeans_custom(new_data2,4)
result.head()


# Plotting the clusters to validate

# In[ ]:


from matplotlib import pyplot as plt
plt.scatter(result[0],result[1], c=result['Cluster'])


# # KNN Regressor

#  Objective : Defining a simple custom function for k-nearest neighbors Regressor which takes a single test point and predicts its target
#  
#  -Euclidean distance
#  
#  -Simple mean of n nearest neighbor targets

# In[ ]:


new_data4 = data.iloc[:500,[0,2,6]]
new_data4.head()


# Train test Split

# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(new_data4.iloc[:,0:2], new_data4.iloc[:,2], test_size=0.2, random_state=42)
X_train.head()


# Scaling the numeric features

# In[ ]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


# ## Custom Function

# In[ ]:


def knn_regr_predictor(point,k):
    distance = []
    # Calculate distance from the test point to every point in train data
    distance.append(dist(X_train,point))
    # Select k nearest points
    d2 = np.argpartition(distance, k)
    d2 = d2.flatten()
    # calculate average of their targets
    return np.average([ y_train[i] for i in d2[:k] ])


# Prediction for a test point

# In[ ]:


knn_regr_predictor(X_test[1:2],10)


# Actual target

# In[ ]:


y_test[1:2]

