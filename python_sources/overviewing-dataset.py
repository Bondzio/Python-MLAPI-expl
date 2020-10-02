#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


from collections import Counter
NUM_CHILD = 1000000
NUM_GIFT = 1000
NUM_CHILD_IN_GIFTWISHLIST = int(NUM_CHILD / NUM_GIFT)
NUM_TWINS = int(NUM_CHILD * 0.004)


# preparing wishlist and twins

# In[ ]:


# load wishlist
df_c = pd.read_csv('../input/child_wishlist.csv', header=None)
df_c.columns = ['c_id'] + ['g_{}'.format(_i) for _i in list(range(10))]

# add twin id
df_t = df_c.copy().iloc[:NUM_TWINS, :]
df_t['t_id'] =df_t.c_id.apply(lambda x: 't_{}'.format(int(x  / 2)))
df_c = pd.merge(df_c, df_t[['c_id', 't_id']], how='left',on='c_id')

df_c
# TWINS_IDX


# preparing goodkids

# In[ ]:


df_g = pd.read_csv('../input/gift_goodkids.csv', header=None)
df_g.columns = ['g_id'] + ['c_{}'.format(_i) for _i in list(range(NUM_CHILD_IN_GIFTWISHLIST))]
print(df_g.shape)
df_g.head(3)


# ## Histogram for top of gift  in child wish list
# - There are gifts which are wished by a few children as by much children.
# - This mean, if child who wants the gift which have a few competitors is in top of list in goodkids list, it is better to give that gift to that child.

# In[ ]:


df_c.groupby('g_0')['c_id'].count().hist(bins=1000, normed=True)


# ## Count of children in goodkids
# - Not all children ( almost half of children ) appear in goodkids list
# - If there are gifts which are wished by both good kids and not goot kids, it is better to give the gift to good kids

# In[ ]:


goodkids_counter = Counter(list(df_g.iloc[:, 1:].values.flatten()))
df_g_hist = pd.DataFrame([(k, v) for k, v in dict(goodkids_counter).items()], columns=['c_id', 'goodkids_cnt'])
df_g_hist.shape


# In[ ]:


df_c_tmp = pd.merge(df_c, df_g_hist, how='left', on='c_id')
print(df_c_tmp.shape)
print(df_c_tmp.goodkids_cnt.describe())
df_c_tmp.head()


# # Same gift which twins want
# - A few (almost 10% ) twins want same gift in wishlist
# - twins do not want same gift as we expected

# In[ ]:


# prepare same gift in twin's wish list 
df_t = df_c[~df_c.t_id.isnull()]
duplication = []
for _t_id in df_t.t_id.unique():
    _wish1 = df_t[df_t.t_id == _t_id].iloc[0, 1:11].values
    _wish2 = df_t[df_t.t_id == _t_id].iloc[1, 1:11].values
    dup = list(set(_wish1) & set(_wish2))
    if len(dup) > 0:
        for _d in dup:
            duplication +=[(_t_id, _d)]


# In[ ]:


_df = pd.DataFrame(duplication, columns=['t_id', 'g_dup'])
print(_df.drop_duplicates('t_id').shape)
_df


# In[ ]:




