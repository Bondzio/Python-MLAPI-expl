#!/usr/bin/env python
# coding: utf-8

# # ANALYSIS OF ACADEMY AWARDS DATASET

# ![img ](https://media.giphy.com/media/srg19CG0cKMuI/giphy.gif)

# In[ ]:


import pandas as pd
import numpy as np 
import plotly
import plotly.graph_objs as go
plotly.offline.init_notebook_mode(connected=True)
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


df = pd.read_csv('../input/database.csv')
df.head(1)


# In[ ]:


dirc = df[(df['Award'] == 'Directing')]['Film'].value_counts()
dirc = dirc[(dirc.values > 3)]
d = df[(df['Award'] == 'Directing') & df['Winner'] == 1]['Film'].value_counts()
d = d[(d.values > 1)]
won = []
nomi = []
for i in d.index:
    if i in dirc.index:
        won.append(d[i])
        nomi.append(dirc[i])


# In[ ]:


trace1 = go.Bar(
    x=d.index,
    y=nomi,
    name='Nominations'
)
trace2 = go.Bar(
    x=d.index,
    y=won,
    name='Won'
)

data = [trace1, trace2]
plotly.offline.iplot({
    "data": data,
    "layout": go.Layout(barmode='group', title="Nominations vs Wins of Directors with more than one oscar"
                           ,width=800,height=500,)
})


# Looks like john ford has the highest win percentage of 80% and William Wyler has the lowest of 25%

# ![img ](https://media.giphy.com/media/xT9IghIG6yXWd64Yms/giphy.gif)

# In[ ]:





# In[ ]:


actor_nom = df[(df['Award'] == 'Actor') ]['Name'].value_counts()
actor_nom = actor_nom[(actor_nom.values > 2)]
actor_win =  df[(df['Award'] == 'Actor') & df['Winner'] == 1]['Name'].value_counts()
won = []
for i in actor_nom.index:
    if i in actor_win.index:
        won.append(actor_win[i])
    else:
        won.append(0)


# In[ ]:


trace1 = go.Bar(
    x=actor_nom.index,
    y=actor_nom.values,
    name='Nominations'
)
trace2 = go.Bar(
    x=actor_nom.index,
    y=won,
    name='Won'
)

data = [trace1, trace2]
plotly.offline.iplot({
    "data": data,
    "layout": go.Layout(barmode='group', title="Nominations vs Wins of Actors with more than one oscar"
                           ,width=1000,height=300,)
})


# Spencer Tracy has the highest number of nominations and wins followed by Laurence Ol and Marlon brando

# In[ ]:


actor_nom = df[(df['Award'] == 'Actor in a Supporting Role') ]['Name'].value_counts()
actor_nom = actor_nom[(actor_nom.values > 2)]
actor_win =  df[(df['Award'] == 'Actor in a Supporting Role') & df['Winner'] == 1]['Name'].value_counts()
won = []
for i in actor_nom.index:
    if i in actor_win.index:
        won.append(actor_win[i])
    else:
        won.append(0)
trace1 = go.Bar(
    x=actor_nom.index,
    y=actor_nom.values,
    name='Nominations'
)
trace2 = go.Bar(
    x=actor_nom.index,
    y=won,
    name='Won'
)

data = [trace1, trace2]
plotly.offline.iplot({
    "data": data,
    "layout": go.Layout(barmode='group', title="Nominations vs Wins of Actor in a Supporting Role with more than one oscar"
                           ,width=1000,height=300,)
})


# In[ ]:


actor_nom = df[(df['Award'] == 'Actor in a Leading Role') ]['Name'].value_counts()
actor_nom = actor_nom[(actor_nom.values > 2)]
actor_win =  df[(df['Award'] == 'Actor in a Leading Role') & df['Winner'] == 1]['Name'].value_counts()
won = []
for i in actor_nom.index:
    if i in actor_win.index:
        won.append(actor_win[i])
    else:
        won.append(0)
trace1 = go.Bar(
    x=actor_nom.index,
    y=actor_nom.values,
    name='Nominations'
)
trace2 = go.Bar(
    x=actor_nom.index,
    y=won,
    name='Won'
)

data = [trace1, trace2]
plotly.offline.iplot({
    "data": data,
    "layout": go.Layout(barmode='group', title="Nominations vs Wins of Actor in a leading Role with more than one oscar"
                           ,width=1000,height=300,)
})


# ![img ](https://media.giphy.com/media/2wYxEYYuf8Vs9hiWtQ/giphy.gif)

# In[ ]:


actress_nom = df[(df['Award'] == 'Actress') ]['Name'].value_counts()
actress_nom = actress_nom[(actress_nom.values >= 3)]
actress_win =  df[(df['Award'] == 'Actress') & df['Winner'] == 1]['Name'].value_counts()
won = []
for i in actress_nom.index:
    if i in actress_win.index:
        won.append(actress_win[i])
    else:
        won.append(0)


# In[ ]:


trace1 = go.Bar(
    x=actress_nom.index,
    y=actress_nom.values,
    name='Nominations'
)
trace2 = go.Bar(
    x=actress_nom.index,
    y=won,
    name='Won'
)

data = [trace1, trace2]
plotly.offline.iplot({
    "data": data,
    "layout": go.Layout(barmode='group', title="Nominations vs Wins of actresss with more than one oscar"
                           ,width=1000,height=300,)
})


# In[ ]:


actress_nom = df[(df['Award'] == 'Actress in a Leading Role') ]['Name'].value_counts()
actress_nom = actress_nom[(actress_nom.values > 2)]
actress_win =  df[(df['Award'] == 'Actress in a Leading Role') & df['Winner'] == 1]['Name'].value_counts()
won = []
for i in actress_nom.index:
    if i in actress_win.index:
        won.append(actress_win[i])
    else:
        won.append(0)
trace1 = go.Bar(
    x=actress_nom.index,
    y=actress_nom.values,
    name='Nominations'
)
trace2 = go.Bar(
    x=actress_nom.index,
    y=won,
    name='Won'
)

data = [trace1, trace2]
plotly.offline.iplot({
    "data": data,
    "layout": go.Layout(barmode='group', title="Nominations vs Wins of actresss in Leading role with more than one oscar"
                           ,width=1000,height=300,)
})


# ![img ](https://media.giphy.com/media/l46CAeMR1XVgrpY5O/giphy.gif)

# In[ ]:


actress_nom = df[(df['Award'] == 'Actress in a Supporting Role') ]['Name'].value_counts()
actress_nom = actress_nom[(actress_nom.values > 2)]
actress_win =  df[(df['Award'] == 'Actress in a Supporting Role') & df['Winner'] == 1]['Name'].value_counts()
won = []
for i in actress_nom.index:
    if i in actress_win.index:
        won.append(actress_win[i])
    else:
        won.append(0)
trace1 = go.Bar(
    x=actress_nom.index,
    y=actress_nom.values,
    name='Nominations'
)
trace2 = go.Bar(
    x=actress_nom.index,
    y=won,
    name='Won'
)

data = [trace1, trace2]
plotly.offline.iplot({
    "data": data,
    "layout": go.Layout(barmode='group', title="Nominations vs Wins of actresss in supporting role with more than one oscar"
                           ,width=1000,height=300,)
})


# In[ ]:


dd = df[(df['Winner'] == 1)]
years = dd['Year'].value_counts()
trace = go.Scatter(
    x = years.index,
    y = years.values,    
    mode='markers',
    marker=dict(
        size=15,
        color = years.values, 
        colorscale='Viridis',
        showscale=True
    )
)
plotly.offline.iplot({
    "data": [trace],
    "layout": go.Layout(title="Number of Oscars given out over the years "
                           ,width=1000,height=300,)
})


# ### On an average about 20-30 Academy Awards are given out each year

# In[ ]:


dd = dd['Name'].value_counts()


# In[ ]:


ds = dd[(dd.values > 4)]
trace0 = go.Bar(
    x=ds.index,
    y=ds.values,
)

data = [trace0]
plotly.offline.iplot({
    "data": [trace0],
    "layout": go.Layout(title="Movies/ Artist with most Oscar wins (Any Award) "
                           ,width=1000,height=300,)
})


# ![img ](https://media.giphy.com/media/3o6EhZHDSQe9Bi4LYs/giphy.gif)

# ## Winners of Gordon E Sawyer Award over the years

# In[ ]:


df[(df['Award'] == 'Gordon E. Sawyer Award')]['Name'].value_counts()


# ## Winners of John A. Bonner Medal of Commendation

# In[ ]:


df[(df['Award'] == 'John A. Bonner Medal of Commendation')]['Name'].value_counts()


# ![img ](https://media.giphy.com/media/cC9kQMcSrQ1Xci4MxI/giphy.gif)
