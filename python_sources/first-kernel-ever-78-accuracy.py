#!/usr/bin/env python
# coding: utf-8

# ### This notebook will make use of the Titanic dataset on Kaggle which can be viewed here, https://www.kaggel.com/c/titanic.
# ### The task is to predict the Survived variable based on several independent variables.

# In[ ]:


import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import preprocessing, model_selection, ensemble, metrics, pipeline, compose, impute
import xgboost as xgb
import category_encoders as ce
import matplotlib.pyplot as plt
import re

# import training dataset
train = pd.read_csv('../input/train.csv')

# import test dataset
test = pd.read_csv('../input/test.csv')


# Now let's see the columns.

# In[ ]:


train.head()


# The final task is to predict the 'Survived' variable. It is seen that Name, Sex, Ticket, Cabin, and Embarked are the categorical variables. Before tackling each, let's check missing.

# In[ ]:


missing = pd.isnull(train).sum() / len(train)
missing = missing[missing > 0]
print(missing)


# In[ ]:


# Pclass
sns.distplot(train['Pclass'])


# Most of the passengers are from third class. How does the surviability change based on class?

# In[ ]:


sns.countplot(x = 'Survived', hue = 'Pclass', data = train)


# Two anomalies: the number of third class passengers who did not survive, and the number of second class passengers being fewer than the number of third class passengers who did survived. It is probably explained through other variables, like Sex.

# In[ ]:


sns.catplot(x = 'Survived', hue = 'Pclass', col = 'Sex', data = train, kind = 'count')


# Considering just the third class who survived, the number is higher than second class' total survival because of more females in the group.

# In[ ]:


# creating a transform function to use later
def transform_1_Sex(data):
    '''
    data should be entire dataframe. Changes data inplace.
    '''
    data['Sex'] = np.vectorize(lambda x: 1 if x == 'female' else 0)(data['Sex'])
    data['Sex_male'] = [0 if x == 1 else 1 for x in data['Sex']]

#transform_1_Sex(train)


# Now let's look at Age where 20% of values are missing.

# In[ ]:


# Age
sns.distplot(train['Age'][pd.isna(train['Age']) == False])


# How does the Survive variable change when age changes?

# In[ ]:


print('Median of actual age: ' + str(np.median(train['Age'][pd.isna(train['Age'])== False])))
print('Quantiles: ' + str(np.quantile(train['Age'][~pd.isna(train['Age'])], [x / 100 for x in range(0, 101, 5)])))
# let's create ranges and check survival
missing = pd.isna(train['Age'])
brackets = np.digitize(train['Age'], np.quantile(train['Age'][~missing], [x / 100 for x in range(0, 101, 5)]))
brackets[missing] = 22 # so that 21 is max, and missing are 22;the function np.digitize treats NaN as out of range(22 here)
_, axes = plt.subplots(1, 2, figsize = (15,7))
sns.countplot(x = brackets, hue = train['Survived'], ax = axes[0])
sns.countplot(x = brackets, hue = train['Sex'], ax = axes[1])


# For all age groups, except the first two and number 10, the passengers who survived were lower than tho who did not. However, there are some groups where the survived were far lower than those who did not. Since the variable seems cyclical (low age - high survival, middle age - low survival, high age - high survival, NaN - low survival), categorical encoding might work well.

# In[ ]:


for i in range(1, 23):
    occurences = train['Survived'][brackets == i]
    print('Survived Percent per age group: ' + str(i) + '\t' + str(sum(occurences) / len(occurences)))


# If the percentage is above 0.5 (arbitrary), then code it as 1, otherwise 0. So, that would be: 1, 2, 10, 14, 21. Those correspond to groups:
# <br>1: 0 - 0.42
# <br>2: 0.42 - 4
# <br>10: 25 - 27
# <br>14: 31.8 - 34
# <br>21: 56 - max

# In[ ]:


# create age transformer
def transform_age(x):
    if pd.isna(x):
        return 0
    elif (x < 4) or ((x >= 25) and (x < 27)) or ((x >= 31.8) and (x < 34)) or (x >= 56):
        return 1
    else:
        return 0

def transform_2_Age(data):
    '''
    data should be entire dataframe. Changes data inplace.
    '''
    data['Age'] = np.vectorize(transform_age)(data['Age'])
    data['Age_low_survival'] = [0 if x == 1 else 1 for x in data['Age']]
#transform_2_Age(train)


# Next are SibSp and Parch. They do not have any missing values. However, these allow a unique opportunity: creation of new variables. The two I think of are TotalFamilyMembers and IsAlone.

# In[ ]:


_, axes = plt.subplots(1, 2, figsize = (15, 7))
sns.distplot(train['SibSp'], ax = axes[0])
sns.distplot(train['Parch'], ax = axes[1])


# How does survival change?

# In[ ]:


_, axes = plt.subplots(1, 2, figsize = (15, 7))
sns.countplot(x = train['SibSp'], hue = train['Survived'], ax = axes[0])
sns.countplot(train['Parch'], hue = train['Survived'], ax = axes[1])


# It seems a higher number means better chances of survival with Parch, however results are mixed with SibSp, with value of 1 being only one where number of survived were higher than those who did not.

# In[ ]:


# create another transformer based on two variables
def transform_3_Parch_SibSp(data):
    '''
    data should be the entire dataframe. Changes data inplace.
    '''
    data['TotalFamilyMembers'] = np.add(data['Parch'], data['SibSp'])
    data['IsAlone'] = np.vectorize(lambda x: 1 if x == 0 else 0)(data['TotalFamilyMembers'])
    data['IsNotAlone'] = [0 if x == 1 else 1 for x in data['IsAlone']]
#transform_3_Parch_SibSp(train)


# Left are Ticket, Fare, Cabin and Embarked. Cabin has a lot of missing values (~77%). So, encode it as 1 if the passenger had a cabin versus 0 if they did not.

# In[ ]:


def transform_4_Cabin(data):
    '''
    data should be entire dataframe. Changes data inplace.
    '''
    data['Cabin'] = np.vectorize(lambda x: 0 if pd.isna(x) else 1)(data['Cabin'])
    data['Cabin_non'] = [0 if x == 1 else 1 for x in data['Cabin']]
#transform_4_Cabin(train)


# Next Embarked has two very little missing values. Give it mode.

# In[ ]:


def transform_5_Embarked(data):
    '''
    data should be entire dataframe. Returns a dataframe which should be assigned.
    '''
    # get mode
    mode = data['Embarked'].value_counts().index[0]
    # give mode
    data.loc[pd.isna(data['Embarked']), ['Embarked']] = mode
    # create columns
    return ce.OneHotEncoder(cols = ['Embarked'], use_cat_names = True).fit_transform(data)
#train = transform_5_Embarked(train)


# Quick analysis of Fare.

# In[ ]:


sns.distplot(train['Fare'])


# Interestingly a lot of the fare is around 0, also this column is heavily skewed.

# In[ ]:


fare = preprocessing.power_transform(np.array(train['Fare']).reshape(-1, 1), method = 'yeo-johnson')
sns.distplot(fare)
# looks better
def transform_6_Fare(data):
    '''
    data should be entire dataframe. Changes data inplace.
    '''
    data['Fare'] = preprocessing.power_transform(np.array(data['Fare']).reshape(-1, 1), method = 'yeo-johnson')
#transform_6_Fare(train)


# Last is Ticket. What does it look like?

# In[ ]:


np.unique(train['Ticket'])
# how about dividing it in numbers and letters?


# In[ ]:


def transform_7_Ticket(data):
    '''
    data should be entire dataframe. Changes data inplace.
    '''
    data['Ticket'] = np.vectorize(lambda x: 1 if re.match('[0-9]+', x) is None else 0)(data['Ticket'])
    # 1 if letter, 0 otherwise
    data['Ticket_non_letter'] = [0 if x == 1 else 1 for x in data['Ticket']]
#transform_7_Ticket(train)


# In[ ]:


# coming back to Pclass, it may be better to categorically encode the variables for better distinction
def transform_8_Pclass(data):
    '''
    data should be entire dataframe. Use this function and assign value again.
    '''
    return ce.OneHotEncoder(cols = ['Pclass'], use_cat_names=True).fit_transform(data)


# Finally, analysis of Name.

# In[ ]:


train['Name']


# In[ ]:


# seems safe to take away first word and comma
salutation = train['Name'].str.split(', ', expand = True)[1].str.split('. ', expand = True)[0]
significant = salutation.value_counts() > 9 #(10% of train)
significant = significant.index[significant]
change_to_misc = np.vectorize(lambda x: 'Misc' if x not in significant else x)(salutation)
np.unique(change_to_misc, return_counts=True)


# In[ ]:


def transform_9_Name(data):
    '''
    data should be entire dataframe. Assign value after return.
    '''
    # the significant ones are Mr, Mrs, Miss, Master, rest Misc
    salutation = data['Name'].str.split(', ', expand = True)[1].str.split('. ', expand = True)[0]
    significant = salutation.value_counts() > 9 #(10% of train)
    significant = significant.index[significant]
    change_to_misc = np.vectorize(lambda x: 'Misc' if x not in significant else x)(salutation)
    data['Title'] = change_to_misc
    return ce.OneHotEncoder(cols = ['Title'], use_cat_names=True).fit_transform(data)


# #### Now it's time to prepare the data. All transformations are ready to be used.

# In[ ]:


def apply_transformations(df: pd.DataFrame):
    '''
    Applies all transformations. The returned dataframe will contain the dependent variable if it was passed.
    '''
    data = df.copy()
    transform_1_Sex(data)
    transform_2_Age(data)
    transform_3_Parch_SibSp(data)
    transform_4_Cabin(data)
    data = transform_5_Embarked(data)
    transform_6_Fare(data)
    transform_7_Ticket(data)
    data = transform_8_Pclass(data)
    data = transform_9_Name(data)
    # take out name
    p_id = data['PassengerId']
    # survived might still be in there
    return (data.drop(['Name', 'PassengerId'], axis = 1), p_id)


# In[ ]:


X, _ = apply_transformations(train)
y = X['Survived']
X.drop('Survived', axis = 1, inplace = True)


# In[ ]:


X.loc[1:10, :]


# In[ ]:


X.columns


# # Now train models.

# In[ ]:


kfold = model_selection.KFold(10, shuffle = True, random_state = 0)


# In[ ]:


rf = ensemble.RandomForestClassifier(n_estimators=100, bootstrap=False, n_jobs=6, random_state=0, verbose=0)
for k, (train_index, test_index) in enumerate(kfold.split(X, y)):
    rf.fit(X.loc[train_index, :], y[train_index])
    print(metrics.accuracy_score(y[test_index], rf.predict(X.loc[test_index, :])))


# In[ ]:


xgb_data = xgb.DMatrix(X, label = y)


# In[ ]:


params = {'eta': 0.2, 'lambda': 0.2, 'alpha': 0, 'eval_metric': 'error', 'objective': 'binary:hinge',
         'max_depth': 10, 'min_child_weight': 2, 'base_score': 0.38}
for k, (train_index, test_index) in enumerate(kfold.split(X, y)):
    xgb_model_1 = xgb.train(dtrain = xgb_data.slice(train_index), evals = [(xgb_data.slice(test_index), 'eval'), 
                                                             (xgb_data.slice(train_index), 'train')],
             early_stopping_rounds = 5, verbose_eval=True, params=params, num_boost_round=100)


# In[ ]:


params = {'eta': 0.1, 'lambda': 0.0, 'alpha': 0, 'eval_metric': 'error', 'objective': 'binary:hinge',
         'max_depth': 5, 'min_child_weight': 3}
for k, (train_index, test_index) in enumerate(kfold.split(X, y)):
    xgb_model_2 = xgb.train(dtrain = xgb_data.slice(train_index), evals = [(xgb_data.slice(test_index), 'eval'), 
                                                             (xgb_data.slice(train_index), 'train')],
             early_stopping_rounds = 5, verbose_eval=True, params=params, num_boost_round=100, xgb_model=xgb_model_1)


# In[ ]:


params = {'eta': 0.005, 'lambda': 0.0, 'alpha': 0, 'eval_metric': 'error', 'objective': 'binary:hinge',
         'max_depth': 10, 'min_child_weight': 2}
for k, (train_index, test_index) in enumerate(kfold.split(X, y)):
    xgb_model_3 = xgb.train(dtrain = xgb_data.slice(train_index), evals = [(xgb_data.slice(test_index), 'eval'), 
                                                             (xgb_data.slice(train_index), 'train')],
             early_stopping_rounds = 5, verbose_eval=True, params=params, num_boost_round=100, xgb_model = xgb_model_2)
    print('\n\nNEW ROUND\n\n')


# In[ ]:


X_test, p_id = apply_transformations(test)
print(X_test.columns)


# In[ ]:


X_test.loc[1:10, X.columns]


# In[ ]:


xgb_test_data = xgb.DMatrix(X_test.loc[:, X.columns])
y_pred = xgb_model_3.predict(xgb_test_data)


# In[ ]:


pd.DataFrame({'PassengerId':p_id,
              'Survived':y_pred}).to_csv('x_3.csv', header = True, index = False)
y_pred = xgb_model_2.predict(xgb_test_data)
pd.DataFrame({'PassengerId':p_id,
              'Survived':y_pred}).to_csv('x_2.csv', header = True, index = False)
y_pred = xgb_model_1.predict(xgb_test_data)
pd.DataFrame({'PassengerId':p_id,
              'Survived':y_pred}).to_csv('x_1.csv', header = True, index = False)

