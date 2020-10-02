#!/usr/bin/env python
# coding: utf-8

# # Importing the required libraries

# In[ ]:



import pandas as pd
import numpy as np
import  matplotlib.pyplot as plt
import  seaborn as sns
import warnings
fig_size = [80, 80]
plt.rcParams['figure.figsize'] = fig_size
warnings.filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')
from subprocess import check_output


# # Reading the data using Pandas

# 1) A bit cleaning of data is done here. Removed few rows based on criteria like minimum number of players as 0 because they do not add value to the observations.

# In[ ]:


print(check_output(["ls", "../input"]).decode("utf8"))
df = pd.read_csv('../input/bgg_db_2017_04.csv', encoding='latin1')

# Data Cleaning
missing = df[(df['min_players'] < 1) 
          | (df['max_players'] < 1) | (df['avg_time'] < 1) 
           | (df['min_time'] < 1) | (df['max_time'] < 1) | (df['year'] < 1950) | (df['max_players'] > 10)]
df = df[(df['min_players'] >= 1) & (df['max_players'] >= 1)  
        & (df['avg_time'] >= 1) & (df['min_time'] >= 1) & (df['max_time'] >= 1) & (df['year'] > 1950) 
        & (df['max_players'] < 10)]
df['avg_players'] = (df['min_players'] + df['max_players'])/2 
df.category = df.category.astype('category')


# # Plot1: Game Rating versus Weight

# 1) This graph is to see relation between weight ranges of the games against ratings.
# 
# 2) It can be observed that higher the weight range, higher the range of ratings.
# 
# 3) It can also be observed that geek rating almost never goes above average rating.
# 
# 4) Also, geek rating for all the weight ranges lies between 5.5 and 6.5.

# In[ ]:


bins = [-1, 1, 2, 3, 4, 5]
df['weight_cat'] = pd.cut(df['weight'], bins=bins, labels=bins[1:])
df['weight_cat']

weight_avg = [df[df['weight_cat'] == i]['avg_rating'] for i in range(1,6)]
weight_geek = [df[df['weight_cat'] == i]['geek_rating'] for i in range(1,6)]

f, axes = plt.subplots(1, 2, figsize = (18, 10), sharex = True, sharey = True) 

k1 = sns.violinplot(data=weight_avg, ax = axes[0] )
k2 = sns.violinplot(data=weight_geek, ax = axes[1])
axes[0].set(xlabel='weight range', ylabel='avgerage rating', xticklabels=['0-1', '1-2', '2-3', '3-4', '4-5'])
axes[1].set(xlabel='weight range', ylabel='geek rating', xticklabels=['0-1', '1-2', '2-3', '3-4', '4-5'])


# # Plot2 : PlayerRanges versus Count

# 1) This is a a graph for observing the player ranges (from minimum to maximum) against their count using bars. For this we add a new column with the name 'player_range'. Excluded player_range with rare occurences keeping threshold limit as 50.
# 
# 2) It can be observed that games with player range 2-4 are highest in number followed by a 2 player game. This observation is quite intuitive as people prefer a one on one or two on two games.
# 
# 3) Interesting there are very few games that can be played alone (last in the graph).

# In[ ]:


df['player_range'] = df['min_players'].astype(str) + '-' + df['max_players'].astype(str)
player_range =  df['player_range'].value_counts()
player_range = player_range[player_range > 50]
vis = sns.barplot(x = player_range.index, y= player_range)
sns.set(font_scale = 2)
vis.set(xlabel='player range', ylabel = 'count')
plt.rcParams["figure.figsize"] = [40, 20]


# # Plot3 : PlayerMean versus Count
# 

# 
# 1) This is a plot showing average number of players for all the games against their count.
# 
# 2) Most of the games, the average number of players is three followed by two.

# In[ ]:


player_counts =  df['avg_players'].value_counts()
player_counts = player_counts[player_counts > 50]
vis = sns.barplot(x = player_counts.index, y = player_counts)
sns.set(font_scale = 2)
plt.title('Mean Player Counts')
vis.set(xlabel='average players')
vis.set(ylabel='player count')
plt.show()


# # Plot4: Game Count versus Year

# 1) Board games released per year consistently increased till 2015 and then there is a downward trend observed.

# In[ ]:


game_count = df['year'].value_counts()
game_count = game_count[game_count > 25]
sns.barplot(x = game_count.index, y = game_count)
plt.title('Mean Player Counts')
vis.set(xlabel='player count')


# # Plot5: Distribution of Average Rating and Geek Rating

# 1) This plot helps in showing the distribution of ratings against the weights. 
# 
# 2) It can be seen that average rating is more or less equally distributed from 5.5 to 8.5 where as geek rating is highly concentrated between 5.5 and 6.

# In[ ]:


f, axes = plt.subplots(1, 2, figsize = (18, 10), sharex = True, sharey = True) 
k1 = sns.kdeplot(df['weight'], df['avg_rating'] ,ax = axes[0])
k2 = sns.kdeplot(df['weight'], df['geek_rating'], ax = axes[1])


# # Plot6: Average Rating versus Geek Rating

# In[ ]:


sns.kdeplot(df['avg_rating'], df['geek_rating'], shade = True, cmap = 'Reds')
sns.set(font_scale = 2)
plt.rcParams["figure.figsize"] = [18, 9]


# # Plot7: Distribution of games across various age groups

# In[ ]:


vis = sns.distplot(df['age'], bins = 30)


# # Plot8: Age versus Weight
# 

# In[ ]:


vis = sns.boxplot(data = df, x = 'age', y = 'weight')


# In[ ]:




