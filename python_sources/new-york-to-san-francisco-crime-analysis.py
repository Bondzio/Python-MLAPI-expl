#!/usr/bin/env python
# coding: utf-8

# ![](https://wp.zillowstatic.com/streeteasy/2/SF_vs_NYC-v2-10a7b4.jpg)

# 

# In[ ]:


#import the libraries we need
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import matplotlib.pyplot as plt
import seaborn as sns
import folium
print(os.listdir("../input"))


# Load the dataset using pandas.

# In[ ]:


data = pd.read_csv('../input/san-francisco-crime-data/Police_Department_Incident_Reports__2018_to_Present.csv')


# In[ ]:


data.shape


# In[ ]:


data.describe()


# In[ ]:


data.head()


# In[ ]:


data.columns = data.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')


# Since the geoJSON has the District values in upper case we convert to uppercase as well.

# In[ ]:


data['Police_District'] = data['Police_District'].str.upper() 


# Now, since I know the structure and the various features of the data, I can easily generate plots for it.

# In[ ]:


data.isnull().sum()
# there are a lot of null values in the data


# Let's clean the data and give a value'NaN' for the empty entries.

# In[ ]:


new_df = data.fillna({
    'CAD_Number' : 'NaN',
    'Filed_Online' : 'NaN',
    'Incident_Subcategory' : 'NaN',
    'Incident_Category' : 'NaN',
    'CNN' : 'NaN',
    'Intersection' : 'NaN',
    'Analysis_Neighborhood' : 'NaN',
    'Supervisor_District' : 'NaN',
    'Latitude' : 'NaN',
    'Longitude' : 'NaN',
    'point' : 'NaN',
    'SF_Find_Neighborhoods' : 'NaN',
    'Current_Police_Districts' : 'NaN',
    'Current_Supervisor_Districts' : 'NaN',
    'Analysis_Neighborhoods' : 'NaN',
    'HSOC_Zones_as_of_2018-06-05' : 'NaN',
    'OWED_Public_Spaces' : 'NaN',
    'Central_Market/Tenderloin_Boundary_Polygon_-_Updated' : 'NaN',
    'Parks_Alliance_CPSI_27+TL_sites' : 'NaN',
})


# In[ ]:


#Check
new_df.isnull().sum()


# Let's make a word cloud to see the most frequently occuring crimes.

# In[ ]:


from wordcloud import WordCloud

plt.rcParams['figure.figsize'] = (10, 8)
plt.style.use('bmh')
wc = WordCloud(background_color = 'pink', width = 1500, height = 1500).generate(str(data['Incident_Description']))
plt.imshow(wc)
plt.axis('off')
plt.show()


# ## Visualizations

# In[ ]:


plt.rcParams['figure.figsize'] = (19, 8)
plt.style.use('ggplot')

sns.countplot(data['Incident_Category'], palette = 'gnuplot')
plt.title('Crime Category Analysis', fontweight = 30, fontsize = 20)
plt.xticks(rotation = 90)
plt.show()


# In[ ]:


plt.rcParams['figure.figsize'] = (20, 9)
plt.style.use('seaborn-bright')
sns.countplot(data['Incident_Day_of_Week'], palette = 'gnuplot')
plt.title('Crime Analysis Day wise', fontweight = 30, fontsize = 20)
plt.xticks(rotation = 90)
plt.show()


# In[ ]:


plt.rcParams['figure.figsize'] = (20, 9)
plt.style.use('Solarize_Light2')
sns.countplot(data['Police_District'], palette = 'gnuplot')
plt.title('Crime Analysis based on District', fontweight = 30, fontsize = 20)
plt.xticks(rotation = 90)
plt.show()


# In[ ]:



plt.rcParams['figure.figsize'] = (20, 9)
plt.style.use('Solarize_Light2')

color = plt.cm.ocean(np.linspace(0, 1, 15))
data['Intersection'].value_counts().head(10).plot.bar(color = color)

plt.title('Top Intersections in Crime',fontsize = 20)
plt.xticks(rotation = 90)
plt.show()


# In[ ]:


plt.rcParams['figure.figsize'] = (20, 9)
plt.style.use('seaborn')
sns.countplot(data['Resolution'])
plt.title('Case Status', fontweight = 30, fontsize = 20)
plt.xticks(rotation = 90)
plt.show()


# In[ ]:


import warnings
warnings.filterwarnings('ignore')

color = plt.cm.twilight(np.linspace(0, 5, 100))
data['Incident_Time'].value_counts().head(20).plot.line(figsize = (15, 9))
plt.title('Distribution of crime over the day', fontsize = 20)
plt.show()


# In[ ]:


#line graph
df = pd.crosstab(data['Incident_Category'], data['Police_District'])
color = plt.cm.Greys(np.linspace(0, 1, 10))
df.div(df.sum(1).astype(float), axis = 0).plot.line(stacked = True,figsize = (18, 12))
plt.title('District vs Category of Crime', fontweight = 30, fontsize = 20)
plt.xticks(rotation = 90)
plt.show()


# In[ ]:


#bar graph
df = pd.crosstab(data['Incident_Category'], data['Police_District'])
color = plt.cm.Greys(np.linspace(0, 1, 10))
df.div(df.sum(1).astype(float), axis = 0).plot.bar(color=color, stacked = True,figsize = (18, 12))
plt.title('District vs Category of Crime', fontweight = 30, fontsize = 20)
plt.xticks(rotation = 90)
plt.show()


# In[ ]:


t = new_df.Police_District.value_counts()


# In[ ]:


t


# In[ ]:


#Creatiing a data frame to get the geospatial distribution based on district
t = data.Police_District.value_counts()
dist= pd.DataFrame(data=t.values, index=t.index, columns=['Count'])
dist.reindex(["Central", "Northern", "Park", "Southern", "Mission", "Tenderloin", "Richmond", "Taraval", "Ingleside", "Bayview"])
dist = dist.reset_index()
dist.rename({'index': 'District'}, axis='columns', inplace=True)
dist[:-1]


# ### THE MAIN MAP : Precinct Map

# In[ ]:


import folium
 
gjson = r'https://cocl.us/sanfran_geojson'
SFmap = folium.Map(location = [37.77, -122.42], zoom_start = 12)
#making a chloropleth map, one can also use plotly, d3js etc.
SFmap.choropleth(
    geo_data=gjson,
    data=dist,
    columns=['District', 'Count'],
    key_on='feature.properties.DISTRICT',
    line_opacity=0.3,
    fill_color='YlOrRd', 
    fill_opacity=0.7, 
    legend_name='Crime Rate in San Francisco'
)
SFmap


# Here we are with the geospatial distribution of crime in San Francisco. The heat map for New York City can be found at https://maps.nyc.gov/crime/. Hope you all enjoyed this kernel. 
# 
# Leave comments on how this could be improved. Have fun!!
