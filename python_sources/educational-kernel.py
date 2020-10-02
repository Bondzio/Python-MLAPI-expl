#!/usr/bin/env python
# coding: utf-8

# # Introduction
# this notebook is especially for beginners in data science.
# in this course, you will find the visualization of titanic dataset data, 
# simple prediction models and also the hard prediction models with score 
# improvement techniques, and also the Ensembling/Stacking between several models.

# # competition goal
# the goal of the competition is to create a model that predicts which passengers survived the Titanic shipwreck.

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

from matplotlib import pyplot as plt
import seaborn as sns
import pylab as plot
import re as re


# # Part 1 : data preparation / cleaning
# in this part, we will explore the available data, identify possible opportunities for functionality engineering as well as numerically code all categorical functionalities.

# In[ ]:


# Load in the train and test datasets
train = pd.read_csv('../input/titanic/train.csv')
test = pd.read_csv('../input/titanic/test.csv')


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


id_train=train['PassengerId']
train.drop('PassengerId',inplace=True,axis=1)
id_test=test['PassengerId']
test.drop('PassengerId',inplace=True,axis=1)


# In[ ]:


train.info()


# In[ ]:


#some feature statistics
train.describe()


# In[ ]:





# In[ ]:


#Visualizing survival based on the gender.
train['Died'] = 1 - train['Survived']
train.groupby('Sex').agg('sum')[['Survived', 'Died']].plot(kind='bar', figsize=(20, 6),
                                                          stacked=True, colors=['b', 'R']);
train.drop('Died',inplace=True,axis=1)


# this graph given us two important information: the number of men is doubled compared to the number of women, and the rate of women surviving is higher than men

# In[ ]:


#Visualizing survival based on the age and sex
fig = plt.figure(figsize=(20, 5))
sns.violinplot(x='Sex', y='Age', 
               hue='Survived', data=train, 
               split=True,
               palette={0: "r", 1: "b"}
              );


# 
# * Younger male tend to survive
# * A large number of passengers between 20 and 40 die
# * The age doesn't seem to have a direct impact on the female survival

# In[ ]:


#Visualizing survival based on the fare ticket
figure = plt.figure(figsize=(25, 7))
plt.hist([train[train['Survived'] == 1]['Fare'], train[train['Survived'] == 0]['Fare']], 
         stacked=True, color = ['b','r'],
         bins = 50, label = ['Survived','Dead'])
plt.xlabel('Fare')
plt.ylabel('Number of passengers')
plt.legend();


# * Passengers with cheaper ticket fares are more likely to die.

# In[ ]:


#Visualizing survival based on the embarkation.

fig = plt.figure(figsize=(20, 5))
sns.violinplot(x='Embarked', y='Fare', hue='Survived', data=train, split=True, palette={0: "r", 1: "b"});


# * The embarkation C have a wider range of fare tickets and therefore the passengers who pay the highest prices are those who survive.

# In[ ]:


full_data = [train, test]


# In[ ]:


#title of people
def get_title(name):
    title_search = re.search(' ([A-Za-z]+)\.', name)
    # If the title exists, extract and return it.
    if title_search:
        return title_search.group(1)
    return ""

for dataset in full_data:
    dataset['Title'] = dataset['Name'].apply(get_title)


# In[ ]:


train.head(10)


# In[ ]:


train.Title.unique()


# *   now let's clean the data and map the features into numerical values.

# In[ ]:


train.info()


# In[ ]:


for dataset in full_data:
    #replace missing values 
    dataset['Age'] = dataset['Age'].fillna(dataset['Age'].median())
    dataset['Embarked'] = dataset['Embarked'].replace(np.NAN,'C')

    # Mapping Sex
    dataset['Sex'] = dataset['Sex'].map( {'female': 0, 'male': 1} ).astype(int)
    
    # Mapping titles
    title_mapping = {'Mr': 1, 'Mrs': 2, 'Miss' : 3, 'Master' : 4, 'Don' : 5, 'Rev' : 6, 'Dr' : 7, 'Mme' : 8, 'Ms' : 9,
       'Major' : 10, 'Lady' : 11 , 'Sir' : 12, 'Mlle' : 13, 'Col' : 14, 'Capt' : 15, 'Countess' : 16,
       'Jonkheer' : 17}
    dataset['Title'] = dataset['Title'].map(title_mapping)
    dataset['Title'] = dataset['Title'].fillna(0)
    
    # Mapping Embarked
    dataset['Embarked'] = dataset['Embarked'].map( {'S': 0, 'C': 1, 'Q': 2} ).astype(int)
    
    


# * the cabin attribute means that we have a people with the cabin and others without (NaN) and the letter that begins the cabin code makes the difference between cabins, so, we will extract this letter and map the cabin attribute

# In[ ]:


for dataset in full_data:
    dataset['Cabin']=dataset['Cabin'].replace(np.NAN,'Z')   
    dataset['Cabin']=dataset['Cabin'].astype(str).str[0]
    dataset['Cabin'] = dataset['Cabin'].map( {'Z': 0, 'C' : 1, 'E': 2, 'G': 3, 'D' : 4, 'A' : 5, 'B': 6, 'F': 7, 'T': 8} ).astype(int)

    


# In[ ]:


drop_elements = ['Name', 'Ticket']
train = train.drop(drop_elements, axis = 1)
test = test.drop(drop_elements, axis = 1)


# In[ ]:


train.info(),test.info()


# In[ ]:


test['Fare']=test['Fare'].replace(np.NaN,float(test['Fare'].max()))
test['Title']=test['Title'].astype(int)


# # Basic models 

# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score, log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression

classifiers = [
    KNeighborsClassifier(3),
    DecisionTreeClassifier(),
    GaussianNB(),
    LinearDiscriminantAnalysis(),
    QuadraticDiscriminantAnalysis(),
    LogisticRegression()]

log_cols = ["Classifier", "Accuracy"]
log  = pd.DataFrame(columns=log_cols)

#croose validation
sss = StratifiedShuffleSplit(n_splits=10, test_size=0.1, random_state=0)
train = train.values
X = train[0::, 1::]
y = train[0::, 0]

acc_dict = {}

for train_index, test_index in sss.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    for clf in classifiers:
        name = clf.__class__.__name__
        clf.fit(X_train, y_train)
        train_predictions = clf.predict(X_test)
        acc = accuracy_score(y_test, train_predictions)
        if name in acc_dict:
            acc_dict[name] += acc
        else:
            acc_dict[name] = acc

for clf in acc_dict:
    acc_dict[clf] = acc_dict[clf] / 10.0
    log_entry = pd.DataFrame([[clf, acc_dict[clf]]], columns=log_cols)
    log = log.append(log_entry)

plt.xlabel('Accuracy')
plt.title('Classifier Accuracy')

sns.set_color_codes("muted")
sns.barplot(x='Accuracy', y='Classifier', data=log, color="b")


# the best scores is : decisionTree 

# In[ ]:


sub=pd.read_csv('../input/titanic/gender_submission.csv')


# In[ ]:


#best parameters for decision_tree 

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

for train_index, test_index in sss.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
param_grid = { 
    "criterion" : ["gini", "entropy"], 
    "min_samples_leaf" : [1, 5, 10, 25, 50, 70], 
    "min_samples_split" : [2, 4, 10, 12, 16, 18, 25, 35]}

dt = DecisionTreeClassifier()

#clf = GridSearchCV(rf, param_grid=param_grid, n_jobs=-1)
clf = RandomizedSearchCV(dt, param_grid, n_jobs=-1)
 
clf.fit(X_train, y_train)
 
print(clf.best_estimator_)


# In[ ]:


#make prediction using decsionTree
model = clf.best_estimator_
model.fit(train[0::, 1::], train[0::, 0])
ts  = test.values
result = model.predict(ts)
sub['Survived']=result
sub['Survived']=sub['Survived'].astype(int)
sub.to_csv('decisiontree_submission.csv',index=False)


# In[ ]:





# # Hard models

# In[ ]:



#best parameters random_forest
for train_index, test_index in sss.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
param_grid = { 
    "criterion" : ["gini", "entropy"], 
    "min_samples_leaf" : [1, 5, 10, 25, 50, 70], 
    "min_samples_split" : [2, 4, 10, 12, 16, 18, 25, 35], 
    "n_estimators": [100, 400, 700, 1000, 1500]}

rf = RandomForestClassifier(n_estimators=100, max_features='auto', oob_score=True, random_state=1, n_jobs=-1)

#clf = GridSearchCV(rf, param_grid=param_grid, n_jobs=-1)
clf = RandomizedSearchCV(rf, param_grid, n_jobs=-1)
 
clf.fit(X_train, y_train)
print(clf.best_estimator_)


# In[ ]:



#cross validation for random_forest
from sklearn.ensemble import RandomForestClassifier
random_forest =clf.best_estimator_
random_forest.fit(X_train, y_train)

Y_pred  = random_forest.predict(X_test)

random_forest.score(X_train, y_train)
acc_random_forest = round(random_forest.score(X_train, y_train)*100, 2)

print (acc_random_forest)


# In[ ]:



#make prediction using randomforest
random_forest.fit(train[0::, 1::], train[0::, 0])
ts  = test.values
result = random_forest.predict(ts)
sub['Survived']=result
sub['Survived']=sub['Survived'].astype(int)
sub.to_csv('random_forest_submission.csv',index=False)


# In[ ]:



import xgboost as xgb
from xgboost import XGBClassifier
for train_index, test_index in sss.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

#best parameters for xgboost
params = {
        'min_child_weight': [1, 5, 10],
        'gamma': [0.5, 1, 1.5, 2, 5],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0],
        'max_depth': [3, 4, 5]
        }
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

xgb = XGBClassifier(learning_rate=0.02, n_estimators=600,
                    silent=True, nthread=1)

clf = GridSearchCV(xgb, param_grid=params)
#clf = RandomizedSearchCV(xgb, param_grid, n_jobs=-1)
 
clf.fit(X_train, y_train)

print(clf.best_estimator_)


# In[ ]:





# In[ ]:



#cross validation for XGboost
xgb = clf.best_estimator_
xgb.fit(X_train, y_train)

Y_pred  = xgb.predict(X_test)

xgb.score(X_train, y_train)
acc_xgb = round(xgb.score(X_train, y_train)*100, 2)

print (acc_xgb)


# In[ ]:


#make prediction using randomforest
xgb.fit(train[0::, 1::], train[0::, 0])
ts  = test.values
result = xgb.predict(ts)
sub['Survived']=result
sub['Survived']=sub['Survived'].astype(int)
sub.to_csv('Xgboost_submission.csv',index=False)


# you can try other hard models such as : LGBM,Adaboost,catboost,NN........
# * thanks to : [Introduction to Ensembling/Stacking in Python](https://www.kaggle.com/arthurtok/introduction-to-ensembling-stacking-in-python/output)
# * [Titanic best working Classifier
# ](https://www.kaggle.com/sinakhorami/titanic-best-working-classifier)
# * [Data Visualization - Titanic survival](https://www.kaggle.com/usharengaraju/data-visualization-titanic-survival)
