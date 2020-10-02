#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('darkgrid')


# In[ ]:


data = pd.read_csv('../input/league-of-legends-diamond-ranked-games-10-min/high_diamond_ranked_10min.csv')
data.head()


# In[ ]:


cols = ['gameId',  'redKills', 'redGoldDiff', 'redExperienceDiff', 'redCSPerMin', 'redGoldPerMin','blueGoldDiff', 'blueExperienceDiff', 'blueCSPerMin', 'blueGoldPerMin', 'redWardsPlaced','redWardsDestroyed','redFirstBlood','redDeaths','redAssists','redEliteMonsters','redDragons','redHeralds','redTowersDestroyed','redTotalGold','redAvgLevel','redTotalExperience','redTotalMinionsKilled','redTotalJungleMinionsKilled']
data = data.drop(cols, axis = 1)
data.info()


# In[ ]:


plt.figure(figsize=(10,10))
sns.heatmap(data.corr(), cmap='YlGnBu', annot=True, fmt='.2f', vmin=0);


# In[ ]:


data.head()


# In[ ]:



bincols = ['blueFirstBlood','blueWins','blueDragons','blueHeralds']
histdata1  = data.drop(bincols, axis = 1)
histdata1.hist( figsize=(11,11), bins=10);


# In[ ]:


nonbincols = ['blueAssists','blueAvgLevel','blueDeaths','blueEliteMonsters','blueKills','blueTotalExperience','blueTotalGold','blueTotalJungleMinionsKilled','blueTowersDestroyed','blueWardsDestroyed','blueWardsPlaced']
histdata2  = data.drop(nonbincols, axis = 1)
histdata2.hist( figsize=(7,7), bins=2);


# In[ ]:


from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
X = data
y = data['blueWins']
scaler = MinMaxScaler()
scaler.fit(X)
X = scaler.transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# In[ ]:


from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(X_train, y_train)

lr.coef_


# In[ ]:




