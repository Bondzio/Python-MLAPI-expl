#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
import seaborn as sns

from sklearn.preprocessing import minmax_scale
from sklearn.preprocessing import normalize
from sklearn.preprocessing import Normalizer
from scipy.stats import boxcox

import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# In[8]:


weather_data = pd.read_csv('../input/Summary of Weather.csv')


# In[9]:


#Lets first see a sample of the data
weather_data.sample(5)


# Atleast this shows there there is some amount of scaling issue in the data.
# Look for example at the scale of STA, MaxTemp, Snowfall, YR columns.
# 
# Some are in 000s, some in 00s, some in 0s
# 

# In[10]:


#Let us understand the nature of data and distribution of it.
weather_data.describe()

#Ok not such anomalies to naked eyes


# In[11]:


#Let us see how categorical data is
weather_data.describe(include=['O'])


# In[12]:


#There are 119040 rows and 31 columns.
print (weather_data.shape)
print ('--'*30)

#Lets see what percentage of each column has null values
#It means count number of nulls in every column and divide by total num of rows.

print (weather_data.isnull().sum()/weather_data.shape[0] * 100)


# Whoa, there are lot of columns with 100% null values. It is better to drop these columns before we proceed. 
# They are not going to add any value or we are not going to loose any value after dropping these columns.
# 
# Lets keep the threshold to 70% so that any column with 70% null values is not going to add any value.
# 

# In[13]:


#weather_data[col].isnull().sum()/weather_data.shape[0] * 100 < 70)
#Commented line to check if that column's null percentage is below 70

cols = [col for col in weather_data.columns if (weather_data[col].isnull().sum()/weather_data.shape[0] * 100 < 70)]
weather_data_trimmed = weather_data[cols]

#STA is more of station code, lets drop it for the moment
weather_data_trimmed = weather_data_trimmed.drop(['STA'], axis=1)

print ('Legitimate columns after dropping null columns: %s' % weather_data_trimmed.shape[1])


# In[14]:


weather_data_trimmed.isnull().sum()


# In[15]:


weather_data_trimmed.sample(5)


# In[16]:


#Check dtypes and look for conversion if needed
weather_data_trimmed.dtypes

#Looks like some columns needs to be converted to numeric field

weather_data_trimmed['Snowfall'] = pd.to_numeric(weather_data_trimmed['Snowfall'], errors='coerce')
weather_data_trimmed['SNF'] = pd.to_numeric(weather_data_trimmed['SNF'], errors='coerce')
weather_data_trimmed['PRCP'] = pd.to_numeric(weather_data_trimmed['PRCP'], errors='coerce')
weather_data_trimmed['Precip'] = pd.to_numeric(weather_data_trimmed['Precip'], errors='coerce')

weather_data_trimmed['Date'] = pd.to_datetime(weather_data_trimmed['Date'])


# In[17]:


#Fill remaining null values. FOr the moment lts perform ffill

weather_data_trimmed.fillna(method='ffill', inplace=True)
weather_data_trimmed.fillna(method='bfill', inplace=True)

weather_data_trimmed.isnull().sum()
#Well no more NaN and null values to worry about


# In[18]:


print (weather_data_trimmed.dtypes)
print ('--'*30)
weather_data_trimmed.sample(3)


# In[19]:


#weather_data_trimmed_scaled = minmax_scale(weather_data_trimmed.iloc[:, 1:])

weather_data_trimmed['Precip_scaled'] = minmax_scale(weather_data_trimmed['Precip'])
weather_data_trimmed['MeanTemp_scaled'] = minmax_scale(weather_data_trimmed['MeanTemp'])
weather_data_trimmed['YR_scaled'] = minmax_scale(weather_data_trimmed['YR'])
weather_data_trimmed['Snowfall_scaled'] = minmax_scale(weather_data_trimmed['Snowfall'])
weather_data_trimmed['MAX_scaled'] = minmax_scale(weather_data_trimmed['MAX'])
weather_data_trimmed['MIN_scaled'] = minmax_scale(weather_data_trimmed['MIN'])

#weather_data_trimmed.sample(3)


# In[20]:


#Plot couple of columns to see how the data is scaled

fig, ax = plt.subplots(4, 2, figsize=(15, 15))

sns.distplot(weather_data_trimmed['Precip'], ax=ax[0][0])
sns.distplot(weather_data_trimmed['Precip_scaled'], ax=ax[0][1])

sns.distplot(weather_data_trimmed['MeanTemp'], ax=ax[1][0])
sns.distplot(weather_data_trimmed['MeanTemp_scaled'], ax=ax[1][1])

sns.distplot(weather_data_trimmed['Snowfall'], ax=ax[2][0])
sns.distplot(weather_data_trimmed['Snowfall_scaled'], ax=ax[2][1])

sns.distplot(weather_data_trimmed['MAX'], ax=ax[3][0])
sns.distplot(weather_data_trimmed['MAX_scaled'], ax=ax[3][1])


# * Precip_norm = normalize(weather_data_trimmed['Precip_scaled'])
# * MeanTemp_norm = normalize(weather_data_trimmed['MeanTemp_scaled'])
# * YR_norm = normalize(weather_data_trimmed['YR_scaled'])
# * Snowfall_norm = normalize(weather_data_trimmed['Snowfall_scaled'])
# * MAX_norm = normalize(weather_data_trimmed['MAX_scaled'])
# * MIN_norm = normalize(weather_data_trimmed['MIN_scaled'])

# In[21]:


Precip_norm = boxcox(weather_data_trimmed['Precip_scaled'].loc[weather_data_trimmed['Precip_scaled'] > 0])
MeanTemp_norm = boxcox(weather_data_trimmed['MeanTemp_scaled'].loc[weather_data_trimmed['MeanTemp_scaled'] > 0])
YR_norm = boxcox(weather_data_trimmed['YR_scaled'].loc[weather_data_trimmed['YR_scaled'] > 0])
Snowfall_norm = boxcox(weather_data_trimmed['Snowfall_scaled'].loc[weather_data_trimmed['Snowfall_scaled'] > 0])
MAX_norm = boxcox(weather_data_trimmed['MAX_scaled'].loc[weather_data_trimmed['MAX_scaled'] > 0])
MIN_norm = boxcox(weather_data_trimmed['MIN_scaled'].loc[weather_data_trimmed['MIN_scaled'] > 0])


# In[22]:


fig, ax = plt.subplots(4, 2, figsize=(15, 15))

sns.distplot(weather_data_trimmed['Precip_scaled'], ax=ax[0][0])
sns.distplot(Precip_norm[0], ax=ax[0][1])

sns.distplot(weather_data_trimmed['MeanTemp_scaled'], ax=ax[1][0])
sns.distplot(MeanTemp_norm[0], ax=ax[1][1])

sns.distplot(weather_data_trimmed['Snowfall_scaled'], ax=ax[2][0])
sns.distplot(Snowfall_norm[0], ax=ax[2][1])

sns.distplot(weather_data_trimmed['MAX_scaled'], ax=ax[3][0])
sns.distplot(MAX_norm[0], ax=ax[3][1])

