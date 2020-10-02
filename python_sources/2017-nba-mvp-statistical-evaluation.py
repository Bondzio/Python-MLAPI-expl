#!/usr/bin/env python
# coding: utf-8

# **Identifying the most "valuable" player based on advanced statistics and analysis**

# In[ ]:


import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
color = sns.color_palette()
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


pie_df = pd.read_csv("../input/nba_2017_pie.csv")
pie_df = pie_df.query('GP>50')
#Filter for players who have played more than 50 games
pie_df = pie_df.query('MIN>25')
#Filter for players who average more than 25 minutes a game
pie_df = pie_df.query('PIE>12')
#Filter players with a significant contribution/usage rate
pie_df.head()


# In[ ]:


plus_minus_df = pd.read_csv("../input/nba_2017_real_plus_minus.csv")
plus_minus_df = plus_minus_df.query('GP>50')
#Filter for players who have played more than 50 games
plus_minus_df = plus_minus_df.query('MPG>25')
#Filter for players who average more than 25 minutes a game
plus_minus_df.head()


# In[ ]:


br_stats_df = pd.read_csv("../input/nba_2017_br.csv")
br_stats_df = br_stats_df.query('G>50')
#Filter for players who have played more than 50 games
br_stats_df = br_stats_df.query('MP>25')
#Filter for players who average more than 25 minutes a game
br_stats_df.head()


# In[ ]:


plus_minus_df.rename(columns={"NAME":"PLAYER", "WINS": "WINS_RPM"}, inplace=True)
players = []
for player in plus_minus_df["PLAYER"]:
    plyr, _ = player.split(",")
    players.append(plyr)
plus_minus_df.drop(["PLAYER"], inplace=True, axis=1)
plus_minus_df["PLAYER"] = players
plus_minus_df.head()


# In[ ]:


nba_players_df = br_stats_df.copy()
nba_players_df.rename(columns={'Player': 'PLAYER','Pos':'POSITION', 'Tm': "TEAM", 'Age': 'AGE', 'TRB': 'REB', "PS/G": "PPG"}, inplace=True)
nba_players_df.drop(["Rk","G", "GS", "TEAM", "POSITION", "AGE", "2P", "2PA", "2P%","3P", "3PA", "3P%", "eFG%","PF", "ORB", "DRB"], inplace=True, axis=1)
nba_players_df = nba_players_df.merge(plus_minus_df, how="inner", on="PLAYER")
nba_players_df.head()


# In[ ]:


pie_df_subset = pie_df[["PLAYER", "NETRTG", "AST%", "AST/TO","REB%", "USG%", "TS%", "W"]].copy()
nba_players_df = nba_players_df.merge(pie_df_subset, how="inner", on="PLAYER")
nba_players_df.drop(["ORPM","DRPM" ], inplace=True, axis=1)
nba_players_df.head()


# In[ ]:


plt.subplots(figsize=(20,15))
ax = plt.axes()
ax.set_title("NBA Player Correlation Heatmap:  2016-2017 Season")
corr = nba_players_df.corr()
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)


# From the heatmap, we can see that **Net Rating (NETRTG)** is most correlated to **wins**

# In[ ]:


#Run a scatterplot to visualize this relationship
sns.lmplot(x="NETRTG", y="W", data=nba_players_df)


# In[ ]:


#Perform linear regression to confirm this relationship
results = smf.ols('W ~NETRTG', data=nba_players_df).fit()
print(results.summary())


# ***The regression formula showed a positive relationship between players' net rating and wins***

# In[ ]:


#Further review top 25 players' value from Net Rating
nba_players_df.nlargest(25,'NETRTG')


# To assess for the **Most *Valuable* player,** I will look to gauge their individual *value* to a team. To do so I will remove players on this list from the **same team** since their Net Rating (NETRTG) is affected by teammates on this list

# In[ ]:


nba_players_df['TEAM'].value_counts()


# The output list shows a number of **teams with multiple players** who qualified for both a **significant amount of playing time** (Minutes and Game played) and **contribution of possession** (PIE)

# In[ ]:


nba_players_df.drop_duplicates(subset ="TEAM", 
                     keep = False, inplace = True) 
#This new dataset will identify players with more individual contribution to team
nba_players_df.drop(["FG","FGA", "FG%", "FT", "FTA", "FT%"], inplace=True, axis=1)
nba_players_df.nlargest(15,'NETRTG')


# In[ ]:


results = smf.ols('W ~NETRTG', data=nba_players_df).fit()
print(results.summary())


# The new dataset containing only **individual standout players** actually produced a **more accurate model (Lower AIC & BIC, Higher Adj. R-squared) ** than the previous model

# In[ ]:


#Create a cummalative value statistic based on the individual affect on scoring (Net Rating), total amount of contribution (Usage Rate) and overall team performance (Ws)
nba_players_df['VALUE'] = round(nba_players_df['NETRTG']*nba_players_df['USG%']*nba_players_df['W']*nba_players_df['GP']/82, 2)
nba_players_df.nlargest(15,'VALUE')


# Based on the results calculated, the Most Valuable Player for the 2016-2017 season should be 
# **James Harden**
# ![](https://clutchpoints.com/wp-content/uploads/2018/06/james-harden-2.jpg)
# ...unfortunately, the media voted Russell Westbrook to be the actual winner
# ![](https://cdn-images-1.medium.com/max/599/1*bzOWBk9RN7scZNSUbETrNA.jpeg)
