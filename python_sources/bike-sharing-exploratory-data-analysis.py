#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# importing libraries

# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sb
sb.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')

Reading data
# In[ ]:


df=pd.read_csv('..//input/london-bike-sharing-dataset/london_merged.csv',parse_dates=True)


# In[ ]:



#Data feature descriptions

# "timestamp" - timestamp field for grouping the data
# "cnt" - the count of a new bike shares
# "t1" - real temperature in C
# "t2" - temperature in C "feels like"
# "hum" - humidity in percentage
# "wind_speed" - wind speed in km/h
# "weather_code" - category of the weather
# "is_holiday" - boolean field - 1 holiday / 0 non holiday
# "is_weekend" - boolean field - 1 if the day is weekend
# "season" - category field meteorological seasons: 0-spring ; 1-summer; 2-fall; 3-winter.

# "weathe_code" category description:
# 1 = Clear ; mostly clear but have some values with haze/fog/patches of fog/ fog in vicinity
# 2 = scattered clouds / few clouds
# 3 = Broken clouds
# 4 = Cloudy
# 7 = Rain/ light Rain shower/ Light rain
# 10 = rain with thunderstorm
# 26 = snowfall
# 94 = Freezing Fog


# Getting first five rows of dataset.

# In[ ]:


df.head()


# Getting info of data

# In[ ]:


df.info()


# Converting timestamp column into Time stamp object.

# In[ ]:


df['timestamp'] = pd.to_datetime(df['timestamp'])


# In[ ]:


type(df['timestamp'].iloc[0])


# Getting Hour,month and day of week from the timestamp column.

# In[ ]:


df['Hour']=df['timestamp'].apply(lambda time: time.hour)
df['Month']=df['timestamp'].apply(lambda time: time.month)
df['day of week']=df['timestamp'].apply(lambda time: time.dayofweek)


# The Day of Week is an integer 0-6. Use the .map() with this dictionary to map the actual string names to the day of the week

# In[ ]:


dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}


# In[ ]:


df['day of week'] = df['day of week'].map(dmap)


# In[ ]:


df.head()


# In[ ]:


# plotting no of counts on each day w.r.t to weather
plt.figure(figsize=(8,4), dpi=100)
sb.countplot(x='day of week',hue='weather_code',data=df,palette='viridis')
# To relocate the legend
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[ ]:


plt.figure(figsize=(8,4), dpi=100)

#plotting Hourly data w.r.t weather.
sb.countplot(x='Hour',data=df,hue='weather_code',palette='viridis')
# To relocate the legend
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[ ]:


plt.figure(figsize=(8,4), dpi=100)
# plotting count of bikes on each day on hourly basis.
sb.countplot(x='day of week',hue='Hour',data=df,palette='viridis')
# To relocate the legend
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[ ]:


# no of bikes according to is_weekend column
plt.figure(figsize=(8,4), dpi=100)
sb.countplot(x='is_weekend',data=df,palette='viridis')


# As we can see the count of bikes are high on weekdays.

# In[ ]:


# no of bikes according to is_holiday column.
plt.figure(figsize=(8,4), dpi=100)
sb.countplot(x='is_holiday',data=df,palette='viridis')


# Number of bikes are higher when there is no holiday.

# In[ ]:


# no. of bikes accoding to season column
plt.figure(figsize=(8,4), dpi=100)
sb.countplot(x='season',data=df,palette='viridis')


# In[ ]:


#no 0f bikes according to weather code
plt.figure(figsize=(8,4), dpi=100)
sb.countplot(x='weather_code',data=df,palette='viridis')


# No of Bikes are higher on the day when the weather is clear.

# In[ ]:


plt.figure(figsize=(8,4), dpi=100)
sb.countplot(x='Month',data=df,palette='viridis')


# In[ ]:


df.max()


# In[ ]:


df.min()


# In[ ]:





# In[ ]:


#seleting row with max humidity
df.iloc[df['hum'].idxmax()]
#we can see when the humidity is high bike count is low


# In[ ]:


#seleting row with min humidity
df.iloc[df['hum'].idxmin()]
#when humidity is low bike count is comparitively high.


# In[ ]:


#seleting row with max wind speed
df.iloc[df['wind_speed'].idxmax()]


# In[ ]:


#seleting row with min wnd speed
df.iloc[df['wind_speed'].idxmin()]
#number of bike count is high with maximum speed.

