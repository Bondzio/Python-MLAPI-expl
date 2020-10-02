#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict
from sklearn import preprocessing
pd.set_option("display.max_columns",100)


import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.tools as tls


# In[2]:


df = pd.read_csv('../input/movie_metadata.csv')
df.head()


# # Types of movies

# In[5]:


genres = df.genres.map(lambda x: x.split("|"))
counts = defaultdict(int)
for l in genres:
    for l2 in l:
        counts[l2] += 1


# In[5]:


data=[go.Bar(x=list(counts.keys()), y=list(counts.values()))]
layout=dict(height=800, width=800, title='Distribution of training labels')
fig=dict(data=data, layout=layout)
py.iplot(data, filename='train-label-dist')


# # Wordcloud about subject

# In[13]:


plot_keywords = df.plot_keywords.map(lambda x: str(x).split("|"))
empty_array = []
for i in plot_keywords:
    empty_array = np.append(empty_array, i)


# In[16]:


from wordcloud import WordCloud
cloud = WordCloud(width=1440, height=1080, relative_scaling=0.5, stopwords=['title']).generate(" ".join(empty_array))
plt.figure(figsize=(20, 15))
plt.imshow(cloud)
plt.axis('off')
plt.show()


# # Budget, Gross and Popularity of the movie

# In[3]:


min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(df[['movie_facebook_likes']].values)
area = np.pi * (15 * x_scaled)**2
plt.scatter(x=df.budget, y= df.gross, s=area, c=df.imdb_score)
plt.xlim((0, 1e9))
plt.title('Gross v. Budget expensed, size related to movie ranking')
plt.xlabel('Budget')
plt.ylabel('Gross')
plt.colorbar()


# In[5]:


area = np.pi * (6 * x_scaled)**2
layout = go.Layout(
    title='Gross v. Budget expensed, size related to movie ranking',
    xaxis=dict(
        title='Budget',
        gridcolor='rgb(255, 255, 255)',
        range=[0, 4e8],
        zerolinewidth=1,
        ticklen=5,
        gridwidth=2,
    ),
    yaxis=dict(
        title='Gross',
        gridcolor='rgb(255, 255, 255)',
        zerolinewidth=1,
        ticklen=5,
        gridwidth=2,
    )
)
data = [go.Scatter(
    x=df.budget.values,
    y=df.gross.values,
    mode='markers',
    text= df.movie_title.values,
    marker=dict(
        size=area,
        sizeref=1.0,
        color=df.imdb_score.values,
        showscale=True
    ))]
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='bubblechart-size')


# * Godzilla was not a good investment
# * Even if Avatar didn't have the best critics it has a good ratio gross/budget

# # Correlations

# In[43]:


df_clean = df.loc[df.loc[df.budget.dropna().index].gross.dropna().index]


# In[44]:


np.corrcoef(df_clean.budget.values.tolist(),df_clean.gross.values.tolist())[0, 1]


# If the budget for the movie is high it doesn't mean that the gross is high

# In[40]:


df_clean = df.dropna(axis=0, how='any')


# In[41]:


np.corrcoef(df_clean.imdb_score.values.tolist(),df_clean.movie_facebook_likes.values.tolist())[0, 1]


# The imdb score is related with the facebook movie likes

# In[12]:


df_corr = df[['num_critic_for_reviews', 'duration', 'director_facebook_likes', 'actor_2_name', 'actor_1_facebook_likes', 'gross', 'genres', 'num_voted_users', 'cast_total_facebook_likes', 'actor_3_name', 'facenumber_in_poster', 'num_user_for_reviews', 'language', 'country', 'content_rating', 'budget', 'title_year', 'imdb_score', 'movie_facebook_likes']].corr()


# In[10]:


def plot_correlation_map( df ):
    corr = df.corr()
    _ , ax = plt.subplots( figsize =( 12 , 10 ) )
    cmap = sns.diverging_palette( 240 , 10 , as_cmap = True )
    _ = sns.heatmap(
        corr, 
        cmap = cmap,
        square=True, 
        cbar_kws={ 'shrink' : .9 }, 
        ax=ax, 
        annot = True, 
        annot_kws = { 'fontsize' : 12 }
    )


# In[11]:


plot_correlation_map(df[['num_critic_for_reviews', 'duration', 'director_facebook_likes', 'actor_2_name', 'actor_1_facebook_likes', 'gross', 'genres', 'num_voted_users', 'cast_total_facebook_likes', 'actor_3_name', 'facenumber_in_poster', 'num_user_for_reviews', 'language', 'country', 'content_rating', 'budget', 'title_year', 'imdb_score', 'movie_facebook_likes']])


# In[17]:


df_corr.columns.values


# In[18]:


trace = go.Heatmap(z=df_corr.values.tolist(),
                   x=df_corr.columns.values,
                   y=df_corr.columns.values)
data=[trace]
py.iplot(data, filename='labelled-heatmap')


# # Map

# In[5]:


df.country.value_counts()


# In[7]:


data = [ dict(
        type = 'choropleth',
        locations = df['country'],
        locationmode='ISO-3',
        z = df['gross'],
        movie_titlext = df['movie_title'],
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            tickprefix = '$',
            title = 'Gross'),
      ) ]

layout = dict(
    title = 'Global gross per country',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

fig = dict( data=data, layout=layout )
py.iplot( fig, validate=False, filename='d3-world-map' )


# In[8]:


df_codes = pd.read_csv('https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv')


# In[ ]:


df_codes.head()


# In[ ]:




