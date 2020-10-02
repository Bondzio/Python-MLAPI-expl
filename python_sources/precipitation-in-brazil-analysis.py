#!/usr/bin/env python
# coding: utf-8

# # What is in this notebook?
# 
# [1. Peek into the Data.](#1)
# 
# 
# [2. States](#2)
# 
# 
# [3. RJ and PI over the years](#3)
# 
# 
# [4. Rain Over the Years](#4)
# 
# 
# [5. Monthly analysis](#5)
# 
# 
# [6. Change in rainfall](#6)

# In[ ]:


import numpy as np ## For Linear Algebra
import pandas as pd ## For Working with data
import plotly.express as px ## Visualization
import plotly.graph_objects as go ## Visualization
import plotly as py  ## Visulization
import matplotlib.pyplot as plt ## Visulization
from scipy import stats ## for stats.
import os


# In[ ]:


for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
path = os.path.join(dirname, filename)

df = pd.read_csv(path)


# <a class='archive' id='1'></a>
# 
# ## Peek into the Data.

# In[ ]:


df.head()


# In[ ]:


df.loc[:,'date'] = pd.to_datetime(df['date'])  ## Changing into datetime object helps in many ways, we'll see ahead.


# In[ ]:


## Now we can extract year and month from datetime object.
df['Year'] = df['date'].dt.year
df['Month'] = df['date'].dt.month


# <a class='archieve' id='2'></a>
# 
# ## STATES

# ### Total rain in all years and median rain on a rainy day, in different states

# In[ ]:


fig = py.subplots.make_subplots(1,2, subplot_titles=['Total Rain', 'Median rain on a Rainy day'])

temp = df.groupby(by=['state'])['precipitation'].sum().reset_index()
trace0 = go.Bar(x=temp['state'], y=temp['precipitation'])

temp = df.groupby(by=['state'])['precipitation'].median().reset_index()
trace1 = go.Bar(x=temp['state'], y=temp['precipitation'])

fig.append_trace(trace0,1,1)
fig.append_trace(trace1,1,2)

fig.show()


# In[ ]:


temp = df.groupby(by=['state', 'Year'])['precipitation'].sum().reset_index()
temp = temp.groupby(by='state')['precipitation'].median().reset_index()
px.bar(temp, 'state', 'precipitation', title='median Rain in an year', color='precipitation',
      color_continuous_scale=px.colors.sequential.Blugrn)


# #### Above graphs tell us that :
# - PA is the most rainy state.
# - It rains least in PI, on a rainy day.
# - Rj is the driest state, followed by PI and SE.
# - On a rainy day it rains less in PI than RJ but overall PI has recieved more rain than RJ. it means PI has longer rainy season than RJ or, more rainy days than RJ.

# <a class='archieve' id='3'></a>
# 
# ## RJ and PI over the years

# In[ ]:


fig = py.subplots.make_subplots(1,2, subplot_titles=['RJ', 'PI'])

rj = df[df['state']=='RJ']
temp = rj.groupby(by='Year')['precipitation'].sum().reset_index()
trace0 = go.Scatter(x=temp['Year'], y=temp['precipitation'])

pi = df[df['state']=='PI']
temp1 = pi.groupby(by='Year')['precipitation'].sum().reset_index()
trace1 = go.Scatter(x=temp1['Year'], y=temp1['precipitation'])

fig.append_trace(trace0,1,1)
fig.append_trace(trace1,1,2)

fig.show()


# ### In above graphs, we can see :
# - RJ recorded most rain in Year 2010.
# - Highest total precipitation in an year for RJ is still less then average yearly precipitation of most states.
# - PI recorded most rain in Year 2009.
# - In year 2001,2016 and 2017, PI recorded least rain.
# - for RJ it was Year 2017.
# - We don't have data for RJ before 2002. This can be the reason for it having lesser total rain recorded.
# - RJ recieved more rain then PI in year (2003, 2005, 2010, 2013, 2015 and  2016) that is almost half the years that it has data of.
# - looking at the above point we can think of reconsidering our analysis about driest state in brazil.

# <a class='archieve' id='4'></a>
# 
# ## Rain over the years

# In[ ]:


fig = py.subplots.make_subplots(1,2, subplot_titles=['Total Rain in Year', 'Median rain on a Rainy day of an Year'])

temp = df.groupby(by=['Year'])['precipitation'].sum().reset_index()
trace0 = go.Scatter(x=temp['Year'], y=temp['precipitation'])

temp = df.groupby(by=['Year'])['precipitation'].median().reset_index()
trace1 = go.Scatter(x=temp['Year'], y=temp['precipitation'])

fig.append_trace(trace0,1,1)
fig.append_trace(trace1,1,2)

fig.show()


# ### In above graphs We can see :
# - it rained least in 2001.
# - it rained most in 2009 and 2011.
# - Year 2000 has highest recorded rain on a rainy day but it has comparitively lesser total rain overall. That means there were not many rainy days or the year had shorter monsoon.
# - Year 2009 and 2011 are the years with most recorded rain, overall in an year.

# <a class='archieve' id='5'></a>
# 
# ## MONTH

# In[ ]:


fig = py.subplots.make_subplots(1,2, subplot_titles=['Total Rain', 'Median rain on a Rainy day'])

temp = df.groupby(by=['Month'])['precipitation'].sum().reset_index()
trace0 = go.Scatter(name= 'Total Rain', x=temp['Month'], y=temp['precipitation'])

temp = df.groupby(by=['Month'])['precipitation'].median().reset_index()
trace1 = go.Scatter(name='Median Rain', x=temp['Month'], y=temp['precipitation'])

fig.append_trace(trace0,1,1)
fig.append_trace(trace1,1,2)

fig.show()


# ### Above graph shows :
# - In Brazil, monsoon stays for four months ( Jan, feb, Mar, Apr ).
# - sep, oct and nov are the driest months in brazil.

# <a class='archieve' id='6'></a>
# 
# ## Change in rainfall.

# In[ ]:


df1 = df.groupby(by='Year')['precipitation'].sum().reset_index()

df1['change'] = 0
for i in range(1,df1.shape[0]):
    df1.loc[i,'change'] = (df1.loc[i,'precipitation']-df1.loc[i-1,'precipitation'])/df1.loc[i-1,'precipitation']

px.bar(df1, 'Year', 'change', color='change', title = 'Change in rainfall over the years :',
      color_continuous_scale=px.colors.sequential.Cividis)

