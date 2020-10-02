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


# In[ ]:


data = pd.read_csv("../input/climate_change.csv")


# In[ ]:


data.info() # We have nine float and two integer factors.


# In[ ]:


data.head()


# In[ ]:


data.columns


# In[ ]:


data.corr()


# In[ ]:


#correlation map
f,ax = plt.subplots(figsize = (15, 15))
sns.heatmap(data.corr(), annot = True, linewidths = .5, fmt = '.2f', ax = ax)
plt.show()


# ### Plotting Data 
# 
# To plot data I am going to use Matplotlib library with three basic plots which are line plot, scatter plot and histogram plot.
# 

# In[ ]:


# Line Plot

data["CFC-11"].plot(kind = 'line', color = "blue", label = "CFC-11", linewidth = 1, alpha = 0.5, linestyle = "-.")
data["CFC-12"].plot(color = 'red',label = "CFC-12", linewidth = 1, alpha = 0.5,linestyle = ":")
plt.xlabel("")
plt.ylabel("")
plt.legend(loc = 'upper left')
plt.grid()
plt.show()


# In[ ]:


# Scatter Plot

data.plot(kind = "scatter", x = 'CH4', y = 'CFC-12', alpha = 0.7)
plt.title("CFC-12 CH4 Scatter Plot")
plt.show()


# In[ ]:


# Histogram
data["CFC-12"].plot(kind = "hist",bins = 70, figsize = (15,10), color = 'r')
#data["CFC-11"].plot(kind = "hist",bins = 70, color = "black")
plt.show()


# In[ ]:


# Filtering Pandas with logical_and

data[np.logical_and(data['CFC-11'] < 200, data["CFC-12"]<500 )]


# In[ ]:


print(data["Aerosols"].value_counts(dropna = False))


# In[ ]:


data.describe()


# In[ ]:


average = sum(data.CO2) / len(data.CO2)
data["CO2-Level"] = ["High" if i > average else "Low" for i in data.CO2]
data.boxplot(column = "CFC-12", by = "CO2-Level")
plt.show()


# To be continued..

# In[ ]:




