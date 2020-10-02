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


# In[ ]:


path = Path('../input/data /data')
path.ls()


# In[ ]:


train = path/'train'


# In[ ]:


np.random.seed(42)
data = ImageDataBunch.from_folder(path, train="train", valid_pct=0.2,
ds_tfms=get_transforms(do_flip=False, flip_vert=False, max_rotate=0,
               max_zoom=0, max_lighting=0, max_warp=0, p_affine=0, p_lighting=0.50, xtra_tfms=None), size=[150,400],bs=64, num_workers=4).normalize(imagenet_stats)


# In[ ]:


data.classes


# In[ ]:


data.show_batch(rows=2)


# In[ ]:


data.classes, data.c, len(data.train_ds),len(data.valid_ds)


# In[ ]:


len(data.train_ds)


# In[ ]:


len(data.valid_ds)


# In[ ]:





# In[ ]:


learn = cnn_learner(data, models.densenet121, metrics=accuracy)


# In[ ]:


#learning_rate =[0.0000000001,0.00000001, 0.000001]


# In[ ]:


learn.fit_one_cycle(40)


# In[ ]:


learn.export('/kaggle/working/d7.pkl')
learn.model_dir="/kaggle/working/models"
learn.save('d5')


# In[ ]:


learn.unfreeze()
learn.freeze()
learn.lr_find()
learn.recorder.plot()


# In[ ]:


learn.recorder.plot(suggestion=True)


# In[ ]:



learn.freeze()
learn.unfreeze()
learn.export('/kaggle/working/d7_2.pkl')
learn.save('d5_2')
learn.lr_find();learn.recorder.plot()


# In[ ]:


learn.recorder.plot_losses()


# In[ ]:


learn.recorder.plot_lr()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


interp = ClassificationInterpretation.from_learner(learn)

interp.plot_confusion_matrix()

