#!/usr/bin/env python
# coding: utf-8

# ## Chennai
# Chennai is the capital of the Indian state of Tamil Nadu.
# . Located on the Coromandel Coast off the Bay of Bengal, it is the biggest cultural, economic and educational centre of south India. According to the 2011 Indian census, it is the sixth-most populous city and fourth-most populous urban agglomeration in India [[1]](https://en.wikipedia.org/wiki/Chennai).
# 
#  <img src="https://i.ibb.co/h1WtMs5/Chennai-Map.png" width="600" height="500" />

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

import os
print(os.listdir("../input"))

import plotly.offline as py
import plotly.graph_objs as go
py.init_notebook_mode(connected=True)


# In[ ]:


PATH_levels = "../input/chennai_reservoir_levels.csv"
PATH_rainfall = "../input/chennai_reservoir_rainfall.csv"
levels = pd.read_csv(PATH_levels)
rainfall = pd.read_csv(PATH_rainfall)

levels.Date = pd.to_datetime(levels.Date,format='%d-%m-%Y')
rainfall.Date = pd.to_datetime(rainfall.Date,format='%d-%m-%Y')

# https://stackoverflow.com/questions/45606458/python-pandas-highlighting-maximum-value-in-column
def highlight_max(data, color='yellow'):
    '''
    highlight the maximum in a Series or DataFrame
    '''
    attr = 'background-color: {}'.format(color)
    #remove % and cast to float
    data = data.replace('%','', regex=True).astype(float)
    if data.ndim == 1:  # Series from .apply(axis=0) or axis=1
        is_max = data == data.max()
        return [attr if v else '' for v in is_max]
    else:  # from .apply(axis=None)
        is_max = data == data.max().max()
        return pd.DataFrame(np.where(is_max, attr, ''),
                            index=data.index, columns=data.columns)


# # Major Water Sources of Chennai
# * Poondi
# * Cholavaram
# * Redhills
# * Chembarambakkam

# In[ ]:


display(levels.head(),rainfall.head())


# From the graph, it is noticeable that water levels are lowest during May-July, while they peak in Nov-Jan.

# # Average Water Levels (2004-2019)

# In[ ]:


trace2 = go.Bar(x = [levels.POONDI.mean()],y = ["Total Volume"],name = "Poondi",orientation = 'h',width=0.3,marker = dict(color = 'rgba(246, 78, 139, 0.6)',
        line = dict(
            color = 'rgba(246, 78, 139, 1.0)',width=3)))
trace1 = go.Bar(x = [levels.REDHILLS.mean()],y = ["Total Volume"],name = "Redhills",orientation = 'h',width=0.3,marker = dict(color = 'rgba(58, 71, 80, 0.6)',
        line = dict(
            color = 'rgba(58, 71, 80, 1.0)',width=3)))

trace4 = go.Bar(x = [levels.CHOLAVARAM.mean()],y = ["Total Volume"],name = "Cholavaram",orientation = 'h',width=0.3,marker = dict(color = 'rgba(120, 100, 180, 0.6)',
        line = dict(
            color = 'rgba(120, 100, 180, 1.0)',width=3)))
trace3 = go.Bar(x = [levels.CHEMBARAMBAKKAM.mean()],y = ["Total Volume"],name = "Chembarambakkam",orientation = 'h',width=0.3,marker = dict(color = 'rgba(58, 190, 120, 0.6)',
        line = dict(
            color = 'rgba(58, 190, 120, 1.0)',width=3)))

data = [trace1,trace2,trace3,trace4]
layout = go.Layout(
    barmode='stack'
)
fig = go.Figure(data=data,layout=layout)
py.iplot(fig)


# In[ ]:


trace1 = go.Scatter(x=levels.Date[:],y=levels.POONDI[:],name='POONDI')
trace2 = go.Scatter(x=levels.Date[:],y=levels.CHOLAVARAM[:],name="CHOLAVARAM")
trace3 = go.Scatter(x=levels.Date[:],y=levels.REDHILLS[:],name="REDHILLS")
trace4 = go.Scatter(x=levels.Date[:],y=levels.CHEMBARAMBAKKAM[:],name="CHEMBARAMBAKKAM")
data=[trace1,trace2,trace3,trace4]

title = go.Layout(title = go.layout.Title(text =  "Water Levels in the major reservoirs (mcft)"))
fig = go.Figure(data = data,layout = title)
py.iplot(fig)


# ### Rainfall peaks during Nov-Jan season.

# In[ ]:


trace5 = go.Scatter(x=rainfall.Date[:],y=rainfall.POONDI[:],name = "POONDI Rainfall")
trace6 = go.Scatter(x=rainfall.Date[:],y=rainfall.CHOLAVARAM[:],name = "Cholavaram Rainfall")
trace7 = go.Scatter(x=rainfall.Date[:],y=rainfall.REDHILLS[:],name = "Redhill Rainfall")
trace8 = go.Scatter(x=rainfall.Date[:],y=rainfall.CHEMBARAMBAKKAM[:],name = "Chembarambakkam Rainfall")

layout = go.Layout(title = go.layout.Title(text="Rainfall (mm)"))
data = [trace5,trace6,trace7,trace8]

fig = go.Figure(data=data,layout=layout)

py.iplot(fig)


# # Highest Average Monthly Rainfall Recorded in a Year
# 
# Novembor 2015 Recorded the Highest Rainfall ever in Chennai. This was during the [South India Floods of 2015](https://en.wikipedia.org/wiki/2015_South_Indian_floods)

# In[ ]:


high_rain = rainfall.groupby(pd.Grouper(key="Date",freq="m")).mean().sort_values(by="POONDI",ascending=False).head(5)
high_rain.style.apply(highlight_max)


# ### Highest Average Monthly Rainfall Recorded
# November marks the highest rainfall season in Chennai

# In[ ]:


monthly_rain = rainfall.groupby(rainfall.Date.dt.month).mean()
monthly_rain.index.name="Month"
monthly_rain.style.apply(highlight_max)


# # Highest Average Monthly Water Levels Recorded
# December records the highest water levels in the reservoirs. This can be attributed to the heavy rainfalls in the month of November.

# In[ ]:


monthly_levels = levels.groupby(levels.Date.dt.month).mean()
monthly_levels.index.name = "Month"
display(monthly_levels.style.apply(highlight_max))


# # Monthly Water level of Reservoirs in 2019
# 
# As of June 2019, Cholavaram,Redhills and Chembarambakkam Reservoirs are empty.

# In[ ]:


import calendar

levels_2019 = levels[levels.Date.dt.year == 2019]

trace9 = go.Scatter(x=levels_2019.Date[:],y=levels_2019.POONDI[:],name="Poondi")
trace10 = go.Scatter(x=levels_2019.Date[:],y=levels_2019.CHOLAVARAM[:],name="Cholavaram")
trace11 = go.Scatter(x=levels_2019.Date[:],y=levels_2019.REDHILLS[:],name="Redhills")
trace12 = go.Scatter(x=levels_2019.Date[:],y=levels_2019.CHEMBARAMBAKKAM[:],name="Chembarambakkam")

data = [trace9,trace10,trace11,trace12]
py.iplot(data)


# ### Chennai has experience very less rainfall in May, which plays a huge factor in the shortage of water.

# In[ ]:


rainfall_may = rainfall[rainfall.Date.dt.month==5].groupby(rainfall.Date.dt.year).mean()
rainfall_may["Total"] = rainfall_may.POONDI + rainfall_may.REDHILLS + rainfall_may.CHEMBARAMBAKKAM + rainfall_may.CHOLAVARAM
rainfall_may.index.name = "Year"
trace13 = go.Bar(x = rainfall_may.index[:],y=rainfall_may.Total[:],marker=dict(color='rgb(120,160,235)'))
layout = go.Layout(title = go.layout.Title(text="Average Rainfall in May"))
fig = go.Figure(data = [trace13],layout=layout)
py.iplot(fig)


# In[ ]:




