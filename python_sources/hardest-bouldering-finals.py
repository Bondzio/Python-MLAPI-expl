#!/usr/bin/env python
# coding: utf-8

# # **Finding the hardest bouldering finals**
# #### Goal: I want to find out, which men bouldering final was the hardest. I will not be looking at youth competitions.

# <img src="https://live.staticflickr.com/65535/47568735262_d8573b06c0_h.jpg">

# ## Reading and formatting data

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


comps = pd.read_csv('/kaggle/input/ifsc-sport-climbing-competition-results/boulder_results.csv')
comps.head(7)


# In[ ]:


#Removing youth competitions
comps = comps[~comps['Competition Title'].str.contains('Youth')]

#Removing all non-finalists
comps = comps[~comps['Final'].isnull()]

#Removing all female competitors
#In each competition there are first listed females, then males
#They are ranked in order from 1 up
male = True
isMale = []
for index, climber in comps.iterrows():
    if climber['Rank'] == 1:
        male = not male
    isMale.append(male)
comps = comps[isMale]


# ## Computing mean values

# In[ ]:


#Adding columns with scores
comps['Tops'] = comps['Final'].str[0].astype(int)
comps['Bonus'] = comps['Final'].str[2].astype(int)
comps['Total'] = comps['Bonus'] + comps['Tops']

#Competition names
comps_unique = comps['Competition Title'].unique()

#Mean values of scores
comps_top_mean = pd.Series(index=comps_unique)
comps_bonus_mean = pd.Series(index=comps_unique)
comps_mean = pd.Series(index=comps_unique)

for comp in comps_unique:
    comp_results = comps[comps['Competition Title'] == comp]
    comps_top_mean[comp] = comp_results['Tops'].mean()
    comps_bonus_mean[comp] = comp_results['Bonus'].mean()
    comps_mean[comp] = comp_results['Total'].mean()


# # Visualising and looking at the results

# ### 1. Mean tops
# There were the least tops in Hachioji (2019), though in Honk Kong (2018), Zakopane (2019) and Hachioji (2018) had also very few tops on average in finals. 

# In[ ]:


from matplotlib import pyplot as plt
comps_top_mean.plot.bar(figsize=(13, 7), title = 'Mean Tops')


# ### 2. Mean bonuses
# Here we can see, that Honk Kong (2018) had the lowest average amount of tops. It was almost 2 times lower than most of the other finals.

# In[ ]:


comps_bonus_mean.plot.bar(figsize=(13, 7), title='Mean Bonuses')


# ### 3. Mean sum
# After analysing the mean sum of tops and bonues we can see, that the hardest finals were in Honk Kong in 2018.

# In[ ]:


comps_mean.plot.bar(figsize=(13, 7), title='Mean sum')


# # Honk Kong hardest, analysing the competition

# In[ ]:


# Honk Kong dataframe
hk_2018 = comps[comps['Competition Title'] == 'Asia Cup (B) - Hong Kong (HKG) 2018']
hk_2018['FullName'] = hk_2018['FIRST'] + ' ' + hk_2018['LAST']


# ### 1. Tops in Honk Kong
# We can see that only 3 finalists managed to top a problem.

# In[ ]:


hk_2018.plot.bar(x='FullName', y='Tops', figsize=(10, 5), rot = 0, legend = False, color = ('yellow', 'silver', 'brown', 'white', 'white'), edgecolor = 'black', title='Tops')


# ### 2. Bonuses
# Only 2 finalists maneged to reach 2 bonuses, the rest reached only 1 bonus.

# In[ ]:


hk_2018.plot.bar(x='FullName', y='Bonus', figsize=(10, 5), rot = 0, legend = False, color = ('yellow', 'silver', 'brown', 'white', 'white'), edgecolor = 'black', title='Bonuses')


# ### 3. Sum

# In[ ]:


hk_2018.plot.bar(x='FullName', y='Total', figsize=(10, 5), rot = 0, legend = False, color = ('yellow', 'silver', 'brown', 'white', 'white'), edgecolor = 'black', title = 'Sum')


# # Conlusion
# The hardest bouldering finals were in Honk Kong in 2018. Although it was second in terms of least reached tops, it had the least reached bonuses. It also had the lowest sum of tops and bonuses. Only three finalists were able to top a boulder. 
