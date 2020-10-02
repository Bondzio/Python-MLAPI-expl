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


# import Library
import numpy as np
import pandas as pd # Data Extraction
#import matplotlib
import matplotlib.pyplot as plt # Data visualization
import seaborn as sns # Data visualization
#import plotly
import plotly.express as px # Data visualization
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# import Dataset
df=pd.read_csv("../input/google-play-store-apps/googleplaystore.csv")


# In[ ]:


#first 5 rows
df.head()


# # Explore the Data

# In[ ]:


# information of the Dataset
df.info()


# In[ ]:


# check null values in dataset
df.isnull().sum()


# In[ ]:


df.describe()


# In[ ]:


df.columns


# # understand the Columns
# 
# App                - Application name
# 
# Category           - Category the app belongs to
# 
# Rating             - Overall user rating of the app
# 
# Reviews            - Number of user reviews for the app
# 
# Size               - Size of the app
# 
# Installs           - Number of user downloads/installs for the app
# 
# Type               -  Paid or Free
# 
# Price              -  Price of the app
# 
# Content Rating     - Age group the app is targeted at - Children / Mature 21+ / Adult
# 
# Genres             - An app can belong to multiple genres (apart from its main category). 
# 
# Last Updated       - Last Updated Application date
# 
# Current Ver        - Current Version of the Application
# 
# Android Ver        - Supported Android Version of the Application

# In[ ]:


df["Content Rating"].value_counts()


# In[ ]:


df.drop(10472,axis=0,inplace=True) #drop the irrelevant row


#  # some questions with datasets
# 
# 1 How many percentage of free application?
# 
# 2 How many percentage lifestyle ,education or another  Category application?
# 
# 3 How many percentage of Art or another Genres of application?
# 
# 4 How many Free or paid application?
# 
# 5 How many Install the application 50,000+ or 10,000+ ?
# 
# 6 What is the Top 10 Category of  application?
# 
# 7 What is the Top 10 Genres of  application?
# 
# 8 How many application give rating 4 or 4.5 or 5?
# 
# 9 How many application supported version android 4.0 or different version?
# 
# 10 Every year How many application was updated?
# 
# 11 Every year How many application was updated or they are free or paid ?
# 
# 12 Display a line graph that display every year update How many application?
# 
# 13 Display a line graph that display which month update largest application?
# 
# 14 Which age group is highest target?

# # Different visualation Charts
# Piechart
# 
# Countplot
# 
# Barplot
# 
# Histogram
# 
# Boxplot
# 
# linegraph

# # Pie Chart

# ## 1 How many percentage of free or paid application?

# In[ ]:


data=df.Type.value_counts()
#plt.pie(df,x=data)


# ## 2 How many percentage lifestyle ,education or another  Category application?

# In[ ]:


# percentage of all category application
app_category=df.Category.value_counts()
fig=px.pie(app_category,values=app_category.values,names=app_category.index,title="App Category")
fig.show()


# ## 3 How many percentage of Art or another Genres of application?

# In[ ]:


app_genres=df.Genres.value_counts()
fig=px.pie(app_genres,values=app_genres.values,names=app_genres.index,title="App Genres")
fig.show()


# ## 4 How many Free or paid application?

# In[ ]:


sns.set_style("dark")


# In[ ]:


# count Type of application(free/paid)?
plt.figure(figsize=(12,7))
ax=sns.countplot(x=df.Type,data=df)

plt.title("Application Type",fontsize=20)

plt.xlabel("Type",fontsize=18)
plt.ylabel("Count",fontsize=18)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# ## 5 How many Install the application 50,000+ or 10,000+ ?

# In[ ]:


plt.figure(figsize=(20,10))

plt.title("No of Install the application",fontsize=24)
plt.xlabel("Installs",fontsize=20)
plt.ylabel("Count",fontsize=20)

ax=sns.countplot(x=df.Installs,data=df)
ax.set_xticklabels(rotation=80,labels=df.Installs)


for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

plt.show()


# ## 6 What is the Top 10 Genres of  application?

# In[ ]:


plt.figure(figsize=(20,10))
App_genres=df.Genres.value_counts().head(10)

plt.title("Top 10 Genres of Application",fontsize=20)
plt.xlabel("Genres",fontsize=18)
plt.ylabel("No.",fontsize=18)
ax=sns.barplot(App_genres.index,App_genres.values)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')
    

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()


# ## 7 What is the Top 10 Category of  application?

# In[ ]:


plt.figure(figsize=(22,10))
App_cats=df.Category.value_counts().head(10)

plt.title("Top 10 Category of Application",fontsize=20)
plt.xlabel("Category",fontsize=18)
plt.ylabel("No.",fontsize=18)
ax=sns.barplot(App_cats.index,App_cats.values)

for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')
    
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()


# # Histogram

# # 8 How many application give rating 4 or 4.5 or 5?

# In[ ]:


plt.figure(figsize=(20,10))

plt.title("Rating count",fontsize=24)
plt.xlabel("",fontsize=20)
plt.ylabel("Count",fontsize=20)
data=df.Rating.value_counts().hist()
print(data)


# In[ ]:


from datetime import datetime
df['Last Updated']=pd.to_datetime(df['Last Updated'])
df['Last Updated']=pd.to_datetime(df['Last Updated'],format='%B %d,%Y')


# In[ ]:


df['Year']=df["Last Updated"].dt.year


# In[ ]:


df['month']=df['Last Updated'].dt.month


# In[ ]:


df.head()


# # 10 Every year How many application was updated?

# In[ ]:


plt.figure(figsize=(20,10))

plt.title("No of App. Last Updated in the year",fontsize=24)
plt.xlabel("Year",fontsize=20)
plt.ylabel("Count",fontsize=20)

ax=sns.countplot(x=df.Year)


for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')

plt.xticks(fontsize=17)
plt.yticks(fontsize=17)

plt.legend()
plt.show()


# ## 11 Every year How many application was updated or they are free or paid ?

# In[ ]:


plt.figure(figsize=(20,10))

plt.title("No of Last Updated in the year",fontsize=24)
plt.xlabel("Year",fontsize=20)
plt.ylabel("Count",fontsize=20)

ax=sns.countplot(x=df.Year,data=df,hue=df.Type)


plt.xticks(fontsize=17)
plt.yticks(fontsize=17)

plt.legend()
plt.show()


# # line graph

# # 12 Display a line graph that display every year update How many application?

# In[ ]:


plt.figure(figsize=(10,7))

bins=[2010,2011,2012,2013,2014,2015,2016,2017,2018]
year_count=df.Year.value_counts().sort_index()
#print(year_count)
plt.plot(year_count.index,year_count.values,'go-')
plt.title("Application updated in each year",fontsize=19)
plt.xlabel("Year",fontsize=14)
plt.ylabel("No. of App",fontsize=14)

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()


# # 13 Display a line graph that display which month update largest application?

# In[ ]:


plt.figure(figsize=(10,7))
year_count=df.month.value_counts().sort_index()
sns.lineplot(x=year_count.index,y=year_count.values,data=df)

plt.title("Highest Application updated in Month ",fontsize=19)
plt.xlabel("Month",fontsize=14)
plt.ylabel("No. of App",fontsize=14)

plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.show()

# Here 2 means februaray 3 means march...12 means december.


# # 14 Which age group is highest target?

# In[ ]:


plt.figure(figsize=(20,10))

plt.title("Highest Age group is targets",fontsize=24)
plt.xlabel("Age group",fontsize=20)
plt.ylabel("Count",fontsize=20)

ax=sns.countplot(x=df['Content Rating'])


for p in ax.patches:
    ax.text(p.get_x() + p.get_width()/2., p.get_height(), '%d'% int(p.get_height()),
           fontsize=15,ha='center',va='bottom')

plt.xticks(fontsize=17)
plt.yticks(fontsize=17)

plt.legend()
plt.show()


# In[ ]:


data=df.Reviews.value_counts()
data

#sns.barplot(df,x=df.Reviews,y=df.Rating)

