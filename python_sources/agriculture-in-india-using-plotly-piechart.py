#!/usr/bin/env python
# coding: utf-8

# **This Kernel is not complete. **
# 
# I was amaze to observe how India's each state is involved in agriculture.
# which state and crop has highest and lowest yield, cultivation and production cost.
# 
# I tried experimenting with Plotly pie chart and result is so visible to get an insight from given data about each state and crop.
# 
# Hope this beginner visulation will help someone. If you like it please 'upvote' and share 'your valuable comment'.
# any suggestions for improvement is also welcome. Thanks

# **Load Libraries**

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np
import pandas as pd
# Seaborn and matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
# Plotly library
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
from plotly import tools
import colorlover as cl

# Others
#import warnings
#warnings.simplefilter(action='ignore', category=FutureWarning)
#init_notebook_mode(connected=True)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


df1 = pd.read_csv('../input/datafile (1).csv')
df1.head(5)


# In[ ]:


print(df1.isnull().sum())


# In[ ]:


df1.columns


# In[ ]:


temp1 = pd.crosstab(df1['State'], df1['Crop'])
temp1.plot(kind='bar', stacked=True, figsize = (16,8))

#fig, axes = plt.subplots(nrows=2, figsize=(6, 10))
#fig, ax = figsize = (6,10)

#temp1.plot(kind='bar', stacked=False, ax=axes[1], figsize = (16,20))
#for ax in axes:
    #ax.set_ylim(bottom=0)
    #plt.subplots_adjust(hspace = 0.9, top = 0.6)


# In[ ]:


df1.columns


# In[ ]:


#state vs crop Yield from each state
#state vs crops Cost of Cultivation (`/Hectare) A2+FL
#state vs crops Cost of Cultivation (`/Hectare) C2
#state vs crops Cost of Production (`/Quintal) C2
#state vs Yield (Quintal/ Hectare) 
import plotly.offline as py 
py.init_notebook_mode(connected=True) # this code, allow us to work with offline plotly version
import plotly.graph_objs as go # it's like "plt" of matplot
import plotly.tools as tls # It's useful to we get some tools of plotly
import warnings # This library will be used to ignore some warnings
from collections import Counter # To do counter of some features


def Plot_PieChart(str1, str_yield, str_cultivation_cost, str_production_cost, title):
    
    yield_crop = df1.groupby(str1)[str_yield].sum().to_frame().reset_index()
    cultivation = df1.groupby(str1)[str_cultivation_cost].sum().to_frame().reset_index()
    production = df1.groupby(str1)[str_production_cost].sum().to_frame().reset_index()

    colors = None
    trace0 = go.Pie(labels=yield_crop[str1], values=yield_crop[str_yield],
                    domain= {'x': [0, .30]}, marker=dict(colors=colors))
    trace1 = go.Pie(labels=cultivation[str1], values=cultivation[str_cultivation_cost],
                    domain= {'x': [0.35, .65]}, marker=dict(colors=colors))
    trace2 = go.Pie(labels=production[str1], values=production[str_production_cost],
                    domain= {'x': [0.70, 1]}, marker=dict(colors=colors))
    layout = dict(title= title, 
                  font=dict(family='Courier New, monospace', size=9, color='#7f7f7f'),
                  height=400, width=800,)
    fig = dict(data=[trace0, trace1, trace2], layout=layout)
    iplot(fig)
    #plotly.offline.iplot(fig)
    


# In[ ]:


str1 = 'Crop'
str_yield = 'Yield (Quintal/ Hectare) '
str_cultivation_cost = 'Cost of Cultivation (`/Hectare) C2'
str_production_cost = 'Cost of Production (`/Quintal) C2'
title = 'Cropwise Yield(Quintal/Hectare), Cultivation_Cost(Hectare) and Production_Cost(/Quintal) in India'
Plot_PieChart(str1, str_yield, str_cultivation_cost, str_production_cost, title)


# **Observation**
# 
# **Crop Yield in India**
# 
# 1) Sugarcane has a highest Yield in India (82.2%)
# 2) Moong has a lowest Yeild in India (0.437%)
# 
# **Cultivation Cost for crop**
# 
# 1) Higest for sugarcane
# 2) lowest for moong
# 3) average for 'paddy, maze, cotton, wheat' etc.
# 
# **Production cost for crop**
# 1) Sugarcane has very minimum production cost.
# 2) Moong has a highest production cost and thus least Yield among country.
# 

# In[ ]:


str1 = 'State'
str_yield = 'Yield (Quintal/ Hectare) '
str_cultivation_cost = 'Cost of Cultivation (`/Hectare) C2'
str_production_cost = 'Cost of Production (`/Quintal) C2'
title = 'Statewise Yield(Quintal/Hectare), Cultivation_Cost(Hectare) and Production_Cost(/Quintal) in India'
Plot_PieChart(str1, str_yield, str_cultivation_cost, str_production_cost, title)


# **Statewise Agriculture Observation in India**
# 
# 
# 1) Karnataka is hiest in yield
# 
# 2) Orissa is least in yield
# 
# 3) Andhrapradesh na dMaharastra spends maximum in cultivation as well in production cost for agriculture
# 
# 4) Bihar and west bengal spends very less in cultivation as well in production cost for agriculture
# 

# In[ ]:


df2 = pd.read_csv('../input/datafile (3).csv')
df2


# In[ ]:


df2.dtypes


# In[ ]:


df2.nunique()


# In[ ]:


df2['Crop_variety'] = df2['Crop'] + '(' + df2['Variety'] +')'
#df2['Crop_variety']


# In[ ]:


crop_var = df2[['Variety','Crop']].groupby('Crop').agg({'Variety' :lambda x: ",".join(x)})
crop_var


# In[ ]:


zone = df2[['Recommended Zone','Crop_variety']].groupby('Recommended Zone').agg({'Crop_variety' :lambda x: ",".join(x)})
zone


# In[ ]:


df_produce = pd.read_csv('../input/produce.csv')
df_produce.head(5)


# In[ ]:


df_produce.shape


# In[ ]:


print(df_produce.nunique())


# In[ ]:


total = df_produce.isnull().sum().sort_values(ascending = False)
percent = (df_produce.isnull().sum()/df_produce.isnull().count() * 100).sort_values(ascending=True)
print(pd.concat([total,percent], axis = 1, keys = ['Total', 'Percent']))


# we can drop columns '3-1993' to '3-2003'. as there are 99% data are missing.
# we can drop column '3-2014' as there are 85% data are missing in that column.

# In[ ]:


df_produce = df_produce.drop([' 3-1993',' 3-1994',' 3-1995',' 3-1996',' 3-1997',
          ' 3-1998',' 3-1999',' 3-2000',' 3-2001',' 3-2002',
         ' 3-1993',' 3-2014','Frequency'], axis = 1)

df_produce.shape


# In[ ]:


df_produce.columns


# In[ ]:


print(df_produce.nunique())


# In[ ]:


df_produce.Unit.unique()


# In[ ]:


df2.dtypes


# In[ ]:


cols1 = list(df_produce['Particulars'])
cols2 = [str(x)[23:] for x in cols1]
cols2


# In[ ]:


crop = df2['Crop             ']
# Create traces
trace0 = go.Scatter(
    x = crop,
    y = df['Production 2006-07'],
    mode = 'markers',
    name = 'markers'
)
trace1 = go.Scatter(
    x = crop,
    y = df['Production 2007-08'],
    mode = 'lines+markers',
    name = 'lines+markers'
)
trace2 = go.Scatter(
    x = crop,
    y = df['Production 2008-09'],
    mode = 'lines',
    name = 'lines'
)

data = [trace0, trace1, trace2]
#iplot(fig)
plotly.offline.iplot(fig)


# In[ ]:




