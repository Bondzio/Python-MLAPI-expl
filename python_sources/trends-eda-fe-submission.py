#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd # package for high-performance, easy-to-use data structures and data analysis
import numpy as np # fundamental package for scientific computing with Python
import matplotlib
import matplotlib.pyplot as plt # for plotting
import seaborn as sns # for making plots with seaborn
color = sns.color_palette()
import plotly.offline as py
py.init_notebook_mode(connected=True)
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.offline as offline
offline.init_notebook_mode()
#import cufflinks and offline mode
import cufflinks as cf
cf.go_offline()

# Venn diagram
from matplotlib_venn import venn2
import re
import nltk
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
eng_stopwords = stopwords.words('english')
import gc

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


# In[ ]:


import os
bp = '/kaggle/input/trends-assessment-prediction'
print(os.listdir(bp))


# In[ ]:


print('Reading data...')
loading_data = pd.read_csv(bp+'/loading.csv')
train_data = pd.read_csv(bp+'/train_scores.csv')
sample_submission = pd.read_csv(bp+'/sample_submission.csv')
print('Reading data completed')


# In[ ]:


print('Size of loading_data', loading_data.shape)
print('Size of train_data', train_data.shape)
print('Size of sample_submission', sample_submission.shape)
print('test size:', len(sample_submission)/5)


# In[ ]:


display(loading_data.head())
display(loading_data.describe())


# In[ ]:


display(train_data.head())
display(train_data.describe())


# In[ ]:


sample_submission.head()


# In[ ]:


targets = list(train_data.columns[1:])
targets


# In[ ]:


# checking missing data
total = train_data.isnull().sum().sort_values(ascending = False)
percent = (train_data.isnull().sum()/train_data.isnull().count()*100).sort_values(ascending = False)
missing_train_data  = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_train_data.head()


# In[ ]:


# checking missing data
total = loading_data.isnull().sum().sort_values(ascending = False)
percent = (loading_data.isnull().sum()/loading_data.isnull().count()*100).sort_values(ascending = False)
missing_test_data  = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_test_data.head()


# In[ ]:


targets= loading_data.columns[1:]
fig, axes = plt.subplots(6, 5, figsize=(18, 15))
axes = axes.ravel()
bins = np.linspace(-0.05, 0.05, 20)

for i, col in enumerate(targets):
    ax = axes[i]
    sns.distplot(loading_data[col], label=col, kde=False, bins=bins, ax=ax)
    # ax.set_title(col)
#     ax.set_xlim([0, 1])
#     ax.set_ylim([0, 6079])
plt.tight_layout()
plt.show()
plt.close()


# In[ ]:


targets= train_data.columns[1:]
fig, axes = plt.subplots(1, 5, figsize=(18, 4))
axes = axes.ravel()
bins = np.linspace(0, 100, 20)

for i, col in enumerate(targets):
    ax = axes[i]
    sns.distplot(train_data[col], label=col, kde=False, bins=bins, ax=ax)
    # ax.set_title(col)
#     ax.set_xlim([0, 1])
#     ax.set_ylim([0, 6079])
plt.tight_layout()
plt.show()
plt.close()


# In[ ]:


fig, ax = plt.subplots(figsize=(8, 6))
cols = loading_data.columns[1:]
sns.heatmap(loading_data[cols].corr(), ax=ax)


# In[ ]:


fig, ax = plt.subplots(figsize=(8, 6))
cols = train_data.columns[1:]
sns.heatmap(train_data[cols].corr(), ax=ax)


# In[ ]:


merged = train_data.merge(loading_data)
# merged.describe()


# In[ ]:


from scipy.spatial.distance import cdist

def calc_corr(df, x_cols, y_cols):
    arr1 = df[x_cols].T.values
    arr2 = df[y_cols].T.values
    corr_df = pd.DataFrame(1 - cdist(arr2, arr1, metric='correlation'), index=y_cols, columns=x_cols)
    return corr_df

input_cols = merged.columns[6:]
output_cols = merged.columns[1:6]

corr_df = calc_corr(merged, input_cols, output_cols)
fig, ax = plt.subplots(figsize=(10, 2))
sns.heatmap(corr_df, ax=ax)


# In[ ]:


get_ipython().system('ls /kaggle/input')


# In[ ]:


sub = pd.read_csv('../input/trends-my-kernel-outputs/sub_2.5.csv')
sub.to_csv('sub.csv', index=False)


# In[ ]:




