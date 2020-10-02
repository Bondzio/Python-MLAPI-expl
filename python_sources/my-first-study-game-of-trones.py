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


import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


data = pd.read_csv('../input/battles.csv')
data_cd = pd.read_csv('../input/character-deaths.csv')
data_cp = pd.read_csv('../input/character-predictions.csv') 


# In[ ]:


data.info()


# In[ ]:


data.corr()


# In[ ]:


f,ax = plt.subplots(figsize=(15,15))
sns.heatmap(data.corr(), annot = True,ax=ax)
plt.show()


# In[ ]:


data.head()


# In[ ]:


data.columns


# **i am wondering what is the comparison between death rate and capture rate**

# In[ ]:


data.major_death.plot(color = "red", label = "major_death",grid = True, linestyle = ':')
data.major_capture.plot(color = "green", label = "major_capture",grid = True, linestyle = '-.')
plt.legend()
plt.xlabel("major_death")
plt.ylabel("major_capture")
plt.title("death_capture_comparison")
plt.show()


# In[ ]:


data.plot(kind ='scatter', x='major_death', y='major_capture', alpha = 0.5, color='red')
plt.xlabel('major_death')
plt.ylabel('major_capture')
plt.title('death_capture_comparison')
plt.show()


# **but as i saw no more correlation between death and capture rates **

# In[ ]:


data.plot(kind ='scatter', x='attacker_size', y='defender_size', alpha = 0.5, color='red')
plt.xlabel('attacker_size')
plt.ylabel('defender_size')
plt.title('attacker_and_defender_size_comparison')
plt.show()


# In[ ]:


data.major_death.plot(kind = "hist", color ="r", bins=50, figsize=(10,10), grid = True)
plt.show()


# In[ ]:


data_cd.columns


# In[ ]:


data_cd.columns = [each.split()[0]+"_"+each.split()[1] if(len(each.split())>1) else each for each in data_cd.columns]


# In[ ]:


data_cd.columns


# In[ ]:


data_cd.Death_Chapter.plot(kind = "hist", color ="r", bins=30, figsize=(10,10), grid = True)
plt.title('Death_Chapter')
plt.xlabel('Death_Chapter')
plt.ylabel('how many death')
plt.show()


# In[ ]:


type(data)
series = data["major_death"]
print(type(series))
data_frame = data[["major_death"]]
print(type(data_frame))


# In[ ]:


data.head(15)


# In[ ]:


#i want to learn wich one is the bigest war and i use two filter
filter1 = data['attacker_size'] > 10000
filter2 = data['defender_size'] > 10000
data[filter1 & filter2]


# In[ ]:


print(data['attacker_outcome'])


# In[ ]:


data[(data['attacker_outcome'] == "loss")]

