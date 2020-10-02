#!/usr/bin/env python
# coding: utf-8

# # Feature generation importance
# In this kernel, I will try to generate useful and meaningful features from the Titanic dataset to boost a classifier.

# In[ ]:


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Machine learning libraries
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier

import warnings
warnings.filterwarnings("ignore")


# In[ ]:


# Settings
train_path = os.path.join('..', 'input', 'train.csv')
test_path = os.path.join('..', 'input', 'test.csv')
submission_path = os.path.join('..', 'input', 'gender_submission.csv')

# Data loading
train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)
submission = pd.read_csv(submission_path)


# ## Data insights
# To start, I will look a bit into the given data.

# In[ ]:


# Let's look at 10 random rows of train_df
train_df.sample(n=10)


# For each passenger, we have 12 columns.
# * PassengerId : just a Id to differentiate passengers, we will drop that as it does not contain any information
# * Survived : our target column, that we will store in another variable
# * Pclass : categorical data, the class of the passenger
# * Name : the name of the passenger, we will need to work a bit on this column to use it
# * Sex : categorical data, sex of the passenger
# * Age : quantitative data, age of the passenger (WARNING : contains NaN values)
# * SibSp : quantitative data, number of siblings / spouses aboard the Titanic
# * Parch : quantitative data, number of parents / children aboard the Titanic
# * Ticket : ticket number, this will be hard to use ! Does it even contain any useful information ?
# * Fare : quantitative data
# * Cabin : categorical data, hard to use... maybe with some preporcessing according to the ship architecture
# * Embarked : categorical data, where the passenger embarked

# In[ ]:


# Let's look at the distribution of passenger according to their survival
train_df['Survived'].value_counts().plot.bar()


# The two classes have roughly the same magnitude. This will be convenient for the training phase.

# In[ ]:


# Let's separate our dataset between the ones who survived and the ones that did not
survived_df = train_df[train_df['Survived'] == 1]
dead_df = train_df[train_df['Survived'] == 0]

# Let's plot a few insights
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 5))
plt.subplots_adjust(hspace=0.6)

survived_df['Pclass'].value_counts().sort_index().plot.bar(ax=axes[0][0], title='Survived Pclass')
dead_df['Pclass'].value_counts().sort_index().plot.bar(ax=axes[0][1], title='Dead Pclass')

survived_df['Embarked'].value_counts().sort_index().plot.bar(ax=axes[1][0], title='Survived embarked place')
dead_df['Embarked'].value_counts().sort_index().plot.bar(ax=axes[1][1], title='Dead embarked place')

survived_df['Sex'].value_counts().sort_index().plot.bar(ax=axes[2][0], title='Survived sex')
dead_df['Sex'].value_counts().sort_index().plot.bar(ax=axes[2][1], title='Dead sex')

plt.show()


# As we can see, women have a better survival chance, as a first class passenger also have a better survival chance. These features will be useful for our classifier.

# In[ ]:


# Let's plot the survival rate per slice of 5 years in age
age_hist = []
for age in range(0, 80, 5):
    tmp_df = train_df[train_df['Age'] < age + 5]
    age_hist += [tmp_df[tmp_df['Age'] >= age]['Survived'].mean()]

plt.plot([age + 2.5 for age in range(0, 80, 5)], age_hist)
plt.xlabel('Age')
plt.ylabel('Survival rate')
plt.title('Survival age per age slices')
plt.show()


# Here we can see that children (under 15) have a higher survival rate : we should maybe create a categorical feature *is_child*
# 
# ## Feature creation
# 
# From now on, we will always modify the test data as we modify the train data.

# In[ ]:


# While we are working on the age, we need to fill NaN values
# For that, we will replace NaN values by the median age
median_age = train_df['Age'].median()
for df in [train_df, test_df]:
    df['Age'].fillna(value=median_age, inplace=True)

    # is_child feature creation
    df['is_child'] = 0
    df.loc[train_df['Age'] < 15, 'is_child'] = 1
    
train_df.sample(n=10)


# Now, let's preprocess categorical columns thanks to the *get_dummies* pandas function. This will give us a one-hot encoded version of each of our categorical variables.

# In[ ]:


train_df['Embarked'].fillna(value=train_df['Embarked'].mode()[0])
test_df['Embarked'].fillna(value=test_df['Embarked'].mode()[0])


train_df = pd.get_dummies(train_df, columns=['Pclass', 'Embarked'])
test_df = pd.get_dummies(test_df, columns=['Pclass', 'Embarked'])

def sex_one_hot_encoding(x):
    if x == 'female':
        return 1
    else:
        return 0
    
train_df['Sex'] = train_df['Sex'].apply(sex_one_hot_encoding)
test_df['Sex'] = test_df['Sex'].apply(sex_one_hot_encoding)

train_df.sample(n=10)


# Let's do at bit of feature engineering on families : family size, alone passenger

# In[ ]:


for df in [train_df, test_df]:
    df['family_size'] = df['SibSp'] + df['Parch']
    
    df['alone_passenger'] = 0
    df.loc[df['family_size'] == 0, 'alone_passenger'] = 1

survival_rate = []
for n in range(train_df['family_size'].max()):
    survival_rate += [train_df[train_df['family_size'] == n]['Survived'].mean()]

# This graph will give us some insights on the family size impact
plt.plot([n for n in range(train_df['family_size'].max())], survival_rate)
plt.xlabel('Family size')
plt.ylabel('Survival rate')
plt.title('Survival age per family size')
plt.show()


# In[ ]:


def is_small_family(n):
    if n <= 3:
        return 1
    else:
        return 0
    
def is_medium_family(n):
    if n > 3 and n <= 5:
        return 1
    else:
        return 0
    
def is_big_family(n):
    if n > 5:
        return 1
    else:
        return 0

for df in [train_df, test_df]:
    df['small_family'] = df['family_size'].apply(is_small_family)
    df['medium_family'] = df['family_size'].apply(is_medium_family)
    df['big_family'] = df['family_size'].apply(is_big_family)
    


# Now, let's store the Survived column in another variable and let's drop the *PassengerId* and the *Ticket* columns.

# In[ ]:


survived = train_df['Survived']

train_df.drop(axis=1, columns=['Survived', 'PassengerId', 'Ticket'], inplace=True)
test_df.drop(axis=1, columns=['PassengerId', 'Ticket'], inplace=True)

train_df.sample(n=10)


# For the cabin, the first letter indicates the deck. This can be an useful information. I will also give the letter U (Unknown) to NaN values as this lack of information may still be useful.

# In[ ]:


def get_deck(cab):
    if cab[0] == 'T':  # no T deck on the Titanic...
        return 'U'
    else:
        return cab[0]

for df in [train_df, test_df]:
    df['Cabin'].fillna('U', inplace=True)

    # is_child feature creation
    df['Cabin'] = df['Cabin'].apply(get_deck)

train_df = pd.get_dummies(train_df, columns=['Cabin'])
test_df = pd.get_dummies(test_df, columns=['Cabin'])

train_df.sample(n=10)


# Now, we only have the Name column to process before starting the training of our classifier.

# In[ ]:


# What could we create from the Name column ?
# maybe a feature with the length of the name, one with the particle
def get_last_name_length(name):
    return len(name.split(',')[0])

particles = ['Mr', 'Mrs', 'Dr', 'Master', 'Miss', 'Ms']
def get_particle(name):
    name = name.split(',')[1]
    particle = name.split('.')[0]
    if particle in particles:
        return particle
    else:
        return 'NO'

for df in [train_df, test_df]:
    df['name_length'] = df['Name'].apply(get_last_name_length)
    df['name_particle'] = df['Name'].apply(get_particle)
    df.drop(axis=1, columns=['Name'], inplace=True)
    
train_df = pd.get_dummies(train_df, columns=['name_particle'])
test_df = pd.get_dummies(test_df, columns=['name_particle'])

train_columns = train_df.columns.values
test_columns = test_df.columns.values
for c in train_columns:
    if c not in test_columns:
        test_df[c] = 0

for c in test_columns:
    if c not in train_columns:
        train_df[c] = 0

train_df.sample(n=10)


# ## Classification
# 
# We will train a few classifiers and score them with a cross-validation strategy
# 

# In[ ]:


# <=== Logistic Regression ===>
logistic_regression = LogisticRegression(solver='lbfgs', max_iter=1000)
scores = cross_val_score(logistic_regression, train_df, survived, cv=5)

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


# In[ ]:


# <=== Linear SVC ===>
linear_svc = LinearSVC(loss='squared_hinge', max_iter=10000)
scores = cross_val_score(linear_svc, train_df, survived, cv=5)

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


# In[ ]:


# <=== RandomForestClassifier ===>
random_forest = RandomForestClassifier(n_estimators=125)
scores = cross_val_score(random_forest, train_df, survived, cv=5)

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


# In[ ]:


# <=== Logistic regression bagging ===>
base_clf = LogisticRegression(solver='lbfgs', max_iter=1000)
lr_bagging = BaggingClassifier(base_clf, n_estimators=11)
scores = cross_val_score(lr_bagging, train_df, survived, cv=5)

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


# In[ ]:


# <=== Linear SVC bagging ===>
base_clf = LinearSVC(loss='squared_hinge', max_iter=10000)
lsvc_bagging = BaggingClassifier(base_clf, n_estimators=11)
scores = cross_val_score(lsvc_bagging, train_df, survived, cv=5)

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


# In[ ]:


# <=== MLP classifier ===>
mlp = MLPClassifier(hidden_layer_sizes=(50, 25, 10), activation='relu', solver='adam', max_iter=1000)
scores = cross_val_score(mlp, train_df, survived, cv=5)

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


# In[ ]:


# <=== Logistic regression boosting ===>
base_clf = LogisticRegression(solver='lbfgs', max_iter=1000)
lr_boosting = AdaBoostClassifier(base_clf, n_estimators=25)
scores = cross_val_score(lr_boosting, train_df, survived, cv=5)

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


# Here, we will select, linear SVC classifier, the random forest classifier and the ada boost classifier. I will now train them on the whole training dataset and predict the output on the test dataset to get a submission.

# In[ ]:


# Parameter dicts for Grid Search
linear_svc_params = {
    'loss': ['squared_hinge', 'hinge'],
    'C': [0.25, 1.0, 2.5, 5.0]
}

random_forest_params = {
    'n_estimators': [125, 151, 175],
    'min_samples_split' : [2, 3, 4],
    'min_samples_leaf': [1, 2, 3]
}

ada_boost_params = {
    'n_estimators': [17, 25, 37],
}


# In[ ]:


linear_svc = LinearSVC(loss='squared_hinge', max_iter=10000)
lsvc_gs = GridSearchCV(linear_svc, linear_svc_params, n_jobs=4, cv=5)
lsvc_gs.fit(train_df, survived)
print("Linear SVC best score : {} --> {}".format(lsvc_gs.best_score_, lsvc_gs.best_params_))
pred_linear_svc = lsvc_gs.predict(test_df.fillna(value=0))

random_forest = RandomForestClassifier(n_estimators=125)
rf_gs = GridSearchCV(random_forest, random_forest_params, n_jobs=4, cv=5)
rf_gs.fit(train_df, survived)
print("Random forest best score : {} --> {}".format(rf_gs.best_score_, rf_gs.best_params_))
pred_random_forest = rf_gs.predict(test_df.fillna(value=0))

base_clf = LogisticRegression(solver='lbfgs', max_iter=1000)
lr_boosting = AdaBoostClassifier(base_clf, n_estimators=25)
ab_gs = GridSearchCV(lr_boosting, ada_boost_params, n_jobs=4, cv=5)
ab_gs.fit(train_df, survived)
print("Ada boost best score : {} --> {}".format(ab_gs.best_score_, ab_gs.best_params_))
pred_lr_boosting = ab_gs.predict(test_df.fillna(value=0))


# In[ ]:


# Ensemble voting between our 3 models
pred = pred_linear_svc + pred_random_forest + pred_lr_boosting
pred = (pred >= 2).astype(np.uint8)


# In[ ]:


submission['Survived'] = pred
submission.to_csv('submission.csv', index=False)

submission['Survived'] = pred_random_forest
submission.to_csv('submission_rf.csv', index=False)


# WIP : still to come --> feature importance, grid search,...
