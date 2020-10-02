#!/usr/bin/env python
# coding: utf-8

# In this notebook, using **"covid_19_data.csv"**, i will compare Turkey and Italy's data in coronavirus outbreak.

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns  # visualization tool
import numpy as np

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In our dataset has many different country's data but we want to just look Turkey and Italy so we will filter using **Country/Region**.

# In[ ]:


data = pd.read_csv('/kaggle/input/novel-corona-virus-2019-dataset/covid_19_data.csv')
filteredDataTurkey = data.loc[data['Country/Region'] == "Turkey"]  # filter data for Turkey
filteredDataItaly = data.loc[data['Country/Region'] == "Italy"]  # filter data for Italy
filteredDataTurkey.info()
filteredDataItaly.info()


# In[ ]:


filteredDataTurkey.corr()  # Recovered and SNo has low correlation, Confirmed and Deaths has big correlation


# In[ ]:


# correlation map for Turkey
f, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(filteredDataTurkey.corr(), annot=True, linewidth=.5, fmt='.1f', ax=ax)
plt.show()


# We dont have any Province/State  values, lets drop it.

# In[ ]:


filteredDataTurkey.drop(["Province/State"], axis=1, inplace=True)
filteredDataItaly.drop(["Province/State"], axis=1, inplace=True)


# In[ ]:


filteredDataTurkey.columns


# In[ ]:


# Confirmed-Recovered Line Plot
# Lets look Confirmed and Recovered cases for Turkey and Italy
filteredDataTurkey.Confirmed.plot(kind='line', color='r', label='Confirmed-Turkey', linewidth=1, alpha=0.75, grid=True,linestyle=':')
filteredDataTurkey.Recovered.plot(color='r', label='Recovered-Turkey', linewidth=1, grid=True)
filteredDataItaly.Confirmed.plot(kind='line', color='b', label='Confirmed-Italy', linewidth=1, alpha=0.75, grid=True,linestyle=':')
filteredDataItaly.Recovered.plot(color='b', label='Recovered-Italy', linewidth=1, grid=True)
plt.legend(loc='upper right')  # legend = puts label into plot
plt.xlabel('Confirmed')  # label = name of label
plt.ylabel('Recovered')
plt.title('Confirmed and Recovered cases for Turkey and Italy')
plt.show()


# In[ ]:


plt.scatter(filteredDataTurkey.Confirmed, filteredDataTurkey.Recovered, c='g', linestyle=':', label='Turkey')
plt.scatter(filteredDataItaly.Confirmed, filteredDataItaly.Recovered, c='b', linestyle=':', label='Italy')
plt.xlabel('Confirmed')
plt.ylabel('Recovered')
plt.title('Confirmed and Recovered cases for Turkey and Italy')
plt.legend(loc='upper left')
plt.show()


# In[ ]:


# Histogram
filteredDataTurkey.Confirmed.plot(kind='hist', bins=100)
plt.show()
# plt.clf()


# In our data just show total death number but i want to show daily death number. Thats why im gonna decrease **Deaths**  from the previous day and gonna put a list that i call **dailyDeathNumberList**. After fill this list im gonna add to my **filterData** as a new column.
# 

# In[ ]:


i = 0
dailyDeathNumberListTurkey = [0] * filteredDataTurkey.shape[
    0]  # we create a list full with zeros with same dimension of our filterData
while i < filteredDataTurkey.shape[0]:  # filteredDataTurkey.shape[c,r]: will give column and row count
    if (i == 0):
        dailyDeathNumberListTurkey[i] = filteredDataTurkey.iloc[i, :].Deaths
    else:
        dailyDeathNumberListTurkey[i] = filteredDataTurkey.iloc[i, :].Deaths - filteredDataTurkey.iloc[i - 1, :].Deaths
    i += 1

# Same for Italy
j = 0
dailyDeathNumberListItaly = [0] * filteredDataItaly.shape[0]
while j < filteredDataItaly.shape[0]:
    if (j == 0):
        dailyDeathNumberListItaly[j] = filteredDataItaly.iloc[j, :].Deaths
    else:
        dailyDeathNumberListItaly[j] = filteredDataItaly.iloc[j, :].Deaths - filteredDataItaly.iloc[j - 1, :].Deaths
    j += 1


# In[ ]:


filteredDataTurkey["DailyDeathNumber"]=dailyDeathNumberListTurkey
filteredDataItaly["DailyDeathNumber"]=dailyDeathNumberListItaly
# After adding Daily Death Number, our filteredData;
filteredDataTurkey.head(10)


# Find the day's data with the highest number of deaths

# In[ ]:


print(filteredDataTurkey.loc[filteredDataTurkey['DailyDeathNumber'].idxmax()])


# In[ ]:


print(filteredDataItaly.loc[filteredDataItaly['DailyDeathNumber'].idxmax()])


# Now, plotting **Recovered** number of changes daily

# In[ ]:


plt.scatter(filteredDataTurkey.ObservationDate, filteredDataTurkey.Recovered, c='g', linestyle=':', label='Turkey')
plt.scatter(filteredDataItaly.ObservationDate, filteredDataItaly.Recovered, c='b', linestyle=':', label='Italy')
plt.xlabel('Confirmed')
plt.ylabel('Recovered')
plt.xticks([])  # used for hiding dates at x-axis
plt.legend(loc='upper left')
plt.show()

