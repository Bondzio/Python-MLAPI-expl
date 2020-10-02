#!/usr/bin/env python
# coding: utf-8

# # Introduction
#    This notebook is about plotting data on map. The language data from WALS dataset is used to plot the languages spoken in and around India grouped by their family.
#    
#    This notebook is beginner level with just five code cells. 

# In[ ]:


import os

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # plotting
import seaborn as sns

from mpl_toolkits.basemap import Basemap

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# # Reading data

# In[ ]:


df = pd.read_csv("../input/wals-dataset/language.csv",
                 usecols=['Name','family','latitude','longitude'])
df


# # Getting the Regional data

# In[ ]:


#Function to get the region with the bounding latitudes and longitudes
def get_region(data,bot_lat, left_lon, top_lat, right_lon):
    '''Gets the data within the region givenby the corner latitude and longitude.
    data = Dataframe from where the regional data has to be taken.
    reg = (Lower Latitude, Left Longitude, Top Latitude, Right Longitude)
    '''
    top = data.latitude <= top_lat
    bot = data.latitude >= bot_lat
    left = data.longitude >= left_lon
    right = data.latitude <= right_lon
    
    index = top&bot&left&right 
    return df[index]
    

india_lang = get_region(df,5,60,40,100)
india_lang


# # Plotting family of the languages
# 
#    We will here be interested in Grouping the languages based on the family they belong.

# In[ ]:


india_lang.family.value_counts()


# In[ ]:


fam_map = Basemap(urcrnrlat=40,llcrnrlat=5,llcrnrlon=60,urcrnrlon=100)

plt.figure(figsize=(12,10))
fam_map.bluemarble(alpha=0.9)
sns.scatterplot(x='longitude', y='latitude', hue = 'family', data =india_lang)

plt.title("Languages of India by Language Groups")
plt.show()


#  Comments are most welcomed!
# 
# Ref:
# https://www.kaggle.com/averkij/wals-dataset-on-the-map/notebook
