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


# In[ ]:


import matplotlib.pyplot as plt 
import seaborn as sns
sns.set()


# In[ ]:


weather_main = pd.read_csv("/kaggle/input/energy-consumption-generation-prices-and-weather/weather_features.csv")
energy_main = pd.read_csv("/kaggle/input/energy-consumption-generation-prices-and-weather/energy_dataset.csv")


# In[ ]:


sample_energy = energy_main.tail(100)
sample_weather = weather_main.tail(100)


# #### SAMPLE_ENERGY EXPLORATION

# In[ ]:


sample_energy


# In[ ]:


sample_energy.info()


# In[ ]:


def unique_values(df): 
    for col in df :
        if df[col].dtypes == "object":
            print (df[col].unique())

unique_values(sample_energy)


# In[ ]:


sample_energy.astype(bool).sum()


# In[ ]:


sample_energy = sample_energy.drop(["generation fossil coal-derived gas","generation fossil oil shale","generation fossil peat","generation geothermal","generation marine","generation wind offshore"], axis =1)


# #### SAMPLE_WEATHER EXPLORATION

# In[ ]:


sample_weather


# In[ ]:


sample_weather.info()


# In[ ]:


unique_values(sample_weather)


# In[ ]:


sample_weather.astype(bool).sum()


# In[ ]:


sample_weather = sample_weather.drop(["rain_1h","rain_3h","snow_3h","weather_icon","weather_description","temp_min","temp_max","clouds_all"], axis =1)


# In[ ]:


sample = sample_energy.merge(sample_weather, left_on="time", right_on="dt_iso")


# In[ ]:


sample = sample.drop(["dt_iso","city_name"], axis =1)


# In[ ]:


sample.head()


# ## DATA VISUALIZATION
# ### Data Distrbution

# In[ ]:


sample.hist(figsize =(30,30))


# In[ ]:


sample = sample.drop(["forecast wind offshore eday ahead","generation hydro pumped storage aggregated"], axis = 1)


# In[ ]:


sample.hist(figsize = (30,30))

