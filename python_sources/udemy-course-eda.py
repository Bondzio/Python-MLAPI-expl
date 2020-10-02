#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt


# In[ ]:


df = pd.read_csv("/kaggle/input/udemy-courses/udemy_courses.csv")


# In[ ]:


df.head()


# In[ ]:


df.info()


# In[ ]:


df.describe()


# In[ ]:


df['is_paid'].unique()
df['is_paid'] = df['is_paid'].astype('category')

df['level'].unique()
df['level'] = df['level'].astype('category')

df['subject'].unique()
df['subject'] = df['subject'].astype('category')


# ### Total number of courses by subject 

# In[ ]:


subjectCounts = df['subject'].value_counts()
fig = plt.figure(figsize = (10,10))
axes = fig.subplots(nrows=2)
fig.subplots_adjust(hspace=0.5)
axes[0].bar(subjectCounts.index,subjectCounts.values)
axes[0].tick_params('x', labelsize=12)
axes[0].set_title('Count of courses by subject', fontsize=18)
axes[0].set_xlabel('Subject category', fontsize=14, labelpad=14)
axes[0].set_ylabel('Count', fontsize=14)

axes[1].pie(subjectCounts.values, labels=subjectCounts.index,  autopct='%.1f', textprops={'fontsize':14})
axes[1].set_title('Count of courses by subject', fontsize=18)


# ### How many are paid courses

# In[ ]:


paidCount = df['is_paid'].value_counts()
fig = plt.figure(figsize = (14,4))
axes = fig.subplots(ncols=2)
axes[0].bar(paidCount.index,paidCount.values)
axes[0].tick_params('x', labelsize=12)
axes[0].set_title('Count of courses by price', fontsize=18)
axes[0].set_xticklabels(['paid', 'unpaid'])
axes[0].set_xlabel('Subject category', fontsize=14, labelpad=14)
axes[0].set_ylabel('Count', fontsize=14)

axes[1].pie(paidCount.values, labels=['paid', 'unpaid'], explode=[0,0.2], autopct='%.1f', textprops={'fontsize':14})
axes[1].set_title('Count of courses by price', fontsize=18)


# ### Distribution of prices

# In[ ]:


pricevscount = df.loc[:,['price','course_id']].groupby('price', as_index=False).count()
fig = plt.figure(figsize=[20,6])
axes = fig.add_axes([0,0,1,1])
axes.bar(pricevscount['price'], pricevscount['course_id'])
axes.set_xticks(pricevscount['price'].values)
axes.tick_params('x', labelsize=16)
axes.tick_params('y', labelsize=16)
axes.set_xlabel('Price', fontsize=20, labelpad=10)
axes.set_ylabel('Count', fontsize=20)
axes.set_title('Distribution of price', fontsize=24)


# In[ ]:


subjectGroup = df.groupby('subject', as_index=False).mean()
fig = plt.figure(figsize=[10,5])
axes = fig.subplots()
axes.bar(subjectGroup['subject'].values, subjectGroup['price'].values, color='g' )
axes.set_xlabel('Subject', fontsize=16)
axes.set_ylabel('Price', fontsize=16)
axes.set_title('Subject X Price', fontsize=18)


# ### # subscribers proportional to # reviews ?

# In[ ]:


subscribersandreviews = df.loc[:,['num_subscribers','num_reviews']].corr()
subscribersandreviews


# In[ ]:


fig = plt.figure(figsize=[10,8])
axes = fig.subplots()
axes.scatter(df['num_subscribers'], df['num_reviews'])
axes.set_xlabel('Number of subscribers', fontsize=16)
axes.set_ylabel('Number of reviews', fontsize=16)


# ### Top five courses with more subscribers

# In[ ]:


df.sort_values('num_subscribers', ascending=False).loc[:,'course_title'].head()


# ### Top five courses with more reviews

# In[ ]:


df.sort_values('num_reviews', ascending=False).loc[:,'course_title'].head()


# ### Top 10 popular courses in udemy

# In[ ]:


df.sort_values(['num_subscribers', 'num_reviews'], ascending=False).loc[:,'course_title'].head(10)


# ### Price of popular courses

# In[ ]:


df.sort_values(['num_subscribers', 'num_reviews'], ascending=False).loc[:,['course_title','price']].head(10)


# ### isUnpaid courses more popular

# In[ ]:


paidPopularityGroups = df.groupby('is_paid', as_index=False).mean()
fig = plt.figure(figsize=(10,4))
axes = fig.subplots(ncols=2)
fig.subplots_adjust(wspace=0.4)
axes[0].bar(paidPopularityGroups['is_paid'], paidPopularityGroups['num_subscribers'], color='g')
axes[1].bar(paidPopularityGroups['is_paid'], paidPopularityGroups['num_reviews'], color='y')
axes[0].set_xticks([0,1])
axes[1].set_xticks([0,1])
axes[0].set_xticklabels(['Unpaid', 'Paid'])
axes[1].set_xticklabels(['Unpaid', 'Paid'])
axes[0].set_ylabel('Number of subscribers', fontsize=14)
axes[1].set_ylabel('Number of reviews', fontsize=14)


# #### Its obvious that unpaid courses are popular

# ### Popularity by subject

# In[ ]:


subjectGroup = df.groupby('subject', as_index=False).mean()
fig = plt.figure(figsize=[20,5])
axes = fig.subplots(ncols=2)
axes[0].bar(subjectGroup['subject'].values, subjectGroup['num_subscribers'].values, color='g' )
axes[1].bar(subjectGroup['subject'].values, subjectGroup['num_reviews'].values, color='y' )
axes[0].set_xlabel('subject', fontsize='18')
axes[1].set_xlabel('subject', fontsize='18')
axes[0].set_ylabel('number of subscribers', fontsize=18)
axes[1].set_ylabel('number of reviews', fontsize=18)
axes[0].set_title('Popularity by subscribers', fontsize=20)
axes[1].set_title('Popularity by reviews', fontsize=20)


# #### Web development courses are more popular than business finance courses even though the count of both the courses are almost equal (1200 and 1195)

# ### Duration of popular courses

# In[ ]:


df.sort_values(['num_subscribers', 'num_reviews'], ascending=False).loc[:,['course_title','price', 'content_duration']].head(10)


# ### Distribution of content duration

# In[ ]:


fig = plt.figure(figsize=(20,10))
axes = fig.subplots()
axes.hist(df['content_duration'], bins=50)
axes.set_xlabel('Hours', fontsize='18')
axes.set_ylabel('Count', fontsize='18')


# In[ ]:


fig = plt.figure(figsize=(20,10))
axes = fig.subplots()
axes.hist(df[df['content_duration'] < 20]['content_duration'], bins=20)
axes.set_xlabel('Hours', fontsize='18')
axes.set_ylabel('Count', fontsize='18')


# #### Most courses are in the range of 1 to 5 hours

# ### Duration of paid and free courses

# In[ ]:


paidGroup = df.groupby('is_paid', as_index=False).mean()
fig = plt.figure(figsize=(10,4))
axes = fig.subplots()
axes.bar(paidGroup['is_paid'], paidGroup['content_duration'], color='g')
axes.set_xticks([0,1])
axes.set_xticklabels(['unpaid', 'paid'])
axes.set_ylabel('Hours')


# In[ ]:


fig = plt.figure(figsize=(20,10))
axes = fig.subplots()
axes.scatter(df['price'], df['content_duration'], color='g')
axes.set_xlabel('Price', fontsize=18)
axes.set_ylabel('Hours', fontsize=18)
axes.set_title('Price X Minutes', fontsize=20)


# ### Number of courses published every year

# In[ ]:


df['published_timestamp'] = pd.to_datetime(df['published_timestamp'])


# In[ ]:


df['year'] = df['published_timestamp'].dt.year
df['month_name'] = df['published_timestamp'].dt.month_name()
df['day'] = df['published_timestamp'].dt.day_name()

df['month_name'] = df['month_name'].astype(pd.CategoricalDtype(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ordered=True))
df['day'] = df['day'].astype(pd.CategoricalDtype(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True))


# In[ ]:


yearGroup = df.loc[:,['course_id', 'year', 'month_name', 'day']].groupby('year', as_index=False).count()
fig = plt.figure()
axes = fig.subplots()
axes.bar(yearGroup['year'], yearGroup['course_id'])
axes.set_xlabel('Year', fontsize=18)
axes.set_ylabel('Count', fontsize=18)


# In[ ]:


monthGroup = df.loc[:,['course_id', 'year', 'month_name', 'day']].groupby('month_name', as_index=False).count()
fig = plt.figure(figsize=(20,6))
axes = fig.subplots()
axes.bar(monthGroup['month_name'], monthGroup['course_id'])
axes.set_xlabel('Month', fontsize=18)
axes.set_ylabel('Count', fontsize=18)


# In[ ]:


dayGroup = df.loc[:,['course_id', 'year', 'month_name', 'day']].groupby('day', as_index=False).count()
fig = plt.figure(figsize=(20,6))
axes = fig.subplots()
axes.bar(dayGroup['day'], dayGroup['course_id'])
axes.set_xlabel('Month', fontsize=18)
axes.set_ylabel('Count', fontsize=18)


# #### Most courses were added during weekdays
