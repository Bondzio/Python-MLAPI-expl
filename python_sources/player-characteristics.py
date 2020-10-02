#!/usr/bin/env python
# coding: utf-8

# #Initialization
# 
# In this piece of code, the required packages are imported. Furthermore, the connection with the database is established and some methods are created for later use.

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import sqlite3

conn = sqlite3.connect('../input/database.sqlite')
c = conn.cursor()

def age_player_weeks (dob, extr_date):
    # cast dates from string to datetime
    dob = datetime.strptime(dob, '%Y-%m-%d %H:%M:%S')
    extr_date = datetime.strptime(extr_date, '%Y-%m-%d %H:%M:%S')
    
    # Subtract the date of birth from the extract date to obtain the age in days
    return (extr_date - dob).days

def prep_player_data (df):
    work_rate_dict = {'low': 0, 'medium': 1, 'high': 2}
    pref_foot_dict = {'left': 0, 'right': 1, 'None': 2}

    df = df.loc[(df['attacking_work_rate'].isin(work_rate_dict.keys())) & 
                (df['defensive_work_rate'].isin(work_rate_dict.keys()))].copy()
    
    df.loc[:, 'preferred_foot'] = df.loc[:, 'preferred_foot'].map(pref_foot_dict)
    df.loc[:, 'attacking_work_rate'] = df.loc[:, 'attacking_work_rate'].map(work_rate_dict)
    df.loc[:, 'defensive_work_rate'] = df.loc[:, 'defensive_work_rate'].map(work_rate_dict)
    
    columns = ['potential', 'preferred_foot', 'attacking_work_rate', 'defensive_work_rate',
              'crossing', 'finishing', 'heading_accuracy', 'short_passing', 'volleys', 
              'dribbling', 'curve', 'free_kick_accuracy', 'long_passing', 'ball_control',
              'acceleration', 'sprint_speed', 'agility', 'reactions', 'balance', 'shot_power',
              'jumping', 'stamina', 'strenght', 'long_shots', 'aggression', 'interceptions',
              'positioning', 'vision', 'penalties', 'marking', 'standing_tackle', 'sliding_tackle',
              'gk_diving', 'gk_handling', 'gk_kicking', 'gk_positioning', 'gk_reflexes', 'player_api_id']
    df = df.loc[:, player_data.columns.isin(columns)]
    
    return df

def nearest(items, given):
    return min(items, key=lambda x: abs(x - given))


# #Test connection & explore data
# 
# In this piece of code, the connection with the database is checked and the first data is extracted from the database. Furthermore, the format of the data is checked.

# In[ ]:


from datetime import datetime

# Obtain player information
dtypes = {'player_api_id': np.int16, 'overall_rating': np.int16, 
          'potential' : np.int16, 'preferred_foot': np.int16, 
          'attacking_work_rate': np.int16, 'defensive_work_rate': np.int16, 
          'crossing': np.int16, 'finishing': np.int16, 
          'heading_accuracy': np.int16, 'short_passing': np.int16, 
          'volleys': np.int16, 'dribbling': np.int16, 'curve': np.int16, 
          'free_kick_accuracy': np.int16, 'long_passing': np.int16, 
          'ball_control': np.int16, 'acceleration': np.int16, 'sprint_speed': np.int16, 
          'agility': np.int16, 'reactions': np.int16, 'balance': np.int16, 
          'shot_power': np.int16, 'jumping': np.int16, 'stamina': np.int16, 
          'strength': np.int16, 'long_shots': np.int16, 'aggression': np.int16, 
          'interceptions': np.int16, 'positioning': np.int16, 
          'vision': np.int16, 'penalties': np.int16, 'marking': np.int16, 
          'standing_tackle': np.int16, 'sliding_tackle': np.int16, 
          'gk_diving': np.int16, 'gk_handling': np.int16, 'gk_kicking': np.int16, 
          'gk_positioning': np.int16, 'gk_reflexes': np.int16, 'height': np.int16, 
          'weight': np.int16, 'birthday': np.str, 'date': np.str}
sql = """SELECT PA.player_api_id, overall_rating, potential, preferred_foot, attacking_work_rate, 
        defensive_work_rate, crossing, finishing, heading_accuracy,
        short_passing, volleys, dribbling, curve, free_kick_accuracy,
        long_passing, ball_control, acceleration, sprint_speed,
        agility, reactions, balance, shot_power, jumping, stamina,
        strength, long_shots, aggression, interceptions, positioning,
        vision, penalties, marking, standing_tackle, sliding_tackle,
        gk_diving, gk_handling, gk_kicking, gk_positioning,
        gk_reflexes, height, weight, P.birthday, PA.date
        FROM Player_Attributes PA INNER JOIN Player P ON PA.player_api_id = P.player_api_id"""
player_data = pd.read_sql_query(sql, conn)
player_data.dtype = dtypes

player_data['age'] = player_data.apply(lambda x: age_player_weeks(x['birthday'], x['date']), axis=1)
# Remove date columns
player_data = player_data.loc[:, player_data.columns != 'birthday']


# #Influence of age on player rating
# 
# This piece of code determines if there is any relationship between the age of a player and the overall rating established from the database. 

# In[ ]:


import matplotlib.pyplot as plt
num_bins = 40
bins = np.linspace(player_data['age'].min(), player_data['age'].max(), num_bins)
bin_labels = ['{0}-{1}'.format(int(x), int(y)) for x, y in zip(bins[:-1], bins[1:])]

player_data['bin'] = pd.cut(player_data['age'], bins, labels=np.arange(1, num_bins))
ratings = player_data.loc[:, ['bin', 'overall_rating', 'potential']].groupby('bin').mean()

best_player_id = player_data.loc[player_data['overall_rating'] == player_data['overall_rating'].max(), 
                                 'player_api_id'].iloc[0]
best_player = player_data.loc[player_data['player_api_id'] == best_player_id, 
                              ['bin', 'overall_rating', 'potential']].groupby('bin').mean()

fig, ax = plt.subplots(1, 1)
ax.plot(ratings.index.tolist(), ratings['overall_rating'], label='Mean rating')
ax.plot(ratings.index.tolist(), ratings['potential'], label='Mean potential')

ax.plot(best_player.index.tolist(), best_player['overall_rating'], 
        linestyle='-', label='Best player')
ax.plot(best_player.index.tolist(), best_player['potential'], 
        linestyle='-', label='Best player potential')

ax.xtick_labels = bin_labels
ax.set_title('Mean rating over time')
ax.set_xlabel('Age')
ax.set_ylabel('Mean rating')
ax.legend(loc='best')

bin_labels = [int(x/365) for x in bins if bins.tolist().index(x) in ax.get_xticks()] + [int(bins[-1]/365)]
ax.set_xticklabels(bin_labels, rotation=60)

# Remove bin column for later processing
player_data = player_data.loc[:, player_data.columns != 'bin']


# #Similar players
# 
# The next piece of code determines a similar player given the stats of a player. 

# In[ ]:


from sklearn.neighbors import NearestNeighbors

df = prep_player_data(player_data)

neig = NearestNeighbors(10)
neig = neig.fit(df.loc[:, df.columns != 'player_api_id'])
columns_fit = df.loc[:, df.columns != 'player_api_id'].columns

player_names = pd.read_sql_query('SELECT player_api_id, player_name FROM Player', conn)
rooney_id = player_names.loc[player_names['player_name'] == 'Wayne Rooney', 'player_api_id'].values[0]

data_rooney = df.loc[df['player_api_id'] == rooney_id, df.columns != 'player_api_id'].iloc[0].reshape(1, -1)

sim_players = neig.kneighbors(data_rooney)
sim_players = df.iloc[sim_players[-1][-1]]
print(player_names.loc[player_names['player_api_id'].isin(sim_players['player_api_id'])])


# #Player profiling

# In[ ]:


from sklearn.cluster import MeanShift, estimate_bandwidth

df = prep_player_data(player_data)
df.loc[:, df.columns != 'player_api_id'] = df.loc[:, df.columns != 'player_api_id'].apply(lambda x: (x - x.mean()) / x.mean(), axis=1)
#add age, weight, and height for clustering
df = pd.merge(df, player_data.loc[:, ['player_api_id', 'age', 'weight', 'height']], on='player_api_id')

band = estimate_bandwidth(df.loc[:, df.columns != 'player_api_id'].values, n_samples=20000, n_jobs=8)

ms = MeanShift(bandwidth=band, bin_seeding=True)
df['Cluster'] = ms.fit_predict(df.values)

#Add cluster labels to the player names
player_names = pd.merge(player_names, df.loc[:, ['player_api_id', 'Cluster']], on='player_api_id')


# In[ ]:


def replace_player_cluster(series):
    corr_player = player_names.loc[player_names['player_api_id'] == series['player_api_id']]
    closest_date = nearest(corr_player['date'], series['date'])
    cluster = corr_player.loc[player_names['date'] == closest_date, 'Cluster']
    return cluster

print(player_names.sample(5))
#home_team_goal, away_team_goal,

sql = """select home_team_goal-away_team_goal goal_diff,
         home_player_1, home_player_2, home_player_3, 
         home_player_4, home_player_5, home_player_6, 
         home_player_7, home_player_8, home_player_9, 
         home_player_10, home_player_11,
         away_player_1, away_player_2, away_player_3
         away_player_4, away_player_5, away_player_6
         away_player_7, away_player_8, away_player_9,
         away_player_10, away_player_11,
         date
         from match"""
match_data = pd.read_sql_query(sql, conn)

# replace player_api_id with cluster number
match_data = match_data.apply(lambda x: replace_player_cluster, axis=1)
print(match_data.sample(5))


# In[ ]:


print(player_data.columns)
print(player_data.loc[:, ['player_api_id', 'age', 'weight', 'height']])

