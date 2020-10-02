#!/usr/bin/env python
# coding: utf-8

# # Introduction

# ### In this pandemic situation, a survey was conducted to check the availability of students for participating in online classes. The participants on this survey were the students (2k18 Batch) of CSE Department of KUET (Khulna University of Engineering & Technology). KUET is one of the most renowned and prestigious universities of Bangladesh.

# # Import Libraries

# In[ ]:


import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
from textblob import TextBlob
import matplotlib.pyplot as plt
import nltk
import matplotlib as mpl
import statistics as st
from itertools import chain
from operator import add
import re
import functools as func
import plotly.graph_objects as go


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


df=pd.read_csv('../input/bangladesh-online-classes-survey-kuetcse18/KUETCSE18.csv')

df.head()


# # District wise sort

# In[ ]:


f, ax = plt.subplots(figsize=(12, 15))
sns.countplot(y='District',data=df, color="r",
             order=df['District'].value_counts().index);


# # Upazilla/Thana wise sort

# In[ ]:


f, ax = plt.subplots(figsize=(12, 18))
sns.countplot(y='Upazila_Thana',data=df, color="r",
             order=df['Upazila_Thana'].value_counts().index);


# # Required Device Availability (Access to the required device needed to reach for the online classes)

# In[ ]:


print(df['Required Device Availability (Access to the required device needed to reach for the online classes)'].value_counts())

sns.countplot(df['Required Device Availability (Access to the required device needed to reach for the online classes)']);


# # Availability of Broadband Connection

# In[ ]:


print(df['Broadband Connection'].value_counts())

sns.countplot(df['Broadband Connection']);


# # Two Month Net (If you don't have broadband connection, will you be able to buy mobile data for two months)

# In[ ]:


print(df['Two Month Net (If you don\'t have broadband connection, will you be able to buy mobile data for two months)'].value_counts())

sns.countplot(df['Two Month Net (If you don\'t have broadband connection, will you be able to buy mobile data for two months)']);


# # Cellular Quality

# In[ ]:


print(df['Cellular Quality'].value_counts())

sns.countplot(df['Cellular Quality']);


# In[ ]:


fig = df['Cellular Quality'].value_counts().plot(kind='pie', 
                                    figsize = (5,5), 
                                    autopct = lambda p : '{:,.0f}'.format(p * df['Cellular Quality'].count()/100) , 
                                    subplots = True,
                                    colormap = "plasma_r", 
                                    title = 'Cellular Network Type', 
                                    fontsize = 15)


# # Net Speed

# In[ ]:


print(df['Net Speed'].value_counts())

sns.countplot(df['Net Speed']);


# In[ ]:


fig = df['Net Speed'].value_counts().plot(kind='pie', 
                                    figsize = (5,5), 
                                    autopct = lambda p : '{:,.0f}'.format(p * df['Net Speed'].count()/100) , 
                                    subplots = True,
                                    colormap = "Accent", 
                                    title = 'Net Speed', 
                                    fontsize = 15)


# # Hall (Resident or Attached to a hall)

# In[ ]:


print(df['Hall'].value_counts())

sns.countplot(df['Hall']);


# # Books availability (At Hall / With you)

# In[ ]:


print(df['Books'].value_counts())

sns.countplot(df['Books']);


# # Class System Preference

# In[ ]:


print(df['Class System Preference'].value_counts())

# Processing Data

recorded = []
recorded.append(len(df.loc[df['Class System Preference'] == 'Recorded Video, Uploaded Lecture Notes (PPT, Word or PDF)']))
recorded.append(len(df.loc[df['Class System Preference'] == 'Recorded Video']))
recorded.append(len(df.loc[df['Class System Preference'] == 'Recorded Video, Online Conference Platforms, Uploaded Lecture Notes (PPT, Word or PDF)']))
recorded.append(len(df.loc[df['Class System Preference'] == 'Recorded Video, Online Conference Platforms, Facebook/Youtube Live, Uploaded Lecture Notes (PPT, Word or PDF)']))
recorded.append(len(df.loc[df['Class System Preference'] == 'Recorded Video, Facebook/Youtube Live, Uploaded Lecture Notes (PPT, Word or PDF)']))
recorded.append(len(df.loc[df['Class System Preference'] == 'Recorded Video, Online Conference Platforms']))

uploaded = []
uploaded.append(len(df.loc[df['Class System Preference'] == 'Recorded Video, Uploaded Lecture Notes (PPT, Word or PDF)']))
uploaded.append(len(df.loc[df['Class System Preference'] == 'Uploaded Lecture Notes (PPT, Word or PDF)']))
uploaded.append(len(df.loc[df['Class System Preference'] == 'Recorded Video, Online Conference Platforms, Uploaded Lecture Notes (PPT, Word or PDF)']))
uploaded.append(len(df.loc[df['Class System Preference'] == 'Recorded Video, Online Conference Platforms, Facebook/Youtube Live, Uploaded Lecture Notes (PPT, Word or PDF)']))
uploaded.append(len(df.loc[df['Class System Preference'] == 'Recorded Video, Facebook/Youtube Live, Uploaded Lecture Notes (PPT, Word or PDF)']))
uploaded.append(len(df.loc[df['Class System Preference'] == 'Online Conference Platforms, Facebook/Youtube Live, Uploaded Lecture Notes (PPT, Word or PDF)']))
uploaded.append(len(df.loc[df['Class System Preference'] == 'Online Conference Platforms, Uploaded Lecture Notes (PPT, Word or PDF)']))

