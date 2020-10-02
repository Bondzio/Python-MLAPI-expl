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


# Read the given csv file

# In[ ]:


udemy_data = pd.read_csv('/kaggle/input/udemy-courses/udemy_courses.csv')
udemy_data.head()


# In[ ]:


udemy_data.describe()


# Remove duplicate records

# In[ ]:


udemy_data.drop_duplicates(inplace=True)


# In[ ]:


udemy_data.describe()


# In[ ]:


udemy_data.describe().isnull().any()


# Duplicates are removed and also dataset doesn't have missing values.

# Lets analyse how many paid courses and free courses are in udemy

# In[ ]:


is_paid_df = pd.DataFrame(udemy_data['is_paid'].value_counts())
is_paid_df.plot.bar(y='is_paid', legend=False, title='No of paid and free courses')


# It shows that there are more paid courses than free courses.
# Lets analyse which type of course is having more subscribers.

# In[ ]:


udemy_groupby_paid = udemy_data.sort_values(by=['num_subscribers'], ascending=False).groupby(by=['is_paid'])
avg_subscription_rate = udemy_groupby_paid['num_subscribers'].agg('mean')
avg_subscription_rate.plot.bar(y='is_paid', title='Average subscription rate')


# In[ ]:


sub_list = avg_subscription_rate.to_list()
sub_list


# Udemy has lot of paid courses.But subscription rate is higher for free courses which is evident from the above graph.

# In[ ]:


free_courses = udemy_groupby_paid.get_group(False)[['course_title','subject','num_subscribers']]
print(f'Before taking avg {len(free_courses)}')
free_courses['num_sub'] = free_courses['num_subscribers'].apply(lambda x:x>sub_list[0])
val = len(free_courses[free_courses['num_sub']==True])
print(f'After taking avg {val}')
free_course_count = free_courses[free_courses['num_sub']==True]['subject'].value_counts()
free_course_count


# In[ ]:


free_course_count.plot.pie(title='Average subscription on subject in free courses',autopct='%1.1f%%')


# In[ ]:


paid_courses = udemy_groupby_paid.get_group(True)[['course_title','subject','num_subscribers']]
print(f'Before taking avg {len(paid_courses)}')
paid_courses['num_sub'] = paid_courses['num_subscribers'].apply(lambda x:x>sub_list[1])
val = len(paid_courses[paid_courses['num_sub']==True])
print(f"After taking avg {val}")
paid_course_count = paid_courses[paid_courses['num_sub']==True]['subject'].value_counts()
paid_course_count


# In[ ]:


paid_course_count.plot.pie(title='Average subscription on subject in paid courses',autopct='%1.1f%%')


# Lets analyse how content_duration is impacting subscription rate

# In[ ]:


content_duration_df = udemy_data[['num_subscribers','content_duration','is_paid','subject','course_title']]
content_duration_df.drop(content_duration_df[content_duration_df['content_duration'] < 10].index, inplace = True)
content_duration_df.plot.scatter(x='content_duration', y='num_subscribers')


# From the above analysis it is found that if **content_duration < 25** more subscriptions are there
