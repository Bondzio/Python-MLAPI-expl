#!/usr/bin/env python
# coding: utf-8

# **How much happy we are...**

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns  # visualization tool
from collections import Counter
get_ipython().run_line_magic('matplotlib', 'inline')
import os
print(os.listdir("../input"))

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))


# In[ ]:


data=pd.read_csv('../input/2017.csv')
datax=pd.read_csv('../input/2016.csv')
dataz=pd.read_csv('../input/2015.csv')


# In[ ]:


data.info()  #data of 2017


# In[ ]:


data.corr


# In[ ]:


#correlation
f,ax = plt.subplots(figsize=(10, 10))
sns.heatmap(data.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
plt.show()


# In[ ]:


#The happiest 10 countries in 2017
data.head(10)


# In[ ]:


#The unhappiest 10 countries in 2017
data.tail(10)


# In[ ]:


data.columns


# In[ ]:


recolumn = ['Country', 'HappinessRank', 'HappinessScore', 'WhiskerHigh',
       'WhiskerLow', 'EconomyGDPperCapita', 'Family',
       'HealthLifeExpectancy', 'Freedom', 'Generosity',
       'TrustGovernmentCorruption', 'DystopiaResidual']
data.columns = recolumn


# In[ ]:


data.columns


# In[ ]:


# Line Plot # relation between happiness and GPD
data.HappinessScore.plot(kind = 'line', color = 'g',label = 'HappinessScore',linewidth=5,alpha = 0.5, grid = True,linestyle = ':')
data.EconomyGDPperCapita.plot(color = 'r',label = 'GDPperCapita',linewidth=2, alpha = 0.9,grid = True,linestyle = '-.')
plt.legend(loc='upper right')     
plt.xlabel('x axis')              
plt.ylabel('y axis')
plt.title('Happiness&GPD')       
plt.show()


# In[ ]:


# Scatter Plot   # relation between happiness and GPD
# x = HapinessScore, y = EconomyGDPperCapita
data.plot(kind='scatter', x='HappinessScore', y='EconomyGDPperCapita',alpha = 1,color = 'red')
plt.xlabel('HappinessScore')              # label = name of label
plt.ylabel('EconomyGDPperCapita')
plt.title('Happiness-GPD Scatter Plot')            # title = title of plot


# In[ ]:


# Freedom of Countries Histogram
data.Freedom.plot(kind = 'hist',bins = 20,figsize = (10,10))
plt.show()


# In[ ]:


series = data['Family']        # data['Family'] = series
print(type(series))
data_frame = data[['Family']]  # data[['Family']] = data frame
print(type(data_frame))


# In[ ]:


x = data['HappinessScore']<3     # In 2017 there are only 2 countries that have lower HappinessScore value than 154 
data[x]


# **There are 7 countries which have higher happiness score value than 3.4 despite they have lower GDP value than 0.3**

# In[ ]:



data[np.logical_and(data['EconomyGDPperCapita']<0.3, data['HappinessScore']>3.4 )]


# In[ ]:


data.describe()


# In[ ]:


data.boxplot(column='TrustGovernmentCorruption')  #visualizing outliers for TrustGovernmentCorruption


# In[ ]:


# Melting the frame
data_new = data.head()    # I only take 5 rows into new data
melted = pd.melt(frame=data_new,id_vars = 'Country', value_vars= ['HappinessScore','EconomyGDPperCapita'])
melted


# In[ ]:


melted.pivot(index = 'Country', columns = 'variable',values='value')


# In[ ]:


# concatenating the frames
data1= data.head()
data2= data.tail()
conc_data_row = pd.concat([data1,data2],axis =0,ignore_index =True) # axis = 0 : adds dataframes in row
conc_data_row

data1= data['HappinessScore'].head()
data2= data['EconomyGDPperCapita'].head()
conc_data_col = pd.concat([data1,data2],axis =1) # axis = 0 : adds dataframes in row
conc_data_col


# In[ ]:


data.dtypes


# mean_happiness = sum(data.HappinessScore)/len(data.HappinessScore)
# data["HappinessScore_level"] = ["Happy" if i > mean_happy else "Unhappy" for i in data.HappinessScore]
# data.loc[:20,["HappinessScore_level","HappinessScore"]] 
# melted = pd.melt(frame=data,id_vars = 'Country', value_vars= ['HappinessScore_level'])
# melted

# In[ ]:


# Plotting all data 
data1 = data.loc[:,["HappinessScore","EconomyGDPperCapita"]]
data1.plot()
# it is confusing


# In[ ]:


# subplots
data1.plot(subplots = True)
plt.show()


# In[ ]:


data['Country'].unique()


# In[ ]:


recolumn = ['Country', 'HappinessRank', 'HappinessScore', 'WhiskerHigh',
       'WhiskerLow', 'EconomyGDPperCapita', 'Family',
       'HealthLifeExpectancy', 'Freedom', 'Generosity',
       'TrustGovernmentCorruption', 'DystopiaResidual']
data.columns = recolumn


# In[ ]:


#Bar Plot for Happiness 
country_list = list(data['Country'].unique())
happinessScore_ratio=[]
for i in country_list:
    x = data[data['Country']==i]
    happinessScore_rate = sum(x.HappinessScore)/len(x)
    happinessScore_ratio.append(happinessScore_rate)
veri = pd.DataFrame({'country_list': country_list,'happinessScore_ratio':happinessScore_ratio})
new_index = (veri['happinessScore_ratio'].sort_values(ascending=False)).index.values
sorted_veri = veri.reindex(new_index)

plt.figure(figsize=(25,10))
sns.barplot(x=sorted_veri['country_list'], y=sorted_veri['happinessScore_ratio'])
plt.xticks(rotation= 90)
plt.xlabel('Countries')
plt.ylabel('Happiness')
plt.title('Happiness of Countries in 2017')


# In[ ]:




