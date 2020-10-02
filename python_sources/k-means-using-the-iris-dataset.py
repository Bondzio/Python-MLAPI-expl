#!/usr/bin/env python
# coding: utf-8

# # Implementing the K Means Algorithm using the Iris Dataset

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
from sklearn import datasets
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


#Loading the iris dataset
iris = datasets.load_iris()


# In[ ]:


#Checking the dataset
iris.data
print(iris.data.shape)


# In[ ]:


#Checking the featues
iris.feature_names


# In[ ]:


#Scaling the data for clustering for better efficiency
x = scale(iris.data)


# In[ ]:


#checking the target
iris.target


# In[ ]:


# Doing the clustering 
clustering = KMeans(n_clusters =3,random_state=1)


# In[ ]:


#Fitting the algorithm
clustering.fit(x)


# In[ ]:


#Labelling the cluster
clustering.labels_


# In[ ]:


#Adding the visualisation
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


#Converting into DataFrame
iris_df = pd.DataFrame(iris.data)


# In[ ]:


iris_df.columns=['sepal_length','sepal_width','petal_length','petal_width']


# In[ ]:


y=pd.DataFrame(iris.target)
y.columns=['targets']


# In[ ]:


y.head()


# In[ ]:


plt.scatter(x=iris_df.petal_length,y=iris_df.petal_width)
plt.title("The actual dataset")


# In[ ]:


import numpy as np
color =np.array(['red','blue','green'])


# In[ ]:


#adding the colors
plt.scatter(x=iris_df.petal_length,y=iris_df.petal_width,c=color[iris.target])
plt.title("The actual dataset")


# In[ ]:


#After the clustering
#adding the colors
color2=np.array(['green','red','blue'])
plt.scatter(x=iris_df.petal_length,y=iris_df.petal_width,c=color2[clustering.labels_])
plt.title("The dataset post clustering")


# # That's all for the first clustering algorithm.Hope you had fun :)

# In[ ]:




