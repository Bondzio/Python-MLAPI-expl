#!/usr/bin/env python
# coding: utf-8

# Let's visualize the visualize how teams perform against one another.
# 
# What I want is similar to  a heat map, but it won't be symmetric.  Instead, the entry $[i,j]$ in the matrix will indicate how many times $i$ has won against $j$.  To do this, I will need to write some functions.
# 
# At the end, we should focus our attention on the rows which have the most red.  Those will indicate teams with a lot of wins.

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from sklearn.preprocessing import LabelEncoder
import matplotlib

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


#Connect to the SQL database
connection = sqlite3.connect('../input/database.sqlite')


#Use the query to extract English Premiere League Data
query = '''
with x as (
SELECT

home_team_api_id,
away_team_api_id,

home_team_goal,
away_team_goal

FROM MATCH
where country_id='1729'
)


Select
b.team_long_name as home_team,
x.home_team_goal as home_score,
c.team_long_name as away_team,
x.away_team_goal as away_score
from x inner join Team b on x.home_team_api_id = b.team_api_id
inner join Team c on x.away_team_api_id = c.team_api_id;
'''

#Get a dataframe
df = pd.read_sql(query,connection)

print(df.columns)
print(df[df.home_team=='Manchester United'])

#I need the team names as integers so I can stuff them in a matrix. Here is how I will do it.
team_encoder = LabelEncoder()

# Fitting the encoder
team_encoder.fit(  list(df.away_team.unique()) + list(df.home_team.unique()) )


#Convert names to integers
df['home_team'] = team_encoder.transform(df.home_team)
df['away_team'] = team_encoder.transform(df.away_team)


# In[ ]:


def result_tuple(x):
    
    return (x.home_team,x.away_team,x.winner)

def winner(x):
    
    if x.away_score==x.home_score:
        return np.NAN
    
    if x.away_score > x.home_score:
        return x.away_team
    else:
        return x.home_team
    
df['winner'] = df.apply(winner,axis = 1)
df.dropna(inplace = True)
data = df.apply(result_tuple,axis = 1).tolist()


# In[ ]:


X = np.zeros((34,34))


for d in data:
    
    i,j,k = [int(j) for j in d]
    
    #Add one to indicate a win
    if i==k:
        X[i,j]+=1
    else:
        X[j,i]+=1


# In[ ]:


fig, ax = plt.subplots(figsize = (10,10))


cmap = matplotlib.cm.get_cmap('RdBu_r', 12)

im = ax.imshow(X, cmap = cmap, interpolation='None')


plt.colorbar(im,fraction=0.046, pad=0.04)
plt.grid('off')




teams = team_encoder.inverse_transform(range(34))

plt.xticks(np.arange(34),teams,rotation = 90)
plt.yticks(np.arange(34),teams)

plt.savefig('Soccer.png')


# In[ ]:





# In[ ]:




