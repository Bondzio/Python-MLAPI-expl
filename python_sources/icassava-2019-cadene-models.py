#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install pretrainedmodels')


# In[ ]:


import pretrainedmodels


# In[ ]:


import os


# In[ ]:


os.listdir("../input/train/train")


# In[ ]:


os.listdir("../input/train/train/cgm")[:10]


# In[ ]:


os.listdir("../input/test/test/0")[:10]


# In[ ]:


from fastai import *
from fastai.vision import *

import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import auc,roc_curve

from math import floor


# In[ ]:


train_path = "../input/train/train"
test_path = "../input/test/test/0"


# In[ ]:


def get_labels(file_path): 
    dir_name = os.path.dirname(file_path)
    split_dir_name = dir_name.split("/")
    dir_levels = len(split_dir_name)
    label  = split_dir_name[dir_levels - 1]
    return(label)


# In[ ]:


get_labels("../input/train/train/cgm/train-cgm-528.jpg")


# In[ ]:


from glob import glob
imagePatches = glob("../input/train/train/*/*.*", recursive=True)
imagePatches[0:10]


# In[ ]:


path=""
tfms = get_transforms() 


# In[ ]:


data = ImageDataBunch.from_name_func(path, imagePatches, label_func=get_labels,  size=500, 
                                     bs=20,num_workers=2,test = test_path,ds_tfms=tfms
                                  ).normalize(imagenet_stats)


# In[ ]:


type(data)


# In[ ]:


data.show_batch(rows=3, figsize=(8,8))


# In[ ]:


def se_resnext50_32x4d(pretrained=False):
    pretrained = 'imagenet' if pretrained else None
    model = pretrainedmodels.se_resnext50_32x4d(pretrained=pretrained)
    return model


# In[ ]:


learner = cnn_learner(data, se_resnext50_32x4d, pretrained=True,
                   cut=-2, split_on=lambda m: (m[0][3], m[1]),metrics = [accuracy])


# In[ ]:


learner.lr_find()
learner.recorder.plot()


# In[ ]:


lr=1e-1
learner.fit_one_cycle(1, lr)


# In[ ]:


learner.save('model-1')


# In[ ]:


learner.unfreeze()


# In[ ]:


learner.lr_find()
learner.recorder.plot()


# In[ ]:


learner.freeze_to(-2)


# In[ ]:


learner.lr_find()
learner.recorder.plot()


# In[ ]:


learner.fit_one_cycle(80, 1e-5)


# In[ ]:


learner.recorder.plot_losses()


# In[ ]:


learner.validate()


# In[ ]:


interp = ClassificationInterpretation.from_learner(learner)


# In[ ]:


interp.plot_top_losses(9, figsize=(15,11))


# In[ ]:


interp.most_confused(min_val=2)


# In[ ]:


preds,y = learner.TTA(ds_type=DatasetType.Test)


# In[ ]:


len(preds)


# In[ ]:


len(os.listdir(test_path))


# In[ ]:


SAMPLE_SUB = '../input/sample_submission_file.csv'
sample_df = pd.read_csv(SAMPLE_SUB)


# In[ ]:


sample_df.head()


# In[ ]:


predictions = preds.numpy()


# In[ ]:


class_preds = np.argmax(predictions, axis=1)


# In[ ]:


for c, i in learner.data.train_ds.y.c2i.items():
    print(c,i)


# In[ ]:


categories = ['cbb','cbsd','cgm','cmd','healthy']

def map_to_categories(predictions):
    return(categories[predictions])

categories_preds = list(map(map_to_categories,class_preds))


# In[ ]:


filenames = list(map(os.path.basename,os.listdir(test_path)))


# In[ ]:


df_sub = pd.DataFrame({'Category':categories_preds,'Id':filenames})


# In[ ]:


df_sub.head()


# In[ ]:


# Export to csv
df_sub.to_csv('submission_categories.csv', header=True, index=False)

