#!/usr/bin/env python
# coding: utf-8

# In this script, I predicted yards gained (Yards.Gained) by each receiver for every game. I used four models, and they all produced similar results with mean absolute error of around 26 yards.  While, the result isn't good enough to beat Daily Fantasy Football and the best professionals, it does well compared to other DFS sites's algorithms. For anyone new to the industry interested in modeling NFL data for DFS purposes, this might be a good place to start. One might need to build a more sophisticated model with more rigorous feature engineering and feature selection to produce any useful result. Some features that might be important to consider are:  
# -Dummy for Whether game is at home or away    
# -Dummy for whether game is a Division game    
# -Injury Variables   
# -Weather Situations    
# -History of player against specific team    
# 
# 
# 
# 
# 
# 

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import linear_model, ensemble
from sklearn.model_selection import cross_val_score
import warnings
warnings.filterwarnings('ignore')





data = pd.read_csv("../input/NFLPlaybyPlay2015.csv")


pass_data = data[data['PassAttempt'] == 1]

pass_data = pass_data[[ 'GameID', 'PassAttempt', 'yrdln', "Receiver", 'ydstogo', 'DefensiveTeam', 'posteam', 'Yards.Gained', 'Touchdown', 'Passer', 'PassOutcome', 'PassLength', 'PassLocation', 'ScoreDiff', 'PosTeamScore']]
pass_data['posteam'].fillna(value = 'NA', inplace = True)
#pass_data[pass_data['posteam'] == np.nan] = 'NA'

sns.countplot(x="DefensiveTeam",hue = 'PassOutcome',orient ='v', data = pass_data)
plt.show()
teamss = np.unique(pass_data['DefensiveTeam'].values)
length = np.unique(pass_data['PassLocation'].astype('str').values)
    
pass_data.loc[pass_data['PassOutcome'] == 'Complete', 'PassOutcome'] = 1.0 
pass_data.loc[pass_data['PassOutcome'] == 'Incomplete Pass', 'PassOutcome'] = 0.0
pass_data['PassOutcome'].fillna(value = 999, inplace = True)
pass_data = pass_data[pass_data['PassOutcome'] != 999]
pass_data['Receptions'] = pass_data["PassOutcome"].astype('int64')


reception_info = pass_data.loc[pass_data['PassOutcome'] != 999, ['Passer', 'Receiver','PassAttempt', 'GameID', "Yards.Gained", 'Receptions', 'DefensiveTeam', 'posteam']].groupby(by = ["posteam", "DefensiveTeam", 'GameID', 'Receiver', 'Passer'], as_index = False).sum()


reception_info.sort_values(by = ["Receiver", "GameID"], inplace = True)


reception_info.reset_index(drop = True, inplace = True)

reception_info['last_four_rec'] = range(len(reception_info))
reception_info['last_four_yds'] = range(len(reception_info))
reception_info['last_two_rec'] = range(len(reception_info))
reception_info['last_two_yds'] = range(len(reception_info))

    
def recs(x):
   ind = list(reception_info['last_four_rec'].values).index(x)
   not_done = True
   i = 4
   while not_done:
       if ind > 4:
           if reception_info.loc[ind, 'Receiver'] == reception_info.loc[ind-i, 'Receiver'] :
               
                  return reception_info['Receptions'].loc[ind - i: ind -1 ].mean()
           elif i == 1:
                  return reception_info['Receptions'].median()
           i = i -1 
       else:
            return reception_info['Receptions'].loc[ind - i: ind -1].sum()
def yds(x):
   ind = list(reception_info['last_four_yds'].values).index(x)
   not_done = True
   i = 4
   while not_done:
       if ind > 4:
           if reception_info.loc[ind, 'Receiver'] == reception_info.loc[ind-i, 'Receiver'] :
               
                  return reception_info['Yards.Gained'].loc[ind - i: ind -1].mean()
           elif i == 1:
                  return reception_info['Yards.Gained'].median()
           i = i -1 
       else:
            return reception_info['Yards.Gained'].loc[ind - i: ind -1].sum()
def yds2(x):
   ind = list(reception_info['last_two_yds'].values).index(x)
   not_done = True
   i = 2
   while not_done:
       if ind > 2:
           if reception_info.loc[ind, 'Receiver'] == reception_info.loc[ind-i, 'Receiver'] :
               
                  return reception_info['Yards.Gained'].loc[ind - i: ind -1].mean()
           elif i == 1:
                  return reception_info['Yards.Gained'].median()
           i = i -1 
       else:
            return reception_info['Yards.Gained'].loc[ind - i: ind -1].sum()
def recs2(x):
   ind = list(reception_info['last_two_rec'].values).index(x)
   not_done = True
   i = 2
   while not_done:
       if ind > 1:
           if reception_info.loc[ind, 'Receiver'] == reception_info.loc[ind-i, 'Receiver'] :
               
                  return reception_info['Receptions'].loc[ind - i: ind -1].mean()
           elif i == 1:
                  return reception_info['Receptions'].median()
           i = i -1 
       else:
            return reception_info['Receptions'].loc[: ind -1].mean()
def teams(x):
    ind = list(teams_info['previous_yds'].values).index(x)
    team = teams_info.loc[ind, 'DefensiveTeam']
    ind2 = list(teams_info['DefensiveTeam'].values).index(team)
    if ind == 0 :
        return teams_info['Yards.Gained'].median()
    elif ind > ind2:
        
        return teams_info.loc[ind2: ind-1, 'Yards.Gained'].mean()
    else:
        return teams_info['Yards.Gained'].median()
def teams2(x):
    ind = list(teams_info['previous2_yds'].values).index(x)
    not_done = True
    i = 2
    while not_done:
       if ind > 2:
           if teams_info.loc[ind, 'DefensiveTeam'] == teams_info.loc[ind-i, 'DefensiveTeam'] :
               
                  return teams_info['Yards.Gained'].loc[ind - i: ind -1].mean()
           elif i == 1:
                  return teams_info['Yards.Gained'].median()
           i = i -1 
       else:
            return teams_info['Yards.Gained'].loc[ind - i: ind -1].mean()
def teamsr(x):
    ind = list(teams_info['previous_rec'].values).index(x)
    team = teams_info.loc[ind, 'DefensiveTeam']
    ind2 = list(teams_info['DefensiveTeam'].values).index(team)
    if ind == 0 :
        return teams_info['Receptions'].median()
    elif ind > ind2:
          return teams_info.loc[ind2: ind-1, 'Receptions'].mean()
    else:
        return teams_info['Receptions'].median()
def teamsr2(x):
    ind = list(teams_info['previous2_rec'].values).index(x)
    not_done = True
    i = 2
    while not_done:
       if ind > 2:
           if teams_info.loc[ind, 'DefensiveTeam'] == teams_info.loc[ind-i, 'DefensiveTeam'] :
               
               return teams_info.loc[ind -i: ind-1, 'Receptions'].mean()     
           elif i == 1:
                  return reception_info['Receptions'].median()
           i = i -1 
       else:
            return teams_info['Receptions'].loc[ind - i: ind -1].mean()
def teamsp(x):
    ind = list(teams_info['previous_plays'].values).index(x)
    team = teams_info.loc[ind, 'DefensiveTeam']
    ind2 = list(teams_info['DefensiveTeam'].values).index(team)
    if ind == 0 :
        return teams_info['PassAttempt'].median()
    elif ind > ind2:
        
        return teams_info.loc[ind2: ind-1, 'PassAttempt'].mean()
    else:
        return teams_info['PassAttempt'].median()
def teamsp2(x):
    ind = list(teams_info['previous4_plays'].values).index(x)
    not_done = True
    i = 4
    while not_done:
       if ind > 4:
           if teams_info.loc[ind, 'DefensiveTeam'] == teams_info.loc[ind-i, 'DefensiveTeam'] :
               
                  return teams_info.loc[ind - i: ind -1, 'PassAttempt'].mean()
           elif i == 1:
                  return teams_info['PassAttempt'].median()
           i = i -1 
       else:
            return teams_info['PassAttempt'].loc[ind - i: ind -1].mean()
        
reception_info['last_four_rec'] = reception_info['last_four_rec'].apply(lambda x: recs(x))  
reception_info['last_four_yds'] = reception_info['last_four_yds'].apply(lambda x: yds(x))  
reception_info['last_two_rec'] = reception_info['last_two_rec'].apply(lambda x: recs2(x))  
reception_info['last_two_yds'] = reception_info['last_two_yds'].apply(lambda x: yds2(x)) 

teams_info = pass_data[['Yards.Gained', "Receptions", "DefensiveTeam", "GameID", "PassAttempt"]].groupby(by = ["GameID", "DefensiveTeam"], as_index = False).sum()
teams_info = teams_info.sort_values(by = ["DefensiveTeam", "GameID"])
teams_info = teams_info[teams_info['Yards.Gained'] > 100]
teams_info.reset_index(drop= True, inplace = True)
teams_info['previous_yds'] = range(len(teams_info))
teams_info['previous2_yds'] = range(len(teams_info))
teams_info['previous_rec'] = range(len(teams_info))
teams_info['previous2_rec'] = range(len(teams_info))
teams_info['previous_plays'] = range(len(teams_info))
teams_info['previous4_plays'] = range(len(teams_info))

teams_info['previous_yds'] = teams_info['previous_yds'].apply(lambda x: teams(x))
teams_info['previous2_yds'] = teams_info['previous2_yds'].apply(lambda x: teams2(x))
teams_info['previous_rec'] = teams_info['previous_rec'].apply(lambda x: teamsr(x))
teams_info['previous2_rec'] = teams_info['previous2_rec'].apply(lambda x: teamsr2(x))
teams_info['previous_plays'] = teams_info['previous_plays'].apply(lambda x: teamsp(x))
teams_info['previous4_plays'] = teams_info['previous4_plays'].apply(lambda x: teamsp2(x))




teams_info = teams_info.drop(['Receptions', 'Yards.Gained', 'PassAttempt'], axis = 1)
reception_info  = reception_info.merge(teams_info, on = ['DefensiveTeam', "GameID"])


print(reception_info.corr()["Yards.Gained"] )



# Example exploration on packers
packers = reception_info.loc[reception_info.posteam == 'GB']
packers['Targets'] = packers.pop('PassAttempt')

 
print (packers.sort_values(by = ['GameID', "Yards.Gained"])[[ 'Yards.Gained', 'Receptions' ,'Receiver', "previous4_plays"]])
print(np.unique(packers.loc[packers.Receptions > 5].Receiver))
print(packers.corr()['Yards.Gained'])



reception_info = reception_info.dropna()



train_x = reception_info[['previous_yds', 'previous2_yds', 'previous_rec', 'previous2_rec', 'previous_plays', 'previous4_plays']]
train_y = reception_info['Yards.Gained']

def train_models(estimators, data, label): 
    result = {}
    for estimator in estimators:
        
        score = -cross_val_score(estimators[estimator], data, label, scoring = "neg_mean_absolute_error").mean()
        result[""+ str(estimator)] = score 
    return pd.Series(result)

estimators = {}
#estimators['Linear Regression'] = linear_model.LinearRegression()
estimators['Random Forest '] = ensemble.RandomForestRegressor()
estimators['Ridge CV'] = linear_model.RidgeCV(alphas = [0.1, 0.2, 0.5, 1, 10])
estimators['Bayesian Ridge'] = linear_model.BayesianRidge()
estimators['LinearRegression'] = linear_model.LinearRegression()


x = train_models(estimators, train_x, train_y)
print (x)
x.plot(kind = 'bar')

