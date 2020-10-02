#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
import gc
import matplotlib.pyplot as plt
import seaborn as sns
import lightgbm as lgb
import logging


# In[ ]:


train = pd.read_csv('../input/training_set.csv')
print(train.shape)
meta_train = pd.read_csv('../input/training_set_metadata.csv')
print(meta_train.shape)


# In[ ]:


train.head()


# In[ ]:


meta_train.head()


# In[ ]:


x = train.copy()
x['mjd'] = x.groupby(['object_id','passband']).mjd.diff() #Try and give the change in flux by a standard time period
x['mjd'] = x['mjd'].fillna(0)
x.flux/=x.mjd
x.flux_err/=x.mjd
x.head()


# In[ ]:


x['cc'] = x.groupby(['object_id','passband'])['mjd'].cumcount()
x.drop('mjd',inplace=True,axis=1)


# In[ ]:


x = x.set_index(['object_id','passband','cc'])


# In[ ]:


x = x.unstack()


# In[ ]:


meta_train = meta_train.set_index('object_id')


# In[ ]:


x = x.join(meta_train,on='object_id',how='left')


# In[ ]:


x = x.reset_index(drop=False)


# In[ ]:


cols = ['_'.join(str(s).strip() for s in col if s) if len(col)==2 else col for col in x.columns ]
x.columns = cols


# In[ ]:


x.head()


# In[ ]:


fluxcolumns = [a  for a in x.columns if a.startswith('flux_') and not a.startswith('flux_err')]


# In[ ]:


x.target.unique()


# In[ ]:


uniques = sorted(x.target.unique())
f, ax = plt.subplots(len(uniques),6)
f.set_figheight(15)
f.set_figwidth(15)
for a in range(len(uniques)):
    for b in range(6):
        ax[a,b].set_xticks([])
   
for i in range(len(uniques)):
    ax[i][0].plot(x[(x.target==uniques[i])&(x.passband==0)][fluxcolumns].mean())
    ax[i][1].plot(x[(x.target==uniques[i])&(x.passband==1)][fluxcolumns].mean())
    ax[i][2].plot(x[(x.target==uniques[i])&(x.passband==2)][fluxcolumns].mean())
    ax[i][3].plot(x[(x.target==uniques[i])&(x.passband==3)][fluxcolumns].mean())
    ax[i][4].plot(x[(x.target==uniques[i])&(x.passband==4)][fluxcolumns].mean())
    ax[i][5].plot(x[(x.target==uniques[i])&(x.passband==5)][fluxcolumns].mean())

