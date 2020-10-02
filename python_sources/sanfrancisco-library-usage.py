#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# # San fransisco library usage 
# 
# 
# Data :https://www.kaggle.com/datasf/sf-library-usage-data?select=Library_Usage.csv
# 

# In[ ]:


#import necessary packages
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


# In[ ]:


Data=pd.read_csv("/kaggle/input/sf-library-usage-data/Library_Usage.csv")


# In[ ]:


Data.head()


# In[ ]:


Data.columns


# In[ ]:


#x=Data['Age Range']
#y=Data['Total Checkouts']

#r = np.corrcoef(x,y)
#print(r)

sns.heatmap(Data.corr())


# In[ ]:


columnTransformer = ColumnTransformer([('encoder', 
                                        OneHotEncoder(), 
                                        [0])], 
                                      remainder='passthrough') 
onehotencoder = OneHotEncoder() 
  
data = np.array(columnTransformer.fit_transform(Data), dtype = np.str)


# In[ ]:


data

