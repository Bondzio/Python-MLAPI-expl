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


# Let's read in the data and look at its shape:

# In[ ]:


data = pd.read_csv('../input/train.csv')
data.head()


# Useful packages

# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# In[ ]:


y = data['label']
X = data.drop(['label'], axis = 1)


# Making a test set to make sure the model works well and finally we test the model with a few different number of estimators to find the best choice.

# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)
#cross validating for number of estimators
Ns = [50, 100, 150, 200, 250, 300]; Accuracies = []
for n in Ns:
    clf = RandomForestClassifier(n_estimators = n)
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    Accuracies.append(score)
    print('\r Accuracy:{}'.format(score), end = "")
Max_score = max(Accuracies)
Best_N = Ns[Accuracies.index(Max_score)]
print( '\n Best Score:', Max_score, Best_N )


# Now we use the parameter that gave us the best accuracy to retrain our model.

# In[ ]:


clf = RandomForestClassifier(n_estimators = Best_N)
clf.fit(X, y)


# Reading in the test set and applying the model on it:

# In[ ]:


test_data = pd.read_csv('../input/test.csv')
test_data.head()


# In[ ]:


prediction = clf.predict(test_data)
print (prediction)
ImageID = range(1, len(prediction)+1)
output = {'ImageId': ImageID, 'Label': prediction}
Output = pd.DataFrame.from_dict(output)
Output.set_index('ImageId', inplace = True)
print (Output.head())
Output.to_csv('./Submission.csv')


# In[ ]:




