#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install tokenize_uk')
get_ipython().system('pip install utils')
get_ipython().system('pip install colorama')


# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import math
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from utils import *
import tokenize_uk
from colorama import Fore, Back, Style

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


files = ['/kaggle/input/ukrainian-texts/Lys_mykyta.txt', '/kaggle/input/ukrainian-texts/Lisova_pisnya_1371650989.txt']
files


# In[ ]:


for src_file in files:
    with open(src_file, 'rb') as f:
        data = f.read()
    text = data.decode('utf-8')
    tokens_text = tokenize_uk.tokenize_sents(text)
tokens_text


# In[ ]:


len(tokens_text)


# In[ ]:


tokens_text[0]


# In[ ]:


tokens_text[897]


# THE END
