#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns  

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
import os
print(os.listdir("../input"))
from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv('../input/globalterrorismdb_0718dist.csv',encoding='ISO-8859-1')


# In[ ]:


data.info()


# In[ ]:


data.corr()


# In[ ]:


f,ax = plt.subplots(figsize=(100 ,100))
sns.heatmap(data.corr(), ax=ax, annot = True)
plt.show()


# In[ ]:


data.head(10)


# In[ ]:


data['iyear'].value_counts()


# In[ ]:


data.columns


# In[ ]:


data.isnull().sum()


# In[ ]:


plt.figure(figsize=(16,6))
sns.heatmap(data.isnull(),cbar=False)


# In[ ]:


Turkey=data[(data['country_txt']=='Turkey')]
Turkey=Turkey[(Turkey['gname'] != 'Unknown')]
Turkey.tail()


# In[ ]:


pd.crosstab(Turkey[Turkey['gname'].isin(Turkey['gname'].
          value_counts()[0:8].index)]['iyear'],Turkey[Turkey['gname'].isin(Turkey['gname'].
                                                                          value_counts()[0:8].index)]
           ['gname']).plot(color=sns.color_palette('Paired', 10),figsize = (18,6))


# In[ ]:


b = data['region_txt']
df2= pd.DataFrame(b)


# In[ ]:


data['casualities']=data['nkill']+data['nwound']
a = data['attacktype1_txt'][data['casualities']==0.0].sort_values()
df = pd.DataFrame(a)
df['attacktype1_txt'].dropna(inplace = True)
df['attacktype1_txt'].value_counts()


# In[ ]:


df3 = pd.concat([df,df2],axis =1)
df3.dropna(inplace =True)
df3.head()


# In[ ]:




