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


#importing libraries
from fastai import *
from fastai.vision import *
from fastai.metrics import error_rate
import os
import pandas as pd
import numpy as np


# In[ ]:


x  = '../input/10-monkey-species/training/training'
path = Path(x)
path.ls()


# In[ ]:


np.random.seed(40)
data = ImageDataBunch.from_folder(path, train = '.', valid_pct=0.2,
                                  ds_tfms=get_transforms(), size=224,
                                  num_workers=4).normalize(imagenet_stats)


# In[ ]:


data


# In[ ]:


data.c


# In[ ]:


print(data.classes)
len(data.classes),data.c


# In[ ]:


learn = cnn_learner(data, models.resnet18, metrics=[accuracy], model_dir = Path('../kaggle/working'),path = Path("."))


# In[ ]:


learn


# In[ ]:


learn.lr_find()
learn.recorder.plot(suggestions=True)


# In[ ]:


lr1 = 1e-04
lr2 = 1e-01
learn.fit_one_cycle(4,slice(lr1,lr2))


# In[ ]:


interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix()


# In[ ]:


img = open_image('../input/10-monkey-species/validation/validation/n8/n819.jpg')
print(learn.predict(img)[0])
img


# In[ ]:




