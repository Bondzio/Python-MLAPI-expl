#!/usr/bin/env python
# coding: utf-8

# # Initialization to fetch covid-19 dataset

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


# # Import libraries what you need as variable declaration

# In[ ]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from pathlib import Path
import plotly.offline as py
import plotly.express as px
import cufflinks as cf
import calendar


# In[ ]:


py.init_notebook_mode(connected=False)
cf.set_config_file(offline=True)
sns.set()
pd.plotting.register_matplotlib_converters
get_ipython().run_line_magic('matplotlib', 'inline')


# # Path file the country what you research 

# In[ ]:


province = pd.read_csv("../input/indonesia/province.csv")
jabar = pd.read_csv("../input/indonesia-coronavirus-cases/jabar.csv")


# In[ ]:


province.head(35)


# In[ ]:


jabar.head(20)


# In[ ]:


#is null?
pv = province.isnull().sum()
pv[pv>0]


# In[ ]:


it_prov = province.dropna()
it_jabar = jabar.dropna()


# In[ ]:


it_prov.isnull().any()
it_jabar.isnull().any()


# In[ ]:


#information 
it_prov.info()


# In[ ]:


#we take only the interest feature
data_province = it_prov[['province_name', 'capital_city', 'latitude', 'longitude', 'confirmed', 'deceased', 'released']].copy()
data_province.head() #ok


# In[ ]:


jabar['date'] = pd.to_datetime(jabar['date'], infer_datetime_format=True)
jabar['date'] = jabar['date'].dt.strftime('%m/%d/%Y')


# In[ ]:


#now for jabar
jabar.isnull().sum()[jabar.isnull().sum()>0]


# In[ ]:


# information
jabar.info()


# In[ ]:


jabar.head()


# # Some Statistics and Visualization

# In[ ]:


daily_info_province = data_province.sort_values(by='confirmed',                                                                                ascending=False)
daily_info_province.style.background_gradient(cmap='Pastel1_r')


# In[ ]:


print('========Province Information on COVID-19 ======================')
print('Number of province are touched: {}'.format(len(daily_info_province.province_name.unique())))
print('Number of people are positive case: {}'.format(daily_info_province.confirmed.sum()))
print('Province most affected: {}'.format((daily_info_province.iloc[0, 1], daily_info_province.iloc[0, 4])))
print('Province less affected: {}'.format((daily_info_province.iloc[25, 1], daily_info_province.iloc[25, 4])))
print('================================================================')


# In[ ]:


#plotting
daily_province = daily_info_province.set_index('province_name')
daily_province['confirmed'].iplot(kind='bar', title='Indonesia affected by COVID-19',                                           yTitle='Total Positive cases', colors='blue', lon='longitude', 
                                          lat='latitude')


# In[ ]:


fig = px.bar(daily_info_province, 
             x="province_name", 
             y="confirmed",
             color='confirmed',
             hover_name="province_name",
             title='Global COVID-19 Infections over time')
fig.update(layout_coloraxis_showscale=False)
fig.show()

