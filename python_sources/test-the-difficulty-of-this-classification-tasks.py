#!/usr/bin/env python
# coding: utf-8

# * Borrowed the idea from a super cool paper from CoNLL 2018: 
# Evolutionary Data Measures: Understanding the Difficulty of Text Classification Tasks
# 
# * Paper: https://arxiv.org/abs/1811.01910
# * Code: https://github.com/Wluper/edm

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


train_df = pd.read_csv("../input/train.csv")
df = train_df.sample(frac=0.02)
sents = df["question_text"].fillna("_##_").values
labels = df["target"].values


# In[ ]:


from edm import report
print(report.get_difficulty_report(sents, labels))

