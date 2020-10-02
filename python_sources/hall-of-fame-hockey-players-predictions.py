#!/usr/bin/env python
# coding: utf-8

# # Summary
# I have had some success developing a model predict which NHL players will be inducted into the hockey Hall of Fame.
# 
# However, the classes of players that get into the hall of fame versus not are completely unbalanced.  I need to oversample the hall of fame players or undersample the non-hall of famers to get a better accuarcy.
# 
# # Problem Understanding
# The problem I am trying to solve is to **predict which NHL hockey players will be inducted into the hockey Hall of Fame**.
# 
# For this research, I'm focusing the scope on just the non-goalie players.
# 
# The prediction likely is based on a hockey player's career performance.  Performance can be measured in a number of different ways including goals, assists, points, and awards received.
# 
# # Data Understanding
# The data I'll be using for this analysis is from the [Professional Hockey Database](https://www.kaggle.com/open-source-sports/professional-hockey-database).  It includes data on a players hall of fame status, points, awards given.
# 
# There are several limitations with the dataset:
# * The latest year is 2011.  However, the dataset may have enough data to help make accurate predictions for players who have inducted into the hall of fame after 2011.
# * I have noted that many players that played after 2011 have been marked as their last NHL year is 2011.   I've made the assumption that if a player's last year is recorded as 2011 then I indicate that they are current players and not included in fitting the prediction.

# # Python Libraries

# In[ ]:


import pandas as pd
from pandas.plotting import scatter_matrix
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, KBinsDiscretizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import train_test_split, KFold, cross_val_score, cross_val_predict, GridSearchCV, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix


# # Data Import & Preprocessing
# The data is imported and preprocessed and then a subset is displayed as example of what is in the dataset.

# In[ ]:


#Have Pandas output more columns 
pd.set_option('display.max_columns', 30)

#Data Import
master = pd.read_csv("../input/Master.csv")
awardsPlayers = pd.read_csv("../input/AwardsPlayers.csv")
scoring = pd.read_csv("../input/Scoring.csv")
scoringSC = pd.read_csv("../input/ScoringSC.csv")
hof = pd.read_csv("../input/HOF.csv")

class PlayersWithCareerStartDates(BaseEstimator, TransformerMixin):
    """Subset only players who have career start dates"""
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[(X.playerID.notnull()) & (X.firstNHL.notnull() | X.firstWHA.notnull())]

class AddIndicators(BaseEstimator, TransformerMixin):
    """Add indicators"""
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        #Add Retired indicator
        X.loc[:, 'retired'] = 1
        X.loc[X.lastNHL == 2011, 'retired'] = 0
        #Add Hall of Fame indicator
        X['hof'] = 0
        X.loc[X.hofyear.notnull(), 'hof'] = 1
        #Add Goalie indicator
        X['goalie'] = 0
        X.loc[X.pos == "G", 'goalie'] = 1
        #Return Dataset
        return X
    
class MergeOtherData(BaseEstimator, TransformerMixin):
    """Merge Players, aggregate sum of points, Counts for All Awards, and Hall of Fame Status by outer join"""
    def __init__(self, score, award, hall):
        self.score = score
        self.award = award
        self.hall = hall
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        #Count of all awards
        awards = self.award.groupby(['playerID']).size().to_frame('awards').reset_index()
        #Sum of all points
        points = self.score[['playerID','Pts']].groupby(['playerID']).sum().reset_index()
        #Merge Players, aggregate sum of points, Counts for All Awards, and Hall of Fame Status by outer join
        X = X.merge(points, left_on='playerID', right_on='playerID', how='left')
        X = X.merge(awards, left_on='playerID', right_on='playerID', how='left')
        X = X.merge(self.hall, left_on='hofID', right_on='hofID', how='left')
        #Rename columns
        X=X.rename(columns = {'year':'hofyear'})
        X=X.rename(columns = {'Pts':'pts'})
        #Assign 0 to variables showing NA as a result of the merge
        X.loc[X.awards.isnull(),'awards'] = 0
        X.loc[X.pts.isnull(),'pts'] = 0
        #Return dataset
        return X
    
class AddPlayersInductedToHOFSince(BaseEstimator, TransformerMixin):
    """Add Years to all players inducted in 2012 and onwards"""
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        hof = [
            {"firstName":"Pavel", "lastName":"Bure", "hofyear":2012},
            {"firstName":"Adam", "lastName":"Oates", "hofyear":2012},
            {"firstName":"Joe", "lastName":"Sakic", "hofyear":2012},
            {"firstName":"Mats", "lastName":"Sundin", "hofyear":2012},
            {"firstName":"Chris", "lastName":"Chelios", "hofyear":2013},
            {"firstName":"Scott", "lastName":"Niedermayer", "hofyear":2013},
            {"firstName":"Brendan", "lastName":"Shanahan", "hofyear":2013},
            {"firstName":"Rob", "lastName":"Blake", "hofyear":2014},
            {"firstName":"Peter", "lastName":"Forsberg", "hofyear":2014},
            {"firstName":"Mike", "lastName":"Modano", "hofyear":2014},
            {"firstName":"Sergei", "lastName":"Fedorov", "hofyear":2015},
            {"firstName":"Phil", "lastName":"Housley", "hofyear":2015},
            {"firstName":"Nicklas", "lastName":"Lidstrom", "hofyear":2015},
            {"firstName":"Chris", "lastName":"Pronger", "hofyear":2015},
            {"firstName":"Eric", "lastName":"Lindros", "hofyear":2016},
            {"firstName":"Dave", "lastName":"Andreychuk", "hofyear":2017},
            {"firstName":"Paul", "lastName":"Kariya", "hofyear":2017},
            {"firstName":"Mark", "lastName":"Recchi", "hofyear":2017},
            {"firstName":"Teemu", "lastName":"Selanne", "hofyear":2017},
            {"firstName":"Martin", "lastName":"St. Louis", "hofyear":2018},
        ]
        for i in hof:
            X.loc[(X.firstName == i["firstName"]) & (X.lastName == i["lastName"]), 'hofyear'] = i["hofyear"]
        return X
    
class VariablesToKeep(BaseEstimator, TransformerMixin):
    """Keep only relevant columns"""
    def __init__(self, variables):
        self.variables = variables
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.variables]
    
class RetiredPlayers(BaseEstimator, TransformerMixin):
    """Output only Retired Players"""
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[X.retired == 1]
    
class NonRetiredPlayers(BaseEstimator, TransformerMixin):
    """Output only Non-Retired Players"""
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[X.retired == 0]

class NonGoalies(BaseEstimator, TransformerMixin):
    """Output only non-Goalies"""
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[players.goalie != 1]
    
class PlayersPredictedHOF(BaseEstimator, TransformerMixin):
    """Players predicted to be in Hall of Fame"""
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X.loc[(X.hofyear > 2011) | (X.hofyear.isnull() & X.predhof == 1), :]
    
class AddYearsPlayed(BaseEstimator, TransformerMixin):
    """Add years played overall, in NHL, and in WHA"""
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        #Calculate first year playing
        X.loc[X.firstNHL <= X.firstWHA, 'firstYear'] = X.firstNHL
        X.loc[X.firstNHL >= X.firstWHA, 'firstYear'] = X.firstWHA
        X.loc[X.firstNHL.isnull(), 'firstYear'] = X.firstWHA
        X.loc[X.firstWHA.isnull(), 'firstYear'] = X.firstNHL
        #Calculate last year playing
        X.loc[X.lastNHL >= X.lastWHA, 'lastYear'] = X.lastNHL
        X.loc[X.lastNHL <= X.lastWHA, 'lastYear'] = X.lastWHA
        X.loc[X.lastNHL.isnull(), 'lastYear'] = X.lastWHA
        X.loc[X.lastWHA.isnull(), 'lastYear'] = X.lastNHL
        #Calculate total years playing
        X.loc[:, 'yearsPlayed'] = X.lastYear-X.firstYear+1
        #Calculate total years playing in one league
        X.loc[:, 'yearsPlayedNHL'] = 0
        X.loc[:, 'yearsPlayedWHA'] = 0
        X.loc[X.firstNHL.notnull(), 'yearsPlayedNHL'] = X.lastNHL-X.firstNHL+1
        X.loc[X.firstWHA.notnull(), 'yearsPlayedWHA'] = X.lastWHA-X.firstWHA+1
        X.loc[(X.lastNHL >= X.lastWHA) & (X.firstNHL <= X.firstWHA), 'yearsPlayedNHL'] = X.lastNHL-X.firstNHL+1-X.yearsPlayedWHA
        X.loc[(X.lastWHA >= X.lastNHL) & (X.firstWHA <= X.firstNHL), 'yearsPlayedNHL'] = X.lastWHA-X.firstWHA+1-X.yearsPlayedNHL
        return X

class AddEraIndicator(BaseEstimator, TransformerMixin):
    """Add era of the player"""
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        eras = ["Founding 1917-1941","Original Six 1942-1967","Expansion 1968-1992","Modern 1993-"]
        X['era'] = pd.cut(X.lastYear, [1917,1941,1967,1992,2011], labels=eras, include_lowest=True)
        X['era_temp'] = X['era']
        X = pd.get_dummies(X, columns=["era_temp"], prefix="era")
        return X
    
variableList = ["firstName","lastName","firstNHL","lastNHL","firstWHA","lastWHA","pos","goalie","birthYear","deathYear","retired","awards","pts","hofyear","hof"]
    
dataPipe = Pipeline([
    ('playersWithCareerStartDates', PlayersWithCareerStartDates()),
    ('mergeOtherData', MergeOtherData(scoring, awardsPlayers, hof)),
    ('addPlayersInductedToHOFSince', AddPlayersInductedToHOFSince()),
    ('addIndicators', AddIndicators()),
    ('variablesToKeep', VariablesToKeep(variableList)),
    ('addYearsPlayed', AddYearsPlayed()),
    ('addEraIndicator', AddEraIndicator())
])

players = dataPipe.fit_transform(master)

retiredNonGoaliePipe = Pipeline([
    ('retiredPlayers', RetiredPlayers()),
    ('nonGoalies', NonGoalies())
])

retiredNonGoalies = retiredNonGoaliePipe.fit_transform(players)

nonGoalies = NonGoalies().transform(players)

#Sample Players Table
players


# # Exploratory Data Analysis
# By investigating the correlationships in the dataset, it was discovered that hall of fame status was correlated with awards and points.  I'm only using retired players for this analysis and it will give a better sense how career stats are related to being inducted to the hall of fame.

# ## Descriptive Analysis

# In[ ]:


retiredNonGoalies.describe()


# ## Correlations
# When looking at correlations between variables, it appears that points and awards most correlate strongly with hall of fame status.  Therefore, the modelling will focus on the relationships between the response variable hall of fame status and two predictors:  awards and points.

# In[ ]:


# calculate the correlation matrix
corr = retiredNonGoalies.corr()
corr['hof'].sort_values(ascending=False)


# ## Distributions
# The pts and awards variables are heavily skewed towards lower totals because most players score and get awarded very few times in a career compared to the top players.
# 
# The other interesting thing is that the hall of fame indicator is heavily skewed towards not being in the hall of fame.  Therefore there is evidence of imbalanced data for the hall of fame indicator, which will further complicate modelling.

# In[ ]:


# Show skatter matrix
sns.pairplot(retiredNonGoalies, vars=["hof","awards","pts"], hue="hof", height=5);


# ## Hall of Fame Indicator
# The hall of fame distribution is heavily skewed towards non-hall of famers for obvious reasons:  only the best get into the hall of fame.  In fact, only 3.3% of all players are in the hall of fame.  This is indicative of imbalanced data.

# In[ ]:


plt.pie(retiredNonGoalies['hof'].value_counts(), autopct='%1.1f%%')
plt.axis('equal')
plt.show()


# ## Points
# The first area of investigation is the relationship of the career number of a hockey player's points - goals and assists - to hall of fame status.
# 
# The analysis shows that there is a statistically significant difference in the number of career points between hall of famers and non-hall of famers.
# 
# There also appears to be a growing number of points necessary to get into the Hall of Fame over the year.
# 
# Some additional future analysis could include t-tests for statistical significance of the points mean between hall of famers and non-hall of famers.

# In[ ]:


#Boxplot of points by Hall of Fame status and Era
sns.boxplot(x="hof", y="pts", hue="era", data=retiredNonGoalies);


# In[ ]:


#See if there is any variance in points by position
sns.boxplot(x="pos", y="pts", data=retiredNonGoalies);


# In[ ]:


#Plot between Points and era
sns.scatterplot(x="lastYear", y="pts", hue="era", data=retiredNonGoalies);


# In[ ]:


#Plot between Points and Year of last game
sns.scatterplot(x="lastYear", y="pts", hue="hof", data=retiredNonGoalies);


# ## Awards
# Awards also seem to strongly suggest differences between hall of fame and non-hall of fame players.
# 
# The number of career awards for those getting in the Hall of Fame is relatively stable over the years.

# In[ ]:


#Awards
sns.boxplot(x="hof", y="awards", hue="era", data=retiredNonGoalies);


# In[ ]:


#Plot between Awards and year of last game
sns.relplot(x="lastYear", y="awards", hue="era", data=retiredNonGoalies);


# In[ ]:


#Plot between Points and Year of last NHL game
sns.scatterplot(x="lastYear", y="awards", hue="hof", data=retiredNonGoalies);


# In[ ]:


#Awards for Goalies
players[(players.goalie == 1)].boxplot(column='awards', by='hof')


# ## Points and Awards

# In[ ]:


sns.relplot(x="pts", y="awards", hue="hof", data=retiredNonGoalies)


# In[ ]:


sns.relplot(x="pts", y="awards", hue="era", data=retiredNonGoalies)


# ## Years played in NHL
# There appears to be a difference between the number of years played in the NHL for hall of famers over non-hall of famers.

# In[ ]:


sns.boxplot(x="hof", y="yearsPlayedNHL", data=retiredNonGoalies);


# ## Years played in WHA

# In[ ]:


sns.boxplot(x="yearsPlayedWHA", y="pts", hue="hof", data=retiredNonGoalies);


# In[ ]:


players.loc[(players.yearsPlayedWHA==6) & (players.hof==1),:]


# # Modelling
# 
# I used a logistic regression to predict the relationship between hall of fame induction and points and awards.  It returned a very high accuracy on both the training and test data of about 98%, but because the hall of fame class is so imbalanced, the accuracy favours heavily predicting who will not be a hall of famer rather than predicting who will be a hall of famer.

# ### Common Functions

# In[ ]:


# Divide the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(retiredNonGoalies.loc[:, retiredNonGoalies.columns != 'hof'], retiredNonGoalies["hof"], test_size=0.2, random_state=34)

transform_pipe = Pipeline([
    ('scale', StandardScaler())
])

modelVariables = ['pts','awards','yearsPlayed','yearsPlayedNHL','yearsPlayedWHA','era_Founding 1917-1941','era_Original Six 1942-1967','era_Expansion 1968-1992','era_Modern 1993-']

def classifyFastAlgorithms(X, y, X_vars):
    parameters = {}
    classifiers = []
    classifiers.append(Pipeline([('transform_pipe', transform_pipe), ('lr', LogisticRegression(solver='lbfgs'))]))
    classifiers.append(Pipeline([('mnb', MultinomialNB())]))
    classifiers.append(Pipeline([('transform_pipe', transform_pipe), ('svc', SVC(gamma='auto', probability=True))]))
    classifiers.append(Pipeline([('transform_pipe', transform_pipe), ('rfc', RandomForestClassifier(n_estimators=100))]))
    #classifiers.append(Pipeline([('transform_pipe', transform_pipe), (KerasClassifier(build_fn=create_model, verbose=0, batch_size=500, epochs=5))]))
    
    for i in classifiers:
        estimate(i, parameters, X, y, X_vars)

    def create_model():
        nnmodel = Sequential()
        nnmodel.add(Dense(8, input_dim=2, activation='relu'))
        nnmodel.add(Dense(8, activation='relu'))
        nnmodel.add(Dense(8, activation='relu'))
        nnmodel.add(Dense(8, activation='relu'))
        nnmodel.add(Dense(1, activation='sigmoid'))
        nnmodel.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])
        return nnmodel
    
# Estimate Function
def estimate(estimator, parameters, X, y, X_vars):
    print("-----------------------------------------------------------------------------")
    print(estimator)
    print("")
    model = GridSearchCV(estimator, parameters, cv=StratifiedKFold(n_splits=5), iid=False, scoring="f1", n_jobs=-1)
    model.fit(X[X_vars], y)
    print("SCORER: %s; BEST SCORE: %r; BEST STD: %r" % (model.scorer_, model.best_score_, model.cv_results_['std_test_score'].item(0)))
    print("BEST PARAMETERS: %s" % (model.best_params_))
    print("")
    predict(model, X, y, X_vars)
    return model
    
#Predict using model
def predict(model, X, y, X_vars):
    y_pred = model.predict(X[X_vars])
    y_pred_prob = model.predict_proba(X[X_vars])
    print("Classification Report")
    print(classification_report(y, y_pred))
    print("")
    print("Confusion Matrix")
    print(confusion_matrix(y, y_pred))
    print("")
    print("Prediction Errors: False Negatives")
    print(X[(y==1) & (y_pred==0)].head())
    print("")
    print("Prediction Errors: False Positives")
    print(X[(y==0) & (y_pred==1)].head())
    print("-----------------------------------------------------------------------------")
    print("")
    data_with_predictions = X
    data_with_predictions.loc[:, 'predhof'] = y_pred
    data_with_predictions.loc[:, 'predhofprob'] = y_pred_prob[:,1]
    return data_with_predictions


# ### Quick Modelling
# I start off with doing some very quick modelling without any grid search for optimal parameters.
# 
# I also do some error analysis and found:
# * False Negatives:
#     * Many of the players from the oldest era of the league (starting in the NHL in 1917) without many points or awards.
# * False Positives:
#     * Players who had a significant career in the WHA
#     * Players who retired close to 2011 - the year of the dataset - and hence may just not have had the chance yet to get into the Hall of Fame.

# In[ ]:


classifyFastAlgorithms(X_train, y_train, modelVariables)


# ### Random Forest
# Random Forest is a promising model. It is tried in more detail with mulitple hyperparameter combinations.

# In[ ]:


pipeline_rf = Pipeline([
    ('transform_pipe', transform_pipe),
    ('rf', RandomForestClassifier())
])

parameters_rf = {
    'rf__n_estimators': [10, 100]
}

model_rf = estimate(pipeline_rf, parameters_rf, X_train, y_train, modelVariables)
print("RUNNING ON TEST DATASET")
predict(model_rf, X_test, y_test, modelVariables)
print("RESULTS RUNNING MODEL ON FULL DATASET")
players_preds_rf = predict(model_rf, nonGoalies, nonGoalies.loc[:, 'hof'], modelVariables)


# ### Logistic Regression
# Logistic Regression is tried in more detail with mulitple hyperparameter combinations.

# In[ ]:


pipeline_lr = Pipeline([
                        ('transform_pipe', transform_pipe),
                        ('lr', LogisticRegression(solver='lbfgs'))
                    ])

parameters_lr = {
                    'lr__C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
                    'lr__class_weight': [{0:1,1:1}, {0:1,1:10}, {0:1,1:100}]
                }

model_lr = estimate(pipeline_lr, parameters_lr, X_train, y_train, modelVariables)
print("RUNNING ON TEST DATASET")
predict(model_lr, X_test, y_test, modelVariables)
print("RESULTS RUNNING MODEL ON FULL DATASET")
players_preds_lr = predict(model_lr, nonGoalies, nonGoalies.loc[:, 'hof'], modelVariables)


# #### Predicted to be in Hall of Fame or is in the Hall of Fame

# In[ ]:


retiredPlayersPredictedHOF = Pipeline([
    ('playersPredictedHOF', PlayersPredictedHOF())
])

retiredPlayersPredictedHOF.fit_transform(players_preds_lr).sort_values(by=['predhofprob'], ascending=False)


# # Future Considerations
# I would like to run hall of fame predictions on the following:
# * Goalie hockery players.  The data is available in the dataset that I used for the non-goalies.
# * Hockey players that played mostly internationally
# * Women hockey players
