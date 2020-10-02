#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import datetime as dt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory


# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        
# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv('/kaggle/input/temperature-readings-iot-devices/IOT-temp.csv', parse_dates=[2])


# In[ ]:


data.head()


# In[ ]:


data.info()


# In[ ]:


# checking if the dataset contaisn null values
data.isnull().sum()


# In[ ]:


# are the in and out values in different cases
data['out/in'].unique()


# In[ ]:


# bar plot for number of in and out temp in the dataset
data['out/in'].value_counts().plot.bar()


# In[ ]:


data['out/in'].value_counts().plot.pie(explode=[0,0.1],  autopct='%1.0f%%')


# In[ ]:


plt.figure(figsize=(10,6))
plt.plot(data['temp'])
plt.ylabel('temp')
plt.title('change in temperature over the dataset')


# In[ ]:


# histogram for the change in temperature
plt.figure(figsize=(14,6))
sns.distplot(data['temp'])


# In[ ]:


# histogram of the various values of temp recorded
plt.figure(figsize=(10,10))
data['temp'].value_counts().plot.bar()
plt.xlabel('Temp')
plt.ylabel('Count')
plt.title('Count of temprature recorded')
plt.show()


# In[ ]:


# extracting the day, month, year and time from the date column
data.rename({'noted_date': 'date'}, axis='columns', inplace=True)
data['month'] = data['date'].dt.month
data['year'] = data['date'].dt.year
data['day'] = data['date'].dt.day
data['time'] = data['date'].dt.time


# In[ ]:


data.head()


# In[ ]:


# dropping the date column
data.drop(['date'], inplace=True, axis=1)


# In[ ]:


# change in temp over months
plt.figure(figsize=(10,6))
sns.scatterplot(data['month'], data['temp'], hue=data['out/in'])


# In[ ]:


data['month'].value_counts()
x = data[data['month'] == 10]


# In[ ]:


f, ax = plt.subplots(1,2, figsize=(10,8))
sns.scatterplot(x['day'], x['temp'], hue=x['out/in'], ax=ax[0])
sns.lineplot(x['day'], x['temp'], hue=x['out/in'], ax=ax[1])
plt.xlabel('days')
plt.ylabel('temp')
ax[0].set_title('Change in temperature in the month of october')


# out of all the days in october, day 17 has the highest recorded number of temp count, lets check the change in temperature on that day

# In[ ]:


new_day = x[x['day'] == 17]
f, ax = plt.subplots(1,2,figsize=(14,8))
sns.lineplot(new_day['time'], new_day['temp'], hue=new_day['out/in'], ax=ax[0])
sns.scatterplot(new_day['time'], new_day['temp'], hue=new_day['out/in'], ax=ax[1])


# The temperature usually rises mostly in the morning around 5 AM till 11 AM

# let's check if its true for all the recorded values

# In[ ]:


# change in temperature wrt time over all the months

f, ax = plt.subplots(1,2, figsize=(15,8))
sns.lineplot(data['time'], data['temp'], hue=data['out/in'], ax=ax[0])
sns.scatterplot(data['time'], data['temp'], hue=data['out/in'], ax=ax[1])
plt.xlabel('Time')
plt.ylabel('Temp')
plt.title('Change in temperature w.r.t time')
plt.show()


# This graph confirms our hypothesis that the temperature indeed rises around the 5 AM mark

# In[ ]:




