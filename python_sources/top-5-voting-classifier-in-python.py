#!/usr/bin/env python
# coding: utf-8

# ## Author: Caio Avelino
# * [LinkedIn](https://www.linkedin.com/in/caioavelino/)
# * [Kaggle](https://www.kaggle.com/avelinocaio)

# ## Project Phases:
# > 
# * **0) Libraries and Data Loading**
# * **1) Exploratory Analysis and Data Cleaning**
# * **2) Feature Importance**
# * **3) Train Model**
# * **4) Voting**
# * **5) Submission**

# # 0-Libraries and Data Loading

# In[ ]:


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from scipy import stats
from matplotlib.gridspec import GridSpec
from scipy.special import boxcox1p
import warnings

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier, ExtraTreesClassifier, VotingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

warnings.filterwarnings("ignore") # ignoring annoying warnings


# > Ignoring warnings that are not relevant for this project.

# In[ ]:


warnings.filterwarnings("ignore")


# > Loading data.

# In[ ]:


gender_submission = pd.read_csv("../input/titanic/gender_submission.csv")
test = pd.read_csv("../input/titanic/test.csv")
train = pd.read_csv("../input/titanic/train.csv")
test["Survived"] = np.nan # we don't have target values for the test


# > Here we concat train and test into one, so we can analyze everything and replace nan values later based on all dataset.

# In[ ]:


dataset = pd.concat([train,test],axis=0).reset_index(drop=True)
dataset = dataset.fillna(np.nan)


# # 1-Exploratory Analysis and Data Cleaning

# In[ ]:


dataset.head(10)


# > Let's see the dataset types, nan quantity for each column and describe them.

# In[ ]:


dataset.dtypes


# In[ ]:


dataset.isnull().sum(axis = 0)


# > **Age**, **Cabin**, **Fare** and **Embarked** have nan values. 
# We will need to analyze each feature individually to get better results.
# **Survived** has nan values just because of test data.

# In[ ]:


dataset.describe()


# > This results shows that probably **Fare**, for example, has outliers, since its maximum value is so much higher than 75% of the data. Also the mean is very different from median (50%).

# ### SibSp and Parch

# In[ ]:


sns.factorplot(x='SibSp', 
               size= 7, 
               aspect= 2,
               data=train, 
               y ='Survived',
               palette = "dark")
plt.xlabel('\nSibSp')
plt.ylabel('Survival Probability\n')
plt.show()


# > Small numbers of SibSp have higher probability to survive.

# In[ ]:


sns.factorplot(x='Parch', 
               size= 7, 
               aspect= 2,
               data=train, 
               y ='Survived',
               palette = "dark")
plt.xlabel('\nParch')
plt.ylabel('Survival Probability\n')
plt.show()


# > Small numbers of Parch have higher probability to survive.

# > Since these features have similar behavior, then we can add them with each person being analyzed.

# In[ ]:


dataset["Family"] = dataset["SibSp"] + dataset["Parch"] + 1
train["Family"] = train["SibSp"] + train["Parch"] + 1
test["Family"] = test["SibSp"] + test["Parch"] + 1


# > Repeating the factorplot for the Family.

# In[ ]:


sns.factorplot(x='Family', 
               size= 7, 
               aspect= 2,
               data=train, 
               y ='Survived', 
               palette = "dark")
plt.xlabel('\nFamily')
plt.ylabel('Survival Probability\n')
plt.show()


# > we don't need these features anymore, since we created another one.

# In[ ]:


dataset = dataset.drop(columns=["SibSp","Parch"])
train = train.drop(columns=["SibSp","Parch"])
test = test.drop(columns=["SibSp","Parch"])


# In[ ]:


plt.figure(figsize=(15,8))
sns.countplot(data=train,
              x='Family',
              palette = "dark")
plt.xlabel('\nFamily')
plt.ylabel('Number of Occurrences\n')
plt.show()


# > The countplot shows that the more families grow, the fewer occurrences happen.

# > Since there are 11 different categories for Family, lets group them in single, medium and big families.

# In[ ]:


dataset.Family = list(map(lambda x: 'Big' if x > 4 else('Single' if x == 1 else 'Medium'), dataset.Family))
train.Family = list(map(lambda x: 'Big' if x > 4 else('Single' if x == 1 else 'Medium'), train.Family))
test.Family = list(map(lambda x: 'Big' if x > 4 else('Single' if x == 1 else 'Medium'), test.Family))


# In[ ]:


plt.figure(figsize=(15,8))
sns.countplot(data=train,
              x='Family',
              palette = "dark")
plt.xlabel('\nFamily')
plt.ylabel('Number of Occurrences\n')
plt.show()


# > Now we have 3 categories.

# In[ ]:


sns.factorplot(x='Family', 
               size= 7, 
               aspect= 2,
               data=train, 
               y ='Survived',
               palette = "dark")
plt.xlabel('\nFamily')
plt.ylabel('Survival Probability\n')
plt.show()


# ### Sex

# In[ ]:


sns.factorplot(x='Sex', 
               size= 7, 
               aspect= 2,
               data=train, 
               y ='Survived',
               palette = "dark")
plt.xlabel('\nSex')
plt.ylabel('Survival Probability\n')
plt.show()


# > This clearly shows that a woman has higher probability to survive.

# > Many models need to receive numbers, not text. So, let's change **sex** from string to integer type.
# 

# In[ ]:


dataset.Sex = dataset.Sex.map({'male': 0, 'female': 1})
train.Sex = train.Sex.map({'male': 0, 'female': 1})
test.Sex = test.Sex.map({'male': 0, 'female': 1})


# ### Pclass

# In[ ]:


sns.factorplot(x='Pclass', 
               size= 7, 
               aspect= 2,
               data=train, 
               y ='Survived',
               kind='bar',
               palette = "dark")
plt.xlabel('\nPclass')
plt.ylabel('Survival Probability\n')
plt.show()


# > This shows that first class has higher probability to survive, probably because of influence.

# ### Fare

# > Since we have not so many nan values for this feature, then we can use the dataset median to fill them.

# In[ ]:


dataset["Fare"] = dataset["Fare"].fillna(dataset["Fare"].median())
train["Fare"] = train["Fare"].fillna(dataset["Fare"].median())
test["Fare"] = test["Fare"].fillna(dataset["Fare"].median())


# > **Fare** can be considered as continuous variable, so we can plot its distribution.

# In[ ]:


plt.figure(figsize=(20,8))
sns.distplot(train['Fare'], color = "steelblue", hist_kws={"rwidth":0.80, 'alpha':1.0})
plt.xticks(np.arange(0,600,10),rotation=45)
plt.xlabel('\nFare')
plt.ylabel('Distribution\n')
plt.show()


# > It seems that the curve has a positive skewness (to the left).

# In[ ]:


plt.figure(figsize=(15,8))
sns.violinplot(y='Fare',
            data=dataset,
            x='Survived',
            palette = "dark")
plt.xlabel('\nSurvived')
plt.ylabel('Fare\n')
plt.show()


# > Probably the people who payed more have higher probability to suvive, but there aren't many.

# > Let's divide *Fare* in categories, first we need to create balanced category shapes.

# In[ ]:


dataset[dataset.Fare.between(0,10)].shape


# In[ ]:


dataset[dataset.Fare.between(11,25)].shape


# In[ ]:


dataset[dataset.Fare.between(26,50)].shape


# In[ ]:


dataset[dataset.Fare > 51].shape


# > So, lets divide the feature values into 3 categories, with similiar shape.

# In[ ]:


dataset.Fare = list(map(lambda x: 'Very Low' if x <= 10 
         else('Low' if (x > 10 and x < 26) 
              else('Medium' if (x >= 26 and x <= 50) else 'High')), dataset.Fare))

train.Fare = list(map(lambda x: 'Very Low' if x <= 10 
         else('Low' if (x > 10 and x < 26) 
              else('Medium' if (x >= 26 and x <= 50) else 'High')), train.Fare))

test.Fare = list(map(lambda x: 'Very Low' if x <= 10 
         else('Low' if (x > 10 and x < 26) 
              else('Medium' if (x >= 26 and x <= 50) else 'High')), test.Fare))


# In[ ]:


sns.factorplot(x='Fare', 
               size= 7, 
               aspect= 2,
               data=train, 
               y ='Survived',
               palette = "dark")
plt.xlabel('\nFare')
plt.ylabel('Survival Probability\n')
plt.show()


# > Here we can see that high fare people have higher probability to survive, and very low fare people have not.

# ### Embarked

# In[ ]:


plt.figure(figsize=(15,8))
sns.countplot(x='Embarked', 
               data=train, 
               palette = "dark")
plt.xlabel('\nEmbarked')
plt.ylabel('Number of Occurrences\n')
plt.show()


# > 'S' ir more frequent in the dataset.

# In[ ]:


sns.factorplot(x='Embarked', 
               size= 7, 
               aspect= 2,
               data=train, 
               y ='Survived',
               palette = "dark")
plt.xlabel('\nEmbarked')
plt.ylabel('Survival Probability\n')
plt.show()


# > Another variable that shows a difference in survival probability.

# > We are going to fill the two nan values with the most frequent category.

# In[ ]:


dataset.Embarked = dataset.Embarked.fillna('S')
train.Embarked = train.Embarked.fillna('S')
test.Embarked = test.Embarked.fillna('S')


# ### Name

# > Getting the title (Mr, Mrs, Miss and others) which is present in all rows and creating another column.

# In[ ]:


title = []
for i in dataset.Name.str.split(', '):
    title.append(i[1].split('. ')[0])
dataset["Title"] = title

title = []
for i in train.Name.str.split(', '):
    title.append(i[1].split('. ')[0])
train["Title"] = title

title = []
for i in test.Name.str.split(', '):
    title.append(i[1].split('. ')[0])
test["Title"] = title


# > Dropping **Name** column that we don't need anymore.

# In[ ]:


dataset = dataset.drop(columns=["Name"])
train = train.drop(columns=["Name"])
test = test.drop(columns=["Name"])


# In[ ]:


plt.figure(figsize=(20,8))
sns.countplot(dataset.Title, palette = "dark")
plt.xticks(rotation=45)
plt.xlabel('\nTitle')
plt.ylabel('Number of Occurrences\n')
plt.show()


# > Titles frequency: we can see that the majority of the people has titles like 'Mr', 'Mrs' and 'Miss'. We can group the others into one category.

# In[ ]:


dataset.Title = list(map(lambda x: x if (x == 'Mr' or x == 'Mrs' or x == 'Miss')
         else('Other'), dataset.Title))

train.Title = list(map(lambda x: x if (x == 'Mr' or x == 'Mrs' or x == 'Miss')
         else('Other'), train.Title))

test.Title = list(map(lambda x: x if (x == 'Mr' or x == 'Mrs' or x == 'Miss')
         else 'Other', test.Title))


# In[ ]:


plt.figure(figsize=(15,8))
sns.countplot(dataset.Title, palette = "dark")
plt.xlabel('\nTitle')
plt.ylabel('Number of Occurrences\n')
plt.show()


# In[ ]:


sns.factorplot(x='Title', 
               size= 7, 
               aspect= 2,
               data=train, 
               y ='Survived',
               palette = "dark")
plt.xlabel('\nTitle')
plt.ylabel('Survival Probability\n')
plt.show()


# > Clearly the gentlemen are in danger.

# ### Cabin

# > This variable doesn't seem to have a lot of value except the first letter. 
# So let's extract it, if nan then let the letter be 'Z'.

# In[ ]:


cabin = []
for i in dataset.Cabin:
    if type(i) != float:
        cabin.append(i[0])
    else:
        cabin.append('Z')
dataset.Cabin = cabin

cabin = []
for i in train.Cabin:
    if type(i) != float:
        cabin.append(i[0])
    else:
        cabin.append('Z')
train.Cabin = cabin

cabin = []
for i in test.Cabin:
    if type(i) != float:
        cabin.append(i[0])
    else:
        cabin.append('Z')
test.Cabin = cabin


# In[ ]:


plt.figure(figsize=(15,8))
sns.countplot(dataset.Cabin, palette = "dark")
plt.xlabel('\nCabin')
plt.ylabel('Number of Occurrences\n')
plt.show()


# In[ ]:


sns.factorplot(x='Cabin', 
               size= 7, 
               aspect= 2,
               data=train, 
               y ='Survived',
               palette = "dark")
plt.xlabel('\nCabin')
plt.ylabel('Survival Probability\n')
plt.show()


# > It seems that people without cabines have less chance to survive, but standard deviations are large for some letters. We can group letters with similar behaviors.

# In[ ]:


dataset.Cabin = dataset.Cabin.map({'B':'BCDE','C':'BCDE','D':'BCDE','E':'BCDE','A':'AFG','F':'AFG','G':'AFG','Z':'Z','T':'Z'})
train.Cabin = train.Cabin.map({'B':'BCDE','C':'BCDE','D':'BCDE','E':'BCDE','A':'AFG','F':'AFG','G':'AFG','Z':'Z','T':'Z'})
test.Cabin = test.Cabin.map({'B':'BCDE','C':'BCDE','D':'BCDE','E':'BCDE','A':'AFG','F':'AFG','G':'AFG','Z':'Z','T':'Z'})


# > Counting them again, by group.

# In[ ]:


plt.figure(figsize=(15,8))
sns.countplot(dataset.Cabin, palette = "dark")
plt.xlabel('\nCabin')
plt.ylabel('Number of Occurrences\n')
plt.show()


# > New factorplot.

# In[ ]:


sns.factorplot(x='Cabin', 
               size= 7, 
               aspect= 2,
               data=train, 
               y ='Survived',
               palette = "dark")
plt.xlabel('\nCabin')
plt.ylabel('Survival Probability\n')
plt.show()


# ### Ticket

# > This variable also doesn't seem to have a lot of value except the first number.

# In[ ]:


tickets = []
for i in dataset.Ticket:
    tickets.append(i.split(' ')[-1][0])
dataset.Ticket = tickets

tickets = []
for i in train.Ticket:
    tickets.append(i.split(' ')[-1][0])
train.Ticket = tickets

tickets = []
for i in test.Ticket:
    tickets.append(i.split(' ')[-1][0])
test.Ticket = tickets


# > Let's see the number of occurrences for each number.

# In[ ]:


plt.figure(figsize=(15,8))
sns.countplot(dataset.Ticket.sort_values(), palette = "dark")
plt.xlabel('\nTicket')
plt.ylabel('Number of Occurrences\n')
plt.show()


# > The more frequent numbers are 1, 2 and 3.

# In[ ]:


sns.factorplot(x='Ticket', 
               size= 7, 
               aspect= 2,
               data=train, 
               y ='Survived',
               palette = "dark",
               order=train.Ticket.sort_values().unique())
plt.xlabel('\nTicket')
plt.ylabel('Survival Probability\n')
plt.show()


# > Since 1, 2 and 3 have more occurrences and the others have large standard deviations, we can group these into one category.

# In[ ]:


dataset.Ticket = list(map(lambda x: 4 if (x == 'L' or int(x) >= 4) else int(x), dataset.Ticket))
train.Ticket = list(map(lambda x: 4 if (x == 'L' or int(x) >= 4) else int(x), train.Ticket))
test.Ticket = list(map(lambda x: 4 if (x == 'L' or int(x) >= 4) else int(x), test.Ticket))


# > New countplot.

# In[ ]:


plt.figure(figsize=(15,8))
sns.countplot(dataset.Ticket.sort_values(), palette = "dark")
plt.xlabel('\nTicket')
plt.ylabel('Number of Occurrences\n')
plt.show()


# > And now we have 4 categories, with different probabilities.

# In[ ]:


sns.factorplot(x='Ticket', 
               size= 7, 
               aspect= 2,
               data=train, 
               y ='Survived',
               palette = "dark",
               order=train.Ticket.sort_values().unique())
plt.xlabel('\nTicket')
plt.ylabel('Survival Probability\n')
plt.show()


# ### Age

# > We will need to see which features have more correlation with age, so we can safely replace nan values.

# In[ ]:


plt.figure(figsize=(15,8))
sns.boxplot(x='Family', data=dataset,y='Age', palette = "dark")
plt.xlabel('\nFamily')
plt.ylabel('Age\n')
plt.show()


# In[ ]:


plt.figure(figsize=(15,8))
sns.boxplot(x='Title',data=dataset,y='Age', palette = "dark")
plt.xlabel('\nTitle')
plt.ylabel('Age\n')
plt.show()


# In[ ]:


plt.figure(figsize=(15,8))
sns.boxplot(x='Ticket',data=dataset,y='Age', palette = "dark")
plt.xlabel('\nTicket')
plt.ylabel('Age\n')
plt.show()


# In[ ]:


plt.figure(figsize=(15,8))
sns.boxplot(x='Sex',data=dataset,y='Age', palette = "dark")
plt.xlabel('\nSex')
plt.ylabel('Age\n')
plt.show()


# In[ ]:


plt.figure(figsize=(15,8))
sns.boxplot(x='Fare',data=dataset,y='Age', palette = "dark")
plt.xlabel('\nFare')
plt.ylabel('Age\n')
plt.show()


# In[ ]:


plt.figure(figsize=(15,8))
sns.boxplot(x='Embarked',data=dataset,y='Age', palette = "dark")
plt.xlabel('\nEmbarked')
plt.ylabel('Age\n')
plt.show()


# In[ ]:


plt.figure(figsize=(15,8))
sns.boxplot(x='Pclass',data=dataset,y='Age', palette = "dark")
plt.xlabel('\nPclass')
plt.ylabel('Age\n')
plt.show()


# In[ ]:


plt.figure(figsize=(15,8))
sns.boxplot(x='Cabin',data=dataset,y='Age', palette = "dark")
plt.xlabel('\nCabin')
plt.ylabel('Age\n')
plt.show()


# > With the boxplots results we can say that Pclass and Title are important to calculate the age.

# > So we can calculate the median of the age grouped by these features.

# In[ ]:


medians = pd.DataFrame(dataset.groupby(['Pclass', 'Title'])['Age'].median())
medians


# > Let's separate the dataset indexes that have **Age** nan values.

# > By creating list of medians based on variables values it's possible to replace nan's safely.

# In[ ]:


ages = []
for i in dataset[dataset.Age.isnull() == True][["Pclass","Title"]].values:
    ages.append(medians.ix[(i[0],  i[1])].Age)
    
dataset.Age[dataset.Age.isnull() == True] = ages


# > Doing the same for Train and Test.

# In[ ]:


index = dataset[dataset.Age.isnull() == True].index
train_idx = index[index <= 890]
test_idx = index[index > 890]

train['Age'][train.index.isin(train_idx)] = dataset['Age'][dataset.index.isin(train_idx)].values
test['Age'][test.index.isin(test_idx - 891)] = dataset['Age'][dataset.index.isin(test_idx)].values


# > Now that we have all ages, it's easy to group them into categories.

# In[ ]:


ages = []
for i in dataset.Age:
    if i < 18:
        ages.append('less_18')
    elif i >= 18 and i < 50:
        ages.append('18_50')
    else:
        ages.append('greater_50')

dataset.Age = ages

ages = []
for i in train.Age:
    if i < 18:
        ages.append('less_18')
    elif i >= 18 and i < 50:
        ages.append('18_50')
    else:
        ages.append('greater_50')

train.Age = ages

ages = []
for i in test.Age:
    if i < 18:
        ages.append('less_18')
    elif i >= 18 and i < 50:
        ages.append('18_50')
    else:
        ages.append('greater_50')

test.Age = ages


# > Let's now see the probabilities for each category.

# In[ ]:


sns.factorplot(x='Age', 
               size= 7, 
               aspect= 2,
               data=train, 
               y ='Survived',
               palette = "dark")
plt.xlabel('\nAge')
plt.ylabel('Survival Probability\n')
plt.show()


# > Children and teenagers have more probability to survive.

# ### Splitting variables into train and test sets

# In[ ]:


# PassengerId is not relevant and Sex (we don't want this variable to get dummied - see next cell)
x_train = train.loc[:, ~train.columns.isin(['PassengerId', 'Survived', 'Sex'])]
y_train = train.Survived
x_test = test.loc[:, ~test.columns.isin(['PassengerId', 'Survived', 'Sex'])]


# > Transforming each category of each column into another column with 1 or 0 value (get_dummies).

# In[ ]:


x_train = pd.get_dummies(x_train)
x_train["Sex"] = train.Sex # adding sex
x_test = pd.get_dummies(x_test)
x_test["Sex"] = test.Sex # adding sex


# # 2-Features Importance

# > Lets see the most important features with the Random Forest Classifier.

# In[ ]:


rf = RandomForestClassifier() 
rf.fit(x_train, y_train)


# In[ ]:


feature_importances = pd.DataFrame(rf.feature_importances_,
                                   index = x_train.columns,
                                   columns=['importance']).sort_values('importance',ascending=False)

plt.figure(figsize=(20,8))
plt.xticks(rotation=45)
plt.plot(feature_importances)
plt.scatter(y=feature_importances.importance,x=feature_importances.index)
plt.ylabel('Importance\n')
plt.grid()
plt.show()


# > It seems that '**Sex**' and '**Mr**' are the most important variables.

# # 3-Train Model

# > Here we are going to try some models.

# ### Adaboost

# In[ ]:


ABC = AdaBoostClassifier(DecisionTreeClassifier())

ABC_param_grid = {"base_estimator__criterion" : ["gini", "entropy"],
                  "base_estimator__splitter" :   ["best", "random"],
                  "algorithm" : ["SAMME","SAMME.R"],
                  "n_estimators" :[5,6,7,8,9,10,20],
                  "learning_rate":  [0.001, 0.01, 0.1, 0.3]}

gsABC = GridSearchCV(ABC, param_grid = ABC_param_grid, cv = 10, scoring = "accuracy", n_jobs = 6, verbose = 1)

gsABC.fit(x_train,y_train)

ada_best = gsABC.best_estimator_

gsABC.best_score_


# ### ExtraTress

# In[ ]:


ExtC = ExtraTreesClassifier()

ex_param_grid = {"max_depth": [3, 4, 5],
                 "max_features": [3, 10, 15],
                 "min_samples_split": [2, 3, 4],
                 "min_samples_leaf": [1, 2],
                 "bootstrap": [False,True],
                 "n_estimators" :[100,200,300],
                 "criterion": ["gini","entropy"]}

gsExtC = GridSearchCV(ExtC, param_grid = ex_param_grid, cv = 10, scoring = "accuracy", n_jobs = 6, verbose = 1)

gsExtC.fit(x_train,y_train)

ext_best = gsExtC.best_estimator_

gsExtC.best_score_


# ### Random Forest

# In[ ]:


rf_test = {"max_depth": [24,26],
           "max_features": [6,8,10],
           "min_samples_split": [3,4],
           "min_samples_leaf": [3,4],
           "bootstrap": [True],
           "n_estimators" :[50,80],
           "criterion": ["gini","entropy"],
           "max_leaf_nodes":[26,28],
           "min_impurity_decrease":[0.0],
           "min_weight_fraction_leaf":[0.0]}

tuning = GridSearchCV(estimator = RandomForestClassifier(), param_grid = rf_test, scoring = 'accuracy', n_jobs = 6, cv = 10)

tuning.fit(x_train,np.ravel(y_train))

rf_best = tuning.best_estimator_

tuning.best_score_


# ### GBM

# In[ ]:


GBM = GradientBoostingClassifier()

gb_param_grid = {'loss' : ["deviance"],
                 'n_estimators' : [450,460,500],
                 'learning_rate': [0.1,0.11],
                 'max_depth': [7,8],
                 'min_samples_leaf': [30,40],
                 'max_features': [0.1,0.4,0.6]}

gsGBC = GridSearchCV(GBM, param_grid = gb_param_grid, cv = 10, scoring = "accuracy", n_jobs = 6, verbose = 1)

gsGBC.fit(x_train,y_train)

gbm_best = gsGBC.best_estimator_

gsGBC.best_score_


# ### SVC

# In[ ]:


SVMC = SVC(probability=True)

svc_param_grid = {'kernel': ['rbf'], 
                  'gamma': [0.027,0.029,0.03,0.031],
                  'C': [45,55,76,77,78,85,95,100],
                  'tol':[0.001,0.0008,0.0009,0.0011]}

gsSVMC = GridSearchCV(SVMC, param_grid = svc_param_grid, cv = 10, scoring = "accuracy", n_jobs = 6, verbose = 1)

gsSVMC.fit(x_train,y_train)

svm_best = gsSVMC.best_estimator_

gsSVMC.best_score_


# ### XGBoost

# In[ ]:


XGB = XGBClassifier()

xgb_param_grid = {'learning_rate': [0.1,0.04,0.01], 
                  'max_depth': [5,6,7],
                  'n_estimators': [350,400,450,2000], 
                  'gamma': [0,1,5,8],
                  'subsample': [0.8,0.95,1.0]}

gsXBC = GridSearchCV(XGB, param_grid = xgb_param_grid, cv = 10, scoring = "accuracy", n_jobs = 6, verbose = 1)

gsXBC.fit(x_train,y_train)

xgb_best = gsXBC.best_estimator_

gsXBC.best_score_


# ## Models Correlations

# > This is a correlation between the models predictions. With the results we can see if its possible to combine them into a Voting Classifier.

# In[ ]:


corr = pd.concat([pd.Series(rf_best.predict(x_test), name="RF"),
                              pd.Series(ext_best.predict(x_test), name="EXT"),
                              pd.Series(svm_best.predict(x_test), name="SVC"), 
                              pd.Series(gbm_best.predict(x_test), name="GBM"),
                              pd.Series(xgb_best.predict(x_test), name="XGB"),
                              pd.Series(ada_best.predict(x_test), name="ADA")],axis=1)

plt.figure(figsize=(18,18))
sns.heatmap(corr.corr(),annot=True)
plt.show()


# # 4-Voting Classifier

# > We can use a Voting Classifier to ensemble all the models and to build a powerfull one.

# In[ ]:


voting = VotingClassifier(estimators=[('rfc', rf_best), 
                                      ('extc', ext_best),
                                      ('svc', svm_best),
                                      ('gbc',gbm_best),
                                      ('xgbc',xgb_best),
                                      ('ada',ada_best)])

v_param_grid = {'voting':['soft',
                          'hard']} # tuning voting parameter

gsV = GridSearchCV(voting, 
                   param_grid = 
                   v_param_grid, 
                   cv = 10, 
                   scoring = "accuracy",
                   n_jobs = 6, 
                   verbose = 1)

gsV.fit(x_train,y_train)

v_best = gsV.best_estimator_

gsV.best_score_


# # 5-Submission

# > Finally, it's time to test the model in the test set and make the submission.

# In[ ]:


pred = v_best.predict(x_test)

submission = pd.DataFrame(test.PassengerId)
submission["Survived"] = pd.Series(pred)


# In[ ]:


submission.to_csv("submission.csv",index=False)


# ### If you made this so far, let me know if you have questions, suggestions or critiques to improve the model.
