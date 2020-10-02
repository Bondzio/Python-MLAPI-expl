#!/usr/bin/env python
# coding: utf-8

# <H1> Titanic Dataset Solution</H1>
# 
# This is my attempt at solving the Titanic Dataset. Here, I employ techniques such as data interpolation, feature conversion, regular expression on string features, random search and grid search for hyperparameter optimization. 

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# <H1> A) Import Train Data and Examine it

# In[ ]:


train = pd.read_csv("train.csv")
testset = pd.read_csv("test.csv")
testset.info()


# From an initial glance, we can see that the "Cabin" feature lacks too many data points for reasonable interpolation. Therefore, we will likely drop it. Other features like *Embarked* and *Age* will probably require some interpolation. Let's first examine the percentage of data missing per feature.

# In[ ]:


print((train.isna().sum()/train.shape[0])*100)


# <H1> B) Data Interpolation and Cleaning

# In[ ]:


#Drop cabin given it is missing too much data
train_clean = train.drop(['Cabin'],axis=1)
test_clean = test.drop(['Cabin'],axis=1)


# To interpolate the missing information, I'm thinking of using two techniques: Mean, Median in combination with Groupby or Multiple Imputation by Chained Equations. There's no right answer here but I assume interpolating the age correlating might influence the classifier's final accuracy.

# <H3> 1) Mean in Combination GroupBy Interpolation

# Here, I interpolate the missing values by grouping them to the gender. Not sure if this is a good idea yet. Will come back later if need be.

# In[ ]:


train_clean['Age'].fillna(train_clean.groupby('Sex')['Age'].transform("mean"), inplace=True)
test_clean['Age'].fillna(test_clean.groupby('Sex')['Age'].transform("mean"), inplace=True)

train_clean['Embarked'] = train_clean['Embarked'].astype('category').cat.codes
test_clean['Embarked'] = test_clean['Embarked'].astype('category').cat.codes

train_clean['Embarked'].fillna(train_clean.groupby('Pclass')['Embarked'].agg(pd.Series.mode),inplace=True)
test_clean['Embarked'].fillna(test_clean.groupby('Pclass')['Embarked'].agg(pd.Series.mode),inplace=True)


# Handling the *Name* feature by extracting important info such as the title

# In[ ]:


# Convert to categorical values Title 
dataset_title = [i.split(",")[1].split(".")[0].strip() for i in train_clean["Name"]]
train_clean["Title"] = pd.Series(dataset_title)
train_clean["Title"].head()

train_clean["Title"] = train_clean["Title"].replace(['Lady', 'the Countess','Countess','Capt', 'Col','Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
train_clean["Title"] = train_clean["Title"].map({"Master":0, "Miss":1, "Ms" : 1 , "Mme":1, "Mlle":1, "Mrs":1, "Mr":2, "Rare":3})
train_clean["Title"] = train_clean["Title"].astype(int)


#Repeat for test set
#Convert to categorical values Title 
dataset_title = [i.split(",")[1].split(".")[0].strip() for i in test_clean["Name"]]
test_clean["Title"] = pd.Series(dataset_title)
test_clean["Title"].head()

test_clean["Title"] = test_clean["Title"].replace(['Lady', 'the Countess','Countess','Capt', 'Col','Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
test_clean["Title"] = test_clean["Title"].map({"Master":0, "Miss":1, "Ms" : 1 , "Mme":1, "Mlle":1, "Mrs":1, "Mr":2, "Rare":3})
test_clean["Title"] = test_clean["Title"].astype(int)


# <H3> 1.5) Multiple Imputation by Chained Equations

# Try later.

# <H3> 2) One Hot Encoding for categorical features

# In[ ]:


train_clean[['C','Q','S']] = pd.get_dummies(train["Embarked"])
test_clean[['C','Q','S']] = pd.get_dummies(test["Embarked"])

train_clean[['M','F']] = pd.get_dummies(train["Sex"])
test_clean[['M','F']] = pd.get_dummies(test["Sex"])

#Combine Sibling Spouse and Parent Child features into one Family Feature
train_clean['FamSize'] = train_clean['SibSp']+train_clean['Parch']+ 1
test_clean['FamSize'] = test_clean['SibSp']+test_clean['Parch']+ 1

#Drop Original Feature columns now that we've encoded them
train_clean = train_clean.drop(['Embarked','Sex','Ticket','SibSp','Parch','PassengerId','Name'],axis=1)
test_clean = test_clean.drop(['Embarked','Sex','Ticket','SibSp','Parch','PassengerId','Name'],axis=1)

train_clean.describe()


# <H3> 3) Feature Scaling

# In[ ]:


from sklearn.preprocessing import RobustScaler
train_clean[["Age","Fare"]] = RobustScaler().fit_transform(train_clean[["Age","Fare"]])
test_clean[["Age","Fare"]] = RobustScaler().fit_transform(test_clean[["Age","Fare"]])


# <H3> 4) Data Visualization

# In[ ]:


g= sns.pairplot(train_clean, hue= "Survived")


# In[ ]:


fig, ax = plt.subplots(figsize=(10,10))
sns.heatmap(train_clean.corr(), vmax=1.0, center=0, fmt='.2f', square=True, linewidths=.5, annot=True, cbar_kws={"shrink":.70})


# In[ ]:


y_train = train_clean["Survived"].values
X_train = train_clean.drop(columns=["Survived"])


# <H1> C) Try Quick and Dirty Solutions

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn import model_selection

models = []
models.append(('RF',RandomForestClassifier(n_estimators=100, max_depth=10,random_state=0)))
models.append(('NB',GaussianNB()))
models.append(("SVM",SVC(gamma='auto')))
models.append(("LR",LogisticRegression(solver='lbfgs')))

results = []
names = []

for name, model in models:
    kfold = model_selection.KFold(n_splits =10, random_state = 7)
    cv_results = model_selection.cross_val_score(model, X_train, y_train, cv=kfold, scoring ="accuracy")
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)


# Initial accuracies aren't bad, random forests and logistic regression and SVMs seem most promising. Let's go with Random Forest and try a random search for the best hyperparamter combination. Then after the random search, we'll use a more refined grid-search to maximize accuracy gains

# <H3> Try Random Hyperparam Tuning

# In[ ]:


from sklearn.model_selection import RandomizedSearchCV

# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

# Use the random grid to search for best hyperparameters
# First create the base model to tune
rf = RandomForestClassifier()
# Random search of parameters, using 3 fold cross validation, 
# search across 100 different combinations, and use all available cores
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
# Fit the random search model
rf_random.fit(X_train, y_train)


# In[ ]:


from sklearn.metrics import accuracy_score

print(rf_random.best_params_)
best_model = rf_random.best_estimator_
preds = best_model.predict(X_train)
accuracy_score(y_train, preds)


# <H3> Try a Grid Search using the Random results
# 

# In[ ]:


from sklearn.model_selection import GridSearchCV

# Create the parameter grid based on the results of random search 
param_grid = {
    'bootstrap': [True],
    'max_depth': [int(x) for x in np.linspace(10, 30, num = 10)],
    'max_features': [2,3],
    'min_samples_leaf': [1],
    'min_samples_split': [10],
    'n_estimators': [int(x) for x in np.linspace(1400, 1800, num = 30)]
}

# Create a based model
rf = RandomForestClassifier()
# Instantiate the grid search model
grid_search = GridSearchCV(estimator = rf, param_grid = param_grid, 
                          cv = 3, n_jobs = -1, verbose = 2)
grid_search.fit(X_train, y_train)


# In[ ]:


print(grid_search.best_params_)
best_model = grid_search.best_estimator_
preds = best_model.predict(X_train)
accuracy_score(y_train, preds)


# In[ ]:




