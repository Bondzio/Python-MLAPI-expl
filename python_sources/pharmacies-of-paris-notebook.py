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
        path = os.path.join(dirname, filename)

# Any results you write to the current directory are saved as output.


# In[ ]:


import pandas as pd

df = pd.read_csv(path)
df.head


# In[ ]:


locations = df[['lng', 'lat']]
locationlist = locations.values.tolist()
len(locationlist)
locationlist[7]


# In[ ]:


import folium
map = folium.Map(location=[ 48.864716, 2.349014], zoom_start=12)
for point in range(0, len(locationlist)):
    folium.Marker(locationlist[point], popup=df['rs'][point]).add_to(map)
map


# In[ ]:


from folium.plugins import MarkerCluster

some_map = folium.Map(location=[48.864716, 2.349014], zoom_start=12)
mc = MarkerCluster()
for point in range(0, len(locationlist)):
    mc.add_child(folium.Marker(locationlist[point], popup=df['rs'][point]))
 
some_map.add_child(mc)
some_map


# In[ ]:




