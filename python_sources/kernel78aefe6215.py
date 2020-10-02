#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()
get_ipython().run_line_magic('matplotlib', 'inline')

import plotly.offline as py
from plotly import tools
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go


# In[ ]:


df = pd.read_csv("../input/chennai_reservoir_levels.csv")
df["Date"] = pd.to_datetime(df["Date"], format='%d-%m-%Y')
df.head()


# In[ ]:


import datetime

def scatter_plot(cnt_srs, color):
    trace = go.Scatter(
        x=cnt_srs.index[::-1],
        y=cnt_srs.values[::-1],
        showlegend=False,
        marker=dict(
            color=color,
        ),
    )
    return trace

cnt_srs = df["POONDI"]
cnt_srs.index = df["Date"]
trace1 = scatter_plot(cnt_srs, 'red')

cnt_srs = df["CHOLAVARAM"]
cnt_srs.index = df["Date"]
trace2 = scatter_plot(cnt_srs, 'blue')

cnt_srs = df["REDHILLS"]
cnt_srs.index = df["Date"]
trace3 = scatter_plot(cnt_srs, 'green')

cnt_srs = df["CHEMBARAMBAKKAM"]
cnt_srs.index = df["Date"]
trace4 = scatter_plot(cnt_srs, 'purple')

subtitles = ["Water Availability in Poondi reservoir - in mcft",
             "Water Availability in Cholavaram reservoir - in mcft",
             "Water Availability in Redhills reservoir - in mcft",
             "Water Availability in Chembarambakkam reservoir - in mcft"
            ]
fig = tools.make_subplots(rows=4, cols=1, vertical_spacing=0.08,
                          subplot_titles=subtitles)
fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 2, 1)
fig.append_trace(trace3, 3, 1)
fig.append_trace(trace4, 4, 1)
fig['layout'].update(height=1200, width=800, paper_bgcolor='rgb(233,233,233)')
py.iplot(fig, filename='h2o-plots')


# In[ ]:


df["total"] = df["POONDI"] + df["CHOLAVARAM"] + df["REDHILLS"] + df["CHEMBARAMBAKKAM"]
df["total"] = df["POONDI"] + df["CHOLAVARAM"] + df["REDHILLS"] + df["CHEMBARAMBAKKAM"]

cnt_srs = df["total"]
cnt_srs.index = df["Date"]
trace5 = scatter_plot(cnt_srs, 'red')

fig = tools.make_subplots(rows=1, cols=1, vertical_spacing=0.08,
                          subplot_titles=["Total water availability from all four reservoirs - in mcft"])
fig.append_trace(trace5, 1, 1)


fig['layout'].update(height=400, width=800, paper_bgcolor='rgb(233,233,233)')
py.iplot(fig, filename='h2o-plots')

