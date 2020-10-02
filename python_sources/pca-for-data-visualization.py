#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"


# In[ ]:


# loading dataset into Pandas DataFrame
df = pd.read_csv(url, names=['sepal length','sepal width','petal length','petal width','target'])


# In[ ]:


df.head()


# In[ ]:


# Standardising the data
features = ['sepal length', 'sepal width', 'petal length', 'petal width']
x = df.loc[:, features].values


# In[ ]:


y = df.loc[:,['target']].values


# In[ ]:


x = StandardScaler().fit_transform(x)


# In[ ]:


pd.DataFrame(data = x, columns = features).head()


# In[ ]:


# PCA projection to 2 components
pca = PCA(n_components=2)


# In[ ]:


principalComponents = pca.fit_transform(x)


# In[ ]:


principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])


# In[ ]:


principalDf.head(5)


# In[ ]:


df[['target']].head()


# In[ ]:


finalDf = pd.concat([principalDf, df[['target']]], axis = 1)
finalDf.head(5)


# In[ ]:


# 2D Visualization
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 Component PCA', fontsize = 20)


targets = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
colors = ['r', 'g', 'b']
for target, color in zip(targets,colors):
    indicesToKeep = finalDf['target'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()


# In[ ]:


# How much information (variance) in each PC
pca.explained_variance_ratio_


# In[ ]:




