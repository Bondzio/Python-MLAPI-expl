#!/usr/bin/env python
# coding: utf-8

# # Data set cleaning and game prediction
# 
# This is my first kernel. Therefore I still got to learn a lot of interesting things and please give me your feedback. Thank you for this very large data set to play with.  
# 
# 
# I want to predict the results of the NBA games in the 2017-2018 season. I will use a simple technique: the moving average. **_"Offense wins games but defense wins championchips"_** that's why we just take into account the regular season and predict the points which will be scored. To predict the scored points we will use the field goal attempts which a team fires on the basket per game and combine this number of shots with their field goal percentage for 2 and 3 point shots. With this prediction method we are able to predict with 56% the right winning team.  
# 
# 
# Before we start predicting we have one important thing to do. The data set _"2012-18_officialBoxScore.csv"_ has **6 lines per game**. This is because both teams have for the same game a single line where they are named first and every game has 3 referees but the data set allows only one referee name per line. So this results in 2 x 3 (=6) lines per game in the data set. For the prediction we omit 5 lines per game so that we can work with one line per game.

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
print(os.listdir("../input"))


# In[ ]:


# load the data set in pandas
df = pd.read_csv("../input/2012-18_officialBoxScore.csv")


# # First Look
# 
# first look into the dataset and ideas and further evaluation

# In[ ]:


df.shape


# we have 44.284 lines in the dataset and 119 features for our analysis

# In[ ]:


pd.set_option('display.max_columns', 130) # we want to see all 119 columns in the output
df.head(6)


# In[ ]:


df.tail(6)


# # Data set cleaning
# 
# which points we have to clarify in this section:  
# * as you can see above we have 3 times the same line (the different officials are responsible that there are 3 lines). This is not important for our analysis. Therefore we will delete those lines
# * you can see above that additionally to the 3 lines corresponding to different officials there a 3 more lines where just the teamAbbr and opptAbbr is switched. We want one line in our data frame per game. We will delete those lines, too. 

# we just keep a few columns which we use or could use in further investigations

# In[ ]:


df = df[["gmDate","gmTime", "seasTyp", "teamAbbr", "teamRslt", "teamPTS", "teamFGA", "teamFGM", "teamFG%", 
        "team2PA", "team2PM", "team2P%", "team3PA", "team3PM", "team3P%", "teamFTA", "teamFTM", "teamFT%", "teamPPS", 
        "opptAbbr", "opptRslt", "opptPTS", "opptFGA", "opptFGM", "opptFG%", "oppt2PA", "oppt2PM",
        "oppt2P%", "oppt3PA", "oppt3PM", "oppt3P%", "opptFTA", "opptFTM", "opptFT%", "opptPPS"]]


# * transfer the column gmDate to a datetime data type. Then sort the column gmDate.  
# * We use in our analysis the season 2017/2018
# * the Season started on 2017-10-18 with the Cavaliers vs. the Celtics and the regular season ended on 2018-04-11. We saw above that the end of our data frame already shows the expected end date. 

# In[ ]:


df["gmDate"] = pd.to_datetime(df["gmDate"])
#df.dtypes
df = df.sort_values("gmDate")

df = df[df["gmDate"]>"2017-10-17"]

df.head()

# set the index new
df = df.reset_index(drop=True)

#df.head()
#df.tail()


# just check whether only season games are included. This should be the case as we selected the corresponding dates.

# In[ ]:


df.seasTyp.unique()


# Because we don't use the referees in our dataframe and already disregard the corresponding columns we now have a lot of lines in our dataset which are the same. We now delete them:  

# In[ ]:


df = df.drop_duplicates()
df.shape


# Now we have all the redundant information caused by the referees deleted out of our data frame.  
# 
# 
# In the next step we need to delete all the redundant information in the data frame which is caused by that for every game exists one row in the data where the home team is mentioned first and one row where the away team is mentioned first.  
# 
# We go through every row in the data set and check whether *game date = game date* and *team = opponent*. We store all double lines in a list and then delete them all.

# In[ ]:


line_counter = 0
drop_list = []

for line_counter in range(0, len(df.index)):
    for delete_line_counter in range(line_counter+1, len(df.index)):
        # compare same date and teamAbbr must be the same as opptAbbr
        if df.iloc[line_counter, 0] == df.iloc[delete_line_counter, 0] and df.iloc[line_counter, 3] == df.iloc[delete_line_counter, 19]:
            drop_list.append(delete_line_counter)
            break
            
            
#print(drop_list)


# Now let's drop every line out of drop_list and show us the shape and the head of the dataframe. We can see the adjusted number of lines. Addtionally we now should a have the desired dataframe with one line per NBA game during the regular season.

# In[ ]:


df = df.drop(df.index[drop_list])
df.shape
df.head(10)


# where are NAs? -> no missing values in our dataframe -> perfect

# In[ ]:


df.isnull().values.any()


# # Prediction
# 
# set the new index -> so that we can iterate through the dataset again (make sure that it is sorted for gmDate ascending)

# In[ ]:


# sort values with the help of game date
df = df.sort_values("gmDate")

# set the index new
df = df.reset_index(drop=True)

df.head()


# In[ ]:


# which teams we have in the NBA 2018/ 2019 season?
teams = df.teamAbbr.unique()
print(teams)


# In[ ]:


# let's prepare the dictionaries before using them

two_fga = {} # 2 point field goal attempts
three_fga = {} # 3 point field goal attempts
two_pfg_perc = {} # 2 point field goal percentage
three_pfg_perc = {} # 3 point field goal percentage

# set up the two_fga dictionary
for team in teams:
    if team not in two_fga:
        two_fga[team] = []

# set up the three_fga dictionary
for team in teams:
    if team not in three_fga:
        three_fga[team] = []
        
# set up the two_pfg_perc dictionary
for team in teams:
    if team not in two_pfg_perc:
        two_pfg_perc[team] = []
        
# set up the three_pfg_perc dictionary
for team in teams:
    if team not in three_pfg_perc:
        three_pfg_perc[team] = []

        
# e.g. the two_fga dictionary contains all teams as the key with an empty list
print(two_fga)


# ## Here we start actually the prediction.  
# **Concept:** We use the average 2 Point field goal attempts of the last 5 games and multiply them with the average of the 2 point field goal percentage of the last 5 games. Then we multiply with 2 to get the predicted 2 point field goals. Accordingly we will do this for the 3 point shots.

# In[ ]:


df.shape # take a look how many lines/ rows we have

line_counter = 0
k = 5 # number of games which we like to use for the average

for line_counter in range(0, len(df.index)):
    first_team = df.loc[line_counter, "teamAbbr"]
    second_team = df.loc[line_counter, "opptAbbr"]
    if len(two_fga[first_team]) == k and len(two_fga[second_team]) == k:
        # Prediction
        # Points first team
        pred_2P_first_team = np.mean(two_fga[first_team]) * np.mean(two_pfg_perc[first_team]) * 2
        pred_3P_first_team = np.mean(three_fga[first_team]) * np.mean(three_pfg_perc[first_team]) * 3
        pred_points_first_team = pred_2P_first_team + pred_3P_first_team # predicted points first team
        df.loc[line_counter, "teamPTSpred"] = pred_points_first_team
        # Points second team
        pred_2P_second_team = np.mean(two_fga[second_team]) * np.mean(two_pfg_perc[second_team]) * 2
        pred_3P_second_team = np.mean(three_fga[second_team]) * np.mean(three_pfg_perc[second_team]) * 3
        pred_points_second_team = pred_2P_second_team + pred_3P_second_team # predicted points second team
        df.loc[line_counter, "opptPTSpred"] = pred_points_second_team
        # prediction right or wrong
        if pred_points_first_team > pred_points_second_team and df.loc[line_counter, "teamPTS"] > df.loc[line_counter, "opptPTS"]:
            df.loc[line_counter, "predRslt"] = 1
        elif pred_points_first_team < pred_points_second_team and df.loc[line_counter, "teamPTS"] < df.loc[line_counter, "opptPTS"]:
            df.loc[line_counter, "predRslt"] = 1
        else:
            df.loc[line_counter, "predRslt"] = 0
        
        # delete oldest entry for prediction
        del two_fga[first_team][-1]
        del three_fga[first_team][-1]
        del two_pfg_perc[first_team][-1]
        del three_pfg_perc[first_team][-1]
        del two_fga[second_team][-1]
        del three_fga[second_team][-1]
        del two_pfg_perc[second_team][-1]
        del three_pfg_perc[second_team][-1]
    # collect data for average calculation
    if len(two_fga[first_team]) < k:
        # write data for first team
        two_fga[first_team].append(df.loc[line_counter, "team2PA"])
        three_fga[first_team].append(df.loc[line_counter, "team3PA"])
        two_pfg_perc[first_team].append(df.loc[line_counter, "team2P%"])
        three_pfg_perc[first_team].append(df.loc[line_counter, "team3P%"])
    if len(two_fga[second_team]) < k:
        # write data second_team
        two_fga[second_team].append(df.loc[line_counter, "oppt2PA"])
        three_fga[second_team].append(df.loc[line_counter, "oppt3PA"])
        two_pfg_perc[second_team].append(df.loc[line_counter, "oppt2P%"])
        three_pfg_perc[second_team].append(df.loc[line_counter, "oppt3P%"])        


# We can see in the last three columns the number of points we predicted for the "team" and the "opponent" and in the column "predRslt" whether our prediction of the winning team was right (=1) or wrong (=0)

# In[ ]:


df.tail()


# Below we see that in some rows our new created columns have a NA value. This happens because we need for every team 5 games to fill our dicitionaries with the data from the first games.

# In[ ]:


df.isna().sum()


# In[ ]:


number_learn = df["predRslt"].isna().sum() # how many games we couldn't predict because of learning -> 79
number_right = df["predRslt"].sum() # how many games we predicted right
rows = len(df.index)
perc_right_pred = number_right / (rows - number_learn)
print(perc_right_pred)


# 56% isn't that bad. Better than a coin flip ;)

# # Further investigation
# 
# Now let's take one step further to see which teams got the most right predictions.

# In[ ]:


# load the standing data set in pandas
standings = pd.read_csv("../input/2012-18_standings.csv")


# In[ ]:


standings.tail()


# so the last stadings reported are from the 2018-04-11 this was the ending of the regular season. So this is perfect. It is the date until we predicted the game outcomes. Let's concentrate on that date.

# In[ ]:


standings = standings[standings["stDate"]=="2018-04-11"]
standings = standings.sort_values(by="gameWon", ascending=False) # sorted by "gameWon" because the rank is per conference

display(standings)


# to be continued
