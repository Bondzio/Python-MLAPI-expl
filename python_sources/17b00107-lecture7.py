#!/usr/bin/env python
# coding: utf-8

# # COVID-19 Day-to-day cases

# In[ ]:


import pandas as pd
import numpy as np

import plotly.express as px


# In[ ]:


df = pd.read_csv("/kaggle/input/novel-corona-virus-2019-dataset/covid_19_data.csv")
df = df.groupby(['ObservationDate', 'Country/Region']).sum().reset_index()

df['daily_existing'] = df['Confirmed'].values-df['Deaths'].diff() - df['Recovered'].diff()

#fig = px.choropleth(df,locations='Country/Region',locationmode='country names',color='Confirmed',hover_name='Country/Region',
                    #animation_frame='ObservationDate',color_continuous_scale='jet')

#fig.update_layout(title_text='Confirmed Cumulative Cases per Country',title_x=0.5)

fig = px.choropleth(df,locations='Country/Region',locationmode='country names',color='daily_existing',hover_name='Country/Region',
                    animation_frame='ObservationDate',color_continuous_scale='jet',range_color=(0,300000))

fig.update_layout(title_text='Remaining Confirmed Cases per Country',title_x=0.5)
fig.show()


# # Earthquakes Data

# - source: https://earthquake.usgs.gov/earthquakes/search/
# - date: April 25, 2015.

# In[ ]:


df = pd.read_csv('/kaggle/input/nepal-earthquake-data/query.csv')

df.index = pd.to_datetime(df['time'])
df['time_col'] = df.index.strftime('%Y-%m-%d %H:00:00') #get string from datetime object


# In[ ]:


df.head()


# In[ ]:


df.columns


# # Exploratory Data Analysis on the Earthquakes Data

# ## 1. On April 25, in which countries/area did the earthquakes happened?

# In[ ]:


df['country'] = df['place'].apply(lambda x: x.split(',')[1] if len(x.split(','))==2 else x.split(',')[0] )
df['country'].unique()


# ## 2. Earthquakes by magnitude (Top 10)

# In[ ]:


df.sort_values(by='mag',ascending=False)[['place','mag']].head(10)


# ## Interactive Map

# In[ ]:


#use scatter_geo
fig = px.scatter_geo(df,lat='latitude',lon='longitude',color='mag',animation_frame='time',color_continuous_scale='Rainbow',range_color=(5.,7.))
fig.show()


# In[ ]:





# In[ ]:





# In[ ]:




