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


# In[ ]:


test = pd.read_csv('/kaggle/input/digit-recognizer/test.csv')
train = pd.read_csv('/kaggle/input/digit-recognizer/train.csv')
sample = pd.read_csv('/kaggle/input/digit-recognizer/sample_submission.csv')


# In[ ]:


test


# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from warnings import filterwarnings
filterwarnings("ignore")


# In[ ]:


y = train.label
X = train.drop('label', 1)


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 200)
model = BaggingClassifier(RandomForestClassifier(), 20, 0.5, 0.3)
model.fit(X_train, y_train)
accuracy_score(y_test, model.predict(X_test))


# In[ ]:


predictions = model.predict(X_test)


# In[ ]:


result = pd.DataFrame({'ImageId': X_test.index, 'Label': predictions})
result


# In[ ]:


model = BaggingClassifier(RandomForestClassifier(), 20, 0.5, 0.3)
model.fit(X, y)
predictions = model.predict(test)
predictions


# In[ ]:


result = pd.DataFrame({'ImageId': (test.index+1), 'Label': predictions})
result
result.to_csv('prediction.csv', index=False)


# In[ ]:


result

