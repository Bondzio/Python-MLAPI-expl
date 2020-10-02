#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import os

import matplotlib.pyplot as plt
import folium

# for dirname, _, filenames in os.walk('/kaggle/input/uncover/hifld'):
for dirname, _, filenames in os.walk('/kaggle/input/uncover/'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


df = pd.read_csv('../input/uncover/hifld/hifld/hospitals.csv')


# In[ ]:


df.head()


# In[ ]:


df.describe(include='all')


# In[ ]:


# replace missing indicator -999 by 0
df.beds[df.beds==-999] = 0
df.beds.describe()


# In[ ]:


# count hospitals and beds by state
df_state_stats = df.groupby('state').agg(
                    n = pd.NamedAgg(column='id', aggfunc='count'),
                    beds = pd.NamedAgg(column='beds', aggfunc='sum'))
df_state_stats['average_beds'] = df_state_stats.beds / df_state_stats.n
df_state_stats


# In[ ]:


n = df.shape[0]
print('Number of hospitals: ', n)


# ### Display all hospitals on map; bubble size ~ number of beds

# In[ ]:


lat = 37
lon = -90
m = folium.Map([lat, lon], zoom_start=4)

for i in range(0,n):
   folium.Circle(
      location=[df.latitude.iloc[i], df.longitude.iloc[i]],
      popup=df.name.iloc[i] + " - number of beds:" + str(df.beds.iloc[i]),
      radius=250.0*np.sqrt(df.beds.iloc[i]),
      color='red',
      fill=True,
      fill_color='red'
   ).add_to(m)

# show map
m


# ### Look at state New York

# In[ ]:


df_NY = df[df.state=='NY']


# In[ ]:


df_NY.describe()


# In[ ]:


n_NY = df_NY.shape[0]
print(n_NY)


# In[ ]:


lat = 42
lon = -72
m = folium.Map([lat, lon], zoom_start=7)

for i in range(0,n_NY):
   folium.Circle(
      location=[df_NY.latitude.iloc[i], df_NY.longitude.iloc[i]],
      popup=df_NY.name.iloc[i] + " - number of beds:" + str(df_NY.beds.iloc[i]),
      radius=100.0*np.sqrt(df_NY.beds.iloc[i]),
      color='red',
      fill=True,
      fill_color='red'
   ).add_to(m)

# show map
m


# ### Look at city New York

# In[ ]:


df_NYC = df[df.city=='NEW YORK']


# In[ ]:


df_NYC.describe()


# In[ ]:


n_NYC = df_NYC.shape[0]
print(n_NYC)


# In[ ]:


lat = 40.8
lon = -74
m = folium.Map([lat, lon], zoom_start=11)

for i in range(0,n_NYC):
   folium.Circle(
      location=[df_NYC.latitude.iloc[i], df_NYC.longitude.iloc[i]],
      popup=df_NYC.name.iloc[i] + " - number of beds:" + str(df_NYC.beds.iloc[i]),
      radius=10.0*np.sqrt(df_NYC.beds.iloc[i]),
      color='red',
      fill=True,
      fill_color='red'
   ).add_to(m)

# show map
m

