#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import math
import matplotlib.pyplot as plt
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


#'../input/LeagueofLegends.csv'
lol = pd.read_csv("../input/LeagueofLegends.csv")
lol.drop('Address', inplace=True, axis=1)
lol.sample(1)


# **Data from CBLoL league**

# In[ ]:


cblol = lol[lol['League'] == 'CBLoL']
print(cblol.shape)
cblol.sample(1)


# In[ ]:


rbkills = cblol.groupby(by=['Year'])['bResult', 'rResult'].sum()
rbkills.plot.bar()
plt.title('red team x blue team kills')
plt.show()


# **blue teams champions**

# In[ ]:


cblol.columns
#cblol[['blueTopChamp', 'blueJungleChamp', 'blueMiddleChamp', 'blueADCChamp','blueSupportChamp']]
cblol['blueTopChamp'].value_counts()[:5]


# In[ ]:


cblol['blueJungleChamp'].value_counts()[:5]


# In[ ]:


cblol['blueMiddleChamp'].value_counts()[:5]


# In[ ]:


cblol['blueADCChamp'].value_counts()[:5]


# In[ ]:


cblol['blueSupportChamp'].value_counts()[:5]


# **red teams champions**

# In[ ]:


cblol['redTopChamp'].value_counts()[:5]


# In[ ]:


cblol['redJungleChamp'].value_counts()[:5]


# In[ ]:


cblol['redMiddleChamp'].value_counts()[:5]


# In[ ]:


cblol['redADCChamp'].value_counts()[:5]


# In[ ]:


cblol['redSupportChamp'].value_counts()[:5]


# **most chosen champions by lane**

# In[ ]:


def laneChamps(lane, cblol):
    blue = 'blue' + str(lane) + 'Champ' 
    red = 'red' + str(lane) + 'Champ'
    lanePick = cblol[red].value_counts()[:5] + cblol[blue].value_counts()[:5]

    for i in range(0,len(lanePick)):
        if math.isnan(lanePick.values[i]):
            #top.values[i] = 0
            if lanePick.index[i] in cblol[red].value_counts()[:5]:
                lanePick.values[i] = cblol[red].value_counts()[:5].loc[lanePick.index[i]]
            else:
                lanePick.values[i] = cblol[blue].value_counts()[:5].loc[lanePick.index[i]]
    return lanePick.sort_values(ascending=False)


# In[ ]:


top = laneChamps('Top', cblol)
top
plt.bar(top.index, top.values)
plt.title('top 5 champions chosen as top')
plt.show()


# In[ ]:


jg = laneChamps('Jungle', cblol)
jg
plt.bar(jg.index, jg.values)
plt.title('top 5 champions chosen as jungle')
plt.show()


# In[ ]:


mid = laneChamps('Middle', cblol)
mid
plt.bar(mid.index, mid.values)
plt.title('top 5 champions chosen as middle')
plt.show()


# In[ ]:


adc = laneChamps('ADC', cblol)
adc
plt.bar(adc.index, adc.values)
plt.title('top 5 champions chosen as adc')
plt.show()


# In[ ]:


sup = laneChamps('Support', cblol)
sup
plt.bar(sup.index, sup.values)
plt.title('top 5 champions chosen as support')
plt.show()


# **Wins as blue team**

# In[ ]:


bwins = cblol[cblol.bResult > cblol.rResult]['blueTeamTag'].value_counts()
plt.bar(bwins.index, bwins.values)
plt.show()


# **Wins as red team**

# In[ ]:


rwins = cblol[cblol.bResult > cblol.rResult]['redTeamTag'].value_counts()
plt.bar(rwins.index, rwins.values)
plt.show()


# **top 5 match with highest and lowest duration**

# In[ ]:


cblol[cblol.gamelength > 60][['blueTeamTag','redTeamTag','gamelength']].sort_values('gamelength', ascending=False)[:5]


# In[ ]:


cblol[cblol.gamelength < 30][['blueTeamTag','redTeamTag','gamelength']].sort_values('gamelength', ascending=True)[:5]


# **Data from NALCS, EULCS, LCK, LMS, and CBLoL leagues**

# **Bans**

# In[ ]:


bans = pd.read_csv('../input/bans.csv')
bans.drop('Address', axis=1, inplace=True)
bans.sample(1)


# In[ ]:


def bansChamps(ban_number, bans):
    ban = 'ban_' + str(ban_number)
    bans_ = bans[bans.Team == 'redBans'][ban].value_counts()[:5] + bans[bans.Team == 'blueBans'][ban].value_counts()[:5]

    for i in range(0,len(bans_)):
        if math.isnan(bans_.values[i]):
            if bans_.index[i] in bans[bans.Team == 'redBans'][ban].value_counts()[:5]:
                bans_.values[i] = bans[bans.Team == 'redBans'][ban].value_counts()[:5].loc[bans_.index[i]]
            else:
                bans_.values[i] = bans[bans.Team == 'blueBans'][ban].value_counts()[:5].loc[bans_.index[i]]
    return bans_.sort_values(ascending=False)


# In[ ]:


ban1 = bansChamps(1, bans)
ban2 = bansChamps(2, bans)
ban3 = bansChamps(3, bans)
ban4 = bansChamps(4, bans)
ban5 = bansChamps(5, bans)


# In[ ]:


totalbans = ban1 + ban2 + ban3 + ban4 + ban5


# In[ ]:


def bansTotal(totalbans, ban1, ban2, ban3, ban4, ban5):
    for i in range(0, len(totalbans)):
        if math.isnan(totalbans.values[i]):
            totalbans.values[i] = 0
            if totalbans.index[i] in ban1:
                totalbans.values[i] += ban1.loc[totalbans.index[i]]
            if totalbans.index[i] in ban2:
                totalbans.values[i] += ban2.loc[totalbans.index[i]]
            if totalbans.index[i] in ban3:
                totalbans.values[i] += ban3.loc[totalbans.index[i]]
            if totalbans.index[i] in ban4:
                totalbans.values[i] += ban4.loc[totalbans.index[i]]
            if totalbans.index[i] in ban5:
                totalbans.values[i] += ban5.loc[totalbans.index[i]]
    return totalbans.sort_values(ascending=False)


# In[ ]:


bans = bansTotal(totalbans, ban1, ban2, ban3, ban4, ban5)[:5]
plt.bar(bans.index, bans.values)
plt.title('top 5 most banned champions')
plt.show()


# **gold**

# In[ ]:


gold = pd.read_csv('../input/gold.csv')
gold.drop('Address', axis=1, inplace=True)
#goldTotal = gold[gold.Type == 'goldblue'].sum() + gold[gold.Type == 'goldred'].sum()
gold.Type.unique()


# In[ ]:


def goldlane(lane, gold):
    red = 'goldred' + str(lane)
    blue = 'goldblue' + str(lane)
    goldLane = gold[gold.Type == blue].sum() + gold[gold.Type == red].sum()
    goldLane.values[0] = 'gold' + str(lane)
    return goldLane


# In[ ]:


top = goldlane('Top', gold)
minutes = []
for m in top.index:
    if m != 'Type':
        minutes.append(m.split('_')[1])
    else:
        minutes.append(m.split('_'))
minutes

d = {'minute' : minutes[1:], 'gold' : top.values[1:]}
top_ = pd.DataFrame(data=d)
top_.plot.line()
plt.title('gold per minute by top')
plt.show()


# In[ ]:


jg = goldlane('Jungle', gold)
d = {'minute' : minutes[1:], 'gold' : jg.values[1:]}
jg_ = pd.DataFrame(data=d)
jg_.plot.line()
plt.title('gold per minute by jungle')
plt.show()


# In[ ]:


mid = goldlane('Middle', gold)
d = {'minute' : minutes[1:], 'gold' : mid.values[1:]}
mid_ = pd.DataFrame(data=d)
mid_.plot.line()
plt.title('gold per minute by mid')
plt.show()


# In[ ]:


adc = goldlane('ADC', gold)
d = {'minute' : minutes[1:], 'gold' : adc.values[1:]}
adc_ = pd.DataFrame(data=d)
adc_.plot.line()
plt.title('gold per minute by adc')
plt.show()


# In[ ]:


sup = goldlane('Support', gold)
d = {'minute' : minutes[1:], 'gold' : sup.values[1:]}
sup_ = pd.DataFrame(data=d)
sup_.plot.line()
plt.title('gold per minute by sup')
plt.show()


# In[ ]:


d = {'minute' : minutes[1:], 'top' : top.values[1:], 'mid' : mid.values[1:], 'jg' : jg.values[1:], 'adc' : adc.values[1:], 'sup' : sup.values[1:]}
lanes = pd.DataFrame(data=d)
lanes.plot.line()


# **Kills**

# In[ ]:


kills = pd.read_csv('../input/kills.csv')
kills.drop('Address', axis=1, inplace=True)
topkillers = kills.Killer.value_counts()[:5]
plt.bar(topkillers.index, topkillers.values)
plt.title('top Killers')
plt.xlabel('Team and Nick')
plt.show()


# In[ ]:


topvictims = kills.Victim.value_counts()[:6]
topvictims = topvictims[topvictims.index != 'None']
topvictims
plt.bar(topvictims.index, topvictims.values)
plt.title('top victims')
plt.xlabel('Team and Nick')
plt.show()


# **fasters kills**

# In[ ]:


kills[['Killer', 'Victim', 'Time']][kills.Time < 25][:5].sort_values('Time')


# **most faster killed monsters**

# In[ ]:


monsters = pd.read_csv('../input/monsters.csv')
print(monsters.Type.unique())
monsters = monsters[['Type','Time']][monsters.Time < 25].sort_values('Time')
dragon = monsters[['Type','Time']][monsters.Type == 'DRAGON'][:5]
earth_dragon = monsters[['Type','Time']][monsters.Type == 'EARTH_DRAGON'][:5]
water_dragon = monsters[['Type','Time']][monsters.Type == 'WATER_DRAGON'][:5]
air_dragon = monsters[['Type','Time']][monsters.Type == 'AIR_DRAGON'][:5]
fire_dragon = monsters[['Type','Time']][monsters.Type == 'AIR_DRAGON'][:5]
baron = monsters[['Type','Time']][monsters.Type == 'BARON_NASHOR'][:5]


# In[ ]:


dragon.Time


# In[ ]:


earth_dragon.Time


# In[ ]:


water_dragon.Time


# In[ ]:


air_dragon.Time


# In[ ]:


fire_dragon.Time


# In[ ]:


baron.Time

