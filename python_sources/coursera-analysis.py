#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns #visualization
import matplotlib.pyplot as plt #visualization
# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


df=pd.read_csv("/kaggle/input/coursera-course-dataset/coursea_data.csv")
df.head()


# In[ ]:


df.info()


# In[ ]:


df=df.drop(df.columns[0],axis=1) #Unnamed:0 column doesn't comes meaningful.


# In[ ]:


df.columns=df.columns.str.replace("_"," ")
df.columns=df.columns.str.title()


# In[ ]:


df.head() #Now its look better


# In[ ]:


len(df) #That shows us number of rows(instances)


# In[ ]:


df["Course Difficulty"].value_counts()


# In[ ]:


sns.countplot(x="Course Difficulty",data=df);


# In[ ]:


df.sort_values(by="Course Rating",ascending=False)


# In[ ]:


df.groupby("Course Organization")["Course Rating"].mean()


# In[ ]:


def course_number(org):
    "This function is returns you number of course of university you asked."
    number=len(df[df["Course Organization"]==org])
    return number


# In[ ]:


course_number("Copenhagen Business School")


# In[ ]:


df["Course Certificate Type"].value_counts()


# In[ ]:


sns.countplot(x="Course Certificate Type",data=df);


# In[ ]:


sns.boxplot(x="Course Certificate Type",y="Course Rating",data=df);


# In[ ]:


diffs=list(df["Course Difficulty"].unique())
diffsr=list(df["Course Difficulty"].value_counts().values)


# In[ ]:


plt.pie(x=diffsr,labels=diffs,autopct="%.1f",startangle=180,explode=[0.01,0.01,0.01,0.01]);
plt.show()


# In[ ]:




