#!/usr/bin/env python
# coding: utf-8

# # Main Idea:
#  This visualisation has been created in order to point the do and dont's of a pubg match

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


data=pd.read_csv('/kaggle/input/pubg-finish-placement-prediction/train_V2.csv')


# In[ ]:


train=data.copy()


# In[ ]:


index=train[train['winPlacePerc'].isnull()==True].index


# ### winPlacePerc has one missing value..We will drop the missing value row as no column has any data in this case

# In[ ]:


train.drop(index,inplace=True)


# In[ ]:


train.info()


# ## **The data types of the columns are okay.But the data is not clean yet as there are some tideness issues.There are some columns which are not required in this analysis.We will drop them.**

# In[ ]:


train.drop(columns={'killPlace','killPoints','killStreaks','maxPlace','winPoints'},inplace=True)


# ### Now the data is clean and we proceed with the clean data

# In[ ]:


import matplotlib.pyplot as plt

import seaborn as sns
plt.style.use('fivethirtyeight')


# In[ ]:


f,size=plt.subplots(figsize=(15,10))
sns.heatmap(train.corr(),annot=True,fmt='.1f',ax=size)


# ## Looking at the above Heatmap we can colnclude that 'winPlacePerc' depends on:
# 
# 1.  **walkDistance**
# 1.  **weaponsAcquired,boosts**
# 1.  **damageDealt,heals,kills,longestKills**
# 1.  **DBNO's,headshotKills,rideDistance,assists**
# 1.  **Revives**
# 1.  **swimDistance,vehicalDestroys**

# ### Some additional information that we  get from here are:
# 1. **There is some correlation between walkDistance and weaponsAcquired**
# 1. **There is some correlation between boosts and walkadistance**
# 1. **There is a huge negative correlation between DBNOs and numgroups**

# In[ ]:


walk=train.copy()
walk=walk[walk['walkDistance']<walk['walkDistance'].quantile(0.99)]
bins_new=plt.hist(walk['walkDistance'],bins=10)[1]


# In[ ]:



walk['walkDistance'] = pd.cut(walk['walkDistance'], bins_new, labels=['0-400m','400-850m', '850-1320m', '1320-1750m','1750-2190m','2190-2650m','2650-3080m','3080-3500m','3500-4000m','4000+'])
plt.figure(figsize=(15,8))
sns.boxplot(x="walkDistance", y="winPlacePerc", data=walk)


# # Conclusion 1:
# 1. **Walking more somehow increases our chances of winning or rather getting a better rank**
# 1. **The suitable range of distance to be walked lies between 3500-4500m.This highly increases our chances of winning **
# 1. **This means that more is the amount of movement less would be the damage caused by our enemies**

# In[ ]:


groups=train.copy()
groups=groups[groups['winPlacePerc']<=1 & (groups['winPlacePerc']>0.8)]
plt.figure(figsize=(15,8))
sns.countplot(y=groups['matchType'],data=groups)


# # Conclusion 2:
# 1. For better performance and to get a good finishing rank squadd-fpp is the most preferred group type,followed by duo 
#    fpp and then squad.. Thus being in group is always advantageous while playing a pubg match 

# In[ ]:


comparison=train.copy()
comparison=comparison[comparison['winPlacePerc']<=1 & (comparison['winPlacePerc']>0.8)]
trace1=comparison['heals']<comparison['heals'].quantile(0.99)
trace2=comparison['boosts']<comparison['boosts'].quantile(0.99)

comparison=comparison[trace1 & trace2]
plt.figure(figsize=(15,8))
sns.distplot(comparison['heals'],hist=False,color='lime')
sns.distplot(comparison['boosts'],hist=False,color='blue')

plt.text(4,0.6,'heals',color='lime',fontsize = 17)
plt.text(4,0.55,'Boosts',color='blue',fontsize = 17)
plt.title('heals vs boosts')


# # Conclusion 3:
#   1. **A pubg player who secured a good rank in a pubg game took more number of boosts than number of heals.**
#   1.  **Thus for better performance in a pubg game try to rely on boosts rather than heals** 

# In[ ]:


vehicles=train.copy()
plt.figure(figsize=(15,8))
sns.pointplot(x='vehicleDestroys',y='winPlacePerc',data=vehicles)
plt.xlabel('Number of Vehicle Destroys')
plt.ylabel('Win Percentage')
plt.title('Vehicle Destroys/ Win Ratio')
plt.grid()
plt.show()


# # Conclusion 4:
# **1. Destroying a vehicle increases your chances of winning**

# In[ ]:


swim = train.copy()

swim['swimDistance'] = pd.cut(swim['swimDistance'], [-1, 0, 5, 20, 5286], labels=['0m','1-5m', '6-20m', '20m+'])

plt.figure(figsize=(15,8))
sns.boxplot(x="swimDistance", y="winPlacePerc", data=swim)



# # Conclusion 5:
# **1. Swimming for more distances increases your chances of winning.. This suggests the fact again that greater the movement greater would be the chances of you being damaged by your enemy**

# In[ ]:


killings=train.copy()
plt.figure(figsize=(15,8))
sns.pointplot(x='kills',y='winPlacePerc',data=killings)
plt.xlabel('kills')
plt.ylabel('Win Percentage')
plt.title('kills/ Win Ratio')
plt.grid()
plt.show()


# # Conclusion 6:
# 
# **This shows an obvious trend that more will be the number of killings more will be the chances of winning**
# 

# In[ ]:


newdata=train.copy()
newdata=newdata[newdata['winPlacePerc']==1]
plt.figure(figsize=(15,8))
sns.pointplot(x='kills',y='winPlacePerc',data=killings,color='#CC0000')
sns.pointplot(x='headshotKills',y='winPlacePerc',data=killings,color='blue')


# # Conclusion 7:
# **1. We see here in the case of winners headshotKills were more effective than normal kills. Thus preferring head shot kills over normal kills increases our chances of winning.**

# # FEATURE ENGINEERING

# In[ ]:


train['totalDistance'] = train['walkDistance']+train['rideDistance']+train['swimDistance']
train['boostsPerWalkDistance'] = train['boosts']/(train['walkDistance']+1)


# *** New columns of total distance and boosts per walk Distance are created**
# 

# In[ ]:


df=train.copy()
df=df[df['boostsPerWalkDistance']<df['boostsPerWalkDistance'].quantile(0.99)]
bi=plt.hist(df['boostsPerWalkDistance'])[1]
bi


# In[ ]:


df['boostsPerWalkDistance'] = pd.cut(df['boostsPerWalkDistance'], bi, labels=['0-0.0008m','0.0009-0.0016m', '0.0017-0.0025m', '0.00266-0.0033m','0.0034-0.0041m','0.0042-0.0049m','0.005-0.0058m','0.0059-0.0065m','0.0066-0.0074m','0.0074+'])
plt.figure(figsize=(15,8))
sns.boxplot(y="boostsPerWalkDistance", x="winPlacePerc", data=df)


# # Conclusion 8:
# 1. As we have seen earlier from the heatmap that there was some correlation between boosts and walk distance.From this graph we find an interesting trend.The boosts when taken with a short distance proves to be more effective and increases our chances of winning than the boosts taken after travelling long distances
# 1. The maximum effectiveness occurs when the boost perwalk distance is between 0.0017-0.0025m

# In[ ]:


train['weaponsAcquiredPerWalkDistance'] = train['weaponsAcquired']/(train['walkDistance']+1)


# In[ ]:


train.columns


# In[ ]:


weapons=train.copy()
weapons=weapons[weapons['weaponsAcquiredPerWalkDistance']<weapons['weaponsAcquiredPerWalkDistance'].quantile(0.99)]
bi_=plt.hist(weapons['weaponsAcquiredPerWalkDistance'])[1]
bi_


# In[ ]:


weapons['weaponsAcquiredPerWalkDistance'] = pd.cut(weapons['weaponsAcquiredPerWalkDistance'], bi_, labels=['0-0.015m','0.016-0.031m', '0.032-0.046m', '0.047-0.062m','0.063-0.077m','0.078-0.093m','0.094-0.108m','0.109-0.124m','0.125-0.139m','0.139+'])
plt.figure(figsize=(15,8))
sns.boxplot(y="weaponsAcquiredPerWalkDistance", x="winPlacePerc", data=weapons)


# # Conclusion 9:
# 1. Again we have seen from the heatmap that there was some correlation between weapons acquired and walk distance.From here we observe another intereseting trend that weapons need to be acquired within a very short distance of walking in order to increase the winning percentage
# 1. The weapons acquired per walk distance should be between the range less than 0.015m. Otherwise the chances of winning falls drastically

# In[ ]:


train['team'] = ['1' if i>50 else '2' if (i>25 & i<=50) else '4' for i in train['numGroups']]


# In[ ]:




