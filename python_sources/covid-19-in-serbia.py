#!/usr/bin/env python
# coding: utf-8

# # Exploratory Data Analysis of Covid-19 Cases in Serbia
# 
# This is just an attempt to visualize Covid-19 spread in Serbia, based on published data. See References for data sources. Notebook will be updated daily, as an updated dataset become available.

# # Background
# 
# To Do:

# # Basic Data Analysis

# In[ ]:


# Project: Novel Corona Virus 2019 Dataset by Kaggle
# Program: COVID-19 in Serbia
# Author:  Radina Nikolic
# Date:    March 20, 2020
#          Added Active Cases and Weeks

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_dark"
from plotly.subplots import make_subplots

import os

# Input data files are available in the "../input/" directory.


# In[ ]:


df_covid = pd.read_csv('/kaggle/input/novel-corona-virus-2019-dataset/covid_19_data.csv',parse_dates=['Last Update'])
df_covid.rename(columns={'ObservationDate':'Date', 'Country/Region':'Country'}, inplace=True)


# Check the latest observation date

# In[ ]:


#Converting date column into correct format
df_covid['Date']=pd.to_datetime(df_covid['Date'])

maxdate=max(df_covid['Date'])

fondate=maxdate.strftime("%Y-%m-%d")
print("The last observation date is {}".format(fondate))
ondate = format(fondate)


# Add Active Cases = Confirmed - Deaths - Recovered

# In[ ]:


#Adding Active cases
df_covid['Active'] = df_covid['Confirmed'] - df_covid['Deaths'] - df_covid['Recovered']
print("Active Cases Column Added Successfully")
df_covid.head()


# # Functions for plotting

# In[ ]:


def plot_bar_chart(confirmed, deaths, recovered, active, country, fig=None):
    if fig is None:
        fig = go.Figure()
    fig.add_trace(go.Bar(x=confirmed['Date'],
                y=confirmed['Confirmed'],
                name='Confirmed'
                ))
    fig.add_trace(go.Bar(x=deaths['Date'],
                y=deaths['Deaths'],
                name='Deaths'
                ))
    fig.add_trace(go.Bar(x=recovered['Date'],
                y=recovered['Recovered'],
                name='Recovered'
                ))
    fig.add_trace(go.Bar(x=active['Date'],
                y=active['Active'],
                name='Active'
                ))

    fig.update_layout(
        title= 'Cumulative Daily Cases of COVID-19 (Confirmed, Deaths, Recovered, Active) - ' + country + ' as of ' + ondate ,
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Number of Cases',
            titlefont_size=14,
            tickfont_size=12,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15, 
        bargroupgap=0.1 
    )
    return fig


# In[ ]:


def plot_line_chart(confirmed, deaths, recovered, active, country, fig=None):
    if fig is None:
        fig = go.Figure()
    fig.add_trace(go.Scatter(x=confirmed['Date'], 
                         y=confirmed['Confirmed'],
                         mode='lines+markers',
                         name='Confirmed'
                         ))
    fig.add_trace(go.Scatter(x=deaths['Date'], 
                         y=deaths['Deaths'],
                         mode='lines+markers',
                         name='Deaths'
                         ))
    fig.add_trace(go.Scatter(x=recovered['Date'], 
                         y=recovered['Recovered'],
                         mode='lines+markers',
                         name='Recovered'
                        ))
    fig.add_trace(go.Scatter(x=active['Date'], 
                         y=active['Active'],
                         mode='lines+markers',
                         name='Active'
                        ))
    fig.update_layout(
        title= 'Number of COVID-19 Cases Over Time - ' + country + ' as of ' + ondate ,
        xaxis_tickfont_size=12,
        yaxis=dict(
           title='Number of Cases',
           titlefont_size=14,
           tickfont_size=12,
        ),
        legend=dict(
           x=0,
           y=1.0,
           bgcolor='rgba(255, 255, 255, 0)',
           bordercolor='rgba(255, 255, 255, 0)'
        )
     )
    return fig


# # What is happening Worldwide

# In[ ]:


confirmed = df_covid.groupby('Date').sum()['Confirmed'].reset_index() 
deaths = df_covid.groupby('Date').sum()['Deaths'].reset_index() 
recovered = df_covid.groupby('Date').sum()['Recovered'].reset_index()
active = df_covid.groupby('Date').sum()['Active'].reset_index()


# In[ ]:


plot_bar_chart(confirmed, deaths, recovered,active, 'Worldwide').show()


# In[ ]:


plot_line_chart(confirmed, deaths, recovered,active, 'Worldwide').show()


# # What is going on in Serbia

# First Cases

# In[ ]:


Serbia_df = df_covid[df_covid['Country'] == 'Serbia'].copy()
Serbia_df.head() 


# The Latest Cases (based on available data)

# In[ ]:


Serbia_df.tail()


# # Visualization

# In[ ]:


confirmed = Serbia_df.groupby('Date').sum()['Confirmed'].reset_index()
deaths = Serbia_df.groupby('Date').sum()['Deaths'].reset_index()
recovered = Serbia_df.groupby('Date').sum()['Recovered'].reset_index()
active = Serbia_df.groupby('Date').sum()['Active'].reset_index()


# In[ ]:


plot_bar_chart(confirmed, deaths, recovered,active,'Serbia').show()


# In[ ]:


plot_line_chart(confirmed, deaths, recovered,active,'Serbia').show()


# As stricter measures were introduced on March 18, 2020, it will be interesting to monitor number of cases in the following days.

# <h4>Weekly Data</h4>

# In[ ]:



#Group by date
Serbia_df=Serbia_df.groupby(['Date']).sum().reset_index()

Serbia_df['Week'] = Serbia_df['Date'].dt.week

Serbia_df.head()


# In[ ]:


#Visualizing Cumaltive trends
fig = go.Figure()
fig.add_trace(go.Scatter(x=Serbia_df['Date'], y=Serbia_df['Confirmed'],
                    mode='lines',name='Confirmed Cases'))
fig.add_trace(go.Scatter(x=Serbia_df['Date'], y=Serbia_df['Deaths'], 
                mode='lines',name='Deaths'))
fig.add_trace(go.Scatter(x=Serbia_df['Date'], y=Serbia_df['Recovered'], 
                mode='lines',name='Recovered Cases'))
fig.add_trace(go.Scatter(x=Serbia_df['Date'], y=Serbia_df['Active'], 
                mode='lines',name='Active'))
  
    
fig.update_layout(title_text='Weekly Trends in Serbia')

fig.show()


# In[ ]:





# # Serbia and Region

# In[ ]:


confirmed = df_covid.groupby(['Date','Country'])['Confirmed'].sum().reset_index()
region =  ["Croatia", "Slovenia","Serbia", "Bosnia and Herzegovina", "North Macedonia", "Montenegro"]


# In[ ]:


fig = go.Figure()
for country in region:
 
    fig.add_trace(go.Scatter(
        x=confirmed[confirmed['Country']==country]['Date'],
        y=confirmed[confirmed['Country']==country]['Confirmed'],
        name = country, # Style name/legend entry with html tags
        connectgaps=True # override default to connect the gaps
    ))
fig.update_layout(title="Number of Confirmed COVID-19 Cases Over Time - Serbia and Region" + ' as of ' + ondate ,)    
fig.show()


# In[ ]:


fig = go.Figure()
for country in region:
 
    fig.add_trace(go.Bar(
        x=confirmed[confirmed['Country']==country]['Date'],
        y=confirmed[confirmed['Country']==country]['Confirmed'],
        name=country
    ))
fig.update_layout(title="Cumulative Daily Cases of COVID-19 (Confirmed) - Serbia and Region"  + ' as of ' + ondate ,)    
fig.show()


# In[ ]:


yu_df = df_covid[df_covid['Country'].isin(region)]
grouped_country = yu_df.groupby(["Country"] ,as_index=False)["Confirmed","Recovered","Deaths"].last().sort_values(by="Confirmed",ascending=False)


# In[ ]:


fig = go.Figure()

fig.add_trace(go.Bar(
    
    y=grouped_country['Country'],
    x=grouped_country['Confirmed'],
    orientation='h',
    text=grouped_country['Confirmed']
    ))
fig.update_traces(textposition='outside')
fig.update_layout(title="Cumulative Number of COVID-19 Confirmed Cases - Serbia and Region" + ' as of ' + ondate)    
fig.show()


# In[ ]:


fig = go.Figure()

trace1 = go.Bar(
    x=grouped_country['Confirmed'],
    y=grouped_country['Country'],
    orientation='h',
    name='Confirmed'
)
trace2 = go.Bar(
    x=grouped_country['Deaths'],
    y=grouped_country['Country'],
    orientation='h',
    name='Deaths'
)
trace3 = go.Bar(
    x=grouped_country['Recovered'],
    y=grouped_country['Country'],
    orientation='h',
    name='Recovered'
)

data = [trace1, trace2, trace3]
layout = go.Layout(
    barmode='stack'
)

fig = go.Figure(data=data, layout=layout)
fig.update_layout(title="Stacked Number of COVID-19 Cases (Confirmed, Deaths, Recoveries) - Serbia and Region" + ' as of ' + ondate)    
fig.show()


# # Serbia and Neighbours

# In[ ]:


confirmed = df_covid.groupby(['Date','Country'])['Confirmed'].sum().reset_index()
neighbours =  ["Croatia", "Slovenia","Serbia", "Bosnia and Herzegovina", "North Macedonia", "Montenegro", "Hungary", "Romania", "Greece","Albania"]


# In[ ]:


fig = go.Figure()
for country in neighbours:
 
    fig.add_trace(go.Scatter(
        x=confirmed[confirmed['Country']==country]['Date'],
        y=confirmed[confirmed['Country']==country]['Confirmed'],
        name = country # Style name/legend entry with html tags
    ))
fig.update_layout(title="Number of Confirmed COVID-19 Cases Over Time - Serbia and Neighbours" + ' as of ' + ondate)    
fig.show()


# In[ ]:


yu_df = df_covid[df_covid['Country'].isin(neighbours)]
grouped_country = yu_df.groupby(["Country"] ,as_index=False)["Confirmed","Recovered","Deaths"].last().sort_values(by="Confirmed",ascending=False)


# In[ ]:


fig = go.Figure()

fig.add_trace(go.Bar(
    
    y=grouped_country['Country'],
    x=grouped_country['Confirmed'],
    orientation='h',
    text=grouped_country['Confirmed']
    ))
fig.update_traces(textposition='outside')
fig.update_layout(title="Cumulative Number of COVID-19 Confirmed Cases - Serbia and Neighbours" + ' as of ' + ondate)    
fig.show()


# # More EU Countries

# In[ ]:


confirmed = df_covid.groupby(['Date','Country'])['Confirmed'].sum().reset_index()
west_neighbours =  ["Austria", "Italy", "Spain", "Germany", "Switzerland"]


# In[ ]:


eu_df = df_covid[df_covid['Country'].isin(west_neighbours)]
grouped_country = eu_df.groupby(["Country"] ,as_index=False)["Confirmed","Recovered","Deaths"].last().sort_values(by="Confirmed",ascending=False)
grouped_country


# In[ ]:


fig = go.Figure()

fig.add_trace(go.Bar(
    
    x=grouped_country['Country'],
    y=grouped_country['Confirmed'],
    #orientation='h',
    text=grouped_country['Confirmed']
    ))
fig.update_traces(textposition='outside')
fig.update_layout(title="Cumulative Number of COVID-19 Confirmed Cases - EU" + ' as of ' + ondate )    
fig.show()


# In[ ]:


fig = go.Figure()

trace1 = go.Bar(
    x=grouped_country['Confirmed'],
    y=grouped_country['Country'],
    orientation='h',
    name='Confirmed'
)
trace2 = go.Bar(
    x=grouped_country['Deaths'],
    y=grouped_country['Country'],
    orientation='h',
    name='Deaths'
)
trace3 = go.Bar(
    x=grouped_country['Recovered'],
    y=grouped_country['Country'],
    orientation='h',
    name='Recovered'
)

data = [trace1, trace2, trace3]
layout = go.Layout(
    barmode='stack'
)

fig = go.Figure(data=data, layout=layout)
fig.update_layout(title="Stacked Number of COVID-19 Cases (Confirmed, Deaths, Recoveries) - EU" + ' as of ' + ondate)    
fig.show()


# # Advanced Data Analysis
# 
# <b>Time Series Analysis</b>
# 
# 

# In[ ]:


ts_confirmed = pd.read_csv('/kaggle/input/novel-corona-virus-2019-dataset/time_series_covid_19_confirmed.csv')
ts_confirmed.rename(columns={'Country/Region':'Country', 'Province/State':'Province' }, inplace=True)
Serbia_C_ts = ts_confirmed[ts_confirmed['Country'] == 'Serbia'].copy()
Serbia_C_ts


# Calculate daily counts

# In[ ]:


ts_diff = Serbia_C_ts[Serbia_C_ts.columns[4:Serbia_C_ts.shape[1]]]
new = ts_diff.diff(axis = 1, periods = 1) 
ynew=list(new.sum(axis=0))


# <b>Epidemic Curve</b>
# 
# An epidemic curve shows the frequency of new cases over time based on the date of onset of disease. This curve is an important plot in epidemiology. The shape of the curve in relation to the incubation period for a particular disease can give clues about the spread and duration of the epidemy.

# In[ ]:


fig = go.Figure()
fig.add_trace(go.Bar(
    y=ynew,
    x=ts_diff.columns,
    text=list(new.sum(axis=0)),
    ))
fig.update_traces(textposition='outside')
fig.update_layout(title="Epidemic Curve - Daily Number of COVID-19 Confirmed Cases in Serbia " + ' as of  ' + ondate,
                 yaxis=dict(title='Number of Cases'))    
fig.show()


# To Do:
# 
# * Clustering of Worldwide Cases
# * Forecasting ....
# * More granular analysis - Age...

# # References
# 
# **Data Sources**
# 
# 1. [Novel Corona Virus 2019 Dataset on Kaggle](https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset)
# 2. [Novel Coronavirus (COVID-19) Cases, provided by JHU CSSE](https://github.com/CSSEGISandData/COVID-19)
