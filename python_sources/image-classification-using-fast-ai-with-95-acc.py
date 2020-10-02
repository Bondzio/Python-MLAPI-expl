#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Import Libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from fastai import *
from fastai.vision import *
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="torch.nn.functional")


# In[ ]:


os.listdir('../input/intel-image-classification')


# In[ ]:


path = '../input/intel-image-classification/seg_train/seg_train'
classes = os.listdir(path)
classes


# In[ ]:


data = ImageDataBunch.from_folder(path, train = '.',valid_pct = 0.2,
                                  ds_tfms = get_transforms(do_flip=True, max_rotate = 90, max_zoom = 1.2),seed = 0, size = 224, num_workers = 0).normalize(imagenet_stats)


# In[ ]:


data.show_batch(3, figsize = (15,10))


# In[ ]:


data.classes


# In[ ]:


print(f'Train Count::{len(data.train_ds)}')
print(f'Validation Count::{len(data.valid_ds)}')


# In[ ]:


learn = cnn_learner(data, models.resnet50, metrics=accuracy)
learn.fit_one_cycle(5)


# In[ ]:


interp = ClassificationInterpretation.from_learner(learn)
interp.plot_top_losses(9, figsize=(15,11))


# In[ ]:


interp.plot_confusion_matrix(figsize=(12,12), dpi = 60)


# In[ ]:


interp.most_confused(min_val=2)


# In[ ]:


learn.model_dir ="/tmp/model/"
learn.save('Intel_FastAI_5epochs')


# In[ ]:


learn.lr_find()


# In[ ]:


learn.recorder.plot()


# In[ ]:


learn.fit_one_cycle(2,max_lr=slice(1e-04,1e-02))


# In[ ]:


test_img = learn.data.train_ds[1][0]
print(learn.predict(test_img))

data.train_ds[1][0]


# In[ ]:


img = data.valid_ds[10][0]
learn.predict(img)
img.show(y=learn.predict(img)[0])


# In[ ]:


img = data.valid_ds[100][0]
learn.predict(img)
img.show(y=learn.predict(img)[0])


# In[ ]:


img = data.valid_ds[5][0]
learn.predict(img)
img.show(y=learn.predict(img)[0])


# In[ ]:




