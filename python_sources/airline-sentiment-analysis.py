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

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('ggplot')


# In[ ]:


data = pd.read_csv('../input/Tweets.csv')


# In[ ]:


tweet_created = []
for x in data.tweet_created:
    tweet_created.append(x[:19])


# In[ ]:


data['tweet_created'] = pd.to_datetime(data.tweet_created)
data['tweet_created_date'] = data.tweet_created.dt.date
data['tweet_created_time'] = data.tweet_created.dt.time
data['tweet_created_hour'] = data.tweet_created.dt.hour


# In[ ]:


data.head()


# In[ ]:


len(data.index) 


# In[ ]:


data.airline.value_counts()


# In[ ]:


colors=sns.color_palette("hls", 10) 
pd.Series(data["airline"]).value_counts().plot(kind = "bar",color=colors,figsize=(8,6),fontsize=10,rot = 0, title = "Airline")


# In[ ]:


data.airline_sentiment.value_counts()


# In[ ]:


colors=sns.color_palette("hls", 10)
pd.Series(data["airline_sentiment"]).value_counts().plot(kind = "bar",color=colors,figsize=(8,6),rot=0, title = "Total_Airline_Sentiment")


# In[ ]:


colors=sns.color_palette("hls", 10)
pd.Series(data["airline_sentiment"]).value_counts().plot(kind="pie",colors=colors,labels=["negative", "neutral", "positive"],explode=[0.05,0.02,0.04],shadow=True,autopct='%.2f', fontsize=12,figsize=(6, 6),title = "Total_Airline_Sentiment")


# In[ ]:


data.negativereason.value_counts()


# In[ ]:


colors=sns.color_palette("GnBu_d", 10) 
pd.Series(data["negativereason"]).value_counts().plot(kind = "barh",color=colors,figsize=(8,6),title = "Negative_Reasons")


# In[ ]:


data.negativereason.value_counts().head(5)


# In[ ]:


pd.Series(data["negativereason"]).value_counts().head(5).plot(kind="pie",labels=["Customer Service Issue", "Late Flight", "Can't Tell","Cancelled Flight","Lost Luggage"], colors=['r', 'g', 'b','c','y'],autopct='%.2f',explode=[0.05,0,0.02,0.03,0.04],shadow=True, fontsize=12,figsize=(6, 6),title="Negative Reasons")


# In[ ]:


data.tweet_location.value_counts()  ##overlap data


# In[ ]:


data.user_timezone.value_counts()


# In[ ]:


pd.Series(data["user_timezone"]).value_counts().head(10).plot(kind = "barh",figsize=(8,6),title = "User_Timezone")


# In[ ]:


air_sen=pd.crosstab(data.airline, data.airline_sentiment)
air_sen


# In[ ]:


percentage=air_sen.apply(lambda a: a / a.sum() * 100, axis=1)
percentage


# In[ ]:


pd.crosstab(index = data["airline"],columns = data["airline_sentiment"]).plot(kind='bar',figsize=(10, 6),alpha=0.5,rot=0,stacked=True,title="Airline_Sentiment")


# In[ ]:


percentage.plot(kind='bar',figsize=(10, 6),alpha=0.5,
                rot=0,stacked=True,title="Airline_Sentiment_Percentage")


# In[ ]:


date_sen=pd.crosstab(data.tweet_created_date, data.airline_sentiment)
date_sen


# In[ ]:


percentage2=date_sen.apply(lambda a: a / a.sum() * 100, axis=1)
percentage2


# In[ ]:


pd.crosstab(index = data["tweet_created_date"],columns = data["airline_sentiment"]).plot(kind='barh',figsize=(12, 8),alpha=0.5,rot=0,stacked=True,title="Airline_Sentiment_by_Date")


# In[ ]:


percentage2.plot(kind='barh',figsize=(12, 8),alpha=0.5,rot=0,stacked=True,title="Airline_Sentiment_by_Date_Percentage")


# In[ ]:


df = data.groupby(['tweet_created_date','airline'])
df = df.airline_sentiment.value_counts()
df.unstack()


# In[ ]:


my_plot = df.unstack().plot(kind='bar',stacked=True,figsize=(24, 16),title="Airline Sentiment by date and Airline")
my_plot.set_xlabel("Airline")
my_plot.set_ylabel("Reviews")


# In[ ]:


pf = data.groupby(['tweet_created_hour']).negativereason.value_counts()
pf.unstack()


# In[ ]:


my_plot = pf.unstack().plot(kind='line',figsize=(12, 8),rot=0,title="Negetive Reasons by Time")
my_plot.set_xlabel("Time")
my_plot.set_ylabel("Negative Reason")
#8:AM to 2:PM customer service issue 
#2:pm to 7:pm late flight
#9:AM cancelled flight


# In[ ]:


my_plot = pf.unstack().plot(kind='bar',stacked=True,figsize=(12, 8),rot=0,title="Negetive Reasons by Time")
my_plot.set_xlabel("Time")
my_plot.set_ylabel("Negative Reason")


# In[ ]:




