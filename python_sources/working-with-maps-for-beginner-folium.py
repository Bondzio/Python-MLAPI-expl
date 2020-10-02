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


# **Creating a map**

# In[ ]:


import folium

# Create map object 
m=folium.Map(location=[42.3601,-71.0589],zoom_start=12)
m
#Generate map
#m.save('map.html')


# **Creating a marker **

# In[ ]:


# Global tooltip 
tooltip='Click for more info'

# Create marker 
folium.Marker([42.36,-71.09],popup='<strong>Location One</strong>',tooltip=tooltip).add_to(m)
m


# **Creating an icon**

# In[ ]:


folium.Marker([42.33,-71.10],popup='<strong>Location One</strong>',tooltip=tooltip,icon=folium.Icon(icon='cloud')).add_to(m)
m


# **Changing color **

# In[ ]:


folium.Marker([42.37,-71.06],popup='<strong>Location One</strong>',tooltip=tooltip,icon=folium.Icon(color='purple')).add_to(m)
m


# **Creating marker with Green Leaf icon**

# In[ ]:


folium.Marker([42.33,-71.04],popup='<strong>Location One</strong>',tooltip=tooltip,icon=folium.Icon(icon='leaf',color='green')).add_to(m)
m


# **Creating a custom icon **

# In[ ]:


logoIcon=folium.features.CustomIcon('../input/Sophia.jpg',icon_size=(50,50))
folium.Marker([42.40,-71.09],popup='<strong>Location Five</strong>',tooltip=tooltip,icon=logoIcon).add_to(m)
m


# **Making a circle marker **

# In[ ]:


folium.CircleMarker(location=[42.37,-71.10],radius=50,popup='My Birthplace',color='#428bca',fill=True,fill_color='#428bca').add_to(m)
m


# **Marking travel path using Folium:**
# The cordinates of travel path can be found out from the http://geojson.io website. We create a travel path file from here 

# In[ ]:




