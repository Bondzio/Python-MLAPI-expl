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
from matplotlib import pylab
import seaborn as sns

import matplotlib.pyplot as plt
noShow = pd.read_csv('../input/KaggleV2-May-2016.csv')
print(noShow.head())
# Any results you write to the current directory are saved as output.


# In[ ]:


noShow.info


# In[ ]:


noShow.describe()


# In[ ]:


noShow.info()


# In[ ]:


new_col_name = ['patient_id', 'appointment_id','gender','schedule_day','appointment_day','age','neighborhood',
               'scholarship','hypertension','diabetes','alcoholism','handicap',
               'sms_received','no_show']
noShow.columns = new_col_name


# In[ ]:


noShow.isnull().sum()


# In[ ]:


noShow.dtypes


# In[ ]:


noShow['appointment_day']=pd.to_datetime(noShow['appointment_day'])
noShow['schedule_day']=pd.to_datetime(noShow['schedule_day'])        


# Age has outliers!

# In[ ]:


noShow.age.min()


# In[ ]:


noShow.age.max()


# In[ ]:


plt.hist(noShow['age'],color = 'blue', edgecolor = 'black',
         bins = int(180/5))


# In[ ]:


noShow.scholarship.min()      


# In[ ]:


noShow.scholarship.max()      


# In[ ]:


plt.hist(noShow['scholarship'],color = 'blue', edgecolor = 'black',
         bins = int(180/5))


# In[ ]:


plt.hist(noShow['hypertension'],color = 'blue', edgecolor = 'black')

