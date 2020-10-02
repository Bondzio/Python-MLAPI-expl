#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd

import os 
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname,filename))


# In[ ]:


train = pd.read_csv('../input/titanic/train.csv')


# In[ ]:


train.describe

train.corr()
# In[ ]:


train.corr()


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.countplot(x = 'Parch', hue = "Survived", data = train)
plt.legend(loc = "upper right", title = "Survived ~ Sibsp")


# In[ ]:


sns.distplot(train[train['Survived'] == 0].Fare, kde=False,rug=False)


# In[ ]:


sns.distplot(train[train['Survived'] == 1].Fare,  kde=False,rug=False)


# In[ ]:


train.isnull().sum()


# In[ ]:


train.drop(['PassengerId','Name','Cabin','Ticket', ], axis=1, inplace=True)
train["Age"].fillna(train["Age"].median(skipna=True), inplace=True)
train["Embarked"].fillna(train['Embarked'].value_counts().idxmax(), inplace=True)


# In[ ]:


train['Alone']=np.where((train["SibSp"]+train["Parch"])>0, 0, 1)
train.drop(['SibSp', 'Parch'], axis=1, inplace=True)


# In[ ]:


pd.get_dummies(train['Sex'])


# In[ ]:


training = pd.get_dummies(train, columns=["Pclass","Embarked","Sex"], drop_first=True)
training


# In[ ]:


from sklearn.preprocessing import StandardScaler
train_standard = StandardScaler()
train_copied = training.copy()
train_standard.fit(train_copied[['Age','Fare']])
train_std = pd.DataFrame(train_standard.transform(train_copied[['Age','Fare']]))
train_std


# In[ ]:


from sklearn.linear_model import LogisticRegression
cols = ["Age","Fare","Alone","Pclass_2","Pclass_2","Embarked_Q","Embarked_S","Sex_male"] 
X = training[cols]
y = training['Survived']
# Build a logreg and compute the feature importances
model = LogisticRegression()
# create the RFE model and select 8 attributes
model.fit(X,y)


# In[ ]:


from sklearn.metrics import accuracy_score
train_predicted = model.predict(X)
accuracy_score(train_predicted, y)


# In[ ]:


test = pd.read_csv('../input/titanic/test.csv')


# In[ ]:


test.isnull().sum()


# In[ ]:


test.drop(['PassengerId','Name','Cabin','Ticket'], axis=1, inplace=True)
test["Age"].fillna(28, inplace=True)
test["Embarked"].fillna(test['Embarked'].value_counts().idxmax(), inplace=True)
test["Fare"].fillna(train.Fare.median(), inplace=True)
test['Alone']=np.where((test["SibSp"]+test["Parch"])>0, 0, 1)
test.drop(['SibSp', 'Parch'], axis=1, inplace=True)
testing=pd.get_dummies(test, columns=["Pclass","Embarked","Sex"], drop_first=True)
print(testing.dtypes)
test_copied = testing.copy()
test_std = train_standard.transform(test_copied[['Age','Fare']])
test_std
testing[['Age','Fare']] = test_std
testing


# In[ ]:


cols = ["Age","Fare","Alone","Pclass_2","Pclass_2","Embarked_Q","Embarked_S","Sex_male"] 
X_test=testing[cols]
print(X_test.dtypes)
test_predicted = model.predict(X_test)


# In[ ]:


sub = pd.read_csv('../input/titanic/gender_submission.csv')


# In[ ]:


sub['Survived'] = list(map(int, test_predicted))
sub.to_csv('submission.csv', index=False)


# In[ ]:




