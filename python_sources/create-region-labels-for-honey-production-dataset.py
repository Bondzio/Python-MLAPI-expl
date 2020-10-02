#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


#Import cleaned data file
honey_data = pd.read_csv('../input/honeyproduction.csv')


# In[3]:


#View structure of the Data
honey_data.head()


# In[4]:


print("Number of records:", len(honey_data))


# # Beekeeping Regions
# 
# A list of the major beekeeping regions can be found here: http://www.beeculture.com/regional-honey-price-report-5/
# I have added an extra region (#8) here for Hawaii and Alaska.

# In[5]:


#Create lists of the beekeeping regions

Region_1 = ["MD","DE","PA","NJ","NY","CT","RI","MA","VT","NH","ME"]
Region_2 = ["TN","NC","SC","KY","WV","VA"]
Region_3 = ["AR","LA","MS","AL","GA","FL"]
Region_4 = ["MN","IA","MO","WI","IL","MI","IN","OH"]
Region_5 = ["MT","WY","ND","SD","NE","KS"]
Region_6 = ["AZ","UT","NM","CO","TX","OK"]
Region_7 = ["WA", "OR", "ID", "CA", "NV"]
Region_8 = ["AK","HI"]


# In[8]:


Region_Label = []
#Label each State by Region
for index in range(0,len(honey_data)):
    if honey_data.state[index] in Region_1:
        Region_Label.append("Region_1")
    elif honey_data.state[index] in Region_2:
        Region_Label.append("Region_2")
    elif honey_data.state[index] in Region_3:
        Region_Label.append("Region_3")
    elif honey_data.state[index] in Region_4:
        Region_Label.append("Region_4")
    elif honey_data.state[index] in Region_5:
        Region_Label.append("Region_5")
    elif honey_data.state[index] in Region_6:
        Region_Label.append("Region_6")
    elif honey_data.state[index] in Region_7:
        Region_Label.append("Region_7")
    else:
        Region_Label.append("Region_8")
        
    
    
        


# In[10]:


#Assign to column in dataframe
honey_data['Region'] = Region_Label


# In[11]:


#View updated dataframe
honey_data.head()


# In[12]:


#Save output to csv
honey_data.to_csv("honeyproductionWithRegionLabels.csv")


# In[ ]:




