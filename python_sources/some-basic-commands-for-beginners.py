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

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


import numpy as np
import pandas as pd 
import glob, os.path
import matplotlib.pyplot as plt

#import libs.


# In[ ]:


soccer= pd.read_csv("../input/mls-salaries-2017.csv")
#read data


# In[ ]:


soccer.head()
#see what we have


# In[ ]:


soccer.info()


# In[ ]:


len(soccer.index)


# In[ ]:


#Avg. Salary
soccer["base_salary"].mean()


# In[ ]:


#max Salary
soccer["base_salary"].max()


# In[ ]:


#Infos of max guaranteed compensation 
soccer[soccer["guaranteed_compensation"] == soccer["guaranteed_compensation"].max()]


# In[ ]:


#Salaries and guaranteed compensation according to positions
soccer.groupby("position").mean()


# In[ ]:


# Number of players according to their positions
soccer["position"].value_counts()


# In[ ]:


#How many player have played each team
soccer["club"].value_counts()


# In[ ]:


#Players who end with 'son'

def re_find(last_name):
    if "son" in last_name.lower():
        return True
    return False

soccer[soccer["last_name"].apply(re_find)]


# In[ ]:


#Sort players from highest salary to lowest

def sortPlayers(salary):
    salaryList = []
    for i,j in salary.iteritems():
        salaryList.append(j)
    return salaryList
soccer["base_salary"] = sortPlayers(soccer["base_salary"])
soccer.sort_values(by = "base_salary",ascending = False,inplace=True)


# In[ ]:


soccer


# In[ ]:


import seaborn as sns
socc2 =  soccer.groupby("club").mean()


# In[ ]:


#Sort clubs according to base salary
def sortClubs(salary):
    salaryList = []
    for i,j in salary.iteritems():
        salaryList.append(j)
    return salaryList
socc2["base_salary"] = sortPlayers(socc2["base_salary"])
socc2.sort_values(by = "base_salary",ascending = False,inplace=True)
socc2.reset_index("club",inplace=True)


# In[ ]:


plt.figure(figsize=(15,10))
sns.barplot(x=socc2["club"], y=socc2["base_salary"])
plt.xticks(rotation= 90)
plt.xlabel('Clubs')
plt.ylabel('Salaries')
plt.title('Clubs & Salaries')


# In[ ]:


#Base on clubs
f,ax = plt.subplots(figsize=(5, 5))
sns.heatmap(socc2.corr(), annot=True, linewidths=0.5,linecolor="red", fmt= '.1f',ax=ax)
plt.show()


# In[ ]:


#Base on players.
f,ax = plt.subplots(figsize=(5, 5))
sns.heatmap(soccer.corr(), annot=True, linewidths=0.5,linecolor="red", fmt= '.1f',ax=ax)
plt.show()


# In[ ]:


# Both two figure gives information us that if salary increase,guaranteed compensation will too.


# In[ ]:


# Find null datas
null_data = soccer[soccer.isnull().any(axis=1)]
null_data


# In[ ]:


# Solution is combine last_name and first name to new column which is name
def fullname(x, y):
    if str(x) == "nan":
        return str(y)
    else:
        return str(x) + " " + str(y)

soccer['name'] = np.vectorize(fullname)(soccer['first_name'], soccer['last_name'])

#then drop last_name and first_name after created name column

soccer = soccer.drop(['last_name', 'first_name'], axis = 1)


# In[ ]:


soccer.head()


# In[ ]:


# Thanks

