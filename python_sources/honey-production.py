#!/usr/bin/env python
# coding: utf-8

# # Basic setup

# In[ ]:


import numpy as np
import pandas as pd
import seaborn as sns
import plotly.offline as py
from matplotlib import pyplot as plt

plt.style.use('fivethirtyeight')
py.init_notebook_mode()


# # Importing data

# In[ ]:


state_code_to_name = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

data = pd.read_csv('../input/honeyproduction.csv').rename(columns={
    'state':'state_code',
    'numcol':'n_colony',
    'yieldpercol':'production_per_colony',
    'totalprod':'total_production',
    'stocks':'stock_held',
    'priceperlb':'price_per_lb',
    'prodvalue':'total_production_value'
})

data['consumption'] = data['total_production'] - data['stock_held']

data['state'] = data['state_code'].apply(lambda x: state_code_to_name[x])

data.head()


# ## Adjusting inflation
# 
# Let's adjust all prices as if they were from 2015.
# 
# I'm going to use this [inflation calculator](http://www.usinflationcalculator.com/).

# In[ ]:


inflation_rate = {
    1998: 1.454,
    1999: 1.423,
    2000: 1.376,
    2001: 1.339,
    2002: 1.317,
    2003: 1.288,
    2004: 1.255,
    2005: 1.214,
    2006: 1.176,
    2007: 1.143,
    2008: 1.101,
    2009: 1.105,
    2010: 1.087,
    2011: 1.054,
    2012: 1.032
}

monetized_features = ['price_per_lb', 'total_production_value']

for year in set(data['year']):
    for feature in monetized_features:
        data.loc[data['year']==year, feature] = inflation_rate[year]*data.loc[data['year']==year, feature]


# # Overall analysis
# 
# Let's plot the average values among the states to see if we can find any patterns.

# In[ ]:


data_by_year = data.groupby('year').mean()
data_by_year['production_per_colony_5e4'] = 50000*data_by_year['production_per_colony']
data_by_year[['total_production', 'production_per_colony_5e4', 'stock_held', 'total_production_value']].plot(ax=plt.subplots(figsize=(15,7))[1])


# Even though the production is decreasing, the total production value is increasing. The price per lb must be skyrocketing!

# In[ ]:


data_by_year[['price_per_lb']].plot(ax=plt.subplots(figsize=(15,3))[1])


# # State by state analysis
# 
# Let's see how the characteristics of each state's production vary through time. We can do it by checking the correlation of the variables with respect to `year`. High positive correlations mean solid growth and low negative correlations mean solid decay. Correlations close to 0 mean undefined/unstable behaviors.

# In[ ]:


def compute_correlation_with_year(df, feature):
    column = 'correlation: '+feature+' vs year'
    df[column] = 0
    for state in df.index:
        corr = data[data['state']==state][[feature, 'year']].corr().at[feature, 'year']
        df.loc[[True if state_index==state else False for state_index in df.index], column] = corr
    return column

correlations_by_state = pd.DataFrame(index=sorted(set(data['state'])))

def plot_correlations(feature):
    column = compute_correlation_with_year(correlations_by_state, feature)
    correlations_by_state.sort_values(column, ascending=False)[[column]].plot(kind='bar', ax=plt.subplots(figsize=(15,3))[1])


# ## Number of colonies

# In[ ]:


plot_correlations('n_colony')


# ## Production per colony

# In[ ]:


plot_correlations('production_per_colony')


# ## Total production

# In[ ]:


plot_correlations('total_production')


# ## Annual consumption

# In[ ]:


plot_correlations('consumption')


# ## Price per lb

# In[ ]:


plot_correlations('price_per_lb')


# ## Total production value

# In[ ]:


plot_correlations('total_production_value')


# # Scoring
# 
# Let's sum up those correlations and use it as our growth score. The growth scores expresses how well the states have been doing across the studied years.

# In[ ]:


score = None

for column in correlations_by_state.columns:
    if score is None:
        score = correlations_by_state[column].copy()
    else:
        score = score + correlations_by_state[column]

correlations_by_state['growth_score'] = score
correlations_by_state['state'] = np.array(correlations_by_state.index)

correlations_by_state.sort_values('growth_score', ascending=False)[['growth_score']].plot(kind='bar', ax=plt.subplots(figsize=(15,3))[1])


# In[ ]:


correlations_by_state = pd.merge(left=correlations_by_state,right=data[['state', 'state_code']].drop_duplicates(), how='left', on='state')

data = [ dict(
    type='choropleth',
    colorscale = 'Portland',
    reversescale = True,
    locations = correlations_by_state['state_code'],
    z = correlations_by_state['growth_score'],
    locationmode = 'USA-states',
    text = correlations_by_state['state'],
    marker = dict(
        line = dict (
            color = 'rgb(255,255,255)',
            width = 2
        ),
    ),

    colorbar = dict(
        title = "Growth score")
)]

layout = dict(
    title = 'Honey production scores (1998 - 2012)',
    geo = dict(
        scope='usa',
        projection=dict( type='albers usa' ),
        showlakes = True,
        lakecolor = 'rgb(255, 255, 255)'
    ),
)
    
figure = dict(data=data, layout=layout)
py.iplot(figure)


# # Summary
# 
# * Honey is becoming rarer and more expensive
# * The number of colonies is decreasing in most of the states
#     * Top 5 states with positive correlation with respect to `year`: North Dakota, Hawaii, Montana, Oregon, South Dakota
#     * Top 5 states with negative correlation with respect to `year`: Missouri, South Carolina, Maryland, Arkansas, Alabama
# * The production per colony is decreasing in most of the states
#     * Top 5 states with positive correlation with respect to `year`: **Mississippi**, **South Carolina**, **Maine**, Oklahoma, Virginia
#     * Top 5 states with negative correlation with respect to `year`: Florida, Oregon, Minnesota, Indiana, Michigan
# * The total production is decreasing in most of the states
#     * Top 5 states with positive correlation with respect to `year`: **Mississippi**, **North Dakota**, **North Carolina**, Kentucky, New Jersey
#     * Top 5 states with negative correlation with respect to `year`: Maryland, Alabama, Missouri, Arizona, Florida
# 
# Very interesting! The producers from Mississippi are doing a great job. Their colonies are increasing in quantity and quality.
# 
# * The annual consumption is decreasing in most of the states
#     * Top 5 states with positive correlation with respect to `year`:  Mississippi, North Dakota, Oregon, North Carolina, Colorado
#     * Top 5 states with negative correlation with respect to `year`: Maryland, Alabama, Missouri, Florida, Minessota
# * The price per lb has increased in ALL states
#     * The growth of the price per lb seems to be a little more irregular in Nevada than in other states
# * Even though most of the states' productions are decreasing, they're still able to increase the total production value. This is certainly due to the tremendous increase in the price per lb.
#     * Top 5 states with positive correlation with respect to `year`: Hawaii, North Dakota, North Carolina, South Carolina, New Jersey
#     * Top 5 states with negative correlation with respect to `year`: **Maryland**, **Missouri**, **Oklahoma**, Arkansas, Arizona
# 
# ### Top 5 honey producers (according to the score):
#   * Mississippi, North Dakota, North Carolina, Kentucky, New Jersey
# 
# ### Bottom 5 honey producers (according to the score):
#   * Missouri, Maryland, Arkansas, Alabama, Florida
# 
# ### Geographic pattern
#   * The northwestern and southeastern portions of the United States are the ones with higher growth scores.
