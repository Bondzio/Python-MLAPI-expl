#!/usr/bin/env python
# coding: utf-8

# In[ ]:





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


# In[ ]:


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
sns.set()


# In[ ]:


train = pd.read_csv('../input/train.csv')
train.head()


# In[ ]:


train.describe()


# In[ ]:


test = pd.read_csv('../input/test.csv')
test.head()


# In[ ]:


test.describe()


# # Let's see if we have missing data

# In[ ]:


sns.heatmap(train.isnull(), cbar=False, cmap='plasma', yticklabels=False)


# We can replace missing age with averaga age. for that we need to learn more about our data  
# 
# As for cabin we will need to drop it since we can't do much about it

# In[ ]:


sns.countplot(x='Survived', data=train, hue='Sex')
# It seems more woman survied than man


# In[ ]:


sns.countplot(x='Survived', data=train, hue='Pclass')
# there is correlation between Passnger class and survival 
# majority of people died are from Pclass 3


# In[ ]:


sns.boxplot(x='Pclass', y='Age', data=train)
# older people could effort better class
# Therefore we will replace missing age values with average age of each passnger class 


# In[ ]:


mean_ages = train.groupby('Pclass')['Age'].mean()
mean_ages


# In[ ]:


def impute_age(cols):
    age = cols['Age']
    pclass = cols['Pclass']

    if pd.isnull(age):
        if pclass == 1:
            return 38
        elif pclass == 2:
            return 29
        else:
            return 25
    else:
        return age

def impute_fare(cols):
    fare = cols['Fare']
    pclass = cols['Pclass']

    if pd.isnull(fare):
        if pclass == 1:
            return 84
        elif pclass == 2:
            return 20
        else:
            return 13
    else:
        return fare


# In[ ]:


train['Age'] = train[['Age', 'Pclass']].apply(impute_age, axis=1)
test['Age'] = test[['Age', 'Pclass']].apply(impute_age, axis=1)
test['Fare'] = test[['Fare', 'Pclass']].apply(impute_fare, axis=1)


# In[ ]:


gender = pd.get_dummies(train['Sex'], drop_first=True)
gender_test = pd.get_dummies(test['Sex'], drop_first=True)


# In[ ]:


embark = pd.get_dummies(train['Embarked'], drop_first=True)
embark_test = pd.get_dummies(test['Embarked'], drop_first=True)


# In[ ]:


pass_class = pd.get_dummies(train['Pclass'], drop_first=True)
pass_class_test = pd.get_dummies(test['Pclass'], drop_first=True)
train.head()


# In[ ]:


train.drop(['Cabin','Sex', 'Embarked','Name','Ticket', 'PassengerId', 'Pclass'], axis=1, inplace=True)
pass_id = test['PassengerId']
test.drop(['Cabin', 'Sex', 'Embarked','Name','Ticket', 'PassengerId', 'Pclass'], axis=1, inplace=True)
train.head()


# In[ ]:


train = pd.concat([train, gender, embark, pass_class], axis=1)
test = pd.concat([test, gender_test, embark_test, pass_class_test], axis=1)
train.head(10)


# In[ ]:


sns.heatmap(train.isnull(), cmap='plasma')


# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB


# In[ ]:


from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
k_fold = KFold(n_splits=10, shuffle=True, random_state=42)


# In[ ]:


# train = train.dropna(inplace=True)
# test = test.dropna(inplace=True)
X = train.drop(['Survived', 'Fare'], axis=1)
y = train['Survived']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y)
X.head()


# In[ ]:


# sns.pairplot(train)
print()


# ## DECISION TREE

# In[ ]:


clf = KNeighborsClassifier(n_neighbors=5)
score = cross_val_score(clf, X_train, y_train, cv=k_fold, n_jobs=1, scoring='accuracy')
print(score)
print("Accuracy: %0.2f (+/- %0.2f)" % (score.mean(), score.std() * 2))


# In[ ]:


clf = LogisticRegressionCV(cv=5, max_iter=125)
score = cross_val_score(clf, X_train, y_train, cv=k_fold, scoring='accuracy')
print(score)
print("Accuracy: %0.2f (+/- %0.2f)" % (score.mean(), score.std() * 2))


# ## RANDOM FOREST

# In[ ]:


clf = RandomForestClassifier(n_estimators=10)
score = cross_val_score(clf, X_train, y_train, cv=k_fold, n_jobs=1, scoring='accuracy')
print(score)
print("Accuracy: %0.2f (+/- %0.2f)" % (score.mean(), score.std() * 2))


# ## Naive Bayes

# In[ ]:


clf = GaussianNB()
score = cross_val_score(clf, X_train, y_train, cv=k_fold, n_jobs=1, scoring='accuracy')
print(score)
print("Accuracy: %0.2f (+/- %0.2f)" % (score.mean(), score.std() * 2))


# ## SVM 

# In[ ]:


clf = SVC(gamma='auto')
score = cross_val_score(clf, X_train, y_train, cv=k_fold, n_jobs=1, scoring='accuracy')
print(score)
print("Accuracy: %0.2f (+/- %0.2f)" % (score.mean(), score.std() * 2))


# ## Highest accuracy achieved by Random Forest and Logistic Regression
# ## TESTING

# In[ ]:


from sklearn.linear_model import LogisticRegression
logmodel = LogisticRegression(solver='lbfgs', max_iter=1000)
logmodel.fit(X_train, y_train)

predictions = logmodel.predict(test.drop('Fare', axis=1))
submission = pd.DataFrame({'PassangerId': pass_id, 'Survived':predictions})
submission.to_csv('submission_logreg.csv', index=False)
submission.head()


# In[ ]:


rfmodel = RandomForestClassifier(n_estimators=100)
rfmodel.fit(X_train, y_train)

predictions = rfmodel.predict(test.drop('Fare', axis=1))
submission = pd.DataFrame({'PassangerId': pass_id, 'Survived':predictions})
submission.to_csv('submission_rf.csv', index=False)
submission.head()


# In[ ]:




