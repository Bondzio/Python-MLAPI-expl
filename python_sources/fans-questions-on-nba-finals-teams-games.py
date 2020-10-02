#!/usr/bin/env python
# coding: utf-8

# This kernel addresses the questions that NBA fans have on NBA final games.

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

champions = pd.read_csv('../input/championsdata.csv')
runnerups = pd.read_csv('../input/runnerupsdata.csv')


# Some records seems to have typo or wrong information. Let's correct them.

# In[ ]:


## 1. Correct broken record

# Seems like there's an additional single quote for one record
champions.loc[champions['Team']=="'Heat'",'Team'] = 'Heat'
champions.loc[champions['Team']=="Warriorrs",'Team'] = 'Warriors'

# Seems like there is an incorrect entry on the year for index number 186
champions[champions['Year'] == 2012]
champions[champions['Year'] == 2013]

# let's change the year to 2013
champions.loc[186,'Year'] = 2013


# Let's combine champion and runnerup and add additional features.

# In[ ]:



combined = champions.merge(runnerups,left_index=True,right_index=True)

combined['WinAccum_x'] = combined.apply(lambda x: combined.loc[(combined.Year_x==x.Year_x) & (combined.Game_x <= x.Game_x), 'Win_x'], axis='columns').sum(axis=1)
combined['WinAccum_y'] = combined.apply(lambda x: combined.loc[(combined.Year_y==x.Year_y) & (combined.Game_y <= x.Game_y), 'Win_y'], axis='columns').sum(axis=1)
combined['WinAccum_x'] = combined['WinAccum_x'].astype('int')
combined['WinAccum_y'] = combined['WinAccum_y'].astype('int')


# **Question 1:** Which teams have won the NBA final and how many times?

# In[ ]:


groupByYear = combined.groupby('Year_x')
groupByYearWinner = groupByYear.agg({'Team_x':lambda x: x.iloc[0]})
groupByYearRunnerup = groupByYear.agg({'Team_y':lambda x: x.iloc[0]})

won = pd.DataFrame(groupByYearWinner['Team_x'].value_counts().rename('No of times won in the final'))
won


# **Question 2:** Which teams have lost in the NBA final and how many times?

# In[ ]:


lost = pd.DataFrame(groupByYearRunnerup['Team_y'].value_counts().rename('No of times lost in the final'))
lost


# **Question 3**: How many times have a team appears in the final?

# In[ ]:


pd.DataFrame(won['No of times won in the final'].add(lost['No of times lost in the final'],fill_value=0),columns=['No of time in the finals']).sort_values(by='No of time in the finals',ascending=False)


# **Question 4**: Which teams have not lost in the NBA final?

# In[ ]:


teamsWon = groupByYearWinner['Team_x'].unique()
teamsLoss = groupByYearRunnerup['Team_y'].unique()
## Question: Which team has not lost in the NBA final?
# teamsWon - teamsLoss
pd.DataFrame(np.setdiff1d(teamsWon,teamsLoss),columns=['Not Loss In the final'])


# **Question 5**: Which teams have not won in the NBA final?

# In[ ]:


# teamsLoss - teamsWon
pd.DataFrame(np.setdiff1d(teamsLoss,teamsWon),columns=['Not Won'])


# **Question 6**: ## which teams have come back and win the final from a 2-0 deficit?

# In[ ]:


combined[ (combined['WinAccum_x']==0) & (combined['WinAccum_y']==2) ] [['Year_x','Team_x','Team_y']].rename(index=str, columns={"Year_x": "Year", "Team_x": "Winner","Team_y": "Runnerup"})


# **Question 7**: Which teams have come back and win the final from a 3-0 deficit?

# In[ ]:


## which team come back and win the final from 3-0 deficit?
combined[ (combined['WinAccum_x']==0) & (combined['WinAccum_y']==3) ] [['Year_x','Team_x','Team_y']].rename(index=str, columns={"Year_x": "Year", "Team_x": "Winner","Team_y": "Runnerup"})


# **Question 8**: Which teams have come back and win the final from a 3-1 deficit?

# In[ ]:



## which team come back and win the final from 3-1 deficit? (Yes we are expecting GSW)
combined[ (combined['WinAccum_x']==1) & (combined['WinAccum_y']==3) ] [['Year_x','Team_x','Team_y']].rename(index=str, columns={"Year_x": "Year", "Team_x": "Winner","Team_y": "Runnerup"})


# **Question 9**: Which teams swept the series

# In[ ]:


combined[ (combined['WinAccum_x']==4) & (combined['WinAccum_y']==0) ] [['Year_x','Team_x','Team_y']].rename(index=str, columns={"Year_x": "Year", "Team_x": "Winner","Team_y": "Runnerup"})


# **PART 2: Points**
# 
# Prepare the features and data structure to analyse points in the NBA final

# In[ ]:


pointsByYears = groupByYear.agg({
    'Team_x':lambda x: x.iloc[0],'Team_y':lambda x:x.iloc[0],
    'PTS_x':[np.sum,np.mean],'PTS_y':[np.sum,np.mean]
})

pointsByYears.columns.set_levels(['Winner','Runnerup','Winner Points','Runnerup Points'],level=0,inplace=True)
pointsByYears.columns.set_levels(['','per game','total'],level=1,inplace=True)

pointsByYears['No of Games'] = groupByYear.count()['Team_x']

pointsByYears[('Total Points','total')] = pointsByYears[('Runnerup Points','total')] + pointsByYears[('Winner Points','total')]
pointsByYears[('Total Points','per game')] = pointsByYears[('Total Points','total')] / pointsByYears['No of Games']

pointsByYears[('Difference In Points','total')] = pointsByYears[('Winner Points','total')] - pointsByYears[('Runnerup Points','total')]
pointsByYears[('Difference In Points','per game')] = pointsByYears[('Difference In Points','total')] / pointsByYears['No of Games']

pointsByYears.head(5)


# **Question 10**: Top 5 Highest scoring series (per game).

# 

# In[ ]:


pointsByYears.sort_values(by=('Total Points','per game'),ascending=False).head(5)


# **Question 11**: Top 5 highest points margin per game

# In[ ]:


pointsByYears.sort_values(by=('Difference In Points','per game'),ascending=False).head(5)


# **Question 12**: What are the series where the runnerup scores more than the champion

# In[ ]:


pointsByYears[pointsByYears['Difference In Points','total']<0]

