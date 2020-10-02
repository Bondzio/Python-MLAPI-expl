#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


# In[ ]:


# This function will reduce our work load of searcing many players 
def GetBestPlayers(dframe,position,num):
    dframe=dframe.sort_values([position,'Overall'],ascending=False)[['ID','Name','Position','Overall',position]].reset_index(drop=True)[:num]
    return(dframe)


# In[ ]:


df=pd.read_csv('./fifadata.csv')
df.drop(columns=['Unnamed: 0'],inplace=True)


# #### Get best team (Best possible 10) for 4-4-2 formation, based on ""Overall"" score across the players in the dataset.
#     Step1: Firstly, pick the positions which will be played in a 4-4-2 formation (CF, CF, CM, CM, RM, LM, CB, CB, RB, LB)
#     Step2: Find top 5-10 players based on a position score (Columns: CF, CM, RM, LM, CB, RB, LB)
#     Step3: Now sort the players based on "Overall" score (Which will be aggregated for the best team)
#     Srep4: Start checking position by position which player makes place for himself in the team (If the player is already there, skip for the next name)
#     Step5: Once all positions are occupied, calculate the sum of "Overall" scores to get the team score

# In[ ]:


poslst=['LS', 'ST', 'RS', 'LW', 'LF', 'CF', 'RF', 'RW', 'LAM', 'CAM', 'RAM', 'LM', 'LCM', 'CM', 'RCM', 'RM', 'LWB', 'LDM', 'CDM', 'RDM', 'RWB', 'LB', 'LCB', 'CB', 'RCB', 'RB']

df_pos=df[['ID','Name','Position','Overall']+poslst]
for col in poslst:
    df_pos[col]=df_pos[col].fillna(0).apply(lambda x : sum([int(i) for i in str(x).split('+')]))


# In[ ]:


# Get best position persons
# Players who have high position stat as well as high overall stat
# Let us now look into 442 formation
# 2-CF, 1-LM, 1-RM, 2-CM, 1-LB, 2-CB, 1-RB
team442=['CF','CF','LM','RM','CM','CM','LB','RB','CB','CB']

lstteam=[]
lstbest=[]
for pos in team442:
    bestlist=list(GetBestPlayers(df_pos,pos,5)['Name'])
    for player in bestlist:
        if (player not in lstteam):  
            lstteam.append(player)
            print(player,pos)
            break


# In[ ]:


df_best_442=pd.DataFrame([lstteam,team442]).T.rename(columns={0:'Name',1:'Position'})
df_best_442=pd.merge(df_pos[['Name','Overall','CF','LM','RM','CM','LB','RB','CB']],df_best_442,on=['Name'])
TotalScore=np.sum(df_best_442.Overall)


# In[ ]:


print("Best 4-4-2 formation team")
print('\n')
print(df_best_442)
print('\n')
print("Score", TotalScore)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




