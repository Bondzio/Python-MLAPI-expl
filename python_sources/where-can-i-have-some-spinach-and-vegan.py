#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
print(os.listdir("../input"))


# In[ ]:


df = pd.read_csv('../input/Datafiniti_Vegetarian_and_Vegan_Restaurants.csv')


# In[ ]:


df_unique_restaurant = df[['name', 'city', 'province', 'latitude', 'longitude', 'cuisines', 'categories']].drop_duplicates()


# In[ ]:


df_unique_restaurant['text'] = df_unique_restaurant['name'] + ',' + df_unique_restaurant['city'] + ', ' + df_unique_restaurant['province'] 
# +', ' + df_unique_restaurant['cuisines'] 


# In[ ]:


df_unique_restaurant['is_vegan_option'] = df_unique_restaurant.cuisines.str.lower().str.contains('vegan')|df_unique_restaurant.categories.str.lower().str.contains('vegan')


# In[ ]:


df_unique_restaurant['is_vegan_option'].value_counts()


# In[ ]:


df_unique_restaurant.head()


# In[ ]:


colorsIdx = {False: 'rgb(255,0,0)', True: 'rgb(0,0,255)'}
col_colours = df_unique_restaurant['is_vegan_option'].map(colorsIdx)


# In[ ]:


#https://plot.ly/python/scatter-plots-on-maps/
#https://stackoverflow.com/questions/49885837/python-plotly-assigning-scatterplot-colors-by-label
import plotly.graph_objects as go

import pandas as pd


fig = go.Figure(data=go.Scattergeo(
        lon = df_unique_restaurant['longitude'],
        lat = df_unique_restaurant['latitude'],
        text = df_unique_restaurant['text'],
        mode = 'markers',
        marker=dict(size=5, color=col_colours, opacity = 0.7)
        #marker_color = df_unique_restaurant['is_vegan_option'],
        ))

fig.update_layout(
        title = 'Restaurants with vegan options in Blue',
        geo_scope='usa',
    )
fig.show()


# In[ ]:


df.info()


# In[ ]:


df.isna().sum()


# In[ ]:


df.country.value_counts()


# In[ ]:


df.cuisines.value_counts()[:5]


# In[ ]:


df.head().T


# In[ ]:


df.id.nunique()


# In[ ]:


df.city.nunique()


# In[ ]:


df.city.value_counts()[:5]


# In[ ]:


#https://stackoverflow.com/questions/26970775/find-string-in-multiple-columns
df_spinach = df[df['menus.name'].str.lower().str.contains('spinach') | df['menus.description'].str.lower().str.contains('spinach')]


# In[ ]:


df_spinach.city.value_counts()


# In[ ]:


df_spinach.cuisines.unique()


# In[ ]:


dfspinach_vegan = df_spinach[df_spinach.cuisines.str.lower().str.contains('vegan')|df_spinach.categories.str.lower().str.contains('vegan')]


# In[ ]:


dfspinach_vegan.info()


# In[ ]:


dfspinach_vegan.city.value_counts()


# In[ ]:


#https://stackoverflow.com/questions/27842613/pandas-groupby-sort-within-groups
dfspinach_vegan.groupby('id')['id'].count().nlargest()


# In[ ]:


most_options = dfspinach_vegan.groupby('id')['id'].count().nlargest()


# In[ ]:


type(most_options)


# In[ ]:


most_options.sum()


# In[ ]:


most_options.index


# In[ ]:


most_options.index.values


# In[ ]:


df.id.isin(most_options.index.values)[:5]


# In[ ]:


#https://songhuiming.github.io/pages/2017/04/02/jupyter-and-pandas-display/
pd.set_option('display.max_colwidth', -1)
dfspinach_vegan[dfspinach_vegan.id.isin(most_options.index.values)][['city', 'name' , 'menus.name', 'menus.description','cuisines', 'id']]


# In[ ]:


groups = dfspinach_vegan[dfspinach_vegan.id.isin(most_options.index.values)].groupby('name')


# In[ ]:


groups.get_group("LuAnne's Wild Ginger All-Asian Vegan")[[ 'address','city', 'province', 'postalCode','phones', 'menus.sourceURLs', 'dateUpdated','cuisines', 'categories', 'imageURLs']].head(1).T


# In[ ]:


groups.get_group("LuAnne's Wild Ginger All-Asian Vegan").dropna(axis=1)[['menus.name', 'menus.description', 'menus.amountMax']]


# In[ ]:


#groups.get_group("LuAnne's Wild Ginger All-Asian Vegan").dropna(axis=1).T


# In[ ]:


from IPython.display import Image
from IPython.core.display import HTML 
Image(url= "http://my_site.com/my_picture.jpg")

