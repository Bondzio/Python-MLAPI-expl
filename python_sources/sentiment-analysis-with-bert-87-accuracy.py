#!/usr/bin/env python
# coding: utf-8

# # Twitter Sentiment Analysis with Bert
# In this notebook we show how to finetune BERT to Sentiment140 dataset to do sentiment classification on twitter.
# We first prepare the data removing urls from the training set and replacing hashtag and mentions with custom tokens.
# Then we fit Bert on the dataset and present the results. 
# 
# Because of kaggle's kernel limitations, we move the computation on Colab Gpu environment which you can follow here
# 
# 

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


# We load the dataset and select only the columns for text and label

# In[ ]:


t140 = pd.read_csv('/kaggle/input/sentiment140/training.1600000.processed.noemoticon.csv',
                   sep=',',
                   header=None,
                   encoding='latin')

label_text = t140[[0, 5]]

# Convert labels to range 0-1                                        
label_text[0] = label_text[0].apply(lambda x: 0 if x == 0 else 1)

# Assign proper column names to labels
label_text.columns = ['label', 'text']

# Assign proper column names to labels
label_text.head()


# Then we preprocess the text replacing hashtags and mentions with custom tokens, ensuring that the model won't overfit on them

# In[ ]:


import re

hashtags = re.compile(r"^#\S+|\s#\S+")
mentions = re.compile(r"^@\S+|\s@\S+")
urls = re.compile(r"https?://\S+")

def process_text(text):
  text = hashtags.sub(' hashtag', text)
  text = mentions.sub(' entity', text)
  return text.strip().lower()
  
def match_expr(pattern, string):
  return not pattern.search(string) == None

def get_data_wo_urls(dataset):
    link_with_urls = dataset.text.apply(lambda x: match_expr(urls, x))
    return dataset[[not e for e in link_with_urls]]


# In[ ]:


label_text.text = label_text.text.apply(process_text)


# We split the dataset and remove tweets with urls because we do not want them to change the meaning of the text, leading the model to learn wrong patterns. Then we store the datasets, because BERT need to load them from disk

# In[ ]:


from sklearn.model_selection import train_test_split
TRAIN_SIZE = 0.75
VAL_SIZE = 0.05
dataset_count = len(label_text)

df_train_val, df_test = train_test_split(label_text, test_size=1-TRAIN_SIZE-VAL_SIZE, random_state=42)
df_train, df_val = train_test_split(df_train_val, test_size=VAL_SIZE / (VAL_SIZE + TRAIN_SIZE), random_state=42)

print("TRAIN size:", len(df_train))
print("VAL size:", len(df_val))
print("TEST size:", len(df_test))


# In[ ]:


df_train = get_data_wo_urls(df_train)
df_train.head()


# In[ ]:


get_ipython().system('mkdir dataset')
df_train.sample(frac=1.0).reset_index(drop=True).to_csv('dataset/train.tsv', sep='\t', index=None, header=None)
df_val.to_csv('dataset/dev.tsv', sep='\t', index=None, header=None)
df_test.to_csv('dataset/test.tsv', sep='\t', index=None, header=None)
get_ipython().system(' cd dataset && ls')


# ## Model Training
# We cannot run this on Kaggle if we want to share this kernel as a notebook
# 

# In[ ]:


#from BertLibrary import BertFTModel
#import numpy as np


# In[ ]:


# !wget https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip
# !unzip uncased_L-12_H-768_A-12.zip


# In[ ]:


# !mkdir output
# ft_model = BertFTModel( model_dir='uncased_L-12_H-768_A-12',
#                         ckpt_name="bert_model.ckpt",
#                         labels=['0','1'],
#                         lr=1e-05,
#                         num_train_steps=30000,
#                         num_warmup_steps=1000,
#                         ckpt_output_dir='output',
#                         save_check_steps=1000,
#                         do_lower_case=False,
#                         max_seq_len=50,
#                         batch_size=32,
#                         )


# ft_trainer =  ft_model.get_trainer()
# ft_evaluator = ft_model.get_evaluator()


# In[ ]:


# ft_trainer.train_from_file('dataset', 35000)


# In[ ]:


# ft_evaluator.evaluate_from_file('dataset', checkpoint="output/model.ckpt-35000") 

