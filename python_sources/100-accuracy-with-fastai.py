#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# In[ ]:


get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


from fastai.vision import *
from fastai.metrics import error_rate


# In[ ]:


path = Path('/kaggle/input/blood-cells/dataset2-master/dataset2-master/images')
path.ls()


# In[ ]:


path.ls()


# In[ ]:


data = ImageDataBunch.from_folder(path, train='TRAIN', test='TEST', valid_pct=0.20,
        ds_tfms=get_transforms(), size=224, num_workers=4).normalize(imagenet_stats)


# In[ ]:


data.classes


# In[ ]:


data.c, len(data.train_ds), len(data.valid_ds)


# In[ ]:


data.show_batch(rows=3, figsize=(5,5))


# In[ ]:


learn = cnn_learner(data, models.resnet34, metrics=error_rate)


# In[ ]:


learn.fit_one_cycle(2)


# In[ ]:


learn.unfreeze()


# In[ ]:


learn.model_dir=Path('/kaggle/working')
learn.lr_find()


# In[ ]:


learn.recorder.plot()


# In[ ]:


learn.fit_one_cycle(3, max_lr=slice(5e-5,5e-4))


# In[ ]:


learn.save('model')


# In[ ]:


interp = ClassificationInterpretation.from_learner(learn)


# In[ ]:


interp.plot_confusion_matrix()


# In[ ]:




