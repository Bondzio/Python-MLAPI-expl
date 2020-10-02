#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory


import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# # Titanic discussion analysis
# 
# Using Beautiful Soup I scraped the discussion in the most popular Kaggle competition: Titanic
# For every topic I extracted the following variables:
# - Title of the topic
# - Tier of the author
# - Number of votes
# - Number of comments
# - Date of post
# 
# The idea is to do some text modelling on the different topics, but since I'm still learning and I kept postponing finishing the basis part of the notebook looking for the perfect approach, I decided to publish the descriptive analysis. The code is not very Pythonesque, but I wanted to focus on the result. Soon, I will do the text analysis on the titles.
# 
# Any feedback would be greatly appreciated.
# 
# 

#  ## Data description

# > ### Data overview
# The webscrape took place in august 2018. After cleaning the data and removing one row with a missing title. The data looks like this

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import datetime as dt
from datetime import timedelta


df = pd.read_csv('../input/output_raw.csv')
df['Post date'] = pd.to_datetime(df['Post date'])
df.head()


# datetime.datetime.strptime(row["Time"], "%Y-%m-%d %H:%M:%S") - datetime.timedelta(hours=3)
df['Post date'] = df['Post date'].apply(lambda x: x - dt.timedelta(hours=6))
df.head()


# In[ ]:


df.info()


# In[ ]:


df.describe()


# ### Topic titles
# 
# The topic titles are all strings. The boxplot shows the distribution of the length by tier. Although most of the titles are around the same length, you can clearly see how the masters and especially grandmasters use considerably shorter titles.

# In[ ]:


df["Title"].str.len().describe()


# In[ ]:


fig, axes = plt.subplots(figsize=(10,10))

axes.boxplot([df['Title'].str.len().dropna(),
             df[df['Tier']=='novice']['Title'].str.len().dropna(),
             df[df['Tier']=='contributor']['Title'].str.len().dropna(),
             df[df['Tier']=='expert']['Title'].str.len().dropna(),
             df[df['Tier']=='master']['Title'].str.len().dropna(),
             df[df['Tier']=='grandmaster']['Title'].str.len().dropna(),
             df[df['Tier']=='staff']['Title'].str.len().dropna(),])
axes.set_xticklabels(['total', 'novice', 'contributor', 'expert', 'master', 'grandmaster', 'staff'])
axes.set_ylim(0,150)

axes.set_title('Length of topic title - boxplot', fontsize=15)


# In[ ]:


df['Title'].value_counts().head(15)


# ### Votes

# In[ ]:


fig, axes = plt.subplots(figsize=(10,10))


axes.boxplot([df['Title'].str.len().dropna(),
             df[df['Tier']=='novice']['Votes'].dropna(),
             df[df['Tier']=='contributor']['Votes'].dropna(),
             df[df['Tier']=='expert']['Votes'].dropna(),
             df[df['Tier']=='master']['Votes'].dropna(),
             df[df['Tier']=='grandmaster']['Votes'].dropna(),
             df[df['Tier']=='staff']['Votes'].dropna(),])
axes.set_xticklabels(['total', 'novice', 'contributor', 'expert', 'master', 'grandmaster', 'staff'])
axes.set_ylim(0,500)

axes.set_title('Number of votes - boxplot', fontsize=15)


# Where novice posts rarely get votes, the numbers increase when the tier of the user is higher. Again, especially the grandmaster's post are rated significantly higher on average. 

# ### Comments

# In[ ]:


fig, axes = plt.subplots(figsize=(10,10))

axes.boxplot([df['Title'].str.len().dropna(),
             df[df['Tier']=='novice']['Number comments'].dropna(),
             df[df['Tier']=='contributor']['Number comments'].dropna(),
             df[df['Tier']=='expert']['Number comments'].dropna(),
             df[df['Tier']=='master']['Number comments'].dropna(),
             df[df['Tier']=='grandmaster']['Number comments'].dropna(),
             df[df['Tier']=='staff']['Number comments'].dropna(),])
axes.set_xticklabels(['total', 'novice', 'contributor', 'expert', 'master', 'grandmaster', 'staff'])
axes.set_ylim(0,250)

axes.set_title('Number of comments - boxplot', fontsize=15)


# Just like numbers for the votes, a higher tier results in more comments. Please notice the scale on the y-axis is different from the previous chart.

#  ## Trends over time

# In[ ]:


df = df.drop(df.index[1554]) # Outlier
df_to2017 = df[df['Post date'].dt.year < 2018]


# In[ ]:


x = []
for item in np.sort(df_to2017['Post date'].dt.to_period("M").unique()):
    x.append(item.to_timestamp())

def time_series(tier):
    series = df_to2017[df_to2017['Tier'] == tier]['Title'].groupby(df_to2017['Post date'].dt.to_period("M")).agg('count')
    list_ts = []
    for item in np.sort(df_to2017['Post date'].dt.to_period("M").unique()):
        if len(series[series.index== item].values) == 0:
            list_ts.append(0)
        else:
            list_ts.append(series[series.index== item].values[0])
    return(list_ts)  
    
y = []
y.append(time_series('novice'))
y.append(time_series('contributor'))
y.append(time_series('expert'))
y.append(time_series('master'))
y.append(time_series('grandmaster'))
y.append(time_series('staff'))

fig, axes = plt.subplots(figsize=(20,10))
plt.stackplot(x,y, labels=['Novice','Contributor','Expert', 'Master', 'Grandmaster', 'Staff'])
plt.legend(loc='upper left')
plt.title('Number of posts by month', fontsize=20)
plt.xticks(fontsize=15)
plt.show()


# 

# In[ ]:


bar_data = df.groupby([(df['Post date'].dt.year),'Tier'])['Title'].size().reset_index()
bar_data = bar_data.set_index(["Post date", "Tier"]).unstack(level=0)

bar_data.columns = ['2012','2013','2014','2015','2016','2017','2018']
bar_data.fillna(0, inplace=True)

for year in list(bar_data):
    bar_data[year] = bar_data[year].apply(lambda x: (x / (bar_data[year].sum())))
from matplotlib import rc
 
fig, axes = plt.subplots(figsize=(20,10))

# y-axis in bold
rc('font', weight='bold')
 
# Values of each group
bars1 = bar_data.iloc[4,:] # novice
bars2 = bar_data.iloc[0,:] # contributor
bars3 = bar_data.iloc[1,:] # expert
bars4 = bar_data.iloc[3,:] # master
bars5 = bar_data.iloc[2,:] # grandmaster
bars6 = bar_data.iloc[5,:] # staff

# The position of the bars on the x-axis
r = [0,1,2,3,4,5,6]
 
names = ['2012','2013','2014','2015','2016','2017','2018']
barWidth = 0.9
 
plt.bar(r, bars1, color='#003f5c', edgecolor='white', width=barWidth)
plt.bar(r, bars2, bottom=bars1, color='#444e86', edgecolor='white', width=barWidth)
plt.bar(r, bars3, bottom=(bars1+bars2), color='#955196', edgecolor='white', width=barWidth)
plt.bar(r, bars4, bottom=(bars1+bars2+bars3), color='#dd5182', edgecolor='white', width=barWidth)
plt.bar(r, bars5, bottom=(bars1+bars2+bars3+bars4), color='#ff6e54', edgecolor='white', width=barWidth)
plt.bar(r, bars6, bottom=(bars1+bars2+bars3+bars4+bars5), color='#ffa600', edgecolor='white', width=barWidth)

plt.xticks(r, names, fontweight='bold', fontsize=15)
plt.legend(['Novice', 'Contributor', 'Expert', 'Master', 'Grandmaster', 'Staff'])
plt.ylim((0,1.05))
plt.title('Annual contribution by tier', fontsize=20)
plt.show()


# These charts clearly show the growth Kaggle has been experiencing over the last few years, especially from 2016 onwards.  The stacked barplot demonstrate how the share of novice contributions decreases. This should be a good thing, as it should translate in more contributions of higher ranked users. 

# ## Most popular times

# In[ ]:


import calendar
fig, axes = plt.subplots(figsize=(20,10))

y = []
for item in np.sort(df_to2017['Post date'].dt.month.unique()):
    y.append(calendar.month_name[item])

x = ((df_to2017['Title'].groupby(df_to2017['Post date'].dt.month).agg('count')).values)
plt.subplot2grid((2,2),(0,0), colspan=2)
plt.title('Number of posts by month', fontsize=20)
plt.xticks(fontsize=15)


plt.bar(y, x)

x = ((df_to2017['Votes'].groupby(df_to2017['Post date'].dt.month).agg('mean')).values)
plt.subplot2grid((2,2),(1,0))
plt.xticks(rotation=45)
plt.title('Average # votes per post', fontsize=20)
plt.xticks(fontsize=15)
plt.bar(y, x)

