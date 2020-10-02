#!/usr/bin/env python
# coding: utf-8

# https://www.google.com/search?rlz=1C1GCEU_enIN873IN873&sxsrf=ALeKk01OmbAd84FW0OIx-2X1PNC4OixdCQ:1591362750744&q=global+warming+hd+image&tbm=isch&chips=q:global+warming+hd+image,g_1:1080p:kqo2vEXUCJ4%3D&usg=AI4_-kSPqsNyzHLXwRdoaglXXpBbGipGnQ&sa=X&ved=2ahUKEwi70N2b4OrpAhVwwTgGHfDED-wQgIoDKAB6BAgIEAQ&biw=1366&bih=657#imgrc=7XYdenjn1ltfsM
# 
# **GLOBAL WARMING**
# 
# *Glaciers are melting, sea levels are rising, cloud forests are dying, and wildlife is scrambling to keep pace. It has become clear that humans have caused most of the past century's warming by releasing heat-trapping gases as we power our modern lives. Called greenhouse gases, their levels are higher now than at any time in the last 800,000 years.*

# In[ ]:


from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# In[ ]:


# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
 for filename in filenames:
  print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import os
print(os.listdir("../input"))


# In[ ]:


df = pd.read_csv('/kaggle/input/daily-temperature-of-major-cities/city_temperature.csv', delimiter=',')


# In[ ]:


df.shape


# In[ ]:


df.columns


# In[ ]:


df.head(10)


# In[ ]:


df.isnull().sum()


# In[ ]:


df.State.value_counts()


# In[ ]:


b = df.Year.max()
a = df.Year.min()
print("The year range from "+ str(a) +" to" + str( b))


# In[ ]:


df.Month.value_counts()


# In[ ]:


def MonthConversion(m):
    if m == 1:
        return "Jan";
    if m ==2:
        return "Feb";
    if m == 3:
        return "Mar";
    if m == 4:
        return "Apr";
    if m == 5:
        return "May";
    if m == 6:
        return "Jun";
    if m == 7:
        return "Jul";
    if m == 8:
        return "Aug";
    if m == 9:
        return "Sep";
    if m == 10:
        return "Oct";
    if m == 11:
        return "Nov";
    if m == 12:
        return "Dec";
    
df["Month"] = df["Month"].apply(MonthConversion)


# In[ ]:


df["Month"].value_counts()


# In[ ]:


df


# In[ ]:


df.Region.value_counts()


# In[ ]:


Asia_df = df[df["Region"] == "Asia"]
Asia_df


# In[ ]:


Asia_df["Country"].value_counts()


# In[ ]:


df["Month"] = df["Month"].astype(str)
df["Day"] = df["Day"].astype(str)
df["Year"] = df["Year"].astype(str)
df["Date"] = df["Month"] + df["Day"] + df["Year"]


# In[ ]:


df.Date.value_counts()


# In[ ]:


df['Year'].value_counts().sort_values()


# In[ ]:


df.Year = df.Year.astype('int64')


# In[ ]:


df.drop(df[df['Year'] < 2000].index, inplace = True) 


# In[ ]:


df['Year'].value_counts().sort_values()


# In[ ]:


df["Year"] = df["Year"].astype(str)
df["Date"] = df["Month"] + df["Day"] + df["Year"]


# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


Asia_df.head()


# In[ ]:


Asia_df.hist()

plt.show()


# In[ ]:


plt.barh(Asia_df.Country, Asia_df.Year,align = "Center")

plt.show()

