#!/usr/bin/env python
# coding: utf-8

# # Background
# Every time I watch the NBA, it seems to me that a 10-20 point differential can be easily overcome in a moments notice. I wanted to explore whether being down at half time was correlated/predictive of a win. 
# 
# Turns out it is quite indicative in general, but it is not indicative for the best teams in the league, e.g. the Warriors, Cavs, Rockets, or the Celtics.

# In[ ]:


import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

pd.options.mode.chained_assignment = None
DOWN_AT_HALF = -1
TIE_AT_HALF = 0
UP_AT_HALF = 1

df16 = pd.read_csv("../input/2016-17_teamBoxScore.csv")
df17 = pd.read_csv("../input/2017-18_teamBoxScore.csv")


# In[ ]:


#Choose on of the following options to pick which dataset
#df = df16
#df = df17
df = pd.concat((df16, df17))


# In[ ]:


df2 = df[["teamAbbr", "teamPTS", "teamPTS1", "teamPTS2", "opptPTS", "opptPTS1", "opptPTS2"]]

#record half time points and point differentials
df2.loc[:, "teamPTSH1"] = df2["teamPTS1"] + df["teamPTS2"]
df2.loc[:, "opptPTSH1"] = df2["opptPTS1"] + df["opptPTS2"]

df2.loc[:, "ptdiffH1"] = df2["teamPTSH1"] - df2["opptPTSH1"]
df2.loc[:, "ptdiff"] = df2["teamPTS"] - df2["opptPTS"]


# In[ ]:


def make_point_diff_mat(df):
    point_diff_df = df[["ptdiffH1", "ptdiff"]]
    point_diff = point_diff_df.as_matrix()
    return point_diff

def make_bool_point_diff_mat(df):
    point_diff = make_point_diff_mat(df)
    bool_point_diff = np.copy(point_diff)
    bool_point_diff[bool_point_diff > 0] = 1
    bool_point_diff[bool_point_diff < 0] = -1
    return bool_point_diff

def prob_of_winning_given(bool_point_diff, event):
    return np.mean((bool_point_diff[bool_point_diff[:,0] == event][:, 1] + 1 ) / 2)


# # Overall Statistics

# In[ ]:


point_diff = make_point_diff_mat(df2)
np.corrcoef(point_diff.T)


# In[ ]:


plt.scatter(point_diff[:, 0], point_diff[:, 1])
plt.ylabel("point differential: end of game")
plt.xlabel("point differential: end of first half")


# In[ ]:


bool_point_diff = make_bool_point_diff_mat(df2)
np.corrcoef(bool_point_diff.T)


# In[ ]:


# Probability of winning given that you are TRAILING in the first half
prob_of_winning_given(bool_point_diff, DOWN_AT_HALF)


# In[ ]:


# Probability of winning given that you are LEADING in the first half
prob_of_winning_given(bool_point_diff, UP_AT_HALF)


# ## Who is most likely to win while DOWN at half

# In[ ]:


max_prob_winning_DOWN_at_half = 0
max_team = None
for abbr in df2.teamAbbr.unique():
    df_team = df2[df.teamAbbr == abbr]
    bool_point_diff_team = make_bool_point_diff_mat(df_team)
    prob = prob_of_winning_given(bool_point_diff_team, DOWN_AT_HALF)    
    if prob > max_prob_winning_DOWN_at_half:
        max_prob_winning_DOWN_at_half = prob
        max_team = abbr
print(max_team)
print(max_prob_winning_DOWN_at_half)


# ## Who is most likely to win while UP at half

# In[ ]:


max_prob_winning_UP_at_half = 0
max_team = None
for abbr in df2.teamAbbr.unique():
    df_team = df2[df.teamAbbr == abbr]
    bool_point_diff_team = make_bool_point_diff_mat(df_team)
    prob = prob_of_winning_given(bool_point_diff_team, UP_AT_HALF)    
    if prob > max_prob_winning_UP_at_half:
        max_prob_winning_UP_at_half = prob
        max_team = abbr
print(max_team)
print(max_prob_winning_UP_at_half)


# # Cavaliers specific

# In[ ]:


df_cavs = df2[df2["teamAbbr"] == "CLE"]


# In[ ]:


point_diff_cavs = make_point_diff_mat(df_cavs)
np.corrcoef(point_diff_cavs.T)


# In[ ]:


plt.scatter(point_diff_cavs[:, 0], point_diff_cavs[:, 1])
plt.ylabel("point differential: end of game")
plt.xlabel("point differential: end of first half")


# In[ ]:


bool_point_diff_cavs = make_bool_point_diff_mat(df_cavs)
np.corrcoef(bool_point_diff_cavs.T)


# In[ ]:


prob_of_winning_given(bool_point_diff_cavs, DOWN_AT_HALF)


# In[ ]:


prob_of_winning_given(bool_point_diff_cavs, UP_AT_HALF)


# # Warriors Specific

# In[ ]:


df_warr = df2[df2.teamAbbr == "GS"]


# In[ ]:


point_diff_warr = make_point_diff_mat(df_warr)
np.corrcoef(point_diff_warr.T)


# In[ ]:


plt.scatter(point_diff_warr[:, 0], point_diff_warr[:, 1])
plt.ylabel("point differential: end of game")
plt.xlabel("point differential: end of first half")


# In[ ]:


bool_point_diff_warr = make_bool_point_diff_mat(df_warr)
np.corrcoef(bool_point_diff_warr.T)


# In[ ]:


prob_of_winning_given(bool_point_diff_warr, DOWN_AT_HALF)


# In[ ]:


prob_of_winning_given(bool_point_diff_warr, UP_AT_HALF)


# In[ ]:




