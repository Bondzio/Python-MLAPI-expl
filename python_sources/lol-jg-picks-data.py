#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# In[ ]:


df = pd.read_csv('../input/leagueoflegends/LeagueofLegends.csv')


# In[ ]:


df.info()


# In[ ]:


junglePicks = df[['blueJungleChamp','redJungleChamp']]
bluePicks = junglePicks.pivot_table(index='blueJungleChamp', aggfunc='size').reset_index()
redPicks = junglePicks.pivot_table(index='redJungleChamp', aggfunc='size').reset_index()
bluePicks.columns = ['champ','bPick']
redPicks.columns = ['champ','rPick']


# In[ ]:


bluePicks = bluePicks.sort_values(by=['bPick'],ascending=False)
figurepx = px.bar(bluePicks, x='champ', y='bPick')
figurepx.show()


# In[ ]:


redPicks = redPicks.sort_values(by=['rPick'],ascending=False)
figurepx = px.bar(redPicks, x='champ', y='rPick')
figurepx.show()


# In[ ]:


junglePicks = pd.merge(bluePicks, redPicks, how='outer', on='champ').sort_values(by=['bPick','rPick'],ascending=False)
figurego = go.Figure(data=[
    go.Bar(name='BLUE SIDE', x=junglePicks['champ'], y=junglePicks['bPick']),
    go.Bar(name='RED SIDE', x=junglePicks['champ'], y=junglePicks['rPick'])
])
figurego.update_layout(barmode='stack')
figurego.show()

