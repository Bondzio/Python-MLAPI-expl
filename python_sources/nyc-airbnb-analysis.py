#!/usr/bin/env python
# coding: utf-8

# ![Title](https://thenypost.files.wordpress.com/2019/03/shutterstock_790067248.jpg?quality=90&strip=all&w=618&h=410&crop=1)
# # <div style="text-align: center" > A Statistical Analysis of airbnb in NYC</div>
# 
# I am supper excited to work with this airbnb dataset especially because this dataset is about NYC's airbnb hosts. I am going to know all the specs. This is going to be fun. Let's get started. 
# 

# # Goals:
# * Do an exploratory EDA of Airbnb. 
# * As a newyorker, I would like to know a bit more about the relation between Airbnb and NY neighbourhood.

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
        
df = pd.read_csv('../input/new-york-city-airbnb-open-data/AB_NYC_2019.csv')

# Any results you write to the current directory are saved as output.


# # About the Dataset
# 
# ## Overview

# In[ ]:


import pandas_profiling
df.profile_report()


# ## Missing Values

# In[ ]:


def missing_percentage(df):
    """This function takes a DataFrame(df) as input and returns two columns, total missing values and total missing values percentage"""
    ## the two following line may seem complicated but its actually very simple. 
    total = df.isnull().sum().sort_values(ascending = False)[df.isnull().sum().sort_values(ascending = False) != 0]
    percent = round(df.isnull().sum().sort_values(ascending = False)/len(df)*100,2)[round(df.isnull().sum().sort_values(ascending = False)/len(df)*100,2) != 0]
    return pd.concat([total, percent], axis=1, keys=['Total','Percent'])

missing_percentage(df)


# These are missing values in this dataset. We will work with them later. 

# ## Memory Usage

# In[ ]:


df.info(memory_usage = 'deep')


# As you can see this is a fairly small dataset and there is no need to worry about reducing memory. However, as I am trying to learn about about this topic, I will demonstrate some techniques to reduce memory usages. First let's write a function with calculate the memory usage of the dataframe and try it on our dataset. 

# In[ ]:


def mem_usage(pandas_obj):
    """This function takes in a DataFrame object as an input and returns a"""
    if isinstance(pandas_obj,pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else: # we assume if not a df it's a series
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2 # convert bytes to megabytes
    return "{:03.2f} MB".format(usage_mb)

mem_usage(df)


# First we will work with "object" data types. 
# 
# ## Object types

# In[ ]:


# This function takes only the 'object' type columns from the the dataFrames and the columns with tunique values 
def reduce_by_category_type(df):
    converted_obj = pd.DataFrame()
    for col in df.columns:
        num_unique_values = len(df[col].unique())
        num_total_values = len(df[col])
        if num_unique_values / num_total_values < 0.5 and df[col].dtype == 'object':
            converted_obj.loc[:,col] = df[col].astype('category')
        else:
            converted_obj.loc[:,col] = df[col]
    return converted_obj

df = reduce_by_category_type(df)


# In[ ]:


mem_usage(df)


# As you can see there is already a massive improvement in the dataset from 23.45 MB to 9.78 MB. Let's work with "int64" datatypes as well. 

# In[ ]:


df.info(memory_usage='deep')


# In[ ]:


df_int = df.select_dtypes(include = 'int64')
print (f" Before working with int types: {mem_usage(df_int)}")
converted_int = df.select_dtypes(include = 'int64').apply(pd.to_numeric,downcast='unsigned')
print (f" After working with the int types: {mem_usage(converted_int)}")
df.loc[:,df_int.columns] = converted_int
print (f" Total usage of the df after: {mem_usage(df)}")


# So, the total improvement of the dataset is from 23.45 MB to 8.01 MB. This is a huge improvement.

# # EDA
# 
# Let's have a preview of the dataset. 

# In[ ]:


df.head()


# In[ ]:


df['adjusted_price'] = df.price/df.minimum_nights


# In[ ]:


df.head()


# ## Top Hosts

# In[ ]:



import plotly.graph_objects as go

temp = df.host_id.value_counts().reset_index().head(20)
temp.columns = ['host_id', 'count']
temp = temp.merge(df[['host_id','host_name']], left_on = 'host_id',right_on = 'host_id', how = 'left', copy = False)
temp.drop_duplicates(inplace = True)

x = temp['host_name']
y = temp['count']

# Use the hovertext kw argument for hover text
fig = go.Figure(data=[go.Bar(x=x, 
                             y=y,
#                              hovertext=['27% market share', '24% market share', '19% market share'],
                            )])
# Customize aspect
fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
fig.update_layout(title_text='Top Airbnb hosts in NYC')
fig.layout.xaxis.title = 'Hosts'
fig.layout.yaxis.title = 'Host listings'
fig.show()


# Let's look at the top 5 hosts in NYC and see where they are hosting in NYC.

# In[ ]:


import plotly.express as px
## Setting the DataFrame
temp = df.host_id.value_counts().reset_index().head(5)
temp.columns = ['host_id', 'count']
temp = temp.merge(df[['host_id','host_name','price', 'latitude','longitude']], left_on = 'host_id',right_on = 'host_id', how = 'left', copy = False)

## Setting up the Visualization..
fig = px.scatter_mapbox(temp, 
                        lat="latitude", 
                        lon="longitude", 
                        color="host_name", 
                        size="price",
#                         color_continuous_scale=px.colors.cyclical.IceFire, 
                        size_max=30, 
                        opacity = .70,
                        zoom=11,
                       )
# "open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner" or 
# "stamen-watercolor" yeild maps composed of raster tiles from various public tile servers which do 
# not require signups or access tokens
# fig.update_layout(mapbox_style="carto-positron", 
#                  )
fig.layout.mapbox.style = 'carto-positron'
fig.update_layout(title_text = 'Top 5 hosts and their hosted Locations<br>(Click legend to toggle hosts)', height = 800)

fig.show()


# It looks like Manhattan is the preferable place for top hosts. Let's plot all the datapoints and see how that looks. 

# In[ ]:


df.head()


# # Overview of all datapoints by Borough

# In[ ]:


## Setting up the Visualization..
fig = px.scatter_mapbox(df, 
                        hover_data = ['price','minimum_nights','room_type'],
                        hover_name = 'neighbourhood',
                        lat="latitude", 
                        lon="longitude", 
                        color="neighbourhood_group", 
                        size="price",
#                         color_continuous_scale=px.colors.cyclical.IceFire, 
                        size_max=30, 
                        opacity = .70,
                        zoom=10,
                       )
# "open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner" or 
# "stamen-watercolor" yeild maps composed of raster tiles from various public tile servers which do 
# not require signups or access tokens
# fig.update_layout(mapbox_style="carto-positron", 
#                  )
fig.layout.mapbox.style = 'stamen-terrain'
fig.update_layout(title_text = 'Airbnb by Borough in NYC<br>(Click legend to toggle borough)', height = 800)
fig.show()


# In[ ]:


colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
labels = df.neighbourhood_group.value_counts().index
values = df.neighbourhood_group.value_counts().values

# Use `hole` to create a donut-like pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
fig.update_traces(marker=dict(colors = colors, line=dict(color='#000000', width=2)))

fig.show()


# It looks like Manhattan and Brooklyn counts for ~85% of all hostings.  

# # How about by Neighbourhood

# In[ ]:


## Setting up the Visualization..
fig = px.scatter_mapbox(df, 
                        lat="latitude", 
                        lon="longitude", 
                        color="neighbourhood", 
#                         size="price",
#                         color_continuous_scale=px.colors.cyclical.IceFire, 
                        size_max=30, 
                        opacity = .70,
                        zoom=10,
                       )
# "open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner" or 
# "stamen-watercolor" yeild maps composed of raster tiles from various public tile servers which do 
# not require signups or access tokens
# fig.update_layout(mapbox_style="carto-positron", 
#                  )
fig.layout.mapbox.style = 'carto-positron'
fig.update_layout(title_text = 'NYC Airbnb by Neighbourhood<br>(Click legend to toggle neighbourhood)', height = 800)

fig.show()


# # Room Types

# In[ ]:


colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
labels = df.room_type.value_counts().index
values = df.room_type.value_counts().values

# Use `hole` to create a donut-like pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
fig.update_traces(marker=dict(colors = colors, line=dict(color='#000000', width=2)))

fig.show()


# In[ ]:


from plotly.subplots import make_subplots

temp_bk = df[df.neighbourhood_group == 'Brooklyn']
temp_qn = df[df.neighbourhood_group == 'Queens']
temp_mn = df[df.neighbourhood_group == 'Manhattan']


labels = df.room_type.value_counts().index.to_list()

fig = make_subplots(1, 3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]],
                    subplot_titles=['Manhattan', 'Brooklyn', 'Queens'])
fig.add_trace(go.Pie(labels=labels, values=temp_mn.room_type.value_counts().reset_index().sort_values(by = 'index').room_type.tolist(), scalegroup='one',
                     name="Manhattan"), 1, 1)
fig.add_trace(go.Pie(labels=labels, values=temp_bk.room_type.value_counts().reset_index().sort_values(by = 'index').room_type.tolist(), scalegroup='one',
                     name="Brooklyn"), 1, 2)
fig.add_trace(go.Pie(labels=labels, values=temp_qn.room_type.value_counts().reset_index().sort_values(by = 'index').room_type.tolist(), scalegroup='one',
                     name="Brooklyn"), 1, 3)


fig.update_layout(title_text='Room Types in top 3 Boroughs')
fig.update_traces(marker=dict(colors = colors, line=dict(color='#000000', width=2)))
fig.show()

