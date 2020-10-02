#!/usr/bin/env python
# coding: utf-8

# # COVID-19 EXPLORATORY DATA ANALYSIS

# #### Pressing Questions:
# 
# - Which countries are the most affected by the coronavirus?
# - How well is the U.S. doing?
# - How did it spread so far?
# - Will a public lockdown work?
# - Should we be worried?

# #### Reference
# - Novel Corona Virus 2019 Dataset (https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset)

# #### Import Modules and Load in Files

# In[ ]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import re
import seaborn as sns
color = sns.color_palette()
from tqdm import tqdm # progress bar
import plotly.offline as py


# Limit floats output to 3 decimal points
pd.set_option('display.float_format', lambda x: '%.3f' % x)

plt.style.use('fivethirtyeight')
get_ipython().run_line_magic('matplotlib', 'inline')

# Increase default figure and font sizes for easier viewing.
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 14

import datetime as dt
from datetime import timedelta
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score,silhouette_samples
from sklearn.linear_model import LinearRegression,Ridge,Lasso
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error,r2_score
import statsmodels.api as sm
from statsmodels.tsa.api import Holt,SimpleExpSmoothing,ExponentialSmoothing
from fbprophet import Prophet
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.tsa.stattools import adfuller


# In[ ]:


"""
!pip install pyramid-arima
from pyramid.arima import auto_arima
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
std=StandardScaler()
"""


# In[ ]:


from pathlib import Path
data_dir = Path('../input/covidcompletesetcc/COVID-19-DATASETS/covid19-global-forecasting-week-1/')

import os
os.listdir(data_dir)


# In[ ]:


data = pd.read_csv(data_dir/'train.csv', parse_dates = ['Date'])
data.head()


# In[ ]:


data.info()


# In[ ]:


data.head(0)


# In[ ]:


data.rename(columns = {'Date': 'date',
                       'Id': 'id',
                       'Province/State':'state',
                       'Country/Region': 'country',
                       'Lat': 'lat',
                       'Long': 'long',
                       'ConfirmedCases':'confirmed',
                       'Fatalities': 'fatalities'
                      }, inplace = True)

data.head()


# 
# - Cleaned data from COVID-19 Complete Dataset (Updated every 24hours)
# - https://www.kaggle.com/imdevskp/corona-virus-report

# In[ ]:


cleaned_data = pd.read_csv('../input/corona-virus-report/covid_19_clean_complete.csv', parse_dates = ['Date'])

cleaned_data.head()


# In[ ]:


# Rename column names
cleaned_data.rename(columns={'Date': 'date', 
                     'Province/State':'state',
                     'Country/Region':'country',
                     'Last Update':'last_updated',
                     'Confirmed': 'confirmed',
                     'Deaths':'deaths',
                     'Recovered':'recovered'
                    }, inplace=True)


# Group columns for 'cases'

cases = ['confirmed', 'deaths', 'recovered', 'active']


# In[ ]:


cleaned_data


# In[ ]:


# Active case = 'confirmed' - 'deaths' - 'recovered'

cleaned_data['active'] = cleaned_data['confirmed'] - cleaned_data['deaths'] - cleaned_data['recovered']

# Replace 'Mainland China' with just 'China'

cleaned_data['country'] = cleaned_data['country'].replace('Mainland China', 'China')

# Fill in missing values (NaN values in 'state' column)

cleaned_data[['state']] = cleaned_data[['state']].fillna('')
cleaned_data[cases] = cleaned_data[cases].fillna(0)
cleaned_data.rename(columns= {'Date': 'date'}, inplace=True)

data_new = cleaned_data


# In[ ]:


print("External Data")

print(f"Earliest Entry: {data_new['date'].min()}")
print(f"Last Entry:     {data_new['date'].max()}")
print(f"Total Days:     {data_new['date'].max() - data_new['date'].min()}")


# # Data Analysis of COVID-19
# - Confirmed Cases Around the Globe
# - Confirmed Deaths Over Time
# - Active Cases Over Time
# - Recovered Cases
# - Comparisons
# - Mortality and Recovery Rates

# # Confirmed Cases Over Time

# In[ ]:


import sys
print('\n'.join(sys.path))


# In[ ]:


# Import modules for plots

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_dark"
from plotly.subplots import make_subplots


# In[ ]:


data_new.head(2)


# In[ ]:


ww_confirmed = data_new.groupby('date')['date','confirmed','deaths'].sum().reset_index()


# In[ ]:


ww_confirmed


# In[ ]:


sns.set_style('darkgrid')
f, ax = plt.subplots(figsize=(10,10))
# ax.axis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

sns.lineplot(ww_confirmed.date, ww_confirmed.confirmed, palette="RdBu")
plt.xlabel('date', fontsize=12)
plt.ylabel('confirmed', fontsize=12)
plt.title('Globally Confirmed Cases Over Time', fontsize=16)
plt.xticks(rotation=90)
plt.show()


# In[ ]:


data_new.columns


# In[ ]:


# Country categories: 'china', 'us', 'italy', 'rest_of_world':

group_china = data_new[data_new['country']=='China'].reset_index()
group_china_date = group_china.groupby('date')['date','confirmed','deaths'].sum().reset_index

group_italy = data_new[data_new['country']=='Italy'].reset_index()
group_italy_date = group_italy.groupby('date')['date','confirmed','deaths'].sum().reset_index

group_us = data_new[data_new['country']=='US'].reset_index()
group_us_date = group_us.groupby('date')['date','confirmed','deaths'].sum().reset_index

group_rest = data_new[~data_new['country'].isin(['China', 'Italy', 'US'])].reset_index()
group_rest_date = group_rest.groupby('date')['date', 'confirmed', 'deaths'].sum().reset_index()


# In[ ]:


group_china_date


# In[ ]:


# China
sns.set_style('darkgrid')
f, ax = plt.subplots(figsize=(10,10))
sns.lineplot(group_china.date, group_china.confirmed, palette="RdBu")
plt.xlabel('date', fontsize=12)
plt.ylabel('confirmed', fontsize=12)
plt.title('Confirmed Cases Over Time in China', fontsize=16)
plt.xticks(rotation=90)
plt.show()

# Italy
sns.set_style('darkgrid')
f, ax = plt.subplots(figsize=(10,10))
sns.lineplot(group_italy.date, group_italy.confirmed, palette="RdBu")
plt.xlabel('date', fontsize=12)
plt.ylabel('confirmed', fontsize=12)
plt.title('Confirmed Cases Over Time in Italy', fontsize=16)
plt.xticks(rotation=90)
plt.show()

# US
sns.set_style('darkgrid')
f, ax = plt.subplots(figsize=(10,10))
sns.lineplot(group_us.date, group_us.confirmed, palette="RdBu")
plt.xlabel('date', fontsize=12)
plt.ylabel('confirmed', fontsize=12)
plt.title('Confirmed Cases Over Time in U.S.', fontsize=16)
plt.xticks(rotation=90)
plt.show()

# Rest
sns.set_style('darkgrid')
f, ax = plt.subplots(figsize=(10,10))
sns.lineplot(group_rest.date, group_rest.confirmed, palette="RdBu")
plt.xlabel('date', fontsize=12)
plt.ylabel('confirmed', fontsize=12)
plt.title('Confirmed Cases Over Time (Rest of the World)', fontsize=16)
plt.xticks(rotation=90)
plt.show()


# - Good news for China - it appears that the coronavirus did not hit critical levels when March arrived compared to Italy who are aggressively affected by the disease.
# - U.S. spike may be an indication of getting more testing and testing results, but this is also concerning because the spike can't conclusively tell us that.
# - Steady increase in other parts of the world.

# In[ ]:


data_new.head()


# In[ ]:


data_new['state'] = data_new['state'].fillna('')

temp = data_new[[col for col in data_new.columns if col != 'state']]

latest = temp[temp['date'] == max(temp['date'])].reset_index()
latest_grouped = latest.groupby('country')['confirmed', 'deaths'].sum().reset_index()


# In[ ]:


latest_grouped


# In[ ]:


import plotly.graph_objects as go
import plotly.express as px # high-level API for rapid data expl. and figure generation
import plotly.io as pio
pio.templates.default = "plotly_dark"
from plotly.subplots import make_subplots


# In[ ]:


worldcasesfig = px.choropleth(latest_grouped, locations="country", 
                    locationmode='country names', color="confirmed", 
                    hover_name="country", range_color=[1,5000], 
                    color_continuous_scale="peach", 
                    title='Countries with Confirmed Cases')

