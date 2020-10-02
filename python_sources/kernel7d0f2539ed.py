#!/usr/bin/env python
# coding: utf-8

# In[ ]:




import numpy as np 
import pandas as pd 
import re
import matplotlib.pyplot as plt
import plotly
import seaborn as sns
import yellowbrick as yel
import os
print(os.listdir("../input"))


# In[ ]:


fifa = pd.read_csv('../input/data.csv')
fifa.head()


# In[ ]:


columns = [
    'Name',
    'Age',
    'Nationality',
    'Overall',
    'Club',
    'Value',
    'Preferred Foot',
    'Position',
    'Jersey Number',
    'Height',
    'Weight',
    'Crossing',
    'Finishing',
    'HeadingAccuracy',
    'ShortPassing',
    'Volleys',
    'Dribbling',
    'Curve',
    'FKAccuracy',
    'LongPassing',
    'BallControl',
    'Acceleration',
    'SprintSpeed',
    'Agility',
    'Reactions',
    'Balance',
    'ShotPower',
    'Jumping',
    'Stamina',
    'Strength',
    'LongShots',
    'Aggression',
    'Interceptions',
    'Positioning',
    'Vision',
    'Penalties',
    'Composure',
    'Marking',
    'StandingTackle',
    'SlidingTackle'
]


# In[ ]:


fifa1 = pd.DataFrame(fifa, columns = columns)
fifa1.head(3)


# In[ ]:


fig, map = plt.subplots(figsize=(16,16))
map = sns.heatmap(fifa1[['Age', 'Overall', 'Value', 'Position', 'Preferred Foot', 'Jersey Number',
                    'Height', 'Weight', 'Nationality', 'Club', 'Crossing', 'Finishing', 'HeadingAccuracy', 'ShortPassing',
                    'Volleys', 'Dribbling', 'Curve', 'FKAccuracy', 'LongPassing', 'BallControl', 'Acceleration',
                    'SprintSpeed', 'Agility', 'Reactions', 'Balance', 'ShotPower', 'Jumping', 'Stamina', 'Strength',
                    'LongShots', 'Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure',
                    'Marking', 'StandingTackle', 'SlidingTackle' ]].corr(), annot = True, linewidths = .5, cmap = 'Greens')
map.set_title(label = 'FIFA Players Heatmap', fontsize = 20)


# In[ ]:


x = fifa1['Overall']
x
y = fifa1['Value']
y


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


xyz = train_test_split(x, y, test_size = .2)


# In[ ]:


f_o_f = sns.lmplot(x = 'Overall', y = 'Finishing', data = fifa1, scatter_kws = {'alpha':0.075}, col = 'Preferred Foot');


# In[ ]:


ss = sns.lineplot(x="Stamina", y="Strength", hue="Preferred Foot",
                  data=fifa1)


# In[ ]:


plt.figure(figsize=(12,8))
pos = sns.countplot(x="Position",  data=fifa1)


# In[ ]:


plt.figure(figsize=(12,6))
pos = sns.countplot(x="Preferred Foot",  data=fifa1)


# In[ ]:


sns.lmplot(x="Overall", y="Value", hue="Preferred Foot", data=fifa1)

