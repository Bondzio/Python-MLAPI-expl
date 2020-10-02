#!/usr/bin/env python
# coding: utf-8

# Analysis of homicide trends in the US. How many females killed other females and using what weapons?
# =====================================

# In[ ]:


# Imports

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


# In[ ]:


# Read CSV file
df = pd.read_csv('../input/database.csv')


# In[ ]:


df.head(5)


# In[ ]:


# Remove Record ID column as it is not useful
df.drop(['Record ID'], axis=1, inplace=True)


# In[ ]:


# What is the total number of records?
len(df)


# **Let's check which states have a large number of crimes**
# ----------------------------------------------------------

# In[ ]:


# Group rows by "State", count records per state (that's what the "size" does) and convert the result into a data frame with 
# column name as "Count"
sd = df.groupby('State').size().to_frame(name='Count')


# In[ ]:


# Let us see what "sd" looks like.
sd.head(5)


# In[ ]:


# Now, we will create a new columns named "State" by using values from "index" State. This will make it easy for us to visualize certain things.
sd['State'] = sd.index


# In[ ]:


# Reset indices to start from 0. Drop the "State" index.
sd.reset_index(drop=True, inplace=True)


# In[ ]:


# Let us look at our "sd" Data Frame again.
sd.head(5)


# Top 10 states with highest homicide rate
# ----------------------------------------

# In[ ]:


# Define dimensions of the plot (width, height)
a4_dims = (15.27, 8.27) 
# Create a figure and axes
fig, ax = plt.subplots(figsize=a4_dims) 
# Sort the "state-data" data frame based on Count in descending order
sd_sorted = sd.sort_values(by=['Count'], ascending=False) 
# Create barplot with "State name" on X and  "Count" on Y, take top 10 values only.
sns.barplot(x='State', y='Count', data=sd_sorted.head(10), ax=ax) 


# Now let us check which states have the lowest homicide rates
# ------------------------------------------------------------

# In[ ]:


a4_dims = (15.27, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)
sd_sorted = sd.sort_values(by=['Count'], ascending=False)
# using "tail(10)" on DF sorted in descending order, since we need last 10
sns.barplot(x='State', y='Count', data=sd_sorted.tail(10)) 


# Now, let us see the a map of US and check out how the homicides are distributed.
# ------------------------------------------------------------------------

# In[ ]:


# We will be using "Ploty" offline to plot data on US map.
# init ploty note book mode which allows us to plot graphs inside a jupyter notebook
init_notebook_mode(connected=True)


# In[ ]:


state_code_dict = {
    'Alabama': 'AL',
'Alaska' : 'AK',
'American Samoa' : 'AS',
'Arizona' : 'AZ',
'Arkansas' : 'AR',
'California' : 'CA',
'Colorado' : 'CO',
'Connecticut' : 'CT',
'Delaware' : 'DE',
'Dist. of Columbia' : 'DC',
'Florida' : 'FL',
'Georgia' : 'GA',
'Guam' : 'GU',
'Hawaii' : 'HI',
'Idaho' : 'ID',
'Illinois' : 'IL',
'Indiana' : 'IN',
'Iowa' : 'IA',
'Kansas' : 'KS',
'Kentucky' : 'KY',
'Louisiana' : 'LA',
'Maine' : 'ME',
'Maryland' : 'MD',
'Marshall Islands' : 'MH',
'Massachusetts' : 'MA',
'Michigan' : 'MI',
'Micronesia' : 'FM',
'Minnesota' : 'MN',
'Mississippi' : 'MS',
'Missouri' : 'MO',
'Montana' : 'MT',
'Nebraska' : 'NE',
'Nevada' : 'NV',
'New Hampshire' : 'NH',
'New Jersey' : 'NJ',
'New Mexico' : 'NM',
'New York' : 'NY',
'North Carolina' : 'NC',
'North Dakota' : 'ND',
'Northern Marianas' : 'MP',
'Ohio' : 'OH',
'Oklahoma' : 'OK',
'Oregon' : 'OR',
'Palau' : 'PW',
'Pennsylvania' : 'PA',
'Puerto Rico' : 'PR',
'Rhode Island' : 'RI',
'South Carolina' : 'SC',
'South Dakota' : 'SD',
'Tennessee' : 'TN',
'Texas' : 'TX',
'Utah' : 'UT',
'Vermont' : 'VT',
'Virginia' : 'VA',
'Virgin Islands' : 'VI',
'Washington' : 'WA',
'West Virginia' : 'WV',
'Wisconsin' : 'WI',
'Wyoming' : 'WY'
}


# In[ ]:


# Now, we need to add postal code in our "sd" i.e state-data DF which contains only state names.
# For each row in out sd DF, we need to get state name and get its corresponding Postal Code from state_code_dict.

# Takes in state name and returns its Postal Code by looking at state_code_dict.
# If state name is NOT found in the "state_code_dict" , return first 2 letters of state name.
def get_postal_code(state):
    if state in state_code_dict:
        return state_code_dict.get(state)
    return state[0:2]


# In[ ]:


# Ok. Let us apply the function created above on sd
sd['State Code'] = sd['State'].apply(get_postal_code)


# In[ ]:


# What does sd look like after we've added the state codes?

sd.head(5)


# Creating the actual map.
# ------------------------

# In[ ]:


# Creating the Choropleth map in ploty involves 3 steps

# Step 1: Init data, Specify what kind of map, color, title, locations and what should be used to plot etc.

data = dict(type='choropleth',
            colorscale = 'YIOrRd',
            locations = sd['State Code'],
            z = sd['Count'],
            locationmode = 'USA-states',
            text = sd['State'],
            marker = dict(line = dict(color = 'rgb(255,255,255)',width = 2)),
            colorbar = {'title':"Homicide Count"}
            ) 


# In[ ]:


# Step 2: Specify the layout, select title and what geo has to be used. There are several kinds of "geo" layouts

layout = dict(title = 'Crimes',
              geo = dict(scope='usa',
                         showlakes = True,
                         lakecolor = 'rgb(85,173,240)')
             )


# In[ ]:


# Step 3: Create figure using data and layout and then plot it.
choromap = go.Figure(data = [data],layout = layout)
iplot(choromap)


# Understanding "Crime Types" based on "Perpetrator Sex"
# ------------------------------------------------------

# In[ ]:


# Create a count plot of "Crime Type" Vs "Count" split based on "Perpetrator Sex"
sns.countplot(x='Crime Type', data=df, hue='Perpetrator Sex')


# Crimes based on "Victim's Ethinicity"
# -------------------------------------

# In[ ]:


sns.countplot(x='Victim Ethnicity', data = df, hue='Perpetrator Sex')


# Which months (across years) had the highest number of homicides?
# ----------------------------------------------------------------

# In[ ]:


a4_dims = (11.7, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)
sns.countplot(ax=ax, data=df, x='Month', hue='Perpetrator Sex')


# How have homicide rates changed from 1980 to 2014?
# ==================================================

# In[ ]:


a4_dims = (20.27, 4.27)
fig, ax = plt.subplots(figsize=a4_dims)
sns.countplot(ax=ax, data=df, x='Year', hue='Perpetrator Sex', )


# How many people killed people of the same gender?
# =================================================

# In[ ]:


# how many people killed people of the same gender?
df_known = df[(df['Victim Sex'] != 'Unknown') & (df['Perpetrator Sex'] != 'Unknown')]


# In[ ]:


gender_kill_count = df_known.groupby(['Victim Sex', 'Perpetrator Sex']).size()
gender_kill_count


# In[ ]:


gender_kill_count_DF = gender_kill_count.to_frame(name='Count')
gender_kill_count_DF


# In[ ]:


gender_kill_count_DF.reset_index(inplace=True)
gender_kill_count_DF


# In[ ]:


gender_kill_count_DF['Vict-Perp-Sex'] = gender_kill_count_DF['Victim Sex'] + ' - ' + gender_kill_count_DF['Perpetrator Sex']
gender_kill_count_DF


# In[ ]:


ax = sns.barplot(x='Vict-Perp-Sex', data=gender_kill_count_DF, y= 'Count', estimator=lambda x: x / 1000)
ax.set(ylabel="Count / 1000")


# In[ ]:


# How many unique weapons were used?
df['Weapon'].nunique()


# In[ ]:


gender_kill_count = df_known.groupby(['Victim Sex', 'Perpetrator Sex', 'Weapon']).size()
gender_kill_count


# In[ ]:


gender_kill_count_DF = gender_kill_count.to_frame(name='Count')
gender_kill_count_DF


# In[ ]:


gender_kill_count_DF.reset_index(inplace=True)
gender_kill_count_DF


# In[ ]:


gender_kill_count_DF.sort_values('Count', inplace=True, ascending=False)
gender_kill_count_DF


# Men have killed 161703 men using handguns
# =========================================

# In[ ]:


# Find the top 5 ways in which Females have killed Females
gender_kill_count_DF.sort_values('Count', inplace=True, ascending=False)
fem_top_5 = gender_kill_count_DF[(gender_kill_count_DF['Perpetrator Sex'] == 'Female') & (gender_kill_count_DF['Victim Sex'] == 'Female')].head(5)
fem_top_5


# In[ ]:


a4_dims = (10.27, 5.27)
fig, ax = plt.subplots(figsize=a4_dims)
ax = sns.barplot(x='Weapon', y='Count', data=fem_top_5, ax=ax, estimator=np.absolute)


# In[ ]:




