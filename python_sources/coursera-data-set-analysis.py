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


# import required packages

# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns


# regex function for finding numbers

# In[ ]:


import re
def extract_number(string_value):
    if string_value:
        extracted_num_list = re.findall('[1-9]\d*[\.\d*]*', string_value)
        return float(extracted_num_list[0])
    return 0


# In[ ]:


def preprocess_no_of_stu_enrolled(cell):
    if "k" in cell:
        num = extract_number(cell)*1000
        return num
    elif "m" in cell:
        num = extract_number(cell) * 1000000
        return num


# Read the input data and get statistical info about that data

# In[ ]:


coursera_data = pd.read_csv('/kaggle/input/coursera-course-dataset/coursea_data.csv')
coursera_data.describe()


# In[ ]:


coursera_data.head()


# In[ ]:


coursera_data.columns


# Check for any missing values

# In[ ]:


coursera_data.isnull().any()


# In[ ]:


coursera_data['course_students_enrolled'] = coursera_data['course_students_enrolled'].apply(lambda x: preprocess_no_of_stu_enrolled(x))


# Convert 'course_students_enrolled' column to float type

# In[ ]:


coursera_data.head()


# In[ ]:


coursera_data.describe()


# Find the top 5 most enrolled courses

# In[ ]:


top_5_courses = coursera_data.nlargest(5,'course_students_enrolled')
top_5_courses.head()


# Visualize the top 5 courses using bar graph

# In[ ]:


plt.figure(figsize=(10,8))
ax = sns.barplot(x='course_title', y='course_students_enrolled', data=top_5_courses)
ax.set_xticklabels(ax.get_xticklabels(), rotation=50, ha="right")
ax.set_xlabel('Course title')
ax.set_ylabel('No. of students enrolled')
ax.set_title('Top 5 courses')
plt.show()


# Find the total number of courses available in coursera based on the course difficulty 
# and visuallize it in a pie chart

# In[ ]:


total_courses = pd.DataFrame(coursera_data['course_difficulty'].value_counts())
total_courses.plot.pie(y='course_difficulty',figsize=(10,10),autopct='%1.1f%%',
                       title='No. of courses based on course difficulty', legend=False)


# Find the top 5 organizations contributing courses in coursera platform

# In[ ]:


top_organization = pd.DataFrame(coursera_data['course_organization'].value_counts()).nlargest(5,'course_organization')
top_organization.plot.pie(y='course_organization',figsize=(10,10),autopct='%1.1f%%',
                       title='Top 5 contributing organizations', legend=False)

