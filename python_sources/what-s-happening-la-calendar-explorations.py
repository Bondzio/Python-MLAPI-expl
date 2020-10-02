#!/usr/bin/env python
# coding: utf-8

# ## Introduction
# This is a starter code for visualizing the What's Happening LA Calendar dataset.

# ## Setup

# In[ ]:


import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import json
import nltk

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# Reading the dataset 
nRowsRead = 1000 # specify 'None' if want to read whole file

# whats-happening-la-calendar-dataset.csv has 29519 rows in reality, but we are only loading/previewing the first 1000 rows
la_cal_df = pd.read_csv('../input/whats-happening-la-calendar-dataset.csv',                        delimiter=',', nrows = nRowsRead) #, converters={'Location Address':CustomParser})
la_cal_df.dataframeName = 'whats-happening-la-calendar-dataset.csv'
nRow, nCol = la_cal_df.shape
print(f'There are {nRow} rows and {nCol} columns')


# Let's take a quick look at what the data looks like:

# In[ ]:


la_cal_df.head(2)


# In[ ]:


# Cleaning up some missing values
la_cal_df['Location Address'].fillna('{}', inplace = True)
la_cal_df['Age Groupings'].replace('Seniors','Senior', inplace=True)


# The Location Adress column has a lot of useful information. Let us spread that out in seperate columns

# In[ ]:


import ast, json
from pandas.io.json import json_normalize

def only_dict(d):
    '''
    Convert json string representation of dictionary to a python dict
    '''
    return ast.literal_eval(d)

# extact the information in the Location Address column
A = json_normalize(la_cal_df['Location Address'].apply(only_dict).tolist()).add_prefix('event_address.')
A.fillna('{}', inplace = True)
B = json_normalize(A['event_address.human_address'].apply(only_dict).tolist()).add_prefix('event_address.')
B=B.rename(columns = {'event_address.address': 'event_address.street'})


# In[ ]:


A.head()


# In[ ]:


B.head()


# In[ ]:


# add the new address columns and fill in missing values with an empty string
la_cal_df = la_cal_df.join([B, A[['event_address.latitude', "event_address.longitude", "event_address.needs_recoding"]]]).fillna('')


# In[ ]:


la_cal_df.head()


# ### What is the event frequency for each age group?

# In[ ]:


# count of events by age grouping
la_cal_df['Age Groupings'].value_counts()


# ### How are the events spread out over different cities?

# In[ ]:


# histogram of the number of events by city
# Note we are ignoring events that do not have the city specified

fig, ax = plt.subplots(figsize=(10, 6))
plt.title('Number of Events by City')
plt.xlabel('City')
plt.ylabel('Event Count')
la_cal_df.loc[la_cal_df['event_address.city'] != '']['event_address.city'].value_counts().plot(ax=ax, kind='bar')


# Looks like LA has the bulk of teh events in this dataset. 
# 
# Hmmm... but what is that "City" city on the x axis?

# In[ ]:


la_cal_df.loc[la_cal_df['event_address.city'] == 'City'].head(5)


# Let's look at one of those addresses...

# In[ ]:


la_cal_df.loc[173]['Location Address']


# My guess is the street name includes part of the city name..but not sure.
# 
# Is the Harbor City - Harbor Gateway the only place referred to as "City"? 

# In[ ]:


(la_cal_df.loc[la_cal_df['event_address.city'] == 'City'])['Location Common Name'].value_counts()


# Let's correct that in our plot then and replace "City" with "Harbor City"

# In[ ]:


# histogram of the number of events by city
# Note we are ignoring events that do not have the city specified

la_cal_df.loc[la_cal_df['event_address.city'] == 'City', ['event_address.city']] = "Harbor City"

fig, ax = plt.subplots(figsize=(10, 6))
plt.title('Number of Events by City')
plt.xlabel('City')
plt.ylabel('Event Count')
la_cal_df.loc[la_cal_df['event_address.city'] != '']['event_address.city'].value_counts().plot(ax=ax, kind='bar')


# ### What about the event titles? What common themes/words do they have?

# In[ ]:


# get a list of bigrams from the given title list
def get_bigrams(titles):
    bigrams_set = [nltk.bigrams(t.split()) for t in titles]
    b_list=[]
    for b_set in bigrams_set:
        for b in b_set:
            b_list.append(''.join([w+' ' for w in b]))
    return b_list


# In[ ]:


# get the top_n most common bigrams in bigram list
# returns a dataframe with top_n bigrams and their frequencies
def get_bigram_freqs(b_list, top_n=10):
    bigram_freqs=nltk.FreqDist(b_list)
    b_res = pd.DataFrame(bigram_freqs.most_common(top_n),                          columns=['Word', 'Frequency'])
    return b_res


# #### Events for Adults
# Let's find the most common bigrams (2 word sequences) in events for Adults

# In[ ]:


adult_titles = (la_cal_df.loc[la_cal_df['Age Groupings']=='Adult'])['Event Name'].str.lower()
adult_bi_list = get_bigrams(adult_titles)
adult_freq_list = get_bigram_freqs(adult_bi_list, top_n=100)


# Let's look at which bigrams are most common. This will tell us something about the events held for this age group.

# In[ ]:


fig, ax = plt.subplots(figsize=(20, 6))
plt.title('Top Bigrams for Adults')
plt.xlabel('Bigrams')
plt.ylabel('Frequency')
plt.xticks(rotation=90)
ax.plot(adult_freq_list['Word'], adult_freq_list['Frequency'])


# #### Events for Children
# Let's find the most common bigrams (2 word sequences) in events for Children

# In[ ]:


child_titles = (la_cal_df.loc[la_cal_df['Age Groupings']=='Child'])['Event Name'].str.lower()
child_bi_list = get_bigrams(child_titles)
child_freq_list = get_bigram_freqs(child_bi_list, top_n=100)


# Let's look at which bigrams are most common. This will tell us something about the events held for this age group.

# In[ ]:


fig, ax = plt.subplots(figsize=(20, 6))
plt.title('Top Bigrams for Children')
plt.xlabel('Bigrams')
plt.ylabel('Frequency')
plt.xticks(rotation=90)
ax.plot(child_freq_list['Word'], child_freq_list['Frequency'])


# In[ ]:




