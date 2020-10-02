#!/usr/bin/env python
# coding: utf-8

# # US Car Dataset

# ![](https://estaticos.efe.com/efecom/recursos2/imagen.aspx?lVW2oAh2vjO1Ph965nvplqxhRgK-P-2bMsMYQ4TncnkXVSTX-P-2bAoG0sxzXPZPAk5l-P-2fU5UQPtGbMWtd4o6jEass3B0Tw-P-3d-P-3d)

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
data = pd.read_csv('/kaggle/input/usa-cers-dataset/USA_cars_datasets.csv', index_col = 0)


# In[ ]:


data.info()


# In[ ]:


data.describe().transpose()


# In[ ]:


print(f'This dataset has {data.shape[0]} rows')
print(f'This dataset has {data.shape[1]} columns')


# In[ ]:


data.isnull().sum()


# In[ ]:


data.head()


# In[ ]:


print('Unique car brands: ',data['brand'].nunique())
print('Unique car models: ',data['model'].nunique())


# In[ ]:


plt.figure(figsize = (18,8))
sns.countplot(data['brand'])
plt.tight_layout()
plt.xticks(rotation = 90)
plt.xlabel('Car Brands', fontsize = 20)
plt.xticks(fontsize = 15)
plt.show()


# In[ ]:


plt.figure(figsize = (25,8))
sns.countplot(data['model'])
plt.tight_layout()
plt.xticks(rotation = 90)
plt.xlabel('Car Models', fontsize = 25)
plt.xticks(fontsize = 15)
plt.show()


# In[ ]:


print(f'Most auctioned off car models: \n{data["model"].value_counts().head()}')


# In[ ]:


plt.figure(figsize = (18,8))
data.groupby('brand')['price'].mean().sort_values(ascending = False).plot.bar()
plt.xticks(rotation = 90, fontsize = 20)
plt.ylabel('Mean Price')
plt.xlabel('Car Brands', fontsize = 25)
plt.tight_layout()
plt.show()


# In[ ]:


print(f'Most auctioned off car brands: \n{data["brand"].value_counts().head()}')


# In[ ]:


plt.figure(figsize = (20,8))
data.groupby('model')['price'].mean().sort_values(ascending = False).plot.bar()
plt.xticks(rotation = 90)
plt.ylabel('Mean Price')
plt.xlabel('Car Models', fontsize = 25)
plt.tight_layout()
plt.show()


# In[ ]:


data.head()


# In[ ]:


plt.figure(figsize = (25,7))
sns.countplot(data['color'])
plt.xticks(rotation = 90, fontsize = 13)
plt.xlabel('Color', fontsize = 20)
plt.title('Most used colors on cars')
plt.show()


# In[ ]:


print('Mean price for a car: ', round(data['price'].mean(),2))


# In[ ]:


plt.figure(figsize = (15,8))
sns.distplot(data['price'])
plt.xlabel('Price', fontsize = 20)
plt.show()


# In[ ]:


df = data.agg({'price': ['sum', 'min', 'max','median'], 'mileage': ['sum', 'min','max','median']})


# In[ ]:


df


# In[ ]:


print('Max Year: ', data['year'].max())
print('Min Year: ', data['year'].min())


# In[ ]:


print(f'Average price per year: \n{data.groupby("year")["price"].mean().sort_values(ascending = False)}')


# In[ ]:


plt.figure(figsize = (18,8))
data.groupby('year')['price'].mean().sort_values(ascending = False).plot.bar()
plt.xticks(rotation = 0)
plt.title('Average price of a car per year', fontsize = 25, pad = 10)
plt.xlabel('Years',fontsize = 25)
plt.show()


# In[ ]:


plt.figure(figsize = (18,8))
sns.scatterplot(data['year'], data['mileage'])
plt.xlabel('Years',fontsize = 25)
plt.ylabel('Mileage')
plt.show()


# In[ ]:


plt.figure(figsize = (20,8))
sns.boxplot(data['year'], data['price'])
plt.xlabel('Years',fontsize = 25)
plt.ylabel('Price')
plt.show()


# In[ ]:


print('Average mileage for an auction car: ', data['mileage'].mean())


# In[ ]:


print('Different car colors: ',data['color'].nunique())


# In[ ]:


print('States in this dataset: ',data['state'].nunique())


# In[ ]:


plt.figure(figsize = (18,8))
sns.countplot(sorted(data['state']))
plt.xticks(rotation = 90)
plt.xlabel('States', fontsize = 20)
plt.show()


# In[ ]:


plt.figure(figsize = (18,8))
data.groupby('state')['price'].mean().sort_values(ascending = False).plot.bar()
plt.title('Average price for a car per state', fontsize = 25, pad = 10)
plt.xlabel('States', fontsize = 15)
plt.tight_layout()
plt.show()


# In[ ]:


print(f'States that auction the most cars: \n{data.groupby("state")["brand"].count()}')


# In[ ]:


print('Unique countries in this dataset: ',data['country'].nunique())


# In[ ]:


data['country'].unique()


# In[ ]:


plt.figure(figsize = (15,8))
sns.countplot(data['country'])
plt.xlabel('Country', fontsize = 20)
plt.show()


# In[ ]:


plt.figure(figsize = (18,7))
sns.countplot(data['brand'], hue = data['country'])
plt.title('Cars auctioned of in the US and Canada', fontsize = 25, pad = 10)
plt.tight_layout()
plt.xticks(rotation = 90, fontsize = 15)
plt.xlabel('Brand', fontsize = 20)
plt.show()


# In[ ]:


print(f'The only cars being auctioned in canada: \n{data[data["country"] ==  " canada"]["brand"]}')


# In[ ]:


data['country'].value_counts()


# In[ ]:


print('Mean price for a car in the US: ',round(data[data['country'] == ' usa']['price'].mean(),2))
print('Mean price for a car in Canada: ',round(data[data['country'] == ' canada']['price'].mean(),2))


# In[ ]:


print(f'Total of clean and salvaged vehicles: \n{data["title_status"].value_counts()}')


# In[ ]:


print(f'Average price for a clean and salvaged vehicle: \n{data.groupby("title_status")["price"].mean()}')


# In[ ]:


plt.figure(figsize = (18,8))
sns.swarmplot(data['title_status'], data['price'])
plt.xlabel('Title Status', fontsize = 20)
plt.ylabel('Price', fontsize = 20)
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




