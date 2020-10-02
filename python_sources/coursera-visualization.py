#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/lakshmansamvith/Coursera-Data-Visualization/blob/master/Coursera.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Import Dataset 

# In[ ]:


import pandas as pd 
import numpy as np 
coursera_df = pd.read_csv(r'/kaggle/input/coursera-course-dataset/coursea_data.csv')


# # Check for Null Values 

# In[ ]:


coursera_df.isnull().any()


# # Checking for Categorical Values and Removing Unecessary Columns

# In[ ]:


categorical_values = (coursera_df.dtypes == 'Object')
unique_variables = [col for col in coursera_df.columns if len(coursera_df[col].unique())<50]
print(unique_variables)
coursera_df.drop(labels=['Unnamed: 0'], axis=1, inplace=True)
coursera_df


# # Converting Course_students_enrolled into a numeric value

# In[ ]:


import re
students_enrolled = coursera_df['course_students_enrolled'].copy()
for ind, val in enumerate(students_enrolled):
    if re.search('m$', students_enrolled[ind]):
       students_enrolled[ind] = students_enrolled[ind].replace('m', '')
       students_enrolled[ind] = str(float(students_enrolled[ind].replace('.', ''))*100)  
    elif re.match('.\.', students_enrolled[ind] ):
       students_enrolled[ind] = students_enrolled[ind].replace('k', '0')
    else: 
       students_enrolled[ind] = students_enrolled[ind].replace('k', '.0')    

student_enrolled_values = [int((float(val)*1000)) for val in students_enrolled]
coursera_df['course_students_enrolled'] = student_enrolled_values


# # Plotting Bar Graph For Top 5 Courses By No of Course Students Enrolled 
# 
# > Indented block
# 
# 

# In[ ]:


import seaborn as sns 
import matplotlib.pyplot as plt 
plt.figure(figsize=(25, 12))
copy_df = coursera_df.sort_values(by=['course_students_enrolled'], ascending=False)
sns.barplot(x=copy_df['course_title'].iloc[:5], y=copy_df['course_students_enrolled'].iloc[:5], label='Course and Strenght Plot')
plt.grid()
plt.xlabel('Course Names')
plt.ylabel('Number of students enrolled in millions')
plt.legend()
plt.figure(figsize=(15, 12))
sns.barplot(x=copy_df['course_organization'].iloc[:5], y=copy_df['course_students_enrolled'].iloc[:5], label='Course Organization')
plt.xlabel('Course_Organization')
plt.ylabel('Number of students enrolled in millions')


# # Countplot for Courses of different ratings

# In[ ]:


copy_df = copy_df.sort_values(by=['course_rating'], ascending=False)
plt.figure(figsize=(20,15))
sns.countplot('course_rating', data=copy_df,)


# # PieChart for percentage of courses according to course_difficulty

# In[ ]:


course_difficulties = list(copy_df['course_difficulty'].unique())
ratios = list((copy_df['course_difficulty'].value_counts()/len(copy_df))*100)
explode=(0.1, 0, 0, 0)
colors = ['violet', 'skyblue', 'white', 'pink']
plt.figure(figsize=(10, 10))
plt.pie(ratios, explode=explode, labels=course_difficulties, shadow=True, autopct='%1.2f%%', colors=colors)


# # PieChart for % of Course_Certification_Types

# In[ ]:


course_types = list(copy_df['course_Certificate_type'].unique())
ratios = list((copy_df['course_Certificate_type'].value_counts()/len(copy_df))*100)
plt.figure(figsize=(10, 10))
plt.pie(ratios,  labels=course_types, shadow=True, autopct='%1.2f%%', )


# # Finding Courses Related to Python, Data Science

# In[ ]:


python_courses = [ val for val in copy_df['course_title']  if re.search('.Python' , val)]
data_science_courses = [ val for val in copy_df['course_title']  if re.search('.Data.Science' , val)]


# # Barplot for showing Top 5 Institutes which provide most of the courses on Coursera 

# In[ ]:


count_values = copy_df['course_organization'].value_counts()[:5]
unique_organizations = count_values.index
percentages = [((val/len(copy_df))*100) for val in count_values]
percentages
plt.figure(figsize=(20, 15))
plt.rcParams.update({'font.size': 12})
sns.barplot(x=unique_organizations, y=percentages, label='Top 5 Courses Providing Institutes')
plt.xlabel("Institutes providing Courses")
plt.ylabel("Percentage of courses by them")
plt.grid()

