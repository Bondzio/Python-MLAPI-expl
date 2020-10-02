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
import matplotlib.pyplot as plt
print(os.listdir("../input"))
df = pd.read_csv('../input/MOP_installed_capacity_sector_mode_wise.csv')
# Any results you write to the current directory are saved as output.


# In[ ]:


df.info()


# In[ ]:


df.State.unique()


# In[ ]:


df.columns


# In[ ]:


df.Mode.unique()


# In[ ]:


df[df.Mode == "Thermal"]['Installed Capacity'].sum()


# In[ ]:


#States with total installed capacity
State_wise = df.groupby(['State']).sum().reset_index()


# In[ ]:


#Total Installed Capacity
df['Installed Capacity'].sum()


# In[ ]:


State_wise[State_wise['Installed Capacity'] == State_wise['Installed Capacity'].max()]


# In[ ]:


State_wise.sort_values('Installed Capacity', ascending = [False])


# In[ ]:


plt.bar(State_wise.State, State_wise['Installed Capacity'])


# In[ ]:


#top 5 states
State_wise.sort_values('Installed Capacity', ascending = [False])[:5]


# In[ ]:


State_mode = df.groupby(['State','Mode']).sum().reset_index()


# In[ ]:


#Top 5 states in Thermal mode
State_mode[State_mode.Mode == 'Thermal'].sort_values('Installed Capacity', ascending = [False])[:5]


# In[ ]:


#Top 5 states in Nuclear Mode
State_mode[State_mode.Mode == 'Nuclear'].sort_values('Installed Capacity', ascending = [False])[:5]


# In[ ]:


#Top 5 states in Hydro mode
State_mode[State_mode.Mode == 'Hydro'].sort_values('Installed Capacity', ascending = [False])[:5]


# In[ ]:


#Top 5 states in RES mode
State_mode[State_mode.Mode == 'RES'].sort_values('Installed Capacity', ascending = [False])[:5]


# In[ ]:




