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


# # Imports

# In[ ]:


from fastai.text import *
from fastai.datasets import URLs
import torch
import pandas as pd
import numpy as np
import logging
import os
import random


# # Utils

# In[ ]:


get_ipython().system('( head -5000 ../input/train.csv ) > train.csv # reducing size to train to quickly run the entire code and submit ')
get_ipython().system('cp ../input/test.csv test.csv')
train_file = 'train.csv'
test_file = 'test.csv'
folder = '.'


# # Load language model

# In[ ]:


data_lm = TextLMDataBunch.from_csv(folder, 
                                   train_file, 
                                   text_cols='question_text', 
                                   label_cols='target')
assert data_lm.device == torch.device('cuda')


# # Save language model

# In[ ]:


data_lm.save('data_lm_export.pkl')


# # Load classifier model

# In[ ]:


data_clas = TextClasDataBunch.from_csv(folder, 
                                       train_file,
                                       test=test_file,
                                       valid_pct=0.1,
                                       vocab=data_lm.train_ds.vocab, 
                                       bs=32,
                                       text_cols='question_text', 
                                       label_cols='target')


# # Save classifier model

# In[ ]:


data_clas.save('data_clas_export.pkl')


# # Fine tune language model

# In[ ]:


# Language model trainer (66 min with whole training set)
learn = language_model_learner(data_lm, AWD_LSTM,
                           drop_mult=0.5)
learn.fit_one_cycle(1 , 1e-2)
learn.save_encoder('encoder')


# # Fine tune classifier model

# In[ ]:


learn_classifier = text_classifier_learner(data_clas, AWD_LSTM, drop_mult=0.5)
learn_classifier.load_encoder('encoder')
learn_classifier.fit_one_cycle(1, 1e-2) 


# # Prediction

# In[ ]:


# Language model prediction
learn.predict("This is a review about", n_words=10)


# In[ ]:


# Classifier model prediction
learn_classifier.predict("This is a review about a question")


# In[ ]:


preds,_ = learn_classifier.get_preds(ds_type=DatasetType.Test)


# In[ ]:


result_df = pd.read_csv("../input/sample_submission.csv")


# In[ ]:


result_df.prediction = preds.numpy()[:, 0]


# In[ ]:


result_df.describe()


# In[ ]:


result_df['prediction'] = (result_df['prediction'] > 0.98).astype(int)


# In[ ]:


result_df.to_csv('submission.csv', index=False)


# In[ ]:




