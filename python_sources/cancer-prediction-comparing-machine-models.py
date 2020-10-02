#!/usr/bin/env python
# coding: utf-8

#  # Cancer prediction | Comparing machine models

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
import json   
from pandas.io.json import json_normalize  
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier , GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier , GradientBoostingClassifier


# ## About this dataset
# 
# Features are computed from a digitized image of a fine needle aspirate (FNA) of a breast mass. They describe characteristics of the cell nuclei present in the image. n the 3-dimensional space is that described in: [K. P. Bennett and O. L. Mangasarian: "Robust Linear Programming Discrimination of Two Linearly Inseparable Sets", Optimization Methods and Software 1, 1992, 23-34].
# 
# This database is also available through the UW CS ftp server: ftp ftp.cs.wisc.edu cd math-prog/cpo-dataset/machine-learn/WDBC/

# In[ ]:


import pandas as pd 

local = '../input/breast-cancer-wisconsin-data/data.csv'
df = pd.read_csv(local, encoding='latin-1', index_col=0)

df.head(10)


# ## Preparing the data

# In[ ]:


df.shape
pd.isnull(df).sum() > 0


# In[ ]:


df = df.drop(['Unnamed: 32'], axis=1)
df.head(10)


# In[ ]:


#my_plot = df.plot("diagnosis", "radius_mean", kind="scatter")


# In[ ]:


#my_plot = df.plot("diagnosis", "perimeter_mean", kind="scatter")


# In[ ]:


df.hist(figsize=(20, 20), color='green')
plt.plot()


# In[ ]:


pd.isnull(df).sum() > 0


# ## Categorization

# In[ ]:


dfX = df.as_matrix(df.columns[2:])
dfY = df.as_matrix(['diagnosis'])


# In[ ]:


df['diagnosis'] = df.diagnosis.astype("category").cat.codes
df.head(10)


# ## Training machine learning models

# In[ ]:


print('Length X:', dfX.shape)
print('Length Y:', dfY.shape)


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(dfX, dfY, test_size=0.20)


# In[ ]:


def KNN(neighbors, X, y):
    model_KNN = KNeighborsClassifier(n_neighbors = 3)
    model_KNN.fit(X , y)
    
    return model_KNN

np.random.seed(1000)
KNN_predict = KNN(4, X_train, y_train)


# In[ ]:


def machine_learning_algorithms(train_X, train_y):   
    n = 4
    estimador = 100
    
    model_SVC = SVC()
    model_SVC.fit(train_X , train_y)

    model_GBC = GradientBoostingClassifier()
    model_GBC.fit(train_X , train_y)
    
    model_KNN = KNeighborsClassifier(n_neighbors = n)
    model_KNN.fit(train_X , train_y)
    

    return [model_SVC,
            model_GBC,
            model_KNN]
    

np.random.seed(1000)
algoritms = machine_learning_algorithms(X_train, y_train)


# In[ ]:


score = []
total = []
classifier = ['SVG', 'GBC','KNN']

for index, name in enumerate(classifier):
    score_train = algoritms[index].score(X_train, y_train) * 100
    score_tests = algoritms[index].score(X_test, y_test) * 100
    
    total.append([name, score_train, score_tests])
    
df_result = pd.DataFrame(total, columns = ['Model', 'Train score', 'Test score'])
print(df_result)


# In[ ]:


ax = df_result.plot.bar(x='Model', y='Train score')
ax.set_ylabel("Score")


# In[ ]:


ax = df_result.plot.bar(x='Model', y='Test score')
ax.set_ylabel("Score")