worldcasesfig.show()


# #### Taking a closer look at Europe

# In[ ]:


data_new.country


# In[ ]:


europe_list = list(['Austria','Belgium','Bulgaria','Croatia','Cyprus','Czechia','Denmark','Estonia','Finland','France','Germany','Greece','Hungary','Ireland',
               'Italy', 'Latvia','Luxembourg','Lithuania','Malta','Norway','Netherlands','Poland','Portugal','Romania','Slovakia','Slovenia',
               'Spain', 'Sweden', 'United Kingdom', 'Iceland', 'Russia', 'Switzerland', 'Serbia', 'Ukraine', 'Belarus',
               'Albania', 'Bosnia and Herzegovina', 'Kosovo', 'Moldova', 'Montenegro', 'North Macedonia'])

eurolist_grouped_latest = latest_grouped[latest_grouped['country'].isin(europe_list)] # Makes sure and verify the countries are within the list


# In[ ]:


eurolist_fig = px.choropleth(eurolist_grouped_latest, locations='country', locationmode='country names', color='confirmed',
                                                    hover_name='country', range_color=[1,2000], color_continuous_scale='portland', 
                                                     title='European Countries with Confirmed Cases', scope='europe', height=800)

eurolist_fig.show()


# - COVID-19 has the strongest effect in Western Europe based on the heatmap.

# In[ ]:


latest_grouped


# In[ ]:


# Confirmed Cases Worldwide (bargraph)

worldconfirmed_figbar = px.bar(latest_grouped.sort_values('confirmed', ascending=False)[:20][::-1],
                                                         x='confirmed', y='country',
                                                         title="Confirmed Cases Worldwide", text='confirmed',
                                                         height=1000, orientation='h')

worldconfirmed_figbar.show()


# In[ ]:


eurolist_grouped_latest


# In[ ]:


# Taking a closer look at confirmed cases in Europe (bargraph)

europeconfirm_figbar = px.bar(eurolist_grouped_latest.sort_values('confirmed', ascending=False)[:10][::-1], 
             x='confirmed', y='country', color_discrete_sequence=['#D63230'],
             title='Confirmed Cases in Europe', text='confirmed', orientation='h')

europeconfirm_figbar.show()


# In[ ]:


# Taking a closer look at confirmed cases in the United States (bargraph)

"""
usa = cleaned_data[cleaned_data['country'] == 'US']

usa_grouped_latest = usa[usa['date'] == max(usa['date'])]
usa_grouped_latest = usa_grouped_latest.groupby('state')['confirmed','deaths'].max().reset_index()

usaconfirm_figbar = px.bar(usa_grouped_latest.sort_values('confirmed', ascending=False)[:10][::-1],
                           x='confirmed', y='state', color_discrete_sequence=['#D63230'], title='Confirmed Cases in the United States',
                           text='confirmed', orientation='h')

usaconfirm_figbar.show()
"""


# # Confirmed Deaths Over Time

# In[ ]:


ww_confirmed.head()


# #### Confirmed Deaths Across the World

# In[ ]:


# Look at confirmed cases across the globe:

ww_confirmed_fig = px.line(ww_confirmed, x='date', y='deaths', title='Global Deaths Over Time', color_discrete_sequence=['#D63230'])
ww_confirmed_fig.show()

# Logarithmic Scale of the figure above
ww_confirmed_fig = px.line(ww_confirmed, x='date', y='deaths', title='Global Deaths Over Time (Log Scale)', log_y = True,
                           color_discrete_sequence=['#D63230'])
ww_confirmed_fig.show()


# #### Confirmed Deaths Over Time Across CHINA, ITALY, U.S., and Rest of the World

# In[ ]:


# China
sns.set_style('darkgrid')
f, ax = plt.subplots(figsize=(10,10))

sns.lineplot(group_china.date, group_china.deaths, palette="RdBu")
plt.xlabel('date', fontsize=12)
plt.ylabel('deaths', fontsize=12)
plt.title('Confirmed Deaths Over Time in China', fontsize=16)
plt.xticks(rotation=90)
plt.show()

# Italy
sns.set_style('darkgrid')
f, ax = plt.subplots(figsize=(10,10))
sns.lineplot(group_italy.date, group_italy.deaths, palette="RdBu")
plt.xlabel('date', fontsize=12)
plt.ylabel('deaths', fontsize=12)
plt.title('Confirmed Deaths Over Time in Italy', fontsize=16)
plt.xticks(rotation=90)
plt.show()

