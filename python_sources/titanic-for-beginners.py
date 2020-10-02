#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


# visualizationb
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


train_df = pd.read_csv("../input/train.csv")
test_df = pd.read_csv("../input/test.csv")
combine = [train_df, test_df]


# In[4]:


print(train_df.columns.values)


# In[5]:


train_df.head()


# In[6]:


train_df.tail()


# In[7]:


train_df.info()
print('_'*40)
test_df.info()


# In[8]:


train_df.describe()


# In[9]:


#Analysis
train_df[['Sex', 'Survived']].groupby(['Sex'], as_index=False).mean().sort_values(by='Sex', ascending = False)


# In[10]:


g = sns.FacetGrid(train_df, col='Survived')
g.map(plt.hist, 'Age', bins=20)


# In[11]:


#wrangle data
print("Before", train_df.shape, test_df.shape, combine[0].shape, combine[1].shape)

train_df = train_df.drop(["Pclass", "Ticket", "Cabin", "SibSp", "Parch", "Fare", "Embarked"], axis=1)
test_df = test_df.drop(["Pclass", "Ticket", "Cabin", "SibSp", "Parch", "Fare", "Embarked"], axis=1)
combine = [train_df, test_df]

print("After", train_df.shape, test_df.shape, combine[0].shape, combine[1].shape)


# In[12]:


#creating new feature
#striping title off name
for dataset in combine:
    dataset['Title'] = dataset.Name.str.extract(' ([A-Za-z]+)\.', expand = False)
    
pd.crosstab(train_df['Title'], train_df['Sex'])


# In[13]:


for dataset in combine:
    dataset['Title'] = dataset['Title'].replace(['Lady', 'Countess','Capt', 'Col',    'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')

    dataset['Title'] = dataset['Title'].replace('Mlle', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Ms', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Mme', 'Mrs')
    
train_df[['Title', 'Survived']].groupby(['Title'], as_index=False).mean()


# In[14]:


train_df.head()


# In[15]:


#we can convert the categorical titles to ordinal
title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}
for dataset in combine:
    dataset['Title'] = dataset['Title'].map(title_mapping)
    dataset['Title'] = dataset['Title'].fillna(0)
    
train_df.head()


# In[16]:


#lets now drop the name column, the passenger id will also be droped in the train_df
train_df = train_df.drop(['Name', 'PassengerId'], axis=1)
test_df = test_df.drop(['Name'], axis=1)
combine = [train_df, test_df]

train_df.shape, test_df.shape


# In[17]:


train_df.head()


# In[18]:


test_df.head()


# In[19]:


#Now we will convert our sex column from string to integer
for dataset in combine:
    dataset['Sex'] = dataset['Sex'].map({"female": 1, "male": 0}).astype(int)

    
train_df.head()


# In[20]:


#Lets check for missing values
train_df[train_df.isnull().any(axis=1)].head()


# In[21]:


#We will resolve missing values with interpolation
newtrain_df = train_df.interpolate()
newtrain_df.head()


# In[22]:


newtest_df = test_df.interpolate()
newtest_df.head()


# In[23]:


#we will create a newcombine to hold the new train and test
newcombine = [newtrain_df, newtest_df]


# In[24]:


#lets group the age into 5
newtrain_df['AgeGroup'] = pd.cut(newtrain_df['Age'], 5)
newtrain_df[['AgeGroup', 'Survived']].groupby(['AgeGroup'], as_index=False).mean().sort_values(by='AgeGroup', ascending = True)


# In[25]:


#Let us replace Age with ordinals based on these group.

for dataset in newcombine:    
    dataset.loc[ dataset['Age'] <= 16, 'Age'] = 0
    dataset.loc[(dataset['Age'] > 16) & (dataset['Age'] <= 32), 'Age'] = 1
    dataset.loc[(dataset['Age'] > 32) & (dataset['Age'] <= 48), 'Age'] = 2
    dataset.loc[(dataset['Age'] > 48) & (dataset['Age'] <= 64), 'Age'] = 3
    dataset.loc[ dataset['Age'] > 64, 'Age']
newtrain_df.head()


# In[26]:


newtest_df.head()


# In[27]:


#we will now drop the agegroup column
newtrain_df = newtrain_df.drop(['AgeGroup'], axis=1)


# In[28]:


newtrain_df.head()


# In[29]:


#Now we are done with wrangling and analyzing, we will now train our model to make predictions, then take its accuracy

from sklearn.linear_model import LogisticRegression


# In[30]:


X_train = newtrain_df.drop("Survived", axis=1)
Y_train = newtrain_df["Survived"]
X_test  = newtest_df.drop("PassengerId", axis=1).copy()
X_train.shape, Y_train.shape, X_test.shape


# In[31]:


# Logistic Regression

logreg = LogisticRegression()
logreg.fit(X_train, Y_train)
Y_pred = logreg.predict(X_test)
accuracy= round(logreg.score(X_train, Y_train) * 100, 2)
accuracy


# In[32]:


#Our model is 77.67 accurate.

