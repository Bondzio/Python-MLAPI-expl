#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# **We can build data frames from csv .**

# In[ ]:


data = pd.read_csv('../input/2017.csv')


# In[ ]:


data.head()


# **We can build dataframe from dictionaries.**

# In[ ]:


dictionary = {"SCHOOL":["marmara","istanbul","yildiz"],
              "FACULTY":["engineering","economic sciences","education"],
              "DEPARTMENT":["industry","economy","math teaching"]}      
data_1 = pd.DataFrame(dictionary)


# In[ ]:


data_1.head()


# **We can build dataframe with zip() method.**

# In[ ]:


film = ["titanic","amelie","leon"]
imdb = ["9.7","8.6","7.5"]
label = ["film","imdb"]
column = [film,imdb]
zipp = list(zip(label,column))
dictt = dict(zipp)
data_2 = pd.DataFrame(dictt)


# In[ ]:


data_2.head()


# In[ ]:


#Add new columns
data_2["kind"] = ["dram","comedy","dram"]
data_2


# In[ ]:


#Broadcasting : Creates new column and assign a value to entire column
data_2["income"] = 0
data_2


# **VISUAL DATA ANALYSIS**

# In[ ]:


#Line plot
data1 = data.loc[:,["Happiness.Score","Whisker.high","Whisker.low"]] #create new data consisting of three columns of data
data1.plot() 
plt.show()


# In[ ]:


#Subplot
data1.plot(subplots = True)
plt.show()


# In[ ]:


#Scatter plot
data1.plot(kind = "scatter",x="Whisker.high",y = "Whisker.low")
plt.show()


# In[ ]:


#Histogram
data1.plot(kind = "hist",y = "Happiness.Score",bins = 20,range= (0,10),normed = True)


# In[ ]:


data1.plot(kind = "hist",y = "Happiness.Score",bins = 5,range= (0,10),normed = True,cumulative = True)


# In[ ]:


#Histogram subplot with non cumulative and cumulative
fig, axes = plt.subplots(nrows=2,ncols=1)
data1.plot(kind = "hist",y = "Whisker.high",bins = 20,range= (0,10),normed = True,ax = axes[0])
data1.plot(kind = "hist",y = "Whisker.high",bins = 20,range= (0,10),normed = True,ax = axes[1],cumulative = True)
plt.savefig('graph.png')
plt


# **INDEXING PANDAS TIME SERIES**

# In[ ]:


time = ["1996-02-26","1996-05-16"]  #list with each index string
print(type(time[0])) 

datetime = pd.to_datetime(time)   #now each index's type is Datetime
print(type(datetime))


# In[ ]:


# close warning
import warnings
warnings.filterwarnings("ignore")

data2 = data.head()
date = ["1996-02-26","1996-03-26","1996-04-26","1995-03-15","1995-03-16"]   #list consisting of strings
datetime = pd.to_datetime(date)
data2["date"] = datetime

data2= data2.set_index("date")  #now our index are dates
data2 


# In[ ]:


print(data2.loc["1996-04-26"])  #use date for indexing


# **RESAMPLING PANDAS TIME SERIES**
# 
# Resampling: statistical method over different time intervals.
# 
# Needs string to specify frequency like "M" = month or "A" = year.

# In[ ]:


data2.resample("A").mean() #average accounts by years


# In[ ]:


data2.resample("M").mean()  #average calculations per month


# In[ ]:


data2.resample("M").first().interpolate("linear") #fill gaps linearly based on first month


# In[ ]:


data2.resample("M").mean().interpolate("linear") #fill gaps with average values

