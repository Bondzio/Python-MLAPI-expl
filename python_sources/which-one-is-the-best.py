#!/usr/bin/env python
# coding: utf-8

#  Code based on notebooks of
#  https://www.kaggle.com/xhlulu/ieee-fraud-xgboost-with-gpu-fit-in-40s  
#  https://www.kaggle.com/davidcairuz/feature-engineering-lightgbm

# In this notebook, I tried random split, time series basd split, kflod and time_series_fold to see which val is the best using catboost.

# In[ ]:


print('loading libs...')
import warnings
warnings.filterwarnings("ignore")
import os
import gc
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import KFold
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import TimeSeriesSplit
from catboost import CatBoostClassifier
print('done')


# In[ ]:


get_ipython().run_cell_magic('time', '', "print('loading data...')\ntrain_transaction = pd.read_csv('../input/ieee-fraud-detection/train_transaction.csv', index_col='TransactionID')\ntest_transaction = pd.read_csv('../input/ieee-fraud-detection/test_transaction.csv', index_col='TransactionID')\ntrain_identity = pd.read_csv('../input/ieee-fraud-detection/train_identity.csv', index_col='TransactionID')\ntest_identity = pd.read_csv('../input/ieee-fraud-detection/test_identity.csv', index_col='TransactionID')\nsample_submission = pd.read_csv('../input/ieee-fraud-detection/sample_submission.csv')\nprint('done')")


# In[ ]:


features=['TransactionDT', 'card1', 'TransactionAmt', 'card2', 'addr1',
       'P_emaildomain', 'D15', 'card5', 'C13', 'dist1', 'D10', 'D4',
       'id_02', 'D1', 'id_20', 'C1', 'id_19', 'D2', 'id_31', 'D8', 'C2',
       'DeviceInfo', 'D11', 'C14', 'C6', 'C11', 'R_emaildomain', 'C9',
       'id_06', 'V313', 'id_05', 'M4', 'D3', 'id_33', 'M6', 'D5', 'dist2',
       'V307', 'V310', 'M5', 'id_01', 'card4', 'id_13', 'C5', 'D9',
       'card3', 'card6', 'id_30', 'V315', 'V314', 'D14', 'C10', 'C8',
       'V130', 'C12', 'id_14', 'V312', 'V83', 'V87', 'V127', 'V62',
       'id_18', 'D6', 'V317', 'V308', 'V320', 'ProductCD', 'V82', 'V76',
       'V61', 'M7', 'V53', 'V54', 'D13', 'V20', 'M3', 'V55', 'V78', 'D12',
       'V283', 'M8', 'V45', 'V38', 'V75', 'M9', 'V285', 'V309', 'V13',
       'V311', 'V131', 'V77', 'V291', 'V12', 'V37', 'V281', 'V282', 'V19',
       'V56', 'V35', 'V36']


# In[ ]:


get_ipython().run_cell_magic('time', '', "print('merging data...')\ntrain = train_transaction.merge(train_identity, how='left', left_index=True, right_index=True)\ntest = test_transaction.merge(test_identity, how='left', left_index=True, right_index=True)\n\nprint('dropping target...')\ny_train = train['isFraud'].copy()\ndel train_transaction, train_identity, test_transaction, test_identity\nX_train = train.drop('isFraud', axis=1)\nX_test = test.copy()\ndel train, test\n\nprint('fillnas...')\nX_train = X_train.fillna(0)\nX_test = X_test.fillna(0)\ngc.collect()\n\nprint('Label Encoding...')\nfor f in X_train.columns:\n    if X_train[f].dtype=='object' or X_test[f].dtype=='object': \n        lbl = preprocessing.LabelEncoder()\n        lbl.fit(list(X_train[f].values) + list(X_test[f].values))\n        X_train[f] = lbl.transform(list(X_train[f].values))\n        X_test[f] = lbl.transform(list(X_test[f].values))\n\nprint('selecting features...')\nX_train = X_train[features]\nX_test=X_test[features]\nprint('Done')")


# In[ ]:


ITERATION = 10000
DEPTH = 9
LR = 0.03
LLR = 9
VERBOSE = 400
BOOL = False
ER = 100


# 1.random train_test_split

# In[ ]:


X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=0)
clf= CatBoostClassifier(iterations=ITERATION, depth=DEPTH, learning_rate=LR, l2_leaf_reg=LLR, loss_function='CrossEntropy',eval_metric='AUC',
                            verbose=VERBOSE,random_state=0)

clf.fit(X_tr, y_tr,eval_set=(X_val, y_val),plot=BOOL , early_stopping_rounds=ER)
y_pred_valid = clf.predict_proba(X_val)[:,1]


# In[ ]:


print(f" AUC: {roc_auc_score(y_val, y_pred_valid)}")  
print('predicting...')
y_preds = clf.predict_proba(X_test)[:,1]
print('submission...')
sample_submission['isFraud'] = y_preds
sample_submission.to_csv("submission_rd.csv", index=False)
print('done')


# 2.time series based split

# In[ ]:


split_ind = int(X_train.shape[0]*0.8)

X_tr = X_train.iloc[:split_ind]
X_val = X_train.iloc[split_ind:]

y_tr = y_train.iloc[:split_ind]
y_val = y_train.iloc[split_ind:]


# In[ ]:


clf= CatBoostClassifier(iterations=ITERATION, depth=DEPTH, learning_rate=LR, l2_leaf_reg=LLR, loss_function='CrossEntropy',eval_metric='AUC',
                            verbose=VERBOSE,random_state=0)

clf.fit(X_tr, y_tr,eval_set=(X_val, y_val),plot=BOOL , early_stopping_rounds=ER)
y_pred_valid = clf.predict_proba(X_val)[:,1]


# In[ ]:


print(f" AUC: {roc_auc_score(y_val, y_pred_valid)}")  
print('predicting...')
y_preds = clf.predict_proba(X_test)[:,1]
print('submission...')
sample_submission['isFraud'] = y_preds
sample_submission.to_csv("submission_ts.csv", index=False)
print('done')


# 3.kfold

# In[ ]:


get_ipython().run_cell_magic('time', '', 'NFOLDS=5\nfolds = KFold(n_splits=NFOLDS)\ncolumns = X_train.columns\nsplits = folds.split(X_train, y_train)\ny_preds = np.zeros(X_test.shape[0])\ny_oof = np.zeros(X_train.shape[0])\nscore = 0\n  \nfor fold_n, (train_index, valid_index) in enumerate(splits):\n    X_tr, X_val = X_train[columns].iloc[train_index], X_train[columns].iloc[valid_index]\n    y_tr, y_val = y_train.iloc[train_index], y_train.iloc[valid_index]    \n    clf= CatBoostClassifier(iterations=ITERATION, depth=DEPTH, learning_rate=LR, l2_leaf_reg=LLR, loss_function=\'CrossEntropy\',eval_metric=\'AUC\',\n                            verbose=VERBOSE,random_state=0)\n\n    clf.fit(X_tr, y_tr,eval_set=(X_val, y_val),plot=BOOL , early_stopping_rounds=ER)\n    y_pred_valid = clf.predict_proba(X_val)[:,1]\n    y_oof[valid_index] = y_pred_valid\n    print(f"Fold {fold_n + 1} | AUC: {roc_auc_score(y_val, y_pred_valid)}")   \n    score += roc_auc_score(y_val, y_pred_valid) / NFOLDS\n    y_preds += clf.predict_proba(X_test)[:,1]/ NFOLDS    \n    del X_tr, X_val, y_tr, y_val\n    gc.collect()  ')


# In[ ]:


print(f"\nMean AUC = {score}")
print(f"Out of folds AUC = {roc_auc_score(y_train, y_oof)}")

print('submission...')
sample_submission['isFraud'] = y_preds
sample_submission.to_csv("submission_kfold.csv", index=False)
print('done')


# 4.time_series_split

# In[ ]:


get_ipython().run_cell_magic('time', '', 'NFOLDS=5\nfolds = TimeSeriesSplit(n_splits=NFOLDS)\ncolumns = X_train.columns\nsplits = folds.split(X_train, y_train)\ny_preds = np.zeros(X_test.shape[0])\ny_oof = np.zeros(X_train.shape[0])\nscore = 0\n  \nfor fold_n, (train_index, valid_index) in enumerate(splits):\n    X_tr, X_val = X_train[columns].iloc[train_index], X_train[columns].iloc[valid_index]\n    y_tr, y_val = y_train.iloc[train_index], y_train.iloc[valid_index]    \n    clf= CatBoostClassifier(iterations=ITERATION, depth=DEPTH, learning_rate=LR, l2_leaf_reg=LLR, loss_function=\'CrossEntropy\',eval_metric=\'AUC\',\n                            verbose=VERBOSE,random_state=0)\n\n    clf.fit(X_tr, y_tr,eval_set=(X_val, y_val),plot=BOOL , early_stopping_rounds=ER)\n    y_pred_valid = clf.predict_proba(X_val)[:,1]\n    y_oof[valid_index] = y_pred_valid\n    print(f"Fold {fold_n + 1} | AUC: {roc_auc_score(y_val, y_pred_valid)}")   \n    score += roc_auc_score(y_val, y_pred_valid) / NFOLDS\n    y_preds += clf.predict_proba(X_test)[:,1]/ NFOLDS    \n    del X_tr, X_val, y_tr, y_val\n    gc.collect()    ')


# In[ ]:


print(f"\nMean AUC = {score}")
print(f"Out of folds AUC = {roc_auc_score(y_train, y_oof)}")

print('submission...')
sample_submission['isFraud'] = y_preds
sample_submission.to_csv("submission_tsfold.csv", index=False)
print('done')