# US
sns.set_style('darkgrid')
f, ax = plt.subplots(figsize=(10,10))
sns.lineplot(group_us.date, group_us.deaths, palette="RdBu")
plt.xlabel('date', fontsize=12)
plt.ylabel('deaths', fontsize=12)
plt.title('Confirmed Deaths Over Time in U.S.', fontsize=16)
plt.xticks(rotation=90)
plt.show()

# Rest
sns.set_style('darkgrid')
f, ax = plt.subplots(figsize=(10,10))
sns.lineplot(group_rest.date, group_rest.deaths, palette="RdBu")
plt.xlabel('date', fontsize=12)
plt.ylabel('deaths', fontsize=12)
plt.title('Confirmed Deaths Over Time (Rest of the World)', fontsize=16)
plt.xticks(rotation=90)
plt.show()


# - Deaths in China have plateau'd since March compared to the rest of the countries.
# - The United State's sharp spike is concerning

# #### Countries with Reported Deaths (World Scope)

# In[ ]:


figdeathglobal = px.choropleth(latest_grouped, locations="country", 
                    locationmode='country names', color="deaths", 
                    hover_name="deaths", range_color=[1,100], 
                    color_continuous_scale="peach", 
                    title='Countries with Reported Deaths (Global-Scope)')

figdeathglobal.show()


# - The U.S., China, and Europe aren't doing well from a quick glance, but need to dive deeper and see how much each of the European countries are affected.

# In[ ]:


figdeatheurope = px.choropleth(eurolist_grouped_latest, locations="country", 
                    locationmode='country names', color="deaths", 
                    hover_name="country", range_color=[1,100], 
                    color_continuous_scale='portland',
                    title='Reported Deaths in EUROPE', scope='europe', height=800)

figdeatheurope.show()


# - Concerning Countries
#     - Spain
#     - Italy
#     - France
#     
# - Countries with Less Severity
#     - Portugal
#     - Ireland
#     - Iceland
# - Italy appears to have suffered the most from COVID-19

# In[ ]:


eurolist_grouped_latest.head()


# In[ ]:


fig_deatheurope = px.bar(eurolist_grouped_latest.sort_values('deaths', ascending=False)[:5][::-1],
x = 'deaths', y = 'country', color_discrete_sequence=['#D63230'],
title = 'Deaths in Europe', text = 'deaths', orientation='h')

fig_deatheurope.show()


# In[ ]:


# US
"""
fig_deathus = px.bar(usa_grouped_latest.sort_values('deaths', ascending=False)[:5][::-1],
x = 'deaths', y = 'state', color_discrete_sequence=['#D63230'],
title = 'Deaths in the United States', text = 'deaths', orientation='h')

fig_deathus.show()
"""


# # Active Cases Over Time

# - Active cases over time is the number of people who are currently affected by the virus (no deaths, no recovery reports)

# In[ ]:


cleaned_data


# In[ ]:


grouped_china = cleaned_data[cleaned_data['country']=='China'].reset_index()
grouped_china_date = grouped_china.groupby('date')['date','confirmed','deaths','active','recovered'].sum().reset_index

grouped_italy = cleaned_data[cleaned_data['country']=='Italy'].reset_index()
grouped_italy_date = grouped_italy.groupby('date')['date','confirmed','deaths','active','recovered'].sum().reset_index

grouped_us = cleaned_data[cleaned_data['country']=='US'].reset_index()
grouped_us_date = grouped_us.groupby('date')['date','confirmed','deaths','active','recovered'].sum().reset_index

grouped_rest = cleaned_data[~cleaned_data['country'].isin(['China', 'Italy', 'US'])].reset_index()
grouped_rest_date = grouped_rest.groupby('date')['date','confirmed','deaths','active','recovered'].sum().reset_index()


# In[ ]:


# China
sns.set_style('darkgrid')
f, ax = plt.subplots(figsize=(10,10))

sns.lineplot(group_china.date, group_china.active, palette="RdBu")
plt.xlabel('Date', fontsize=12)
plt.ylabel('Active Cases', fontsize=12)
plt.title('Active Cases in China', fontsize=16)
plt.xticks(rotation=90)
plt.show()

# Italy
sns.set_style('darkgrid')
f, ax = plt.subplots(figsize=(10,10))
sns.lineplot(group_italy.date, group_italy.active, palette="RdBu")
plt.xlabel('Date', fontsize=12)
plt.ylabel('Active Cases', fontsize=12)
plt.title('Active Cases in Italy', fontsize=16)
plt.xticks(rotation=90)
plt.show()

# US
sns.set_style('darkgrid')
f, ax = plt.subplots(figsize=(10,10))
sns.lineplot(group_us.date, group_us.active, palette="RdBu")
plt.xlabel('Date', fontsize=12)
plt.ylabel('Active Cases', fontsize=12)
plt.title('Active Cases in U.S.', fontsize=16)
plt.xticks(rotation=90)
plt.show()

# Rest
sns.set_style('darkgrid')
f, ax = plt.subplots(figsize=(10,10))
sns.lineplot(group_rest.date, group_rest.active, palette="RdBu")
plt.xlabel('Date', fontsize=12)
plt.ylabel('Active Cases', fontsize=12)
plt.title('Active Cases (Rest of the World)', fontsize=16)
plt.xticks(rotation=90)
plt.show()


# - Cases in China have plummetted.
# - What is working in China?
#     - Strict lockdowns?
# - Active cases elsewhere have climbed exponentially, especially seeing how steep the slope is for the United States.

# In[ ]:


cleaned_data['state'] = cleaned_data['state'].fillna('')

temp = cleaned_data[[col for col in data_new.columns if col != 'state']]

latest = temp[temp['date'] == max(temp['date'])].reset_index()
latest_grouped = latest.groupby('country')['confirmed', 'deaths','active','recovered'].sum().reset_index()


# In[ ]:


latest_grouped.head()


# In[ ]:


fig_activeworld = px.choropleth(latest_grouped, locations = 'country', locationmode = 'country names',
                               color='active', hover_name = 'active', range_color = [1,1000],
                               color_continuous_scale = 'peach', title = 'Active Cases (Global)')

fig_activeworld.show()


# In[ ]:


eurolist_grouped_latest.head()


# In[ ]:


"""
fig_activeeurope = px.choropleth(eurolist_grouped_latest, locations = 'country', locationmode = 'country names',
                               color='active', hover_name = 'active', range_color = [1,1000],
                               color_continuous_scale = 'portland', title = 'Active Cases in European Countries',
                                scope = 'europe', height = 700)

fig_activeeurope.show()

"""


# In[ ]:


fig_activeworld_bar = px.bar(latest_grouped.sort_values('active', ascending = False)[:10][::-1],
                            x = 'active', y = 'country', title = 'Active Cases (Globally)',
                            text = 'active', orientation = 'h')

fig_activeworld_bar.show()


# - The global snapshot of active cases does not account for the increase in infected people.

# # Recovered Cases

# In[ ]:


latest_grouped.head()


# In[ ]:


fig_recoverworld = px.bar(latest_grouped.sort_values('recovered', ascending = False)[:10][::-1],
                         x = 'recovered', y = 'country', title = 'Recovered Cases (Globally)',
                         text = 'recovered', orientation = 'h')

fig_recoverworld.show()


# - China appears to be doing well in patients recovering from the COVID-19; however, China's population is overwhelming different from other countries so it'll be trickier to compare China's recovery rates with other countries.
# - How does cruise ship have more recoveries than Germany and Belgium?
# - Is Italy doing okay relative to their countries population?
# - Could the aging population and culture be an impact on number of active cases and recovery rates?
# 

# # Comparisons

# #### Plot Cases Over Time

# In[ ]:


cleaned_data.head()


# In[ ]:


compare_cases = cleaned_data.groupby('date')['recovered','deaths','active'].sum().reset_index()

"""Melt function:massage a DataFrame into a format where one or more columns are identifier variables, while all other columns, considered measured variables, are unpivoted to the row axis, leaving just two non-identifier columns, variable and value.
"""
    
compare_cases = compare_cases.melt(id_vars='date', value_vars=['recovered','deaths','active'],
                                  var_name='case', value_name='count')

compare_cases.head()


# In[ ]:


compare_cases_fig = px.line(compare_cases, x="date", y="count", color='case', title='Cases over time: Line Plot',
                            color_discrete_sequence = ['cyan', 'red', 'orange'])

compare_cases_fig.show()


compare_cases_fig = px.area(compare_cases, x="date", y="count", color='case', title='Cases over time: Area Plot',
                            color_discrete_sequence = ['cyan', 'red', 'orange'])

compare_cases_fig.show()


# - Active cases across the board are climbing dramatically toward March, with deaths slowly increasing.
# - China's recovery rate or the number of recovered relative to their population could mask the actual plots for deaths and recovered patients.
# - Removing China from the equation, a graph is needed to see how the rest of the world is doing (see figure below).

# #### Plot Cases for the Rest of the World (minus China)

# In[ ]:


cleaned_data.head()


# In[ ]:


# Remove China from equation
compare_cases_rest = cleaned_data[cleaned_data['country'] != 'China']

compare_casesrest_grouped = compare_cases_rest.groupby('date')['recovered','deaths','active'].sum().reset_index()

compare_cases_melt = compare_casesrest_grouped.melt(id_vars = 'date', value_vars = ['recovered','deaths','active'],
                                                   var_name = 'case', value_name = 'count')

compare_cases_melt.head()


# In[ ]:


compare_casesrest_fig = px.line(compare_cases_melt, x = 'date', y = 'count', color = 'case',
                               title = 'Cases from the Rest of the World')

compare_casesrest_fig.show()


compare_casesrest_fig = px.area(compare_cases_melt, x = 'date', y = 'count', color = 'case',
                               title = 'Cases from the Rest of the World')

compare_casesrest_fig.show()


# - It appears that active cases are also increasing drastically for the rest of the world.
# - Recovery rates for the rest of the world is noticeably low compared to the previous graph with China taken into account.
#     - What is China doing that is increasing their recovery rates for patients with the virus?
#     

# # Mortality & Recovery Rates

# In[ ]:


cleaned_data.head(3)


# In[ ]:


cleaned_data_latest = cleaned_data[cleaned_data['date'] == max(cleaned_data['date'])]

cleaned_data_latestgroup = cleaned_data_latest.groupby('country')['confirmed','deaths','recovered','active'].sum().reset_index()

cleaned_data_latestgroup.head(3)


# #### Dig deeper and see trends in deaths per confirmed cases (100)

# In[ ]:


# Mortality Rate = (# deaths / # confirmed) * 100
## Round product
cleaned_data_latestgroup['mortality_rate'] = round((cleaned_data_latestgroup['deaths']/cleaned_data_latestgroup['confirmed'])
                                                  * 100, 2)
cleaned_data_latestgroup.head(2)


# In[ ]:


# Sort 'confirmed' to 100 case batches
mort_rate = cleaned_data_latestgroup[cleaned_data_latestgroup['confirmed'] > 100]
mort_rate = mort_rate.sort_values('mortality_rate', ascending = False)

mort_rate.head()


# In[ ]:


mortrate_fig = px.bar(mort_rate.sort_values('mortality_rate', ascending = False)[:10][::-1],
                     x = 'mortality_rate', y = 'country', title = 'DEATHS per 100 Confirmed Cases',
                     text = 'mortality_rate', color_discrete_sequence = ['darkred'], orientation = 'h')

mortrate_fig.show()


# #### Countries with Low Mortality Rates

# In[ ]:


low_mortrate = cleaned_data_latestgroup[cleaned_data_latestgroup['confirmed'] > 100]

low_mortrate = low_mortrate.sort_values('mortality_rate', ascending = True)[['country','confirmed','deaths']][:15]

low_mortrate.head(2)


# In[ ]:


# Add color gradient to chart
low_mortrate.sort_values('confirmed', ascending = False)[['country','confirmed','deaths']][:20].style.background_gradient(cmap = 'Reds')


# #### RECOVERIES per 100 Confirmed Cases

# In[ ]:


# Recovery Rate = (# recoveries / # confirmed) * 100
## Round product to two decimals
cleaned_data_latestgroup['recovery_rate'] = round((cleaned_data_latestgroup['recovered']/cleaned_data_latestgroup['confirmed'])
                                                  * 100, 2)

# Sort 'confirmed' to 100 case batches
recov_rate = cleaned_data_latestgroup[cleaned_data_latestgroup['confirmed'] > 100]
recov_rate = recov_rate.sort_values('recovery_rate', ascending = False)

recov_rate.head()


# In[ ]:


recov_rate_fig = px.bar(recov_rate.sort_values('recovery_rate', ascending = False)[:10][::-1],
                     x = 'recovery_rate', y = 'country', title = 'RECOVERIES per 100 Confirmed Cases',
                     text = 'recovery_rate', color_discrete_sequence = ['darkgreen'], orientation = 'h')


recov_rate_fig.show()


# #### Countries with the WORST Recovery Rates

# In[ ]:


low_recovrate = recov_rate[recov_rate['confirmed'] > 100]

low_recovrate = low_recovrate.sort_values('recovery_rate', ascending = True)[['country','confirmed','recovered']][:20]

low_recovrate.head()


# In[ ]:


# Add color gradient to chart
low_recovrate.sort_values('confirmed', ascending = False)[['country','confirmed','recovered']][:20].style.background_gradient(cmap = 'Greens')


# # GLOBAL SCOPE

# In[ ]:


data_new


# In[ ]:


formated_gdf = data_new.groupby(['date', 'country'])['confirmed', 'deaths'].max()
formated_gdf = formated_gdf.reset_index()
formated_gdf['date'] = pd.to_datetime(formated_gdf['date'])
formated_gdf['date'] = formated_gdf['date'].dt.strftime('%m/%d/%Y')
formated_gdf['size'] = formated_gdf['confirmed'].pow(0.3)

fig = px.scatter_geo(formated_gdf, locations="country", locationmode='country names', 
                     color="confirmed", size='size', hover_name="country", 
                     range_color= [0, 1500], 
                     projection="natural earth", animation_frame="date", 
                     title='COVID-19: Spread Over Time', color_continuous_scale="portland")

fig.show()


# In[ ]:


covid = pd.read_csv("../input/novel-corona-virus-2019-dataset/covid_19_data.csv")
covid.head()


# In[ ]:


print("Size/Shape of the dataset: ",covid.shape)
print("Checking for null values:\n",covid.isnull().sum())
print("Checking Data-type of each column:\n",covid.dtypes)


# In[ ]:


# Dropping column as SNo is of no use, and "Province/State" contains too many missing values
covid.drop(["SNo"], 1, inplace = True)


# In[ ]:


#Converting "Observation Date" into Datetime format
covid["ObservationDate"] = pd.to_datetime(covid["ObservationDate"])


# In[ ]:


# Grouping Different Types of Cases as per Date
datewise = covid.groupby(["ObservationDate"]).agg({"Confirmed":'sum',"Recovered":'sum',"Deaths":'sum'})


# In[ ]:


datewise["Days Since"] = datewise.index-datewise.index[0]
datewise["Days Since"] = datewise["Days Since"].dt.days


# In[ ]:


train_ml=datewise.iloc[:int(datewise.shape[0]*0.95)]
valid_ml=datewise.iloc[int(datewise.shape[0]*0.95):]
model_scores=[]


# In[ ]:


lin_reg = LinearRegression(normalize = True)

lin_reg.fit(np.array(train_ml["Days Since"]).reshape(-1,1),np.array(train_ml["Confirmed"]).reshape(-1,1))


# In[ ]:


prediction_valid_linreg = lin_reg.predict(np.array(valid_ml["Days Since"]).reshape(-1,1))


# In[ ]:


model_scores.append(np.sqrt(mean_squared_error(valid_ml["Confirmed"],prediction_valid_linreg)))

print("Root Mean Square Error for Linear Regression: ", np.sqrt(mean_squared_error(valid_ml["Confirmed"], prediction_valid_linreg)))


# In[ ]:


plt.figure(figsize=(11,6))
prediction_linreg=lin_reg.predict(np.array(datewise["Days Since"]).reshape(-1,1))
plt.plot(datewise["Confirmed"],label="Actual Confirmed Cases")
plt.plot(datewise.index,prediction_linreg, linestyle='--',label="Predicted Confirmed Cases using Linear Regression",color='black')
plt.xlabel('Time')
plt.ylabel('Confirmed Cases')
plt.title("Confirmed Cases Linear Regression Prediction")
plt.xticks(rotation=90)
plt.legend()


# - The Linear Regression Model is absolutely falling apart.

# #### Polynomial Regression for Prediction of Confirmed Cases

# In[ ]:


train_ml=datewise.iloc[:int(datewise.shape[0]*0.95)]
valid_ml=datewise.iloc[int(datewise.shape[0]*0.95):]


# In[ ]:


poly = PolynomialFeatures(degree = 8) 

train_poly=poly.fit_transform(np.array(train_ml["Days Since"]).reshape(-1,1))
valid_poly=poly.fit_transform(np.array(valid_ml["Days Since"]).reshape(-1,1))
y = train_ml["Confirmed"]


# In[ ]:


linreg = LinearRegression(normalize = True)
linreg.fit(train_poly,y)


# In[ ]:


prediction_poly = linreg.predict(valid_poly)
rmse_poly = np.sqrt(mean_squared_error(valid_ml["Confirmed"], prediction_poly))
model_scores.append(rmse_poly)

print("Root Mean Squared Error for Polynomial Regression: ",rmse_poly)


# In[ ]:


comp_data = poly.fit_transform(np.array(datewise["Days Since"]).reshape(-1,1))

plt.figure(figsize=(11,6))
predictions_poly=linreg.predict(comp_data)
plt.plot(datewise["Confirmed"],label="Train Confirmed Cases",linewidth=3)
plt.plot(datewise.index,predictions_poly, linestyle='--',label="Best Fit for Polynomial Regression",color='black')
plt.xlabel('Time')
plt.ylabel('Confirmed Cases')
plt.title("Confirmed Cases Polynomial Regression Prediction")
plt.xticks(rotation=90)

plt.legend()


# In[ ]:


new_prediction_poly = []

for i in range(1,18):
    new_date_poly=poly.fit_transform(np.array(datewise["Days Since"].max()+i).reshape(-1,1))
    new_prediction_poly.append(linreg.predict(new_date_poly)[0])


# #### Support Vector Machine ModelRegressor for Prediction of Confirmed Cases

# In[ ]:


train_ml = datewise.iloc[:int(datewise.shape[0]*0.95)]
valid_ml = datewise.iloc[int(datewise.shape[0]*0.95):]


# In[ ]:


#Intializing SVR Model

svm = SVR(C = 1, degree = 5, kernel = 'poly', epsilon = 0.01)


# In[ ]:


# Fitting Model on the Training Data

svm.fit(np.array(train_ml["Days Since"]).reshape(-1,1), np.array(train_ml["Confirmed"]).reshape(-1,1))


# In[ ]:


prediction_valid_svm = svm.predict(np.array(valid_ml["Days Since"]).reshape(-1,1))


# In[ ]:


model_scores.append(np.sqrt(mean_squared_error(valid_ml["Confirmed"], prediction_valid_svm)))

print("Root Mean Square Error for Support Vectore Machine: ", np.sqrt(mean_squared_error(valid_ml["Confirmed"], prediction_valid_svm)))


# In[ ]:


plt.figure(figsize = (11,6))
prediction_svm = svm.predict(np.array(datewise["Days Since"]).reshape(-1,1))
plt.plot(datewise["Confirmed"],label = "Train Confirmed Cases",linewidth = 3)
plt.plot(datewise.index,prediction_svm, linestyle = '--',label = "Best Fit for SVR",color = 'black')
plt.xlabel('Time')
plt.ylabel('Confirmed Cases')
plt.title("Confirmed Cases Support Vector Machine Regressor Prediction")
plt.xticks(rotation = 90)
plt.legend()


# In[ ]:


new_date = []
new_prediction_lr = []
new_prediction_svm = []

for i in range(1,18):
    new_date.append(datewise.index[-1]+timedelta(days=i))
    new_prediction_lr.append(lin_reg.predict(np.array(datewise["Days Since"].max()+i).reshape(-1,1))[0][0])
    new_prediction_svm.append(svm.predict(np.array(datewise["Days Since"].max()+i).reshape(-1,1))[0])


# In[ ]:


pd.set_option('display.float_format', lambda x: '%.6f' % x)

model_predictions=pd.DataFrame(zip(new_date,new_prediction_lr,new_prediction_poly,new_prediction_svm),
                               columns=["Dates","Linear Regression Prediction","Polynonmial Regression Prediction","SVM Prediction"])

model_predictions.head()


# - Predictions of Linear Regression are not close to actual values.
