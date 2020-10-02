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

import os
print(os.listdir("../input"))
from fastai.text import *
from tqdm import tqdm_notebook as tqdm
# Any results you write to the current directory are saved as output.


# In[ ]:


import fastai
fastai.__version__


# In[ ]:


train_df = pd.read_csv('../input/songdata.csv')


# In[ ]:


train_df.head()


# In[ ]:


data_lm = TextLMDataBunch.from_csv('../input/', 'songdata.csv')


# In[ ]:


data_lm.show_batch()


# In[ ]:


learn = language_model_learner(data_lm, AWD_LSTM,model_dir="/tmp/model/")


# In[ ]:


learn.lr_find()
learn.recorder.plot(skip_start=25)


# In[ ]:


learn.fit_one_cycle(1, 5e-2, moms=(0.8,0.7))


# In[ ]:


learn.unfreeze()


# In[ ]:


learn.fit_one_cycle(1, 1e-2, moms=(0.8,0.7))


# In[ ]:


learn.predict("How much does", n_words=10)


# In[ ]:


learn.predict("Why does", n_words=10)


# In[ ]:




