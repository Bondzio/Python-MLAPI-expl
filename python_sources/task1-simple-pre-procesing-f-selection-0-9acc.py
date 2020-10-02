#!/usr/bin/env python
# coding: utf-8

# **TASK 1**
# 
# This  notebooks show an approch with Support Vector Machines and Random Forest in order to solve the Task one of the challenge. The main steps are described as bellow:
# 
# * Pre-processing
# * Feature Selecion
# * Search Paramters ans Classification with SVM and Random Forest
# * Results and analysis
# 

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


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from pandas import set_option
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBClassifier
from sklearn.svm import SVC,LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report,confusion_matrix, plot_confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel
from sklearn.pipeline import Pipeline


# In[ ]:


dataset = pd.read_excel('/kaggle/input/covid19/dataset.xlsx')
dataset.head()


# Verifing all nullable values.

# In[ ]:


dataset.isnull().sum()

Dropping Patient ID.
# In[ ]:


dataset.drop(['Patient ID'], axis=1, inplace = True)
numeric_cols = []
category_cols = []
object_cols = []


# ## Data pre-processing

# Special Treatment for Urine - pH:

# Creates a List of all Numeric cols and Categorical cols.

# In[ ]:


for c in dataset.columns:
    print("Col {} Format {}".format(c, dataset[c].dtype ) )
    if(dataset[c].dtype == np.float64 or dataset[c].dtype == np.int64):
          numeric_cols.append(c)
  
    else:
          category_cols.append(c)


# Get all positives and negatives samples for COVID-19 and fill all "na" with the meaning of each class.

# In[ ]:


positives = dataset['SARS-Cov-2 exam result'] == 'positive'
negatives = dataset['SARS-Cov-2 exam result'] == 'negatives'

for nu in numeric_cols:
    meancolpos = dataset[nu][positives].mean()
    meancolneg = dataset[nu][negatives].mean()
       
    dataset[nu][positives].fillna(meancolpos, inplace = True)
    dataset[nu][negatives].fillna(meancolpos, inplace = True)


# Creates a list of all Categorical Cols and applies one hot enconding for these categorical features:

# In[ ]:


for ca in category_cols:
    dataset[ca].fillna('Not tested/Not Aplicable', inplace = True)
    
    onehotenc = pd.get_dummies(dataset[ca]) 
    
    for o in onehotenc.columns:
        onehotenc.rename(columns={ o: ca + "-" + str(o)}, inplace=True)
    
    dataset.drop([ca], axis=1,inplace = True)
    
    dataset = pd.concat([dataset, onehotenc], axis=1)


# In[ ]:


dataset.isnull().sum()

resisnull = dataset.isnull().sum()

print(resisnull)

for i, v in resisnull.items():  
    if(v > 0):
        print("Dropping Col {}".format(i))
        dataset.drop([i], axis=1,inplace = True)
        
resisnull = dataset.isnull().sum()
print(resisnull)


# Store class values:

# In[ ]:


y = dataset["SARS-Cov-2 exam result-positive"].values
dataset.drop(["SARS-Cov-2 exam result-positive", "SARS-Cov-2 exam result-negative"], axis =1, inplace= True)


# ## Feature Selection using Linear SVC

# Verify the correlation of all features:

# In[ ]:


set_option('precision', 2)
corr = dataset.corr(method='pearson')
sns.heatmap(corr)


# Remove features with high correlation:

# In[ ]:


columns = np.full((corr.shape[0],), True, dtype=bool)
for i in range(corr.shape[0]):
    for j in range(i+1, corr.shape[0]):
        if corr.iloc[i,j] >= 0.9 or corr.iloc[i,j] <= -0.9:
            if columns[j]:
                columns[j] = False
selected_columns = dataset.columns[columns]
dataset = dataset[selected_columns]


# Verify the correlation one more time after romoves high correlations:

# In[ ]:


set_option('precision', 2)
corr = dataset.corr(method='pearson')
sns.heatmap(corr)


# Creates de Matriz X, training and test set:

# In[ ]:


print(dataset.shape)

X = dataset.values
seed = 7
test_size = 0.30


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
X_select = StandardScaler().fit_transform(X)


# Apply a LinearSVM in order to select the more important features:

# In[ ]:


lsvc = LinearSVC(C=0.1, penalty="l1", dual=False).fit(X_select, y)
model = SelectFromModel(lsvc, prefit=True)
X_new = model.transform(X_select)

print(X_new.shape)

mask = model.get_support() #list of booleans
new_features = [] # The list of your K best features
feature_names = list(dataset.columns.values)

for bool, feature in zip(mask, feature_names):
    if bool:
        new_features.append(feature)
        print(feature)


# ## Experiment #1 SVM with all features
Training the first model using SVM-RBF and Search the hyper-parameters using GridSearch, f1_macro were used because we have an unbalanced  data:
# In[ ]:


