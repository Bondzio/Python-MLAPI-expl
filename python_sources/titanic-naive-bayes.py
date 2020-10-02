#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd


# In[ ]:


train = pd.read_csv("/kaggle/input/titanic/train.csv")
train.sample(10)


# In[ ]:


test = pd.read_csv("/kaggle/input/titanic/test.csv")
test.sample(10)


# In[ ]:


print('train shape:', train.shape)
print('test shape:', test.shape)


# ### Imputing Missing Values

# In[ ]:


print(train.info())
print(test.info())


# In[ ]:


#there are empty values for age, cabin, and fare, we will replace them using median, and mode

# for efficient data cleaning
data_cleaner = [train,test]

for dataset in data_cleaner:
    dataset['Age'].fillna(dataset['Age'].median(), inplace = True)
    dataset['Embarked'].fillna(dataset['Embarked'].mode()[0], inplace = True)
    dataset['Fare'].fillna(dataset['Fare'].mode()[0], inplace = True)


# In[ ]:


print(train.info())
print(test.info())


# > ### Feature Engineering

# In[ ]:


#https://www.kaggle.com/ldfreeman3/a-data-science-framework-to-achieve-99-accuracy

for dataset in data_cleaner:   
    
    # create variable family size by adding siblings and parent/children
    dataset['FamilySize'] = dataset['SibSp'] + dataset['Parch'] + 1
    
    # alone passengers usually survive better
    dataset['IsAlone'] = 0
    #dataset[dataset['FamilySize'] == 1]['IsAlone'] = 1
    dataset['IsAlone'].loc[dataset['FamilySize'] == 1] = 1   
    
    # title
    dataset['Title'] = dataset['Name'].str.split(", ", expand=True)[1].str.split(".", expand=True)[0]
    
train.head()


# In[ ]:


train['Title'].value_counts()


# In[ ]:


# clean up titles
for dataset in data_cleaner:   
    for i in range(len(dataset)):
        if dataset['Title'][i] not in ['Mr', 'Miss', 'Mrs', 'Master', 'Dr', 'Rev']:
            dataset['Title'][i] = 'Others'

train.sample(5)


# > ### Training data with Naive Bayes
# 
# Why Naive Bayes? Eventually I want to turn this into a graphical model kernel to apply some bayesian network ;) stay tuned

# In[ ]:


train = train.drop(['Name', 'Ticket', 'Cabin'],axis = 1)
one_hot_encoded_training_predictors = pd.get_dummies(train)
train = one_hot_encoded_training_predictors.align(one_hot_encoded_training_predictors,
                                                                    join='left', 
                                                                    axis=1)
train = train[0]


# In[ ]:


test = test.drop(['Name', 'Ticket', 'Cabin'],axis = 1)
one_hot_encoded_training_predictors = pd.get_dummies(test)
test = one_hot_encoded_training_predictors.align(one_hot_encoded_training_predictors,
                                                                    join='left', 
                                                                    axis=1)
test = test[0]


# In[ ]:


# train test spilt
# https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html

from sklearn.model_selection import train_test_split

X = train.drop(['Survived'], axis = 1)
y = train['Survived']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


# In[ ]:


#htps://scikit-learn.org/stable/modules/naive_bayes.html
from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB()
y_pred = gnb.fit(X_train, y_train)
predictions = gnb.predict(X_test)

from sklearn.metrics import accuracy_score

accuracy_score(y_test, predictions)


# In[ ]:


test['Survived'] = gnb.predict(test)


# In[ ]:


submission = test[['PassengerId', 'Survived']]
submission.to_csv('submission.csv', index=False)


# In[ ]:


submission.head()


# In[ ]:




