#!/usr/bin/env python
# coding: utf-8

# Earthquakes From 1965 to 2016

# In[15]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))


# In[16]:


from pandas import DataFrame
from pandas import Series
import matplotlib.pyplot as plt
earthquake_data = pd.read_csv("../input/database.csv")
earthquake_data.shape


# In[17]:


latitude_list=[]
longitude_list=[]
for row in earthquake_data.Latitude:
     latitude_list.append(row)
for row in earthquake_data.Longitude:
    longitude_list.append(row)
    


# In[18]:


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


# In[19]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[20]:


earthquake_map = Basemap(projection='robin', lat_0=-90,lon_0=130,resolution='c', area_thresh=1000.0)


# In[21]:


earthquake_map.drawcoastlines()
earthquake_map.drawcountries()
earthquake_map.drawmapboundary()
earthquake_map.bluemarble()
earthquake_map.drawstates()
earthquake_map.drawmeridians(np.arange(0, 360, 30))
earthquake_map.drawparallels(np.arange(-90, 90, 30))

x,y = earthquake_map(longitude_list, latitude_list)
earthquake_map.plot(x, y, 'ro', markersize=1)
plt.title("Locations where EarthQuakes,Rock Bursts & NuclearExplosions happened between 1965 to 2016")
 
plt.show()


# In[22]:


g8 = earthquake_data[earthquake_data['Magnitude'] > 6.5]
g8['Location Source'].value_counts()


# In[23]:



plt.hist(earthquake_data['Magnitude'])
plt.xlabel('Magnitude Size')
plt.ylabel('Number of Occurrences')


# Magnitude Type
# Magnitudes can be based on any of the following:
# ML: Local (Richter) magnitude
# MS: surface wave magnitude scale
# MB (Mb): Body wave magnitude scale
# MW (Mw): Moment magnitude scale
# MD (Md): Duration magnitude/signal duration
# MWC: ?
# MWW: ? 
# MWR: ?
# MH: ?

# In[24]:


import seaborn as sns
sns.countplot(x="Magnitude Type",data=earthquake_data)
plt.ylabel('Frequency')
plt.title('Magnitude Type vs Frequency')


# In[25]:


import datetime
earthquake_data['date']=earthquake_data['Date'].apply(lambda x: pd.to_datetime(x))


# In[26]:


earthquake_data['year']=earthquake_data['date'].apply(lambda x:str(x).split('-')[0])


# In[27]:



plt.figure(figsize=(25,8))
sns.set(font_scale=1.0)
sns.countplot(x="year",data=earthquake_data)
plt.ylabel('Number of Earthquakes')
plt.xlabel('Number of Earthquakes in each year')


# In[28]:


earthquake_data['year'].value_counts()[::-1]


# In[30]:


x=earthquake_data['year'].unique()
y=earthquake_data['year'].value_counts()
count=[]
for i in range(len(x)):
    count.append(y[x[i]])

plt.figure(figsize=(10,8))    
plt.scatter(x,count)
plt.xlabel('Year')
plt.ylabel('Number of earthquakes')
plt.title('Earthquakes between 1965 to 2016')
plt.show()


# Relation between Magnitude of earthquake and depth 

# In[32]:


plt.scatter(earthquake_data["Magnitude"],earthquake_data["Depth"])


# In[ ]:




