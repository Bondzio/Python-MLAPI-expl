#!/usr/bin/env python
# coding: utf-8

# In[4]:


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


# In[5]:


import bq_helper


# In[6]:


# create a helper object for our bigquery dataset
hacker_news = bq_helper.BigQueryHelper(active_project= "bigquery-public-data", 
                                       dataset_name = "noaa_gsod.gsod")


# In[7]:


# print a list of all the tables in the hacker_news dataset
noaa_gsod.gsod.list_tables()


# In[ ]:




