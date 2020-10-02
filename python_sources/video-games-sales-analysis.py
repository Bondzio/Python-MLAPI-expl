#!/usr/bin/env python
# coding: utf-8

# In[23]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[24]:


games = pd.read_csv("../input/vgsales.csv")
games.info()


# In[25]:


games.describe()


# In[26]:


games.corr()


# In[27]:


fig = plt.figure(figsize = (14,10))
sns.heatmap(games.corr(),linewidths = 5,annot = True)
plt.show()


# In[28]:


games[(games["NA_Sales"].max() == games["NA_Sales"])]#We found game that make maximum sales in NA


# In[29]:


games[games["EU_Sales"].max() == games["EU_Sales"]]#We found game that make maximum sales in EU


# In[30]:


games[games["JP_Sales"].max() == games["JP_Sales"]]#We found game that make maximum sales in JP


# In[31]:


games[games["Other_Sales"].max() == games["Other_Sales"]]#We found game that make maximum sales in other regions


# In[32]:


games.head()


# In[33]:


games.tail()


# In[34]:


games["Platform"].unique()#We found name of game platforms


# In[35]:


# Rank of game platforms according to global sales
array = ["NA_Sales","EU_Sales","JP_Sales","Other_Sales","Global_Sales"]
games.groupby("Platform").sum().sort_values("Global_Sales",ascending = False)[array]


# In[36]:


#We can draw the bar graph game platforms according to global sales
group = games.groupby("Platform").sum()["Global_Sales"]
fig,axis = plt.subplots(figsize = (18,8))
axis.bar(group.keys(),list(group))
axis.set_xlabel("Platforms")
axis.set_ylabel("Global Sales(million)")
plt.show()


# In[37]:


games["Publisher"].nunique()


# In[38]:


# Top 5 Publishers from global sales
group = games.groupby("Publisher")
group.sum().sort_values("Global_Sales",ascending = False)[["NA_Sales","EU_Sales","JP_Sales","Other_Sales","Global_Sales"]].head()


# In[39]:


# 5 Publishers that make the least sales global
group.sum().sort_values("Global_Sales",ascending = False)[["NA_Sales","EU_Sales","JP_Sales","Other_Sales","Global_Sales"]].tail()


# In[40]:


games["Genre"].unique()# We can see different game types


# In[41]:


# We can see game types sales region to region
group = games.groupby("Genre")
group.sum().sort_values("Global_Sales",ascending = False)[["NA_Sales","EU_Sales","JP_Sales","Other_Sales","Global_Sales"]]


# In[42]:


# We can draw the bar graph game types according to global sales
fig,axis = plt.subplots(figsize = (18,8))
group = group.sum()["Global_Sales"]
axis.bar(group.keys(),list(group))
axis.set_xlabel("Kinds of Games")
axis.set_ylabel("Total Global Sales(million)")
plt.show()

