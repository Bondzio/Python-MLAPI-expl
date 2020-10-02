#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats


# In[ ]:


path = "../input/rainfall-in-india/rainfall in india 1901-2015.csv"
data = pd.read_csv(path)
data.head()


# In[ ]:


data.info()


# In[ ]:


data.describe()


# In[ ]:


# Getting to know which SUBDIVISION receives maximum rainfall in India annually
data[['SUBDIVISION', 'ANNUAL']].sort_values(by='ANNUAL', ascending = False).head(20)


# *Arunachal Pradesh is a clear winner here occupying 18/20 entries.*

# In[ ]:


sns.distplot(data['ANNUAL'], hist =True)


# *The right skewness in this plot can be explained by some eastern states which are receiving more than enough rain annually.*

# *This distribution is not a normal(gaussian) distribution.*

# # India

# In[ ]:


# Annual rainfall in subdivisions of India
plt.figure(figsize=(20,18))
ax = sns.boxplot(x="SUBDIVISION", y="ANNUAL", data=data, width=1, linewidth=2)
ax.set_xlabel('Subdivision',fontsize=30)
ax.set_ylabel('Annual Rainfall (in mm)',fontsize=30)
plt.title('Annual Rainfall in Subdivisions of India',fontsize=40)
ax.tick_params(axis='x', labelsize=20, rotation=90)
ax.tick_params(axis='y', labelsize=20, rotation=0)


# *Clearly we can see that Arunachal Pradesh has recorded maximum rainfall annually but its median is similar to Coastal Karnataka.*

# In[ ]:


# Average monthly rainfall in India
ax=data[['JAN', 'FEB', 'MAR', 'APR','MAY', 'JUN', 'AUG', 'SEP', 'OCT','NOV','DEC']].mean().plot.bar(width=0.5, linewidth=2, figsize=(16,10))
plt.xlabel('Month',fontsize=30)
plt.ylabel('Monthly Rainfall (in mm)', fontsize=30)
plt.title('Monthly Rainfall in Subdivisions of India', fontsize=25)
ax.tick_params(labelsize=10)
plt.grid()


# *As expected, average rainfall received is maximum in the month of August followed by June and then September.*

# In[ ]:


# Average monthly rainfall in India
ax = data[['Jan-Feb', 'Mar-May', 'Jun-Sep', 'Oct-Dec']].mean().plot.bar(width=0.5, linewidth=2, figsize=(16,10))
plt.xlabel('Quarter',fontsize=15)
plt.ylabel('Quarterly Rainfall (in mm)', fontsize=15)
plt.title('Quarterly Rainfall in India', fontsize=20)
ax.tick_params(labelsize=15)
plt.grid()


# In[ ]:


# Visualizing annual rainfall over the years(1901-2015) in India
ax = data.groupby("YEAR").mean()['ANNUAL'].plot(ylim=(1000,2000),color='r',marker='o',linestyle='-',linewidth=2,figsize=(12,10));
plt.xlabel('Year',fontsize=20)
plt.ylabel('Annual Rainfall (in mm)',fontsize=20)
plt.title('Annual Rainfall from Year 1901 to 2015 in India',fontsize=25)
ax.tick_params(labelsize=15)
plt.grid()


# *Quite average stats it seems to be. It is due to the rainfall received in some parts of India is extremely low or extremely high.*

# # Rajasthan

# **Now, let's analyze the rainfall data of Rajasthan(Because I am from Rajasthan!!).**

# In[ ]:


# Getting rainfall data for Rajasthan
Rajasthan = data.loc[((data['SUBDIVISION'] == 'WEST RAJASTHAN') | (data['SUBDIVISION'] == 'EAST RAJASTHAN'))]
Rajasthan.head()


# In[ ]:


# Average monthly rainfall in Rajasthan
ax = Rajasthan[['JAN', 'FEB', 'MAR', 'APR','MAY', 'JUN', 'AUG', 'SEP', 'OCT','NOV','DEC']].mean().plot.bar(width=0.5, linewidth=2, figsize=(16,10))
plt.xlabel('Month',fontsize=30)
plt.ylabel('Monthly Rainfall (in mm)', fontsize=30)
plt.title('Monthly Rainfall in Rajasthan', fontsize=25)
ax.tick_params(labelsize=10)
plt.grid()


# *August happens to be the most rainy month in Rajasthan.*

# In[ ]:


# Average monthly rainfall in Rajasthan
ax=Rajasthan[['Jan-Feb', 'Mar-May', 'Jun-Sep', 'Oct-Dec']].mean().plot.bar(width=0.5, linewidth=2, figsize=(16,10))
plt.xlabel('Quarter',fontsize=15)
plt.ylabel('Quarterly Rainfall (in mm)', fontsize=15)
plt.title('Quarterly Rainfall in Rajasthan', fontsize=20)
ax.tick_params(labelsize=15)
plt.grid()


# *Only Jun-Sep seems to have received maximum rainfall, that too is minimum as compared to other subdivisions.*

# In[ ]:


# Visualizing annual rainfall over the years(1901-2015) in Rajasthan
ax = Rajasthan.groupby("YEAR").mean()['ANNUAL'].plot(ylim=(50,1500),color='r',marker='o',linestyle='-',linewidth=2,figsize=(12,10));
plt.xlabel('Year',fontsize=20)
plt.ylabel('Rajasthan Annual Rainfall (in mm)',fontsize=20)
plt.title('Rajasthan Annual Rainfall from Year 1901 to 2015',fontsize=25)
ax.tick_params(labelsize=15)
plt.grid()


# *Look at the stats as the highest rainfall recorded is around 1500mm and the rest is below 800mm. Surely, it is receiving very much less rainfall than some of the eastern states' minimum recorded rainfall.*
# * Also, it seems that the highest rainfall recorded ever was in 1917 and the lowest in 1918(one year later).

# In[ ]:


print('Average annual rainfall received by Rajasthan = ',int(Rajasthan['ANNUAL'].mean()),'mm')
a = Rajasthan[Rajasthan['YEAR'] == 1917]
a


# # Arunachal Pradesh

# **Since, we know that Arunachal Pradesh has recorded maximum rainfall over the years, let's analyze it.**

# In[ ]:


# Getting rainfall data for Arunachal Pradesh
Arunachal = data.loc[(data['SUBDIVISION'] == 'ARUNACHAL PRADESH')]
Arunachal.head()


# In[ ]:


# Average monthly rainfall in Arunachal
ax = Arunachal[['JAN', 'FEB', 'MAR', 'APR','MAY', 'JUN', 'AUG', 'SEP', 'OCT','NOV','DEC']].mean().plot.bar(width=0.5, linewidth=2, figsize=(16,10))
plt.xlabel('Month',fontsize=30)
plt.ylabel('Monthly Rainfall (in mm)', fontsize=30)
plt.title('Monthly Rainfall in Arunachal', fontsize=25)
ax.tick_params(labelsize=10)
plt.grid()


# *All months happen to be rainy in Arunachal Pradesh. Someone is getting wet every month!!!!!.*

# In[ ]:


# Average monthly rainfall in Arunachal Pradesh
ax = Arunachal[['Jan-Feb', 'Mar-May', 'Jun-Sep', 'Oct-Dec']].mean().plot.bar(width=0.5, linewidth=2, figsize=(16,10))
plt.xlabel('Quarter',fontsize=15)
plt.ylabel('Quarterly Rainfall (in mm)', fontsize=15)
plt.title('Quarterly Rainfall in Arunachal', fontsize=20)
ax.tick_params(labelsize=15)
plt.grid()


# *Even Mar-May quarter in Arunachal is receiving more than 20% rainfall than the maximum one recorded in Rajasthan.*

# In[ ]:


# Visualizing annual rainfall over the years(1901-2015) in Arunachal Pradesh
ax = Arunachal.groupby("YEAR").mean()['ANNUAL'].plot(ylim=(1500,6500),color='r',marker='o',linestyle='-',linewidth=2,figsize=(12,10));
plt.xlabel('Year',fontsize=20)
plt.ylabel('Arunachal Annual Rainfall (in mm)',fontsize=20)
plt.title('Arunachal Annual Rainfall from Year 1901 to 2015',fontsize=25)
ax.tick_params(labelsize=15)
plt.grid()


# *Look at the drop in average rainfall over the years, but still it is holding the record of maximum rainfall.*

# In[ ]:


print('Average annual rainfall received by Arunachal Pradesh = ',int(Arunachal['ANNUAL'].mean()),'mm')
a = Arunachal[Arunachal['YEAR'] == 1948]
a


# **Let's find out which states and years have recorded the maximum and minimum rainfall in India.**

# In[ ]:


# Subdivisions receiving maximum and minimum rainfall
print(data.groupby('SUBDIVISION').mean()['ANNUAL'].sort_values(ascending=False).head(10))
print('\n')
print("--------------------------------------------")
print(data.groupby('SUBDIVISION').mean()['ANNUAL'].sort_values(ascending=False).tail(10))


# *As you can see that the subdivsions receiving maximum rainfall belongs to the southern and eastern parts of India whereas those receiving minimum rainfall belongs to the northern parts of India.*

# In[ ]:


# Years which recorded maximum and minimum rainfall
print(data.groupby('YEAR').mean()['ANNUAL'].sort_values(ascending=False).head(10))
print('\n')
print("--------------------------------------------")
print(data.groupby('YEAR').mean()['ANNUAL'].sort_values(ascending=False).tail(10))


# **Hope you liked this notebook and learned something new; if you did, then please vote, it would really mean a lot to me. THANK YOU!!!**
