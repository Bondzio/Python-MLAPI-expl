#!/usr/bin/env python
# coding: utf-8

# # Day-to day cases of Corona Virus Worldwide(country-based)
# we will be using plotly gor this exercise.

# In[ ]:


import pandas as pd
import plotly.express as px

df = pd.read_csv('../input/novel-corona-virus-2019-dataset/covid_19_data.csv',header=0)
df = df.groupby(['ObservationDate','Country/Region']).sum().reset_index()

df['daily_existing'] = df['Confirmed'].values-df['Deaths'].diff()-df['Recovered'].diff()

fig = px.choropleth(df,locations='Country/Region',locationmode='country names',color='Confirmed',hover_name='Country/Region',animation_frame='ObservationDate',color_continuous_scale='Plasma',range_color=(0.1,300000))
fig.update_layout(title_text='Confirmed Cumulative Cases per Country Takafumi Sakuma',title_x=0.5)
fig.show()


# # Hourly golbal map of earthquake epicenters
# reference
# https://earthquake.usgs.gov/earthquakes/search/

# In[ ]:


df=pd.read_csv('../input/april-25-2015-earthquake/Nepal_query.csv')

df.index = pd.to_datetime(df['time'])
df['time'] = df.index.strftime('%Y-%m-%d %H:00:00')
fig = px.scatter_geo(df,lat='latitude',lon='longitude',color='mag',animation_frame='time',color_continuous_scale='oryel',range_color=(4.,7.))
fig.show()

