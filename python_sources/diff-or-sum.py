#!/usr/bin/env python
# coding: utf-8

# The saga continues with trying to differentiate the classes.  We know that distinguishing between 88,92 is easy where 42,90 is hard for most models

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.metrics import log_loss
from sklearn.model_selection import StratifiedKFold
import matplotlib.pyplot as plt
import seaborn as sns 


# In[ ]:


meta_train = pd.read_csv('../input/training_set_metadata.csv')
train = pd.read_csv('../input/training_set.csv')


# In[ ]:


for ix in range(2):
    fig, axes = plt.subplots(2, 6,figsize=(15,10))
    for i, t in enumerate([42,90]):
        for pb in train.passband.unique():
            oid = meta_train[meta_train.target==t].object_id.values[ix]
            a = train[(train.passband==pb)&(train.object_id==oid)]
            x = a.groupby(['object_id','passband'])['mjd','flux'].diff().fillna(0)
            x['object_id'] = a.object_id
            x = x.groupby(['object_id'])['mjd','flux'].cumsum().fillna(0)
            x['object_id'] = a.object_id
            x['detected'] = a.detected
            axes[i, pb].scatter(x.mjd,x.flux,s=1)


# In[ ]:


for ix in range(2):
    fig, axes = plt.subplots(2, 6,figsize=(15,10))

    for i, t in enumerate([88,92]):
        for pb in train.passband.unique():
            oid = meta_train[meta_train.target==t].object_id.values[ix]
            a = train[(train.passband==pb)&(train.object_id==oid)]
            x = a.groupby(['object_id','passband'])['mjd','flux'].diff().fillna(0)
            x['object_id'] = a.object_id
            x = x.groupby(['object_id'])['mjd','flux'].cumsum().fillna(0)
            x['object_id'] = a.object_id
            x['detected'] = a.detected
            axes[i, pb].scatter(x.mjd,x.flux,s=1)


# Now let us do some Lomb Scargle

# In[ ]:


from astropy.stats import LombScargle


# In[ ]:


for ix in range(2):
    fig, axes = plt.subplots(2, 6,figsize=(15,10))
    for i, t in enumerate([42,90]):
        for pb in train.passband.unique():
            oid = meta_train[meta_train.target==t].object_id.values[ix]
            a = train[(train.passband==pb)&(train.object_id==oid)]
            x = a.groupby(['object_id','passband'])['mjd','flux'].diff().fillna(0)
            x['object_id'] = a.object_id
            x = x.groupby(['object_id'])['mjd','flux'].cumsum().fillna(0)
            x['object_id'] = a.object_id
            x['detected'] = a.detected
            frequency, power = LombScargle(x.mjd,x.flux).autopower(nyquist_factor=2)
            axes[i, pb].scatter(frequency,power,s=1)


# In[ ]:


for ix in range(2):
    fig, axes = plt.subplots(2, 6,figsize=(15,10))
    for i, t in enumerate([88,92]):
        for pb in train.passband.unique():
            oid = meta_train[meta_train.target==t].object_id.values[ix]
            a = train[(train.passband==pb)&(train.object_id==oid)]
            x = a.groupby(['object_id','passband'])['mjd','flux'].diff().fillna(0)
            x['object_id'] = a.object_id
            x = x.groupby(['object_id'])['mjd','flux'].cumsum().fillna(0)
            x['object_id'] = a.object_id
            x['detected'] = a.detected
            frequency, power = LombScargle(x.mjd,x.flux).autopower(nyquist_factor=2)
            axes[i, pb].scatter(frequency,power,s=1)

