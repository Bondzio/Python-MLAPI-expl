#!/usr/bin/env python
# coding: utf-8

# # Day-to-day cases of Corona Virus Worldwide(country-vased)
# We will be using ploty for this exercise.

# In[ ]:


import pandas as pd
import plotly.express as px

df = pd.read_csv('../input/novel-corona-virus-2019-dataset/covid_19_data.csv',header=0)
df = df.groupby(['ObservationDate','Country/Region']).sum().reset_index()

df['daily_existing'] = df['Confirmed'].values-df['Deaths'].diff()-df['Recovered'].diff()

fig = px.choropleth(df,locations='Country/Region',locationmode='country names',color='daily_existing',hover_name='Country/Region',animation_frame='ObservationDate',color_continuous_scale='Burg',range_color=(0.1,200000.))
fig.update_layout(title_text='Remaining Confirmed Cases per Country of each day',title_x=0.5)
fig.show()


# # Hourly global map of earthquake epicenters
# 

# In[ ]:


df = pd.read_csv('../input/earthquake/query(1).csv',header=0)

df.index = pd.to_datetime(df['time'])
df['time'] = df.index.strftime('%y-%m-%d %H:00:00')
fig = px.scatter_geo(df,lat='latitude',lon='longitude',color='mag',animation_frame='time',color_continuous_scale='Rainbow',range_color=(5.,8.))
fig.show()

