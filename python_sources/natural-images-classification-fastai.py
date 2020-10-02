#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

import os

from fastai import *
from fastai.vision import *


# In[ ]:


image_path = "../input/data/natural_images/"
image_list = list()

for label in os.listdir(image_path):
    for file in os.listdir("{}/{}".format(image_path, label)):
        image_list.append({"fname": "{}/{}/{}".format(image_path, label, file), "label": label})
        
df = pd.DataFrame(image_list)

trn_idx, val_idx = train_test_split(range(df.shape[0]), test_size=0.15, random_state=42)


# In[ ]:


data = (ImageList.from_df(path="./", df=df)
        .split_by_idx(val_idx)
        .label_from_df(cols="label")
        .transform(tfms=get_transforms(), size=224)
        .databunch(bs=32)
        .normalize(imagenet_stats))


# In[ ]:


data.show_batch(rows=3, figsize=(10, 8))


# In[ ]:


learn = create_cnn(data, models.resnet50, metrics=[accuracy])


# In[ ]:


learn.lr_find()


# In[ ]:


learn.recorder.plot()


# In[ ]:


learn.fit_one_cycle(2, 1e-02)


# In[ ]:


interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix(title='Confusion matrix')


# In[ ]:




