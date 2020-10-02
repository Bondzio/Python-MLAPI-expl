#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns  # visualization tool

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


data = pd.read_csv('../input/Seasons_Stats.csv')


# In[ ]:


data.info()


# In[ ]:


data.corr()  # correlation


# In[ ]:


# correlation map
f,ax = plt.subplots(figsize=(20, 20))
sns.heatmap(data.corr(), annot = True, linewidths = 1, fmt = '.1f',ax = ax)
plt.show()


# In[ ]:


data.head(10)  # First 10 data


# In[ ]:


data.sample(10)


# In[ ]:


data.columns  # Columns


# In[ ]:


data.shape  # Data shape


# In[ ]:


data.dtypes  # Data types


# In[ ]:


data.describe()  # Description of datas


# **Line Plot - Scatter Plot - Histogram Plot**

# In[ ]:


# Line Plot
data.PTS.plot(kind = 'line', color = 'b', label = 'Points', linewidth = 1.5, alpha = 0.4, grid = True, linestyle = ':')
data.AST.plot(kind = 'line', color = 'r', label = 'Assists', linewidth = 1.5, alpha = 0.4, grid = True, linestyle = '-.')
plt.legend(loc = 'upper right')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.title('Points - Assists Line Plot')
plt.show()


# In[ ]:


# Scatter Plot 
data.plot(kind = 'scatter', x = 'PTS', y = 'WS', alpha = 0.3, color = 'red')
plt.xlabel('Points')
plt.ylabel('Win Shares')
plt.title('Points - Win Shares Scatter Plot')
plt.show()


# In[ ]:


# Histogram
# G : Game
data.G.plot(kind = 'hist', bins = 50, figsize = (10, 10))
plt.title('Game Histogram')
plt.xlabel('Number of Player')
plt.show()


# In[ ]:


x = data['PTS'] > 2500  # Who score over 2500 points
data[x]


# In[ ]:


totalScore = data.PTS + data.AST   # totalScore = Points + Assist
data["TotalScore"] = totalScore
newData = data.copy()
newData.sort_values('TotalScore', axis = 0, ascending = False, inplace = True, na_position = 'last')
newData["ScoreLevel"] = ["Legendary" if i > 4000 else "Perfect" if i > 3000 else "Very Good" if i > 2000 else "Good" for i in newData.TotalScore]
newData.loc[:1000,["Player","Year","Pos","TotalScore","ScoreLevel"]]


# In[ ]:


print(data['Pos'].value_counts(dropna = False))  # Frequency of player positions


# In[ ]:


data.boxplot(column = 'MP') # Minute Played
plt.show()


# In[ ]:


# melting
data_new = data.sample(5)
melted = pd.melt(frame = data_new, id_vars = 'Player', value_vars = ['PTS', 'AST'])
melted


# In[ ]:


# Reverse of melting
# pivot()
melted.pivot(index = 'Player', columns = 'variable', values = 'value')


# In[ ]:


data.info()


# In[ ]:


data['Player'].value_counts(dropna=False) # counts of player values
#There are 67 nan values


# In[ ]:


data.dropna(axis = 0,subset = ['Player'],inplace = True) # drop nan values


# In[ ]:


assert data['Player'].notnull().all() # returns nothing because we drop nan values


# In[ ]:


data['3P'].isnull().sum() # counts of nan values of column '3P'


# In[ ]:


data['3PA'].isnull().sum() # counts of nan values of column '3PA'


# In[ ]:


data['3P%'].isnull().sum() # counts of nan values of column '3P%'


# In[ ]:


# Fill columns with average
# 3P: 3-Point Field Goals, 3PA: 3-Point Attempt Field Goals, 3P%: 3-Point Field Goal Percentage
data['3P'].fillna(data['3P'].mean(),inplace = True)
data['3PA'].fillna(data['3PA'].mean(),inplace = True)
data['3P%'].fillna(data['3P%'].mean(),inplace = True)


# In[ ]:


data.info()


# In[ ]:





# In[ ]:




