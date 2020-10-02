#!/usr/bin/env python
# coding: utf-8

# In[34]:


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


# In[29]:


cwd = os.getcwd();cwd


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')

from fastai.vision import *
from fastai.metrics import *


# In[ ]:


bs = 32
path = untar_data(URLs.PETS)
path.ls()


# In[ ]:


fnames = get_image_files(path/'images')


# In[ ]:


np.random.seed(42)
pat = r'/([^/]+)_\d+.jpg$'

data = ImageDataBunch.from_name_re(path/'images',
                                  fnames,
                                  pat,
                                  ds_tfms=get_transforms(),
                                  size=224,
                                  bs=bs).normalize(imagenet_stats)


# In[ ]:


data.show_batch(rows=3, figsize=(6,6))


# In[ ]:


learn = cnn_learner(data, models.resnet34, metrics=error_rate)
learn.fit_one_cycle(4)


# In[25]:


learn.save('./stage-1')


# In[35]:


Path('/kaggle/').ls()


# In[37]:


learn.save('/kaggle/working/stage-1')


# In[38]:


Path('/kaggle/working/').ls()


# In[28]:


path.ls()


# In[ ]:


interp = ClassificationInterpretation.from_learner(learn)
interp.plot_top_losses(9, heatmap=False)


# In[ ]:


interp.plot_confusion_matrix(figsize=(12,12), dpi=60)


# In[ ]:


interp.most_confused(min_val=2)


# In[ ]:




