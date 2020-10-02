#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime
import glob
import matplotlib.pyplot as plt
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
from subprocess import check_output



plt.style.use('ggplot')
get_ipython().run_line_magic('matplotlib', 'inline')

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

print(check_output(["ls", "../input"]).decode("utf8"))


# In[ ]:


path = '../input/'
#all_files = glob.glob(path + "/*.csv")
#^^ loading all data is a mess as noted in data desc, change in data format 2014->2015 :( 
#let's just load in 2015-17
years = ["2015", "2016", "2017"]
all_files = [(path + "crime_incident_data" + year + ".csv") for year in years]
crimes = pd.concat((pd.read_csv(f) for f in all_files))
#^^can't parse dates bc time is int64 :(
crimes.head(3)


# Blech "Occur Time" as an int64? Cmon PPD. Ok, let's turn into useable data.

# In[ ]:


def int_to_strtime(d):
    """convert int hhmm to str HH:MM """
    (h, s) = (d[:2], d[2:])
    timestr = h + ':' + s
    return timestr

#left pad zeros to form hhmm
crimes['Occur Time'] = crimes['Occur Time'].apply('{:0>4}'.format)
crimes['Occur_time'] = crimes['Occur Time'].apply(int_to_strtime)
crimes['Occur_timestamp'] = pd.to_datetime(crimes['Occur Date'] + ' ' + crimes['Occur_time'])

crimes['Hour'] = crimes['Occur_timestamp'].dt.hour
crimes['Date'] = crimes['Occur_timestamp'].dt.date
crimes['Day_of_Week'] = crimes['Occur_timestamp'].dt.dayofweek
crimes.head(3)


# Great, looks timestamped. Let's set that as the index, do some housekeeping, and move on to some viz.

# In[ ]:


crimes.index = pd.DatetimeIndex(crimes['Occur_timestamp'])
useless_columns = ['Case Number', 'Number of Records', 'Occur Date', 'Occur Month Year', 
                    'Occur Time', 'Open Data X', 'Open Data Y', 'Report Month Year', 'Occur_time']
crimes.drop(useless_columns, inplace=True, axis=1)
crimes = crimes[crimes['Occur_timestamp'] > '2015-01-01']
crimes.shape


# In[ ]:


crimes.info()


# In[ ]:


def draw_crimes_per_day_histo(df):
    """helper func to redraw crimes per day"""
    plt.figure(figsize=(15,6))
    plt.title('Distribution of Crimes per day', fontsize=16)
    plt.tick_params(labelsize=14)
    sns.distplot(df.resample('D').size(), bins=50)
draw_crimes_per_day_histo(crimes)


# A few observations:
# 
# * Looks like we have missing or incomplete data for some days....
# * True crime rate seems to be in range 100-200 a day, with median around 160ish

# In[ ]:


#longitudinal look
def draw_crimes_per_day_longit(df):
    """helper func to draw long graph"""
    plt.figure(figsize=(15,6))
    df.resample('M').size().plot(label='Total per month')
    plt.title('Crimes per month', fontsize=16)
    plt.xlabel('')
    plt.legend(prop={'size':16})
    plt.tick_params(labelsize=16)
draw_crimes_per_day_longit(crimes)


# Ah, looks like datetime is missing for early data. Since this is not complete for 2017 either, maybe if we just take May 2015 to May 2017 we'll have some useable data.

# In[ ]:


crimes = crimes['20150501':'20170430']
draw_crimes_per_day_longit(crimes)


# In[ ]:


draw_crimes_per_day_histo(crimes)


# Ok looks better. Let's get to it! Let's see what the most common crimes are in Portland, May '15-May '17.

# In[ ]:


#what are
counts = crimes.groupby(['Offense Type']).size().sort_values()
counts.plot(kind='barh', figsize=[15,15], title='Calls by Incident Type')


# Yikes, careful where you park your car in Portland.....let's do a deeper dive on crimes with more than 5k occurrences.

# In[ ]:


common_crimes = counts[counts > 5000]
names = common_crimes.index
names


# In[ ]:


g = sns.FacetGrid(crimes, 
                  row="Offense Type", 
                  row_order=names,
                  size=1.9, aspect=4, 
                  sharex=True,
                  sharey=False)

g.map(sns.distplot, "Hour", bins=24, kde=False, rug=False)


# Couple observations:
# 
# * shoplifting peaks in afternoon-early evening
# * burglary has some similar peaks, but is surprisingly common all day
# * related--burglary is the only crime that doesn't decline during the early morning
# * vandalism and motor vehicle-related crimes tend to peak late night-early morning.
# 
# Let's do some more time-series analysis of the data. Let's take a monthly rolling average to see if there are any variations.

# In[ ]:


crime_ts = crimes.groupby(['Offense Type','Date'], 
        as_index=['Offense Type',
                'Date']).count().ix[:,1].unstack(level=0).unstack(level=0).fillna(0)


# In[ ]:


for i, col in zip(range(1, len(names) + 1), names):
    plt.subplot(len(names), 1, i)
    plt.title(col, y=.8, x=.8)
    crime_ts[col].rolling(window=30, min_periods=30).mean().plot(figsize=(20,20))


# 
# * Looks like motor vehicle theft is trending up?
# * Looks like there was a small ~20% spike in identity theft activity last holiday season
# 
# **TO DO**
# 
# * neighborhood analysis
# * more general spatial analysis, let's see some maps!

# In[ ]:


#test
published_dataset = crimes.to_csv("../input/test_publish")


# In[ ]:




