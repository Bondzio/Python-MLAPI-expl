#!/usr/bin/env python
# coding: utf-8

# This is a walkthrough the Mortality Dataset.

# In[ ]:


import pandas as pd
import numpy as np
import datetime


import warnings
warnings.filterwarnings("ignore")
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="white", color_codes=True)




# Read data 
FILE="../input/mort.csv"
d=pd.read_csv(FILE,encoding = "ISO-8859-1")


# In[ ]:


d['Category'].value_counts()


# In[ ]:


t=d[d["Location"]=='United States'][['Location',"% Change in Mortality Rate, 1980-2014 (Min)",
                                   "% Change in Mortality Rate, 1980-2014 (Max)" ]]

t.sort_values(by=["% Change in Mortality Rate, 1980-2014 (Min)"],ascending=True)


# In[ ]:


t=d[['Location',"% Change in Mortality Rate, 1980-2014 (Min)",
                                   "% Change in Mortality Rate, 1980-2014 (Max)" ]]
t.sort_values(by=["% Change in Mortality Rate, 1980-2014 (Min)"],ascending=True).head(40)

