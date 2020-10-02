#!/usr/bin/env python
# coding: utf-8

# <h1 align='center'>MyAnimeList dataset processing and visualisations</h1>

# In[ ]:


# CSV file importation
import pandas as pd

df_anime = pd.read_csv("../input/myanimelist/anime_cleaned.csv")
df_anime.head()
#pd.set_option('display.max_rows', df_anime.shape[0]+1)


# In[ ]:


df_anime.shape


# Shape of the csv file : 33 columns and 6668 rows
# 
# Choice of only keeping the 8 following columns :

# In[ ]:


# filtering columns

df_anime = df_anime.filter(items=['title', 'type', 'source', 'episodes', 'duration', 'score', 'scored_by', 'aired_from_year'])
df_anime.head()


# In[ ]:


import plotly.express as px

tips = px.data.tips()
fig = px.histogram(df_anime, y="type", orientation="h").update_xaxes(categoryorder='total ascending')
fig.show()


# In[ ]:


fig = px.histogram(df_anime, x="source")
fig.show()


# In[ ]:


fig = px.histogram(df_anime, x="type", y="title", color="source")
fig.show()


# In[ ]:


fig = px.histogram(df_anime, x="aired_from_year")
fig.show()


# In[ ]:


px.scatter(df_anime,x='episodes',size= 'episodes', color='episodes')


# In[ ]:


fig = px.histogram(df_anime, x="duration")
fig.show()


# *The values of this duration column need to be homogenized. The following function is meant to give it a '00:00:00' format :*

# In[ ]:


# modifications on the duration column
import re 

def clean_duration(duration): 
    if re.search(r'[0-9]+(?= hr)', duration):
        hr = re.search(r'[0-9]+(?= hr)', duration).group(0)
        if len(hr)!=2:
            hr = '0'+hr
    else :
        hr = '00'
    if re.search(r'[0-9]+(?= min)', duration):
        mn = re.search(r'[0-9]+(?= min)', duration).group(0)
        if len(mn)!=2:
            mn = '0'+mn
    else :
        mn = '00'
    if re.search(r'[0-9]+(?= sec)', duration):
        sec = re.search(r'[0-9]+(?= sec)', duration).group(0)
        if len(sec)!=2:
            sec = '0'+sec
    else :
        sec = '00'
        
    if len(hr+':'+mn+':'+sec)==8:
        return hr+':'+mn+':'+sec
    else : 
        cp++1
        return duration
         
df_anime['duration'] = df_anime['duration'].apply(clean_duration)
df_anime


# In[ ]:


sorted_duration = df_anime.sort_values('duration', ascending=True)
fig = px.histogram(sorted_duration, x="duration")
fig.show()


# In[ ]:


fig = px.histogram(df_anime, x="score")
fig.show()


# In[ ]:


fig = px.histogram(df_anime, x="scored_by")
fig.show()


# *1st peak = scored_by 0 to 5000*

# In[ ]:


px.scatter(df_anime,x='scored_by',color = 'score', size = 'score')

