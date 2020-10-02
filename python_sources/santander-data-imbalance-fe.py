#!/usr/bin/env python
# coding: utf-8

# **I want to utilize what other guys did and implement some imbalance techniques.**
# 
# [Gabriel](https://www.kaggle.com/gpreda/santander-eda-and-prediction) added some nice statistical features.
# 
# [Andrew](https://www.kaggle.com/artgor/santander-eda-fe-fs-and-models/data) used ELI5 for feature importance and choosed top 100. His ***main trick*** is using NN (Nearest Neighbours) for feature engineering. Also he noted that feature scaling severely decreases score!!!
# 
# [Nanashi](https://www.kaggle.com/jesucristo/santander-magic-lgb-0-901) did some data augmenation - copying once negative, twice positive (t=2). He also has parameter, which gives number of positive copies and t//2 less negative once.
# 
# [OIe](https://www.kaggle.com/omgrodas/lightgbm-with-data-augmentation) did very simple data augmentation - just randomly coping positive targets 2 times...
# 
# In [this blog](https://www.analyticsvidhya.com/blog/2017/03/imbalanced-classification-problem/), a guy mentions K-Means clustering for data oversampling. I found [kmeans-smote](https://pypi.org/project/kmeans-smote/) library for that.
# 
# [Zichen's blog](https://towardsdatascience.com/practical-tips-for-class-imbalance-in-binary-classification-6ee29bcdb8a7) has some more details on handling imbalanced data. There is whole library for them - [imbalanced-learn](https://github.com/scikit-learn-contrib/imbalanced-learn). He also gives some up/down-sampling algorithm with RandomForest. Also he says that ROC is nor the best metrics in this case...
# 
# Additional good model beside Gboosts and NN is SVM. Also look what did TPOT and other AutoML found!

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

from sklearn.neighbors import NearestNeighbors
from numba import jit


# In[ ]:


# Read in features from GitHub
train_data = pd.read_csv('../input/train.csv')
test_data = pd.read_csv('../input/test.csv')
sample_submission = pd.read_csv('../input/sample_submission.csv')

print('Training data shape: ', train_data.shape)
print('Testing data shape:  ', test_data.shape)


# In[ ]:


train_data.describe()


# # 1 Feature Engineering
# ## Stat-features by [Gabriel](https://www.kaggle.com/gpreda/santander-eda-and-prediction)

# In[ ]:


get_ipython().run_cell_magic('time', '', "idx = features = train_data.columns.values[2:202]\nfor df in [test_data, train_data]:\n    df['sum'] = df[idx].sum(axis=1)  \n    df['min'] = df[idx].min(axis=1)\n    df['max'] = df[idx].max(axis=1)\n    df['mean'] = df[idx].mean(axis=1)\n    df['std'] = df[idx].std(axis=1)\n    df['skew'] = df[idx].skew(axis=1)\n    df['kurt'] = df[idx].kurtosis(axis=1)\n    df['med'] = df[idx].median(axis=1)")


# In[ ]:


train_data[train_data.columns[202:]].head()


# ## Nearest Neighbor by [Andrew](https://www.kaggle.com/artgor/santander-eda-fe-fs-and-models/data)

# In[ ]:


get_ipython().run_cell_magic('time', '', "X = train_data.drop(['ID_code', 'target'], axis=1)\nX_test = test_data.drop(['ID_code'], axis=1)\nneigh = NearestNeighbors(4, n_jobs=-1)\nneigh.fit(X)")


# In[ ]:


get_ipython().run_cell_magic('time', '', "\ndists, _ = neigh.kneighbors(X, n_neighbors=4)\nmean_dist = dists.mean(axis=1)\nmax_dist = dists.max(axis=1)\nmin_dist = dists.min(axis=1)\n\ntrain_data['mean_dist_4'] = mean_dist\ntrain_data['max_dist_4'] = max_dist\ntrain_data['min_dist_4'] = min_dist")


# In[ ]:


get_ipython().run_cell_magic('time', '', "\ntest_dists, _ = neigh.kneighbors(X_test, n_neighbors=3)\ntest_mean_dist = test_dists.mean(axis=1)\ntest_max_dist = test_dists.max(axis=1)\ntest_min_dist = test_dists.min(axis=1)\n\ntest_data['mean_dist_4'] = test_mean_dist\ntest_data['max_dist_4'] = test_max_dist\ntest_data['min_dist_4'] = test_min_dist")


# In[ ]:


train_data[train_data.columns[210:]].head()


# In[ ]:


train_data.to_csv('train_milos4.csv', index=False)
test_data.to_csv('test_milos4.csv', index=False)
sample_submission.to_csv('sample_submission.csv', index=False)


# In[ ]:


print('Training data shape: ', train_data.shape)
print('Testing data shape:  ', test_data.shape)

