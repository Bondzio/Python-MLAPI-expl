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


# # Task Details
# As of August 2019, this data set contains almost 50 thousand airbnb listings in NYC. The purpose of this task is to predict the price of NYC Airbnb rentals based on the data provided and any external dataset(s) with relevant information.
# 
# # Evaluation
# A solution with low root-mean-squared error (RMSE) based on cross-validation that can be reproduced and interpreted is ideal. Given the limited number of variables in this dataset, accurate predictions will be difficult.

# In[ ]:


df = pd.read_csv('/kaggle/input/new-york-city-airbnb-open-data/AB_NYC_2019.csv')
df.head()


# # Some quick stats...

# In[ ]:


df.describe()


# In[ ]:


df.describe(include=['object'])


# In[ ]:


df['neighbourhood_group'].value_counts().to_frame()


# In[ ]:


df['room_type'].value_counts().to_frame()


# In[ ]:


df_grp1 = df[['neighbourhood_group','price']].groupby(['neighbourhood_group'],as_index=False).mean()
df_grp1=df_grp1.rename(columns={'price':'average_price'})
df_grp1


# In[ ]:


df_grp2 = df[['room_type','price']].groupby(['room_type'],as_index=False).mean()
df_grp2=df_grp2.rename(columns={'price':'average_price'})
df_grp2


# In[ ]:


df_grp3 = df[['neighbourhood_group','room_type','price']].groupby(['neighbourhood_group','room_type'],as_index=False).mean()
df_grp3 = df_grp3.rename(columns={'price':'average_price'})
df_pivot = df_grp3.pivot(index='room_type',columns='neighbourhood_group')
df_pivot


# # Lets throw in some visuals

# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(15, 6))
sns.scatterplot(x=df.longitude,y=df.latitude,hue=df.neighbourhood_group)
plt.title('Airbnb distribtion across the 5 boroughs of NY')


# In[ ]:


import folium
from folium import plugins
# New York coordinates
lat = 40.7128
lon = -74.0060
ny_map = folium.Map(location=[lat,lon], zoom_start=12)   # create new york map
# instantiate a marker cluster for the airbnb locations in the dataframe
airbnb =  plugins.MarkerCluster().add_to(ny_map)

# randomly select a portion of the data for plotting on the map
df_smp = df.sample(frac=0.1, replace=False, random_state=1)
latitudes = list(df_smp.latitude)
longitudes = list(df_smp.longitude)
price = list(df_smp.price)
labels = ['$'+str(x)+' per night' for x in price]  # add pop-up price to each marker on the map
# loop through the data and add markers to feature group
i = 0
for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker(
        location=[lat, lng],
        icon=None,
        popup=label,
    ).add_to(airbnb)

ny_map


# In[ ]:


colors_list = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen']
explode_list = [0.05, 0.05, 0, 0.05, 0.05] # ratio for each feature with which to offset each wedge.

df_grp1['average_price'].plot(kind='pie',
                            figsize=(15, 6),
                            autopct='%1.1f%%', 
                            startangle=45,    
                            shadow=True,       
                            labels=None,         # turn off labels on pie chart
                            pctdistance=1.12,    # the ratio between the center of each pie slice and the start of the text generated by autopct 
                            colors=colors_list,  # add custom colors
                            explode=explode_list # 'explode' lowest 3 continents
                            )

# scale the title up by 12% to match pctdistance
plt.title('Average Airbnb Price in New York 5 Boroughs', y=1.12) 
plt.axis('equal') 
# add legend
plt.legend(labels=df_grp1['neighbourhood_group'], loc='upper left') 

plt.show()


# In[ ]:


ax = df_pivot.T.plot.bar(figsize=(12, 6))
plt.ylabel('Average price ($)')
plt.xlabel('Boroughs')
ax.set_xticklabels(df_grp1['neighbourhood_group'])


# In[ ]:


fig,ax = plt.subplots()
im = ax.pcolor(df_pivot, cmap='hot_r')

ylabels = df_pivot.columns.levels[1]
xlabels = df_pivot.index

ax.set_xticks(np.arange(df_pivot.shape[1]) + 0.5, minor=False)
ax.set_yticks(np.arange(df_pivot.shape[0]) + 0.5, minor=False)

ax.set_xticklabels(ylabels, minor=False)
ax.set_yticklabels(xlabels, minor=False)

#rotate label if too long
plt.xticks(rotation=45)

cbar = fig.colorbar(im)
cbar.ax.set_ylabel('average price')
plt.show()


# # Lets develop a model based on numeric features only

# In[ ]:


df_num = df.select_dtypes(exclude=['object'])
df_num.head()


# In[ ]:


nan = df_num.isnull()
for column in nan.columns.values.tolist():
    print(nan[column].value_counts())
    print('')


# only the column 'reviews_per_month' has NaNs. We deal it...

# In[ ]:


df_num.fillna(0, inplace=True)


# Now we train a model...

# In[ ]:


# remove features that don't contribute to price prediction
X = df_num.drop(['id','host_id','latitude','longitude','price'],axis=1)
y = df_num['price']


# I have a habit of testing multiple models...

# In[ ]:


from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.linear_model import LinearRegression 
from sklearn.linear_model import SGDRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split

lr = LinearRegression()
sgdr = SGDRegressor()
mlpreg = MLPRegressor(random_state=0, max_iter=100)
svrl = SVR(kernel='linear',C=0.01)
rfreg = RandomForestRegressor()
xgr = XGBRegressor()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
scaler = StandardScaler() 

pipeline = Pipeline(steps=[('scaler',scaler),('name',xgr)])
model = pipeline.fit(X_train,y_train)
score = model.score(X_test,y_test)
predict = model.predict(X_test)
mae = mean_absolute_error(y_test,predict)#, squared=False)
    
print('score: %1.3f, mae: %1.4f'%(score,mae))


# All the tested models performed poorly. Let's add some non-numeric features. 

# In[ ]:


# room_type and neigbourhood_group
rmtyp = pd.get_dummies(df['room_type'])
neigh_grp = pd.get_dummies(df['neighbourhood_group'])
neigh = pd.get_dummies(df['neighbourhood'])
df_new = pd.concat([df_num,rmtyp,neigh_grp,neigh], axis=1)
df_new.head()


# Now we re-train..

# In[ ]:


X = df_new.drop(['id','host_id','price','latitude','longitude'],axis=1)
y = df_new['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=9)

pipeline = Pipeline(steps=[('scaler',scaler),('name',xgr)])
model = rfreg.fit(X_train,y_train)
score = model.score(X_test,y_test)
predict = model.predict(X_test)
mae = mean_absolute_error(y_test,predict)
    
print('score: %1.3f, mae: %1.4f'%(score,mae))


# Not much improvement. Lets check for outliers in the price labels..
# 

# In[ ]:


plt.figure(figsize=(10,6), dpi=80)
sns.boxplot(df_new['price'])


# In[ ]:


# price outliers removal
q3 = df_new['price'].quantile(0.75)
q1 = df_new['price'].quantile(0.25)
price_ub = q3 + 1.5*(q3-q1)      # upper bound
price_lb = q1 - 1.5*(q3-q1)     # lower bound
df_new2 = df_new[df_new.price < price_ub]
print('removed outliers: ',df_new.shape[0]-df_new2.shape[0])


# In[ ]:


X = df_new2.drop(['id','host_id','price','latitude','longitude'],axis=1) 
y = df_new2['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=30)

pipeline = Pipeline(steps=[('scaler',scaler),('name',xgr)])
model = pipeline.fit(X_train,y_train)
score = model.score(X_test,y_test)
predict = model.predict(X_test)
mae = mean_absolute_error(y_test,predict)
    
print('score: %1.3f, mae: %1.4f'%(score,mae))


# Removal of outliers helped!

# Lets check cross validation scores

# In[ ]:


from sklearn.model_selection import cross_val_score

cv_score = cross_val_score(xgr, X, y, cv=4, scoring='neg_mean_absolute_error')
print('cross validation mae: ', -1*cv_score)


# **Not bad!**

# In[ ]:


#predict = model.predict(X)
prdct = pd.DataFrame(predict, columns=['predicted_price'])
df_submit = pd.concat([df_new2['id'],prdct], axis=1)
df_submit.to_csv('NY_airbnb_predicted_price.csv')


# 
