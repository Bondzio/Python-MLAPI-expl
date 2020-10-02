#!/usr/bin/env python
# coding: utf-8

# maybe this kernel is a rehash of https://www.kaggle.com/yag320/list-of-fake-samples-and-public-private-lb-split .

# In[1]:


import gc
import os
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
from multiprocessing import Pool

import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
PATH="../input/"
os.listdir(PATH)


# In[2]:


def merge_train_test(df_train, df_test):
    if "target" not in df_test.columns.values:
        df_test["target"] = -1
    res = pd.concat([df_train, df_test])
    res.reset_index(inplace=True, drop=True)
    return res

def split_train_test(df):
    df_train = df[df["target"] >= 0]
    df_test = df[df["target"] <= -1]
    df_train.reset_index(inplace=True, drop=True)
    df_test.reset_index(inplace=True, drop=True)
    assert list(df_train["ID_code"].values) == [f"train_{i}" for i in range(200000)]
    assert list(df_test["ID_code"].values) == [f"test_{i}" for i in range(200000)]
    return df_train, df_test


# In[3]:


get_ipython().run_cell_magic('time', '', 'train_df = pd.read_csv(PATH+"train.csv")\ntest_df = pd.read_csv(PATH+"test.csv")')


# ## 1. real/fake split

# In[4]:


class CountEncoder:
    def fit(self, series):
        self.counts = series.groupby(series).count()
    
    def transform(self, series):
        return series.map(self.counts).fillna(0).astype(np.int16)


# count encoding with all data. since I had known count encoding improves CV (also LB, but little), I guessed there are some secret in count encoding.

# In[5]:


get_ipython().run_cell_magic('time', '', 'df_merged = merge_train_test(train_df, test_df)\nfor i in range(200):\n    enc = CountEncoder()\n    var = df_merged[f"var_{i}"]\n    enc.fit(var)\n    df_merged[f"{i}_count_enc"] = enc.transform(var)')


# compare the mean of count of train and test.

# In[6]:


train_df, test_df = split_train_test(df_merged)
for v in range(10):
    cnt_mean_trn = train_df[f"{v}_count_enc"].mean()
    cnt_mean_test = test_df[f"{v}_count_enc"].mean()
    print(f"cnt_mean_trn={cnt_mean_trn:2.5f}, cnt_mean_test={cnt_mean_test:2.5f}, diff={cnt_mean_trn-cnt_mean_test:.5f}")


# count of test data is 1.5 larger than train data. strange...

# then checked: how many `count_enc==1` in the same row?

# In[7]:


get_ipython().run_cell_magic('time', '', 'df_merged["count_enc_1s"] = 0\nfor v in range(200):\n    df_merged["count_enc_1s"] += (df_merged[f"{v}_count_enc"]==1)\ntrain_df, test_df = split_train_test(df_merged)')


# In[8]:


plt.figure(figsize=(20, 4))
plt.hist(train_df["count_enc_1s"], range=(-0.5, 99.5), bins=100, alpha=0.5, label="train")
plt.hist(test_df["count_enc_1s"], range=(-0.5, 99.5), bins=100, alpha=0.5, label="test")
plt.legend()
plt.show()


# !?!?!?

# `count_enc_1s==0` can mean all values in the row are duplicated.
# 
# how many `count_enc_1s==0` rows?

# In[9]:


(test_df["count_enc_1s"]==0).sum()


# I submitted a file and found that the rows with `count_enc_1s==0` does not affect public LB.  
# so I thought those are private data.

# In[10]:


test_df["target"] = -1 - (test_df["count_enc_1s"] == 0)  # -1: public?  -2: private?
test_df.head()

# actually -1 is real and -2 is fake


# ## 2. public/private split

# I found that:  
# *all values in private? data also appears in public? data.*

# In[11]:


get_ipython().run_cell_magic('time', '', 'for val, df_grouped in test_df.groupby(f"var_{v}"):\n    if -2 in df_grouped["target"].values:\n        assert -1 in df_grouped["target"].values\nprint("ok")')


# so it can be said that all values in private? data are duplicated from public? data.

# then I thought:  
# *the target of data duplicated from `target==1` is 1?*

# if the value which is unique in public? data appeares in some private data, maybe those have the same target value.  
# (cf. graph features in Quora Question Pairs)

# In[12]:


# unionfind tree
class Uf:
    def __init__(self, N):
        self.Par = list(range(N))

    def root(self, x):
        if self.Par[x] == x:
            return x
        else:
            self.Par[x] = self.root(self.Par[x])
            return self.Par[x]

    def same(self, x, y):
        return self.root(x) == self.root(y)

    def unite(self, x, y):
        x = self.root(x)
        y = self.root(y)
        if x != y:
            self.Par[x] = y


# In[13]:


get_ipython().run_cell_magic('time', '', 'from itertools import groupby\nfrom operator import itemgetter\n\nindex = range(200000)\ntarget = test_df["target"].values\n\nuf = Uf(200000)\nfor v in range(200):\n    data = test_df[f"var_{v}"].values\n    for k, g in groupby(sorted(zip(data, target, index)), key=itemgetter(0)):  # grouping by raw value\n        g = list(g)\n        if [tgt for _, tgt, _ in g].count(-1) == 1:  # if the value is unique in public? data\n            idx0 = g[0][2]\n            for _, _, idx in g[1:]:\n                uf.unite(idx0, idx)  # belong to same group')


# In[14]:


from collections import defaultdict
cnt = defaultdict(int)
for i in test_df.index.values:
    cnt[uf.root(i)] += 1
cnt


# In[15]:


cnt = defaultdict(int)
for i in test_df[target==-1].index.values:
    cnt[uf.root(i)] += 1
cnt


# In[16]:


cnt = defaultdict(int)
for i in test_df[target==-2].index.values:
    cnt[uf.root(i)] += 1
cnt


# public? and private? were split into two groups.
# 
# then I found one of the group does not affect LB.  
# so I was confused but my teammate mamas suggested private? was not private, but fake.
# 
# we finally found true public/private split and real/fake split.

# In[18]:


test_df["public_private"] = [uf.root(idx)==166779 for idx in range(200000)]
test_df.head()


# In[ ]:




