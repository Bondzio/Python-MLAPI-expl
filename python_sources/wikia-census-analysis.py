#!/usr/bin/env python
# coding: utf-8

# # Load data 
# 
# 

# In[ ]:


import pandas as pd
import numpy as np
import pylab
get_ipython().run_line_magic('matplotlib', 'inline')

import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected=True)

df = pd.read_csv("../input/20181019-wikia_stats_users.csv")
df.drop_duplicates(subset=['url'], inplace=True)
df.head()


# In[ ]:


def describeMetric(df, metric):
    print(df[metric].describe())
    print("90%: {}".format(df[metric].quantile(0.9)))
    print("95%: {}".format(df[metric].quantile(0.95)))
    print("99%: {}".format(df[metric].quantile(0.99)))


# # Content stats
# 
# - `stats.pages` refers to all pages in the wiki, including articles, talk pages, redirects, etc.
# - `stats.articles` refers to the number of content pages in the wiki.
# 
# ## Pages
# 

# In[ ]:


describeMetric(df, 'stats.pages')


# ## Articles

# In[ ]:


describeMetric(df, 'stats.articles')


# # User stats

# In[ ]:


describeMetric(df,'users_1')


# # Edit stats

# In[ ]:


describeMetric(df, 'stats.edits')


# ## Edits per page

# In[ ]:


df['editsperpage'] = df['stats.edits'] / df['stats.pages']


# In[ ]:


describeMetric(df, 'editsperpage')


# # Distribution by language

# In[ ]:


groupByLanguage = df.groupby(by="lang")
byLanguage = groupByLanguage.id.count()
byLanguage.sort_values(ascending=False, inplace=True)
byLanguage


# In[ ]:


def langOther(x):
    if x in byLanguage.index[:8].values:
        return x
    else:
        return 'other'
    
byLanguage.index[:8]
df['language'] = df['lang']
df['language'] = df['language'].apply(langOther)


# In[ ]:


byReducedLanguage = df.groupby(by="language").id.count()
byReducedLanguage.sort_values(ascending=False, inplace=True)
byReducedLanguage


# In[ ]:


values = byReducedLanguage.values
values = 100*(values/values.sum())


data = [go.Bar(
            x=values,
            y=byReducedLanguage.index.values,
            orientation = 'h'
)]

annotations = [dict(
            x=x+8,
            y=y,
            xref='x',
            yref='y',
            text='{0:.2f}%'.format(x),
            showarrow=False
        ) for (x,y) in zip(values, list(range(0,len(values))))]

layout = go.Layout(
    xaxis=dict(
        range=[0,101],
        domain=[0,0.5],
        tickfont=dict(
            size=14,
        ),
        #showline=True
    ),
    yaxis=dict(
        tickfont=dict(
            size=14,
        ),
        ticksuffix=" "
    ),
    annotations = annotations
);


iplot(go.Figure(data= data, layout=layout), filename="byLanguage")


# # Distribution by hub category
# 
# Hub categories are defined by Wikia

# In[ ]:


groupByHub = df.groupby(by="hub")
byHub = groupByHub.id.count()
byHub.sort_values(ascending=False, inplace=True)
byHub


# In[ ]:


values = byHub.values
values = 100*(values/values.sum())


data = [go.Bar(
            x=values,
            y=byHub.index.values,
            orientation = 'h'
)]

annotations = [dict(
            x=x+8,
            y=y,
            xref='x',
            yref='y',
            text='{0:.2f}%'.format(x),
            showarrow=False
        ) for (x,y) in zip(values, list(range(0,len(values))))]

layout = go.Layout(
    xaxis=dict(
        range=[0,101],
        domain=[0,0.5],
        tickfont=dict(
            size=14,
        ),
        #showline=True
    ),
    yaxis=dict(
        tickfont=dict(
            size=14,
        ),
        ticksuffix=" "
    ),
    annotations = annotations
);


iplot(go.Figure(data= data, layout=layout), filename="byHub")


# # Analysis of Active and Inactive wikis
# 
# **Active wikis** are the ones with at least 1 user (`user_1`) and at least 1 active user in the previous 30 days (`stats.activeUsers`)
# 

# In[ ]:


threshold = 1
totalWikis = len(df) 
deadWikis = df[(df['stats.activeUsers']<threshold)|(df['users_1']==0)]
print ("Dead Wikis: {} ({:05.2f}%)".format(len(deadWikis), 100*len(deadWikis)/totalWikis))


# In[ ]:


aliveWikis = df[(df['stats.activeUsers']>=threshold)&(df['users_1']>0)]
print ("Alive Wikis: {} ({:05.2f}%)".format(len(aliveWikis), 100*len(aliveWikis)/totalWikis))
print("With less than 5 articles: {}".format(len(aliveWikis[aliveWikis['stats.articles']<5])))
print("With less than 24 pages: {}".format(len(aliveWikis[aliveWikis['stats.pages']<24])))
print("With less than 4 users: {}".format(len(aliveWikis[aliveWikis['users_1']<4])))


# ## Scatterplot of the number of users over the number of articles, distinguishing between active wikis (green) and inactive wikis (black)

# In[ ]:


fig = pylab.figure(figsize=(12,8))
ax = pylab.gca()
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xlabel('Users', {'size': 'large'})
ax.set_ylabel('Articles', {'size': 'large'})
ax.scatter(aliveWikis['users_1'].values,aliveWikis['stats.articles'].values, c='g',alpha=0.7)
ax.scatter(deadWikis['users_1'].values,deadWikis['stats.articles'].values, c='black', alpha=0.3)


# ## Scatterplot of the number of users over the number of edits, distinguishing between active wikis (green) and inactive wikis (black)
# 

# In[ ]:


fig = pylab.figure(figsize=(12,8))
ax = pylab.gca()
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xlabel('Users', {'size': 'large'})
ax.set_ylabel('Edits', {'size': 'large'})
ax.scatter(aliveWikis['users_1'].values,aliveWikis['stats.edits'].values, c='g',alpha=0.7)
ax.scatter(deadWikis['users_1'].values,deadWikis['stats.edits'].values, c='black', alpha=0.3)


# ## Scatterplot of the number of articles over the number of edits, distinguishing between active wikis (green) and inactive wikis (black)

# In[ ]:


fig = pylab.figure(figsize=(12,8))
ax = pylab.gca()
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xlabel('Articles', {'size': 'large'})
ax.set_ylabel('Edits', {'size': 'large'})
ax.scatter(aliveWikis['stats.articles'].values,aliveWikis['stats.edits'].values, c='g',alpha=0.7)
ax.scatter(deadWikis['stats.articles'].values,deadWikis['stats.edits'].values, c='black', alpha=0.3)


# ## Cummulative of wikis having at least U users

# In[ ]:


histAlive, binsAlive = np.histogram(aliveWikis[['users_1']],bins=int(aliveWikis[['users_1']].max()))
yAlive = np.cumsum(histAlive[::-1])[::-1]

histDead, binsDead = np.histogram(deadWikis[['users_1']],bins=int(deadWikis[['users_1']].max()))
yDead = np.cumsum(histDead[::-1])[::-1]


# In[ ]:


data = [
    go.Scattergl(
        x=binsAlive[0:len(binsAlive)-1],
        y=yAlive,     
        mode='markers',
        name="Active wikis",
        marker=dict(
            symbol='circle',
            opacity=0.7,
            color='green',
            size=8
        )
    ),
    go.Scattergl(
        x=binsDead[0:len(binsDead)-1],
        y=yDead, 
        mode='markers',
        name="Inactive wikis",
        marker=dict(
            symbol='circle',
            opacity=0.7,
            color='black',
            size=8
        )
    )
]

layout = go.Layout(
    xaxis=dict(
        type='log',
        autorange=True,
        domain=[0,0.5],
        exponentformat="power",
        title="At least U users"
    ),
    yaxis=dict(
        type='log',
        autorange=True,
        exponentformat="power",
        title="Number of wikis"
    ),
    legend=dict(
        x=0.3,
        y=0.9
    )
)

iplot(go.Figure(data= data, layout=layout))


# ## Cummulative of wikis having at least E edits
# 

# In[ ]:


histAlive, binsAlive = np.histogram(aliveWikis[['stats.edits']],bins= 100000)#int(aliveWikis[['stats.edits']].max()))
yAlive = np.cumsum(histAlive[::-1])[::-1]

histDead, binsDead = np.histogram(deadWikis[['stats.edits']],bins=100000)#int(deadWikis[['stats.edits']].max()))
yDead = np.cumsum(histDead[::-1])[::-1]


# In[ ]:


data = [
    go.Scattergl(
        x=binsAlive[0:len(binsAlive)-1],
        y=yAlive,     
        mode='markers',
        name="Active wikis",
        marker=dict(
            symbol='circle',
            opacity=0.7,
            color='green',
            size=8
        )
    ),
    go.Scattergl(
        x=binsDead[0:len(binsDead)-1],
        y=yDead, 
        mode='markers',
        name="Inactive wikis",
        marker=dict(
            symbol='circle',
            opacity=0.7,
            color='black',
            size=8
        )
    )
]

layout = go.Layout(
    xaxis=dict(
        type='log',
        autorange=True,
        domain=[0,0.5],
        exponentformat="power",
        title="At least E edits"
    ),
    yaxis=dict(
        type='log',
        autorange=True,
        exponentformat="power",
        title="Number of wikis"
    ),
    legend=dict(
        x=0.3,
        y=0.9
    )
)

iplot(go.Figure(data= data, layout=layout))


# ## Cummulative of wikis having at least P articles

# In[ ]:


histAlive, binsAlive = np.histogram(aliveWikis[['stats.articles']],bins= 100000)#int(aliveWikis[['stats.articles']].max()))
yAlive = np.cumsum(histAlive[::-1])[::-1]

histDead, binsDead = np.histogram(deadWikis[['stats.articles']],bins=100000)#int(deadWikis[['stats.articles']].max()))
yDead = np.cumsum(histDead[::-1])[::-1]


# In[ ]:


data = [
    go.Scattergl(
        x=binsAlive[0:len(binsAlive)-1],
        y=yAlive,     
        mode='markers',
        name="Active wikis",
        marker=dict(
            symbol='circle',
            opacity=0.7,
            color='green',
            size=8
        )
    ),
    go.Scattergl(
        x=binsDead[0:len(binsDead)-1],
        y=yDead, 
        mode='markers',
        name="Inactive wikis",
        marker=dict(
            symbol='circle',
            opacity=0.7,
            color='black',
            size=8
        )
    )
]

layout = go.Layout(
    xaxis=dict(
        type='log',
        autorange=True,
        domain=[0,0.5],
        exponentformat="power",
        title="At least P articles"
    ),
    yaxis=dict(
        type='log',
        autorange=True,
        exponentformat="power",
        title="Number of wikis"
    ),
    legend=dict(
        x=0.3,
        y=0.9
    )
)

iplot(go.Figure(data= data, layout=layout), filename="edits-cumsum")

