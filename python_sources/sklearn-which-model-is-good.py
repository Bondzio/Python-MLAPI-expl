#!/usr/bin/env python
# coding: utf-8

# # Introduction
# I'll build a model with logistic regression, SVM and random forest by using sklearn.  
# And I'll evaluate the three models and consider which one to choose.

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


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score
import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings(action='ignore', category=ConvergenceWarning)
warnings.filterwarnings(action='ignore', category=DeprecationWarning)


# ## Load and check the dataset

# In[ ]:


data = pd.read_csv('../input/heart.csv')


# In[ ]:


data.head()


# In[ ]:


data.dtypes


# In[ ]:


data.isnull().sum()


# 
# All columns are numerical.  
# However, there are columns that should be treated as categories rather than numbers. 

# In[ ]:


data['cp'] = data['cp'].astype(object)
data['restecg'] = data['restecg'].astype(object)
data['slope'] = data['slope'].astype(object)
data['ca'] = data['ca'].astype(object)
data['thal'] = data['thal'].astype(object)
data = pd.get_dummies(data,drop_first=True)
data.head()


# In[ ]:


target = data['target']


# In[ ]:


data = data.drop(columns='target')


# In[ ]:


X_train,X_test,Y_train,Y_test = train_test_split(data,target,random_state=0)
scaler = StandardScaler()
scaler.fit(X_train)
# Logistic Regression and SVM use scaled data.
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)


# This time I'll compare the performance of Logistic Regression, SVM and Random Forest.  
# *In the code, it is abbreviated as follows.  
# Logistic Regression : LR  
# SVM: SVM  
# Random Forest : RF  

# ## Train three models

# In[ ]:



# LogisticRegression Train
param_grid = {'C':[0.001,0.01,0.1,1,10,100],
              'solver':['lbfgs','liblinear','sag','saga'],
              'max_iter':[1,5,10,25,50,75,100,125,150]}

lr = GridSearchCV(LogisticRegression(random_state=0),param_grid,cv=5)
lr.fit(X_train_scaled,Y_train)

# SVM Train
param_grid = {'C':[0.001,0.01,0.1,1,10,100],
             'gamma':[0.001,0.01,0.1,1,10,100]}


svm = GridSearchCV(SVC(),param_grid,cv=5)
svm.fit(X_train_scaled,Y_train)

# RandomForest Train
# When the depth is 2 or more, it becomes over fitting.
param_grid = {'n_estimators':[10,25,50,75,100,125,150],
              'max_depth':[1]}

rf = GridSearchCV(RandomForestClassifier(random_state=0),param_grid,cv=5)
rf.fit(X_train,Y_train)


# In[ ]:


print('LogisticRegression train set score: {:.2f}'.format(lr.score(X_train_scaled,Y_train)))
print('LogisticRegression test set score: {:.2f}'.format(lr.score(X_test_scaled,Y_test)))
print('LogisticRegression best paramerters: {}'.format(lr.best_params_))

print('SVM train set score: {:.2f}'.format(svm.score(X_train_scaled,Y_train)))
print('SVM test set score: {:.2f}'.format(svm.score(X_test_scaled,Y_test)))
print('SVM best paramerters: {}'.format(svm.best_params_))

print('RandomForest train set score: {:.2f}'.format(rf.score(X_train,Y_train)))
print('RandomForest test set score: {:.2f}'.format(rf.score(X_test,Y_test)))
print('RandomForest best paramerters: {}'.format(rf.best_params_))


# **Logistic regression has the best result. **  
# Next, check the result of cross validation.  

# ## Check cross-validation score

# In[ ]:



data = pd.concat([X_train,X_test])
data_scaled = np.concatenate([X_train_scaled,X_test_scaled])
target = pd.concat([Y_train,Y_test])
lr_scores = cross_val_score(lr,data_scaled,target,cv=5)
svm_scores = cross_val_score(svm,data_scaled,target,cv=5)
rf_scores = cross_val_score(rf,data,target,cv=5)


# In[ ]:


print('LR Cross-validation scores: ',lr_scores)
print('LR Mean Cross-validation scores: ',lr_scores.mean())

print('SVM Cross-validation scores: ',svm_scores)
print('SVM Mean Cross-validation scores: ',svm_scores.mean())

print('RF Cross-validation scores: ',rf_scores)
print('RF Mean Cross-validation scores: ',rf_scores.mean())


# 
# **As a result of cross validation, the result of logistic regression is the best.**  
# I'll analyze the results from different perspectives.  

# ## Check precision , recall and f1-score 

# In[ ]:


predict = lr.predict(X_test_scaled)
print("---Classification Report about LR---")
print(classification_report(Y_test,predict))


# In[ ]:


predict = svm.predict(X_test_scaled)
print("---Classification Report about SVM---")
print(classification_report(Y_test,predict))


# In[ ]:


predict = rf.predict(X_test)
print("---Classification Report about RF---")
print(classification_report(Y_test,predict))


# 
# The above shows **precision, recall, f1-score** of the three models.  
#   
# I'll clarify each definition.  
# ![](https://cdn-ak.f.st-hatena.com/images/fotolife/p/protoidea/20190210/20190210130811.png)  
#   
# **precision = TP/(TP + FP)  
# recall = TP/(TP+FN)  
# f1-score = 2 * (precision * recall)/(presion + recall)  
# TPR = recall  
# FPR = FP/(FP + TN)**  
#   
# Next, let's check the precision-recall-curve and ROC-curve.

# ## Check precision-recall-curve and ROC-curve

# In[ ]:


import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
from sklearn.metrics import precision_recall_curve
precision_lr,recall_lr,thresholds_lr = precision_recall_curve(Y_test,lr.decision_function(X_test_scaled))
precision_svm,recall_svm,thresholds_svm = precision_recall_curve(Y_test,svm.decision_function(X_test_scaled))
precision_rf,recall_rf,thresholds_rf = precision_recall_curve(Y_test,rf.predict_proba(X_test)[:,1])

plt.plot(precision_lr,recall_lr,label='LR')
plt.plot(precision_svm,recall_svm,label='SVM')
plt.plot(precision_rf,recall_rf,label='RF')

close_zero_lr = np.argmin(np.abs(thresholds_lr))
close_zero_svm = np.argmin(np.abs(thresholds_svm))
close_default_rf = np.argmin(np.abs(thresholds_rf -0.5))

plt.plot(precision_lr[close_zero_lr],recall_lr[close_zero_lr],'o',markersize=10,label="threshold zero lr",fillstyle="none",mew=2)
plt.plot(precision_svm[close_zero_svm],recall_svm[close_zero_svm],'^',markersize=10,label="threshold zero svm",fillstyle="none",mew=2)
plt.plot(precision_rf[close_default_rf],recall_rf[close_default_rf],'x',markersize=10,label="threshold 0.5 rf",fillstyle="none",mew=2)

plt.xlabel('Precision')
plt.ylabel('Recall')
plt.legend()


# In[ ]:


fpr_lr,tpr_lr,thresholds_lr = roc_curve(Y_test,lr.decision_function(X_test_scaled))
fpr_svm,tpr_svm,thresholds_svm = roc_curve(Y_test,svm.decision_function(X_test_scaled))
fpr_rf,tpr_rf,thresholds_rf = roc_curve(Y_test,rf.predict_proba(X_test)[:,1])

plt.plot(fpr_lr,tpr_lr,label="ROC Curve LR")
plt.plot(fpr_svm,tpr_svm,label="ROC Curve SVM")
plt.plot(fpr_rf,tpr_rf,label="ROC Curve RF")

close_zero_lr = np.argmin(np.abs(thresholds_lr))
close_zero_svm = np.argmin(np.abs(thresholds_svm))
close_default_rf = np.argmin(np.abs(thresholds_rf -0.5))

plt.plot(fpr_lr[close_zero_lr],tpr_lr[close_zero_lr],'o',markersize=10,label="threshold zero lr",fillstyle="none",mew=2)
plt.plot(fpr_svm[close_zero_svm],tpr_svm[close_zero_svm],'^',markersize=10,label="threshold zero svm",fillstyle="none",mew=2)
plt.plot(fpr_rf[close_default_rf],tpr_rf[close_default_rf],'x',markersize=10,label="threshold 0.5 rf",fillstyle="none",mew=2)

plt.xlabel("FPR")
plt.ylabel("TPR")
plt.legend(loc=4)


# Logistic regression and SVM have marked a threshold of 0, marking 0.5 in random forest.  
# Logistic regression has good results in total.  
# But, if you want to raise 'recall', it seems better to use SVM.  
# I guess that  **It is important to increase 'recall' in this problem** , because It is dangerous to mistakenly predict that heart disease is not a heart disease.  
# I think we should choose SVM that can increase recall while keeping precison high.
