#!/usr/bin/env python
# coding: utf-8

# # Introduction
# Hi! 
# 
# WritingPrompts dataset consists of two separated files , i.e. "prompts" and "stories". 
# 
# To be able to finetune using HuggingFace GPT-2, we will combine this two files into 1, and still use 1 line-by-line basis.
# Also, as recommended by FAIR, we will truncated the stories to only first 1,000 words

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


DIR = "/kaggle/input/writing-prompts/writingPrompts/"
data = [DIR+"train", DIR+"test", DIR+"valid"]

TARGET_DIR = '/kaggle/working/'
target_data = [TARGET_DIR+"train", TARGET_DIR+"test", TARGET_DIR+"valid"]


# In[ ]:


from tqdm import tqdm_notebook as tqdm

NUM_WORDS = 300 # originally, FAIR use 1000, but here I use 300 just to be able to train distilgpt2 quickly

for name_id in tqdm(range(len(data))):
    fp = open(data[name_id] + ".wp_source") 
    ft = open(data[name_id] + ".wp_target") 
    
    stories = ft.readlines()
    prompts = fp.readlines()
    
    assert len(prompts) == len(stories)
    
    new_stories = [prompts[i].rstrip()+ " <endprompts> " + " ".join(stories[i].split()[0:NUM_WORDS]) for i in range(len(stories))]
    
    
    with open(target_data[name_id] + ".wp_combined", "w") as o:
        for line in new_stories:
            o.write(line.strip() + "\n")
        print('finish writing',target_data[name_id] + ".wp_combined")
    
    fp.close()
    ft.close()


# In[ ]:


get_ipython().system('ls -sh')


# We can now directly use the generated files for GPT2 finetuning

# In[ ]:


get_ipython().system('head train.wp_combined')
get_ipython().system('head test.wp_combined')


# In[ ]:




