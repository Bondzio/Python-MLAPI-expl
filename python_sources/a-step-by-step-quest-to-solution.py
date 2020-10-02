#!/usr/bin/env python
# coding: utf-8

# # DON'T Overfit: A step-by-step quest to solution
# 
# The plan is as follows:
# - As a first step I will explore the Logistic regression (right now it achieved 0.844)
# - Next, will deal with the feature selection
# - After that I will try to understand the difference between the train and the test sets 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from sklearn import metrics
import sklearn.preprocessing, sklearn.kernel_ridge, sklearn.model_selection, sklearn.linear_model
import multiprocessing
import seaborn as sns
import scipy.stats


# In[ ]:


submission = pd.read_csv('../input/sample_submission.csv')
train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')
print(f'Shape of the train {train.shape}')
print(f'Shape of the test {test.shape}')
test.head()


# In[ ]:


data = train.iloc[:, 2:].values
ref = train['target'].values
#train['target'].value_counts()
#plt.figure()
sns.countplot(train['target'])
#plt.show()


# ### The first shot: Logistic regression
# We train the Logistic regression with different parameters, including optimizing the regularization strength

# In[ ]:


model_default = sklearn.linear_model.LogisticRegression()
model_default.fit(data, ref)

predict_test = model_default.predict_proba(test.iloc[:, 1:].values)
submission['target'] = predict_test
submission.to_csv('submission_logreg_default.csv', index=False)

model = sklearn.linear_model.LogisticRegression(class_weight='balanced', penalty='l1', C=0.1, solver='liblinear')
model.fit(data, ref)

predict_test = model.predict_proba(test.iloc[:, 1:].values)
submission['target'] = predict_test
submission.to_csv('submission_logreg_l1.csv', index=False)


# In[ ]:


def cross_validation(X, y, model, parameters, pname, nfold=10):
    cv_method = sklearn.model_selection.KFold(n_splits=nfold, shuffle=True, random_state=13)
    rgr = sklearn.model_selection.GridSearchCV(model, parameters, n_jobs=multiprocessing.cpu_count()-1, cv=cv_method, scoring='roc_auc')
    rgr.fit(X, y)
    plt.semilogx(parameters[pname], rgr.cv_results_['mean_test_score'], 'o-r')
    plt.xlabel(pname)
    plt.ylabel('ROC-AUC')
    plt.title(f'{nfold}-Fold cross validation')
    print(f"The best {pname} parameter is {rgr.best_params_[pname]}")
    return rgr


# In[ ]:


model = sklearn.linear_model.LogisticRegression(class_weight='balanced', penalty='l1', solver='liblinear')
parameters = {'C': np.logspace(-2, 5, 40)}
rgr = cross_validation(data, ref, model, parameters, 'C', nfold=10)


# In[ ]:


predict_test = rgr.best_estimator_.predict_proba(test.iloc[:, 1:].values)
submission['target'] = predict_test
submission.to_csv('submission_logreg_cv_l1.csv', index=False)


# ### Summarizing the results of submitting the LogisticRegression:
# - A default Logistic regression trained on the train set and all the features gives 0.274 score in the leaderboard of the competition - much worse than the 0.5 of the completely random submission
# - A Logistic regressoin with the parameters: 'class_weight='balanced', penalty='l1', C=0.1, solver='liblinear'' gives score of 0.844
# - Optimizing the parameter C with the 40-fold cross-validation doesn't improve the score: 0.843

# ### Next: Averaging the model
# 

# In[ ]:


def cross_validation_average(X, y, X_test, model, nfold=10):
    scores = []
    y_test = 0
    folds = sklearn.model_selection.StratifiedKFold(n_splits=nfold, shuffle=True, random_state=13)
    for idx, (train_index, valid_index) in enumerate(folds.split(X, y)):
        X_train, X_valid = X[train_index], X[valid_index]
        y_train, y_valid = y[train_index], y[valid_index]
        print(f'Process fold no {idx}: train/validation={len(y_train)}/{len(y_valid)}')

        model = model
        model.fit(X_train, y_train)
        y_pred_valid = model.predict(X_valid).reshape(-1,)
        score = metrics.roc_auc_score(y_valid, y_pred_valid)
        y_test += model.predict_proba(X_test)[:, 1]
        scores.append(score)

    plt.plot(range(nfold), scores, 'o-r')
    plt.xlabel('N-Fold')
    plt.ylabel('ROC-AUC')
    plt.title(f'{nfold}-Fold cross validation scores')
    print(f"Results: Max={np.max(scores)}, Mean={np.mean(scores)}, STD={np.std(scores)}")
    return scores, y_test/nfold


# In[ ]:


scores, predict_test = cross_validation_average(data, ref, test.iloc[:, 1:].values, rgr.best_estimator_, nfold=10)
submission['target'] = predict_test
submission.to_csv('submission_logreg_cv_l1_average.csv', index=False)


# Summarizing the results of submitting the LogisticRegression:
# - Averaging over 10 folds of the same model gives the result 0.842 - not an improvement comparing to the previous result

# 
