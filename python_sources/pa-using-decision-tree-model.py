#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importing libraries
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from sklearn import linear_model
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score


# In[ ]:


# Importing data set into pima dataframe:
pima = pd.read_csv("../input/diabetes.csv")


# In[ ]:


# Checking Available columns
pima.columns


# Here we will be presenting missing data in terms of "Total" missing values and "Percent" of missing values.

# In[ ]:


# Calculating total NULL values (in descending order)
total = pima.isnull().sum().sort_values(ascending=False)

# Calculating percentage of NULL values(total/count * 100) (in descending order)
percent = ((pima.isnull().sum()/pima.isnull().sum().count())*100).sort_values(ascending=False)

missing_data = pd.concat([total,percent],axis = 1, keys=['Total','Percent'])
missing_data


# Finding Dependent and Independent Variables

# In[ ]:


# Correlation matrix
pima.corr()


# From above correlation matrix we can see maximum correlation of column 'outcome' is with 'Insulin' and 'BMI'

# Building Decision Tree Model

# In[ ]:


# Seperating variables:
y = pima[['Outcome']]
x = pima[['Glucose','BMI','Age','Pregnancies']]


# In[ ]:


# Creating training and test data sets
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.20,random_state=0)

# Check shape of data sets
x_train.shape,y_train.shape,x_test.shape,y_test.shape


# In[ ]:


# Creating Instnce/Object of Decision Tree class
pima_DTree = DecisionTreeClassifier()

# Fitting our model:
pima_DTree.fit(x_train,y_train)


# In[ ]:


# Predicting Values
pima_predict = pima_DTree.predict(x_test)

# Checking first five values
pima_predict[:5]


# In[ ]:


# Checking Accuracy score
accuracy_score(y_test,pima_predict)

