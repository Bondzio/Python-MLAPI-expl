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


data = pd.read_csv('../input/world-billionaires/billionaires.csv')


# In[ ]:


data.head()


# In[ ]:


data['net_worth'] =  data['net_worth'].astype('float16')


# In[ ]:


data.info(memory_usage='deep')


# In[ ]:


data.describe().transpose()


# In[ ]:


###import plotting library
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


##boxplots used for detecting outliers

for col in data.select_dtypes(include=['int64','float16']).columns:
    data[[col]].boxplot()
    plt.show()


# In[ ]:


##distribution of age

##how billionaires under 30 have changed over the years
for i in data['year'].unique().tolist()[::-1]:
    sns.kdeplot(data.loc[data['year'] == i,'age']).set_title(i)
#     plt.title("Year : ",i)
    plt.show()


# In[ ]:


data['year'].unique().tolist()[::10]


# In[ ]:


data.sort_values(by = ['net_worth']).groupby('year').min()

