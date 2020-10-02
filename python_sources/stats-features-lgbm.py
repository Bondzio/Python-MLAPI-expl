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


print(os.listdir("../input/stats-df"))


# In[ ]:


import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.metrics import mean_squared_error
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


num_submission = 3
random_state = 3213


# In[ ]:


train_df = pd.read_csv('../input/santander-customer-transaction-prediction/train.csv')
test_df = pd.read_csv('../input/santander-customer-transaction-prediction/test.csv')


# In[ ]:


target = train_df['target']


# In[ ]:


train_stats = pd.read_csv('../input/stats-df/stats_train.csv')
test_stats = pd.read_csv('../input/stats-df/stats_test.csv')


# In[ ]:


swap = train_stats.columns[1:]


# In[ ]:


extra_train = pd.concat([train_df.transpose(), train_stats.transpose()]).transpose()


# In[ ]:


del extra_train["Unnamed: 0"]


# In[ ]:


extra_train.head()


# In[ ]:


extra_test = pd.concat([test_df.transpose(), test_stats.transpose()]).transpose()


# In[ ]:


del extra_test["Unnamed: 0"]


# In[ ]:


extra_test.head()


# In[ ]:


del train_df, test_df, train_stats, test_stats


# In[ ]:


features = [c for c in extra_train.columns if c not in ['ID_code', 'target']]


# In[ ]:


def augment(x,y,t=2):
    xs,xn = [],[]
    for i in range(t):
        mask = y>0
        x1 = x[mask].copy()
        ids = np.arange(x1.shape[0])
        for c in range(x1.shape[1]):
            np.random.shuffle(ids)
            x1[:,c] = x1[ids][:,c]
        xs.append(x1)

    for i in range(t//2):
        mask = y==0
        x1 = x[mask].copy()
        ids = np.arange(x1.shape[0])
        for c in range(x1.shape[1]):
            np.random.shuffle(ids)
            x1[:,c] = x1[ids][:,c]
        xn.append(x1)

    xs = np.vstack(xs)
    xn = np.vstack(xn)
    ys = np.ones(xs.shape[0])
    yn = np.zeros(xn.shape[0])
    x = np.vstack([x,xs,xn])
    y = np.concatenate([y,ys,yn])
    return x,y


# In[ ]:


lgb_params = {
    "objective" : "binary",
    "metric" : "auc",
    "boosting": 'gbdt',
    "max_depth" : 90,
    "num_leaves" : 15,
    "learning_rate" : 0.01000123,
    "bagging_freq": 5,
    "bagging_fraction" : 0.4,
    "feature_fraction" : 0.05,
    "min_data_in_leaf": 150,
    "min_sum_heassian_in_leaf": 15,
    "tree_learner": "voting",
    "boost_from_average": "false",
    "lambda_l1" : 10,
    "lambda_l2" : 10,
    "bagging_seed" : random_state,
    "verbosity" : 1,
    "seed": random_state
}


# In[ ]:


num_folds = 3
folds = StratifiedKFold(n_splits=num_folds, shuffle=False, random_state=random_state)
oof = extra_train[['ID_code', 'target']]
oof['predict'] = 0
predictions = extra_test[['ID_code']]
val_aucs = []
feature_importance_df = pd.DataFrame()


# In[ ]:


X_test = extra_test[features].values


# In[ ]:


for fold, (trn_idx, val_idx) in enumerate(folds.split(extra_train.values, target.values)):
    print("Fold :{}".format(fold + 1))
    X_train, y_train = extra_train.iloc[trn_idx][features], target.iloc[trn_idx]
    X_valid, y_valid = extra_train.iloc[val_idx][features], target.iloc[val_idx]
    
    N = 4
    p_valid,yp = 0,0
    for i in range(N):
        X_t, y_t = augment(X_train.values, y_train.values)
        X_t = pd.DataFrame(X_t)
        X_t = X_t.add_prefix('var_')
        X_t.columns = [*X_t.columns[:200], *swap]
    
        trn_data = lgb.Dataset(X_t.values, label=y_t)
        val_data = lgb.Dataset(X_valid.values, label=y_valid)
        evals_result = {}
        lgb_clf = lgb.train(lgb_params,
                        trn_data,
                        110000,
                        valid_sets = [trn_data, val_data],
                        early_stopping_rounds=3500,
                        verbose_eval = 1000,
                        evals_result=evals_result
                       )
        p_valid += lgb_clf.predict(X_valid.values)
        yp += lgb_clf.predict(X_test)
    fold_importance_df = pd.DataFrame()
    fold_importance_df["feature"] = features
    fold_importance_df["importance"] = lgb_clf.feature_importance()
    fold_importance_df["fold"] = fold + 1
    feature_importance_df = pd.concat([feature_importance_df, fold_importance_df], axis=0)
    oof['predict'][val_idx] = p_valid/N
    val_score = roc_auc_score(y_valid, p_valid)
    val_aucs.append(val_score)
    
    predictions['fold{}'.format(fold+1)] = yp/N


# In[ ]:


mean_auc = np.mean(val_aucs)
std_auc = np.std(val_aucs)
all_auc = roc_auc_score(oof['target'], oof['predict'])
print("Mean auc: %.9f, std: %.9f. All auc: %.9f." % (mean_auc, std_auc, all_auc))


# In[ ]:


cols = (feature_importance_df[["feature", "importance"]]
        .groupby("feature")
        .mean()
        .sort_values(by="importance", ascending=False)[:1000].index)
best_features = feature_importance_df.loc[feature_importance_df.feature.isin(cols)]

plt.figure(figsize=(14,26))
sns.barplot(x="importance", y="feature", data=best_features.sort_values(by="importance",ascending=False))
plt.title('LightGBM Features (averaged over folds)')
plt.tight_layout()
plt.savefig('lgbm_importances.png')


# In[ ]:


predictions['target'] = np.mean(predictions[[col for col in predictions.columns if col not in ['ID_code', 'target']]].values, axis=1)
predictions.to_csv('lgb_all_predictions.csv', index=None)
sub_df = pd.DataFrame({"ID_code":extra_test["ID_code"].values})
sub_df["target"] = predictions['target']
sub_df.to_csv("lgb_stats_aug_submission{}.csv".format(num_submission), index=False)
oof.to_csv('lgb_oof.csv', index=False)

