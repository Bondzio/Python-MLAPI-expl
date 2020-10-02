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

# Any results you write to the current directory are saved as output.


# ### Fast AI setup

# In[ ]:


get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


from fastai import *
from fastai.vision import *
import torch


# ### First look at the Data

# In[ ]:


path = Path('../input/aptos2019-blindness-detection')
path_train = path/'train_images'
path_test = path/'test_images'
path, path_train, path_test


# In[ ]:


labels = pd.read_csv(path/'train.csv')
labels.head()


# In[ ]:


img = open_image(path_train/'000c1434d8d7.png')
img.show(figsize = (7,7))
print(img.shape)


# In[ ]:


# Distribution of the 5 diagnosis categories
labels['diagnosis'].value_counts().plot(kind = 'bar', title='Distribution of diagnosis categories')
plt.show()


# The non-uniform distribution of data in our training set can be easily observed

# ### Creating a DataBunch

# In[ ]:


# Apply data augmentation to the images
tfms = get_transforms(
    do_flip=True,
    flip_vert=False,
    max_warp=0.2,
    max_rotate=360.,
    max_zoom=1.2,
    max_lighting=0.1,
    p_lighting=0.5
)


# In[ ]:


# Applying aptos19 normalization and standard deviation stats, from a pre-trained model found on a kaggle kernel
aptos19_stats = ([0.42, 0.22, 0.075], [0.27, 0.15, 0.081])


# In[ ]:


test_labels = pd.read_csv(path/'sample_submission.csv')
test = ImageList.from_df(test_labels, path = path_test, suffix = '.png')


# In[ ]:


src = (ImageList.from_df(labels, path = path_train, suffix = '.png')
       .split_by_rand_pct(seed = 2019)
       .label_from_df(cols = 'diagnosis')
       .add_test(test) )


# In[ ]:


data = (
    src.transform(
        tfms,
        size = 446, 
        resize_method=ResizeMethod.SQUISH,
        padding_mode='zeros'
    )
    .databunch(bs=16)
    .normalize(aptos19_stats))


# In[ ]:


# data


# In[ ]:


# data.show_batch(3, figsize = (7,7))


# In[ ]:


print(data.classes)
print(len(data.train_ds))
print(len(data.valid_ds))
print(len(data.test_ds))


# ### Setting up the Model

# In[ ]:


get_ipython().system('mkdir -p /tmp/.cache/torch/checkpoints')
get_ipython().system('cp ../input/resnet34/resnet34.pth /tmp/.cache/torch/checkpoints/resnet34-333f7ec4.pth')
get_ipython().system('cp ../input/resnet152/resnet152.pth /tmp/.cache/torch/checkpoints/resnet152-b121ed2d.pth')

get_ipython().system('cp ../input/resnet50/resnet50.pth /tmp/.cache/torch/checkpoints/resnet50-19c8e357.pth')


# In[ ]:


kappa = KappaScore("quadratic")
kappa


# In[ ]:


from sklearn.metrics import cohen_kappa_score
def quadratic_kappa(y_hat, y):
    return torch.tensor(cohen_kappa_score(torch.round(y_hat), y, weights='quadratic'),device='cuda:0')


# In[ ]:


learn = cnn_learner(
    data, 
        models.resnet50, 
    metrics = [accuracy,quadratic_kappa], 
    model_dir = Path('../kaggle/working'),
    path = Path("."),
    pretrained=True
)


# In[ ]:


# learn.lr_find()
# learn.recorder.plot()


# In[ ]:


learn.fit_one_cycle(5, slice(1e-2, 1e-1))


# In[ ]:


learn.save('resnet50-1')


# ### Unfreeze and Learn some more

# In[ ]:


# learn.lr_find()
# learn.recorder.plot()


# In[ ]:


# learn.fit_one_cycle(4, slice(2e-6,2e-5))


# In[ ]:


# learn.save('resnet152-2')


# In[ ]:


# learn.load('resnet152-2');


# In[ ]:


# learn.export()


# ### Double the size of images

# In[ ]:


# data = (
#     src.transform(
#         tfms,
#         size = 448, 
#         resize_method=ResizeMethod.SQUISH,
#         padding_mode='zeros'
#     )
#     .databunch(bs=8)
#     .normalize(aptos19_stats))


# In[ ]:


# learn.data = data


# In[ ]:


# learn.freeze()


# In[ ]:


# learn.lr_find()
# learn.recorder.plot()


# In[ ]:


# learn.fit_one_cycle(5, 6e-4)


# In[ ]:


# learn.save('resnet152-3')


# In[ ]:


# learn.load('resnet152-3');


# In[ ]:


# learn.lr_find()


# In[ ]:


# learn.recorder.plot()


# In[ ]:


# learn.fit_one_cycle(8,slice(1e-6, 1e-5))


# In[ ]:


# learn.save('resnet152-4')


# In[ ]:


# learn.load('resnet152-4');


# ### Get Predictions

# In[ ]:


# learn.load('resnet152-4');


# In[ ]:


preds, _ = learn.get_preds(ds_type=DatasetType.Test)


# ### Preparing Submission

# In[ ]:


submission = pd.read_csv(path/'sample_submission.csv')
submission.head()


# In[ ]:


preds = np.array(preds.argmax(1)).astype(int).tolist()
preds[:5]


# In[ ]:


submission['diagnosis'] = preds
submission.head()


# In[ ]:


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# In[ ]:


submission.to_csv('submission.csv', index = False)

