#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# PROJECT: IMPROVING NIGERIA'S CAESAREAN SECTION SERVICES: THE DATA SCIENCE ROLE

#    @ Author: ODERINDE, Taiwo Emmanuel


# In[ ]:


import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# source file
df =pd.read_csv('../input/csdataset.csv', index_col=0)
df


# In[ ]:


# Opening up our dataset
df.describe().transpose()


# In[ ]:


col = df.columns
print(col)


# In[ ]:


y = df.management
list = ['survey_id','improved_water_supply', 'improved_sanitation',
       'vaccines_fridge_freezer','sector']
x = df.drop(list,axis = 1 )
x.head()


# In[ ]:


ax = sns.countplot(y,label="Count")       # M = 212, B = 357
##print('Not offering CS: ',0)
#print('Offering CS : ',1)


# In[ ]:


x.describe()


# In[ ]:


f,ax = plt.subplots(figsize=(18, 18))
sns.heatmap(x.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)


# In[ ]:


df.info()


# In[ ]:


# Ckeck if there are null values or NA in this column

df.isnull().values.any()


# In[ ]:


# This is the total number of null values in our Dataset.

df.isnull().sum()


# In[ ]:


# Feature Selection - Dropping some columns

df.drop('facility_type_display', axis=1, inplace=True)
df.drop('child_health_measles_immun_calc', axis=1, inplace=True)
df.drop('community', axis=1, inplace=True)
df.drop('ward', axis=1, inplace=True)
df.drop('improved_water_supply', axis=1, inplace=True)
df.drop('improved_sanitation', axis=1, inplace=True)
df.drop('vaccines_fridge_freezer', axis=1, inplace=True)
df.drop('antenatal_care_yn', axis=1, inplace=True)
df.drop('family_planning_yn', axis=1, inplace=True)
df.drop('malaria_treatment_artemisinin', axis=1, inplace=True)
df.drop('sector', axis=1, inplace=True)
df.drop('gps', axis=1, inplace=True)
df.drop('survey_id', axis=1, inplace=True)

df.isnull().sum()


# In[ ]:


df.describe().transpose()


# In[ ]:


# Now we can start Data Analysis, but we need to know the right data for answering our question;
# hence, we need to decide what to measure

# For example, we can check for relationship in our Data,


# In[ ]:


# # Relationship between longitude and latitude should inform us about the area where the survey was conducted
df.plot(kind="scatter", x="longitude", y="latitude", alpha=0.4)
plt.show()


# In[ ]:


# Now, comparing the areas where Maternal health Delivery 
#Services is being conducted to C-Section rendering Hospitals
sns.pairplot(df)


# In[ ]:


df.plot(kind="scatter", x="longitude", y="latitude",
    label="maternal_health_delivery_services",
    c="maternal_health_delivery_services", cmap=plt.get_cmap("rainbow"),
    colorbar=True, alpha=0.9, figsize=(10,7),
)
plt.legend()
plt.show()


# In[ ]:


df.plot(kind="scatter", x="longitude", y="latitude",
    label="c_section_yn",
    c="c_section_yn", cmap=plt.get_cmap("rainbow"),
    colorbar=True, alpha=0.9, figsize=(10,7),
)
plt.legend()
plt.show()


# In[ ]:


# This code calculates the distance between two points using longitude and latitude
from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 6373.0

lat1 = radians( 5.076200 )
lon1 = radians(5.871500)
lat2 = radians(6.447500)
lon2 = radians(9.049100)

dlon = lon2 - lon1
dlat = lat2 - lat1

a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
c = 2 * atan2(sqrt(a), sqrt(1 - a))

distance = R * c

#print("Result:", distance)
print("Should be:", distance, "km")


# In[ ]:


df.count()


# In[ ]:


# Total number of hospitals where C-Section column has a value
df['c_section_yn'].count()


# In[ ]:


# This shows that only 5,246 Hospitals are rendering C-Section in Nigeria.
cs = df[df['c_section_yn']==1].count()
cs


# In[ ]:


mhd = df[df['maternal_health_delivery_services']==1].count()
mhd


# In[ ]:


# This shows that only 28,332 Hospitals are not rendering C-Section in Nigeria.
ncs = df[df['c_section_yn']==0].count()
ncs


# In[ ]:


nmhd = df[df['maternal_health_delivery_services']==0].count()
nmhd


# In[ ]:


data = {'MEDICAL SERVICES':['Maternal_health_delivery_services','c_section_yn'],
        'OFFERING':[20920,5246]}

OFFERING = DataFrame(data)


OFFERING


# In[ ]:


data = {'MEDICAL SERVICES':['Maternal_health_delivery_services','c_section_yn'],
        'NOT_OFFERING':[12531,28332]}

NOT_OFFERING = DataFrame(data)


NOT_OFFERING


# In[ ]:


compare= pd.merge(OFFERING,NOT_OFFERING,how='inner',on='MEDICAL SERVICES')
compare


# In[ ]:


compare.plot.bar()


# In[ ]:


df['c_section_yn']


# In[ ]:


df['c_section_yn']==1


# In[ ]:


df['longitude']


# In[ ]:


df['latitude']


# In[ ]:


# Lets pick two two points from our longitude and latitude column
from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 6373.0

lat1 = radians( 5.076200 )
lon1 = radians(5.871500)
lat2 = radians(6.447500)
lon2 = radians(9.049100)

dlon = lon2 - lon1
dlat = lat2 - lat1

a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
c = 2 * atan2(sqrt(a), sqrt(1 - a))

distance = R * c

#print("Result:", distance)
print("Should be:", distance, "km")


# In[ ]:


gps = {'longitude':df['longitude'],
        'latitude':df['latitude']}

location = DataFrame(gps)


location


# In[ ]:


def lg(x):
    for i in range(len(df)):
        if df['unique_lga'][i] == x:
            return df['longitude'][i]

lg('cross_river_obudu')


# In[ ]:





# In[ ]:




