#!/usr/bin/env python
# coding: utf-8

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


# ## 1. Import data

# In[ ]:


train  = pd.read_csv('/kaggle/input/train.csv')
test = pd.read_csv('/kaggle/input/test.csv')


# ## 2. Clean NA's

# In[ ]:


print(train.isnull().sum())


# In[ ]:


train['Embarked'] = train['Embarked'].fillna(value = 'S')
train['Age'] = train['Age'].fillna(train['Age'].mean())


# In[ ]:


print(train.isnull().sum())


# In[ ]:


test.isnull().sum()


# In[ ]:


test['Age'] = test['Age'].fillna(test['Age'].mean())
test['Fare'] = test['Fare'].fillna(test['Fare'].mean())


# In[ ]:


test.isnull().sum()


# ## 3. Select vaiables

# In[ ]:


train = train[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked', 'Survived']]
X_test = test[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']]


# In[ ]:


X_train = train[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']]
y_train = train['Survived']


# In[ ]:


X_train.head()


# In[ ]:


X_test.head()


# ## 4. Create vaiables Dummy

# In[ ]:


X_train['Sex'].replace(['female', 'male'], [0,1], inplace = True)
X_train['Embarked'].replace(['Q', 'S', 'C'], [0, 1, 2], inplace = True)
X_train.head()


# In[ ]:


X_test['Sex'].replace(['female', 'male'], [0,1], inplace = True)
X_test['Embarked'].replace(['Q', 'S', 'C'], [0, 1, 2], inplace = True)
X_test.head()


# ## 5. Scale variables for classifier

# In[ ]:


from sklearn.preprocessing import StandardScaler
sc_x = StandardScaler()
X_train = sc_x.fit_transform(X_train)
X_test = sc_x.fit_transform(X_test)


# ## 6. Import models

# In[ ]:


from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import Perceptron
from xgboost import XGBClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import KFold, cross_val_score


# In[ ]:


seed = 0
models = []
models.append(('Decission Tree', DecisionTreeClassifier(random_state = seed)))
models.append(('Random forest', RandomForestClassifier(random_state = seed)))
models.append(('Logistic Regresion', LogisticRegression(random_state = seed)))
models.append(('SVM',SVC(random_state=seed)))
models.append(('KNN',KNeighborsClassifier()))
models.append(('Perceptron',perceptron.Perceptron()))
models.append(('Adaboost',AdaBoostClassifier(random_state=seed)))
models.append(('Naive Bayes',GaussianNB()))
models.append(('XGBoost',XGBClassifier()))


# In[ ]:


from sklearn.metrics import confusion_matrix


# ## 7. Results Models with confusion matrix and R3 of each model

# In[ ]:


for name, model in models:
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)


# In[ ]:


svc = SVC()
svc.fit(X_train, y_train)
y_pred = svc.predict(X_test)


# In[ ]:


y_pred


# In[ ]:


output = pd.DataFrame({
    'PassengerId': test['PassengerId'],
    'Survived': y_pred
})

output.to_csv('submission.csv', index=False)


# In[ ]:


pd.read_csv('submission.csv')


# In[ ]:





# In[ ]:




