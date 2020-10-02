#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# #data exploration
# 
# **#world_cup_raw_data**
# #Year	Country	Winner	Runners-Up	Third	Fourth	GoalsScored	QualifiedTeams	MatchesPlayed	Attendance
# #	Year	Country	Winner	Runners-Up	Third	Fourth	GoalsScored	QualifiedTeams	MatchesPlayed	Attendance
# #0	1930	Uruguay	Uruguay	Argentina	USA	Yugoslavia	70	13	18	590.549
# #1	1934	Italy	Italy	Czechoslovakia	Germany	Austria	70	16	17	363.000
# #2	1938	France	Italy	Hungary	Brazil	Sweden	84	15	18	375.700
# #3	1950	Brazil	Uruguay	Brazil	Sweden	Spain	88	13	22	1.045.246
# #4	1954	Switzerland	Germany FR	Hungary	Austria	Uruguay	140	16	26	768.607
# **#world_cup_raw_data: data have organization, 20 rows( observations), 10 columns( characteristics), not have missing data**
# *##year: ordinal
# ##country: nominal
# ##Winner: nominal
# ##Runners-Up: second, nominal
# ##Third: nominal
# ##Fourth: nominal
# ##GoalsScored: ordinal
# ##QualifiedTeams: ordinal
# ##MatchesPlayed: ordinal
# ##Attendance: ordinal*

# In[ ]:


world_cup_raw_data= pd.read_csv("../input/WorldCups.csv")
world_cup_raw_data.head()


# In[ ]:


world_cup_raw_data.shape


# In[ ]:


world_cup_raw_data.isnull().sum()


# In[ ]:


world_cup_raw_data.describe()


# In[ ]:


world_cup_raw_data.hist()


# In[ ]:


import matplotlib.pyplot as plt
plt.figure(figsize=(5,5))
plt.scatter(world_cup_raw_data.Year,world_cup_raw_data.Country)


# In[ ]:


import matplotlib.pyplot as plt
plt.figure(figsize=(5,5))
plt.plot(world_cup_raw_data.Year,world_cup_raw_data.GoalsScored)


# In[ ]:


import matplotlib.pyplot as plt
plt.figure(figsize=(5,5))
plt.plot(world_cup_raw_data.Year,world_cup_raw_data.QualifiedTeams)


# In[ ]:


import matplotlib.pyplot as plt
plt.figure(figsize=(5,5))
plt.plot(world_cup_raw_data.Year,world_cup_raw_data.MatchesPlayed)


# In[ ]:


import matplotlib.pyplot as plt
plt.figure(figsize=(5,5))
plt.plot(world_cup_raw_data.Year,world_cup_raw_data.Attendance)


# In[ ]:





# ##data question: 
# top winner?-->Brazil( 5 times)
# top Runners-Up?-->Netherlands( 3 times)
# top Third?-->Germany( 3 times)
# top Fourth?-->Uruguay( 3 times)
# next winner can be Brazil?
# ##
# Country is Winner?-->Uruguay,Italy,England,Argentina,France
# Country is Runners-Up-->Brazil,Sweden
# Country is Third-->Chile,Italy,Germany
# Country is Fourth-->Brazil

# In[ ]:


world_cup_raw_data['Winner'].describe()


# In[ ]:


#winner and times
world_cup_raw_data.Winner.value_counts().plot(kind='bar')


# In[ ]:


world_cup_raw_data['Winner'].hist()


# In[ ]:


##point to the winner in year
import matplotlib.pyplot as plt
t=world_cup_raw_data.iloc[:,[0,2]]
plt.figure(figsize=(5,5))
plt.scatter(t.Year,t.Winner,color='red')
plt.show()


# In[ ]:





# In[ ]:


#what years that Brazil is Winner
brazil_winner=world_cup_raw_data[world_cup_raw_data['Winner']=='Brazil']
brazil_winner.Year.value_counts().plot(kind='bar')


# In[ ]:


#Country is Winner?
country_is_winner= world_cup_raw_data[(world_cup_raw_data['Winner']==world_cup_raw_data['Country'])]
country_is_winner


# In[ ]:


country_is_winner.Winner.value_counts().plot(kind='bar')


# In[ ]:


world_cup_raw_data['Runners-Up'].describe()


# In[ ]:


#country is runners-up
country_is_runnersup=world_cup_raw_data[(world_cup_raw_data['Runners-Up']==world_cup_raw_data['Country'])]
country_is_runnersup


# In[ ]:


country_is_runnersup.Country.value_counts().plot(kind='bar')


# In[ ]:


world_cup_raw_data['Third'].describe()


# In[ ]:


#country is third
country_is_third = world_cup_raw_data[(world_cup_raw_data['Third']==world_cup_raw_data['Country'])]
country_is_third


# In[ ]:


country_is_third.Country.value_counts().plot(kind='bar')


# In[ ]:


world_cup_raw_data['Fourth'].describe()


# In[ ]:


#country is fourth
country_is_fourth = world_cup_raw_data[(world_cup_raw_data['Fourth']==world_cup_raw_data['Country'])]
country_is_fourth


# In[ ]:


country_is_fourth.Country.value_counts().plot(kind='bar')


# #data exploration
# **#world_cup_matches_raw_data**
# #Year	Datetime	Stage	Stadium	City	Home Team Name	Home Team Goals	Away Team Goals	Away Team Name	Win conditions
# #Attendance	Half-time Home Goals	Half-time Away Goals	Referee	Assistant 1	Assistant 2	RoundID	MatchID	Home Team Initials	Away Team Initials
# **#world_cup_matches_raw_data: organization, 4572 rows( observation), 20 columns( characteristic), 3720 missing data rows**
# *##Year: ordinal
# ##Datatime: ordinal
# ##Stage: nominal
# ##Stadium: nominal
# ##City: nominal-->(count:852;unique:151;top:Mexico City;freq:23)
# ##HomTeamName: nominal
# ##HomeTeamGoals: ordinal
# ##AwayTeamGoals: ordinal
# ##AwayTeamName: nominal
# ##Winconditions: nominal
# ##Attendance: ordinal
# ##Half-timeHomeGoals: ordinal
# ##Half-timeAwayGoals: ordinal
# ##Referee: nominal
# ##Assistant 1,2: nominal
# ##RoundID: ordinal
# ##MatchID: ordinal
# ##HomeTeamInitials: nominal
# ##AwayTeamInitials: nominal*

# In[ ]:


world_cup_matches_raw_data= pd.read_csv("../input/WorldCupMatches.csv")
world_cup_matches_raw_data.head()


# In[ ]:


world_cup_matches_raw_data.shape


# In[ ]:


world_cup_matches_raw_data.isnull().sum()


# In[ ]:


world_cup_matches_raw_data.describe()


# In[ ]:


#drop 3722 missing data rows will condition "all missing columns"
#world_cup_matches_filter_data: 852 rows, Attendance column is missing 2 rows
world_cup_matches_filter_data= world_cup_matches_raw_data.dropna(how='all')
world_cup_matches_filter_data.describe()
world_cup_matches_filter_data.shape
world_cup_matches_filter_data.isnull().sum()
world_cup_matches_filter_data[world_cup_matches_filter_data['Attendance'].isnull()]


# In[ ]:


#first year winner is brasil 1958
brazil_winner_1958= world_cup_matches_filter_data[world_cup_matches_filter_data.Year==1958]
brazil_winner_1958[(brazil_winner_1958['Home Team Name']=='Brazil') | (brazil_winner_1958['Away Team Name']=='Brazil')]


# #data exploration
# #RoundID	MatchID	Team Initials	Coach Name	Line-up	Shirt Number	Player Name	Position	Event
# #world_cup_players_raw_data: organization, 37784 rows( observation), 9 columns( characteristic), missing data(Position: 33641, Event: 28715)
# ##RoundID: ordinal
# ##MatchID: ordinal
# ##Team Initials: nominal
# ##Coach Name: nominal
# ##Line-up: nominal
# ##Shirt Number: ordinal
# ##Player Name: nominal
# ##Position: nominal
# ##Event: nominal

# In[ ]:


world_cup_players_raw_data= pd.read_csv("../input/WorldCupPlayers.csv")
world_cup_players_raw_data.head()


# In[ ]:


world_cup_players_raw_data.shape


# In[ ]:


world_cup_players_raw_data.isnull().sum()


# In[ ]:


world_cup_matches_raw_data.describe()


# In[ ]:


#MatchID 1343.0( final Brazill-Sweeden 1958)
#brazil players
world_cup_players_raw_data[(world_cup_players_raw_data['MatchID']==1343) & (world_cup_players_raw_data['Team Initials'] == 'BRA')]


# In[ ]:


#MatchID 1343.0( final Brazill-Sweeden 1958)
#sweeden players
world_cup_players_raw_data[(world_cup_players_raw_data['MatchID']==1343) & (world_cup_players_raw_data['Team Initials'] == 'SWE')]


# ##have no any story about this data, to be continued
# #years= world_cup_matches_raw_data['Year'].value_counts()
# #years.plot(kind='bar')
# 
