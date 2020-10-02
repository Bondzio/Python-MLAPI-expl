#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# Principal Component Analysis (or PCA) uses linear algebra to transform the dataset into a compressed form.
# 
# Generally this is called a data reduction technique. A property of PCA is that you can choose the number of dimensions or principal component in the transformed result.
# 
# In the example below, we use PCA and select 2 principal components from 849 features

# **Importing Dataset Covid19 and price dataset**

# In[ ]:


df=pd.read_csv('../input/ntt-data-global-ai-challenge-06-2020/COVID-19_and_Price_dataset.csv')


# Shape of the Dataset consist of 125 rows and 849 columns

# In[ ]:


df.shape


# In[ ]:


df=df.drop(['Date'], axis=1)


# Importing Sklearn Library for standard scaler function

# In[ ]:


from sklearn.preprocessing import StandardScaler
scaler= StandardScaler()
scaler.fit(df)


# In[ ]:


Scaled_data= scaler.transform(df)


# Importing PCA from sklearn to reduce the dimension of the dataset and preserve the relevant features.

# In[ ]:


from sklearn.decomposition import PCA


# In[ ]:


pca=PCA(n_components=2)
pca.fit(Scaled_data)


# In[ ]:


x_pca=pca.transform(Scaled_data)


# After applying PCA techique Dimension of the dataset readuced to 2 from 849

# In[ ]:


Scaled_data.shape


# In[ ]:


x_pca.shape


# **Plotted the compressed data and found the some correlation in the dataset**

# In[ ]:


import matplotlib.pyplot as plt
plt.figure(figsize=(8,6))
plt.scatter(x_pca[:,0],x_pca[:,1])
plt.xlabel('first component')
plt.ylabel('second component')

