#!/usr/bin/env python
# coding: utf-8

# ># <font color="#e23e57"><b>Introduction</b></font>
# In this **kernel**, we will study the city of Barcelona. We will take a look at Barcelona's **population** and **transport** system.
# 

# ># <font color="#e23e57"><b>Loading required libraries and all datasets</b></font>

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

import plotly
import plotly.plotly as py
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.offline as offline
offline.init_notebook_mode()

# lib for the map
import folium

import os
print(os.listdir("../input"))


# ># <font color="#e23e57"><b>Barcelona Population</b></font>

# In[ ]:


# import population dataset and display header
population_df = pd.read_csv("../input/population.csv")
population_df.head()


# In[ ]:


population_df.info()


# In[ ]:


total_pop = population_df.loc[population_df['Year'] == 2017]['Number'].sum()
f'Total Population of Barcelona = {total_pop}'


# In[ ]:


temp_df = population_df.loc[population_df['Year'] == 2017].groupby(['Gender'])['Number'].sum()

trace = go.Pie(labels = temp_df.index,
               values = temp_df.values,
               marker = dict(colors=['#E53916','#2067AD'], line = dict(color='#FFFFFF', width=2.5))
              )

data = [trace]
layout = go.Layout(title="Gender-Wise Distribution for Year-2017")
fig = go.Figure(data=data, layout=layout)

plotly.offline.iplot(fig)


# In[ ]:


male = population_df.loc[population_df['Gender'] == 'Male'].groupby(['Year'])['Number'].sum()
female = population_df.loc[population_df['Gender'] == 'Female'].groupby(['Year'])['Number'].sum()

trace0 = go.Bar(x = male.index,
                y= male.values,
                name = "Male",
                marker = dict(color='rgb(236,154,41)'),
                opacity = 0.8
               )

trace1 = go.Bar(x = female.index,
                y = female.values,
                name = "Female",
                marker = dict(color='rgb(168,32,26)'),
                opacity = 0.8
               )

data = [trace0,trace1]
layout = go.Layout(barmode = 'group',
                   xaxis = dict(tickangle=-30),
                   title="Gender-Wise Distribution Across the Years",
                      )
fig = go.Figure(data=data,layout=layout)

plotly.offline.iplot(fig)


# # <font color="#e23e57">Conclusion</font>
# 1. Women outnumber men.
# 2. Over the five years, there has not been significant change in the population of the city.

# # <font color="#e23e57">Which district holds the highest number of population?</font>

# In[ ]:


dist_df = population_df.loc[population_df['Year'] == 2017].groupby(['District.Name'])['Number'].sum()

trace0 = go.Bar(x = dist_df.index,
                y = dist_df.values,
                marker = dict(color=list(dist_df.values),
                                  colorscale='Reds'),
                )

data = [trace0]
layout = go.Layout(xaxis = dict(tickangle=-30),
                   title="District-Wise Distribution of population (Year 2017)",
                      )
fig = go.Figure(data=data,layout=layout)

plotly.offline.iplot(fig)


# # <font color="#e23e57">Conclusion</font>
#  **Eixample** is the most populated district in the city and **Les Corts** the less.

# ># <font color="#e23e57"><b>Transport</b></font>

# In[ ]:


transport_df =pd.read_csv("../input/transports.csv")
transport_df.head()


# # <font color="#e23e57"><b>Metro Location</b></font>

# In[ ]:


metro = transport_df.loc[transport_df['Transport'] == 'Underground']
metro = metro[['Latitude','Longitude','Station']]

barcelona_coordinates = [41.3851, 2.1734]

map_metro = folium.Map(location=barcelona_coordinates, tiles='OpenStreetMap', zoom_start=12)

for elem in metro.iterrows():
    folium.CircleMarker([elem[1]['Latitude'],elem[1]['Longitude']],
                        radius=5,
                        color='blue',
                        popup=elem[1]['Station'],
                        fill=True).add_to(map_metro)
map_metro


# # <font color="#e23e57"><b>Bus Location</b></font>

# In[ ]:


busstop_df =pd.read_csv("../input/bus_stops.csv")
busstop_df.head()


# In[ ]:


bus = busstop_df.loc[busstop_df['Transport'] == 'Day bus stop']

map_bus = folium.Map(location=barcelona_coordinates, tiles='OpenStreetMap', zoom_start=12)

for elem in bus[:100].iterrows():
    folium.Marker([elem[1]['Latitude'],elem[1]['Longitude']],
                  popup=str(elem[1]['Bus.Stop']),
                  icon=folium.Icon(color='blue', icon='stop')).add_to(map_bus)
    
map_bus

