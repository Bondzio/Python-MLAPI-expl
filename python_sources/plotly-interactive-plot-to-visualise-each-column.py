#!/usr/bin/env python
# coding: utf-8

# Movinga Exploratory Data Analysis
# =====================================
# **Author**: `Anjukan Kathirgamanathan <https://github.com/anjukan>`
# **Date**: 04/02/2020
# 
# 
# This tutorial shows how to visualise the Movinga data in an interactive plotly plot with a dropdown menu.
# 
# **Packages**

# In[ ]:


# General Packages
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Packages for Plotting
import plotly.graph_objects as go
import plotly.offline as offline
from plotly.offline import init_notebook_mode, iplot
from plotly.graph_objs import Scatter, Figure, Layout
offline.init_notebook_mode()
import IPython.display
from IPython.display import HTML, Image
init_notebook_mode(connected=True)


# **Load Data**

# In[ ]:


# Load the data
df = pd.read_csv("/kaggle/input/movinga-best-cities-for-families-2019/Movinga_best_cities.csv")

# Inspect the data
print(df.info())


# **Format Data**

# In[ ]:


# Convert required columns to float and select only columns that we will be plotting
cols=[i for i in df.columns if i not in ["City","Country","Lat","Long"]]
for col in cols:
    df[col]=pd.to_numeric(df[col])


# **Set up Plot**

# In[ ]:


# Initialise lists for storing plot data
data = []
list_updatemenus = []

# For every indicator, set visibility and labelling properties
for n, indicator in enumerate(cols):
    visible = [False] * len(cols)
    visible[n] = True
    temp_dict = dict(label = str(indicator),
                 method = 'update',
                 args = [{'visible': visible},
                         {'title': 'Best Cities for Families 2019<br>Source: <a href=https://www.movinga.de/en/cities-of-opportunity-for-families>Movinga</a><br>Indicator :' + indicator},
                        ])
    list_updatemenus.append(temp_dict)


# In[ ]:


# Create the individual plots for every indicator
for indicator in cols:
    trace = (go.Scattergeo(
    name = str(indicator),
    lon = df['Long'],
    lat = df['Lat'],
    text = df['City'] + ' , ' + df['Country'] + ' , ' + indicator + ' : ' + df[indicator].astype(str),
    mode = 'markers',
    hoverinfo = 'text',
    marker = dict(
        size = 20,
        opacity = 0.8,
        reversescale = True,
        autocolorscale = False,
        symbol = 'circle',
        line = dict(
            width=1,
            color='rgba(102, 102, 102)'
        ),
        colorscale = 'Bluered',
            cmin = 0,
            color = df[indicator],
            cmax = df[indicator].max(),
            colorbar_title = indicator
    )))
    data.append(trace)


# In[ ]:


# Select initial plot on render
data[13]['visible'] = True

# Specify layout properties of the figure such as dropdown button location and title
layout = dict(updatemenus=list([
            dict(buttons= list_updatemenus, direction="down",
            #pad={"r": 0, "t": 0},
            showactive=False,
            x=0.9,
            xanchor="left",
            y=1.15,
            yanchor="top")
            ]),
            title='Best Cities for Families 2019<br>Source: <a href=https://www.movinga.de/en/cities-of-opportunity-for-families>Movinga</a><br>Indicator : Total', title_x=0.5, showlegend = False)
fig = dict(data=data, layout=layout)

# Plot
offline.iplot(fig, filename='movinga')


# It's as easy as that to create an interactive plotly plot. I think it's a good use of an interactive plot compared to a static plot as it allows you to focus on the criteria that matters to you without being lost in all the columns. I'm pretty happy with how the plot came out although notice that there seem to be several legends overlapping each other on the first default plot rendered. I haven't been able to fix this yet so if you find a way, please let me know! I also created a dash version of this same plot using the plotly dash functionality. It's hosted on heroku [here](https://movinga-cities-dash-app.herokuapp.com/). I shall share the code for that later. Anyway, let me know what you think or if you have any suggestions!
