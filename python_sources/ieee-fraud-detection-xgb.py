#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import random
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from xgboost.sklearn import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import PredefinedSplit, GridSearchCV


# In[ ]:


SEED = 31
N_ESTIMATORS = 10000
TARGET = 'isFraud'
VALIDATION_PERCENT = 0.16
SCORING = 'roc_auc'


# In[ ]:


def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    
seed_everything(SEED)


# In[ ]:


file_folder = '../input/ieee-fraud-detection-preprocess'
train = pd.read_csv(f'{file_folder}/train.csv')
test = pd.read_csv(f'{file_folder}/test.csv')
print(f'train={train.shape}, test={test.shape}')


# In[ ]:


def _keep(col):
    if col == TARGET:
        return False
    if col.startswith('_pc_'):
        return False
    if '_to_' in col:
        return False
    return True


PREDICTORS = [c for c in train.columns.values if _keep(c)]
print(f'{len(PREDICTORS)} predictors={PREDICTORS}')


# In[ ]:


val_size = int(VALIDATION_PERCENT * len(train))
train_size = len(train) - val_size
train_ind = [-1] * train_size
val_ind = [0] * val_size
ps = PredefinedSplit(test_fold=np.concatenate((train_ind, val_ind)))
val = train[-val_size:]
val.info()


# In[ ]:


get_ipython().run_cell_magic('time', '', "y_train = train[TARGET]\nx_train = train[PREDICTORS]\ny_val = val[TARGET]\nx_val = val[PREDICTORS]\nmodel = XGBClassifier(learning_rate=0.1, n_estimators=N_ESTIMATORS, reg_alpha=1, reg_lambda=0, tree_method='hist')\npipe = Pipeline([('model', model)])\nparam_grid = {\n    'model__max_depth': [8],\n    'model__colsample_bytree': [0.75]\n}\ncv = GridSearchCV(pipe, cv=ps, param_grid=param_grid, scoring=SCORING)\ncv.fit(x_train, y_train, model__eval_set=[(x_val, y_val)], model__eval_metric='auc', model__early_stopping_rounds=200, model__verbose=False)\nprint('best_params_={}\\nbest_score_={}'.format(repr(cv.best_params_), repr(cv.best_score_)))")


# In[ ]:


x_test = test[PREDICTORS]
sub = pd.read_csv(f'../input/ieee-fraud-detection/sample_submission.csv')
sub[TARGET] = cv.predict_proba(x_test)[:,1]
sub.head()


# In[ ]:


sub.to_csv('submission.csv', index=False)
print(os.listdir("."))

