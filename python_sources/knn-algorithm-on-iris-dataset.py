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


df = pd.read_csv("../input/iris/Iris.csv")
X = df.iloc[:, 1:5]
y = df.iloc[:, 5]
X.head()


# In[ ]:


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3, random_state=0)
print('Number of samples in the training set is: {}'.format(X_train.shape))
print('Number of samples in the test set is: {}'.format(X_test.shape))


# In[ ]:


# KNN algorithm 
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=4, p=2, metric='minkowski', algorithm='auto')
knn.fit(X_train, y_train)
print('Accuracy on training data: {:.2f}'.format(knn.score(X_train, y_train)))
print('Accuracy on test data: {:.2f}'.format(knn.score(X_test, y_test)))

