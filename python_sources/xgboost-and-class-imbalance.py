#!/usr/bin/env python
# coding: utf-8

# The purpose of this notbook is to perform the following tasks:
#  
#  1. [Baseline Xgboost](#1)
#  2. [Custom Weight Xgboost](#2)
#  3. [scale_pos_weight Xgboost](#3)
#  
# The idea is to show how to use custom weight or scale_pos_weight to balance the target feature for Xgboost. The parameters are not optimized because the purpose is to demonstrate the use of scale_pos_weight and custom weight. The input data comes from the [here](https://www.kaggle.com/wti200/data-preparation-binning-and-imputaion).

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn import preprocessing
import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import roc_auc_score


# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


train = pd.read_csv("../input/data-preparation-binning-and-imputaion/train_clean_RobustScaler.csv", index_col = 'TransactionID')


# In[ ]:


# Label Encoding
cols = [c for c in train if c not in ['isFraud', 'TransactionID', 'TransactionDT']]

for f in train[cols].columns:
    if train[f].dtype=='object': 
        lbl = preprocessing.LabelEncoder()
        lbl.fit(list(train[f].values))
        train[f] = lbl.transform(list(train[f].values))

cols = [c for c in train if c not in ['isFraud', 'TransactionID', 'TransactionDT']]
y=np.array(train['isFraud'])
X=np.array(train[cols])


# In[ ]:


# Time series split
tscv = TimeSeriesSplit(n_splits=2)

for train_index, test_index in tscv.split(train):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
del train


# ### [Base line Xgboost](#1)<a id="1"></a> <br>
# 
# * Here a simple xgboost. Here we do not account for the class imbalance.

# In[ ]:


dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test)

# %% [code]
params = {
    'objective': 'binary:logistic',
    'max_depth' : 8,
    'silent': 1,
    'eta':1
}
num_rounds=5

bst=xgb.train(params, dtrain, num_rounds)
y_test_preds = (bst.predict(dtest) > 0.5).astype('int')


pd.crosstab(
    pd.Series(y_test, name='Actual'),
    pd.Series(y_test_preds, name='Predicted'),
    margins=True
)


print('Accuracy: {0:.2f}'.format(accuracy_score(y_test, y_test_preds)))
print('Precision: {0:.2f}'.format(precision_score(y_test, y_test_preds)))
print('Recall: {0:.2f}'.format(recall_score(y_test, y_test_preds)))
print('AUC ROC: {0:.2f}'.format(roc_auc_score(y_test, y_test_preds)))


# ### [Custom Weight Xgboost](#2)<a id="2"></a> <br>
# * Explicitly tell the algorithme to assign more weight to minority class by using the weight argument.
# 

# In[ ]:


params = {
    'objective': 'binary:logistic',
    'max_depth' : 8,
    'silent': 1,
    'eta':1
}
num_rounds=5

weights = np.zeros(len(y_train))
weights[y_train == 0] = 1
weights[y_train == 1] = 5

dtrain = xgb.DMatrix(X_train, label=y_train, weight=weights) # weight added
dtest = xgb.DMatrix(X_test)


bst=xgb.train(params, dtrain, num_rounds)
y_test_preds = (bst.predict(dtest) > 0.5).astype('int')


pd.crosstab(
    pd.Series(y_test, name='Actual'),
    pd.Series(y_test_preds, name='Predicted'),
    margins=True
)

print('Accuracy: {0:.2f}'.format(accuracy_score(y_test, y_test_preds)))
print('Precision: {0:.2f}'.format(precision_score(y_test, y_test_preds)))
print('Recall: {0:.2f}'.format(recall_score(y_test, y_test_preds)))
print('AUC ROC: {0:.2f}'.format(roc_auc_score(y_test, y_test_preds)))


# ### [scale_pos_weight](#3)<a id="3"></a> <br>
# 
# * Scale_pos_weight is the ratio of number of negative class to the positive class. 

# In[ ]:


params = {
    'objective': 'binary:logistic',
    'max_depth' : 8,
    'silent': 1,
    'eta':1
}
num_rounds=5

dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test)

# %% [code]
train_labels = dtrain.get_label()
ratio= float(np.sum(train_labels == 0)) / np.sum(train_labels == 1)
params['scale_pos_weight'] = ratio

# %% [code]
bst=xgb.train(params, dtrain, num_rounds)
y_test_preds = (bst.predict(dtest) > 0.5).astype('int')

pd.crosstab(
    pd.Series(y_test, name='Actual'),
    pd.Series(y_test_preds, name='Predicted'),
    margins=True
)

# %% [code]
print('Accuracy: {0:.2f}'.format(accuracy_score(y_test, y_test_preds)))
print('Precision: {0:.2f}'.format(precision_score(y_test, y_test_preds)))
print('Recall: {0:.2f}'.format(recall_score(y_test, y_test_preds)))
print('AUC ROC: {0:.2f}'.format(roc_auc_score(y_test, y_test_preds)))