online = []
online.append(len(df.loc[df['Class System Preference'] == 'Recorded Video, Online Conference Platforms, Uploaded Lecture Notes (PPT, Word or PDF)']))
online.append(len(df.loc[df['Class System Preference'] == 'Online Conference Platforms']))
online.append(len(df.loc[df['Class System Preference'] == 'Recorded Video, Online Conference Platforms, Facebook/Youtube Live, Uploaded Lecture Notes (PPT, Word or PDF)']))
online.append(len(df.loc[df['Class System Preference'] == 'Recorded Video, Facebook/Youtube Live, Uploaded Lecture Notes (PPT, Word or PDF)']))
online.append(len(df.loc[df['Class System Preference'] == 'Online Conference Platforms, Facebook/Youtube Live, Uploaded Lecture Notes (PPT, Word or PDF)']))
online.append(len(df.loc[df['Class System Preference'] == 'Online Conference Platforms, Uploaded Lecture Notes (PPT, Word or PDF)']))

live = []
live.append(len(df.loc[df['Class System Preference'] == 'Recorded Video, Online Conference Platforms, Facebook/Youtube Live, Uploaded Lecture Notes (PPT, Word or PDF)']))
live.append(len(df.loc[df['Class System Preference'] == 'Recorded Video, Facebook/Youtube Live, Uploaded Lecture Notes (PPT, Word or PDF)']))
live.append(len(df.loc[df['Class System Preference'] == 'Online Conference Platforms, Facebook/Youtube Live, Uploaded Lecture Notes (PPT, Word or PDF)']))
live.append(len(df.loc[df['Class System Preference'] == 'Facebook/Youtube Live']))

labels = ['Recorded Video', 'Online Conference Platforms', 'Uploaded Lecture Notes (PPT, Word or PDF)', 'Facebook/Youtube Live']
sizes = [sum(recorded), sum(uploaded), sum(online), sum(live)]

import plotly.graph_objects as go

# Use textposition='auto' for direct text
fig = go.Figure(data=[go.Bar(
            x=labels, y=sizes,
            text=sizes,
            textposition='auto',
        )])

fig.update_traces(marker_color='rgb(100,100,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=3)
fig.update_layout(title_text='Class System Preference')
fig.show()


# # Prefered Assessment Method

# In[ ]:


print(df['Prefered Assessment Method'].value_counts())

# Processing Data

online = []
online.append(len(df.loc[df['Prefered Assessment Method'] == 'After resuming the offline classes, Through online platforms, Both of these as per requirement']))
online.append(len(df.loc[df['Prefered Assessment Method'] == 'Through online platforms, Both of these as per requirement']))
online.append(len(df.loc[df['Prefered Assessment Method'] == 'After resuming the offline classes, Through online platforms']))
online.append(len(df.loc[df['Prefered Assessment Method'] == 'Through online platforms']))
online.append(len(df.loc[df['Prefered Assessment Method'] == 'After resuming the offline classes, Both of these as per requirement']))
online.append(len(df.loc[df['Prefered Assessment Method'] == 'Both of these as per requirement']))

offline = []
offline.append(len(df.loc[df['Prefered Assessment Method'] == 'After resuming the offline classes, Through online platforms, Both of these as per requirement']))
offline.append(len(df.loc[df['Prefered Assessment Method'] == 'After resuming the offline classes']))
offline.append(len(df.loc[df['Prefered Assessment Method'] == 'After resuming the offline classes, Through online platforms']))
offline.append(len(df.loc[df['Prefered Assessment Method'] == 'After resuming the offline classes, Both of these as per requirement']))
offline.append(len(df.loc[df['Prefered Assessment Method'] == 'Through online platforms, Both of these as per requirement']))
offline.append(len(df.loc[df['Prefered Assessment Method'] == 'Both of these as per requirement']))

both = []
both.append(len(df.loc[df['Prefered Assessment Method'] == 'After resuming the offline classes, Through online platforms, Both of these as per requirement']))
both.append(len(df.loc[df['Prefered Assessment Method'] == 'After resuming the offline classes, Through online platforms']))
both.append(len(df.loc[df['Prefered Assessment Method'] == 'After resuming the offline classes, Both of these as per requirement']))
both.append(len(df.loc[df['Prefered Assessment Method'] == 'Through online platforms, Both of these as per requirement']))
both.append(len(df.loc[df['Prefered Assessment Method'] == 'Both of these as per requirement']))


# Plot

labels = ['After resuming the offline classes', 'Through online platforms', 'Both of these as per requirement']
sizes = [sum(online), sum(offline), sum(both)]

# Use textposition='auto' for direct text
fig = go.Figure(data=[go.Bar(
            x=labels, y=sizes,
            text=sizes,
            textposition='auto',
        )])

fig.update_traces(marker_color='rgb(100,100,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=3)
fig.update_layout(title_text='Prefered Assessment Method')
fig.show()


# # Comments

# In[ ]:


print(df['Comments'].value_counts())


# # References:
# 
# * https://www.kaggle.com/tasnimnishatislam/bangladesh-online-survey
# 
# * https://www.kaggle.com/sazinsamin/online-class-analysis
# 
# 
# ## Please upvote if you like it.
# 
# ## Thank You!
# 
# 

# In[ ]:




