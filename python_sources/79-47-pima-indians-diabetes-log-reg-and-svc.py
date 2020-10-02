#!/usr/bin/env python
# coding: utf-8

# # Pima Indians Diabetes Database

# ## Predict the onset of diabetes based on diagnostic measures

# The previous notebook is no longer accessible because I had 2 accounts and I did not know that this was forbidden. So I post this one online.For good advices for people like me who begin in machine learning there is this web site http://machinelearningmastery.com/python-machine-learning-mini-course/ given by Jason Brownlee. If you have any advices or any comments don't hesitate.

# In[ ]:


# Import Libraries
import numpy
import pandas
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from math import *
from sklearn.metrics import classification_report
get_ipython().run_line_magic('matplotlib', 'inline')


# First, load the data and let's look at some informations about the dataset. 

# In[ ]:


# Number of times pregnant
# Plasma glucose concentration
# Diastolic blood pressure
# Triceps skin fold thickness
# 2-Hour serum insulin
# Body mass index
# Diabetes pedigree function
# Age
# Class
rdm_state = 99
data = pandas.read_csv('../input/diabetes.csv')
print(data.shape)
print(data.head())


# In[ ]:


data.info() # We verify the different informations like missing value.


# In[ ]:


data.describe() # Complete description of the data.


# We can see for Glucose, BloodPressure, SkinThickness, Insulin, BMI the minimum is 0 for some fields we will replace them with the mean of the fields not equal to zero. Thank to <a href="https://www.kaggle.com/atulnet">Atul A</a> because it was by looking at his work that I saw this problem. I put the link to access it. <a href="https://www.kaggle.com/atulnet/d/uciml/pima-indians-diabetes-database/pima-diabetes-keras-implementation">Pima Diabetes - Keras implementation</a>

# In[ ]:


fields = ['Glucose','BloodPressure','SkinThickness','Insulin','BMI']
for field in fields :
    print('field %s : num 0-entries: %d' % (field, len(data.loc[ data[field] == 0, field ])))


# In[ ]:


def replace_zero_field(data, field):
    nonzero_vals = data.loc[data[field] != 0, field]
    avg = nonzero_vals.median()
    length = len(data.loc[ data[field] == 0, field])   # num of 0-entries
    data.loc[ data[field] == 0, field ] = avg
    print('Field: %s; fixed %d entries with value: %.3f' % (field,length, avg))

for field in fields :
    replace_zero_field(data,field)
print()
for field in fields :
    print('Field %s : num 0-entries: %d' % (field, len(data.loc[ data[field] == 0, field ])))


# In[ ]:


data.describe()


# Now we convert the data into an array and split it in two. We separate the array into input and output components.

# In[ ]:


data_arr = data.values
X = data_arr[:,0:8]
Y = data_arr[:,8]
print(data_arr.shape)
print(X.shape)
print(Y.shape)


# Then we split the input and output components into train and test data.

# In[ ]:


test_size = 0.25
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=rdm_state)


# Now we search what is the best model for our classification problem.

# In[ ]:


#Model we are testing 
models = []
models.append(('LR', LogisticRegression()))
models.append(('RF',RandomForestClassifier(n_estimators=120, max_features=7)))
models.append(('SVC',svm.SVC(kernel='linear')))
models.append(('QDA',QuadraticDiscriminantAnalysis()))


# In[ ]:


results = []
names = []
scoring = 'accuracy'
for name, model in models:
    kfold = KFold(n_splits=10, random_state=rdm_state)
    cv_results = cross_val_score(model, X_train,Y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    print(name, round(100*cv_results.mean(),2),"%","(+/- ", round(100*cv_results.std(),2),"% )")


# Preprocessing the data and see the effect on the differents models.

# In[ ]:


#Normalize X
normalized_X = preprocessing.normalize(X)
X_train, X_test, Y_train, Y_test = train_test_split(normalized_X, Y, test_size=test_size, random_state=rdm_state)


# In[ ]:


results = []
names = []
for name, model in models:
    kfold = KFold(n_splits=10, random_state=rdm_state)
    cv_results = cross_val_score(model, X_train,Y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    print(name, round(100*cv_results.mean(),2),"%","(+/- ", round(100*cv_results.std(),2),"% )")


# In[ ]:


#Rescale X
standardized_X = preprocessing.scale(X)
X_train, X_test, Y_train, Y_test = train_test_split(standardized_X, Y, test_size=test_size, random_state=rdm_state)


# In[ ]:


results = []
names = []
for name, model in models:
    kfold = KFold(n_splits=10, random_state=rdm_state)
    cv_results = cross_val_score(model, X_train,Y_train, cv=kfold, scoring=scoring)
    results.append(cv_results)
    names.append(name)
    print(name, round(100*cv_results.mean(),2),"%","(+/- ", round(100*cv_results.std(),2),"% )")


# It seems like the SVC and Log Regression performs best. We can now do some parameter optimization, let's see the result for these two models with the train and test data without preprocessing for beginning, then rescale the data.

# In[ ]:


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=rdm_state)

mdl = svm.SVC()

# prepare a range of values to test
param_grid = [
  {'C': [0.99,0.1,1,10], 'kernel': ['linear']}
 ]

grid = GridSearchCV(estimator=mdl, param_grid=param_grid,cv=5,scoring='precision')
grid.fit(X_train, Y_train)
# summarize the results of the grid search
print("Best score SVC : ",round(100*grid.best_score_,2),"%")
print("Best estimator for SVC parameter C : ",grid.best_estimator_.C)

mdl = LogisticRegression()

# prepare a range of values to test
param_grid = [
  {'C': [0.99,0.1,1,10]}
 ]

grid1 = GridSearchCV(estimator=mdl, param_grid=param_grid,cv=5)
grid1.fit(X_train, Y_train)
# summarize the results of the grid search
print("Best score linear regression : ",round(100*grid1.best_score_,2),"%")
print("Best estimator for linear regression parameter C : ",grid.best_estimator_.C)


# ## Results with log regression and SVC : 

# In[ ]:


def cross_valid(model, X_test, y_test, nb_folds):
    fold_size = X_test.shape[0] // nb_folds
    scores = []
    for i in range(nb_folds):
        beg = i * fold_size
        end = (i + 1) * fold_size
        scores.append(model.score(X_test[beg:end],y_test[beg:end]))
    return 'Score : {}% (+/- {}%)'.format(round(numpy.mean(scores)*100,2),round(numpy.std(scores)*100,2))


# In[ ]:


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=rdm_state)

kfold = KFold(n_splits=10, random_state=rdm_state)
log = LogisticRegression(C=grid1.best_estimator_.C)
log.fit(X_train,Y_train)
print("Cross validation train data : ",cross_valid(log,X_train,Y_train,5))
print("Accuracy test data : ",cross_valid(log,X_test,Y_test,5))


# In[ ]:


X_train, X_test, Y_train, Y_test = train_test_split(standardized_X, Y, test_size=test_size, random_state=rdm_state)

kfold = KFold(n_splits=10, random_state=rdm_state)
log = LogisticRegression(C=grid1.best_estimator_.C)
log.fit(X_train,Y_train)
print("Cross validation train data : ",cross_valid(log,X_train,Y_train,5))
print("Accuracy test data : ",cross_valid(log,X_test,Y_test,5))


# In[ ]:


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test_size, random_state=rdm_state)

kfold = KFold(n_splits=10, random_state=rdm_state)
svc = svm.SVC(kernel='linear',C=grid.best_estimator_.C)
svc.fit(X_train,Y_train)
print("Cross validation train data : ",cross_valid(svc,X_train,Y_train,5))
print("Accuracy test data : ",cross_valid(svc,X_test,Y_test,5))


# In[ ]:


X_train, X_test, Y_train, Y_test = train_test_split(standardized_X, Y, test_size=test_size, random_state=rdm_state)

kfold = KFold(n_splits=10, random_state=rdm_state)
svc = svm.SVC(kernel='linear',C=grid.best_estimator_.C)
svc.fit(X_train,Y_train)
print("Cross validation train data : ",cross_valid(svc,X_train,Y_train,5))
print("Accuracy test data : ",cross_valid(svc,X_test,Y_test,5))


# # Importance of features :

# In[ ]:


featuresImportances = log.coef_
indicesColumns = numpy.argsort(featuresImportances,axis=None)
indicesColumns = indicesColumns[::-1] #reverse the list
featuresImportances = featuresImportances[0]

#From the most to the least important
for i in range(data.shape[1]-1):
    print(i+1,data.columns.values[indicesColumns[i]],":",featuresImportances[indicesColumns[i]])


# In[ ]:


featuresImportances = log.coef_
indicesColumns = numpy.argsort(featuresImportances,axis=None)
indicesColumns = indicesColumns[::-1]
featuresImportances = featuresImportances[0]

#From the most to the least important
for i in range(data.shape[1]-1):
    print(i+1,data.columns.values[indicesColumns[i]],":",featuresImportances[indicesColumns[i]])


# # Best result with preprocessing and using linear regression
# ## Cross validation train data :  77.22 % (+/- 4.96 %)
# ## Accuracy test data : 79.47 %