pipe = Pipeline([
    ('scaler',StandardScaler()),
    ('clf', SVC())
])


list_C = [0.001, 0.01, 0.1, 1, 10,100]
list_gamma = [0.001, 0.01, 0.1, 1, 10, 100]

parametros_grid = dict(clf__C=list_C, clf__gamma=list_gamma)
gridSVM = GridSearchCV(pipe, parametros_grid, cv=5, scoring='f1_macro', verbose = 10, n_jobs  = 4)
gridSVM.fit(X_train,y_train)

print(gridSVM.best_score_)
print(gridSVM.best_params_)


# Analysing the results with training set

# In[ ]:


y_true, y_pred = y_test, gridSVM.predict(X_test)
print(classification_report(y_true, y_pred))


# Plot the confusion Matrix:

# In[ ]:


bestPipe = gridSVM.best_estimator_
bestSVM = bestPipe['clf']
print(bestSVM)

cm = confusion_matrix(y_true, y_pred)
print(cm)
plot_confusion_matrix(bestSVM, X_test, y_test, normalize = 'true')


# ## Experiment #2 SVM with features from LinearSVM

# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=test_size, random_state=seed)

pipe = Pipeline([
    ('scaler',StandardScaler()),
    ('clf', SVC())
])


list_C = [0.001, 0.01, 0.1, 1, 10,100]
list_gamma = [0.001, 0.01, 0.1, 1, 10, 100]

parametros_grid = dict(clf__C=list_C, clf__gamma=list_gamma)
gridSVM = GridSearchCV(pipe, parametros_grid, cv=5, scoring='f1_macro', verbose = 10, n_jobs  = 4)
gridSVM.fit(X_train,y_train)

print(gridSVM.best_score_)
print(gridSVM.best_params_)


# Plot the confusion Matrix Experiment #2:

# In[ ]:


y_true, y_pred = y_test, gridSVM.predict(X_test)
print(classification_report(y_true, y_pred))

bestPipe = gridSVM.best_estimator_
bestSVM = bestPipe['clf']
print(bestSVM)

cm = confusion_matrix(y_true, y_pred)
print(cm)
plot_confusion_matrix(bestSVM, X_test, y_test, normalize = 'true')


# ## Experiment #3 Random Forest with All features

# In[ ]:


X_rf = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_xgb, y, test_size=test_size, random_state=seed)


forest = RandomForestClassifier(random_state = 1)

n_estimators = [100, 300, 500, 800]
max_depth = [5, 8, 15, 25, 30]
min_samples_split = [2, 5, 10, 15]
min_samples_leaf = [1, 2, 5] 

hyperF = dict(n_estimators = n_estimators, max_depth = max_depth,  
              min_samples_split = min_samples_split, 
             min_samples_leaf = min_samples_leaf)

GridSearchCV(forest, hyperF, cv = 5, verbose = 1, n_jobs = 10, scoring='f1_macro')

bestpipe = gridF.fit(X_train, y_train)


# In[ ]:


print(gridF.best_score_)
print(gridF.best_params_)


# In[ ]:


print(classification_report(y_true, y_pred))

bestEst = gridF.best_estimator_
print(bestEst)


cm = confusion_matrix(y_true, y_pred)
print(cm)
plot_confusion_matrix(bestEst, X_test, y_test, normalize = 'true')


# ## Experiment #4 Random Forest with Selected Features

# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=test_size, random_state=seed)


forest = RandomForestClassifier(random_state = 1)

n_estimators = [100, 300, 500, 800]
max_depth = [5, 8, 15, 25, 30]
min_samples_split = [2, 5, 10, 15]
min_samples_leaf = [1, 2, 5] 

hyperF = dict(n_estimators = n_estimators, max_depth = max_depth,  
              min_samples_split = min_samples_split, 
             min_samples_leaf = min_samples_leaf)

GridSearchCV(forest, hyperF, cv = 5, verbose = 1, n_jobs = 10, scoring='f1_macro')

gridF.fit(X_train, y_train)


# In[ ]:


print(classification_report(y_true, y_pred))

bestEst = gridF.best_estimator_
print(bestEst)


cm = confusion_matrix(y_true, y_pred)
print(cm)
plot_confusion_matrix(bestEst, X_test, y_test, normalize = 'true')


# # Results:

# The best result was obtained using SVM with the characteristics selected through LinearSVM, since the dataset is unbalanced, we analyzed the f1_macro as an important measure to decide which is the best classification.
# 
# In the confusion matrix we can analyze that for all classifiers the model still makes a lot of wrong classifications  for positive records, however this is also due to the nature of the datset.
# 
# Other methods of feature selection can be applied such as heuritics (Genetic algorithms for example) and other types of classifiers such as neural networks and essemble.
