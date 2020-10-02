#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV, LinearRegression, Ridge, RidgeCV

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.''


# In[ ]:


df_season = pd.read_csv('../input/Seasons_Stats.csv')


# In[ ]:


df_season.columns


# In[ ]:


df_season = df_season[['Year', 'Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP', 'PTS']]


# In[ ]:


df_season.describe()


# In[ ]:


df_2017 = df_season[df_season.Year == 2017]


# In[ ]:


df_2017.describe()


# In[ ]:


df_2017.head(5)


# In[ ]:


df_new = df_2017[['Player', 'Pos', 'G', 'PTS', 'Age']].copy()


# In[ ]:


df_new.head(5)


# In[ ]:


df_new = df_new.groupby('Player').sum()


# In[ ]:


df_new.head(5)


# In[ ]:


df_new['PPG'] = df_new['PTS']/df_new['G']


# In[ ]:


df_new.head(5)


# In[ ]:


df_players = pd.read_csv('../input/player_data.csv')


# In[ ]:


df_players.head(5)


# In[ ]:


df_players = df_players[['name', 'position', 'height', 'weight', 'college']]


# In[ ]:


df_players.head(5)


# In[ ]:


df_players = df_players.rename(columns={'name':'Player', 'position':'Position', 'height':'Height', 'weight':'Weight', 'college':'College'})


# In[ ]:


df_2017set = pd.merge(df_players, df_new, on='Player')


# In[ ]:


df_2017set.head(5)


# In[ ]:


df_2017set.isnull().sum()


# In[ ]:


del df_2017set['Age']


# In[ ]:


df_2017set.describe()


# In[ ]:


#df_2017set[df_2017set.PPG > 25]


# In[ ]:


df_2017set.head(5)


# In[ ]:


inches = []
position = []

for i in range(0, len(df_2017set)):
    temp = list(df_2017set.iloc[i]['Height'])
    feet = int(''.join(temp[0]))
    inch = int(''.join(temp[2:]))
    tot = feet*12 + inch
    inches.append(tot)
    if df_2017set.iloc[i]['Position'] == 'C-F':
        position.append('C')
    elif df_2017set.iloc[i]['Position'] == 'F-G' or df_2017set.iloc[i]['Position'] == 'F-C':
        position.append('F')
    elif df_2017set.iloc[i]['Position'] == 'G-F':
        position.append('G')
    else:
        pos = df_2017set.iloc[i]['Position']
        position.append(pos)


# In[ ]:


df_2017set.insert(3, "Height in inches", inches)


# In[ ]:


df_2017set.insert(2, 'Position2', position)


# In[ ]:


df_2017set.head(8)


# In[ ]:


del df_2017set['Height']


# In[ ]:


del df_2017set['Position']


# In[ ]:


df_2017set = df_2017set.rename(columns={'Height in inches':'Height'})


# In[ ]:


df_2017set = df_2017set.rename(columns={'Position2':'Position'})


# In[ ]:


#df_2017set["Player"][index] = 'rename'


# In[ ]:


df_2017set.head(8)


# In[ ]:


df_2017set.boxplot(column='Weight', by='Position')


# In[ ]:


df_2017set.boxplot(column='PPG', by='Position')


# In[ ]:




