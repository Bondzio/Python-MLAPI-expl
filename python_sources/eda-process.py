#!/usr/bin/env python
# coding: utf-8

# Chennai, on the Bay of Bengal in eastern India, is the capital of the state of Tamil Nadu. Chennai is going through water crisis. This is just start if we dont take care of our natural resources. 
# 
# https://www.thehindu.com/news/cities/chennai/train-carrying-water-from-jolarpettai-arrives-in-chennai/article28409328.ece 
# 
# By this article you can imagine the criticality of the issue. 
# 
# I have taken Chennai Water Management Dataset to visualize different aspects of water supply to the city. 
# 
# It will be running kernel, I will keep improving it so stay tuned.

# In[ ]:


# load the libraries
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))


# There are 2 types of the dataset 
# 1. Reservior Level 
# 2. Rainfall 

# In[ ]:


# understand the water levels
df_levels = pd.read_csv('../input/chennai_reservoir_levels.csv')
df_levels.head(2)


# In[ ]:


# understand the dataset first 
df_rainfall = pd.read_csv('../input/chennai_reservoir_rainfall.csv')
df_rainfall.head()


# In[ ]:


# understanding the statsitical properties 
df_levels.describe()


# In[ ]:


df_rainfall.index = pd.to_datetime(df_rainfall['Date'])
df_rainfall.head(2)


# In[ ]:


df_levels.index = pd.to_datetime(df_levels['Date'])
df_levels.head(2)


# In[ ]:


# making datetime an index
del df_levels['Date']
del df_rainfall['Date']


# In[ ]:


df_levels.head(2)


# In[ ]:


df_levels.tail(2)


# In[ ]:


import matplotlib.pyplot as plt 


# In[ ]:


#sns.distplot(df_levels['POONDI'])
#plt.grid(df_levels['POONDI'])
#df_levels.plot()

# drawing the plot to understand the variance against time
import matplotlib.pyplot as plt 
'''
plt.subplot(411)
plt.plot(df_rain['POONDI'])
plt.xlabel('Poondi')
plt.tight_layout()

plt.subplot(412)
plt.plot(df_levels['CHOLAVARAM'])
plt.xlabel('CHOLAVARAM')
plt.tight_layout()

plt.subplot(413)
plt.plot(df_levels['REDHILLS'])
plt.xlabel('REDHILLS')
plt.tight_layout()

plt.subplot(414)
plt.plot(df_levels['CHEMBARAMBAKKAM'])
plt.xlabel('CHEMBARAMBAKKAM')
plt.tight_layout()
'''


# In[ ]:


df_levels['POONDI'].plot()
plt.xlabel('Poondi')
plt.tight_layout()


# In[ ]:


df_levels['CHEMBARAMBAKKAM'].plot()
plt.xlabel('CHEMBARAMBAKKAM')
plt.tight_layout()


# In[ ]:


df_levels['CHOLAVARAM'].plot()
plt.xlabel('CHOLAVARAM')
plt.tight_layout()


# In[ ]:


plt.figure(figsize=(10,5))
df_rainfall['POONDI'].plot()


# In[ ]:


# adding few extra columns 
df_rainfall['Year'] = df_rainfall.index.year
df_rainfall['Month'] = df_rainfall.index.month
df_rainfall['Weekday Name'] = df_rainfall.index.weekday_name

# Display a random sampling of 5 rows
df_rainfall.sample(5, random_state=0)


# In[ ]:


# adding few extra columns 
df_levels['Year'] = df_levels.index.year
df_levels['Month'] = df_levels.index.month
df_levels['Weekday Name'] = df_levels.index.weekday_name

# Display a random sampling of 5 rows
df_levels.sample(5, random_state=0)


# In[ ]:


import seaborn as sns

# Use seaborn style defaults and set the default figure size
sns.set(rc={'figure.figsize':(11, 4)})


# In[ ]:


# to know how it scatter very year
col_plt = ['POONDI', 'REDHILLS', 'CHOLAVARAM', 'CHEMBARAMBAKKAM']
axes = df_rainfall[col_plt].plot(marker='.', alpha=0.5, linestyle='None', figsize=(11, 9), subplots=True)
for ax in axes:
    ax.set_ylabel('Daily Rainfall')


# In[ ]:


# to know how it scatter very year
sns.countplot(df_levels['POONDI'])


# In[ ]:


# how was rain last year in POONDI
df_rainfall.loc['2018', 'POONDI'].plot()


# In[ ]:


# raind fall at POONDI in one month
df_rainfall.loc['2018-08':'2018-09', 'POONDI'].plot()


# In[ ]:


# let us look on statstical properties 
df_rainfall.describe()
# there are zero values which no rainfall at data day


# In[ ]:


df_rainfall.head()


# In[ ]:


# let us use  pandas profiling to get the data informartion 
from pandas_profiling import ProfileReport
ProfileReport(df_rainfall)


# In[ ]:


# let us use  pandas profiling to get the data informartion 
# Pansdas profile for water levels
ProfileReport(df_levels)

