#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
import scipy as sp
import matplotlib.pyplot as plt


# In[ ]:


import os
os.chdir('../input/')


# In[ ]:


data=pd.read_csv('melb_data.csv')
data.head(5)


# In[ ]:


data.columns


# In[ ]:


data.describe(include=[np.number])


# In[ ]:


numerical_feats = data.dtypes[data.dtypes != "object"].index
print("Number of Numerical features: ", len(numerical_feats))

categorical_feats = data.dtypes[data.dtypes == "object"].index
print("Number of Categorical features: ", len(categorical_feats))


# In[ ]:


numerical_feats


# In[ ]:


categorical_feats


# In[ ]:


missing= data.isnull().sum() 
missing = missing[missing > 0]
missing.plot.bar() 


# In[ ]:


missing


# In[ ]:


sns.heatmap(data.isnull(),yticklabels=False,cbar=False)


# In[ ]:


#replace the Nan values with mean
data['Car'].mean()


# In[ ]:


data['Car']=data['Car'].replace(np.NaN,data['Car'].mean())


# In[ ]:


data['BuildingArea']=data['BuildingArea'].replace(np.NaN,data['BuildingArea'].mean())


# In[ ]:


data['YearBuilt']=data['YearBuilt'].replace(np.NaN,data['YearBuilt'].mean())


# In[ ]:


data.isnull().sum()


# In[ ]:


ca=data.iloc[ : , :-1].values
ca


# In[ ]:


data['CouncilArea']=data['CouncilArea'].replace(np.NaN,0)


# In[ ]:


data.isnull().sum() #no more missing value


# In[ ]:


sns.heatmap(data.isnull(),yticklabels=False,cbar=False)


# In[ ]:


data.shape


# In[ ]:


data.head()


# In[ ]:


names=['Suburb', 'Address', 'Rooms', 'Type', 'Price', 'Method', 'SellerG',
       'Date', 'Distance', 'Postcode', 'Bedroom2', 'Bathroom', 'Car',
       'Landsize', 'BuildingArea', 'YearBuilt', 'CouncilArea', 'Lattitude',
       'Longtitude', 'Regionname', 'Propertycount']
df=data[names]
correlations= df.corr()
fig=plt.figure(figsize=(15,12))
ax=fig.add_subplot(111)
cax=ax.matshow(correlations,vmin=-1,vmax=1)
fig.colorbar(cax)
ticks=np.arange(0,15,1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(names)
ax.set_yticklabels(names)
plt.show()


# In[ ]:


# 5 features:
#Price,Rooms,Distance,car,Bedroom2


# In[ ]:


data.dtypes


# Exploratory Analysis

# In[ ]:


pp= data[['Rooms','Distance','Postcode','Bedroom2','Price']] 
sns.set(style= 'ticks', palette= 'Set2')
sns.pairplot(data, vars= pp)
plt.show() 


# In[ ]:


sns.regplot(x='Bedroom2',y='Price',data=data)


# In[ ]:


#2 to 5 bedrooms have higher price.


# In[ ]:


sns.regplot(x='Rooms',y='Price',data=data)


# In[ ]:


#Price goes up with number of rooms upto 5 and then comes down as no of rooms increase.


# In[ ]:


sns.regplot(x='Distance',y='Price',data=data)


# In[ ]:


#houses closer have more price


# In[ ]:


sns.regplot(x='Postcode',y='Price',data=data)


# In[ ]:


pp2= data[['Bathroom','Car','Landsize','BuildingArea','YearBuilt','Price']] 
sns.set(style= 'ticks', palette= 'Paired')
sns.pairplot(data, vars= pp2)
plt.show() 


# In[ ]:


sns.stripplot(x='Bathroom',y='Price',data=data)


# In[ ]:


#Price goes up with number of rooms upto 4 and then comes down as no of rooms increase.
#2 to 4 bathrooms in a house have higher price


# In[ ]:


sns.stripplot(x='Car',y='Price',data=data)


# In[ ]:


#space for upto 4 cars have higher demand and price.


# In[ ]:


sns.stripplot(x='Landsize',y='Price',data=data)


# In[ ]:


#The price is high for small-sized plots


# In[ ]:


sns.stripplot(x='BuildingArea',y='Price',data=data)


# In[ ]:


#The price is high for a small-medium sized buildings.


# In[ ]:


sns.stripplot(x='YearBuilt',y='Price',data=data)


# In[ ]:


#Price is high for newer houses.


# In[ ]:


pp2= data[['Lattitude','Longtitude','Propertycount','Price']]
sns.set(style= 'ticks', palette= 'Dark2')
sns.pairplot(data, vars= pp2)
plt.show() 


# In[ ]:


sns.distplot(a= data['Lattitude'], kde= False)


# In[ ]:


sns.distplot(a= data['Longtitude'], kde= False)


# In[ ]:


sns.distplot(a= data['Propertycount'], kde= False)


# In[ ]:


sns.boxplot(x= 'Price', y= 'Regionname', data= data)


# In[ ]:


sns.boxplot(x= 'Price', y= 'CouncilArea', data= data)


# In[ ]:


sns.boxplot(x= 'Price', y= 'Type', data= data)


# In[ ]:


## Prices: depends on availability of number of rooms in a house.Price is highest when there are 5 rooms.
## Distance From CBD: if the distance from CBD is less, price will be high.
## House Price increases with increase in Building Area.
## Propertycount:The number of properties in each suburbs has only slight variation in prices.
## CouncilAreas such as "Port Philip","Stonnington","GlenEira","Bayside","Manningham", the prices are higher.
## Types:most of people prefer house(most of people liked cottage and villa type) and average price is also high compared to other two.
## Southern Metropolitian houses have higher price.


# In[ ]:




