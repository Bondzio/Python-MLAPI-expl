#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


travel = pd.read_csv("../input/travel insurance.csv", delimiter=",")
travel.head()


# Checking for Null values (can see some in Gender)

# In[ ]:


print(travel['Gender'].value_counts())

print(travel.isnull().any())

print(travel['Gender'].isnull().sum())


# In[ ]:


travel = travel.dropna()

# check again...

print(travel['Gender'].any() == np.nan)


# Checking the data in the 'Age' column

# In[ ]:


travel['Age'].describe()

# Drop the max age of 118 since there is no one on Earth that old...


# In[ ]:


travel = travel[travel.Age != 118]


# Checking the data in the 'Duration' column

# In[ ]:


travel['Duration'].describe()
# will remove the instance of 0 Duration


# In[ ]:


travel = travel[travel.Duration != 0]


# ### Some Visualizations... ###

# In[ ]:


print(travel['Duration'].any() == 0)

## What about the number of claims approved, and/or what can we say about our target variable?

travel['Claim'].value_counts()


# In[ ]:


import seaborn as sns

bins = np.linspace(travel.Duration.min(), travel.Duration.max(), 10)
g = sns.FacetGrid(travel, col="Gender", hue="Claim", palette="Set2", col_wrap=2)
g.map(plt.hist, 'Duration', bins=bins, ec="k")

g.axes[-1].legend()
plt.show()


# In[ ]:


bins = np.linspace(travel.Age.min(), travel.Age.max(),10)
g = sns.FacetGrid(travel, col='Gender',hue='Claim', palette='Set2', col_wrap=2)
g.map(plt.hist, 'Age', bins=bins, ec='k')

g.axes[-1].legend()
plt.show()


# ### Pre-Processing ###

# In[ ]:


travel.groupby(['Gender'])['Claim'].value_counts(normalize=True)
travel['Gender'].replace(to_replace=['F','M'], value=[0,1],inplace=True)


# In[ ]:


Feature = travel[['Duration', 'Distribution Channel', 'Net Sales',  'Age', 'Gender']]
Feature = pd.concat([Feature,pd.get_dummies(travel['Distribution Channel'])], axis=1)


# In[ ]:


Feature.head()


# In[ ]:


X = Feature[['Duration', 'Net Sales', 'Age', 'Gender', 'Offline','Online']]


# In[ ]:


X.head()


# In[ ]:


y = travel['Claim']
y = travel['Claim'].replace(to_replace=['Yes','No'], value=[0,1]).values
y[0:5]


# In[ ]:


# now use train/split to split data
from sklearn.model_selection import train_test_split

X_trainset, X_testset, y_trainset, y_testset = train_test_split(X, y, test_size=0.3, random_state=3)


# In[ ]:


print(X_trainset.shape)
print(y_trainset.shape)

print(X_testset.shape)
print(y_testset.shape)


# In[ ]:


from sklearn import preprocessing
X = preprocessing.StandardScaler().fit(X).transform(X)
X[0:5]


# In[ ]:


from sklearn.linear_model import LogisticRegression

LR = LogisticRegression(C=0.01, solver='liblinear').fit(X_trainset,y_trainset)
yhat=LR.predict(X_trainset)
y_proba=LR.predict_proba(X_trainset)


# In[ ]:


from sklearn.metrics import jaccard_similarity_score

print(jaccard_similarity_score(y_trainset, yhat))


# In[ ]:




