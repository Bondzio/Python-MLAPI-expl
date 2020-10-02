#!/usr/bin/env python
# coding: utf-8

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


data_path = '/kaggle/input/AOML_1998_2012_shipboard_survey_Data_File.xls'


# In[ ]:


df = pd.read_excel(data_path,'Database')


# In[ ]:


df.head()


# In[ ]:


df.Date[0].strftime("%Y")


# In[ ]:


df.Date = df.Date.apply(lambda x: x.strftime("%Y"))


# In[ ]:


df.head()


# In[ ]:


df = df.drop(['GMT'], axis=1)


# In[ ]:


df.Latitude.unique().shape


# In[ ]:





# In[ ]:


df = df[(df.Latitude>=24.4517) & (df.Latitude<=25.295) & (df.Longitude>=-83.0022) & (df.Longitude<=-80.2093)]


# In[ ]:


df.head()


# In[ ]:


temp_df = df.groupby('Date')['SST','SSS','Chl a'].mean()
temp_df


# In[ ]:


df.Date.min(), df.Date.max()

