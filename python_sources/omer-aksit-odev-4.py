#!/usr/bin/env python
# coding: utf-8

# **AN INTRODUCTION TO PANDAS DATAFRAMES, MATPLOTLIB AND PANDAS TIME SERIES**
# 
# - building dataframes from scratch
# - visual exploratory data analysis
# - statistical exploratory data analysis
# - indexing pandas time series
# - resampling pandas time series

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


data=pd.read_csv("/kaggle/input/heart-disease-uci/heart.csv")


# In[ ]:


# building a pandas dataframe from scratch
countries=["spain","italy"]
capitals=["madrid","rome"]
populations=[10,12]
labels=["Country","Capital","Pop"]
all_lists=[countries,capitals,populations]
zipped=zip(labels,all_lists)
zipped_list=list(zipped)
dict1=dict(zipped_list)
df=pd.DataFrame(dict1)
df


# **Visual Exploratory Data Analysis**

# In[ ]:


data.head()


# In[ ]:


import warnings
dir(warnings)


# In[ ]:


#line plot
warnings.filterwarnings("ignore")
data[["trestbps","thalach"]].plot(kind='line',subplots=True)
plt.show()


# In[ ]:


#scatter plot
data.plot(kind="scatter",x="trestbps",y="thalach",color='b',alpha=0.5)
plt.title("Scatter plot: trestbps and thalach")
plt.show()


# Looks like trestbps and thalach are not so correlated. Let's check it out.

# In[ ]:


data[["trestbps","thalach"]].corr()     #Correlation is close to 0, which confirms our intuition from scatter plot.


# In[ ]:


#histogram
data.plot(kind="hist",y="trestbps",bins=50,range=(80,210))
plt.show()


# In[ ]:


data.plot(kind="hist",y="trestbps",bins=50,range=(80,210),cumulative=True)
plt.show()


# **Statistical exploratory data analysis**

# In[ ]:


data.trestbps.describe()


# **INDEXING PANDAS TIME SERIES**

# In[ ]:


data1=data.head(6)
data1


# In[ ]:


time_list=["1990-01-10","1990-02-10","1990-04-10","1990-01-01","1991-06-10","1991-06-15"]
time_object=pd.to_datetime(time_list)
data1["birth_date"]=time_object
data1=data1.set_index("birth_date")
data1


# In[ ]:


print(data1.loc["1990-01-10"])
print(data1.loc["1990-02-10":"1995-06-10"])


# **RESAMPLING PANDAS TIME SERIES**

# In[ ]:


data1


# In[ ]:


data1.resample("A").mean()


# In[ ]:


data1.resample("M").mean()


# In[ ]:


data1.resample("M").mean().interpolate()


# In[ ]:


data1.resample("M").first().interpolate()


# In[ ]:


data1.resample("M").last().interpolate()


# In[ ]:




