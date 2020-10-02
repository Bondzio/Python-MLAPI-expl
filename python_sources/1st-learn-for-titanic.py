# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.

# data analysis and wrangling
import pandas as pd
import numpy as np
import random as rnd

# visualization
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

# machine learning

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier


# import data
train_df = pd.read_csv('/kaggle/input/titanic/train.csv')
test_df = pd.read_csv('/kaggle/input/titanic/test.csv')

combine = [train_df,test_df]

print(train_df.columns.values) # names all features

train_df.head()
train_df.tail()
train_df.dtypes # check type of all columns (train_df[''].dtype)
train_df.info()# check type of all columns, and NA value
test_df.info()
train_df['Sex'].value_counts(normalize = True) # count specific value
train_df.describe() # describe train dataset
train_df.describe(include = ['O']) # describe category
#train_df['Title'].unique() # list name of all variable

# Correlating - pivot table
train_df[['Pclass','Survived']].groupby(['Pclass'], as_index = False).mean().sort_values(by = 'Survived', ascending = False)
train_df[['Sex','Survived']].groupby(['Sex'], as_index = False).mean().sort_values(by = 'Survived', ascending = False)
train_df[['SibSp','Survived']].groupby(['SibSp'], as_index = False).mean().sort_values(by = 'Survived', ascending = False)
train_df[['Parch','Survived']].groupby(['Parch'], as_index = False).mean().sort_values(by = 'Survived', ascending = False)

# Plot a category variable
#g = sns.FacetGrid(train_df, col = 'Survived')
#g.map(plt.hist, 'Age', bins = 20)
#plt.show()

#grid =  sns.FacetGrid(train_df, col = 'Survived', row = 'Pclass', size = 2.2, aspect = 1.6)
#grid.map(plt.hist, 'Age', alpha = .5, bins = 20)
#grid.add_legend();

#grid = sns.FacetGrid(train_df, row = 'Embarked', size = 2.2, aspect = 1.6)
#grid.map(sns.pointplot, 'Pclass', 'Survived','Sex', palette = 'deep')
#grid.add.legend();

#grid = sns.FacetGrid(train_df, row = 'Embarked', col = 'Survived', size = 2.2, aspect = 1.6)
#grid.map(sns.barplot, 'Sex', 'Fare', alpha =.5, ci = None)
#grid.add_legend();

print('Before', train_df.shape, test_df.shape, combine[0].shape, combine[1].shape)

train_df = train_df.drop(['Ticket','Cabin'], axis =1)
test_df = test_df.drop(['Ticket','Cabin'], axis =1)
combine = [train_df, test_df]

'After', train_df.shape, test_df.shape, combine[0].shape, combine[1].shape

# Extract title
for dataset in combine:
    dataset['Title'] = dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)

pd.crosstab(train_df['Title'], train_df['Sex'])  

# Replace value

for dataset in combine:
    dataset['Title'] = dataset['Title'].replace(['Lady','Countess','Capt','Col',\
                                                'Don','Dr','Major','Rev','Sir','Jonkheer','Dona'],'Rare')
    dataset['Title'] = dataset['Title'].replace('Mlle','Miss')
    dataset['Title'] = dataset['Title'].replace('Ms','Miss')
    dataset['Title'] = dataset['Title'].replace('Mme','Mrs')

train_df[['Title', 'Survived']].groupby(['Title'], as_index = False).mean()

# convert the categorical titles to ordinal
title_mapping = {'Mr':1,'Miss':2, 'Mrs':3, 'Master':4,'Rare':5}
for dataset in combine:
    dataset['Title'] = dataset['Title'].map(title_mapping)
    dataset['Title'] = dataset['Title'].fillna(0)

train_df.head()

train_df = train_df.drop(['Name', 'PassengerId'], axis=1)
test_df = test_df.drop(['Name'], axis = 1)
combine = [train_df, test_df]
train_df.shape, test_df.shape

# convert categorical features
for dataset in combine:
    dataset['Sex'] = dataset['Sex'].map({'female':1, 'male':0}).astype(int)

train_df.head()

# Complete a numerical continuous feature

#grid = sns.FacetGrid(train_df, row = 'Pclass', col = 'Sex', size = 2.2, aspect =1.6)
#grid.map(plt.hist, 'Age', alpha =.5, bins =20)
#grid.add_legend()

guess_ages = np.zeros((2,3))
guess_ages

# check a specific row
for dataset in combine:
    for i in range(0, 2):
        for j in range(0, 3):
            guess_df = dataset[(dataset['Sex'] == i) & (dataset['Pclass'] == j+1)]['Age'].dropna()

            # age_mean = guess_df.mean()
            # age_std = guess_df.std()
            # age_guess = rnd.uniform(age_mean - age_std, age_mean + age_std)
            age_guess = guess_df.median()
            # Convert random age float to nearest .5 age
            guess_ages[i,j] = int( age_guess/0.5 + 0.5 ) * 0.5

for dataset in combine:         
    for i in range(0, 2):
        for j in range(0, 3):
            dataset.loc[(dataset.Age.isnull()) & (dataset.Sex == i) & (dataset.Pclass == j+1),\
                    'Age'] = guess_ages[i,j]
    dataset['Age'] = dataset['Age'].astype(int)

train_df.head()

# Create age band for age
#grid = sns.FacetGrid(train_df,col = 'Survived')
#grid.map(plt.hist,'Age')
#grid.add.legend()

train_df['AgeBand'] = pd.cut(train_df['Age'],5) # divide the whole range into 5 intervals
train_df[['AgeBand','Survived']].groupby(['AgeBand'], as_index = False).mean().sort_values(by = 'AgeBand', ascending = True)

# replace Age with ordinals for all dataset
for dataset in combine:
    dataset.loc[dataset['Age'] <= 16, 'Age'] = 0
    dataset.loc[(dataset['Age'] > 16) & (dataset['Age'] <= 32), 'Age'] = 1
    dataset.loc[(dataset['Age'] > 32) & (dataset['Age'] <= 48), 'Age'] = 2
    dataset.loc[(dataset['Age'] > 48) & (dataset['Age'] <= 64), 'Age'] = 3
    dataset.loc[(dataset['Age'] > 64), 'Age'] = 4 # Ageband is object
train_df.head()

# Remove ageband
train_df = train_df.drop(['AgeBand'], axis = 1)
combine = [train_df, test_df]
train_df.head()

# Create new features combining existing features
for dataset in combine:
    dataset['FamilySize'] = dataset['SibSp'] + dataset['Parch'] + 1
train_df[['FamilySize','Survived']].groupby(['FamilySize'], as_index= False).mean().sort_values(by = 'Survived',ascending = False)

for dataset in combine:
    dataset['IsAlone'] = 0
    dataset.loc[dataset['FamilySize'] == 1, 'IsAlone'] = 1

train_df[['IsAlone', 'Survived']].groupby(['IsAlone'], as_index = False).mean()

train_df = train_df.drop(['Parch','SibSp','FamilySize'],axis = 1)
test_df = test_df.drop(['Parch','SibSp','FamilySize'],axis = 1)
combine = [train_df, test_df]

train_df.head()

# Combine Age and Pclass
for dataset in combine:
    dataset['Age*Class'] = dataset.Age * dataset.Pclass
    
train_df.loc[:,['Age*Class', 'Age','Pclass']].head(10)


# Complete a categorical feature 

freq_port = train_df.Embarked.dropna().mode()[0] # most frequent variable
freq_port

for dataset in combine:
    dataset['Embarked'] = dataset['Embarked'].fillna(freq_port)
    
train_df[['Embarked','Survived']].groupby(['Embarked'], as_index = False).mean().sort_values(by = 'Survived', ascending = False)    

# Convert categorical into numeric

for dataset in combine:
    dataset['Embarked'] = dataset['Embarked'].map({'S': 0, 'C': 1, 'Q': 2}).astype(int)

train_df.head()
# fill in Na for test_fare
test_df['Fare'].fillna(test_df['Fare'].median(),inplace = True)
test_df.head()


# Create Fareband with qcut
train_df['FareBand'] = pd.qcut(train_df['Fare'],4)
train_df['FareBand'].value_counts()

plt.hist(train_df['Fare'])
plt.show()

# Change fare into ordinal value based on the FareBand
for dataset in combine:
    dataset.loc[dataset['Fare'] <= 7.91, 'Fare'] = 0
    dataset.loc[(dataset['Fare'] > 7.91) & (dataset['Fare'] <= 14.454), 'Fare'] = 1     
    dataset.loc[(dataset['Fare'] > 14.454) & (dataset['Fare'] <= 31), 'Fare'] = 2
    dataset.loc[dataset['Fare'] > 31, 'Fare'] = 3
    dataset['Fare'] = dataset['Fare'].astype(int) # transfer into interger
    
train_df = train_df.drop(['FareBand'], axis = 1)
combine = [train_df, test_df]

train_df.head(10)

# Model, prediction, and solve
X_train = train_df.drop('Survived', axis = 1)
Y_train = train_df['Survived']
X_test = test_df.drop('PassengerId',axis = 1).copy()
X_train.shape, Y_train.shape, X_test.shape

# logistic regression

#logreg = LogisticRegression()
##logreg.fit(X_train, Y_train)
#Y_pred = logreg.predict(X_test)
#acc_log = round(logreg.score(X_train, Y_train)*100,2)
#acc_log

#coeff_df = pd.DataFrame(train_df.columns.delete(0))
#coeff_df.columns = ['Feature']
#coeff_df['Correlation'] = pd.Series(logreg.coef_[0])

#coeff_df.sort_values(by = 'Correlation',ascending = False)

# SVM
#svc = SVC()
#svc.fit(X_train, Y_train)
#Y_pred = svc.predict(X_test)
#acc_svc = round(svc.score(X_train, Y_train)*100,2)
#acc_svc

# KNN
#knn = KNeighborsClassifier(n_neighbors = 3)
#knn.fit(X_train, Y_train)
#Y_pred = knn.predict(X_test)
#acc_knn = round(knn.score(X_train, Y_train)*100,2)
#acc_knn

# Gaussian Naive Bayes
#gaussian = GaussianNB()
#gaussian.fit(X_train, Y_train)
#Y_pred = gaussian.predict(X_test)
#acc_gaussian = round(gaussian.score(X_train, Y_train) * 100, 2)
#acc_gaussian



# Perceptron

#perceptron = Perceptron()
#perceptron.fit(X_train, Y_train)
#Y_pred = perceptron.predict(X_test)
#acc_perceptron = round(perceptron.score(X_train, Y_train) * 100, 2)
#acc_perceptron


# Linear SVC

#linear_svc = LinearSVC()
#linear_svc.fit(X_train, Y_train)
#Y_pred = linear_svc.predict(X_test)
#acc_linear_svc = round(linear_svc.score(X_train, Y_train) * 100, 2)
#acc_linear_svc

# Stochastic Gradient Descent

#sgd = SGDClassifier()
#sgd.fit(X_train, Y_train)
#Y_pred = sgd.predict(X_test)
#acc_sgd = round(sgd.score(X_train, Y_train) * 100, 2)
#acc_sgd



# Decision Tree

#decision_tree = DecisionTreeClassifier()
#decision_tree.fit(X_train, Y_train)
#Y_pred = decision_tree.predict(X_test)
#acc_decision_tree = round(decision_tree.score(X_train, Y_train) * 100, 2)
#acc_decision_tree

# Random Forest

random_forest = RandomForestClassifier(n_estimators=100)
random_forest.fit(X_train, Y_train)
Y_pred = random_forest.predict(X_test)
random_forest.score(X_train, Y_train)
acc_random_forest = round(random_forest.score(X_train, Y_train) * 100, 2)
acc_random_forest

# Evaluation
#models = pd.DataFrame({
#    'Model': ['Support Vector Machines', 'KNN', 'Logistic Regression', 
#              'Random Forest', 'Naive Bayes', 'Perceptron', 
#              'Stochastic Gradient Decent', 'Linear SVC', 
#              'Decision Tree'],
#    'Score': [acc_svc, acc_knn, acc_log, 
#              acc_random_forest, acc_gaussian, acc_perceptron, 
#              acc_sgd, acc_linear_svc, acc_decision_tree]})
#models.sort_values(by='Score', ascending=False)

output = pd.DataFrame({
        "PassengerId": test_df["PassengerId"],
        "Survived": Y_pred
    })

output.to_csv('my_submission.csv', index = False)



    
    
    
    