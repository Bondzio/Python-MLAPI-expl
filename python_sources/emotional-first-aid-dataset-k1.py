#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install efaqa-corpus-zh')


# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import efaqa_corpus_zh

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os

corpus = list(efaqa_corpus_zh.load())
print("size: %s" % len(corpus))
print(corpus[0]["title"])

# Any results you write to the current directory are saved as output.


# In[ ]:




