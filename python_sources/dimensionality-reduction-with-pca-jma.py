#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import seaborn as sns
sns.set()


# In[ ]:


rnd_num = np.random.RandomState(42)
X = np.dot(rnd_num.rand(2,2), rnd_num.randn(2, 500)).T


# In[ ]:


X


# In[ ]:


X[:, 0] = - X[:, 0]


# In[ ]:


from sklearn.decomposition import PCA


# In[ ]:


pca = PCA(n_components=2)
pca.fit(X)


# In[ ]:


print(pca.components_)


# In[ ]:


print(pca.explained_variance_)


# In[ ]:


print(pca.explained_variance_ratio_)


# In[ ]:


plt.scatter(X[:, 0], X[:, 1], alpha=0.3)


# plot data

for k, v in zip(pca.explained_variance_, pca.components_):
    vec = v * 3 * np.sqrt(k)
    
    ax = plt.gca()
    arrowprops=dict(arrowstyle='<-',
                    linewidth=4,
                    shrinkA=0, shrinkB=0)
    ax.annotate('', pca.mean_, pca.mean_ + vec, arrowprops=arrowprops)
    ax.text(-0.90, 1.2,'PC1', ha='center', va='center', rotation=-42, size=12)
    ax.text(-0.1,-0.6,'PC2', ha='center', va='center', rotation=50, size=12)
plt.axis('equal');


# In[ ]:


pca = PCA(n_components=1)
pca.fit(X)
X_pca = pca.transform(X)


# In[ ]:


X.shape


# In[ ]:


X_pca.shape


# In[ ]:


X_new = pca.inverse_transform(X_pca)
plt.scatter(X[:, 0], X[:, 1], alpha=0.2);
plt.scatter(X_new[:, 0], X_new[:, 1], alpha=0.8)
plt.axis('equal');

