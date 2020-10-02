#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd

import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.tools as tls

import gc
from kaggle.competitions import twosigmanews

pd.options.mode.chained_assignment = None
pd.options.display.max_columns = 999

# Get 2Sigma environment
env = twosigmanews.make_env()


# In[ ]:


(market_train_df, news_train_df) = env.get_training_data()


# In[ ]:


market_train_df.shape


# In[ ]:


news_train_df.shape


# In[ ]:


market_train_df.head(5)


# In[ ]:


news_train_df.head()


# In[ ]:


gc.collect()


# In[ ]:


merge_df = pd.merge(market_train_df, news_train_df, how='inner',left_on=['assetName','time'], right_on = ['assetName','time'])


# In[ ]:


merge_df.shape


# In[ ]:


merge_df.head(10)


# In[ ]:


merge_df.isna().sum()


# In[ ]:


merge_df.dropna()


# In[ ]:


merge_df.isna().sum()


# ### Stay Connected For More Updates...###

# In[ ]:




