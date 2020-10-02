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


import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt

from pandas.plotting import scatter_matrix
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib


# Dataset information:
# 
# This dataset is originally from the National Institute of Diabetes and Digestive and Kidney Diseases. Several constraints were placed on the selection of these instances from a larger database. In particular, all patients here are females at least 21 years old of Pima Indian heritage.
# 
# Pregnancies: Number of times pregnant
# 
# Glucose: Plasma glucose concentration a 2 hours in an oral glucose tolerance test
# 
# BloodPressure: Diastolic blood pressure (mm Hg)
# 
# SkinThickness: Triceps skin fold thickness (mm)
# 
# Insulin: 2-Hour serum insulin (mu U/ml)
# 
# BMI: Body mass index (weight in kg/(height in m)^2)
# 
# DiabetesPedigreeFunction: Diabetes pedigree function
# 
# Age: Age (years)
# 
# Outcome: Class variable (0 or 1)

# In[ ]:


ds = pd.read_csv("../input/pima-indians-diabetes-database/diabetes.csv")
ds.head()


# In[ ]:


ds.info()


# In[ ]:


ds.hist(figsize=(11,10))
plt.show()


# In[ ]:


array = ds.values
X = array[:,0:8]
Y = array[:,8]
validation_size = 0.20
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size = validation_size, random_state = 0)


# In[ ]:


scoring = 'accuracy'

model = LogisticRegression()

kfold = model_selection.KFold(n_splits=10, random_state = 0)
cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
    
msg = "%s: %f (%f)" % ("LR", cv_results.mean(), cv_results.std())
print(msg)


# In[ ]:


model.fit(X_train, Y_train)
predictions = model.predict(X_validation)

print("LR Accuracy:", accuracy_score(Y_validation, predictions))

print(classification_report(Y_validation, predictions))
print ("ROC:", roc_auc_score(Y_validation, predictions))

fpr, tpr, thresholds = roc_curve(Y_validation, predictions)

plt.plot([0, 1], [0, 1], linestyle='--')

plt.plot(fpr, tpr, marker='.')

plt.show()


# In[ ]:




