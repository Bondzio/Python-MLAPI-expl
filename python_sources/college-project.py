#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
df = pd.read_csv('/kaggle/input/udemy-courses/udemy_courses.csv')


# In[ ]:


df.columns


# In[ ]:


df.drop(columns = ['course_id', 'course_title', 'url'],axis= 1,inplace = True)


# In[ ]:


df.head()


# In[ ]:


df_price = df.groupby(by='subject').sum()[['price']]
df_price.reset_index(inplace = True)
df_price


# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111)
ax.bar(x= df_price['subject'],height=df_price['price'], label = 'Price',width = 0.2,color = 'red')
#df_price.plot(kind = 'bar',ax=ax)
ax.set_ylabel('Net Price ($) of Coures avliable for Subjects')
ax.set_xlabel('Subject')
ax.set_title('Net Price Vs Subject')
ax.legend()


# In[ ]:


df_sub = df.groupby(by ='subject').sum()[['num_subscribers']]
df_sub.reset_index(inplace = True)
df_sub.rename(columns = {'num_subscribers':'NumOfSubcribers','subject':'Subject'},inplace =True)
df_sub['Subject']


# In[ ]:


fig1 = plt.figure(figsize=(10,8))
ax1 = fig1.add_subplot(111)
NumSub = round(df_sub['NumOfSubcribers']/1000)
ax1.bar(x= df_sub['Subject'],height = NumSub,color = 'blue',label = 'Number of Subcribers',width= 0.3)
ax1.set_title('Number of Subcribers Vs Subject')
ax1.set_ylabel('Number of Subscriber in Thousands') 
ax1.set_xlabel('Subjects')
ax1.legend()


# In[ ]:


df['is_paid'].value_counts()


# In[ ]:


df.groupby(by = 'is_paid').sum()


# In[ ]:


fig2 = plt.figure(figsize=(10,8))
ax2 = fig2.add_subplot(111)
df.groupby(by='level').sum()[['num_lectures']].plot(kind = 'bar',
                                                    title = 'Number of Lectures for different Levels Vs Levels',
                                                    ax=ax2,
                                                    width = 0.3,
                                                    )
ax2.set_xlabel('Levels')
ax2.set_ylabel('Number of Subscribers')
ax2.legend(['Subscribers'])


# In[ ]:


df['RevenueGenrated'] = df['num_subscribers']*df['price']
df_rev = df.groupby(by='subject')[['RevenueGenrated']].sum()
df_rev.reset_index(inplace = True)
df_rev


# In[ ]:


fig_rev = plt.figure(figsize=(10,8))
ax_rev = fig_rev.add_subplot(111)
ax_rev.bar(x=df_rev['subject'],height = df_rev['RevenueGenrated']/1000000,width = 0.2,label = 'Subjects')
ax_rev.set_ylabel('Revenue Generated by each subject in millions dollars ',fontsize = 12)
ax_rev.set_xlabel('Subjects',fontsize = 12)
ax_rev.set_title('Revenue Generated by Udemy for each subjects',fontsize = 12)
ax_rev.legend(fontsize = 12)


# In[ ]:


import plotly
import plotly.express as px
import plotly.graph_objects as go


# In[ ]:


df1=df['subject'].value_counts().reset_index()
fig=go.Figure(data=[go.Pie(labels=df1['index'],
                          values=df1['subject'],
                          hole=.4,
                          title="Share of each Course")])
fig.update_layout(title="Udemy Course Subjects")
fig.show()


# Revenue generated by each subject

# In[ ]:


df['RevenueGenrated'] = df['num_subscribers']*df['price']
df_rev = df.groupby(by='subject')[['RevenueGenrated']].sum()
df_rev.reset_index(inplace = True)
df_rev


# In[ ]:


fig_rev = plt.figure(figsize=(10,8))
ax_rev = fig_rev.add_subplot(111)
ax_rev.bar(x=df_rev['subject'],height = df_rev['RevenueGenrated']/1000000,width = 0.2,label = 'Subjects')
ax_rev.set_ylabel('Revenue Generated by each subject in millions dollars ',fontsize = 12)
ax_rev.set_xlabel('Subjects',fontsize = 12)
ax_rev.set_title('Revenue Generated by Udemy for each subjects',fontsize = 12)
ax_rev.legend(fontsize = 12)


# In[ ]:




