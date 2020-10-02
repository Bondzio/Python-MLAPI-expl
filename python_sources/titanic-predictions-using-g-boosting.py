#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# # Read data

# In[ ]:


train = pd.read_csv("../input/titanic/train.csv")
test = pd.read_csv("../input/titanic/test.csv")


# In[ ]:


train.describe()


# In[ ]:


train.head()


# In[ ]:


print(train.columns)


# In[ ]:


print(pd.isnull(train).sum())


# Data shape

# In[ ]:


print('train shape:',train.shape)
print('test shape:',test.shape)


# In[ ]:


# Change type of 'Sex' feature to numeric
sex_num = {"male": 1, "female": 0}
train['Sex'] = train['Sex'].map(sex_num)
test['Sex'] = test['Sex'].map(sex_num)


# In[ ]:


train.head()


# In[ ]:


train = train.drop(['Name','Cabin','Ticket','Age'], axis = 1)


# In[ ]:


train.head()


# In[ ]:


print(pd.isnull(train).sum())


# In[ ]:


train = train.fillna({"Embarked": "S"})


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


print(test.isnull().sum())


# In[ ]:


test = test.drop(['Name'], axis = 1)


# In[ ]:


test = test.drop(['Cabin','Ticket','Age'], axis = 1)


# In[ ]:


test.head()


# In[ ]:


train['Embarked'] = train['Embarked'].map( {'S': 0, 'C': 1, 'Q': 2} ).astype(int)
test['Embarked'] = test['Embarked'].map( {'S': 0, 'C': 1, 'Q': 2} ).astype(int)


# In[ ]:


train.head()


# In[ ]:


print(train.isnull().sum())


# In[ ]:


median_fare = test.groupby(['Pclass','SibSp','Parch'])['Fare'].median()[3][0][0]
test['Fare'] = test['Fare'].fillna(median_fare)


# In[ ]:


print(test.isnull().sum())


# In[ ]:


data=[train,test]
for df in data:
    data_correlation = df.corr().abs()
    plt.figure(figsize=(10, 10))
    sns.heatmap(data_correlation, annot=True,cmap='YlGnBu')
    plt.show()


# In[ ]:


predictors = train.drop(['Survived', 'PassengerId'], axis=1)
target = train["Survived"]
x_train, x_val, y_train, y_val = train_test_split(predictors, target, test_size = 0.469, random_state = 0)


# In[ ]:


gb = GradientBoostingClassifier()
gb.fit(x_train, y_train)
y_pred = gb.predict(x_val)
acc_gb = round(accuracy_score(y_pred, y_val) * 100, 2)
print('The accuracy value',acc_gb)


# In[ ]:


submit = pd.DataFrame({'PassengerId':test["PassengerId"],'Survived':y_pred})
x=submit.to_csv('submission.csv')

