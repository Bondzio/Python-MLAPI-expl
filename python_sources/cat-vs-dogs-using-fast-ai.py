#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


from fastai.vision import *


# In[ ]:


path = Path('../input/dogs-cats-images/dataset/training_set/')
path.ls()


# In[ ]:


np.random.seed(2)
data = ImageDataBunch.from_folder(path, train=".", valid_pct=0.2,ds_tfms=get_transforms(), size=224, num_workers=4).normalize(imagenet_stats)


# In[ ]:



data.classes


# In[ ]:


data.show_batch(rows=6,figsize=(7,8))


# In[ ]:


data.classes, data.c, len(data.train_ds),len(data.valid_ds)


# In[ ]:


learn = cnn_learner(data, models.resnet34, metrics=accuracy)


# In[ ]:


learn.fit_one_cycle(2)


# In[ ]:


learn.model_dir ="/tmp/model/"


# In[ ]:


learn.save('stage-1')


# In[ ]:


interp = ClassificationInterpretation.from_learner(learn)


# In[ ]:


doc(interp.plot_top_losses)
#interp.plot_top_losses(9,figsize=(15,11))


# In[ ]:


interp.plot_top_losses(9,figsize=(15,11))


# In[ ]:


interp.plot_confusion_matrix(figsize = (10,10),dpi=50)


# In[ ]:


interp.most_confused(min_val=2)


# In[ ]:


check_img = learn.data.train_ds[1000][0]
print(learn.predict(check_img))
data.train_ds[1000][0]


# In[ ]:




