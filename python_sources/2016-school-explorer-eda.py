#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import matplotlib as matplot
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


school_data = pd.read_csv("../input/2016 School Explorer.csv")

# The column School Income Estimate is converted to Float Data type by removing $ and ,

school_data['School Income Estimate'] = school_data['School Income Estimate'].str.replace(',', '')
school_data['School Income Estimate'] = school_data['School Income Estimate'].str.replace('$', '')
school_data['School Income Estimate'] = school_data['School Income Estimate'].str.replace(' ', '')
school_data['School Income Estimate'] = school_data['School Income Estimate'].astype(float)


# In[ ]:


def percent_to_int(df_in):
    for col in df_in.columns.values:
        if col.startswith("Percent") or col.endswith("%") or col.endswith("Rate"):
            df_in[col] = df_in[col].astype(np.object).str.replace('%', '').astype(float)
    return df_in

school_data = percent_to_int(school_data)


# ** Question 1 **
#  **How many number of Schools  are there in every cities**
# 
#  **Find the top 5 districts  which has more number of schools**

# In[ ]:




school_count = school_data.pivot_table(index = 'City', values = 'School Name' ,aggfunc = 'count')



top_cities_school = school_count['School Name'].sort_values(ascending=False).iloc[:5]

# Plotting the top five count of schools in a bar graph

top_cities_school.plot.bar()


# ** Average School Income Estimate of the Top 5 Districts**

# In[ ]:




school_top_count = school_data.groupby('City')['School Name'].count().reset_index()

school_top_count = school_top_count.sort_values('School Name',ascending=False)

school_top_count=pd.DataFrame(school_top_count)

city = school_data.groupby('City')['Zip'].count().reset_index()

city = city.sort_values('Zip',ascending=False)

city=pd.DataFrame(city)

school_city_count =pd.merge(city,school_top_count,how='left', on='City')

top_5_cities = school_city_count.sort_values('School Name',ascending=False).iloc[:5,0]

top_5_data = school_data[school_data.City.isin(top_5_cities)]

top_5_data


sns.boxplot( x='School Income Estimate', y='City',data=top_5_data)

plt.title("Average School Income Estimate of the Top 5 Districts")

plt.xlabel("School Income Estimate")

plt.ylabel("District Name")

plt.show();


# *The above boxplot indicates that STATEN ISLAND district has an average income of 72000 USD compared to the Top 5 Districts with most number of schools *

# **Question 3**
# 
# **What is the relationship between Students Attendance rate and ( Collaborative Teachers,'Rigorous Instruction %',Supportive Environment %,Effective School Leadership %,Strong Family-Community Ties %,Trust %)**

# In[ ]:




features_list = ['Student Attendance Rate','Rigorous Instruction %',
'Collaborative Teachers %',
'Supportive Environment %',
'Effective School Leadership %',
'Strong Family-Community Ties %',
'Trust %']


# In[ ]:


top_5_data[ features_list ].corr()



plt.figure(figsize=(12, 10))


sns.heatmap(top_5_data[ features_list ].corr(), cmap='YlGnBu')


# *The Student Attendance rate doesnt have any correlation with other features like  'Rigorous Instruction %',Collaborative Teachers %, Supportive Environment%, Effective School Leadership %,Strong Family-Community Ties %,Trust %*
# 
# *But there exists some correlation between 
#      Trust and Collaborative Teachers %
#      Trust and Effective School Leadership %
#      Effective School Leadership % and Collaborative Teachers %*
# 

# **Question 4**
# 
#  **Is there any relationship between School Income Estimate and Community School?**

# In[ ]:


f,ax=plt.subplots(figsize=(6,6))
ax=plt.subplot(111)
sns.boxplot(y='School Income Estimate',x="Community School?",data=school_data,palette="Set1")
ax.set_title("School Incom Estimate vs. Community School?",size=15)
plt.show()


#  *From the above box plot it is evident that 
#             * Non-community schools have a high income than the community schools*

# **Question 5**
# 
# **What are the factors that impact the income of the School (Both community and Non Community)**
# 

# In[ ]:


features_list = ['School Income Estimate',
                 'Economic Need Index',
 'Percent ELL',
 'Percent Asian',
 'Percent Black',
 'Percent Hispanic',
 'Percent Black / Hispanic',
 'Percent White',
 'Student Attendance Rate',
 'Percent of Students Chronically Absent',
 'Rigorous Instruction %',
 'Collaborative Teachers %',
 'Supportive Environment %',
 'Effective School Leadership %',
 'Strong Family-Community Ties %',
 'Trust %']

tmp =school_data[features_list]


# In[ ]:


corrmat = tmp.corr()
f, ax = plt.subplots(figsize = (25, 5))
sns.heatmap(pd.DataFrame(corrmat.loc['School Income Estimate',:]).T, square=True, linewidths=.5, annot=True)
ax.xaxis.tick_top()
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.show()


# *From the heatmap we can see that school income is highly relevant to "Percent white".*
# 
# *Other variables are irrelelavent in determining the School Income Estimate*
