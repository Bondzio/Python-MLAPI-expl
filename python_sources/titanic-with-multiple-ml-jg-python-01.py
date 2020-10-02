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


# **Load the Training Data**

# In[ ]:


train_data = pd.read_csv("/kaggle/input/titanic/train.csv")
train_data.head()


# **Load the Training Data**

# In[ ]:


test_data = pd.read_csv("/kaggle/input/titanic/test.csv")
test_data.head()


# **Explore a pattern - Assumsions that all female passengers survived (and all male passengers died).**

# In[ ]:


women = train_data.loc[train_data.Sex == 'female']['Survived']
rate_women = sum(women)/len(women)

print('% of women who survived: ', rate_women)


# In[ ]:


men = train_data.loc[train_data.Sex == 'male']['Survived']
rate_men = sum(men)/len(men)

print('% of men who survived: ', rate_men)


# USE RANDOM FOREST MODEL

# In[ ]:


from sklearn.ensemble import RandomForestClassifier

# Get the predictor variable (Y)
y = train_data["Survived"]

# Consider the features to be included in the model and get the feature variables (X)
features = ["Pclass", "Sex", "SibSp", "Parch"]
X = pd.get_dummies(train_data[features])
X_test = pd.get_dummies(test_data[features])

# Create the model
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
model.fit(X, y)

# Perform the prediction
predictions = model.predict(X_test)

# Create a output CVS file for submission
output = pd.DataFrame({'PassengerId': test_data.PassengerId, 'Survived': predictions})
output.to_csv('jg_submission.csv', index=False)
print("Your submission was successfully saved!")

