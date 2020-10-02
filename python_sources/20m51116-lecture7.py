#!/usr/bin/env python
# coding: utf-8

# # Day-to-day cases of Corona Virus worldwide (country-based)
# 
# We will be using plotly for this exercise.

# In[ ]:


import pandas as pd
import plotly.express as px

df = pd.read_csv('../input/novel-corona-virus-2019-dataset/covid_19_data.csv', header = 0)
df = df.groupby(['ObservationDate','Country/Region']).sum().reset_index()

df['daily_existing'] = df['Confirmed'].values-df['Deaths'].diff()-df['Recovered'].diff()

fig = px.choropleth(df,locations='Country/Region',locationmode='country names',color='Confirmed',hover_name='Country/Region',animation_frame='ObservationDate',color_continuous_scale='Reds',range_color=(0.1,300000.))
fig.update_layout(title_text='Ryohei Ogawa',title_x=0.5)
fig.show()


# # Hourly grobal map of earthquake epicenters

# In[ ]:


df = pd.read_csv('../input/march-11-2011-earthquake-oldest/query_new.csv', header = 0)

df.index = pd.to_datetime(df['time'])
df['time'] = df.index.strftime('%Y-%m-%d %H:00:00')
fig = px.scatter_geo(df, lat='latitude', lon='longitude', color='mag', animation_frame='time', color_continuous_scale='Aggrnyl', range_color=(5.,7.))
fig.update_layout(title_text='Locations happened more than 5 degree of magnitude in March 11, 2011',title_x=0.5)
fig.show()

