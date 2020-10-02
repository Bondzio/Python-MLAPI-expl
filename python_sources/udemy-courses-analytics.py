#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import dates
import matplotlib.dates as mdates
import numpy as np
import plotly.express as px
get_ipython().run_line_magic('matplotlib', 'inline')

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# Let'see our data

# In[ ]:


udemy=pd.read_csv('../input/udemy-courses/udemy_courses.csv')
udemy=udemy.sort_values(['published_timestamp'])
udemy.drop([2066], inplace=True)
udemy.tail()


# Change 'published_timestamp' to datetimme 

# In[ ]:


udemy['published_timestamp']=pd.to_datetime(udemy['published_timestamp'],errors = 'coerce')
udemy.head()


# See How amount of offered courses and subscribers has been changing through the time

# In[ ]:


fig, ax = plt.subplots(1,2,figsize=(30,10))
ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m')) 
ax[0].plot(udemy.set_index("published_timestamp").groupby(pd.Grouper(freq='M')).subject.size(), label='amount')
ax[0].set_title('Amount of offered courses')
ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m')) 
ax[1].plot(udemy.set_index("published_timestamp").groupby(pd.Grouper(freq='M')).num_subscribers.sum())
ax[1].set_title('Amount of subscribers')
plt.legend()
plt.show()


# See How amount of offered courses and subscribers has been changing through the time for every subject

# In[ ]:


fig, ax = plt.subplots(4,2,figsize=(20,15))
ax[0,0].plot(udemy[udemy.subject=='Web Development'].set_index("published_timestamp").groupby(pd.Grouper(freq='M')).size(),color='g')
ax[0,1].plot(udemy[udemy.subject=='Web Development'].set_index("published_timestamp").groupby(pd.Grouper(freq='M')).num_subscribers.sum(),color='g')
ax[1,0].plot(udemy[udemy.subject=='Musical Instruments'].set_index("published_timestamp").groupby(pd.Grouper(freq='M')).size(), color='blue')
ax[1,1].plot(udemy[udemy.subject=='Musical Instruments'].set_index("published_timestamp").groupby(pd.Grouper(freq='M')).num_subscribers.sum(), color='blue')
ax[2,0].plot(udemy[udemy.subject=='Graphic Design'].set_index("published_timestamp").groupby(pd.Grouper(freq='M')).size(), color='red')
ax[2,1].plot(udemy[udemy.subject=='Graphic Design'].set_index("published_timestamp").groupby(pd.Grouper(freq='M')).num_subscribers.sum(), color='red')
ax[3,0].plot(udemy[udemy.subject=='Business Finance'].set_index("published_timestamp").groupby(pd.Grouper(freq='M')).size(), color='yellow')
ax[3,1].plot(udemy[udemy.subject=='Business Finance'].set_index("published_timestamp").groupby(pd.Grouper(freq='M')).num_subscribers.sum(), color='yellow')
ax[0,0].set_title('Web Development courses')
ax[0,1].set_title('Web Development subscribers')
ax[1,0].set_title('Musical Instruments courses')
ax[1,1].set_title('Musical Instruments subscribers')
ax[2,0].set_title('Graphic Design courses')
ax[2,1].set_title('Graphic Design subscribers')
ax[3,0].set_title('Business Finance courses')
ax[3,1].set_title('Business Finance subscribers')
plt.show()


# How amount of subscribers of free and paid courses has been changing

# In[ ]:


fig, ax = plt.subplots(1,2,figsize=(30,10))
ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m')) 
ax[0].plot(udemy[udemy.price==0].set_index("published_timestamp").groupby(pd.Grouper(freq='M')).num_subscribers.sum(), label='subscribers of free courses')
ax[0].set_title('subscribers of free courses')
ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m')) 
ax[1].plot(udemy[udemy.price!=0].set_index("published_timestamp").groupby(pd.Grouper(freq='M')).num_subscribers.sum(), label='Subscribers of paid courses')
ax[1].set_title('Subscribers of paid courses')
plt.legend()
plt.show()


# Let's see what profit paid courses has brought. Wee see that the most profitable subject is Web development and the most popular level among all subjects is "All levels"

# In[ ]:


udemy['profit']=udemy.num_subscribers*udemy.price
profit_info=pd.DataFrame(udemy.groupby(['subject', 'level']).profit.sum())
profit_info=profit_info.reset_index()



tidy_df = profit_info.melt(id_vars="subject")

fig = px.bar(profit_info, x="subject", y="profit", color='level', barmode="group", title='Profit of subject and level', template='seaborn')
fig.show()


# Let's see amount of subscribers for subjects and levels. Wee see that this graphic looks like the previous chart. Only Beginner level of Musical Instruments is not.

# In[ ]:


subs=udemy.groupby(['subject', 'level']).num_subscribers.sum()
subs=subs.reset_index()
tidy_df = profit_info.melt(id_vars="subject")

fig = px.bar(subs, x="subject", y="num_subscribers", color='level', barmode="group", title='Amount of subscribers of subject and level')
fig.show()


# Let's see Amount of subscribers of subject and level for free and paid courses. Wee see again the most popular subject is Web development, second is Business finance. For free courses amount of subscribers of All levels and Beginner level is quite the same, but for paid courses all levels courses is more popular.

# In[ ]:


subs1=udemy.groupby(['subject','is_paid', 'level']).num_subscribers.sum()
subs1=subs1.reset_index()
tidy_df = subs1.melt(id_vars=["subject", 'is_paid', 'level'])

fig = px.bar(tidy_df, x="is_paid", y="value", color='subject', hover_data=['level'], title='Amount of subscribers of subject and level for free and paid courses')
fig.update_xaxes(ticktext=['free', 'paid'])
fig.show()


# See the Distribution of Price and Number of subscribers. Surprisingly, free courses are not so popular. There is only 717K subscribers for free courses, 3,5M for paid courses with price = 20$, 1,3M for 120$

# In[ ]:


fig=px.scatter(x=udemy.price.unique(), y=udemy.groupby('price').num_subscribers.sum(), size=(udemy.groupby('price').num_subscribers.sum()), color=udemy.groupby('price').num_subscribers.sum(),
          title='Distribution of Price and Number of subscribers')
fig.update_xaxes(title_text='Price')
fig.update_yaxes(title_text='Num os suscribers')


#     TOP 25 FREE COURSES

# In[ ]:


v=udemy[udemy.is_paid==False].sort_values('num_subscribers', ascending=False)[:25]
fig=px.pie(v[:25], values='num_subscribers', names='course_title')
fig.show()


# TOP 25 FREE COURSES SUMMARY
# * The most popular sunject is Web development (17 courses)
# * All of them are All levels and Beginner level (14 and 11)
# * Mean number of reviews is 2923
# * Mean number of lecture is 33
# * Mean duration is 4

# In[ ]:


print(v.subject.value_counts())
print(v.level.value_counts())
print(v.num_reviews.mean())
print(v.num_lectures.mean())
print(v.content_duration.mean())


# TOP 25 PAID COURSES

# In[ ]:


c=udemy[udemy.is_paid==True].sort_values('num_subscribers', ascending=False)[:25]
fig=px.pie(v[:25], values='num_subscribers', names='course_title')
fig.show()


# TOP 25 PAID COURSES SUMMARY
# * The most popular subject is Web development
# * All of them are All levels
# * Mean number of reviews is 6884
# * Mean number of lecture is 158
# * Mean duration is 18
# * Mean price is 150$
# 
# 

# In[ ]:


print(c.subject.value_counts())
print(c.level.value_counts())
print(c.num_reviews.mean())
print(c.num_lectures.mean())
print(c.content_duration.mean())
print(c.price.mean())

