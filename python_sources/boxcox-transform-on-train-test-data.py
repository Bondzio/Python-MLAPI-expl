#!/usr/bin/env python
# coding: utf-8

# In [this notebook](https://www.kaggle.com/rtatman/data-cleaning-challenge-scale-and-normalize-data/) I talk about scaling and normalizing data. This minimal example shows how to use a Box Cox transformation to normalize both trianing and testing data. :)  

# In[6]:


# import modules
import numpy as np
from scipy import stats
from sklearn.model_selection import train_test_split

# plotting modules
import seaborn as sns
import matplotlib.pyplot as plt

# generate non-normal data
original_data = np.random.exponential(size = 1000)

# split into testing & training data
train,test = train_test_split(original_data, shuffle=False)

# transform training data & save lambda value
train_data,fitted_lambda = stats.boxcox(train)

# use lambda value to transform test data
test_data = stats.boxcox(test, fitted_lambda)

# (optional) plot train & test
fig, ax=plt.subplots(1,2)
sns.distplot(train_data, ax=ax[0])
sns.distplot(test_data, ax=ax[1])


# In[ ]:




