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


# **1.** Import the Data

# In[ ]:


#import Data with pandas library
df = pd.read_csv('../input/winemag-data-130k-v2.csv')


# **2.** Check Summary info of the data

# In[ ]:


#Information About Data
df.info()


# **3. ** Check the Name of the Columns

# In[ ]:


# names of Columns
df.columns


# In[ ]:


#Change the column name "Unnamed : 0" to "#Index and recheck the name of the column"
df=df.rename(columns = {'Unnamed: 0':'#Index'})
df.columns


# **4. **Correlation of the columns

# In[ ]:


df.corr()


# As we have only two non-string columns (First one is the index) there is only two column output for correlation

# **5.** Check the Correlation Heat Map

# In[ ]:


#Correlation Heat Map
sns.heatmap(df.corr(),vmax = 1, vmin = 0,annot = True)
plt.show()


# It seems Price and the Points have positive correleation

# **6. ** Check First 5 data

# In[ ]:


#First 5 Data
df.head(5)


# **7. **Line Plot the Points of the wines

# In[ ]:


#line plot of the points 
plt.figure(figsize=(20,10))
plt.plot(df.points, color = 'orange',label = 'Points', linewidth=0.3,alpha=0.7)
plt.xlabel('Index')
plt.ylabel('Point')
plt.title('Wine Point Line Graph')
plt.legend()
plt.show()


# **8.** Scatter Country to Price

# In[ ]:


#Scatter Plot of Countries Points
plt.figure(figsize=(30,10))
plt.scatter(df.country, df.points,color = 'g')
plt.xticks(rotation=90)
plt.xlabel ('Country')
plt.ylabel('Points')
plt.title("Countries Wine Points")
plt.show()


# **9. **Histogram Plot of Variety

# In[ ]:


# Frequency of Variety
plt.figure(figsize=(30,10))
plt.hist(df.country, bins = 30)
plt.xticks(rotation=90)
plt.xlabel = ('Country')
plt.ylabel('Frequency')
plt.title('Productivity of Countries')
plt.show()


# **10.** Some Filtering Operations

# In[ ]:


# Wines have point above 95
point_filter = df.points > 95
df[point_filter].head(5)


# In[ ]:


#Wine have price below 200
price_filter = df.price<200
df[price_filter].head(5)


# In[ ]:


# Point % Price Filter
df[np.logical_and(point_filter, price_filter)].head(5)


# In[ ]:




