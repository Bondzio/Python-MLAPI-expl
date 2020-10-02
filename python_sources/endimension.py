#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
import matplotlib.pyplot as plt
from skimage import io
import skimage.external.tifffile as ti

# Any results you write to the current directory are saved as output.


# # Preprocessing Stage

# In[ ]:





# In[2]:


def visualize(current):
    Y = os.listdir(current)
    ims = ti.imread(Y)
    ti.imshow(ims)


# In[3]:


dir="/kaggle/input/sample_dataset_for_testing/sample_dataset_for_testing/fullsampledata"


# In[4]:


j = os.listdir(dir);j


# In[6]:


for i in j:
    t = os.path.join(dir,i) ##till subset3mask
    print(t)
    k = os.listdir(t)      ##will show 1..3.3.33..3 wala thing
    y = os.path.join(t,k[0])
    print(y)
    current = y
    visualize(current)
    


# In[7]:


def imgshow(foldername,filename):
    iaddress  = os.path.join(dir,foldername)
    cc = os.listdir(iaddress)
    ffad = os.path.join(iaddress,cc[0],filename)
    f =ti.imread(ffad)
    ti.imshow(f)


# In[8]:


import warnings
warnings.filterwarnings("ignore")


# In[10]:


imgshow("subset3mask","139.tiff")


# In[ ]:





# # Post visualization

# In[ ]:




