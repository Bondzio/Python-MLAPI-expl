#!/usr/bin/env python
# coding: utf-8

# 
# ### The notebook is combine simple methods for feature engineering.
# ### Random Forest

# ## Intro

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score


# In[ ]:


train = pd.read_csv('/kaggle/input/titanic/train.csv')
test = pd.read_csv('/kaggle/input/titanic/test.csv')


# In[ ]:


train.drop(['Ticket', 'Cabin'], axis=1, inplace=True)


# In[ ]:


train.head().T


# ## Feature engineering

# In[ ]:


test.drop(['Ticket', 'Cabin'], axis=1, inplace=True)


# In[ ]:


test.head().T


# In[ ]:


train.isnull().sum()


# In[ ]:


test.isnull().sum()


# In[ ]:


train['Age'].fillna(train['Age'].median(), inplace=True)
test['Age'].fillna(test['Age'].median(), inplace=True)
train['Embarked'].fillna('S', inplace=True)
test['Fare'].fillna(test['Fare'].median(), inplace=True)


# In[ ]:


train.loc[ train['Fare'] <= 7.91, 'Fare']                             = 0
train.loc[(train['Fare'] > 7.91) & (train['Fare'] <= 14.454), 'Fare'] = 1
train.loc[(train['Fare'] > 14.454) & (train['Fare'] <= 31), 'Fare']   = 2
train.loc[ train['Fare'] > 31, 'Fare']                                = 3
train['Fare'] = train['Fare'].astype(int)

test.loc[ test['Fare'] <= 7.91, 'Fare']                            = 0
test.loc[(test['Fare'] > 7.91) & (test['Fare'] <= 14.454), 'Fare'] = 1
test.loc[(test['Fare'] > 14.454) & (test['Fare'] <= 31), 'Fare']   = 2
test.loc[ test['Fare'] > 31, 'Fare']                               = 3
test['Fare'] = test['Fare'].astype(int)


# In[ ]:


train['Title'] = train['Name'].str.split(", ", expand=True)[1].                str.split(".", expand=True)[0]
test['Title'] = test['Name'].str.split(", ", expand=True)[1].                str.split(".", expand=True)[0]


# In[ ]:


train['Title'].unique()


# In[ ]:


train['Title'] = train['Title'].replace(['Don', 'Major', 'Sir', 'Col', 'Capt',                                        'Major', 'Jonkheer'], 'Mr')
train['Title'] = train['Title'].replace(['Mlle', 'Mme', 'Ms'], 'Miss')
train['Title'] = train['Title'].replace(['Mme', 'Dona', 'Lady', 'Countess',                                         'the Countess'], 'Mrs')

test['Title'] = test['Title'].replace(['Don', 'Major', 'Sir', 'Col', 'Capt',                                        'Major', 'Jonkheer'], 'Mr')
test['Title'] = test['Title'].replace(['Mlle', 'Mme', 'Ms'], 'Miss')
test['Title'] = test['Title'].replace(['Mme', 'Dona', 'Lady', 'Countess',                                       'the Countess'], 'Mrs')


# In[ ]:


train.loc[ train['Age'] <= 16, 'Age']                        = 0
train.loc[(train['Age'] > 16) & (train['Age'] <= 32), 'Age'] = 1
train.loc[(train['Age'] > 32) & (train['Age'] <= 48), 'Age'] = 2
train.loc[(train['Age'] > 48) & (train['Age'] <= 64), 'Age'] = 3
train.loc[ train['Age'] > 64, 'Age']                         = 4

test.loc[ test['Age'] <= 16, 'Age']                       = 0
test.loc[(test['Age'] > 16) & (test['Age'] <= 32), 'Age'] = 1
test.loc[(test['Age'] > 32) & (test['Age'] <= 48), 'Age'] = 2
test.loc[(test['Age'] > 48) & (test['Age'] <= 64), 'Age'] = 3
test.loc[ test['Age'] > 64, 'Age']                        = 4


# In[ ]:


train['Title'].unique(), test['Title'].unique()


# In[ ]:


train['Family'] = train['Parch'] + train['SibSp']

test['Family'] = test['Parch'] + test['SibSp']


# In[ ]:


train = pd.concat([train, pd.get_dummies(train['Pclass'], prefix='Pclass'),
                     pd.get_dummies(train['Sex'], prefix='Sex'),
                     pd.get_dummies(train['Family'], prefix='Family'),
                     pd.get_dummies(train['Embarked'], prefix='Embarked'),
                     pd.get_dummies(train['Age'], prefix='Age'),
                     pd.get_dummies(train['Fare'], prefix='Fare'),
                     pd.get_dummies(train['Title'], prefix='Title')],
                    axis=1)
test = pd.concat([test, pd.get_dummies(test['Pclass'], prefix='Pclass'),
                     pd.get_dummies(test['Sex'], prefix='Sex'),
                     pd.get_dummies(test['Family'], prefix='Family'),
                     pd.get_dummies(test['Embarked'], prefix='Embarked'),
                     pd.get_dummies(test['Age'], prefix='Age'),
                     pd.get_dummies(test['Fare'], prefix='Fare'),
                     pd.get_dummies(test['Title'], prefix='Title')],
                    axis=1)


# In[ ]:


train.drop(['Pclass', 'Name', 'Sex', 'Age', 'Fare', 'SibSp',            'Parch', 'Embarked', 'PassengerId', 'Title', 'Family'], axis=1, inplace=True)
test.drop(['Pclass', 'Name', 'Sex', 'Age', 'Fare', 'SibSp',           'Parch', 'Embarked', 'PassengerId', 'Title', 'Family'], axis=1, inplace=True)


# In[ ]:


train.shape, test.shape


# In[ ]:


train.head(25)


# In[ ]:


train.columns, test.columns


# In[ ]:


y = train['Survived']
train.drop('Survived', axis=1, inplace=True);


# In[ ]:


print(set(test.columns) - set(train.columns))


# In[ ]:


train.shape, test.shape


# In[ ]:


train.head().T


# In[ ]:


test.head().T


# ## Training machine learning model

# In[ ]:


rf = RandomForestClassifier(random_state=42, n_estimators=50,                           criterion='gini', max_depth=15)
rf.fit(train, y)
y_rf = rf.predict(test)
best_rf = round(rf.score(train, y) * 100, 2)
best_rf


# In[ ]:


rf_params = {'max_depth': list(range(4,10)),
               'n_estimators': list(range(100, 1100, 100))}

rf_grid = GridSearchCV(rf, rf_params,
                         cv=10, n_jobs=-1,
                        verbose=True)
rf_grid.fit(train, y)


# In[ ]:


rf_grid.best_params_, rf_grid.best_score_


# In[ ]:


rf_new = RandomForestClassifier(random_state=42, max_depth=5, n_estimators=250,                               criterion='gini')
rf_new.fit(train, y)
y_rf = rf_new.predict(test)
best_rf = round(rf_new.score(train, y) * 100, 2)
best_rf


# In[ ]:


final_rf = pd.DataFrame()
tit_test = pd.read_csv('/kaggle/input/titanic/test.csv')
final_rf['PassengerId'] = tit_test['PassengerId']
final_rf['Survived'] = y_rf
final_rf.to_csv('submission_rf.csv',index=False)

