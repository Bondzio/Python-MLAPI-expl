#!/usr/bin/env python
# coding: utf-8

# I have used the [ULMFiT](https://arxiv.org/abs/1801.06146) method on the task. It comprises the following training steps:
# 
# - Take a language model (LM) pre-trained on a large general domain corpus, in this case an AWD-LSTM trained on WikiText-103
# - Fine-tune the LM on the task text (train and test) using the various fastai training tricks including traingular slanted learning rates
# - Further fine-tune on the classification task using gradual unfreezing of layers
# 
# I've managed to get up to 0.818 F1, but this varies significantly between runs.

# In[ ]:


## libraries
import numpy as np
import pandas as pd
from fastai.text import *
from pathlib import Path


# In[ ]:


## create directory and path for models
if not os.path.isdir('../model'):
    os.makedirs('../model')
    
path_model = Path("../model")


# In[ ]:


## read in datasets
train = pd.read_csv('/kaggle/input/nlp-getting-started/train.csv')
test = pd.read_csv('/kaggle/input/nlp-getting-started/test.csv')
sub = pd.read_csv('/kaggle/input/nlp-getting-started/sample_submission.csv')


# In[ ]:


## create databunch with both train and test text and label for language model
bs = 48
data_lm = (TextList.from_df(pd.concat([train[['text']], test[['text']]], ignore_index=True, axis=0), path_model)
           .split_by_rand_pct(0.1)
           .label_for_lm()
           .databunch(bs=bs))


# In[ ]:


## check tokenisation looks ok on training set
data_lm.show_batch()


# In[ ]:


## create lm learner with pre-trained model
learn = language_model_learner(data_lm, AWD_LSTM, drop_mult=0.3)


# In[ ]:


## run lr finder
learn.lr_find()


# In[ ]:


## plot lr finder
learn.recorder.plot(skip_end=15)


# In[ ]:


## train for one epoch frozen
learn.fit_one_cycle(1, 1.3e-2, moms=(0.8,0.7))


# In[ ]:


## unfreeze and train for four further cycles unfrozen
learn.unfreeze()
learn.fit_one_cycle(4, 1e-3, moms=(0.8,0.7))


# In[ ]:


## save model and encoder
learn.save('fine_tuned')
learn.save_encoder('fine_tuned_enc')


# In[ ]:


## training set with text and target
df = train[['text', 'target']]


# In[ ]:


## test set with text
df_test = test[['text']]


# In[ ]:


## create databunch for classification task, 
## including randomly selected validation set, and test set
bs = 16
data_clas = (TextList.from_df(df, path_model, vocab=data_lm.vocab)
             #.split_none()
             .split_by_rand_pct(0.1)
             .label_from_df('target')
             .add_test(TextList.from_df(df_test, path_model, vocab=data_lm.vocab))
             .databunch(bs=bs))


# In[ ]:


## check test set looks ok
data_clas.show_batch(ds_type=DatasetType.Test)


# In[ ]:


## create classification learning, including f1 score in metrics, and add encoder
learn = text_classifier_learner(data_clas, AWD_LSTM, drop_mult=0.5, metrics=[accuracy, FBeta(beta=1)])
learn.load_encoder('fine_tuned_enc')


# In[ ]:


## run lr finder
learn.lr_find()


# In[ ]:


## plot lr finder
learn.recorder.plot()


# In[ ]:


## train for 1 cycle frozen
learn.fit_one_cycle(1, 2e-2, moms=(0.8,0.7))


# In[ ]:


## unfreeze the last 2 layers and train for 1 cycle
learn.freeze_to(-2)
learn.fit_one_cycle(1, slice(1e-2/(2.6**4),1e-2), moms=(0.8,0.7))


# In[ ]:


## unfreeze the last 3 layers and train for 1 cycle
learn.freeze_to(-3)
learn.fit_one_cycle(1, slice(5e-3/(2.6**4),5e-3), moms=(0.8,0.7))


# In[ ]:


## unfreeze all and train for 2 cycles
learn.unfreeze()
learn.fit_one_cycle(2, slice(1e-3/(2.6**4),1e-3), moms=(0.8,0.7))


# In[ ]:


## get test set predictions and ids
preds, _ = learn.get_preds(ds_type=DatasetType.Test,  ordered=True)
preds = preds.argmax(dim=-1)

id = test['id']


# In[ ]:


my_submission = pd.DataFrame({'id': id, 'target': preds})
my_submission.to_csv('submission.csv', index=False)


# In[ ]:




