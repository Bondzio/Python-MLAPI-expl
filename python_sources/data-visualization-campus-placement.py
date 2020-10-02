#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt 
import seaborn as sns

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


df=pd.read_csv('../input/factors-affecting-campus-placement/Placement_Data_Full_Class.csv')


# In[ ]:


df.info()


# In[ ]:


df.head()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


df['hsc_b'].notnull


# In[ ]:


sns.countplot(x='gender',data=df)


# In[ ]:


sns.countplot(x='ssc_b',hue='gender',data=df)


# In[ ]:


sns.countplot(x='hsc_s',hue='gender',data=df)


# In[ ]:


sns.countplot(x = 'degree_t', hue='gender',data = df)


# In[ ]:


sns.scatterplot(x = 'ssc_p', y = 'status', data = df)


# In[ ]:


sns.scatterplot(x = 'hsc_p', y = 'status', data = df)


# In[ ]:


sns.scatterplot(x = 'ssc_p', y = 'status', data = df)


# In[ ]:


sns.scatterplot(x = 'mba_p', y = 'status', data = df)


# In[ ]:


sns.countplot(x='specialisation',hue='status',data=df)


# In[ ]:


sns.countplot(x='workex',hue='status',data=df)


# In[ ]:




