#!/usr/bin/env python
# coding: utf-8

# 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# 

# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


train_data = pd.read_csv("/kaggle/input/train.csv")
train_data.head()


# In[ ]:


test_data = pd.read_csv("/kaggle/input/test.csv")
test_data.head()


# In[ ]:


women = train_data.loc[train_data['Sex'] == 'female']['Survived']
rate_women = sum(women)/len(women)
print ("% of women who survived: ", rate_women)


# In[ ]:


men = train_data.loc[train_data['Sex'] == 'male']['Survived']
rate_men = sum(men)/len(men)
print("% of men who survived: ", rate_men)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier

y = train_data['Survived']                             # define y-axis (labels)

features = ['Pclass','Sex','SibSp','Parch'] 
X = pd.get_dummies(train_data[features])               # define x-axis (features) for training data
X_test = pd.get_dummies(test_data[features])           # define x-axis (features) for test data

model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)  # pick a model
model.fit(X,y)                                         # train the model
predictions = model.predict(X_test)                    # test the model

output = pd.DataFrame({'PassengerId': test_data.PassengerId, 'Survived': predictions})
output.to_csv('my_submission.csv',index=False)
print("Your submission was successfully saved!")


# In[ ]:




