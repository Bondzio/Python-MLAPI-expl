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


# In[ ]:


get_ipython().system('ls -al /kaggle/input/flower_data/flower_data/train/87/')


# In[ ]:


import PIL
import PIL.Image


# In[ ]:


path = '/kaggle/input/flower_data/flower_data/train/87/'
filename = 'image_05519.jpg'
pf = path+filename

PIL.Image.open(pf)


# In[ ]:




