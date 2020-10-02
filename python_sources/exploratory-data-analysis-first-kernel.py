#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import folium
from folium import plugins

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


#loading the csv file
data=pd.read_csv('../input/crime.csv',encoding='latin-1')


# In[ ]:


#reading the data 
data.head()


# In[ ]:


#Checking the datatypes of the features
data.info()


# Now I would like to explore the frequency and the gravity of the columns 
# 1.  OFFENSE_CODE_GROUP
# 2.  DISTRICT

# In[ ]:


#creating a function to return to 10 frequent rows in a relative columns
def top10(x):
    return data[x].value_counts().head(10)

#lets check the top 10 offense_code_group
top10('OFFENSE_CODE_GROUP').plot.bar()


# The most frequently occured offense code group is Motor Vehicle Accident Response. Let us further investigate into that offense code group
# 

# In[ ]:


#lets look into the offense description and the frequency with respect to the offense group Motor Vehicle Accident Response
data['OFFENSE_DESCRIPTION'][data['OFFENSE_CODE_GROUP']== 'Motor Vehicle Accident Response'].value_counts().sort_values().plot.barh()


# we can understand from the above that the most of the Motor Vehicle accidents led to the Property damages and the human injuries are comparitively less
# 
# 

# In[ ]:


#lets take a look in to Larceny and move on to the different features
data['OFFENSE_DESCRIPTION'][data['OFFENSE_CODE_GROUP']== 'Larceny'].value_counts().sort_values().plot.barh()


# we can notice that most of thefts of the personal properties were taken place in the buildings and the shops

# In[ ]:


#lets check the missing values in the column
data.DISTRICT.isna().sum()


# *  There are just 1774 missing values in the above column so we can ignore and perform the analysis as it would not effect much****

# In[ ]:


#lets look at the top 10 frequent crimes enabled districts
top10('DISTRICT').plot.bar()


# In[ ]:


#lets see the kind of thefts that's most taken place in the top 3 disctricts
data['OFFENSE_CODE_GROUP'][data['DISTRICT']=='B2'].value_counts().head(10).plot.bar()


# In[ ]:


fig,a= plt.subplots(1,3,figsize=(20,6))
i=0
column=['B2','C11','D4']
for col in column:
    a[i].bar(data['OFFENSE_CODE_GROUP'][data['DISTRICT']==col].value_counts().head(10).index,
          data['OFFENSE_CODE_GROUP'][data['DISTRICT']==col].value_counts().head(10).values)
    plt.draw()
    a[i].set_xticklabels(a[i].get_xticklabels(),rotation=30,ha='right')
    a[i].set_xlabel(col)
    a[i].set_ylabel('frequency')
    i+=1
   
plt.show()


# D-4 district is more prone to Larceny thefts

# In[ ]:


#replacing the  null values with N in the shooting column 
data['SHOOTING']=data['SHOOTING'].replace(np.nan,'N')


# In[ ]:


data['OFFENSE_DESCRIPTION'][data['SHOOTING']=='Y'].value_counts().head(10).sort_values().plot.barh()


# The above visualization shows most of gunshooting acts fall under the Assault-Aggrevated-Battery and Murder,Non-negligient Manslaughter

# * let us now tap into the Geo-spatial data visualization

# In[ ]:


data[['Lat','Long','STREET']].head()


# In[ ]:


#setting up the map for the boston co-ordinates
mapping=folium.Map([42.262607, -71.121186],zoomstart=11)
mapping


# In[ ]:


#now lets convert the latitudes and longitudes of streets in to a (n,2) matrix
streetMap= data[['Lat','Long']][data['SHOOTING']=='Y']
#replacing the null values with zero
streetMap=streetMap.replace(np.nan,0)
#converting the latitude and longitude to (n,2)matrix
streetMap= streetMap.values
#now adding the heat signatures to the mapping
mapping.add_child(plugins.HeatMap(streetMap,radius=15))
mapping


# heat map suggestes Dorchester Neighborhood has more shootings, checked the google search for the neighborhood and noticed two news highlights and both include shooting related incedents.

# In[ ]:


#lets check the drug related crimes
streetMap=data[['Lat','Long']][data['OFFENSE_CODE_GROUP']=='Drug Violation']
#replacing the null values with zero
streetMap=streetMap.replace(np.nan,0)
#making the (n,2) matrix for [lat,long] values
streetMap=streetMap.values
#injecting heat signature into the map
mapping.add_child(plugins.HeatMap(streetMap,radius=10))


# In[ ]:




