#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

get_ipython().run_line_magic('matplotlib', 'inline')


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


# In[ ]:


get_ipython().system('pip install git+https://github.com/fastai/fastai@2e1ccb58121dc648751e2109fc0fbf6925aa8887')

get_ipython().system('apt update && apt install -y libsm6 libxext6')


# In[ ]:


from fastai.imports import *
from fastai.structured import *
from pandas_summary import DataFrameSummary
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from IPython.display import display
from sklearn import metrics


# In[ ]:


PATH = '../input'


# In[ ]:


df_raw = pd.read_csv(f'{PATH}/train.csv', low_memory=False)


# In[ ]:


df_raw.describe()


# In[ ]:


def display_all(df):
    with pd.option_context('display.max_rows',1000):
        with pd.option_context('display.max_columns',1000):
            display(df)
display_all(df_raw.tail().transpose())


# In[ ]:


df_raw['SalePrice'] = np.log(df_raw['SalePrice'])


# In[ ]:


train_cats(df_raw)


# In[ ]:


df_train, y, nas = proc_df(df_raw, 'SalePrice')


# In[ ]:


def split_vals(a,n): return a[:n].copy(), a[n:].copy()

n_valid=280
n_trn=len(df_train)-n_valid

X_train, X_valid = split_vals(df_train, n_trn)
y_train, y_valid = split_vals(y, n_trn)


X_train.shape, X_valid.shape, y_train.shape


# In[ ]:


def rmse(x,y): return math.sqrt(((x-y)**2).mean())
def print_score(m):
    res = [rmse(m.predict(X_train), y_train),
           rmse(m.predict(X_valid), y_valid),
           m.score(X_train, y_train), m.score(X_valid, y_valid)]
    if hasattr(m, 'oob_score_'): res.append(m.oob_score_)
    print(res)


# In[ ]:


m=RandomForestRegressor(n_jobs=-1, n_estimators=20, max_features=0.5, min_samples_leaf=3, oob_score=True)
get_ipython().run_line_magic('time', 'm.fit(X_train, y_train)')
print_score(m)


# In[ ]:


def plot_fi(fi): return fi.plot('cols', 'imp', 'barh', figsize=(10,16), legend=False)


# In[ ]:


fi = rf_feat_importance(m, df_train)
plot_fi(fi[fi.imp>0.005])


# In[ ]:


to_keep = fi[fi.imp>0.005].cols


# In[ ]:


len(to_keep)


# In[ ]:


df_trn2 = df_train[to_keep]


# In[ ]:


X_train, X_valid = split_vals(df_trn2, n_trn)

m=RandomForestRegressor(n_jobs=-1, n_estimators=20, max_features=0.5, min_samples_leaf=3, oob_score=True)
get_ipython().run_line_magic('time', 'm.fit(X_train, y_train)')
print_score(m)


# In[ ]:


fi = rf_feat_importance(m, df_trn2)
plot_fi(fi)


# In[ ]:


from scipy.cluster import hierarchy as hc


# In[ ]:


corr=np.round(scipy.stats.spearmanr(df_trn2).correlation,4)
corr_condensed = hc.distance.squareform(1-corr)
z = hc.linkage(corr_condensed, method='average')
fig = plt.figure(figsize=(10,16))
dendrogram = hc.dendrogram(z, labels=df_trn2.columns, orientation='left', leaf_font_size=16)


# In[ ]:




