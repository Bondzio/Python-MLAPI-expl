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


import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import tensorflow.python.framework.dtypes


# In[ ]:


data_path = '/kaggle/input/Coral_cover_data.xlsx'


# In[ ]:


df = pd.read_excel(data_path)


# In[ ]:


df.Location.unique()


# In[ ]:


df1 = df[df.Location == "Florida_Keys"]    
df2 = df[df.Location == "French_Polynesia"] 
df3 = df[df.Location == "Main_Hawaiian_Islands"]
df4 = df[df.Location == "USVI"]


# In[ ]:


df1.shape,df2.shape,df3.shape,df4.shape


# In[ ]:


df1 = df1[df1.Percent_cover!=0.00]
df2 = df2[df2.Percent_cover!=0.00]
df3 = df3[df3.Percent_cover!=0.00]
df4 = df4[df4.Percent_cover!=0.00]


# In[ ]:


df1.shape,df2.shape,df3.shape,df4.shape


# In[ ]:





# In[ ]:


df1 = df1.sort_values(by=['Site_name','Taxon','Year'])


# In[ ]:


df1[:30]


# In[ ]:


df1.Sub_location.unique()


# In[ ]:


df1.Latitude.unique().min(), df1.Latitude.unique().max()


# In[ ]:


df1.Longitude.unique().max(), df1.Longitude.unique().min()


# In[ ]:


df1.Year.min(), df1.Year.max()


# In[ ]:


df1 = df1[(df1.Year>=1998) & (df1.Year<=2012)]


# In[ ]:


df1.shape

