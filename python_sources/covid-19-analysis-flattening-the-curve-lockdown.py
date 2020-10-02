#!/usr/bin/env python
# coding: utf-8

# # COVID'19 Analysis: Before Lockdown & After 50 Days of Lockdown all over the world

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
import matplotlib.pyplot as plt
import matplotlib
import plotly.express as px
from sklearn.preprocessing import StandardScaler
import os
import plotly.io as pio;
pio.renderers.default='notebook'

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session 


# In[ ]:


# Display output not only of last command but all commands in a cell
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# In[ ]:


# Set pandas options to display results
pd.options.display.max_rows = 1000
pd.options.display.max_columns = 1000


# In[ ]:


os.chdir('/kaggle/input/covid19/')
os.listdir()


# In[ ]:


ad1 = pd.read_csv("LockdownBef.csv")
ad1.head()

sns.jointplot(ad1.Cases,
              ad1.Death,
              kind = "kde"
              )


# In[ ]:


ad = pd.read_csv("World.csv")
ad.head()
         # 2.2 Check data types of attributes
ad.dtypes

# 2.3 Some more dataset related information
ad.info()               # Also informs how much memory dataset takes
                        #   and status of nulls

ad.memory_usage()

ad.shape                
ad.columns.values
len(ad.columns)         

len(ad.Country.unique())                
ad.Country.value_counts()               


# *** STATUS OF COVID 19 : BEFORE STARTING OF LOCKDOWN ***

# In[ ]:


##################
# Plotting
##################
px.histogram(data_frame = ad,
                     x  = 'Country',
                     y  = 'Death%',  # Ht to be decided as per histfunc()
                     histfunc = 'avg'   # One of 'count', 'sum', 'avg', 'min', or 'max'
             )

sns.distplot(ad.Infected)


# In[ ]:


sns.distplot(ad.Death)
px.histogram(data_frame = ad,
                     x  = 'Country',
                     y  = 'Recovered%',  # Ht to be decided as per histfunc()
                     histfunc = 'avg',   # One of 'count', 'sum', 'avg', 'min', or 'max'
                         marginal = 'violin'
            )


# In[ ]:


px.histogram(data_frame =ad,
             x = 'Country',
             facet_row = 'Death%',
             )


# In[ ]:


px.density_contour(
                   data_frame =ad,
                   x = 'Infected',
                   y = 'Death',
                   )


# In[ ]:


px.density_contour(
                   data_frame =ad,
                   x = 'Recovered',
                   y = 'Death',
                   )


# In[ ]:


fig = px.density_contour(
                         data_frame =ad,
                         x = 'Country',
                         y = 'Recovered%',
                         z ='Death%',
                        )
fig.update_traces(
                  contours_coloring="fill",
                  contours_showlabels = True
                 )


# In[ ]:


ad1 = pd.read_csv("LockdownBef.csv")
ad.head()
fig = px.density_contour(
                         data_frame =ad1,
                         x = 'Country',
                         y = 'Cases',
                         z ='Death'
                        )
fig.update_traces(
                  contours_coloring="fill",
                  contours_showlabels = True
                 )


# In[ ]:


ad2= pd.read_csv("ReliefPackageGDP.csv")
ad2.head()


# **STATUS OF COVID 19:AFTER 50TH DAY OF LOCKDOWN COMPLETION**

# In[ ]:


px.histogram(data_frame = ad2,
                     x  = 'Country',
                     y  = 'Package%VsGDP',  # Ht to be decided as per histfunc()
                     histfunc = 'avg'   # One of 'count', 'sum', 'avg', 'min', or 'max'
             )


# In[ ]:


sns.jointplot(ad.Infected,
              ad.Death,
              kind = "hex"
              )


# In[ ]:


ad3 = pd.read_csv("LockdownAfter.csv")
ad3.head()

sns.jointplot(ad3.Cases,
              ad3.Death,
              kind = "kde"
              )


# In[ ]:


ad4 = pd.read_csv("India.csv")
ad4.head()


# In[ ]:


import numpy as np                   # for multi-dimensional containers 
import pandas as pd                  # for DataFrames
import plotly.graph_objects as go    # for data visualisation
import plotly.io as pio              # to set shahin plot layout
import plotly.express as px
import os


# In[ ]:


access_token = 'pk.eyJ1IjoidmluZWV0dml2ZWsiLCJhIjoiY2thNmhycXRoMDcyejJxbGVwbmljZ3B6cSJ9.sPysD0hYOgxXvPEVYrmy9A'
px.set_mapbox_access_token(access_token)


# # Today 28.05.2020, Statewise CORONA update :-

# In[ ]:


data = pd.read_csv("Statewise270520.csv")
data.head()
data.shape   
data.columns.values


# In[ ]:


data.head()
data.info()


# In[ ]:


missing_states = pd.isnull(data['STATE'])
missing_states
# 3.2
data.loc[missing_states,'STATE'] = data.loc[missing_states,'STATE']


# In[ ]:


data.shape
#data = data.dropna()
data.head()


# In[ ]:


state_mask = data['STATE'] == data['STATE'].max()


# In[ ]:


fig = px.scatter_mapbox(
                        data,
                        lat="LAT",
                        lon="LONG",
                        size="DEAD",    # Size of bubble
                        size_max=75,         # Limit max size of bubble to this value
                        color="DEAD",
                        color_continuous_scale=px.colors.sequential.Pinkyl,
                        hover_name="STATE",           
                        mapbox_style='dark',
                        zoom=5,
                        width=900,
                        height=900
                     )


# In[ ]:


fig.layout.coloraxis.showscale = False


# In[ ]:


fig.show()


# In[ ]:


fig = px.scatter_mapbox(
                        data,
                        lat="LAT",
                        lon="LONG",
                        size="DEAD",
                        size_max=75,
                        color="DEAD",
                        color_continuous_scale=px.colors.sequential.Pinkyl,
                        hover_name="STATE",           
                        mapbox_style='dark',
                        zoom=5,
                        width=800,
                        height=800,
                        animation_frame="STATE",
                        animation_group="STATE"
                     )


# In[ ]:


fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 1000
fig.layout.coloraxis.showscale = False
fig.layout.sliders[0].pad.t = 10
fig.layout.updatemenus[0].pad.t= 10
fig.show()


# # Remember, CORONA is very dangerous. So, Stay Safe.
# # Jaan Hai, Jahaan Hai..
# # Take Care 
# # Thank you for giving ur valuable time/feedback

# In[ ]:




