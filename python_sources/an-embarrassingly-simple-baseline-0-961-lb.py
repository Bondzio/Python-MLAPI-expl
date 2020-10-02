#!/usr/bin/env python
# coding: utf-8

# Credit goes to @suicaokhoailang
# 
# https://www.kaggle.com/suicaokhoailang/an-embarrassingly-simple-baseline-0-960-lb

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
import math


# In[ ]:


df = pd.read_csv("../input/liverpool-ion-switching/test.csv")


# In[ ]:


n_groups = 40
df["group"] = 0
for i in range(n_groups):
    ids = np.arange(i*50000, (i+1)*50000)
    df.loc[ids,"group"] = i


# In[ ]:


for i in range(n_groups):
    sub = df[df.group == i]
    signals = sub.signal.values
    imax, imin = math.floor(np.max(signals)), math.ceil(np.min(signals))
    signals = (signals - np.min(signals))/(np.max(signals) - np.min(signals) + 2)
#     signals = (signals - np.min(signals))/(np.max(signals) - np.min(signals))
    signals = signals*(imax-imin)
    df.loc[sub.index,"open_channels"] = np.array(signals,np.int)


# In[ ]:


sample_df = pd.read_csv("../input/liverpool-ion-switching/sample_submission.csv", dtype={'time':str})


# In[ ]:


sample_df.open_channels = np.array(df.open_channels, np.int)
sample_df.to_csv("submission.csv",index=False)


# In[ ]:


get_ipython().system('head submission.csv')

