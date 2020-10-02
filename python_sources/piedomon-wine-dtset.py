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


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn import datasets
import matplotlib.pyplot as plt
plt.style.use('ggplot')


# In[ ]:


df=pd.read_csv('../input/wine.csv')


# In[ ]:


df.head()


# In[ ]:


df.class_name.unique()


# In[ ]:


X= df.drop('class_name',axis=1).values
y= df.class_name.values
print(X.shape,y.shape)


# In[ ]:


from sklearn.cluster import KMeans

# Create a KMeans instance with 3 clusters: model
model = KMeans(n_clusters=3)

# Fit model to points
model.fit(X)

# Determine the cluster labels of new_points: labels
labels = model.predict(X)


# In[ ]:


df1=pd.DataFrame({'labels':labels,'varieties':y})


# In[ ]:


ct=pd.crosstab(df1['labels'],df1.varieties)
print(ct)


# Kmeans cluster dontrcorrespond well with the wine varieties
# Tis is because of higher variance difference bw the features

# In[ ]:


df.head()


# In[ ]:


df.describe()


# In[ ]:


from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
scaler= StandardScaler()
kmeans= KMeans(n_clusters=3)
pipeline= make_pipeline(scaler,kmeans)
pipeline.fit(X)
outcome= pipeline.predict(X)


# In[ ]:


df2=pd.DataFrame({'labels':outcome,'varieties':y})
ct=pd.crosstab(df2['labels'],df2.varieties)
print(ct)


# thus incorporating standardization gives better clustering with kmeans

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




