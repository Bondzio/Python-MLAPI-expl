#!/usr/bin/env python
# coding: utf-8

# # KSI Data Cleaning
# *[Geospatial Club](http://bit.ly/uwgeospatial) - Winter 2019*
# 
# This notebook is about perfomring data cleaning on the dataset called [Killed or Seriously Injured](http://bit.ly/open-data-ksi-toronto) provided by the City of Toronto Police Open Data portal.
# 
# The Data Cleaning of this dataset was in preparation for another kernel that was used for a workshop called [Machine Learning for Geospatial Data](https://www.kaggle.com/jrmistry/uwgeo-club-ml-for-vector-geodata-workshop-1/).

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


# In[ ]:


df_ksi = pd.read_csv('../input/KSI.csv')


# In[ ]:


df_ksi.info()


# In[ ]:


df_ksi.sample(5)


# # Issues Discovered with Dataset that will be Cleaned
# 
# 1. DATE field is only accurate for year, month, & day
# 2. Attribute 'ACCLASS' should be optimized for fatal vs non-fatal incidents
# 3. Fatal incidents can be represented in a boolean manner
# 4. The following attributes represent boolean values and should be encoded as such:
# 
# 
# * CYCLIST
# * AUTOMOBILE
# * MOTORCYCLE
# * TRUCK
# * TRSN_CITY_VEH
# * EMERG_VEH
# * PASSENGER
# * SPEEDING
# * AG_DRIV
# * REDLIGHT
# * ALCOHOL
# * DISABILITY

# In[ ]:


from datetime import datetime

def str_to_datetime(string):
    return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S.%fZ")


# In[ ]:


def calculate_minutes(row):
    if row['Hour'] == 0:
        return row['TIME']
    else:
        return int(str(row['TIME'])[len(str(row['Hour'])):])


# In[ ]:


def calculate_weekday(row):
    return datetime(year = row['YEAR'],
                    month = row['MONTH'],
                    day = row['DAY'],
                    hour = row['HOUR'],
                    minute = row['MINUTES']
                   ).weekday()


# In[ ]:


def data_clean(data):
    # The commented code below is just for referrence on how to manipulate entire columns at once.
    #data['Age'] = data['Age'].fillna(data['Age'].median())
    #data['Gender'] = data['Sex'].map({'female':0, 'male':1}).astype(int)
    #data['Family'] = data['Parch'] + data['SibSp']
    #data['Fare'] = data['Fare'].fillna(data['Fare'].mean())
    #data = data.drop(['SibSp','Parch','Sex','Name','Cabin','Embarked','Ticket'],axis=1)
    
    for attribute in ['PEDESTRIAN', 'CYCLIST', 'AUTOMOBILE', 'MOTORCYCLE', 'TRUCK', 'TRSN_CITY_VEH', 'EMERG_VEH', 'PASSENGER', 'SPEEDING', 'AG_DRIV', 'REDLIGHT', 'ALCOHOL', 'DISABILITY']:
        data[attribute] = data[attribute].map({'Yes': 1,
                                               '': 0}).fillna(0).astype(int)
    
    data['FATAL'] = data['ACCLASS'].map({'Non-Fatal Injury': 0,
                                         'Property Damage Only': 0,
                                         'Fatal': 1}).fillna(0)
    
    date_temp = data['DATE'].apply(str_to_datetime)
    data['MONTH'] = date_temp.apply(lambda x: x.month)
    data['DAY'] = date_temp.apply(lambda x: x.day)
    data['HOUR'] = data['Hour']
    data['MINUTES'] = data.apply(calculate_minutes, axis=1)
    data['WEEKDAY'] = data.apply(calculate_weekday, axis=1)#.map({0: 'Monday',1: 'Tuesday',2: 'Wednesday',3: 'Thursday',4: 'Friday',5: 'Saturday',6: 'Sunday'})
    
    print(data.columns)
        
    return data[['ACCNUM',
                 'YEAR',
                 'MONTH',
                 'DAY',
                 'HOUR',                 
                 'MINUTES',
                 'WEEKDAY',
                 'LATITUDE',
                 'LONGITUDE',
                 'Ward_Name',
                 'Ward_ID',
                 'Hood_Name',
                 'Hood_ID',
                 'Division',
                 'District',
                 'STREET1',
                 'STREET2',
                 'OFFSET',
                 'ROAD_CLASS'] + list(data.columns[15:-12]) + ['FATAL']
               ]


# In[ ]:


df_ksi_clean = data_clean(df_ksi.copy())


# In[ ]:


df_ksi_clean.sample(5)


# In[ ]:


df_ksi_clean.info()


# In[ ]:


df_ksi_clean.to_csv('KSI_CLEAN.csv', index = False)

