#!/usr/bin/env python
# coding: utf-8

# **This is an attempt to Kaggle's Titanic competition. I hope you enjoy it!**

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# ### Modules

# In[ ]:


import os
from pandas import Series, DataFrame

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

from sklearn.metrics import confusion_matrix

from sklearn import preprocessing
from sklearn.feature_selection import SelectFromModel
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import StratifiedKFold

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

from sklearn import neighbors as grid_search

import statsmodels.api as sm
import statsmodels.formula.api as smf

get_ipython().run_line_magic('matplotlib', 'inline')

print('Modules loaded')


# ### Import data

# In[ ]:


titanic = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')

### Explore and edit input files ###
titanic.head()
titanic.dtypes

test.head()
test.dtypes

titanic.info()
print('o+o+o+o+o+o+o+o')
test.info()


# In[ ]:


os.getcwd()


# In[ ]:


fig = plt.figure(figsize=(9,4))
#
plt.subplot2grid((1,3), (0,0))
sns.countplot(x='Survived', data=titanic)
plt.subplot2grid((1,3), (0,1))
sns.countplot(x='Embarked', hue='Pclass', data=titanic)
plt.subplot2grid((1,3), (0,2))
sns.countplot(x='Survived', hue='Embarked', data=titanic)


# In[ ]:


#For some reason there is a higher survival rate for the passengers embarked in C. Perhpas is an artefact 
#related either to the number of passengers embarked (less representative sample) or the fares paid (more rich passengers 
#embarking here or there. See Pclass analysis below)

embark_percent_titanic = titanic[['Embarked', 'Survived']].groupby(['Embarked'],as_index=False).mean()
#
sns.barplot(x='Embarked', y='Survived', data=embark_percent_titanic,order=['S','C','Q'])


# In[ ]:


#Embarking port should not have any prediction power per se, but let's leave it just
#in case and create some dummy variables
embark_dummies_titanic  = pd.get_dummies(titanic['Embarked'])
titanic = titanic.join(embark_dummies_titanic)
#titanic = titanic.drop(['Embarked'], axis=1, inplace=True)
embark_dummies_test  = pd.get_dummies(test['Embarked'])
test = test.join(embark_dummies_test)


# ### Fare

# In[ ]:


#Average fare for survivors and victims
mean_fare_survive = titanic[['Fare', 'Survived']].groupby(['Survived']).mean()#Histograms of fares
plt.hist(titanic['Fare'],bins=25)


# In[ ]:


##Histograms of fares and other plots
fig = plt.figure(figsize=(20,10))
#
plt.subplot2grid((2,1), (0,0))
plt.hist(titanic['Fare'],bins=25, log=True) #Log turned on just to exagerate the less frequent values
plt.subplot2grid((2,3), (1,0))
sns.boxplot(x='Survived', y='Fare', data=titanic)
plt.subplot2grid((2,3), (1,1))
sns.boxplot(x='Survived', y=np.log(titanic.Fare), data=titanic) ##Log turned on just for exageration
plt.subplot2grid((2,3), (1,2))
sns.violinplot(x='Survived', y='Fare', data=titanic)


# ### Age

# In[ ]:


survived_age = titanic[titanic.Survived == 1].Age
dead_age = titanic[titanic.Survived == 0].Age


# In[ ]:


##Histograms and other plots
fig = plt.figure(figsize=(20,10))
#
plt.subplot2grid((1,2), (0,0))
#plt.hist([survived_age, dead_age], stacked=True, align='left', range=(0,100), color = ['b','r'], bins=100)
plt.hist(titanic['Age'], align='left', range=(0,100), bins=100)
plt.subplot2grid((1,2), (0,1))
sns.violinplot(x='Survived', y='Age', data=titanic, ylim=(0,100))


# In[ ]:


#Notice that the survival rate of children (<15 y) and old people (>60 y)
#We should perhaps separate these two groups and make an indicator variable for each. *See Sex category below


# In[ ]:


#Parents and children
survived_Parch = titanic[titanic.Survived == 1].Parch.dropna()
dead_Parch = titanic[titanic.Survived == 0].Parch.dropna()

titanic['ParchIO'] = titanic['Parch']
titanic['ParchIO'].loc[titanic['Parch'] > 0] = 1
titanic['ParchIO'].loc[titanic['Parch'] == 0] = 0
Parch_percent = titanic[['Survived', 'ParchIO']].groupby(['ParchIO'], as_index=False).mean()

test['ParchIO'] = test['Parch']
test['ParchIO'].loc[test['Parch'] > 0] = 1
test['ParchIO'].loc[test['Parch'] == 0] = 0

fig = plt.figure(figsize=(20,7))
#
plt.subplot2grid((1,2), (0,0))
plt.hist([survived_Parch, dead_Parch], stacked=True, align='left', range=(0,10), bins=10)
plt.subplot2grid((1,2), (0,1))
sns.barplot(x='ParchIO', y='Survived', data=Parch_percent)


# In[ ]:


#Siblings and spouse
survived_SibSp = titanic[titanic.Survived == 1].SibSp.dropna()
dead_SibSp = titanic[titanic.Survived == 0].SibSp.dropna()

titanic['SibSpIO'] = titanic.SibSp
titanic['SibSpIO'].loc[titanic['SibSp'] > 0] = 1
titanic['SibSpIO'].loc[titanic['SibSp'] == 0] = 0
SibSp_percent = titanic[['Survived', 'SibSpIO']].groupby(['SibSpIO'], as_index=False).mean()

test['SibSpIO'] = test.SibSp
test['SibSpIO'].loc[test['SibSp'] > 0] = 1
test['SibSpIO'].loc[test['SibSp'] == 0] = 0

fig = plt.figure(figsize=(20,7))
#
plt.subplot2grid((1,2), (0,0))
plt.hist([survived_SibSp, dead_SibSp], stacked=True, align='left', range=(0,10), bins=10)
plt.subplot2grid((1,2), (0,1))
sns.barplot(x='SibSpIO', y='Survived', data=SibSp_percent)


# In[ ]:


#Combining the two '''Let's start with a simple case and just use the column FamilyIO, ie. traveling alone or accompanied.'''
titanic['Family'] = titanic.Parch + titanic.SibSp
test['Family'] = test.Parch + test.SibSp

survived_Family = titanic[titanic.Survived == 1].Family.dropna()
dead_Family = titanic[titanic.Survived == 0].Family.dropna()

#Convert to binary variable
titanic['FamilyIO'] = titanic.Family
titanic['FamilyIO'].loc[titanic['FamilyIO'] > 0] = 1
titanic['FamilyIO'].loc[titanic['FamilyIO'] == 0] = 0

survived_FamilyIO = titanic[titanic.Survived == 1].FamilyIO.dropna()
dead_FamilyIO = titanic[titanic.Survived == 0].FamilyIO.dropna()

family_percent = titanic[['Survived', 'FamilyIO']].groupby(['FamilyIO'], as_index=False).mean()

test['FamilyIO'] = test.Family
test['FamilyIO'].loc[test['FamilyIO'] > 0] = 1
test['FamilyIO'].loc[test['FamilyIO'] == 0] = 0

fig = plt.figure(figsize=(20,7))
#
plt.subplot2grid((1,3), (0,0))
plt.hist([survived_FamilyIO, dead_FamilyIO], stacked=True, bins=2)
plt.subplot2grid((1,3), (0,1))
sns.countplot(x='FamilyIO', data=titanic)
plt.subplot2grid((1,3), (0,2))
sns.barplot(x='FamilyIO', y='Survived', data=family_percent)


# In[ ]:


### Sex


# In[ ]:


'''Shall we distinguish between males, females and children?
What is a children? Less than 12, 14, 16?
Let's start with the assumption that children means less than 12'''

titanic['MaleFemale'] = titanic.Sex
titanic['MaleFemale'].loc[titanic.Age <=15] = 'child'
titanic['MaleFemale'].loc[(titanic.Age >=60) & (titanic.Sex == 'male')] = 'oldman'
titanic['MaleFemale'].loc[(titanic.Age >=60) & (titanic.Sex == 'female')] = 'oldwoman'
Sex_percent = titanic[['Survived', 'MaleFemale']].groupby(['MaleFemale'], as_index=False).mean()

'''We should also try to understand if there is a correlation between sex and traveling alone
We could try that later on'''

fig = plt.figure(figsize=(20,20))
#
plt.subplot2grid((2,2), (1,0))
sns.barplot(x='MaleFemale', y='Survived', data=Sex_percent)
plt.subplot2grid((2,2), (1,1))
sns.countplot(x='MaleFemale', data=titanic)


# In[ ]:


#There are not too many samples for older men and women (>60 y), so I have doubts about increasing the complexity 
#of the model.
#Let's keep it simple for now...

titanic['MaleFemale'].loc[(titanic.MaleFemale == 'oldman')] = 'male'
titanic['MaleFemale'].loc[(titanic.MaleFemale == 'oldwoman')] = 'female'


#Add dummies variable
sex_dummies_titanic = pd.get_dummies(titanic.MaleFemale)
titanic = titanic.join(sex_dummies_titanic)

test['MaleFemale'] = test.Sex
test['MaleFemale'].loc[(test.Age <=15)] = 'child'
sex_dummies_test = pd.get_dummies(test.MaleFemale)
test = test.join(sex_dummies_test)


# In[ ]:


print(sex_dummies_titanic.head())
titanic.head()


# ### Pclass

# In[ ]:


'''The class can be a proxy for the fare paid, which seems to have an effect. 
Let's investigate the class of travel and if it shows some similarities to the 
fares variables, we will discard the latter nd use Pclass in the initial prediction attempt'''

fig, (axis1, axis2) = plt.subplots(1, 2, figsize=(10, 5))
sns.barplot(x='Pclass', y='Fare', data=titanic, ax=axis1)
sns.barplot(x='Pclass', y='Survived', data=titanic, ax=axis2)

Pclass_dummies_titanic = pd.get_dummies(titanic.Pclass, prefix='clas')
titanic = titanic.join(Pclass_dummies_titanic)

Pclass_dummies_test = pd.get_dummies(test.Pclass, prefix='clas')
test = test.join(Pclass_dummies_test)


# ### Conclusions from preliminary analysis
# From the charts and the preliminary analysis, we could say a few things:<br><br>
# -o- Embarkment port: It is not directly correlated with survival... why would it be? However, there is a higher proportion of 1st class passengers boarding on 'C' than in the other ports. At the end, it might be class of travel the real difference, more than the actual geography.<br>
# -o- Sex: being female was an advantage, probably because of the priority in accessing the lifeboats. Men have a considerable lower survival rate than men<br>
# -o- Age: children have also a higher survival rate than male adults, but after 60 y.o. survival decreases dramatically, even if the population of >60 is very low.<br>
# -o- Family members: having family members was a clear advantage. Either if it was having a parents/children or siblings/spouse on board. Perhaps to do both withthe dnamics of the evacuation and with family solidarity <br>
# -o- Cabin: large number of NaNs, so we will ignore for a while. However, there is room for some information there. Could these numbers tell something about the location of the cabin? Could the fare or the class be a proxy for cabin location and somehow the effect of lacking the cabin location is minimised? <br>
# -o- Class: traveling 1st class was a clear advantage, to a lesser degree 2nd class too. 3rd class was a clear disadvantage, either due to their cabin location or to a lower priority during the evacuation.<br>
# -o- Fare: I assume it would have been correlated to the class very strongly and to simplify, I leave it out for now.

# ### Dataframe edition
# 
# Now let's see our dataframe and make it ready for analysis

# In[ ]:


titanic.info()


# In[ ]:


titanic.Age.describe()


# In[ ]:


#titanic.csv: two missing values in 'embarked', a few more in 'age'
titanic['Embarked'] = titanic['Embarked'].fillna('S')
test.Embarked = test.Embarked.fillna('S')
#Let's fill the missing ages with samples from a ditribution based on the 714 age values present
#We could use the median, or relate the age to the title (Mr., Mrs., Miss). I chose to sample random values
#according to a distribution
#np.random.normal(loc=26.7, scale=14.5)
nan_mask1 = np.isnan(titanic.Age)
titanic.Age[nan_mask1] = np.random.randint(0, high=80, size=np.count_nonzero(nan_mask1))
nan_mask2 = np.isnan(test.Age)
test.Age[nan_mask2] = np.random.randint(0, high=80, size=np.count_nonzero(nan_mask2))


# In[ ]:


titanic.Age.describe()
plt.hist(titanic.Age, align='left', range=(0,100), bins=100)


# In[ ]:


titanic.head()


# In[ ]:


titanic.info()
print('---------')
test.info()


# We need to drop the columns that we consider either:<br><br>
# 1) Irrelevant / No prediction power or <br>
# 2) No needed for our required level of complexity. <br><br>
# I will leave the embarking port for now, even if this variable could be rather correlated to some other, or mean nothing too. <br><br>
# Simplifications for initial attempt:<br><br>
# --keep separate Parch and SibSp dummy variables<br>
# --Ignore age <br>
# --keep explicit variables for Pclass=3 and for 'child'

# In[ ]:


features = ['PassengerId', 'Pclass', 'Name', 'Sex', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked', 'Family', 'MaleFemale']
titanic = titanic.drop(features, axis=1)
test = test.drop(features, axis=1)


# In[ ]:


titanic.head()


# In[ ]:


test.head()


# ### Analysis
# 
# First let's define a function for extracting the fitting scores fo the different models\
# Extracted from the model written by the Kaggle user 'vinceallenvince' (THANKS)

# In[ ]:


def check_classifiers(X, y):
    """
    Returns a sorted list of accuracy scores from fitting and scoring passed data
    against several alogrithms.
    """
    _cv = 4
    classifier_score = {}
    
    scores = cross_val_score(LogisticRegression(), X, y, cv=_cv)
    classifier_score['LogisticRegression'] = scores.mean()
    
    scores = cross_val_score(KNeighborsClassifier(), X, y, cv=_cv)
    classifier_score['KNeighborsClassifier'] = scores.mean()
    
    scores = cross_val_score(RandomForestClassifier(), X, y, cv=_cv)
    classifier_score['RandomForestClassifier'] = scores.mean()
    
    scores = cross_val_score(SVC(), X, y, cv=_cv)
    classifier_score['SVC'] = scores.mean()
    
    scores = cross_val_score(GaussianNB(), X, y, cv=_cv)
    classifier_score['GaussianNB'] = scores.mean()

    #return sorted(classifier_score.items(), key=operator.itemgetter(1), reverse=True)
    return sorted(classifier_score.items(), reverse=True)


# In[ ]:


titanic['nullhyp'] = 0
titanic.head()


# In[ ]:


features = ['nullhyp']
X_train = titanic[features]
y_train = titanic.Survived

check_classifiers(X_train, y_train)


# In[ ]:


model_lr1 = LogisticRegression()
model_lr1.fit(X_train, y_train)


# In[ ]:


print(model_lr1.intercept_)
model_lr1.coef_


# In[ ]:


#Let's get the odds by applying the exponential
print(np.exp(model_lr1.intercept_))
np.exp(model_lr1.coef_)


# In[ ]:


confusion_matrix(y_train, model_lr1.predict(X_train))


# We can see how the scores of the models = 0.61, representing the actual proportion of survivors and victims.
# The confusion matrix also represents this, with 342 false negatives (actual survivors) and 549 true negatives (actual victims). 
# 
# ### Statistical models using the available data
# 
# Using all the available features...

# In[ ]:


#features = ['C', 'Q', 'S', 'Age', 'ParchIO', 'SibSpIO', 'child', 'female', 'male', 'oldman', 'oldwoman', 'clas_1', 'clas_2', 'clas_3']
features = ['C', 'Q', 'S', 'Age', 'ParchIO', 'SibSpIO', 'child', 'female', 'male', 'clas_1', 'clas_2', 'clas_3']
X_train = titanic[features]
y_train = titanic.Survived

check_classifiers(X_train, y_train)


# Simplifying the model, aiming at using the variables that should have greater impact... <br>
# No ports of embarkment, merging of SibSp and Parch, no redundant variables (male and clas_3)

# In[ ]:


#features = ['C', 'Q', 'S', 'Age', 'ParchIO', 'SibSpIO', 'child', 'female', 'male', 'oldman', 'oldwoman', 'clas_1', 'clas_2', 'clas_3']
features = ['Age', 'FamilyIO', 'child', 'female', 'clas_1', 'clas_2']
X_train = titanic[features]
y_train = titanic.Survived

check_classifiers(X_train, y_train)


# We see that the scores do not diminish significantly, and even increase for certain algorithms

# #### **Logistic regression using sklearn**

# In[ ]:


model_lr1 = LogisticRegression(C=1e4)
model_lr1.fit(X_train, y_train)


# In[ ]:


print(model_lr1.intercept_)
model_lr1.coef_


# In[ ]:


#Let's get the odds by applying the exponential
print(np.exp(model_lr1.intercept_))
np.exp(model_lr1.coef_)


# In[ ]:


confusion_matrix(y_train, model_lr1.predict(X_train))


# In[ ]:


model_lr1.score(X_train, y_train)


# #### **Random Forest Classifier**
# 
# I noticed that the score improved slightly by including the Parch and SibSp variables separately. *emphasized text*

# In[ ]:


#features = ['C', 'Q', 'S', 'Age', 'ParchIO', 'SibSpIO', 'child', 'female', 'male', 'clas_1', 'clas_2', 'clas_3']
features = ['Age', 'ParchIO', 'SibSpIO', 'child', 'female', 'male', 'clas_1', 'clas_2', 'clas_3']
X_train = titanic[features]
y_train = titanic.Survived

check_classifiers(X_train, y_train)


# In[ ]:


model_rf1 = RandomForestClassifier(n_estimators=100)
model_rf1.fit(X_train, y_train)


# In[ ]:


confusion_matrix(y_train, model_rf1.predict(X_train))


# In[ ]:


importance = pd.DataFrame(model_rf1.feature_importances_)
features_df = pd.DataFrame(features)
Feature_importance = pd.concat([features_df, importance], axis=1)

Feature_importance


# In[ ]:


model_rf1.score(X_train, y_train)


# In[ ]:


model_rf1.classes_


# ### Predictions

# In[ ]:


test.head()


# In[ ]:


features = ['Age', 'ParchIO', 'SibSpIO', 'child', 'female', 'male', 'clas_1', 'clas_2', 'clas_3']
X_test = test[features]


# In[ ]:


prediction = model_rf1.predict(X_test)


# In[ ]:


prediction


# In[ ]:


#join the predictions to the dataframe


# In[ ]:


testx = pd.read_csv('../input/test.csv')
testx.head()


# In[ ]:


#features = ['C', 'Q', 'S', 'Age', 'ParchIO', 'SibSpIO', 'child', 'female', 'male', 'clas_1', 'clas_2', 'clas_3']
print(testx.columns)
print(test.columns)


# A full dataframe in case we want to explore the results...

# In[ ]:


test_prediction = pd.DataFrame({'PassengerId': testx['PassengerId'],
                  'Pclass': testx['Pclass'],
                  'Name': testx['Name'],
                  'Sex': testx['Sex'],
                  'Age': testx['Age'],
                  'SibSp': testx['SibSp'],
                  'Parch': testx['Parch'],
                  'Fare': testx['Fare'],
                  'Embarked': testx['Embarked'],
                  'Survived': prediction})


# In[ ]:


test_prediction


# In[ ]:


model_rf1.predict_proba(X_train)


# In[ ]:


test_prediction.Survived.describe()


# **Our prediction using the model tell us that 36% of the remaining passengers (on the test file) survived. This is consistent with the ca. 39% of passengers that survived in the train file.**

# In[ ]:


submission = test_prediction[['PassengerId', 'Survived']]
print('Done!')
submission.to_csv("submission_tawonque.csv",index=False)

