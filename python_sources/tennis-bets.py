#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
get_ipython().system('pip install xgboost')
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score


# #### Import data

# In[ ]:


path = "../input/atpdata/"
data = pd.read_csv(path + "ATP.csv")


# In[ ]:


data.head()


# In[ ]:


data.shape


# In[ ]:


data.info()


# ### Clean "Score" column

# In[ ]:


#The score column is the most important in this data set.
data["score"].isna().sum()


# In[ ]:


#We can delete the row with NaN score (0.1% of data)
#we will drop the rows with "W/O" score (0.43 % of data)
data_drop_nanScore = data.dropna(axis=0, subset=["score"])
data_drop_nanScore = data_drop_nanScore[data_drop_nanScore["score"] != 'W/O']
data_drop_nanScore = data_drop_nanScore[data_drop_nanScore["score"] != ' W/O']
data_drop_nanScore = data_drop_nanScore[data_drop_nanScore["score"] != 'DEF']
data_drop_nanScore = data_drop_nanScore[data_drop_nanScore["score"] != 'In Progress']
data_drop_nanScore = data_drop_nanScore[data_drop_nanScore["score"] != 'Walkover']
# we observed some scores having weird format (example 6-Feb)
#This line below is to drop them
expression = re.compile("\d+-[a-zA-Z]+")
weird_score = [x for x in data_drop_nanScore.score.values.tolist() if re.search(expression, x)]
for s in weird_score:
    data_drop_nanScore = data_drop_nanScore[data_drop_nanScore["score"] != s]  

# We kept ~99% of the initial data
display(data_drop_nanScore.shape)


# In[ ]:


#Using score column, let's compute the set won foreach player. the new columns will be: 
# l_setW and w_setW
def score_to_sets(score):
    
    """
    this function will compute l_setW, w_setW
    score: the game score
    return
    l_setW: set won by the loser
    w_setW: set won by the winner
    """
         
    #Correct some particular cases
    #score end with 'RET' or 'ABN' or 'ABD' ....
    if score[-3:] == 'RET' or score[-3:] == 'ABN'        or score[-3:] == 'DEF' or score[-3:] == 'ABD':
        score = score[:-4]
    if score[-21:] == "Played and unfinished": 
        score = score[:-22]
    if score[-20:] == "Played and abandoned": 
        score = score[:-21]    
    if score[-7:] == "Default":
        score = score[:-8]
    if score[-10:] == "Unfinished":
        score = score[:-11]
    
    l_setW, w_setW = 0, 0
    sets = score.split()
    for set_i in sets:
        #Deal with particular score (tie break)
        #exp: 3-6 7-6(5)
        if set_i[-1] == ")":
            # the 2 lines of code below ensure this cases:
            #    3-6 7-6(5)
            #    6-7(10) 7-5
            #    6-12(10) 7-5  12-6
            tie_break = set_i.split("(")
            tie_break = int(tie_break[1][:-1])
            #Theorically, it is possible to get tie_break > 100 but practically no
            if tie_break < 10:
                set_i = set_i[:-3]
            else:
                set_i = set_i[:-4]
        
        #Deal with particular score (example 7-6 1-6 [10-6])        
        if set_i[0] == "[":
            set_i = set_i[1:-1]
        set_i = set_i.split("-")
        if int(set_i[0]) > int(set_i[1]):
            w_setW += 1
        elif int(set_i[0]) < int(set_i[1]):
            l_setW += 1
        

    return l_setW, w_setW

sets_won = data_drop_nanScore["score"].apply(lambda x : score_to_sets(x) )


# In[ ]:


data_drop_nanScore["l_setW"] = sets_won.apply(lambda x: x[0])
data_drop_nanScore["w_setW"] = sets_won.apply(lambda x: x[1])
data_drop_nanScore.reset_index()


# In[ ]:


data_drop_nanScore.info()


# We have now 2 possibilities: \
# 1- Take all the rows and drop columns 1stIn, 1stWon, 2ndWon, SvGms, ace, bpFaced, bpSaved, df, svpt. \
# 2- Take ~50% of data rows (starting from ~1990) and keep all the columns. \
# 
# In this work, we will follow the second possibility for two reasons. The first is to have more features on each player. The second, even with 50% of the data, we still have 80000 rows. It is largely enough to do ML. (We can also test the first possibility in future work).

# In[ ]:


subset = [
    "l_1stIn", "l_1stWon", "l_2ndWon", "l_SvGms", "l_ace",
    "l_bpFaced", "l_bpSaved", "l_df", "l_svpt",
    "w_1stIn", "w_1stWon", "w_2ndWon", "w_SvGms", "w_ace",
    "w_bpFaced", "w_bpSaved", "w_df", "w_svpt"
    ]
data_drop_nanScore_cleaned = data_drop_nanScore.dropna(axis=0, subset=subset)


# In[ ]:


data_drop_nanScore_cleaned.info()


# ### I- Handling with missing Data

# In[ ]:


# We drop draw_size column. It is an empty column
data_drop_nanScore_cleaned = data_drop_nanScore_cleaned.drop(labels=["draw_size"], axis=1)


# ### Loser player columns

# #### loser_age

# In[ ]:


#loser_age: The best solutipon is to fill NaN values with the median.
# The column distribution agree with our choice
# loser_age before modification
n_Nan_l_age = data_drop_nanScore_cleaned.dropna(axis=0, subset=["loser_age"])["loser_age"]
plt.figure(figsize=(10,10))
sns.distplot(n_Nan_l_age)

# Fill Nan with the median
median_loser_age = n_Nan_l_age.median()
data_drop_nanScore_cleaned["loser_age"] = data_drop_nanScore_cleaned["loser_age"]                                          .fillna(median_loser_age)

# loser_age after modification (fillna)

sns.distplot(data_drop_nanScore_cleaned["loser_age"])
plt.legend(labels=['Before fillna','after fillna'])
plt.title("loser_age distribution")


# #### loser_entry

# In[ ]:


# We choose to drop loser_entry column (no clear method to fill nan values)
data_drop_nanScore_cleaned = data_drop_nanScore_cleaned.drop(labels=["loser_entry"], axis=1)


# #### loser_hand

# In[ ]:


data_drop_nanScore_cleaned["loser_hand"].value_counts()


# To fill loser_hand, we propose to see if we can find the hand, for the given player, in another game.

# In[ ]:


# Get the loser with nan loser_hand
nan_hand_names = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_hand"]                                           .isnull()]["loser_name"].unique()
print(nan_hand_names)

# See if the loser_hand is defined for another game
# when the player is a loser
for name in nan_hand_names:
    hands = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_name"] == name]["loser_hand"]
    if hands.isnull().all() == False:
        print("loser_hand founded for loser_name" + name)
# when the player is a winner
for name in nan_hand_names:
    hands = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_name"] == name]["winner_hand"]
    if hands.isnull().all() == False:
        print("loser_hand founded for winner_name" + name)


# The code above show 0 result. We propose to fill the NaN with R (Right handed is most frequent).
# This link as reference https://summerofjeff.wordpress.com/2011/02/12/the-prevalence-of-lefties-in-mens-tennis/ .
# We choose also to keep U value. We estimate that a player with U (N/A hand) is "unknown". The probability that he lose, is higher. This can help the predictive model to decide the winning player.

# In[ ]:


max_loser_hand = data_drop_nanScore_cleaned["loser_hand"].value_counts().idxmax()
data_drop_nanScore_cleaned["loser_hand"] = data_drop_nanScore_cleaned["loser_hand"]                                          .fillna(max_loser_hand)


# In[ ]:


data_drop_nanScore_cleaned["loser_hand"].value_counts()


# #### loser_ht

# In[ ]:


n_Nan_l_ht = data_drop_nanScore_cleaned.dropna(axis=0, subset=["loser_ht"])["loser_ht"]
plt.figure(figsize=(10,10))
sns.distplot(n_Nan_l_ht)


# In[ ]:


data_drop_nanScore_cleaned.describe()["loser_ht"]


# For loser_ht, we will proceed the same as loser_hand (try to find ht in another game)

# In[ ]:


# Get the loser with nan loser_ht
nan_ht_names = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_ht"]                                           .isnull()]["loser_name"].unique()
print(nan_ht_names)

# See if the loser_ht is defined for another game
# when the player is a loser
for name in nan_ht_names:
    ht = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_name"] == name]["loser_ht"]
    if ht.isnull().all() == False:
        print("loser_ht founded for loser_name" + name)
# when the player is a winner
for name in nan_hand_names:
    ht = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_name"] == name]["winner_ht"]
    if ht.isnull().all() == False:
        print("loser_ht founded for loser_name" + name)


# If a player have a Nan ht in a game, he will have Nan ht in all the games.\
# We will fill the  Nan ht with the mean.

# In[ ]:


data_drop_nanScore_cleaned["loser_ht"].mean()


# In[ ]:


mean_loser_ht = data_drop_nanScore_cleaned["loser_ht"].mean()
data_drop_nanScore_cleaned["loser_ht"] = data_drop_nanScore_cleaned["loser_ht"]                                          .fillna(mean_loser_ht)


# #### loser_rank

# The code below is to see if we can get the ranking from the given files. \
# We commented all the code except for one condition.\
# Ater running the code, we confirme that we can not fill the nan ranking using this method.

# In[ ]:


# Get the loser with nan loser_ht
nan_rank_id = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_rank"]                                           .isnull()]["loser_id"]
nan_rank_dates = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_rank"]                                           .isnull()]["tourney_date"]

# print(nan_rank_id)
# print(nan_rank_dates)


ranks = []
suffix = "atp_rankings_"

index = 0
for date in nan_rank_dates:
    id_player = nan_rank_id.to_list()[index]
    index = index + 1
    if int(str(date)[:4][-2:]) == 19:
        file_rank = path + suffix + "current.csv"
        df_rank = pd.read_csv(file_rank)
        df_rank = df_rank[df_rank["ranking_date"] == date]
        lst3 = [value for value in df_rank.player.to_list()]
        if (id_player in lst3):
            print("ok")

        
#     elif (year >= 10 
#         and year <=18):
#         file_rank = path + suffix + "10s.csv"
        
#     elif (year >= 0
#         and year <= 9):   
#         file_rank = path + suffix + "00s.csv"

#     elif (year >= 90
#         and year <= 99):
#         file_rank = path + suffix + "90s.csv"

#     elif (year >= 80
#           and year <= 89):
#         file_rank = path + suffix + "80s.csv"

#     elif (year >= 70
#         and year <= 79):
#         file_rank = path + suffix + "70s.csv"


# We didn't succed to fill the NaN ranks using the methd above.\
# As the Nan ranks are for unranked players, We propose to affect  "max(l_rank) + 1" to the first nan rank, "max(l_rank) + 2" to the second nan rank , and so on.

# In[ ]:


n_Nan_l_rank = data_drop_nanScore_cleaned.dropna(axis=0, subset=["loser_rank"])["loser_rank"]
plt.figure(figsize=(10,10))
sns.distplot(n_Nan_l_rank)


# In[ ]:


n_Nan_l_rank.describe()


# In[ ]:


add = 0
for index in nan_rank_id.index:
    data_drop_nanScore_cleaned.at[index, "loser_rank"] = n_Nan_l_rank.max() + add
    add = add + 1 


# In[ ]:


plt.figure(figsize=(10,10))
sns.distplot(data_drop_nanScore_cleaned["loser_rank"])


# #### loser_rank_points

# In[ ]:


n_Nan_l_rank_points = data_drop_nanScore_cleaned.dropna(axis=0, subset=["loser_rank_points"])["loser_rank_points"]
plt.figure(figsize=(10,10))
sns.distplot(n_Nan_l_rank_points)


# In[ ]:


n_Nan_l_rank_points.describe()


# In[ ]:


nan_rank_points_id = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_rank_points"]                                           .isnull()]["loser_id"]


# In[ ]:


len(nan_rank_points_id)


# In[ ]:


len(nan_rank_id)


# In[ ]:


# let's see if the player is unranked, he have a nan rank points
inter = nan_rank_id[nan_rank_id.isin(nan_rank_points_id)]
print((inter == nan_rank_id).sum())


# We see clearly that all the unraked players haven't rank points. We propose to fill this nan points with zero.

# In[ ]:


nan_rank_points_id.shape


# In[ ]:


print(nan_rank_points_id.shape)
for index in nan_rank_id.index:
    data_drop_nanScore_cleaned.at[index, "loser_rank_points"] = 0
print(data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_rank_points"]                                           .isnull()]["loser_id"].shape)


# For the rest of nan rank points, we propose to fill them with the average of "last_rank_points" and "future_rank_points" for a given player (the date is t). \
# > last_rank_points : the first valid rank points on t-i (i > 0).\
# > future_rank_points : the first valid rank points on t+i (i > 0

# In[ ]:


new_nan_rank_points_id = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_rank_points"]                                           .isnull()]["loser_id"]
new_nan_rank_points_rank = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_rank_points"]                                           .isnull()]["loser_rank"]
nan_rank_points_dates = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_rank_points"]                                           .isnull()]["tourney_date"]
nan_rank_points_seeds = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_rank_points"]                                           .isnull()]["loser_seed"]


# In[ ]:


index = 0
points = []
for date in nan_rank_points_dates:
#     date = 19910204
    print(date)
    id_player = new_nan_rank_points_id.to_list()[index]
#     id_player = 101723
    print(id_player)
    # games and dates when the player lose and win
    df_player = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_id"] == id_player]
    df_player_winner = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_id"] == id_player]
    print(df_player.shape)
    df_dates = df_player["tourney_date"].to_list()
    df_dates_winner = df_player_winner["tourney_date"].to_list()
    # seperate the date in loser/winner and last/future
    df_dates_last = [d for d in df_dates if d < date]
    df_dates_last_winner = [d for d in df_dates_winner if d < date]
    df_dates_future = [d for d in df_dates if d > date]
    df_dates_future_winner = [d for d in df_dates_winner if d > date]
    print("****dates*******")
#     print(df_dates)
#     print(df_dates_last)
#     print(df_dates_last_winner)
#     print(df_dates_future)
#     print(df_dates_future_winner)
    
    
    loser_points_last = 0
    winner_points_last = 0
    loser_points_future = 0
    winner_points_future = 0
    # get the nearest points from the actual date 
    for d in df_dates_last[::-1]:
        if len(df_dates_last) > 0:
            loser_points_last = df_player[df_player["tourney_date"]                                               == d]["loser_rank_points"]
            if (loser_points_last.last_valid_index()):
                break
        
    for d in df_dates_last_winner[::-1]:
        if len(df_dates_last_winner) > 0:
            winner_points_last = df_player_winner[df_player_winner["tourney_date"]                                               == d]["winner_rank_points"]         
            if  (winner_points_last.last_valid_index()):
                break
                
    for d in df_dates_future:
        if len(df_dates_future) > 0:
            loser_points_future = df_player[df_player["tourney_date"]                                               == d]["loser_rank_points"]
            if (loser_points_future.first_valid_index()):
                break
            
    for d in df_dates_future_winner:
        if len(df_dates_future_winner) > 0:
            winner_points_future = df_player_winner[df_player_winner["tourney_date"]                                               == d]["winner_rank_points"]
            if (winner_points_future.first_valid_index()):
                break
    
    print("******** points * *******")      
    print(loser_points_last)
    print(winner_points_last)
    print(loser_points_future)
    print(winner_points_future)
    
    # handle the situation when the dataFrame is all NaN values          
    if (type(loser_points_last) != int)         and not(loser_points_last.last_valid_index()):
        loser_points_last = 0
    if (type(winner_points_last) != int)         and not(winner_points_last.last_valid_index()):
        winner_points_last = 0
    if (type(loser_points_future) != int)         and not(loser_points_future.first_valid_index()):
        loser_points_future = 0
    if (type(winner_points_future) != int)         and not(winner_points_future.first_valid_index()):
        winner_points_future = 0
    
    
    # get the ids of the points
    id_loser_last = 0
    if type(loser_points_last) != int: 
        id_loser_last = loser_points_last.last_valid_index()
    id_winner_last = 0
    if type(winner_points_last) != int: 
        id_winner_last = winner_points_last.last_valid_index()
    id_loser_future = 0
    if type(loser_points_future) != int: 
        id_loser_future = loser_points_future.first_valid_index()
    id_winner_future = 0
    if type(winner_points_future) != int: 
        id_winner_future = winner_points_future.first_valid_index()
    
    print("******ids****")
    print(id_loser_last)
    print(id_winner_last)
    print(id_loser_future)
    print(id_winner_future)
    
    # chose last/future , loser/winner points based on the id (undirectly to the date)
    point_last = 0
    if id_loser_last > 0 and id_winner_last > 0:
        if id_loser_last < id_winner_last:
            point_last = winner_points_last[id_winner_last]
        else:
            point_last = loser_points_last[id_loser_last]
    elif id_loser_last == 0 and id_winner_last != 0:
        point_last = winner_points_last[id_winner_last]
    elif id_loser_last != 0 and id_winner_last == 0:
            point_last = loser_points_last[id_loser_last]
            
    point_future = 0
    if id_loser_future > 0 and id_winner_future > 0:
        if id_loser_future < id_winner_future:
            point_future = loser_points_future[id_loser_future]
        else:
            point_future = winner_points_future[id_winner_future]
    elif id_loser_future == 0 and id_winner_future != 0:
        point_future = winner_points_future[id_winner_future]
    elif id_loser_future != 0 and id_winner_future == 0:
            point_future = loser_points_future[id_loser_future]
        
    print("******point result*******")
    print(point_last)
    print(point_future)
    # if we have two values, we return the average, else we return the non zero value 
    # else return zero
    if(point_last == 0):
        points.append(point_future)
    elif(point_future == 0):
        points.append(point_last)
    else:
        points.append((point_last + point_future) / 2.0)
    
    index += 1
#     break


# In[ ]:


p = 0
for index in new_nan_rank_points_id.index:
#     print(index)
    data_drop_nanScore_cleaned.at[index, "loser_rank_points"] = points[p]
    p += 1
print(data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_rank_points"]                                           .isnull()]["loser_id"].shape)


# In[ ]:


plt.figure(figsize=(10,10))
sns.distplot(data_drop_nanScore_cleaned["loser_rank_points"])


# #### loser_seed

# We move now to the column "loser_seed". Despite her big imporatnce for betting, we fill ourself forced to drop this column.

# In[ ]:


print(data_drop_nanScore_cleaned["loser_seed"].isnull().sum())
data_drop_nanScore_cleaned = data_drop_nanScore_cleaned.drop(labels=["loser_seed"], axis=1)


# #### match_num

# The match_num column showed some biased values. It is due to the approch taken to identify a match in a tourney. It is possible to unbias this column. Due to lack of time, we will simply drop this column. 

# In[ ]:


plt.figure(figsize=(10,10))
sns.distplot(data_drop_nanScore_cleaned["match_num"])


# In[ ]:


data_drop_nanScore_cleaned = data_drop_nanScore_cleaned.drop(labels=["match_num"], axis=1)


# #### minutes

# For the "minutes" column, we will fill it with the mean(). We can enhance the approximation by do a splitting based on number of set played. 

# In[ ]:


n_Nan_minutes = data_drop_nanScore_cleaned.dropna(axis=0, subset=["minutes"])["minutes"]
plt.figure(figsize=(10,10))
sns.distplot(n_Nan_minutes)

# Fill Nan with the median
mean_minutes = n_Nan_minutes.mean()
data_drop_nanScore_cleaned["minutes"] = data_drop_nanScore_cleaned["minutes"]                                          .fillna(mean_minutes)


# ### Winner player columns

# To handle the missing values for the winner_player, we will exactly the same. It is better to have a clean code. In this work, we will do just a copy of the code above and do the modifications (loser -> winner)

# In[ ]:


data_drop_nanScore_cleaned.info()


# #### winner_age

# In[ ]:


#winner_age: The best solutipon is to fill NaN values with the median.

n_Nan_w_age = data_drop_nanScore_cleaned.dropna(axis=0, subset=["winner_age"])["winner_age"]
plt.figure(figsize=(10,10))
sns.distplot(n_Nan_w_age)

# Fill Nan with the median
median_winner_age = n_Nan_w_age.median()
data_drop_nanScore_cleaned["winner_age"] = data_drop_nanScore_cleaned["winner_age"]                                          .fillna(median_winner_age)

# loser_age after modification (fillna)

sns.distplot(data_drop_nanScore_cleaned["winner_age"])
plt.legend(labels=['Before fillna','after fillna'])
plt.title("winner_age distribution")


# #### winner_entry

# In[ ]:


# We choose to drop loser_entry column (no clear method to fill nan values)
data_drop_nanScore_cleaned = data_drop_nanScore_cleaned.drop(labels=["winner_entry"], axis=1)


# #### winner_hand

# In[ ]:


data_drop_nanScore_cleaned["winner_hand"].value_counts()


# In[ ]:


# Get the loser with nan loser_hand
nan_hand_names = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_hand"]                                           .isnull()]["winner_name"].unique()
print(nan_hand_names)

# See if the winner_hand is defined for another game
# when the player is a loser
verify_name = []
for name in nan_hand_names:
    hands = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_name"] == name]["loser_hand"]
    if hands.isnull().all() == False:
        verify_name.append(name)
        print("loser_hand founded for winner_name" + name)
# when the player is a winner
for name in nan_hand_names:
    hands = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_name"] == name]["winner_hand"]
    if hands.isnull().all() == False:
        verify_name.append(name)
        print("loser_hand founded for winner_name" + name)


# In[ ]:


# affect to players in verify_name the mean_loser_ht
for name in verify_name:
    for row_index in data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_name"] == name].index:
        data_drop_nanScore_cleaned.loc[row_index,'winner_hand'] = "R"


# In[ ]:


max_winner_hand = data_drop_nanScore_cleaned["winner_hand"].value_counts().idxmax()
data_drop_nanScore_cleaned["winner_hand"] = data_drop_nanScore_cleaned["winner_hand"]                                          .fillna(max_winner_hand)


# In[ ]:


data_drop_nanScore_cleaned["winner_hand"].value_counts()


# #### winner_ht

# In[ ]:


n_Nan_w_ht = data_drop_nanScore_cleaned.dropna(axis=0, subset=["winner_ht"])["winner_ht"]
plt.figure(figsize=(10,10))
sns.distplot(n_Nan_w_ht)


# In[ ]:


data_drop_nanScore_cleaned.describe()["winner_ht"]


# In the Loser part, we already affected height to some player. We have to ensure that they will have the height as a loser or a winner.

# In[ ]:


# Get the loser with nan loser_ht
nan_ht_names = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_ht"]                                           .isnull()]["winner_name"].unique()
print(nan_ht_names)

# See if the loser_ht is defined for another game
# when the player is a loser
# save in verify_name, the players that already have a ht
verify_name = []
for name in nan_ht_names:
    ht = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_name"] == name]["loser_ht"]
    if ht.isnull().all() == False:
#         print(ht)
        verify_name.append(name)
        print("loser_ht founded for winner_name " + name)
# when the player is a winner
for name in nan_hand_names:
    ht = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_name"] == name]["winner_ht"]
    if ht.isnull().all() == False:
        verify_name.append(name)
        print("winner_ht founded for winner_name " + name)


# In[ ]:


# affect to players in verify_name the mean_loser_ht
for name in verify_name:
    for row_index in data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_name"] == name].index:
        data_drop_nanScore_cleaned.loc[row_index,'winner_ht'] = mean_loser_ht


# In[ ]:


mean_winner_ht = data_drop_nanScore_cleaned["winner_ht"].mean()
data_drop_nanScore_cleaned["winner_ht"] = data_drop_nanScore_cleaned["winner_ht"]                                          .fillna(mean_winner_ht)


# #### winner_rank

# In[ ]:


# Get the loser with nan loser_ht
nan_rank_id = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_rank"]                                           .isnull()]["winner_id"]
nan_rank_dates = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_rank"]                                           .isnull()]["tourney_date"]

# print(nan_rank_id)
# print(nan_rank_dates)


ranks = []
suffix = "atp_rankings_"

index = 0
for date in nan_rank_dates:
    id_player = nan_rank_id.to_list()[index]
    index = index + 1
    if int(str(date)[:4][-2:]) == 19:
        file_rank = path + suffix + "current.csv"
        df_rank = pd.read_csv(file_rank)
        df_rank = df_rank[df_rank["ranking_date"] == date]
        lst3 = [value for value in df_rank.player.to_list()]
        if (id_player in lst3):
            print("ok")

        
#     elif (year >= 10 
#         and year <=18):
#         file_rank = path + suffix + "10s.csv"
        
#     elif (year >= 0
#         and year <= 9):   
#         file_rank = path + suffix + "00s.csv"

#     elif (year >= 90
#         and year <= 99):
#         file_rank = path + suffix + "90s.csv"

#     elif (year >= 80
#           and year <= 89):
#         file_rank = path + suffix + "80s.csv"

#     elif (year >= 70
#         and year <= 79):
#         file_rank = path + suffix + "70s.csv"


# In[ ]:


n_Nan_w_rank = data_drop_nanScore_cleaned.dropna(axis=0, subset=["winner_rank"])["winner_rank"]
plt.figure(figsize=(10,10))
sns.distplot(n_Nan_w_rank)


# In[ ]:


n_Nan_w_rank.describe()


# In[ ]:


add = 0
for index in nan_rank_id.index:
    data_drop_nanScore_cleaned.at[index, "winner_rank"] = n_Nan_w_rank.max() + add
    add = add + 1 


# In[ ]:


plt.figure(figsize=(10,10))
sns.distplot(data_drop_nanScore_cleaned["winner_rank"])


# #### winner_rank_points

# In[ ]:


n_Nan_w_rank_points = data_drop_nanScore_cleaned.dropna(axis=0, subset=["winner_rank_points"])["winner_rank_points"]
plt.figure(figsize=(10,10))
sns.distplot(n_Nan_w_rank_points)


# In[ ]:


n_Nan_w_rank_points.describe()


# In[ ]:


nan_rank_points_id = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_rank_points"]                                           .isnull()]["winner_id"]


# In[ ]:


len(nan_rank_points_id)


# In[ ]:


len(nan_rank_id)


# In[ ]:


# let's see if the player is unranked, he have a nan rank points
inter = nan_rank_id[nan_rank_id.isin(nan_rank_points_id)]
print((inter == nan_rank_id).sum())


# In[ ]:


nan_rank_points_id.shape


# In[ ]:


print(nan_rank_points_id.shape)
for index in nan_rank_id.index:
    data_drop_nanScore_cleaned.at[index, "winner_rank_points"] = 0
print(data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_rank_points"]                                           .isnull()]["winner_id"].shape)


# In[ ]:


new_nan_rank_points_id = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_rank_points"]                                           .isnull()]["winner_id"]
new_nan_rank_points_rank = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_rank_points"]                                           .isnull()]["winner_rank"]
nan_rank_points_dates = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_rank_points"]                                           .isnull()]["tourney_date"]
nan_rank_points_seeds = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_rank_points"]                                           .isnull()]["winner_seed"]


# In[ ]:


index = 0
points = []
for date in nan_rank_points_dates:
#     date = 19910204
    print(date)
    id_player = new_nan_rank_points_id.to_list()[index]
#     id_player = 101723
    print(id_player)
    # games and dates when the player lose and win
    df_player = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["loser_id"] == id_player]
    df_player_winner = data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_id"] == id_player]
    print(df_player.shape)
    df_dates = df_player["tourney_date"].to_list()
    df_dates_winner = df_player_winner["tourney_date"].to_list()
    # seperate the date in loser/winner and last/future
    df_dates_last = [d for d in df_dates if d < date]
    df_dates_last_winner = [d for d in df_dates_winner if d < date]
    df_dates_future = [d for d in df_dates if d > date]
    df_dates_future_winner = [d for d in df_dates_winner if d > date]
    print("****dates*******")
#     print(df_dates)
#     print(df_dates_last)
#     print(df_dates_last_winner)
#     print(df_dates_future)
#     print(df_dates_future_winner)
    
    
    loser_points_last = 0
    winner_points_last = 0
    loser_points_future = 0
    winner_points_future = 0
    # get the nearest points from the actual date 
    for d in df_dates_last[::-1]:
        if len(df_dates_last) > 0:
            loser_points_last = df_player[df_player["tourney_date"]                                               == d]["loser_rank_points"]
            if (loser_points_last.last_valid_index()):
                break
        
    for d in df_dates_last_winner[::-1]:
        if len(df_dates_last_winner) > 0:
            winner_points_last = df_player_winner[df_player_winner["tourney_date"]                                               == d]["winner_rank_points"]         
            if  (winner_points_last.last_valid_index()):
                break
                
    for d in df_dates_future:
        if len(df_dates_future) > 0:
            loser_points_future = df_player[df_player["tourney_date"]                                               == d]["loser_rank_points"]
            if (loser_points_future.first_valid_index()):
                break
            
    for d in df_dates_future_winner:
        if len(df_dates_future_winner) > 0:
            winner_points_future = df_player_winner[df_player_winner["tourney_date"]                                               == d]["winner_rank_points"]
            if (winner_points_future.first_valid_index()):
                break
    
    print("******** points * *******")      
    print(loser_points_last)
    print(winner_points_last)
    print(loser_points_future)
    print(winner_points_future)
    
    # handle the situation when the dataFrame is all NaN values          
    if (type(loser_points_last) != int)         and not(loser_points_last.last_valid_index()):
        loser_points_last = 0
    if (type(winner_points_last) != int)         and not(winner_points_last.last_valid_index()):
        winner_points_last = 0
    if (type(loser_points_future) != int)         and not(loser_points_future.first_valid_index()):
        loser_points_future = 0
    if (type(winner_points_future) != int)         and not(winner_points_future.first_valid_index()):
        winner_points_future = 0
    
    
    # get the ids of the points
    id_loser_last = 0
    if type(loser_points_last) != int: 
        id_loser_last = loser_points_last.last_valid_index()
    id_winner_last = 0
    if type(winner_points_last) != int: 
        id_winner_last = winner_points_last.last_valid_index()
    id_loser_future = 0
    if type(loser_points_future) != int: 
        id_loser_future = loser_points_future.first_valid_index()
    id_winner_future = 0
    if type(winner_points_future) != int: 
        id_winner_future = winner_points_future.first_valid_index()
    
    print("******ids****")
    print(id_loser_last)
    print(id_winner_last)
    print(id_loser_future)
    print(id_winner_future)
    
    # chose last/future , loser/winner points based on the id (undirectly to the date)
    point_last = 0
    if id_loser_last > 0 and id_winner_last > 0:
        if id_loser_last < id_winner_last:
            point_last = winner_points_last[id_winner_last]
        else:
            point_last = loser_points_last[id_loser_last]
    elif id_loser_last == 0 and id_winner_last != 0:
        point_last = winner_points_last[id_winner_last]
    elif id_loser_last != 0 and id_winner_last == 0:
            point_last = loser_points_last[id_loser_last]
            
    point_future = 0
    if id_loser_future > 0 and id_winner_future > 0:
        if id_loser_future < id_winner_future:
            point_future = loser_points_future[id_loser_future]
        else:
            point_future = winner_points_future[id_winner_future]
    elif id_loser_future == 0 and id_winner_future != 0:
        point_future = winner_points_future[id_winner_future]
    elif id_loser_future != 0 and id_winner_future == 0:
            point_future = loser_points_future[id_loser_future]
        
    print("******point result*******")
    print(point_last)
    print(point_future)
    # if we have two values, we return the average, else we return the non zero value 
    # else return zero
    if(point_last == 0):
        points.append(point_future)
    elif(point_future == 0):
        points.append(point_last)
    else:
        points.append((point_last + point_future) / 2.0)
    
    index += 1
#     break


# In[ ]:


p = 0
for index in new_nan_rank_points_id.index:
#     print(index)
    data_drop_nanScore_cleaned.at[index, "winner_rank_points"] = points[p]
    p += 1
print(data_drop_nanScore_cleaned[data_drop_nanScore_cleaned["winner_rank_points"]                                           .isnull()]["winner_id"].shape)


# #### winner_seed

# In[ ]:


print(data_drop_nanScore_cleaned["winner_seed"].isnull().sum())
data_drop_nanScore_cleaned = data_drop_nanScore_cleaned.drop(labels=["winner_seed"], axis=1)


# ### II. Organize the data

# Now, we will reorganize our data in order to adapt to the problem. Our idea is to split the data in two loser_player and winner_player. We will give to the losers the target 0 and to the winners the taget 1. We will concatenate the two dataframes. It is about a classification problem in order to know on which player bet.

# In[ ]:


data_drop_nanScore_cleaned.tail()


# In[ ]:


#dataframe winner
columns_w = [
    "best_of", "w_1stIn", "w_1stWon", "w_2ndWon", "w_SvGms", "w_ace", "w_bpFaced", "w_bpSaved",
    "w_df", "w_svpt", "winner_age", "winner_hand", "winner_ht", "winner_id", "winner_ioc",
    "winner_name", "winner_rank", "winner_rank_points", "minutes", "round", "score",
    "surface", "tourney_date", "tourney_id", "tourney_level", "tourney_name", "w_setW"
    ]
df_w = data_drop_nanScore_cleaned[columns_w]
df_w["label"] = 1


# In[ ]:


# dataframe loser
df_l = data_drop_nanScore_cleaned.copy()
df_l = df_l.iloc[:,:26]
df_l["w_setW"] = data_drop_nanScore_cleaned["l_setW"]
df_l.columns = columns_w
df_l["label"] = 0


# In[ ]:


# players datafame
player_df = pd.concat([df_w, df_l], ignore_index=True)
player_df.head()


# ### III. Handle with categorical features

# In this part, we will work in the categorical features in order to transform them to numerical. We will do the necessary encodings. We will also drop some columns (unrelevant from our point of view).

# In[ ]:


player_df.dtypes


# In[ ]:


player_df["round"].value_counts()


# We will drop "RR" and "BR". We will get ordinal attributes

# In[ ]:


player_df = player_df[player_df["round"] != 'RR']
player_df = player_df[player_df["round"] != 'BR']


# In[ ]:


player_df["round"].value_counts()


# In[ ]:


round_num = {
    'round': {
        'R128': 0, 'R64': 1, 'R32': 2, 'R16': 3,
        'QF': 4, 'SF': 5, 'F': 6
        }
    }


# In[ ]:


player_df.replace(round_num, inplace=True)


# In[ ]:


player_df["round"].value_counts()


# We will drop column score (we undirectly have it in the label).

# In[ ]:


player_df.drop(["score"], axis=1, inplace=True)


# #### surface

# In[ ]:


player_df["surface"].value_counts()


# In[ ]:


from sklearn.preprocessing import LabelEncoder
lb = LabelEncoder()
player_df['surface'] = lb.fit_transform(player_df['surface'].astype(str))


# In[ ]:


player_df["surface"].value_counts()


# #### tourney_date, tourney_id and tounrney_name

# We will drop this columns.

# In[ ]:


player_df.drop(["tourney_date"], axis=1, inplace=True)
player_df.drop(["tourney_id"], axis=1, inplace=True)
player_df.drop(["tourney_name"], axis=1, inplace=True)


# #### tourney_level

# In[ ]:


player_df["tourney_level"].value_counts()


# In[ ]:


level_num = {
    'tourney_level': {
        'A': 0, 'F': 1, 'M': 2, 'G': 3
        }
    }


# In[ ]:


player_df.replace(level_num, inplace=True)


# In[ ]:


player_df["tourney_level"].value_counts()


# #### Winner_hand, winner_id, winner_name and winner_ioc

# In[ ]:


player_df["winner_hand"].value_counts()


# In[ ]:


lb_encoder = LabelEncoder()
player_df['winner_hand'] = lb_encoder.fit_transform(player_df['winner_hand'].astype(str))


# In[ ]:


player_df["winner_hand"].value_counts()


# In[ ]:


player_df.drop(["winner_id"], axis=1, inplace=True)
player_df.drop(["winner_name"], axis=1, inplace=True)


# In[ ]:


player_df["winner_ioc"].value_counts()


# In[ ]:


lb_encoder = LabelEncoder()
player_df['winner_ioc'] = lb_encoder.fit_transform(player_df['winner_ioc'].astype(str))


# In[ ]:


player_df["winner_ioc"].value_counts()


# #### w_setW

# We will delete also our created feature "w_setW". We will explain this in the Further work section.

# In[ ]:


player_df.drop(["w_setW"], axis=1, inplace=True)


# In[ ]:


player_df.dtypes


# ### IV. Vizualisation

# #### a- Correlation heatMap

# In[ ]:


corr = player_df.corr()
fig, ax = plt.subplots(figsize=(20, 20))
sns.heatmap(corr, annot= True, fmt='.2f', linewidths=0.5, ax=ax)


# The correlation matrix shows some high correlated features especially for "w_svpt". It is correlated to "w_1stIn", "w_1stWon", "w_2ndWon" and "w_SvGms". In this work, we will not drop the correlated features but we think that it can be tested in further work

# #### b- Age, ioc plot

# In[ ]:


df = player_df[["winner_age", "tourney_level", "winner_rank", "label"]]
df.columns = ["age", "tourney_level", "rank", "label"]
sns.pairplot(df, hue = "label", size=3 )


# <bold><u>__tourney_level x winner_age__</u></bold>: For level G (grand Shlam), the max is 40 but for level A it is 48. This can be explained by the facct that the oldest player join A level competition in the end of their professional career. \
# <bold><u>__tourney_level x winner_rank__</u></bold>: The first ranked players win the hardest tourney (G and M).\
# <bold><u>__winner_rank x winner_age__</u></bold>: We can seperate the plot in two parts, from  rank 0 to 1500 and from 1500 to 2500.
# For the first part, we have the shape of triangle => by the time (the age), the player win points and go higher in the rank. The second part can be explained by the entrance of new player in the ranking or by the end_career players.

# ### V- Prediction Models

# In[ ]:


player_df.head()


# ### a- Split Data 

# In[ ]:


X = player_df.drop(['label'],axis=1)
y = player_df["label"]
display(X.shape)
display(y.shape)


# In[ ]:


#Split train/test 90%-10%
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, stratify = y) #10%
#split raw data 
display(X_train.shape)
display(y_train.shape)


# #### b- Model1 : SVM

# In[ ]:


pipeline = Pipeline([
    ('scaler',MinMaxScaler()),
    ('svm', svm.SVC())
])


param_grid = {
    'svm__kernel': ['linear','rbf'],
    'svm__C':[1],
    'svm__gamma':[0.001]
}

cv = 2

svm_grid = GridSearchCV(pipeline, param_grid = param_grid, cv = cv, verbose=1, n_jobs = -1,scoring='f1')

svm_grid.fit(X_train, y_train)


# In[ ]:


svm_grid.best_score_


# In[ ]:


y_pred = svm_grid.predict(X_test)


# In[ ]:


f1_score(y_test, y_pred)


# In[ ]:


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = ["0", "1"]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax


# In[ ]:


# Plot non-normalized confusion matrix
plot_confusion_matrix(y_test, y_pred, classes=["class_names"],
                      title='Confusion matrix SVM')


# #### c- Model2: XGBoost

# In[ ]:


pipeline = Pipeline([
    ('scaler',MinMaxScaler()),
    ('xgb', XGBClassifier())
])


param_grid = {
    'xgb__max_depth': [4],
    'xgb__min_child_weight':[0.01],
    'xgb__colsample_bytree':[0.7],
    'xgb__subsample':[0.6],
    'xgb__learning_rate':[0.1]
}

cv = 2

xgb_grid = GridSearchCV(pipeline, param_grid = param_grid, cv = cv, verbose=1, n_jobs = -1,scoring='f1')

xgb_grid.fit(X_train, y_train)


# In[ ]:


xgb_grid.best_score_


# In[ ]:


y_pred = xgb_grid.predict(X_test)


# In[ ]:


f1_score(y_test, y_pred)


# In[ ]:


# Plot non-normalized confusion matrix
plot_confusion_matrix(y_test, y_pred, classes=["class_names"],
                      title='Confusion matrix XGBoost')


# #### d- Model3: Logistic Regression

# In[ ]:


pipeline = Pipeline([
    ('scaler',MinMaxScaler()),
    ('lr', LogisticRegression())
])


param_grid = {
    'lr__penalty' : ['l1', 'l2'],
    'lr__C' : [0.1]# np.logspace(-4, 4, 20)
}

cv = 2

lr_grid = GridSearchCV(pipeline, param_grid = param_grid, cv = cv, verbose=1, n_jobs = -1,scoring='f1')

lr_grid.fit(X_train, y_train)


# In[ ]:


lr_grid.best_score_


# In[ ]:


y_pred = lr_grid.predict(X_test)


# In[ ]:


f1_score(y_test, y_pred)


# In[ ]:


# Plot non-normalized confusion matrix
plot_confusion_matrix(y_test, y_pred, classes=["class_names"],
                      title='Confusion matrix Logistic Regression')


# ### VI- Further Work

# We hope that our approach was clear. In this section, we will present other ideas that can be more adapted to bettings. \
# 1. Clean the code.
# 2. Use sklearn imputers to handle the new (unseen) data.
# 3. Analyse features correlation and features selection.
# 4. Tune the models (modify the range of the parameters).
# 5. Combine the models.
# 6. Test a second approach based on Time Series Forecasting:
#     1. Build multiv-variate time series for each player.
#     2. Assign to each time-serie probability of winning a game or a set. We started this work by creating the feature "w_SetW".
#     3. For a new game, forecast/predict the probabilities for both players.
#     4. Bet on the player with higher probability.
