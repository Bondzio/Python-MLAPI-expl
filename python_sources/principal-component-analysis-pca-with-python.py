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


# **During EDA when we have large set of variables we often get confused and lost deciding which features to choose so that our model will be safe from overfitting. In such cases the Dimension Reduction comes into play.In these cases we can make use of a unsupervised Algorithm known as PCA.
# PCA is used to find inter-relation between variables in the data y reducing the dimensions of a feature in such a way that they are statistically independent & not correlated.**

# In this notebook we will use sklearn package for Principal Component Analysis 

# **DATA**

# Here, we are going to use a sample pre-processed wine data containing various numerical features of a wine.

# In[ ]:


import pandas as pd
import numpy as np
wine = pd.read_csv("../input/wine-data/wine_data.csv")
wine.head()


# In[ ]:


#Dropping Index
wine = wine.iloc[:,1:] 
wine.head()


# In[ ]:


#normalizing the values

from sklearn.preprocessing import scale 
wine_norm = scale(wine) 
wine_norm


# **Building the PCA model.**

# In[ ]:



from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

pca = PCA()
pca_values = pca.fit_transform(wine_norm)


# **Varience**

# In[ ]:


# The amount of variance that each PCA explains
var = pca.explained_variance_ratio_ 
plt.plot(var)
pd.DataFrame(var)


# Here, we can conclude that the out of the 14 principal components the first 4 PC contributes to the 69% of total varience.

# In[ ]:


# Cumulative variance 
var1 = np.cumsum(np.round(var,decimals = 4)*100) 
var1
# Variance plot for PCA components obtained 
plt.plot(var1,color="red")


# In[ ]:


#storing PCA values to a data frame
new_df = pd.DataFrame(pca_values[:,0:4])
new_df


# 
