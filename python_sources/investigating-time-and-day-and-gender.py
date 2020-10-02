#!/usr/bin/env python
# coding: utf-8

# From a glance at the data, it looks to be about a month. Looking at a single location (Beijing), is there any regular pattern over the week?
# 
# ### First, the standard imports...

# In[ ]:


import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns 
from mpl_toolkits.basemap import Basemap
get_ipython().run_line_magic('matplotlib', 'inline')


# ### Get all the events in Beijing

# In[ ]:


df_events = pd.read_csv("../input/events.csv", dtype={'device_id': np.str})

idx_beijing = (df_events["longitude"]>116) &              (df_events["longitude"]<117) &              (df_events["latitude"]>39.5) &              (df_events["latitude"]<40.5)
df_events_beijing = df_events[idx_beijing]

print("Total # events:", len(df_events))
print("Total # Beijing events:", len(df_events_beijing))


plt.figure(1, figsize=(12,6))
plt.title("Events by day")
plt.hist(df_events_beijing['timestamp'].map( lambda x: pd.to_datetime(x).dayofweek ), bins=7)
plt.show()


# A fairly flat distribution there. Pandas defines "0" as Monday, and "6" as Sunday so it looks like Monday is the least busy day, by maybe 10%.
# 
# What about each hour separately?

# In[ ]:


plt.figure(1, figsize=(12,6))
plt.title("Events by hour")
plt.hist(df_events_beijing['timestamp'].map( lambda x: pd.to_datetime(x).dayofweek*24 + pd.to_datetime(x).hour ), bins=168)
plt.show()


# Looks like the quietest times is 04:00 on Monday morning. Makes sense, people will need to be in work a few hours later.
# 
# ### Is there a gender split?

# In[ ]:


df_gender_age = pd.read_csv("../input/gender_age_train.csv", dtype={'device_id': np.str})
print("Total number of people in training set: ", len(df_gender_age))
df_joined = pd.merge(df_gender_age, df_events_beijing, on="device_id", how="inner")
print("Number of Beijing events in training set: ", len(df_joined))
df_female = df_joined[df_joined["gender"]=="F"]
df_male = df_joined[df_joined["gender"]=="M"]
print("Number of male events in Beijing: ", len(df_male))
print("Number of female events in Beijing: ", len(df_female))

plt.figure(1, figsize=(12,12))
plt.subplot(211)
plt.title("Female events by hour")
plt.hist(df_female['timestamp'].map( lambda x: pd.to_datetime(x).dayofweek*24 + pd.to_datetime(x).hour ), bins=168)
plt.subplot(212)
plt.title("Male events by hour")
plt.hist(df_male['timestamp'].map( lambda x: pd.to_datetime(x).dayofweek*24 + pd.to_datetime(x).hour ), bins=168)
plt.show()


# OK, there are some gender differences there. Women generally seem to have more of a rest in the early hours of the morning, with the notable exception of Friday night/Saturday morning, where they're even more likely than the men to be active. There's also a very large spike on Thursday evening. Could this be after-work drinks?
# 
# ### What about age?

# In[ ]:


df_under = df_joined[df_joined["age"]<30]
df_between = df_joined[(df_joined["age"]>=30) & (df_joined["age"]<40)]
df_over = df_joined[df_joined["age"]>=40]
print("Number of under-30s events in Beijing: ", len(df_under))
print("Number of 30-something events in Beijing: ", len(df_between))
print("Number of over-40s events in Beijing: ", len(df_over))

plt.figure(1, figsize=(12,18))
plt.subplot(311)
plt.title("Under-30s events by hour")
plt.hist(df_under['timestamp'].map( lambda x: pd.to_datetime(x).dayofweek*24 + pd.to_datetime(x).hour ), bins=168)
plt.subplot(312)
plt.title("30-something events by hour")
plt.hist(df_between['timestamp'].map( lambda x: pd.to_datetime(x).dayofweek*24 + pd.to_datetime(x).hour ), bins=168)
plt.subplot(313)
plt.title("Over-40s events by hour")
plt.hist(df_over['timestamp'].map( lambda x: pd.to_datetime(x).dayofweek*24 + pd.to_datetime(x).hour ), bins=168)
plt.show()


# Interesting. Looks like our over-40s are really busy on Saturday afternoons.
# 
# There's a similar bump on Friday night for the under-30s as for the women... that suggests that an event just after midnight on Friday night/Saturday morning is disproportionately likely to be both female and under 30. What are the actual ratios?

# In[ ]:


idx_friday_night = df_joined['timestamp'].map( lambda x: (pd.to_datetime(x).dayofweek==5) & (pd.to_datetime(x).hour < 6) )
df_friday_night = df_joined[idx_friday_night]
print("Number of Friday night events: ", len(df_friday_night))
print("Number of unique devices: ", df_friday_night["device_id"].nunique())

print("\nBeijing Night Owls:")
df_friday_night["group"].value_counts()


# That fits our intuition from the other charts, then. Given that males outnumber females 2:1 in the data, and it's a small age range, that's quite a striking 'win' for F24-26 to represent a full 20% of the Friday night events.
# 
# Does this pattern apply more generally? And what are the overall user ratios?

# In[ ]:


print("Total users: ", len(df_gender_age))
print("\nUser group counts:")
df_gender_age["group"].value_counts()


# Wow, so 1/17th (5.6%) of the users (F24-26) account for 1/5th (20.1%) of Friday night events in Beijing.
# 
# It's too slow trying to check the whole of China, so I think I need to fix how I'm doing time calculations... to be continued in another Notebook.
