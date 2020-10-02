#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns  # visualization tool

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# Let's import our dataset

# In[ ]:


data = pd.read_csv("../input/2017.csv")


# If we run these (.info() and .columns()) commands, it's able to see what that dataset have characteristic properties as columns. (for .info() command, we also can see properties of these columns.) 

# In[ ]:


data.info()


# In[ ]:


data.columns


# In[ ]:


data.head(10) #shows first 10 rows


# In[ ]:


data.rename(columns={"Economy..GDP.per.Capita.":"GDP"}, inplace = True) 


# In[ ]:


data.rename(columns={"Happiness.Rank":"HappinessRank"}, inplace= True)


# **Pay attention!!** we changed names of 2 columns which are "Happiness.Rank" and "Economy..GDP.per.Capita." as "HappinessRank" and "GDP"

# In[ ]:


data.tail(10) #shows last 10 rows


# In[ ]:


data.corr() #creates a correlation figure with rates among the columns 


# In[ ]:


#Correlation map
f,ax = plt.subplots(figsize=(18, 18))
sns.heatmap(data.corr(), annot=True, linewidths=.5, fmt= '.01f',ax=ax)
plt.show()


# In[ ]:


#histogram
#bins = number of bar in figure
data.GDP.plot(kind="hist",bins=154,figsize=(15,15))
plt.show()


# In[ ]:


ax = plt.gca()

data.plot(kind='line', x = "HappinessRank",y = "GDP", color = "green", ax=ax,grid = True,figsize = (15,15))
data.plot(kind='line', x = "HappinessRank",y = "Freedom", color = 'red', ax=ax,grid = True)
data.plot(kind='line', x = "HappinessRank",y = "Trust..Government.Corruption.", color = 'b', ax=ax,grid = True)
plt.legend(loc = "upper left")
plt.show()


# In[ ]:


data.rename(columns={"Happiness.Score":"HappinessScore"}, inplace = True) 


# In[ ]:


#Let's classify countries whether they are livable or not. Our treshold is is average happiness score
#(Of course that is not the right way to determine countries that livable or not)  
threshold = sum(data.HappinessScore)/len(data.HappinessScore)
data["livable"] = [True if i > threshold else False for i in data.HappinessScore]
data.loc[::5,["Country","GDP","livable"]]


# If we're about to analyze statistical values down here;
# * **Count:** Number of entries
# * **Mean:** Average of entries 
# * **Std:** Standart deviation
# * **Min:** Minimum entry
# * **25%:** First quantile
# * **50%:** Second quantile or median of serie
# * **75%:** Third quantile
# * **Max:** Maximum entry
# 
# What is quantile?
# 
# * 1,4,5,6,8,9,11,12,13,14,15,16,17 
# * The median is the number that is in middle of the sequence. In this case it would be 11.
# 
# * The lower quartile is the median in between the smallest number and the median i.e. in between 1 and 11, which is 6.
# 
# * The upper quartile, you find the median between the median and the largest number i.e. between 11 and 17, which will be 14 according to the question above.

# In[ ]:


data.describe()


# In[ ]:


#Black line at top is max
#Blue line at top is 75%
#Blue (or middle) line is median (50%)
#Blue line at bottom is 25%
#Black line at bottom is min
data.boxplot(column="HappinessScore", by="livable")

