#!/usr/bin/env python
# coding: utf-8

# A Quick comparision of different Classifiers applied on the popular Bank_loan_Classification dataset

# # **Import Libraries**

# In[1]:


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


# In[2]:


import numpy as np    # For array operations
import pandas as pd   # For DataFrames
import matplotlib.pyplot as plt    # For plotting
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix,mean_squared_error,accuracy_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split


# # EDA

# **Read the Dataset**

# In[3]:


unibank = pd.read_csv('../input/bank-loan-classification/UniversalBank.csv')
unibank.head()


# Data types

# In[4]:


## Check the datatype of each variable
unibank.dtypes


# Dropping Unneccesary columns 

# In[5]:


## Drop columns which are not significant
unibank.drop(["ID","ZIP Code"],axis=1,inplace=True)


# Converting Categorical Columns to Dummies

# In[6]:


## Convert Categorical Columns to Dummies
cat_cols = ["Family","Education","Personal Loan","Securities Account","CD Account","Online","CreditCard"]
unibank = pd.get_dummies(unibank,columns=cat_cols,drop_first=True,)


# Train-Test Split

# In[7]:


## Split the data into X and y
X = unibank.copy().drop("Personal Loan_1",axis=1)
y = unibank["Personal Loan_1"]

## Split the data into trainx, testx, trainy, testy with test_size = 0.20 using sklearn
trainx, testx, trainy, testy = train_test_split(X, y, test_size=0.20)

## Print the shape of X_train, X_test, y_train, y_test
print(trainx.shape)
print(testx.shape)
print(trainy.shape)
print(testy.shape)


# # Scaling Numeric features

# In[9]:


from sklearn.preprocessing import StandardScaler

## Scale the numeric attributes
scaler = StandardScaler()
scaler.fit(trainx.iloc[:,:5])

trainx.iloc[:,:5] = scaler.transform(trainx.iloc[:,:5])
testx.iloc[:,:5] = scaler.transform(testx.iloc[:,:5])


# # Logistic Regression

# In[10]:


# Logistic Regression
X = trainx
y = trainy
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score 
model = LogisticRegression()
model.fit(X , y)
predicted_classes = model.predict(X)
accuracy = accuracy_score(y,predicted_classes)
parameters = model.coef_


# In[11]:


print(accuracy)
print(parameters)
print(model)


# In[12]:


model.fit(testx , testy)
predicted_classes_test = model.predict(testx)
accuracy = accuracy_score(testy,predicted_classes_test)
print(accuracy)


# # Naive Bayes 

# In[54]:


from sklearn.naive_bayes import GaussianNB

NB = GaussianNB()

NB.fit(X , y)

NB_train_pred = NB.predict(X)
print(accuracy_score(y,NB_train_pred))

NB_test_pred = NB.predict(testx)
print(accuracy_score(testy,NB_test_pred))


# # KNN Classifier

# In[13]:


knn_classifier = KNeighborsClassifier(algorithm='brute',weights='distance')
params = {'n_neighbors':[1,11,25],'metric':["euclidean",'cityblock']}
grid = GridSearchCV(knn_classifier,param_grid=params,scoring='accuracy',cv=10)


# In[14]:


grid.fit(trainx,trainy)
print(grid.best_score_)
print(grid.best_params_)


# In[15]:


best_knn = grid.best_estimator_
pred_train = best_knn.predict(trainx) 
pred_test = best_knn.predict(testx)
print("Accuracy on train is:",accuracy_score(trainy,pred_train))
print("Accuracy on test is:",accuracy_score(testy,pred_test))


# # Decision Tree

# In[16]:


from sklearn import tree
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.model_selection import GridSearchCV
# Defining the model
# Fit / train the model
dtc = tree.DecisionTreeClassifier()
dtc.fit(trainx,trainy)


# In[17]:


# Get the prediction for both train and test
pred_train = dtc.predict(trainx)
pred_test = dtc.predict(testx)
# Measure the accuracy of the model for both train and test sets
print("Accuracy on train is:",accuracy_score(trainy,pred_train))
print("Accuracy on test is:",accuracy_score(testy,pred_test))


# In[19]:


# Max_depth = 3

dtc_2 = tree.DecisionTreeClassifier(max_depth=3)
dtc_2.fit(trainx,trainy)

pred_train2 = dtc_2.predict(trainx)
pred_test2 = dtc_2.predict(testx)

print("Accuracy on train is:",accuracy_score(trainy,pred_train2))
print("Accuracy on test is:",accuracy_score(testy,pred_test2))


# # SVM

# In[20]:


from sklearn.svm import SVC

## Create an SVC object and print it to see the default arguments
svc = SVC()
print(svc)


# In[21]:


## Fit
svc.fit(trainx,trainy)

## Predict
train_predictions = svc.predict(trainx)
test_predictions = svc.predict(testx)


# In[22]:


### Train data accuracy
from sklearn.metrics import accuracy_score
print(accuracy_score(trainy,train_predictions))
      
### Test data accuracy
print(accuracy_score(testy,test_predictions))


# Search Grid for Hyper paramenter tuning

# In[23]:


from sklearn.model_selection import GridSearchCV

svc_grid = SVC()
 

param_grid = {

'C': [0.001, 0.01, 0.1, 1, 10],
'gamma': [0.001, 0.01, 0.1, 1], 
'kernel':['linear','rbf']}

 
svc_cv_grid = GridSearchCV(estimator = svc_grid, param_grid = param_grid, cv = 10)


# In[24]:


svc_cv_grid.fit(X = trainx, y = trainy)
print(svc_cv_grid.best_score_,svc_cv_grid.best_params_)


# In[27]:


best_svc = svc_cv_grid.best_estimator_
pred_train = best_svc.predict(trainx) 
pred_test = best_svc.predict(testx)
print("Accuracy on train is:",accuracy_score(trainy,pred_train))
print("Accuracy on test is:",accuracy_score(testy,pred_test))


# In[49]:


print(roc_auc_score(trainy, pred_train))
print(roc_auc_score(testy, pred_test))


# # Random Forest

# In[28]:


from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier()
print(rfc)


# In[29]:


rfc.fit(trainx,trainy)
## Predict
rfc_train_predictions = rfc.predict(trainx)
rfc_test_predictions = rfc.predict(testx)

### Train data accuracy
from sklearn.metrics import accuracy_score
print(accuracy_score(trainy,rfc_train_predictions))
      
### Test data accuracy
print(accuracy_score(testy,rfc_test_predictions))


# Search Grid for Hyper paramenter tuning

# In[30]:


from sklearn.model_selection import RandomizedSearchCV

## n_jobs = -1 uses all cores of processor
## max_features is the maximum number of attributes to select for each tree
rfc_grid = RandomForestClassifier(n_jobs=-1, max_features='sqrt', class_weight='balanced_subsample')
 
# Use a grid over parameters of interest
## n_estimators is the number of trees in the forest
## max_depth is how deep each tree can be
## min_sample_leaf is the minimum samples required in each leaf node for the root node to split
## "A node will only be split if in each of it's leaf nodes there should be min_sample_leaf"
 
param_grid = {"n_estimators" : [10, 25, 50, 75, 100],
           "max_depth" : [10, 12, 14, 16, 18, 20],
           "min_samples_leaf" : [5, 10, 15, 20]}
 
rfc_cv_grid = RandomizedSearchCV(estimator = rfc_grid, param_distributions = param_grid, cv = 3, n_iter=10)
rfc_cv_grid.fit(trainx, trainy)
rfc_cv_grid.best_estimator_


# In[31]:


## Predict
rfc2_train_predictions = rfc_cv_grid.predict(trainx)
rfc2_test_predictions = rfc_cv_grid.predict(testx)

print(accuracy_score(trainy,rfc2_train_predictions))
      
### Test data accuracy
print(accuracy_score(testy,rfc2_test_predictions))


# # AdaBoost Classifier

# In[32]:


# import modules as necessary
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier


# In[33]:


# Create adaboost-decision tree classifer object
Adaboost_model = AdaBoostClassifier(
    DecisionTreeClassifier(max_depth=2),
    n_estimators = 600,
    learning_rate = 1)


# In[34]:


# Train model
get_ipython().run_line_magic('time', 'Adaboost_model.fit(trainx, trainy)')


# In[35]:


# Predict on Train 
train_preds = Adaboost_model.predict(trainx)
# Predict on Test 
test_preds = Adaboost_model.predict(testx)


# In[36]:


print(accuracy_score(trainy, train_preds))
print(accuracy_score(testy, test_preds))


# Search Grid for Hyper paramenter tuning

# In[37]:


from sklearn.model_selection import GridSearchCV

param_grid = {'n_estimators' : [100, 150, 200],
              'learning_rate' : [0.1, 0.5, 0.9]}

Adaboost_model_clf = GridSearchCV(AdaBoostClassifier(
            DecisionTreeClassifier(max_depth=2)), param_grid, n_jobs=-1)


# In[38]:


# Train model
get_ipython().run_line_magic('time', 'Adaboost_model_clf.fit(trainx, trainy)')


# In[39]:


# Find best model
best_ada_model = Adaboost_model_clf.best_estimator_
print (Adaboost_model_clf.best_score_, Adaboost_model_clf.best_params_) 


# In[40]:


# Predict on Train 
train_preds2 = best_ada_model.predict(trainx)
# Predict on Test 
test_preds2 = best_ada_model.predict(testx)

print(accuracy_score(trainy, train_preds2))
print(accuracy_score(testy, test_preds2))


# # Gradient Boosting

# In[41]:


from sklearn.ensemble import GradientBoostingClassifier
GBM_model = GradientBoostingClassifier(n_estimators=50,
                                       learning_rate=0.3,
                                       subsample=0.8)

get_ipython().run_line_magic('time', 'GBM_model.fit(X=trainx, y=trainy)')


# In[42]:


gtrain_pred = GBM_model.predict(trainx)
gtest_pred = GBM_model.predict(testx)

print(accuracy_score(trainy, gtrain_pred))
print(accuracy_score(testy, gtest_pred))


# Search Grid for Hyper paramenter tuning

# In[43]:


# Model in use
GBM = GradientBoostingClassifier() 
 
# Use a grid over parameters of interest
param_grid = { 
           "n_estimators" : [100,150,200,250],
           "max_depth" : [5, 10],
           "learning_rate" : [0.1,0.5,0.9]}
 
CV_GBM = GridSearchCV(estimator=GBM, param_grid=param_grid, cv= 10)


# In[44]:


get_ipython().run_line_magic('time', 'CV_GBM.fit(X=trainx, y=trainy)')


# In[45]:


# Find best model
best_gbm_model = CV_GBM.best_estimator_
print (CV_GBM.best_score_, CV_GBM.best_params_)


# In[46]:


g2train_pred = GBM_model.predict(trainx)
g2test_pred = GBM_model.predict(testx)

print(accuracy_score(trainy, g2train_pred))
print(accuracy_score(testy, g2test_pred))


# AUC Scores

# In[48]:



from sklearn.metrics import roc_auc_score
print(roc_auc_score(trainy, g2train_pred))
print(roc_auc_score(testy, g2test_pred))


# # Cat Boost

# In[64]:


#importing library and building model
from catboost import CatBoostClassifier
catmodel=CatBoostClassifier(iterations=50, depth=12, learning_rate=0.1,)
catmodel.fit(X,y,plot=True)


# In[65]:


cat_train_pred = catmodel.predict(X)
cat_test_pred = catmodel.predict(testx)

print(accuracy_score(trainy, cat_train_pred))
print(accuracy_score(testy, cat_test_pred))


# # Comparison

# A quick Comparision of Accuracy metrics for each of the models

# 
# ![image.png](attachment:image.png)
