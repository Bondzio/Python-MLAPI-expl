#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('reload_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

from fastai import *
from fastai.vision import *

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


PATH = Path('../input')
input_size = 32
batch_size = 32


# In[ ]:


arabic_labels = ['alef', 'beh', 'teh', 'theh', 'jeem', 'hah', 'khah', 'dal', 'thal',
                'reh', 'zain', 'seen', 'sheen', 'sad', 'dad', 'tah', 'zah', 'ain', 
                'ghain', 'feh', 'qaf', 'kaf', 'lam', 'meem', 'noon', 'heh', 'waw', 'yeh']
np.random.seed(42)
tfms = get_transforms(do_flip=False)
s = '([^/\d]+)\d+.jpg$'
data = (ImageItemList.from_folder(PATH)
        .random_split_by_pct()
        .label_from_re(s,classes = arabic_labels)
        .transform(tfms,size=input_size)
        .databunch(bs=batch_size)
        .normalize(imagenet_stats))


# In[ ]:


data.show_batch(3)


# In[ ]:


learn = create_cnn(data,models.resnet50,model_dir = Path("../working/tmp/models"),metrics=[accuracy,error_rate])


# In[ ]:


learn.fit_one_cycle(4)


# In[ ]:


learn.lr_find()


# In[ ]:


learn.recorder.plot()


# In[ ]:


learn.save('stage-1-50')


# In[ ]:


learn.load('stage-1-50')


# In[ ]:


learn.unfreeze()


# In[ ]:


learn.fit_one_cycle(14,max_lr=slice(1e-5,0.003/5))


# In[ ]:


learn.save('stage-2-50')


# In[ ]:


interp = ClassificationInterpretation.from_learner(learn)


# In[ ]:


# Showing training examples with largest losses along with their prediction, actual, loss, and probability of predicted class.
interp.plot_top_losses(5)


# In[ ]:


# Replace validation set with the test set to get the accuracy on the held-out test set
s = '([^/\d]+)\d+.jpg$'
data_test = (ImageItemList.from_folder(PATH)
        .split_by_folder(train='train', valid='test')
        .label_from_re(s,classes = arabic_labels)
        .transform(tfms,size=input_size)
        .databunch(bs=batch_size) 
        .normalize(imagenet_stats))
        
learn.validate(data_test.valid_dl,metrics=[accuracy,error_rate])


# In[ ]:


learn.show_results()


# In[ ]:




