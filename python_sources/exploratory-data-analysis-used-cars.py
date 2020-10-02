#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns #visualization
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap #create map
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# ## 1. Load the data & quick look

# ### 1.1. Load Data

# In[ ]:


df = pd.read_csv('/kaggle/input/craigslist-carstrucks-data/craigslistVehiclesFull.csv')


# ### 1.2. Quick Look

# In[ ]:


df.shape


# In[ ]:


df.head()


# In[ ]:


df.tail()


# In[ ]:


df.info()


# In[ ]:


df.describe()


# ## 2. Missing values identification and handling
# ##### We have to fill the missing values based on the column's data type (numerical or categorical)

# In[ ]:


df.isnull().sum()


# ### 2.1. Find the missing values percentage. If more than 50%, then drop it.

# In[ ]:


more_than_50 = df.columns.where((df.isnull().sum()/len(df) * 100) >= 50).dropna()
df = df.drop(columns = more_than_50)
df.shape


# ### 2.2. group the columns based on the data type. We fill the nan of 'numerical' with the mean, and 'categorical' with mode

# In[ ]:


numerical = ['odometer','weather']
categorical = ['year','manufacturer','make','condition','cylinders',
               'fuel','title_status','transmission','drive','type','paint_color',
              'county_fips','county_name', 'state_fips','state_code']
unused = ['image_url']


# ##### fill the nan value with the data mean

# In[ ]:


for num in numerical:
    df[num] = df[num].fillna(df[num].mean())


# In[ ]:


for cat in categorical:
    df[cat] = df[cat].fillna(df[cat].mode().values[0])


# In[ ]:


df = df.drop(columns = unused)


# In[ ]:


df.isnull().sum()


# ### 2.3. Drop irrelevan values

# ##### Company History Benz Patent Motor Car: The first stationary gasoline engine developed by Carl Benz was a one-cylinder two-stroke unit which ran for the first time on 1885.

# In[ ]:


df = df.where(df['year']>1885)
df = df.dropna()


# In[ ]:


df.shape


# ##### county-level FIPS codes have five digits of which the first two are the FIPS code of the state to which the county belongs. Hence, we can drop the state FIPS.

# In[ ]:


df = df.drop(columns = 'state_fips')
df.shape


# ## 3. Visualization

# ### 3.1. Visualize the Pearson Correlation of the numerical data

# In[ ]:


#create correlation
corr = df.corr(method = 'pearson')

#convert correlation to numpy array
mask = np.array(corr)

#to mask the repetitive value for each pair
mask[np.tril_indices_from(mask)] = False
fig, ax = plt.subplots(figsize = (15,12))
fig.set_size_inches(15,15)
sns.heatmap(corr, mask = mask, vmax = 0.9, square = True, annot = True)


# ### 3.2. Visualize the numerical data with boxplot

# In[ ]:


numerical = ['lat', 'long','odometer','weather', 'price']
categorical = ['year','manufacturer','make','condition','cylinders',
               'fuel','title_status','transmission','drive','type','paint_color',
              'county_fips','county_name','state_code', 'state_name', 'city']


# In[ ]:


fig = plt.figure(figsize = (20,20))
axes = 320
for num in numerical:
    axes += 1
    fig.add_subplot(axes)
    sns.boxplot(data = df, x = num)
plt.show()


# ### 3.3. Visualize the categorical data

# #### 3.3.1. Visualize yearly production with countplot

# In[ ]:


plt.figure(figsize=(20,15))
ax = sns.countplot(x='year',data=df);
ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha="right",fontsize=6);


# #### 3.3.2. Visualize top 10 highest years of production

# In[ ]:


years_top10 = df['year'].value_counts().iloc[:10]
years = pd.DataFrame({'year': years_top10.index, 'count': years_top10.values})
plt.figure(figsize=(15,10))
ax = sns.barplot(x='year',y='count',data=years, order=years['year']);
ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha="right",fontsize=6);


# #### 3.3.3. Visualize the most data point on the map with Basemap

# In[ ]:


df_shuffled = df.sample(frac=1)
fig = plt.figure(figsize=(10, 10))
m = Basemap(projection='lcc', resolution=None,
            width=8E6, height=8E6, 
            lat_0=45, lon_0=-100,)
m.etopo(scale=0.5, alpha=0.5)
i = 0
for index, row in df_shuffled.iterrows():
    lat = row['lat']
    lon = row['long']
    xpt, ypt = m(lon, lat)
    m.plot(xpt,ypt,'.',markersize=0.2,c="red")
    # stopping criteria
    i = i + 1
    if (i == 10000): break


# #### 3.3.4. Visualize top 10 manufacturers

# In[ ]:


manufacturers_top10 = df['manufacturer'].value_counts().iloc[:10]
manufacturers = pd.DataFrame({'manufacturer': manufacturers_top10.index, 'count': manufacturers_top10.values})
plt.figure(figsize=(15,10))
ax = sns.barplot(y='manufacturer',x='count',data=manufacturers, order=manufacturers['manufacturer']);
ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha="right",fontsize=6);


# #### 3.3.5. Visualize transmission, fuel, condition, and cylinders with pyplot

# In[ ]:


pie = ['transmission','fuel','condition','cylinders']

fig = plt.figure(figsize = (15,15))
axes = 220
for p in pie:
    axes += 1
    fig.add_subplot(axes)
    plt.pie(df[p].value_counts(), labels=df[p].unique(),autopct='%1.1f%%', shadow=True, startangle=45);
    plt.title(p.upper())
plt.show()

