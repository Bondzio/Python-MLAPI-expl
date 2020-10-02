#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# ## Load Data

# In[ ]:


train_df = pd.read_csv('/kaggle/input/novartis-data/Train.csv')
train_df.head()


# In[ ]:


test_df = pd.read_csv('/kaggle/input/novartis-data/Test.csv')
test_df.head()


# ## Analysis

# #### Hackerearth did not have much info about the features in general but it is stated that the features X1 to X15 are anonymized logging parameters. The date and incident id are part of the logging process & i will at this point leave out the possibilty that date may give us a pattern and rather rely on the meta data provided by the other features to show a pattern. Target values are 1 or 0, so let us solve the classification problem.

# In[ ]:


train_df.describe()


# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[ ]:


correlations = train_df.corr()

fig, ax = plt.subplots(figsize=(10,10))
sns.heatmap(correlations, vmax=1.0, center=0, fmt='.2f', square=True, linewidths=.5, annot=True, cbar_kws={"shrink": .70})
plt.show();


# ### The matrix above shows that the corelation between variables are not creating issue of multi-collinearity.

# ## Train data cleaning

# In[ ]:


# dropping date & Incident Id as they are randomly assigned data. As per the problem statement the anonymous logs are
# the ones containing the pattern.

X = train_df.drop(['INCIDENT_ID', 'DATE'], axis=1)


# In[ ]:


X.isnull().sum()


# In[ ]:


# Since the missing values in X_12 are less than 1% of the whole package, we will go ahead and drop null values.
X.dropna(inplace=True)
X.isnull().sum()


# In[ ]:


y = X['MULTIPLE_OFFENSE']
X = X.drop(['MULTIPLE_OFFENSE'], axis=1)


# ## Test data cleaning

# In[ ]:


test_df.isnull().sum()


# In[ ]:


# We will go ahead and delete the two rows.
# mean fill the "Missing at random" values
test_df.fillna(train_df['X_12'].mean(), inplace=True)
n_test_df = test_df.drop(['INCIDENT_ID', 'DATE'], axis=1)
n_test_df.isnull().sum()


# ## Model Training

# ### For model selection we will generate cross-val-score for linear, SVC and tree based model. Our model selction would be based on accuracy. Also K-fold cross validation will reduce the overfitting danger.

# In[ ]:


from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

# train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# ### Calculating cross val score on some well known variants of classifiers.

# In[ ]:


print("Logistic Regression : ", cross_val_score(LogisticRegression(max_iter=1000), X_train, y_train, cv=10, scoring='accuracy').mean())
print("Support Vector : ", cross_val_score(SVC(), X_train, y_train, cv=10, scoring='accuracy').mean())
print("Naive : ", cross_val_score(GaussianNB(), X_train, y_train, cv=10, scoring='accuracy').mean())
print("K Neighbours : ", cross_val_score(KNeighborsClassifier(), X_train, y_train, cv=10, scoring='accuracy').mean())
print("Random Forest : ", cross_val_score(RandomForestClassifier(), X_train, y_train, cv=10, scoring='accuracy').mean())


# ### Model of choice - Random Forest. Let's now do some hyperparameter tuning before final submission.

# In[ ]:


#Since cross val score proved that the forest will be a perfect fot the data, will go ahead and train the data on the same.

from sklearn.model_selection import RandomizedSearchCV

n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
max_features = ['auto', 'sqrt']
max_depth = [3, 5, 7, 11, 21, None]
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
bootstrap = [True, False]

params = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}
model = RandomForestClassifier()
model_cv = RandomizedSearchCV(model, params, cv=10)
model_cv.fit(X_train, y_train)

print(model_cv.best_params_)
print(model_cv.best_score_)


# In[ ]:


prediction = model_cv.predict(n_test_df)

output = pd.DataFrame({'INCIDENT_ID': test_df.INCIDENT_ID, 'MULTIPLE_OFFENSE': prediction})
output.to_csv('my_submission.csv', index=False)

