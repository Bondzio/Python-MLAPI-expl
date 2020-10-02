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


# ## Data Import

# In[ ]:


calls_for_service = pd.read_csv('../input/police-department-calls-for-service.csv')
incidents = pd.read_csv('../input/police-department-incidents.csv')


# ## Data Analysis
# 
# ### How many rows does each dataset contain? 

# In[ ]:


print(f'The Calls For Service dataset contains {len(calls_for_service):,} rows.')
print(f'The Police Incidents dataset contains {len(incidents):,} rows.')


# ### What are the columns in each dataset?

# In[ ]:


print(f'Calls for Service: {list(calls_for_service.columns)}\n')
print(f'Police Incidents: {list(incidents.columns)}')


# ### What are the columns in each dataset? How many are numerical? 

# In[ ]:


# What are the data types of the columns?
calls_for_service.info()


# In[ ]:


incidents.info()


# ### How many missing values are in each column? Which columns have the most missing values? 

# In[ ]:


calls_for_service.isnull().sum().sort_values(ascending=False)


# In[ ]:


incidents.isnull().sum().sort_values(ascending=False)


# ### What is the min/max dates available in each dataset?

# In[ ]:


print(
f"""Calls for Service:
Min Report Date: {pd.to_datetime(calls_for_service['Report Date']).min().strftime('%Y-%m-%d')}
Max Report Date: {pd.to_datetime(calls_for_service['Report Date']).max().strftime('%Y-%m-%d')}
Min Call Date: {pd.to_datetime(calls_for_service['Call Date']).min().strftime('%Y-%m-%d')}
Max Call Date: {pd.to_datetime(calls_for_service['Call Date']).max().strftime('%Y-%m-%d')}
"""
)


# In[ ]:


print(
f"""Incidents:
Min Date: {pd.to_datetime(incidents['Date']).min().strftime('%Y-%m-%d')}
Max Date: {pd.to_datetime(incidents['Date']).max().strftime('%Y-%m-%d')}
"""
)


# ### What are the top 10 most common crimes in the Calls for Service dataset?  What are the most common incident categories in the Incidents dataset?

# In[ ]:


calls_for_service.groupby(['Original Crime Type Name']).count().loc[:, 'Crime Id'].sort_values(ascending=False).head(10)


# In[ ]:


incidents.groupby(['Category']).count().loc[:, 'IncidntNum'].sort_values(ascending=False).head(10)


# ### What day of week had the most average daily calls in July 2018 (Calls for Service dataset)? 

# In[ ]:


# Convert Call Date Time column to Datetime object
calls_for_service['Call Date Time'] = pd.to_datetime(calls_for_service['Call Date Time'])


# In[ ]:


# Derive Call Date and Day of Week Columns
calls_for_service.loc[:, 'Call Date'] = calls_for_service['Call Date Time'].apply(lambda x: x.strftime('%Y-%m-%d'))
calls_for_service.loc[:, 'Day of Week'] = calls_for_service['Call Date Time'].apply(lambda x: x.strftime('%A'))

# Isolate July data
cfs_jul18 = calls_for_service[(calls_for_service['Call Date'] >= '2018-07-01') &
                              (calls_for_service['Call Date'] <= '2018-07-31')]


# In[ ]:


crimes_by_day_of_week = pd.DataFrame(cfs_jul18.groupby('Day of Week').nunique().loc[:, ['Crime Id', 'Call Date']])
crimes_by_day_of_week.loc[:, 'AVG Crimes'] = crimes_by_day_of_week['Crime Id'] / crimes_by_day_of_week['Call Date']
crimes_by_day_of_week.sort_values('AVG Crimes', ascending=False)


# ### What was the most common time of day for a DRUG/NARCOTIC incident to occur in 2016? 2017?

# In[ ]:


incidents['Date'] = pd.to_datetime(incidents.Date)

# Isolate 2016, 2017
incidents_1617 = incidents[(incidents['Date'] >= '2016-01-01') &
                           (incidents['Date'] <= '2017-12-31')]

# Isolate DRUG/NARCOTIC incidents
incidents_1617 = incidents_1617[incidents_1617['Category'] == 'DRUG/NARCOTIC']


# In[ ]:


from datetime import datetime
incident_time = incidents_1617.set_index('Date').loc[:, ['IncidntNum', 'Time']]
incident_time['Hour'] = incident_time.Time.apply(lambda x: datetime.strptime(x, '%H:%M').strftime('%H'))
#incident_time.groupby(['Hour']).nunique().loc[:, 'IncidntNum'].sort_values(ascending=False)


# In[ ]:


# Not finished ... 

