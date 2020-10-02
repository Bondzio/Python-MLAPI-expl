#!/usr/bin/env python
# coding: utf-8

#  # 1.Remaining COVID Cases Per Country 

# In[ ]:


import pandas as pd
import plotly.express as px

df = pd.read_csv('../input/novel-corona-virus-2019-dataset/covid_19_data.csv',header = 0)
df = df.groupby(['ObservationDate','Country/Region']).sum().reset_index()
df['daily_existing'] = df['Confirmed'].values-df['Deaths'].diff()-df['Recovered'].diff()

fig = px.choropleth(df,locations= 'Country/Region', locationmode = 'country names', color = 'daily_existing', hover_name = 'Country/Region',animation_frame='ObservationDate',color_continuous_scale ='Inferno', range_color = (0.1,10000.))
fig.update_layout(title_text='Chu Tianru ',title_x=0.5)
fig.show()


# # 2.Hourly global map **on the day of April 2015 Nepal Earthquake(2015.4.25)**

# In[ ]:


df = pd.read_csv('../input/2015425-earthquakes/query.csv',header = 0)

df.index = pd.to_datetime(df['time'])
df['time'] = df.index.strftime('%y-%m-%d %H:00:00')
fig = px.scatter_geo(df, lat='latitude',lon='longitude',color='mag',animation_frame='time',color_continuous_scale ='Inferno', range_color = (5.,7.))
fig.show()

