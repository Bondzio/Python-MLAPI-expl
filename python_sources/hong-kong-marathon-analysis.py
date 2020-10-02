#!/usr/bin/env python
# coding: utf-8

# Just getting started with Kaggle and learning a lot of this for the first time...
# ------------------------------------------------------------------------

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import datetime as dt
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from matplotlib import pyplot as plt
import seaborn as sns

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


challenge=pd.read_csv('../input/challenge.csv')
run=pd.read_csv('../input/run1.csv')
#challenge.head()


# Some functions to return gender, class (age category) and a given time in minutes

# In[ ]:


#print(challenge['10km Time'])
def get_gender(a):
    return a[1]
def get_class(a):
    return a[2:]
def get_time(x):
    if x=='':
        return None
    elif x=='nan':
        return None
    elif x=='NaN':
        return None
    else:
        return (dt.datetime.strptime(str(x),"%H:%M:%S")-dt.datetime.strptime('00:00:00',"%H:%M:%S")).total_seconds()/60


# In[ ]:


challenge['gender']=challenge['Category'].apply(get_gender)
run['gender']=run['Category'].apply(get_gender)

challenge['agecat']=challenge['Category'].apply(get_class)
run['agecat']=run['Category'].apply(get_class)

challenge['OfficialTimeMinutes']=challenge['Official Time'].apply(get_time)
run['OfficialTimeMinutes']=run['Official Time'].apply(get_time)

challenge['NetTimeMinutes']=challenge['Net Time'].apply(get_time)
run['NetTimeMinutes']=run['Net Time'].apply(get_time)

challenge=challenge.dropna()
run=run.dropna()


# In[ ]:


full_data = pd.concat([challenge,run])

full_data['10kTimeMinutes']=full_data['10km Time'].apply(get_time)
full_data['HalfWayTimeMinutes']=full_data['Half Way Time'].apply(get_time)
full_data['30kTimeMinutes']=full_data['30km Time'].apply(get_time)

full_data['SecondHalfMinutes']=full_data['NetTimeMinutes'] - full_data['HalfWayTimeMinutes']
full_data['split']=full_data['SecondHalfMinutes'] - full_data['HalfWayTimeMinutes']
full_data['split_pc']=full_data['split'] / full_data['NetTimeMinutes'] *100

full_data['Q4Minutes']=full_data['NetTimeMinutes'] - full_data['30kTimeMinutes']
full_data['Q3Minutes']=full_data['30kTimeMinutes'] - full_data['HalfWayTimeMinutes']
full_data['Q2Minutes']=full_data['HalfWayTimeMinutes'] - full_data['10kTimeMinutes']
full_data['Q1Minutes']=full_data['10kTimeMinutes']

#full_data


# Split into two datasets for males/females
# ----------------------------------------
# 
# (in seconds)

# In[ ]:


df_males=full_data[(full_data.gender == 'M')]
df_females=full_data[(full_data.gender == 'F')]

#Also create datasets for different age categories
df_males_S=full_data[(full_data.agecat == 'S')]
df_males_M1=full_data[(full_data.agecat == 'M1')]
df_males_M2=full_data[(full_data.agecat == 'M2')]
#df_males.tail(5)
#print (df_females.count())


# In[ ]:


my5minRange = range(120,400,5)
my10minRange = range(120,400,10)
bins = np.linspace(120,360,70)

plt.hist (df_males.NetTimeMinutes, bins, alpha=0.75, label='Men')
plt.hist (df_females.NetTimeMinutes, bins, alpha=0.75, label='Women')
plt.legend(loc='upper right')


# Below is a graph showing the distribution of splits (a negative number is a negative split, meaning the second half of the marathon was run faster than the first). These are shown as a percentage of the total marathon time.
# 
# The distribution is split into two datasets, those for people who ran a sub 4 marathon and those who ran for longer than 4 hours.

# In[ ]:


#time_distribution.sort_values()
my5minRange = range(120,400,5)
my10minRange = range(120,400,10)
bins = np.linspace(-20, 30, 70)

plt.hist(full_data[(full_data.NetTimeMinutes >240)]['split_pc'], bins, alpha=0.75, label='Over 4hrs')
plt.hist(full_data[(full_data.NetTimeMinutes <= 240)]['split_pc'], bins, alpha=0.75, label='Sub 4hrs')
plt.legend(loc='upper right')

print ("Sub4 split mean: ", full_data[(full_data.NetTimeMinutes <=240)]['split_pc'].mean())
print ("Sub4 split SD: ", full_data[(full_data.NetTimeMinutes <=240)]['split_pc'].std())
print ("Over4 split mean: ", full_data[(full_data.NetTimeMinutes >240)]['split_pc'].mean())
print ("Over4 split SD: ", full_data[(full_data.NetTimeMinutes >240)]['split_pc'].std())


# This shows all runners' splits plotted on a graph as points. Using Numpy's polyfit() function, we can perform a least squares linear regression to this data and plot that function as a line (y=0.04x - 7.7). Not a huge gradient, but a gradient nonetheless, showing that runners' splits (as a percentage of their total marathon time) generally increase as their total marathon time goes up. An indication, perhaps, that running an even pace (or even negative split) goes hand in hand with a quick marathon time.

# In[ ]:


plt.scatter(full_data['NetTimeMinutes'],full_data['split_pc'])

# calc the trendline
z = np.polyfit(full_data['NetTimeMinutes'], full_data['split_pc'], 1)
p = np.poly1d(z)
plt.plot(full_data['NetTimeMinutes'],p(full_data['NetTimeMinutes']),"r--")

print (z)

