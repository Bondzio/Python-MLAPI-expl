#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import warnings
warnings.filterwarnings('ignore')

#setting up our enviroment
get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


from fastai import *
from fastai.vision import *
from fastai.metrics import error_rate
import os
import pandas as pd
import numpy as np


# In[ ]:


x  = '../input/waste-classification-data/DATASET/TRAIN'


# In[ ]:


path = Path(x)
path.ls()


# In[ ]:


np.random.seed(7)
data = ImageDataBunch.from_folder(path, train = '.', valid_pct=0.2,
                                  ds_tfms=get_transforms(), size=224,
                                  num_workers=4).normalize(imagenet_stats)


# In[ ]:


data.show_batch(rows=3, figsize=(7,6),recompute_scale_factor=True)


# In[ ]:


data


# In[ ]:


print(data.classes)
len(data.classes),data.c


# In[ ]:


learn = cnn_learner(data, models.resnet18, metrics=[accuracy], model_dir = Path('../kaggle/working'),path = Path("."))


# In[ ]:


learn.lr_find()
learn.recorder.plot(suggestions=True)


# In[ ]:


lr1 = 1e-3
lr2 = 1e-1
learn.fit_one_cycle(2,slice(lr1,lr2))
#can take more epochs; 4+ recommended


# In[ ]:


interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix()


# In[ ]:


learn.unfreeze()


# In[ ]:


learn.lr_find()
learn.recorder.plot()


# In[ ]:


lr = 1e-4
learn.fit_one_cycle(2,lr)
#can take more epochs; abobe 10 recommended


# In[ ]:


img = open_image('../input/waste-classification-data/DATASET/TEST/O/O_12632.jpg')
print(learn.predict(img)[0])
img


# In[ ]:


learn.export(file = Path("/kaggle/working/export.pkl"))


# In[ ]:


learn.model_dir = "/kaggle/working"
learn.save("stage-1",return_path=True)

