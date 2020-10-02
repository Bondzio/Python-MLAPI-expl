#!/usr/bin/env python
# coding: utf-8

# # day-to-day Corona Virus cases Worldwide (Country based)

# In[ ]:


import pandas as pd
import plotly.express as px

df=pd.read_csv("../input/novel-corona-virus-2019-dataset/covid_19_data.csv",header=0)
df =df.groupby(['ObservationDate','Country/Region']).sum().reset_index()

fig=px.choropleth(df, locations="Country/Region",locationmode='country names', color='Confirmed',hover_name='Country/Region',animation_frame='ObservationDate',color_continuous_scale="Blues", range_color=(0.1,100000.))
fig.update_layout(title_text='Confirmed CUmulative Cases per Country--MA CHENEN',title_x=0.5)
fig.show()


# In[ ]:


df=pd.read_csv("../input/novel-corona-virus-2019-dataset/covid_19_data.csv",header=0)
df =df.groupby(['ObservationDate','Country/Region']).sum().reset_index()

df['daily_existing']=df['Confirmed']-df['Deaths'].diff()-df['Recovered'].diff()

fig=px.choropleth(df, locations="Country/Region",locationmode='country names', color='daily_existing',hover_name='Country/Region',animation_frame='ObservationDate',color_continuous_scale="Blues", range_color=(0.1,100000.))
fig.update_layout(title_text='Remaining Confirmed Cases per Country of each day--MA CHENEN',title_x=0.5)
fig.show()


# # hourly global map of earthquake epicentres
# 
# nepal earthquake on 2015/04/25
# 
# the link of the message resource
# http://news.163.com/special/niboer/

# In[ ]:


df=pd.read_csv('../input/april-25/query.csv',header=0)

df.index=pd.to_datetime(df['time'])
df['time']=df.index.strftime('%Y-%m-%d %H:00:00')
fig=px.scatter_geo(df,lat='latitude',lon='longitude',color='mag',animation_frame='time',color_continuous_scale='Solar', range_color=(5.,8.))
fig.update_layout(title_text='Earthquake on April 25,2015--MA CHENEN',title_x=0.5)
fig.show()


# In[ ]:




