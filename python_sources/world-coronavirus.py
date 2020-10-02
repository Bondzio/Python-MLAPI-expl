#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point,Polygon

import folium
from folium import Choropleth, Circle, Marker
from folium.plugins import HeatMap, MarkerCluster

import requests 


# **World CoronaData**

# In[ ]:


URL = "https://coronavirus-tracker-api.herokuapp.com/v2/locations"


# In[ ]:


# sending get request and saving the response as response object 
r = requests.get(url = URL) 

# extracting data in json format 
data = r.json() 


# In[ ]:


asian_countries = [ 'Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Bhutan, Brunei', 'Burma,Cambodia',
                   'China', 'East Timor', 'Georgia', 'Hong Kong','India', 'Indonesia', 'Iran', 'Iraq','Israel', 'Japan', 
                   'Jordan', 'Kazakhstan', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Lebanon', 'Malaysia', 'Mongolia', 'Nepal', 
                   'North Korea', 'Oman', 'Pakistan', 'Papua New Guinea', 'Philippines', 'Qatar', 'Russia', 
                   'Saudi Arabia', 'Singapore', 'South Korea', 'Sri Lanka', 'Syria', 'Taiwan', 'Tajikistan', 
                   'Thailand', 'Turkey', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'Vietnam', 'Yemen']


# In[ ]:


south_asian = ['Sri Lanka', 'India', 'Bangladesh', 'Bhutan', 'Nepal', 'Pakistan','Maldives']
empty_list = []


# In[ ]:


coordintes_confirmed = []
for values in data['locations']:
    country = values['country']
    latitude = float((values['coordinates'])['latitude'])
    longitude = float((values['coordinates'])['longitude'])
    confirmed = int((values['latest'])['confirmed'])
    coordintes_confirmed.append((country,latitude,longitude,confirmed))


# **Make Pandas DataFrame from the list**

# In[ ]:


world_frame = pd.DataFrame(coordintes_confirmed, columns=['Country', 'Latitude', 'Longitude', 'Confired_Cases'])


# In[ ]:


world_frame


# In[ ]:


world_frame = world_frame.reindex(world_frame.index.repeat(world_frame.Confired_Cases))


# In[ ]:


world_frame_ = world_frame.copy()


# In[ ]:


nepal_frame = world_frame[world_frame.Country == 'Nepal']


# In[ ]:


world_frame.head()


# **Convert DataFrame to GeoDataFrame**

# In[ ]:


geometry = [Point(xy) for xy in zip(world_frame.Latitude, world_frame.Longitude)]
world_frame = world_frame.drop(['Latitude','Longitude', 'Confired_Cases'], axis = 1)
crs = {'init' : 'epsg:4326'}
gdf_world = GeoDataFrame(world_frame, crs=crs, geometry=geometry)


# In[ ]:


gdf_world.head(2)


# **Preprocessing for Choropleth maps**

# In[ ]:


gdf_world_indexed = gdf_world.set_index('Country')


# **Count No of Confirmed in each Country**

# In[ ]:





# In[ ]:


plot_dict = gdf_world.Country.value_counts()
plot_dict.head()


# In[ ]:


#read world map shape file
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))


# In[ ]:


nepal = world.loc[world['name'].isin(['Nepal'])]
nepal['geometry']


# **Plotting Nepal **

# In[ ]:


ax = nepal.plot(figsize=(10,10), color='None', edgecolor='gainsboro')


# ****SouthAsia Map Follium: Memory Heavvy**

# In[ ]:


#m_1 = folium.Map(location=[25.0376,76.4563],tiles='cartodbpositron', zoom_start=8)


# Add a choropleth map to the base map
#Choropleth(geo_data=gdf_world_indexed.__geo_interface__, 
  #         data=plot_dict, 
   #        key_on="feature.id", 
    #       fill_color='YlGnBu', 
     #      legend_name='World CoronaVirus Confirmed Case'
      #    ).add_to(m_1)

# Display the map#
#m_1


# **HeatMap World**

# In[ ]:


# Create a base map
m_2 = folium.Map(location=[25.0376,76.4563], tiles='openstreetmap', zoom_start=2)

# Add a heatmap to the base map
HeatMap(data=world_frame_[['Latitude', 'Longitude']], radius=10).add_to(m_2)

# Display the map
m_2


# In[ ]:


m_2


# **MarkerCluster HeatMap**

# In[ ]:


#import math


# In[ ]:


#m_3 = folium.Map(location=[25.0376,76.4563], tiles='openstreetmap', zoom_start=3)

# Add points to the map
#mc = MarkerCluster()
#for idx, row in world_frame_.iterrows():
#    if not math.isnan(row['Longitude']) and not math.isnan(row['Latitude']):
#        mc.add_child(Marker([row['Longitude'], row['Latitude']]))
#m_3.add_child(mc)

# Display the map
#m_3


# In[ ]:




