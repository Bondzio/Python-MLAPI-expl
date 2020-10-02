#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.max_columns', 100)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

#import os
#for dirname, _, filenames in os.walk('/kaggle/input'):
#    for filename in filenames:
#        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# ## The Covid-19 dataset for all NJ counties

# In[ ]:


df = pd.read_csv('/kaggle/input/covid19-new-jersey-nj-local-dataset/Covid-19-NJ-Counties.csv', index_col='Date', parse_dates=['Date'])
print(f"Data is from {min(df.index).date()} to {max(df.index).date()} for all NJ counties")
print("Here's the most recent sample of data :")
df.tail(10)


# ### Let's find the (interesting) counties that have the highest number of cases

# #### All counties

# In[ ]:


counties = set(df.columns) - set(['Total Positive Cases', 'Total Negative Cases', 'Deaths', 'Under Investigation'])
counties


# #### NJ counties with highest number of positive cases. We'll focus on just these counties.

# In[ ]:


highest_counties = df.iloc[-1][counties].nlargest(10).index
list(highest_counties)


# ## Simple trendline of the total positive cases in these counties

# In[ ]:


highest_deaths_df = df[list(highest_counties) + ['Deaths']]
ax = highest_deaths_df.plot(figsize=(20, 10), rot=45)
ax.set_ylabel('Number of positive cases')
ax.set_title('Total Positive cases over time by county + Deaths', fontweight='bold', fontsize='x-large')
ax.set_xticks(highest_deaths_df.index)
ax.set_xticklabels(highest_deaths_df.index.strftime('%b-%d'))
plt.show()


# You can see an exponential-like curve in March, but the numbers look much better (lower) in April & dare I say, that the curve seems to be flattening!!

# ## Let's look at the daily rate of change between the counties

# In[ ]:


# Skipping the first few rows due to high data variability & the graph isn't very useful
# Also, taking a simple moving average to smoothen the curve
pct_change = df[40:].pct_change().rolling(5, 1).mean() * 100
ax = pct_change[highest_counties].plot(figsize=(20, 10), rot=45)
ax.set_ylabel('Percent daily rate of change')
ax.set_title('Percent daily rate of change over time by counties', fontweight='bold', fontsize='x-large')
ax.set_xticks(pct_change.index)
ax.set_xticklabels(pct_change.index.strftime('%b-%d'))
plt.show()


# The initial numbers are erratic since there are too few samples. But the daily rate of change of all counties is decreasing (in general) & now it's below 5% as of May 3rd for most counties which is great! So, the number of positive cases are not doubling or tripling, every day.

# In[ ]:


pct_change.iloc[-10][counties].nlargest(25)


# ## Let's see the best & worst counties in terms of daily Rate of Change

# In[ ]:


# We'll look at data since March 20th to avoid the erratic data before.
# Also, we'll include only 10 counties that have the highest number of cases
recent_df = df[df.index > '2020-03-20']
recent_pct_change = recent_df.pct_change()
highest_counties_for_recent = df.iloc[-1][counties].nlargest(10).index
recent_pct_change[highest_counties_for_recent].mean().sort_values()


# ## Days to double
# How many days does it take for the number of positive cases to double? For that, the daily rate of change needs to be 100%.

# In[ ]:


# Disabling Union county since it's numbers are erratic around the mid-June time-frame
days_to_double = 100.0/pct_change
ax = days_to_double[set(highest_counties) - {'Union'}].rolling(5, 1).mean().plot(figsize=(20, 10), rot=45)
ax.set_ylabel('Number of days for cases to double')
ax.set_title('Number of days for cases to double over time by county', fontweight='bold', fontsize='x-large')
ax.set_xticks(days_to_double.index)
ax.set_xticklabels(days_to_double.index.strftime('%b-%d'))
plt.show()


# It's encouraging to see that the trend is increasing over time. This is in-spite of more tests being done every day!
# 
# For most of the counties with the largest number of cases, it seems that it takes >50 days for the cases to double as of May 16th. Also, Bergen county which was the first NJ county to get a load of cases & the second-highest number of cases so far (as of May 16th) is not increasing at a rapid rate, taking >250 days to double the number of cases!

# ## Logarithmic plot for New Cases vs Total cases
# We'll just plot for the counties that have the highest number of cases. Also, we'll take a Simple Moving average to smoothen the curve (remove irregularities).

# In[ ]:


melted_df = df[highest_counties].reset_index().melt(id_vars='Date', var_name='County', value_name='Total Cases')
melted_df['New Cases'] = melted_df.groupby('County')['Total Cases'].transform(lambda x: x.diff().rolling(5, 1).mean())
plt.figure(figsize=(20,20))
grid = sns.lineplot(x="Total Cases", y="New Cases", hue="County", data=melted_df)
grid.set(xscale="log", yscale="log")
grid.set_title('New cases vs existing cases at log scale', fontweight='bold', fontsize='x-large')
plt.show()


# So, all counties are initially (& during the middle) increasing at the 45-degree exponential-growth-rate line on this curve. But towards the end (as of Apr 12th), for many counties the number of new cases is decreasing as compared to the existing cases which is further evidence of the curve flattening! For more info, please see my inspiration for this graph here :
# 
# https://www.youtube.com/watch?v=54XLXg4fYsc
# 
# Thanks to minutephysitcs Youtube channel for creating the above video!

# ## NJ Counties map over time for Covid-19 cases

# In[ ]:


from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    geojson = json.load(response)

#geojson["features"][0]

nj_counties_fips = dict()
nj_counties_fips['type'] = geojson['type']
nj_counties_fips['features'] = []
for item in geojson['features']:
    if int(item['id']) >= 34001 and int(item['id']) <= 34041:
        nj_counties_fips['features'].append(item)


# In[ ]:


melted_df = df[counties].reset_index().melt(id_vars='Date', var_name='County', value_name='Total Cases')
melted_df['New Cases'] = melted_df.groupby('County')['Total Cases'].transform(lambda x: x.diff().rolling(4, 1).mean())
melted_df['Date'] = melted_df['Date'].astype('str')


# In[ ]:


import plotly.express as px
fig = px.choropleth(melted_df, geojson=nj_counties_fips, color="Total Cases",
                    locations="County", featureidkey="properties.NAME",
                    projection="mercator", animation_frame="Date", color_continuous_scale='viridis_r',
                    title='Total Cases for top NJ counties over time')
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
fig.show()


# Bergen county starts with the highest number of cases & doesn't leave that post. But, we can see how other counties like Hudson & Essex which are closer to NYC start getting affected over time as well.

# ## NJ Counties map over time for rate-of-growth for Covid-19 cases

# In[ ]:


melted_df = melted_df[melted_df['Date'] != melted_df['Date'].min()]
melted_df['Ratio'] = (melted_df['New Cases']/melted_df['Total Cases']).rolling(3, 1).mean()


# In[ ]:


import plotly.express as px
fig = px.choropleth(melted_df, geojson=nj_counties_fips, color="Ratio",
                    locations="County", featureidkey="properties.NAME",
                    projection="mercator", animation_frame="Date", color_continuous_scale='viridis_r',
                    title='Ratio of New Cases to Existing for top NJ counties over time')
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
fig.show()


# At the start (in early March), the northern counties have higher rates of cases than the southern states (probably due to their proximity to New York). But by the end of April, the rate of new cases seems to be decreasing/lower in the northern counties as compared to the southern counties.

# ### Number of cases (positive, negative & under investigation) over time

# In[ ]:


ax = df[['Total Positive Cases', 'Total Negative Cases', 'Deaths', 'Under Investigation']].plot(figsize=(20, 10), rot=45)
ax.set_ylabel('Number of cases')
ax.set_title('Cases + Deaths over time', fontweight='bold', fontsize='x-large')
ax.set_xticks(df.index)
ax.set_xticklabels(df.index.strftime('%b-%d'))
plt.show()


# There are usually more negative cases than positive cases which I am hoping means that even if you get tested or have symptoms, you are more likely to not be affected than be affected (but I could be wrong). Also, it's great that NJ has kept the number of cases under investigation to a constant level over time inspite of the increasing number of cases.

# ## Analyze Covid-19 cases with NJ county demographics data

# In[ ]:


demo = pd.read_csv('/kaggle/input/nj-counties-census-demographics/NJCountyDemographics.csv', index_col='County/State')
cols = {'Population estimates, July 1, 2019,  (V2019)': 'Population estimate 2019',
        'Population, Census, April 1, 2010': 'Population Census 2010',
        'Black or African American alone, percent': 'Percentage of Black or African Americans',
        'Housing units,  July 1, 2018,  (V2018)': 'Housing units 2018',
        'Median value of owner-occupied housing units, 2014-2018': 'Median house value 2014-2018',
        'Households with a broadband Internet subscription, percent, 2014-2018': 'Percentage with Internet 2014-2018',
        'High school graduate or higher, percent of persons age 25 years+, 2014-2018': 'Percentage of high school graduates 2014-2018',
        'Persons  without health insurance, under age 65 years, percent': 'Percentage with no health insurance under 65',
        'Median household income (in 2018 dollars), 2014-2018': 'Median household income 2014-2018',
        'Persons in poverty, percent': 'Percentage of people in poverty',
        'Total employer establishments, 2017': 'Total employer establishments, 2017',
        'Population per square mile, 2010': 'Population per square mile, 2010',
        'Land area in square miles, 2010': 'Land area in square miles, 2010'}
demo = demo.reset_index().rename(cols, axis=1)[['County/State'] + list(cols.values())]
demo['County/State'] = demo['County/State'].str.replace(' County', '')
demo.head()


# In[ ]:


# Remove initial data since it has high variation to be useful
melted_df = df[12:][highest_counties].reset_index().melt(id_vars='Date', var_name='County', value_name='Total Cases')
melted_df['New Cases'] = melted_df.groupby('County')['Total Cases'].transform(lambda x: x.diff().rolling(4, 1).mean())
#melted_df


# In[ ]:


demo_df = melted_df.merge(demo, left_on='County', right_on='County/State', how='inner').drop('County/State', axis=1)
demo_df['Date'] = demo_df['Date'].dt.strftime("%b%d")
demo_df.head()


# ### New cases vs Total cases for NJ counties with demographics information over time
# 
# These graphs have a size & color gradient which stand for different demographics

# In[ ]:


import plotly.express as px
fig = px.scatter(demo_df, x="Total Cases", y="New Cases", size='Land area in square miles, 2010',
                 color='Population estimate 2019', animation_frame="Date", animation_group="County",
                 range_x=[0,20000], range_y=[-50,750], size_max=45, hover_name='County', text='County',
                 width=600, title="Size of bubbles is governed by land area of the county in 2010",
                color_continuous_scale='viridis_r')
fig.show()


# In[ ]:


import plotly.express as px
fig = px.scatter(demo_df, x="Total Cases", y="New Cases", size='Median house value 2014-2018',
                 color='Housing units 2018', animation_frame="Date", animation_group="County",
                 range_x=[0,20000], range_y=[-50,750], size_max=45, hover_name='County', text='County',
                 width=600, title="Size of bubbles is governed by Median house value 2014-2018",
                color_continuous_scale='viridis_r')
fig.show()


# In[ ]:


import plotly.express as px
fig = px.scatter(demo_df, x="Total Cases", y="New Cases", size='Percentage with no health insurance under 65',
                 color='Median household income 2014-2018', animation_frame="Date", animation_group="County",
                 range_x=[0,20000], range_y=[-50,750], size_max=45, hover_name='County', text='County',
                 width=600, title="Size of bubbles is governed by percentage with no health insurance under 65",
                color_continuous_scale='viridis_r')
fig.show()


# In[ ]:


import plotly.express as px
fig = px.scatter(demo_df, x="Total Cases", y="New Cases", size='Median household income 2014-2018',
                 color='Percentage of Black or African Americans', animation_frame="Date", animation_group="County",
                 range_x=[0,20000], range_y=[-50,750], size_max=45, hover_name='County', text='County',
                 width=600, title="Size of bubbles is governed by median household income 2014-2018",
                color_continuous_scale='viridis_r')
fig.show()


# In[ ]:


import plotly.express as px
fig = px.scatter(demo_df, x="Total Cases", y="New Cases", size='Percentage of people in poverty',
                 color='Total employer establishments, 2017', animation_frame="Date", animation_group="County",
                 range_x=[0,20000], range_y=[-50,750], size_max=45, hover_name='County', text='County',
                 width=600, title="Size of bubbles is governed by percentage of people in poverty",
                color_continuous_scale='viridis_r')
fig.show()


# In[ ]:


import plotly.express as px
fig = px.scatter(demo_df, x="Total Cases", y="New Cases", size='Percentage of high school graduates 2014-2018',
                 color='Percentage with Internet 2014-2018', animation_frame="Date", animation_group="County",
                 range_x=[0,20000], range_y=[-50,750], size_max=45, hover_name='County', text='County',
                 width=600, title="Size of bubbles is governed by percentage of high school graduates 2014-2018",
                color_continuous_scale='viridis_r')
fig.show()


# We can see how Covid-19 is affecting different counties & communities with different demographics. Let me know if there is any particular combination that you would like to see.

# Finally, I just wanted to express solidarity with everyone who has lost a loved one or has to face hardships due to the Covid-19 virus. May their souls rest in peace & may we all come out stronger on the other side!

# In[ ]:




