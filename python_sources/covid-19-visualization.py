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


import numpy as np
import pandas as pd


# In[ ]:


import plotly as py
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)


# In[ ]:


df = pd.read_csv("/kaggle/input/covid_19_data.csv")


# In[ ]:


df.columns


# In[ ]:


df = df.rename(columns={'Country/Region':'Country'})
df = df.rename(columns={'ObservationDate':'Date'})


# In[ ]:


df


# In[ ]:


df_countries = df.groupby(['Country', 'Date']).sum().reset_index().sort_values('Date', ascending=False)


# In[ ]:


df_countries


# In[ ]:


df_countries['Country'].value_counts()


# In[ ]:


df_countries = df_countries.drop_duplicates(subset = ['Country'])


# In[ ]:


df_countries


# In[ ]:


df_countries = df_countries[df_countries['Confirmed']>0]


# In[ ]:


df_countries


# In[ ]:


fig = go.Figure(data=go.Choropleth(
    locations = df_countries['Country'],
    locationmode = 'country names',
    z = df_countries['Confirmed'],
    colorscale = 'reds',
    marker_line_color = 'black',
    marker_line_width = 0.5,
))
fig.update_layout()


# In[ ]:


df_countrydate = df.groupby(['Date','Country']).sum().reset_index()
df_countrydate


# In[ ]:


fig = px.choropleth(df_countrydate, 
                    locations="Country", 
                    locationmode = "country names",
                    color="Confirmed", 
                    hover_name="Country", 
                    animation_frame="Date"
                   )
fig.update_layout(
    title_text = 'Global Spread of Coronavirus',
    title_x = 0.5,
    geo=dict(
        showframe = False,
        showcoastlines = False,
    ))
    
fig.show()


# In[ ]:




