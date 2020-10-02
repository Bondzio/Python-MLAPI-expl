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


# In[ ]:


# Load the training data
train_data = pd.read_csv("../input/train.csv", low_memory = False)


# In[ ]:


# Question 1. What percentage of your training set loans are in default??
train_data.default.mean() # calculate percentage of loans in default


# In[ ]:


# Question 2. Which ZIP code has the highest default rate?

train_data.groupby(by = 'ZIP')['default'].sum() / train_data.groupby(by = 'ZIP')['default'].count() # calculate the default rate by zip code 
#MT04PA has the highest default rate


# In[ ]:


# Question 3. What is the default rate in the first year for which you have data?

train_data.default[train_data.year==0].mean() # calculate the default rate for year 0


# In[ ]:


# Question 4. What is the correlation between age and income? 

train_data['age'].corr(train_data['income']) # determine correlation between age and income


# In[ ]:


# 5. What is the in-sample accuracy? That is, find the accuracy score of the fitted model for predicting the outcomes using the whole training dataset?

# create the X_train matrix. Select the variables to test and convert the categorical variables into dummy variables
X_train = pd.get_dummies(train_data[['loan_size','payment_timing','education','income','job_stability','rent','occupation','ZIP']])

# create the y_train column
y_train = train_data.default


# In[ ]:


# import the Random Forrest Classifier
from sklearn.ensemble import RandomForestClassifier

# Train the Random Forrest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42, oob_score=True, n_jobs=-1)
clf.fit(X_train, y_train)


# In[ ]:


# define y_predict as the predicted values generated by the classifier
y_predict = clf.predict(X_train)

# Import sklearn metrics
from sklearn import metrics

# Calculate and print sample accuracy 
print("Accuracy:", metrics.accuracy_score(y_train, y_predict))


# In[ ]:


# Question 6. What is the out of bag score for the model? 

print(clf.oob_score_)


# In[ ]:


# 7. What is the out of sample accuracy? That is, find the accuracy score of the model using the test data without re-estimating the model parameters.?

# import the test data
test_data = pd.read_csv("../input/test.csv", low_memory = False)

# create the X_test matrix. Select the variables to test and convert the categorical variables into dummy variables
X_test = pd.get_dummies(test_data[['loan_size','payment_timing','education','income','job_stability','rent','occupation','ZIP']])

# create the y_test matrix.
y_test = test_data.default


# In[ ]:


# define y_predict_test_data as the predicted values generated by the classifier
y_predict_test = clf.predict(X_test)

# Calculate and print sample accuracy 
print("Accuracy:", metrics.accuracy_score(y_test, y_predict_test))


# In[ ]:


# Question 8. What is the predicted average default probability for all non-minority members in the test set?
# Question 9. What is the predicted average default probability for all minority members in the test set?


# add the predictions back into the data set
test_data['prediction'] = y_predict_test

# calculate default probability by minority status
test_data.groupby(['minority']).mean().prediction


# In[ ]:


# Question 10. Is the loan granting scheme (the cutoff, not the model) group unaware?

# Yes, the loan granting scheme applies a single cutoff for all people i.e. is their probability of repayment 50%


# In[ ]:


# Question 11. Has the loan granting scheme achieved demographic parity? Compare the share of approved female applicants to the share of rejected female applicants. Do the same for minority applicants. Are the shares roughly similar between approved and rejected applicants? What does this indicate about the demographic parity achieved by the model?

# Calcualte the percentage of approved applicants by gender
print((1-test_data.groupby(['sex']).mean().prediction))

# Calcualte the percentage of approved applicants by minority
print((1-test_data.groupby(['minority']).mean().prediction))

# The model does not achieve full demographic parity. The share of approved females is similar to the share of approved males. However, the share of approved minorities is less than the share of approved non-minorities.


# In[ ]:


# Question 12. Is the loan granting scheme equal opportunity? Compare the share of successful non-minority applicants that defaulted to the share of successful minority applicants that defaulted. Do the same comparison of the share of successful female applicants that default versus successful male applicants that default. What do these shares indicate about the likelihood of default in different population groups that secured loans?

print(test_data.groupby(['minority','prediction']).mean().default)

print(test_data.groupby(['sex','prediction']).mean().default)

# The loan does not grant equal opportunity. 11% of approved minority's default, whilst 14% of approved non-minorities default. However, the gap is a lot closer for gender. 

