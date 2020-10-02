#!/usr/bin/env python
# coding: utf-8

# # COVID-19: A Starter EDA and Forecast
# 
# ---

# ## Imports

# In[ ]:


import plotly.graph_objects as go
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import os


# In[ ]:


df = pd.read_csv('../input/novel-corona-virus-2019-dataset/covid_19_data.csv',parse_dates=['Last Update'])
df.rename(columns={'ObservationDate':'Date', 'Country/Region':'Country'}, inplace=True)

df_confirmed = pd.read_csv("/kaggle/input/novel-corona-virus-2019-dataset/time_series_covid_19_confirmed.csv")
df_recovered = pd.read_csv("/kaggle/input/novel-corona-virus-2019-dataset/time_series_covid_19_recovered.csv")
df_deaths = pd.read_csv("/kaggle/input/novel-corona-virus-2019-dataset/time_series_covid_19_deaths.csv")

df_confirmed.rename(columns={'Country/Region':'Country'}, inplace=True)
df_recovered.rename(columns={'Country/Region':'Country'}, inplace=True)
df_deaths.rename(columns={'Country/Region':'Country'}, inplace=True)
df_confirmed.head()


# # Starting EDA

# ## In the US

# In[ ]:


fig = go.Figure()
fig.add_trace(go.Bar(x=df['Date'],
                y=df['Confirmed'],
                name='Confirmed',
                marker_color='purple'
                ))

fig.update_layout(
    title='Worldwide Corona Virus Cases - Confirmed',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Number of Cases',
        titlefont_size=16,
        tickfont_size=14,
    )

)
fig.show()


# There is a steady increase over time when it comes to confirmed cases.

# In[ ]:


fig = go.Figure()
fig.add_trace(go.Bar(x=df['Date'],
                y=df['Deaths'],
                name='Deaths',
                marker_color='black'
                ))

fig.update_layout(
    title='Worldwide Corona Virus Cases - Deaths',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Number of Cases',
        titlefont_size=16,
        tickfont_size=14,
    )

)
fig.show()


# A specific look at the USA shows that:

# In[ ]:


df_us = pd.read_csv("../input/covid19-in-usa/us_covid19_daily.csv")
df_us_reg = pd.read_csv("../input/covid19-in-usa/us_states_covid19_daily.csv")


# In[ ]:


fig = go.Figure()
fig.add_trace(go.Bar(x=df_us['date'],
                y=df_us['positive'],
                name='Confirmed in USA',
                marker_color='purple'
                ))

fig.update_layout(
    title='Corona Virus Cases - Confirmed in USA',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Number of Cases',
        titlefont_size=16,
        tickfont_size=14,
    )

)
fig.show()


# > In the USA, cases have been steadily rising. Let's look at deaths now:

# In[ ]:


fig = go.Figure()
fig.add_trace(go.Bar(x=df_us['date'],
                y=df_us['death'],
                name='Deaths in USA',
                marker_color='red'
                ))

fig.update_layout(
    title='Corona Virus Cases - Deaths in USA',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Number of Cases',
        titlefont_size=16,
        tickfont_size=14,
    )

)
fig.show()


# ---
# 
# ---

# In[ ]:


sns.clustermap(df.corr())


# # **Forecasting: Part 1. Prophet**
# 
# ---

# We'll use Facebook's prophet library to forecast cases.

# In[ ]:


import fbprophet as fb


# For prophet to work, we must rename date to `ds` and `Confirmed` to `y`.

# In[ ]:


df["ds"] = df["Date"]
df["y"] = df["Confirmed"]


# In[ ]:


model = fb.Prophet(yearly_seasonality=True) 
model.fit(df)


# Let's make future dataframe and have a look.

# In[ ]:


future = model.make_future_dataframe(periods = 10, freq = 'MS')  
# now lets make the forecasts
forecast = model.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()


# Well, looks like the future is, well, grim to say the least of the current situation.

# ---

# In[ ]:


fig = go.Figure()
fig.add_trace(go.Bar(x=forecast['ds'],
                y=forecast['yhat'],
                name='Predicted Cases',
                marker_color='red'
                ))

fig.update_layout(
    title='Corona Virus Cases - Our Prediction',
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='Number of Cases',
        titlefont_size=16,
        tickfont_size=14,
    )

)
fig.show()


# In[ ]:


model.plot(forecast)


# ---
# 
# # This is a work in progress. If you like it, please upvote!
# 
# ---
