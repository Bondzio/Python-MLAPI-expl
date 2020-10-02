#!/usr/bin/env python
# coding: utf-8

# In[ ]:


### TODO:
# 1. Do feature engineering on group level instead of user level
# 2. Separate data between first person mode and free for all mode
# 3. Eliminate cheaters and anomalies
# 4. Develop prediction funcgion
#    - Final ranking per match can be determined using this formula -> 100/maxPlace, as ranking interval


# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import xgboost
from matplotlib import pyplot as plt


# In[ ]:


### Read training data
train = pd.read_csv('../input/train_V2.csv')


# In[ ]:


train.columns


# In[ ]:


train.head(5)


# In[ ]:


from pylab import rcParams
rcParams['figure.figsize'] = 10, 8


# In[ ]:


matchTypes = train.groupby('matchId')['matchType'].first().value_counts()


# In[ ]:


matchTypes.index


# In[ ]:


fig, ax = plt.subplots()
ax.bar(np.arange(len(matchTypes.index)),matchTypes.values,align='center')
ax.set_xticks(np.arange(len(matchTypes.index)))
ax.set_xticklabels(matchTypes.index,rotation=70)
plt.title("Match type queue distribution")
plt.show()


# ### 1. Group Level Inspection and Feature Engineering

# Features need to be generated on a group level. Below is the explanation. Let's inspect data for matchId **a10357fd1a4a91**

# In[ ]:


### Inspect a match data
matchA_df = train[train.matchId == 'a10357fd1a4a91']


# In[ ]:


### Inspect a group
matchA_df[matchA_df.groupId == '654c638629b8fc']


# In[ ]:


### select groupIds in a match
playerGroups = matchA_df[['Id','groupId']]


# In[ ]:


### Number of players per group
playerCountGroup = playerGroups.groupby('groupId',as_index=False).agg({'Id':'count'}).sort_values('Id').rename(columns={"Id":"players"}).reset_index(drop=True)


# In[ ]:


playerCountGroup


# Various number of players in a group may exist in one match. Player queuing solo will be in a group with only 1 member.

# In[ ]:


### Total players in this match
print("Total players: {}".format(playerCountGroup.players.sum()))
print("Total groups: {}".format(playerCountGroup.groupId.count()))


# Now notice the distribution of placement ranking which we would like to predict

# In[ ]:


### Notice the percentage ranking
matchA_df[['winPlacePerc']].drop_duplicates().sort_values('winPlacePerc').reset_index(drop=True)


# There are 26 placements which actually correspond to the number of groups. The interval could be retrieved using:

# In[ ]:


### The increment of winPlacePerc is retrieved using:
print((100/float(26))/100)


# Because the ranking is spread based on the number of groups in one match, group level features need to be generated!

# In[ ]:


### Generate group level features    

def generate_group_level_features(dataset,feature_columns=['kills','assists','boosts']):
    features = dataset[["matchId","groupId",*feature_columns]].reset_index(drop=True)
    matchGroups = features[["matchId","groupId"]].drop_duplicates().reset_index(drop=True)
    
    ### predefined basic statistic operations
    _stats = ['max','min','sum','mean','std']
    
    ### calculate group level features
    for f in feature_columns:
        for s in _stats:
            new_field = '{s}_{f}'.format(s=s,f=f)
            print(new_field)
            matchGroups = pd.merge(matchGroups,
                features.groupby(["matchId","groupId"],as_index=False)\
                .agg({f:s}).rename(columns={f:new_field}).fillna(0)[["matchId","groupId",new_field]].drop_duplicates(),
                on=['matchId','groupId'],how='inner'
            )
            
    return matchGroups.reset_index(drop=True)


# In[ ]:


### sample of group level features
#generate_group_level_features(matchA_df)


# In[ ]:


import time
s = time.time()
groupLevelFeatures_train = generate_group_level_features(train)
e = time.time()
print("elapsed {}s".format(e-s))


# In[ ]:


groupLevelFeatures_train.to_csv("groupLevelFeatures_train.csv",index=False)


# In[ ]:


# dummy
# a = pd.DataFrame(data=[{"a":1,"b":2},{"a":3,"b":6}])

# for i,r in a.iterrows():
#     print(r['a'])

# def dum(x):
#     x['c'] = x['a'] + x['b']
#     return x

# a = a.apply(lambda x: dum(x),1)

# a.iloc[0]['c'] = 12

# a


# ### 2. Separate Game Modes data

# (TODO) <br>
# There are several game modes / match types in PUBG <br>
# https://pubg.gamepedia.com/Game_Modes <br>
# Patterns might differ for example between First Person Mode and Third Person Mode even though the players are on solo queue game.

# ### 3. Eliminate Anomalies

# (TODO) <br>
# There are already existing kernel out there mentioning anomalies or cheaters in PUBG matches. <br>
# We need to adopt some of them.

# ### 4. Prediction Functions

# (TODO) <br>
# Because how dynamic a winPlacePerc value can be, custom prediction function needs to be developed
