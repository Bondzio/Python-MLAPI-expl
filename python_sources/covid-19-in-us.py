#!/usr/bin/env python
# coding: utf-8

# # Exploratory Data Analysis of Covid-19 Cases in US
# 
# This is just an attempt to visualize Covid-19 spread in US, based on published data. See References for data sources. Notebook will be updated daily, as an updated dataset become available. 
# 
# 
# Note: More preprocessing is required for Province/State data. Clarification needed on Cruise ship's data.

# # Background
# 
# To Do:

# # Basic Data Analysis

# In[ ]:


# Project: Novel Corona Virus 2019 Dataset by Kaggle
# Program: COVID-19 in US 
# Author:  Radina Nikolic
# Date:    March 22, 2020
#          April 24, 2020 Active cases and week added

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
df_covid.rename(columns={'ObservationDate':'Date', 'Country/Region':'Country', 'Province/State':'State' }, inplace=True)


# Check the latest observation date

# In[ ]:


#Converting date column into correct format
df_covid['Date']=pd.to_datetime(df_covid['Date'])

maxdate=max(df_covid['Date'])

fondate=maxdate.strftime("%Y-%m-%d")
print("The last observation date is {}".format(fondate))
ondate = format(fondate)


# Active Cases = Confirmed - Deaths - Recovered

# In[ ]:


#Adding Active cases
df_covid['Active'] = df_covid['Confirmed'] - df_covid['Deaths'] - df_covid['Recovered']
#print("Active Cases Column Added Successfully")
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


plot_bar_chart(confirmed, deaths, recovered,active,'Worldwide').show()


# In[ ]:


plot_line_chart(confirmed, deaths, recovered, active, 'Worldwide').show()


# # What is happening in US

# First Cases

# In[ ]:


US_df = df_covid[df_covid['Country'] == 'US'].copy()
US_df.head() 


# The Latest Cases (based on available data)

# In[ ]:


US_df.tail()


# # Visualization

# In[ ]:


confirmed = US_df.groupby('Date').sum()['Confirmed'].reset_index()
deaths = US_df.groupby('Date').sum()['Deaths'].reset_index()
recovered = US_df.groupby('Date').sum()['Recovered'].reset_index()
active = US_df.groupby('Date').sum()['Active'].reset_index()


# In[ ]:


plot_bar_chart(confirmed, deaths, recovered,active, 'US').show()


# In[ ]:


plot_line_chart(confirmed, deaths, recovered,active,'US').show()


# # Across United States

# In[ ]:


confirmed = US_df.groupby(['Date', 'State'])['Confirmed'].sum().reset_index()
states = US_df['State'].unique()
states


# In order to perform an analysis by State, data must be cleaned. 

# In[ ]:


# Clean Data
US_df = US_df.replace(to_replace =['Chicago, IL', 'Cook County, IL', 'Chicago'],  
                            value ="Illinois")
US_df = US_df.replace(to_replace =['Delaware County, PA', 'Wayne County, PA', 'Wayne County, PA', 'Montgomery County, PA'],  
                            value ="Pennsylvania")
US_df = US_df.replace(to_replace =['Hillsborough, FL', 'Santa Rosa County, FL', 'Sarasota, FL',
                                   'Broward County, FL', 'Lee County, FL', 'Manatee County, FL',                              
                                   'Okaloosa County, FL','Volusia County, FL', 'Charlotte County, FL'],  
                            value ="Florida") 
US_df = US_df.replace(to_replace =['Los Angeles, CA', 'Orange, CA','Santa Clara, CA', 'San Benito, CA', 
                                   'Travis, CA', 'Humboldt County, CA','Sacramento County, CA','Santa Cruz County, CA',
                                   'Shasta County, CA', 'Riverside County, CA', 'Fresno County, CA',
                                   'Placer County, CA', 'San Mateo, CA', 'Sonoma County, CA',
                                   'Orange County, CA', 'Contra Costa County, CA', 'San Francisco County, CA',
                                   'Yolo County, CA', 'Santa Clara County, CA', 'Alameda County, CA',
                                   'San Diego County, CA','Madera County, CA', 'Berkeley, CA'],  
                            value ="California") 
US_df = US_df.replace(to_replace =['Virgin Islands, U.S.', 'United States Virgin Islands'],  
                            value ="Virgin Islands") 
US_df = US_df.replace(to_replace =['Westchester County, NY', 'New York City, NY',
                                   'Queens County, NY','New York County, NY', 'Nassau County, NY',
                                   'Rockland County, NY', 'Saratoga County, NY',
                                   'Suffolk County, NY', 'Ulster County, NY'],  
                            value ="New York") 
US_df = US_df.replace(to_replace =['King County, WA', 'Seattle, WA','Snohomish County, WA',
                                   'Clark County, WA','Grant County, WA','Unassigned Location, WA',
                                   'Jefferson County, WA', 'Pierce County, WA', 
                                   'Spokane County, WA', 'Kittitas County, WA'],  
                            value ="Washington") 
US_df = US_df.replace(to_replace =['San Antonio, TX', 'Lackland, TX', 'Harris County, TX', 
                                   'Fort Bend County, TX', 'Collin County, TX','Montgomery County, TX'],  
                            value ="Texas")
US_df = US_df.replace(to_replace =['Boston, MA', ' Norfolk County, MA', 'Suffolk County, MA', 
                                   'Middlesex County, MA', 'Norwell County, MA', 'Plymouth County, MA',
                                   'Norfolk County, MA', 'Unknown Location, MA' , 'Berkshire County, MA'],  
                            value ="Massachusetts")
US_df = US_df.replace(to_replace =['Virgin Islands, U.S.', 'United States Virgin Islands'],  
                            value ="Virgin Islands") 


# In[ ]:


states = US_df['State'].unique()
states


# To Do: More work on data cleaning for US States is required (at least for the top 20 most affected states). Clarification with Cruises data required. Where to assign them?
#        is there better way to assign existing data to the proper state?

# In[ ]:


grouped_country = US_df.groupby(["State"] ,as_index=False)["Confirmed","Recovered","Deaths"].last().sort_values(by="Confirmed",ascending=False)
grouped_country = grouped_country.head(20)

top_20_states = grouped_country["State"].unique()


# In[ ]:


fig = go.Figure()

fig.add_trace(go.Bar(
    
    y=grouped_country['State'],
    x=grouped_country['Confirmed'],
    orientation='h',
    text=grouped_country['Confirmed']
    ))
fig.update_traces(textposition='outside')
fig.update_layout(title="Cumulative Number of COVID-19 Confirmed Cases - By State" + ' as of ' + ondate + " Top 20" )  
fig.show()


# Focus will be on 20 top affected states. 
# 

# In[ ]:


confirmed = US_df.groupby(['Date', 'State'])['Confirmed'].sum().reset_index()
confirmed = confirmed[confirmed['State'].isin(top_20_states)]


# In[ ]:


fig = go.Figure()
for state in states:
 
    fig.add_trace(go.Scatter(
        x=confirmed[confirmed['State']==state]['Date'],
        y=confirmed[confirmed['State']==state]['Confirmed'],
        name = state, # Style name/legend entry with html tags
        connectgaps=True # override default to connect the gaps
    ))
fig.update_layout(title="Number of Confirmed COVID-19 Cases Over Time - US - by State - Top 20 as of " + ondate)    
fig.show()


# Let's look only from the date when more than 100 cases were reported.

# In[ ]:


confirmed = US_df.groupby(['Date', 'State'])['Confirmed'].sum().reset_index()
confirmed = confirmed[confirmed['Confirmed'] > 5000] 
confirmed = confirmed[confirmed['State'].isin(top_20_states)]


# In[ ]:


fig = go.Figure()
for state in states:
 
    fig.add_trace(go.Scatter(
        x=confirmed[confirmed['State']==state]['Date'],
        y=confirmed[confirmed['State']==state]['Confirmed'],
        name = state, # Style name/legend entry with html tags
        connectgaps=True # override default to connect the gaps
    ))
fig.update_layout(title="Number of Confirmed COVID-19 Cases (>5000) Over Time - US by State - Top 20 as of " + ondate)    
fig.show()


# In[ ]:


fig = go.Figure()

trace1 = go.Bar(
    x=grouped_country['Confirmed'],
    y=grouped_country['State'],
    orientation='h',
    name='Confirmed'
)
trace2 = go.Bar(
    x=grouped_country['Deaths'],
    y=grouped_country['State'],
    orientation='h',
    name='Deaths'
)
trace3 = go.Bar(
    x=grouped_country['Recovered'],
    y=grouped_country['State'],
    orientation='h',
    name='Recovered'
)

data = [trace1, trace2, trace3]
layout = go.Layout(
    barmode='stack'
)

fig = go.Figure(data=data, layout=layout)
fig.update_layout(title="Number of COVID-19 Cases (Confirmed, Deaths, Recoveries) - US by State" + ' as of ' + ondate + " Top 20")    
fig.show()


# # Advanced Data Analysis
# 
# <b>Time Series Analysis</b>
# 

# In[ ]:


ts_confirmed = pd.read_csv('/kaggle/input/novel-corona-virus-2019-dataset/time_series_covid_19_confirmed.csv')
ts_confirmed.rename(columns={'Country/Region':'Country', 'Province/State':'State' }, inplace=True)
US_C_ts = ts_confirmed[ts_confirmed['Country'] == 'US'].copy()
US_C_ts


# Calculate Daily counts

# In[ ]:


ts_diff = US_C_ts[US_C_ts.columns[4:US_C_ts.shape[1]]]
new = ts_diff.diff(axis = 1, periods = 1) 
ynew=list(new.sum(axis=0))


# **Epidemic Curve**
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
fig.update_layout(title="Epidemic Curve - Daily Number of COVID-19 Confirmed Cases in US " + ' as of  ' + ondate,
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
