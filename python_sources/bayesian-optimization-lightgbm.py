#!/usr/bin/env python
# coding: utf-8

# ## Bayesian Optimization - LightGBM

# Thanks to [NanoMathias's awesome notebook](https://www.kaggle.com/nanomathias/bayesian-optimization-of-xgboost-lb-0-9769/notebook), I got introduced to Scikit-Optimize and really felt the power of beyesian approach in parameter tuning.
# 
# However, it seems like BayesSearchCV is still not capable of dealing with complex setups(e.g. specify categorical features in lightgbm)(Update: as Bai Xue has pointed out in comment section: BayesSearchCV is actually more flexible than I thought..)
#  . After hours of exploring the package, here I'm going to shed some light on how to build a very flexible BayesSearch framework by using gp_minimize.
# 

# In[ ]:


import pandas as pd
import numpy as np
import xgboost as xgb
import lightgbm as lgb
import gc

from skopt.space import Real, Integer
from skopt.utils import use_named_args
import itertools
from sklearn.metrics import roc_auc_score
from skopt import gp_minimize


# Instead of doing cross-validation, in this notebook I'm going to use a simple fixed training and testing set. Just for illustration purpose :)

# In[ ]:


TRAINING_SIZE = 300000
TEST_SIZE = 50000

# Load data
train = pd.read_csv(
    '../input/train.csv', 
    skiprows=range(1,184903891-TRAINING_SIZE-TEST_SIZE), 
    nrows=TRAINING_SIZE,
    parse_dates=['click_time']
)

val = pd.read_csv(
    '../input/train.csv', 
    skiprows=range(1,184903891-TEST_SIZE), 
    nrows=TEST_SIZE,
    parse_dates=['click_time']
)

# Split into X and y
y_train = train['is_attributed']
y_val = val['is_attributed']


# Specify the parameter space we want to explore.

# In[ ]:


# from that dimension (`'log-uniform'` for the learning rate)
space  = [Integer(3, 10, name='max_depth'),
          Integer(6, 30, name='num_leaves'),
          Integer(50, 200, name='min_child_samples'),
          Real(1, 400,  name='scale_pos_weight'),
          Real(0.6, 0.9, name='subsample'),
          Real(0.6, 0.9, name='colsample_bytree')
         ]


# Below is the fun part. The function gp_minimize requires an objective function and what the function all needs is basically a metric we want to minimize. Of course, we can just use whatever training setup we have been using but just tweak it to return a AUC to minimize..(negative AUC)

# In[ ]:


def objective(values):
    

    params = {'max_depth': values[0], 
          'num_leaves': values[1], 
          'min_child_samples': values[2], 
          'scale_pos_weight': values[3],
            'subsample': values[4],
            'colsample_bytree': values[5],
             'metric':'auc',
             'nthread': 8,
             'boosting_type': 'gbdt',
             'objective': 'binary',
             'learning_rate':0.15,
             'max_bin': 100,
             'min_child_weight': 0,
             'min_split_gain': 0,
             'subsample_freq': 1}
    

    print('\nNext set of params.....',params)
    
    feature_set = ['app','device','os','channel']
    categorical = ['app','device','os','channel']
    
    
    early_stopping_rounds = 50
    num_boost_round       = 1000
    
        # Fit model on feature_set and calculate validation AUROC
    xgtrain = lgb.Dataset(train[feature_set].values, label=y_train,feature_name=feature_set,
                           categorical_feature=categorical)
    xgvalid = lgb.Dataset(val[feature_set].values, label=y_val,feature_name=feature_set,
                          categorical_feature=categorical)
    
    evals_results = {}
    model_lgb     = lgb.train(params,xgtrain,valid_sets=[xgtrain, xgvalid], 
                              valid_names=['train','valid'], 
                               evals_result=evals_results, 
                               num_boost_round=num_boost_round,
                                early_stopping_rounds=early_stopping_rounds,
                               verbose_eval=None, feval=None)
    
    auc = -roc_auc_score(y_val, model_lgb.predict(val[model_lgb.feature_name()]))
    
    print('\nAUROC.....',-auc,".....iter.....", model_lgb.current_iteration())
    
    gc.collect()
    
    return  auc


# Alright, let's run the tuning process.

# In[ ]:


res_gp = gp_minimize(objective, space, n_calls=20,
                     random_state=0,n_random_starts=10)

"Best score=%.4f" % res_gp.fun


# In[ ]:


from skopt.plots import plot_convergence

plot_convergence(res_gp)


# The best AUC here is pretty weird but I guess that's all because I'm using a very arbitrary training and validation set :)
