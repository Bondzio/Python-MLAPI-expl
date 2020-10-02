#!/usr/bin/env python
# coding: utf-8

# ###hi i have tried to perform enhanced analysis of the give dataset.
# ###Kindly upvote the kernel if you find it worthwhile
# ###EDA, Data visualisation

# **Sanfrancisco Crime Analysis**

# **Importing some Basic Libraries**

# In[ ]:


get_ipython().system('pip install squarify')


# In[ ]:


# for some basic operations
import numpy as np 
import pandas as pd 
from shapely.geometry import Point
import geopandas as gpd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# for visualizations
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
from matplotlib import cm
import urllib.request
import shutil
import zipfile
import folium
from folium.plugins import HeatMap
import squarify

# for providing path
import os
import re

import geoplot as gplt
import lightgbm as lgb
import eli5
from eli5.sklearn import PermutationImportance
print(os.listdir("../input"))


# **Reading the Dataset**

# In[ ]:


# reading the dataset

crime_data = pd.read_csv('../input/Police_Department_Incidents_-_Previous_Year__2016_.csv')

# check the shape of the data
crime_data.shape


# In[ ]:


# checking the head of the data

crime_data.head(5)


# In[ ]:


crime_data.dtypes


# In[ ]:


crime_data.describe(include='all')


# In[ ]:


# filling the missing value in PdDistrict using the mode values

crime_data['PdDistrict'].fillna(crime_data['PdDistrict'].mode()[0], inplace = True)

crime_data.isnull().any().any()


# In[ ]:


# checking if there are any null values

crime_data.isnull().sum()


# ## Data Visualization

# In[ ]:


# different categories of crime

plt.figure(figsize=(20,10))
plt.title('Major Crimes in Sanfrancisco')

sns.countplot(y=crime_data['Category'])


plt.show()


# In[ ]:


crime_data.Category.value_counts().plot(kind='hist')


# In[ ]:


# Regions with count of crimes

plt.figure(figsize=(20,10))
crime_data['PdDistrict'].value_counts().plot.bar(figsize = (12, 8))

plt.title('District with Most Crime')

plt.show()


# **Top 15 Addresses in Sanfrancisco in Crime**

# In[ ]:


# Regions with count of crimes

plt.figure(figsize=(15,8))
plt.title('Top 15 Regions in Crime')
crime_data['Address'].value_counts().head(10).plot.hist(figsize=(15,8))
plt.show()


# In[ ]:


# Regions with count of crimes


crime_data['DayOfWeek'].value_counts().head(15).plot.pie(figsize = (15, 8), explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1))

plt.title('Crime count on each day',fontsize = 20)
plt.show()


# In[ ]:


# Regions with count of crimes

crime_data['Resolution'].value_counts().plot.line(figsize = (15, 8))

plt.title('Resolutions for Crime',fontsize = 20)
plt.xticks(rotation = 90)
plt.show()


# In[ ]:


plt.figure(figsize=(15,8))
crime_data['Date'] = pd.to_datetime(crime_data['Date'])

crime_data['Month'] = crime_data['Date'].dt.month
sns.countplot(crime_data['Month'])
plt.title('Crimes in each Months')

plt.show()


# In[ ]:


# checking the time at which crime occurs mostly

import warnings
warnings.filterwarnings('ignore')
crime_data['Time'].value_counts().head(20).plot.line(figsize = (15, 9))

plt.title('Distribution of crime over the day', fontsize = 20)
plt.show()


# In[ ]:



df = pd.crosstab(crime_data['Category'], crime_data['PdDistrict'])
color = plt.cm.Greys(np.linspace(0, 1, 10))

df.div(df.sum(1).astype(float), axis = 0).plot.hist(stacked = True, color = color, figsize = (18, 12))
plt.title('District vs Category of Crime', fontweight = 30, fontsize = 20)

plt.show()


# ## Geospatial Visualization

# In[ ]:


t = crime_data.PdDistrict.value_counts()

table = pd.DataFrame(data=t.values, index=t.index, columns=['Count'])
table = table.reindex(["CENTRAL", "NORTHERN", "PARK", "SOUTHERN", "MISSION", "TENDERLOIN", "RICHMOND", "TARAVAL", "INGLESIDE", "BAYVIEW"])

table = table.reset_index()
table.rename({'index': 'Neighborhood'}, axis='columns', inplace=True)

table


# In[ ]:


plt.figure(figsize=(20,10))
sns.barplot(x=table['Neighborhood'],y=table['Count'])


# ###Training and Testing

# In[ ]:


train_df=pd.read_csv('../input/Police_Department_Incidents_-_Previous_Year__2016_.csv')
train_df.sample(3)


# In[ ]:


all_districts=train_df.PdDistrict.unique()
all_districts, len(all_districts)

