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


# In[ ]:


import sklearn.datasets as dt


# In[ ]:


cars = pd.read_csv("../input/carsdata/cars.csv", na_values=' ')


# In[ ]:


cars.head()


# In[ ]:


cars=cars.dropna()
cars['cubicinches']= cars['cubicinches'].astype(int)


# In[ ]:


cars.columns = ['mpg', 'cylinders', 'cubicinches', 'hp', 'weightlbs', 'time-to-60',
       'year', 'brand']


# In[ ]:


cars.describe()


# In[ ]:


x = cars.iloc[:, :7]
x.head()


# In[ ]:


x_array = x.values
x_array


# In[ ]:


import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
wcss = []
for i in range(1,11):
    kmeans = KMeans(n_clusters=i,init='k-means++',max_iter=300,n_init=10,random_state=0)
    kmeans.fit(x_array)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,11),wcss)
plt.title('Metodo cotovelo - Elbow Method')
plt.xlabel('clusters')
plt.ylabel('')
plt.show()


# In[ ]:


kmeans = KMeans(n_clusters=4,init='k-means++',max_iter=300,n_init=10,random_state=0)
cars['clusters'] =kmeans.fit_predict(x_array)
cars.head()
cars.groupby("clusters").agg('mean').plot.bar(figsize=(10,7.5))
plt.title("Cluster")

