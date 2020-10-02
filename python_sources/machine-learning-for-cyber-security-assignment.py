#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# classifier models
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
# modules to handle data
import pandas as pd
import numpy as np


# In[ ]:


train = pd.read_csv( '../input/train.csv')
test = pd.read_csv( '../input/test.csv')


# In[ ]:


# save PassengerId for final submission
passengerId = test.PassengerId

# merge train and test
titanic = train.append(test, ignore_index=True)
# create indexes to separate data later on
train_idx = len(train)
test_idx = len(titanic) - len(test)


# In[ ]:


# view head of data 
titanic.head()


# In[ ]:


# get info on features
titanic.info()


# In[ ]:


# create a new feature to extract title names from the Name column
titanic['Title'] = titanic.Name.apply(lambda name: name.split(',')[1].split('.')[0].strip())


# In[ ]:


# normalize the titles
normalized_titles = {
    "Capt":       "Officer",
    "Col":        "Officer",
    "Major":      "Officer",
    "Jonkheer":   "Royalty",
    "Don":        "Royalty",
    "Sir" :       "Royalty",
    "Dr":         "Officer",
    "Rev":        "Officer",
    "the Countess":"Royalty",
    "Dona":       "Royalty",
    "Mme":        "Mrs",
    "Mlle":       "Miss",
    "Ms":         "Mrs",
    "Mr" :        "Mr",
    "Mrs" :       "Mrs",
    "Miss" :      "Miss",
    "Master" :    "Master",
    "Lady" :      "Royalty"
}


# In[ ]:


# map the normalized titles to the current titles 
titanic.Title = titanic.Title.map(normalized_titles)


# In[ ]:


# view value counts for the normalized titles
print(titanic.Title.value_counts())


# In[ ]:


# group by Sex, Pclass, and Title 
grouped = titanic.groupby(['Sex','Pclass', 'Title']) 


# In[ ]:


# view the median Age by the grouped features 
grouped.Age.median()


# In[ ]:


# apply the grouped median value on the Age NaN
titanic.Age = grouped.Age.apply(lambda x: x.fillna(x.median()))


# In[ ]:


# fill Cabin NaN with U for unknown
titanic.Cabin = titanic.Cabin.fillna('U')
# find most frequent Embarked value and store in variable
most_embarked = titanic.Embarked.value_counts().index[0]

# fill NaN with most_embarked value
titanic.Embarked = titanic.Embarked.fillna(most_embarked)
# fill NaN with median fare
titanic.Fare = titanic.Fare.fillna(titanic.Fare.median())

# view changes
titanic.info()


# In[ ]:


# size of families (including the passenger)
titanic['FamilySize'] = titanic.Parch + titanic.SibSp + 1


# In[ ]:


# map first letter of cabin to itself
titanic.Cabin = titanic.Cabin.map(lambda x: x[0])


# In[ ]:


# Convert the male and female groups to integer form
titanic.Sex = titanic.Sex.map({"male": 0, "female":1})
# create dummy variables for categorical features
pclass_dummies = pd.get_dummies(titanic.Pclass, prefix="Pclass")
title_dummies = pd.get_dummies(titanic.Title, prefix="Title")
cabin_dummies = pd.get_dummies(titanic.Cabin, prefix="Cabin")
embarked_dummies = pd.get_dummies(titanic.Embarked, prefix="Embarked")
# concatenate dummy columns with main dataset
titanic_dummies = pd.concat([titanic, pclass_dummies, title_dummies, cabin_dummies, embarked_dummies], axis=1)

# drop categorical fields
titanic_dummies.drop(['Pclass', 'Title', 'Cabin', 'Embarked', 'Name', 'Ticket'], axis=1, inplace=True)

titanic_dummies.head()


# In[ ]:


# create train and test data
train = titanic_dummies[ :train_idx]
test = titanic_dummies[test_idx: ]

# convert Survived back to int
train.Survived = train.Survived.astype(int)
# create X and y for data and target values 
X = train.drop('Survived', axis=1).values 
y = train.Survived.values
# create array for test set
X_test = test.drop('Survived', axis=1).values


# In[ ]:


# create param grid object 
forrest_params = dict(     
    max_depth = [n for n in range(9, 14)],     
    min_samples_split = [n for n in range(4, 11)], 
    min_samples_leaf = [n for n in range(2, 5)],     
    n_estimators = [n for n in range(10, 60, 10)],
)


# In[ ]:


# instantiate Random Forest model
forrest = RandomForestClassifier()


# In[ ]:


# build and fit model 
forest_cv = GridSearchCV(estimator=forrest,     param_grid=forrest_params, cv=5) 
forest_cv.fit(X, y)


# In[ ]:


print("Best score: {}".format(forest_cv.best_score_))
print("Optimal params: {}".format(forest_cv.best_estimator_))


# In[ ]:


# random forrest prediction on test set
forrest_pred = forest_cv.predict(X_test)


# In[ ]:


# dataframe with predictions
kaggle = pd.DataFrame({'PassengerId': passengerId, 'Survived': forrest_pred})


# In[ ]:


kaggle.to_csv("TitanicForSLIITCyberML.csv", index=False)


# In[ ]:




