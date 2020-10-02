#!/usr/bin/env python
# coding: utf-8

# # Reality price prediction
# 
# Here, we are given a house pricing dataset. In this notebook we will have a look at some basic explorations, also with plotly.
# 
# The dataset includes a lot of features, many of them specifying distances to keypoints like the next
# 
# * park
# * preschool
# * metro station
# * church
# * ...
# 
# We will use different kind of visualization techniques to get a first grasp of the data.
# 
# **If you like this notebook, please upvote it, thanks :)**

# In[ ]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from subprocess import check_output

get_ipython().run_line_magic('matplotlib', 'inline')
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.tools as tls

print(check_output(["ls", "../input"]).decode("utf8"))

macro = pd.read_csv('../input/macro.csv')
df = pd.read_csv("../input/train.csv")
df.head() 


# In[ ]:


print(list(df.columns))


# In[ ]:


macro.head()


# In[ ]:


df.info()


# # Distribution of target
# 
# Looking the price histogram, we can see a very long tail to the right, as there are only a few but very high priced objects.

# In[ ]:


plt.figure(figsize=(12,8))
sns.distplot(df['price_doc'])


# # Boxplot explorations
# 
# Here, we'll look at boxplot for different factors found in the data, let's see whether there is something interesting to find.

# In[ ]:


boxes = []
for cafe_count in df['cafe_count_500'].unique():
    y = df[df['cafe_count_500'] == cafe_count]['price_doc'].values
    b = go.Box(
        x=y,
        name = 'Cafe count {}'.format(cafe_count),
    )
    boxes.append(b)

py.iplot(boxes)


# In[ ]:


boxes = []
for floor in df['floor'].unique():
    y = df[df['floor'] == floor]['price_doc'].values
    b = go.Box(
        x=y,
        name = 'Floor {}'.format(floor),
    )
    boxes.append(b)

py.iplot(boxes)


# Well, thats surprising, there are apartments with no rooms. :)

# In[ ]:


boxes = []
for num_room in df['num_room'].unique():
    y = df[df['num_room'] == num_room]['price_doc'].values
    b = go.Box(
        x=y,
        name = '#Rooms {}'.format(num_room),
    )
    boxes.append(b)

py.iplot(boxes)


# In[ ]:


#boxes = []
#for build_year in df['build_year'].unique():
#    y = df[df['build_year'] == build_year]['price_doc'].values
#    b = go.Box(
#        x=y,
#        name = 'Buildyear {}'.format(build_year),
#    )
#    boxes.append(b)
#py.iplot(boxes)


# In[ ]:


# water_km


# # Jointplots
# 
# Lets now explore some joint plots of a few numeric predictors.
# 
# According to the data dictionary, _full_sq_ is the total area of the apartment and _life_sq_ is the living area in square meters. What is interesting here, that there seem to be a few objects that have higher area to live in than the full area of the apartment.

# In[ ]:


df = df[df['full_sq'] < 300]
df = df[df['life_sq'] < 300]
sns.jointplot("full_sq", "life_sq", data=df.sample(10000), kind="reg")


# In[ ]:


sns.jointplot("park_km", "preschool_km", data=df.sample(10000), kind="reg")


# In[ ]:


sns.jointplot("park_km", "full_sq", data=df.sample(10000), kind="reg")


# # Rolling window estimates
# 
# Now, let's have a look at different rolling window estimates of the reality prices by ordering in different dimensions. What we can see from the first plot, is that the reality prices are increasing over time. With different rolling windows sizes we are capturing more short term or longer term effects.

# In[ ]:


df['ts'] = pd.to_datetime(df['timestamp'])
df.ts.head()


# In[ ]:


df['rolling_price_300'] = df['price_doc'].rolling(window=300, center=False).mean()
df['rolling_price_1200'] = df['price_doc'].rolling(window=1200, center=False).mean()
ax = df.sort_values('ts').plot(x='ts', y='rolling_price_300', figsize=(12,8))
df.sort_values('ts').plot(x='ts', y='rolling_price_1200', color='r', ax=ax)
plt.ylabel('price')


# In[ ]:


df = df.sort_values('water_km')
df['rolling_price_300_water'] = df['price_doc'].rolling(window=300, center=False).mean()
ax = df.plot(x='water_km', y='rolling_price_300_water', figsize=(12,8))


# Price seems to depend a lot on the distance to the next park & the next big church.

# In[ ]:


df = df.sort_values('park_km')
df['rolling_price_300_park_km'] = df['price_doc'].rolling(window=300, center=False).mean()
ax = df.plot(x='park_km', y='rolling_price_300_park_km', figsize=(12,8))


# In[ ]:


df = df.sort_values('big_church_km')
df['rolling_price_300_big_church_km'] = df['price_doc'].rolling(window=300, center=False).mean()
ax = df.plot(x='big_church_km', y='rolling_price_300_big_church_km', figsize=(12,8))


# In[ ]:


df = df.sort_values('mosque_km')
df['rolling_price_300_mosque_km'] = df['price_doc'].rolling(window=300, center=False).mean()
ax = df.plot(x='mosque_km', y='rolling_price_300_mosque_km', figsize=(12,8))


# This looks like a good feature to filter out low priced apartments. The price for apartments rapidly drops with the distance to the next preschool.

# In[ ]:


df = df.sort_values('preschool_km')
df['rolling_price_300_preschool_km'] = df['price_doc'].rolling(window=300, center=False).mean()
ax = df.plot(x='preschool_km', y='rolling_price_300_preschool_km', figsize=(12,8))


# In[ ]:


df = df.sort_values('full_sq')
df['rolling_price_300_full_sq'] = df['price_doc'].rolling(window=300, center=False).mean()
ax = df.plot(x='full_sq', y='rolling_price_300_full_sq', figsize=(12,8))


# In[ ]:


df = df.sort_values('area_m')
df['rolling_price_300_area_m'] = df['price_doc'].rolling(window=300, center=False).mean()
ax = df.plot(x='area_m', y='rolling_price_300_area_m', figsize=(12,8))


# # Adding more dimensions
# 
# Let's encode more information into our visualizations by taking a few promising features from the previous plots.
# 
# There are three spatial dimensions, the fourth dimension is the color, which indicates the price of the object.

# In[ ]:


from sklearn.preprocessing import StandardScaler


# In[ ]:


#X = StandardScaler().fit_transform(df.fillna(0.0)[['area_m', 'full_sq', 'num_room']])
X = df.fillna(0.0)[['area_m', 'full_sq', 'num_room']].values
X.shape


# In[ ]:


df['log_price'] = np.log10(df['price_doc'].values)


# In[ ]:


trace1 = go.Scatter3d(
    x=X[:,0],
    y=X[:,1],
    z=X[:,2],
    mode='markers',
    marker=dict(
        sizemode='diameter',
        color = df['log_price'].values,
        colorscale = 'Portland',
        colorbar = dict(title = 'price_doc'),
        line=dict(color='rgb(255, 255, 255)'),
        opacity=0.5
    )
)

data=[trace1]
layout=dict(
    height=800,
    width=800,
    scene=go.Scene(
        xaxis=go.XAxis(title='area_m'),
        yaxis=go.YAxis(title='full_sq'),
        zaxis=go.ZAxis(title='num_room')
    ),
    title='Prices by three dimensions'
)
fig=dict(data=data, layout=layout)
py.iplot(fig, filename='3DBubble')


# In[ ]:


X = df.fillna(0.0)[['preschool_km', 'park_km', 'num_room']].values


# In[ ]:


trace1 = go.Scatter3d(
    x=X[:,0],
    y=X[:,1],
    z=X[:,2],
    mode='markers',
    marker=dict(
        sizemode='diameter',
        color = df['log_price'].values,
        colorscale = 'Portland',
        colorbar = dict(title = 'price_doc'),
        line=dict(color='rgb(255, 255, 255)'),
        opacity=0.5
    )
)

data=[trace1]
layout=dict(
    height=800,
    width=800,
    scene=go.Scene(
        xaxis=go.XAxis(title='preschool_km'),
        yaxis=go.YAxis(title='park_km'),
        zaxis=go.ZAxis(title='num_room')
    ),
    title='Prices by three dimensions'
)
fig=dict(data=data, layout=layout)
py.iplot(fig, filename='3DBubble')


# In[ ]:


X = df.fillna(0.0)[['industrial_km', 'full_sq', 'num_room']].values


# In[ ]:


trace1 = go.Scatter3d(
    x=X[:,0],
    y=X[:,1],
    z=X[:,2],
    mode='markers',
    marker=dict(
        sizemode='diameter',
        color = df['log_price'].values,
        colorscale = 'Portland',
        colorbar = dict(title = 'price_doc'),
        line=dict(color='rgb(255, 255, 255)'),
        opacity=0.5
    )
)

data=[trace1]
layout=dict(
    height=800,
    width=800,
    scene=go.Scene(
        xaxis=go.XAxis(title='industrial_km'),
        yaxis=go.YAxis(title='full_sq'),
        zaxis=go.ZAxis(title='num_room')
    ),
    title='Prices by three dimensions'
)
fig=dict(data=data, layout=layout)
py.iplot(fig, filename='3DBubble')


# In[ ]:


X = df.fillna(0.0)[['floor', 'full_sq', 'railroad_km']].values


# In[ ]:


trace1 = go.Scatter3d(
    x=X[:,0],
    y=X[:,1],
    z=X[:,2],
    mode='markers',
    marker=dict(
        sizemode='diameter',
        color = df['log_price'].values,
        colorscale = 'Portland',
        colorbar = dict(title = 'price_doc'),
        line=dict(color='rgb(255, 255, 255)'),
        opacity=0.5
    )
)

data=[trace1]
layout=dict(
    height=800,
    width=800,
    scene=go.Scene(
        xaxis=go.XAxis(title='floor'),
        yaxis=go.YAxis(title='full_sq'),
        zaxis=go.ZAxis(title='railroad_km')
    ),
    title='Prices by three dimensions'
)
fig=dict(data=data, layout=layout)
py.iplot(fig, filename='3DBubble')


# ### more to come soon :)

# In[ ]:




