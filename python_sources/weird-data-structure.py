#!/usr/bin/env python
# coding: utf-8

# Look at the diagonals

# In[ ]:


import pandas as pd
import numpy as np
from pathlib import Path


# In[ ]:


root = Path("../input")


# In[ ]:


train = pd.read_csv(root.joinpath("train.csv"))
test = pd.read_csv(root.joinpath("test.csv"))


# In[ ]:


target = train.target.values
del train['target']
train['target'] = target
test['target'] = -1


# In[ ]:


x = train['var_0'].value_counts()
x = x[x==1].reset_index(drop=False)
x.head()


# In[ ]:


candidates = []
for c in train.columns[1:-1]:
    if(train[train[c] == x['index'][0]].shape[0]==1):
        candidates.append(c)
indexes = []
for c in candidates:
    indexes.append(train[train[c] == x['index'][0]].index.values[0])
y = train.iloc[indexes][candidates]
y.head(y.shape[0])


# In[ ]:


candidates = []
for c in test.columns[1:-1]:
    if(test[test[c] == x['index'][0]].shape[0]==1):
        candidates.append(c)
indexes = []
for c in candidates:
    indexes.append(test[test[c] == x['index'][0]].index.values[0])
y = test.iloc[indexes][candidates]
y.head(y.shape[0])


# In[ ]:


candidates = []
for c in train.columns[1:-1]:
    if(train[train[c] == x['index'][1]].shape[0]==1):
        candidates.append(c)
indexes = []
for c in candidates:
    indexes.append(train[train[c] == x['index'][1]].index.values[0])
y = train.iloc[indexes][candidates]
y.head(y.shape[0])


# In[ ]:


candidates = []
for c in test.columns[1:-1]:
    if(test[test[c] == x['index'][1]].shape[0]==1):
        candidates.append(c)
indexes = []
for c in candidates:
    indexes.append(test[test[c] == x['index'][1]].index.values[0])
y = test.iloc[indexes][candidates]
y.head(y.shape[0])