x = ((df_to2017['Number comments'].groupby(df_to2017['Post date'].dt.month).agg('mean')).values)
plt.subplot2grid((2,2),(1,1))
plt.xticks(rotation=45)
plt.title('Average # comments per post', fontsize=20)
plt.xticks(fontsize=15)


plt.bar(y, x)

plt.tight_layout()
plt.show()


# Especially during the winter (holiday) period the number of posts, votes and comment go up. Most likely because for most data scientist use Kaggle in their spare time.

# In[ ]:


## import calendar
fig, axes = plt.subplots(figsize=(20,10))

y = []
for item in np.sort(df_to2017['Post date'].dt.weekday.unique()):
    y.append(calendar.day_name[item])

x = ((df_to2017['Title'].groupby(df_to2017['Post date'].dt.weekday).agg('count')).values)
plt.subplot2grid((2,2),(0,0), colspan=2)
plt.title('Number of posts by weekday', fontsize=20)
plt.bar(y, x)

x = ((df_to2017['Votes'].groupby(df_to2017['Post date'].dt.weekday).agg('mean')).values)
plt.subplot2grid((2,2),(1,0))
plt.title('Average # votes per post', fontsize=20)
plt.bar(y, x)

x = ((df_to2017['Number comments'].groupby(df_to2017['Post date'].dt.weekday).agg('mean')).values)
plt.subplot2grid((2,2),(1,1))
plt.title('Average # comments per post', fontsize=20)
plt.bar(y, x)

plt.tight_layout()
plt.show()


# The trend from the previous chart where we can see more activity during the holiday period is confirmed in the weekly numbers. Given that the popularity is by far the highest on Sundays. 

# In[ ]:


import calendar
fig, axes = plt.subplots(figsize=(20,10))

y = []
for item in np.sort(df_to2017['Post date'].dt.hour.unique()):
    y.append(item)

x = ((df_to2017['Title'].groupby(df_to2017['Post date'].dt.hour).agg('count')).values)
plt.subplot2grid((2,2),(0,0), colspan=2)
plt.title('Number of posts by hour of the day (UTC-5)', fontsize=20)
plt.bar(y, x)

x = ((df_to2017['Votes'].groupby(df_to2017['Post date'].dt.hour).agg('mean')).values)
plt.subplot2grid((2,2),(1,0))
plt.title('Average # votes per post', fontsize=20)
plt.bar(y, x)

x = ((df_to2017['Number comments'].groupby(df_to2017['Post date'].dt.hour).agg('mean')).values)
plt.subplot2grid((2,2),(1,1))
plt.title('Average # comments per post', fontsize=20)
plt.bar(y, x)

plt.tight_layout()
plt.show()


# In[ ]:


# ORGINAL TIME HEATMAP

df_matrix = pd.DataFrame(columns=['Sup'])

for week in df['Post date'].dt.weekday.unique():
    # print(week)
    # print(df_to2017[df_to2017['Post date'].dt.weekday == week].groupby(df_to2017['Post date'].dt.hour)['Votes'].mean())
    df_matrix = df_matrix.append((df_to2017[df_to2017['Post date'].dt.weekday == week].groupby(df['Post date'].dt.hour)['Title'].size()), ignore_index=True)

df_matrix = df_matrix.drop(['Sup'], axis=1)
df_matrix = df_matrix.applymap(lambda x: x/(df.shape[0]))
df_matrix

f, ax = plt.subplots(figsize=(20, 5))
ax = sns.heatmap(df_matrix,cmap='coolwarm')
ax.set_yticklabels(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday',], rotation=45)
plt.title('Proportion of posts by day/hour (UTC-5)', fontsize=20)
# ax.set_title('Proportion of posts by day/hour (UTC-5)', fontsize=20)


# Unlike aggregated data for months and days, it is harder to pinpoint the most popular moments by time, given that Kaggle is an international community. For these charts I used the UTC-5 (New York, US) time zone. 
# The peaks during the morning might be explained by these timezones, since during this time the early US Kaggles overlap with the late-night Europeans, given that those are the most active areas.
# 
# Combining the time trends, posting on a Sunday morning around the holiday period might be the best time to get exposure for your contribution. Given that I try to make data driven decisions, I reckon posting this at this very moment, should increase my chances in receiving valuable community feedback, which is - again - more than welcome.

# 
