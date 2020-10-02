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


# In[ ]:


from fastai.vision import *
from fastai.metrics import error_rate


# In[ ]:


import glob
train_arr = []
for file in glob.glob("../input/train/train/*/*"):
    train_arr.append({"name": file, "label": file.split("/")[-2]})
df = pd.DataFrame(train_arr)


# In[ ]:


test_df = pd.read_csv(f"../input/sample_submission.csv")


# In[ ]:


df.sample(frac=1).head()


# In[ ]:


df["label"].value_counts()


# In[ ]:


import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode,iplot
import plotly.figure_factory as ff
init_notebook_mode(connected=True)
import matplotlib.cm as cm
import re


# In[ ]:


get_ipython().system('pip install imagesize')


# In[ ]:


import imagesize
df["width"] = 0
df["height"] = 0
df["aspect_ratio"] = 0.0
for idx, row in df.iterrows():
    width, height = imagesize.get(row["name"])
    df.at[idx, "width"] = width
    df.at[idx, "height"] = height
    df.at[idx, "aspect_ratio"] = float(height) / float(width)


# In[ ]:


df.head()


# In[ ]:


path = Path("../input")
SEED = 24
tfms = get_transforms(do_flip=True, max_rotate=10, max_zoom=1.3, max_lighting=0.4, max_warp=0.25, xtra_tfms=[rgb_randomize(channel=0, thresh=0.9, p=0.1),rgb_randomize(channel=2, thresh=0.9, p=0.1),rgb_randomize(channel=2, thresh=0.9, p=0.1)])
data = ImageDataBunch.from_folder(path/"train",valid_pct=0.2, ds_tfms=tfms, size=128, bs=64, seed=SEED).normalize(imagenet_stats)


# In[ ]:


data.show_batch(rows=2, figsize=(5,5))


# In[ ]:


learn = cnn_learner(data, models.resnet34, metrics=[accuracy],model_dir="/tmp/model/")


# In[ ]:


learn.lr_find()
learn.recorder.plot()


# In[ ]:


lr=5e-2
learn.fit_one_cycle(15,slice(lr))


# In[ ]:


learn.save('stage1')


# In[ ]:


learn.load('stage1')


# In[ ]:


learn.unfreeze()


# In[ ]:


learn.lr_find()
learn.recorder.plot()


# In[ ]:


learn.fit_one_cycle(10, slice(7e-6, (7e-6)/10))


# In[ ]:


learn.save('stage-2')


# In[ ]:


path = Path("../input")
SEED = 24
tfms = get_transforms(do_flip=True, max_rotate=10, max_zoom=1.3, max_lighting=0.4, max_warp=0.25, xtra_tfms=[rgb_randomize(channel=0, thresh=0.9, p=0.1),rgb_randomize(channel=2, thresh=0.9, p=0.1),rgb_randomize(channel=2, thresh=0.9, p=0.1)])
data = ImageDataBunch.from_folder(path/"train",valid_pct=0.2, ds_tfms=tfms, size=256, bs=64, seed=SEED).normalize(imagenet_stats)


# In[ ]:


learn.data = data


# In[ ]:


learn.freeze()


# In[ ]:


learn.lr_find()
learn.recorder.plot()


# In[ ]:


lr=7e-3


# In[ ]:


learn.fit_one_cycle(15, slice(lr))


# In[ ]:


learn.save('stage-3')


# In[ ]:


learn.load('stage-3')


# In[ ]:


learn.unfreeze()


# In[ ]:


learn.lr_find()
learn.recorder.plot()


# In[ ]:


learn.fit_one_cycle(10, slice(1e-5, 1e-4))


# In[ ]:


path = "../input"
test_df = pd.read_csv(f"{path}/sample_submission.csv")
sub_df = pd.read_csv(f"{path}/sample_submission.csv")
data.add_test(ImageList.from_df(test_df, path, folder="test/test"))


# In[ ]:


test_probs, _ = learn.get_preds(ds_type=DatasetType.Test)
test_preds = [data.classes[pred] for pred in np.argmax(test_probs.numpy(), axis=-1)]


# In[ ]:


sub_df = pd.read_csv(f"{path}/sample_submission.csv")
sub_df.predicted_class = test_preds
sub_df.to_csv("submission.csv", index=False)


# In[ ]:




