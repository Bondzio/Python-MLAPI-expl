#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# Import the data

# In[ ]:


data = pd.read_csv('../input/HR_comma_sep.csv')
data.head(10)


# In[ ]:


# convert label features to integers
data["salary_level"] = data["salary"].map({"low":1, "medium":2, "high":3})


# In[ ]:


data_scaled = data[['satisfaction_level','last_evaluation','number_project','average_montly_hours'
                    ,'salary_level','time_spend_company','Work_accident','promotion_last_5years']]
data_scaled.head()


# In[ ]:


from sklearn import preprocessing
data_scaled_2 = preprocessing.scale(data_scaled)


# In[ ]:


data_scaled_2_df = pd.DataFrame(data_scaled_2)
data_scaled_2_df.columns = data_scaled.columns
data_scaled_2_df.index = data_scaled.index
data_scaled_2_df.head()


# we should try and do some pca

# In[ ]:


from sklearn.decomposition import PCA


# In[ ]:


pca = PCA()
pca.fit(data_scaled_2_df)
all_pca = pca.transform(data_scaled_2_df)
print("shape:", all_pca.shape)


print(sum(pca.explained_variance_ratio_[0:8]))
print(sum(pca.explained_variance_ratio_[0:7]))
print(sum(pca.explained_variance_ratio_[0:6]))
print(sum(pca.explained_variance_ratio_[0:5]))
print(sum(pca.explained_variance_ratio_[0:4]))
print(sum(pca.explained_variance_ratio_[0:3]))
print(sum(pca.explained_variance_ratio_[0:2]))
print(sum(pca.explained_variance_ratio_[0:1]))


# In[ ]:


print(pca.components_)


# In[ ]:


pca = PCA(n_components=2)
pca.fit(data_scaled_2_df)
X_reduced = pca.transform(data_scaled_2_df)
print("Reduced dataset shape:", X_reduced.shape)

import pylab as pl
pl.scatter(X_reduced[:, 0], X_reduced[:, 1],
           cmap='RdYlBu')


# In[ ]:


from sklearn.cluster import KMeans
k_means = KMeans(n_clusters=5, random_state=0) # Fixing the RNG in kmeans
k_means.fit(data_scaled_2_df)
y_pred = k_means.predict(data_scaled_2_df)

pl.scatter(X_reduced[:, 0], X_reduced[:, 1], c=y_pred,
           cmap='RdYlBu');

