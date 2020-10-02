#!/usr/bin/env python
# coding: utf-8

# Analysis of best restaurants in Bangalore at Basavanagudi Location 

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd # data processing , csv file I/O(e.g. pd.read_csv)
import numpy as np # linear Algebra
import matplotlib.pyplot as plt # to represent the data graphically
import seaborn as sn

import os
print(os.listdir("../input"))


# In[ ]:


df = pd.read_csv("../input/zomato.csv",low_memory=True) 
df.head()


# In[ ]:


#Printing column names and info
df.info() 
for col in df.columns: 
    print(col)


# In[ ]:


#Cleansing Data with columns
data_df = df.drop(['url', 'address','phone','listed_in(city)'], axis=1)
print('Columns after removing all url,address,phone, listed in city columns')
print(data_df.columns)
data_df


# In[ ]:


#Displaying data of restaurants located at Basavanagudi

data_df= data_df[data_df['location'] == 'Basavanagudi']
data_df


# In[ ]:


#Filling NaN value with 0
data_df=data_df.fillna(0)
data_df


# In[ ]:


#Replacing /5 with Null in Rate Column
data_df.rate = data_df.rate.astype('str')
data_df.rate = data_df.rate.apply(lambda x: x.replace('/5','').strip())
data_df


# In[ ]:


#Deleting row indexes from dataFrame 
indexNames = data_df[data_df['rate'] == 'NEW'].index
data_df.drop(indexNames , inplace=True)

indexNames = data_df[data_df['rate'] == '-'].index
data_df.drop(indexNames , inplace=True)

data_df


# In[ ]:


#Converting Rate Column datetype to float
data_df.rate = data_df.rate.astype('float')
data_df.info()


# In[ ]:


#Renaming column names just for convenience
data_df.rename(columns={'approx_cost(for two people)': 'average_cost'}, inplace=True)
data_df.rename(columns={'restaurant_type': 'restauranttype'}, inplace=True)
data_df.info()


# In[ ]:


#Ploting Rate Graph
plt.figure(figsize=(8,8))
sn.countplot(data_df['rate'])


# In[ ]:


plt.figure(figsize=(20, 10))
plt.subplot(1, 2, 1)
plt.scatter(data_df['rate'], data_df['average_cost'])
plt.title('Rate and Cost');


# In[ ]:


#Ploting Restaurant type and its data count
plt.figure(figsize=(20,5))
chart = sn.countplot( data=data_df,x='rest_type',palette='Set1')
chart.set_xticklabels(chart.get_xticklabels(), rotation=40)


# In[ ]:


#Displaying cuisines and its count
print(data_df['cuisines'].value_counts())


# In[ ]:


#Plotting Online Delivery Options
sn.countplot(x='online_order',data=data_df,palette='Set1')


# In[ ]:


#Finding  Average cost 
avgc=max(data_df.average_cost)
avgc


# In[ ]:


#Finding Maximum Value of Votes
data_df.loc[:,"votes"].max()


# In[ ]:


#Data of restaurants with rating greater than 4.5 and average cost lesser than 900
datacost=data_df[['name','rate','average_cost','cuisines','dish_liked']].groupby(['rate'], sort = True)
datacost=datacost.filter(lambda x: x.mean() >= 4.5)
datacost

datarate=datacost[['name','rate','average_cost','cuisines','dish_liked']].groupby(['rate'], sort = True)
datarate=datarate.filter(lambda x: x.mean() < 900)
datarate


# In[ ]:


#Restaurant data with higher votes ,considering 2230 half of the 4460 max value
datavotes=data_df[['name','votes']].groupby(['votes'], sort = True)
datavotes=datavotes.filter(lambda x: x.mean() >= 2230) 
datavotes.sort_values("votes", axis = 0, ascending = True, inplace = True, na_position ='last')
datavotes


# In[ ]:


#Merging data of  Average cost,higher rate (datarate) and votes(datavotes)
result = pd.merge(datarate, datavotes, on='name')
result


# In[ ]:


print('\t Displaying Restaurant Names and Dishes Liked ')
grouped = result.groupby("name")["dish_liked"]
grouped.apply(lambda x:x.value_counts())

