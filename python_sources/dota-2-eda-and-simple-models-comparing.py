#!/usr/bin/env python
# coding: utf-8

# # General information
# This kernel is dedicated to EDA of [Dota 2 Winner Prediction Competition ](https://www.kaggle.com/c/mlcourse-dota2-win-prediction)
# 
# We are provided with prepared data and described features as well as with a lot of "raw" json data. We need to predict winner of the game. 
# Evaluation metric is [ROC-AUC](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc). 
# 
# <left><img src='https://kor.ill.in.ua/m/610x385/1848785.jpg'>

# To simplify you navigation through this kernel: 
# 
# * [Main data exploration](#maindata)
#   * [Target distribution](#Target)
#   * [General features](#Generalfeatures)
#   * [Coordinates features](#Coordinatesfeatures)
#   * [T-SNE on means coordinates features](#TSNE)
#   * [KDA](#KDA)
# * [Models comparison](#simplemodels)
# * [LGBM feature importance](#FeatureImportance)
# * [Submission](#Submission)

# In[ ]:


import os
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, ShuffleSplit, KFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression,Ridge, RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

from lightgbm import LGBMClassifier
import xgboost as xgb
from catboost import CatBoostClassifier

import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set()

import time
import datetime

#import shap
# load JS visualization code to notebook
#shap.initjs()

import warnings
warnings.filterwarnings("ignore")


# In[ ]:


get_ipython().run_cell_magic('time', '', "PATH_TO_DATA = '../input/'\n\nsample_submission = pd.read_csv(os.path.join(PATH_TO_DATA, 'sample_submission.csv'), \n                                    index_col='match_id_hash')\ndf_train_features = pd.read_csv(os.path.join(PATH_TO_DATA, 'train_features.csv'), \n                                    index_col='match_id_hash')\ndf_train_targets = pd.read_csv(os.path.join(PATH_TO_DATA, 'train_targets.csv'), \n                                   index_col='match_id_hash')\ndf_test_features = pd.read_csv(os.path.join(PATH_TO_DATA, 'test_features.csv'), \n                                   index_col='match_id_hash')")


# # Main data exploration
# <div id="maindata">
# </div>
# 
# In this part I'll focus on features created by organizers. 

# In[ ]:


df_train_features.head(3)


# In[ ]:


df_test_features.head(3)


# In[ ]:


df_train_targets.head(3)


# In[ ]:


print('Shape of Training set: {0}\nShape of Test set: {1}'.format(df_train_features.shape,df_test_features.shape))


# So, we have almost 40k entries in train dataset and we need to predict results of other 10k battles.
# 
# ** UPD: ** Thanks to  [@sonfire](https://www.kaggle.com/sonfire), [@ecdrid](https://www.kaggle.com/adityaecdrid) and [@ambisinistra](https://www.kaggle.com/ambisinistra) who helps me to understand some features in `df_train_targets`. <br>
# * `time_remaining` means how much time remains till the end of the game at the point of time at which all characteristics and statistics shown. Indeed, if you'll sum `game_time` and `time_remaining` you receive exactly `duration` of the game. <br>
# * `next_roshan_team` tell us about next team after that point of time which will take roshan.
# 
# Maybe I have to read more about Dota, they have competitions with [prizes](http://dota2.prizetrac.kr/) more than on Kaggle. 
# 
# ![Hm](http://img4.wikia.nocookie.net/__cb20150117182228/plantsvszombies/images/5/57/Wait-what.jpg)
# 
# Just kiddin :) 
# 
# Let's continue, first I'll select target and then divide features on groups and observe them and their correllation with target.

# ## Target 
# <div id="Target">
# As we know ROC-AUC is almost robust to class imbalance but let's see how it's distributed to better understand data: 
# </div>
# 
# 

# In[ ]:


target = pd.Series(df_train_targets['radiant_win'].map({True: 1, False: 0}))


# In[ ]:


plt.hist(target);
plt.title('Target distribution');


# ## General features
# <div id="Generalfeatures">
# </div>

# In[ ]:


general_features = ['game_time', 'game_mode', 'lobby_type', 'objectives_len', 'chat_len']
gen_feat_df = df_train_features[general_features].copy()
gen_feat_df['target'] = target
plt.figure(figsize=(8, 5));
ax = sns.heatmap(gen_feat_df.corr(),annot=True,)


# Just a little notice if you prefer other view of heatmap (check out [documentation](https://seaborn.pydata.org/generated/seaborn.heatmap.html) for more):

# In[ ]:


plt.figure(figsize=(8, 5));
mask = np.zeros_like(gen_feat_df.corr())
mask[np.triu_indices_from(mask)] = True
with sns.axes_style("white"):
    ax = sns.heatmap(gen_feat_df.corr(), mask=mask,annot=True)


# As we see correlation between target and general features is low, which seems to be logical. 
# Game time or type of the game, as far as I know it, shouldn't affect much on winning side. 
# Let's move to more interesting features and first take a look on map: 
# 
# ![Dota 2 Map](https://habrastorage.org/webt/vq/h2/9c/vqh29cm1vd-69blhriyqr98saww.png)
# 
# As description said `The goal is to destroy the opponent's fountain. No draws are possible in Dota 2.` which means that coordinates could be useful.
# Logic is the following: team which is on the enemy fonte at the end of the game won.

# ## Coordinates features
# <div id="Coordinatesfeatures">
# </div>

# In[ ]:


print('Top 10 features correlated with target (abs values):')
print(abs(df_train_features.corrwith(target)).sort_values(ascending=False)[0:10])


# I have no idea why there is no single x coordinate feature in top 10. Who have an idea pleas share in comments! 

# In[ ]:


r_y_coord = ['r{0}_y'.format(i) for i in range(1,6)]
r_x_coord = ['r{0}_x'.format(i) for i in range(1,6)]
r_coord = r_y_coord+r_x_coord

d_y_coord = ['d{0}_y'.format(i) for i in range(1,6)]
d_x_coord = ['d{0}_x'.format(i) for i in range(1,6)]
d_coord = d_y_coord+d_x_coord


# In[ ]:


coord_feat_df = df_train_features[r_coord+d_coord].copy()
coord_feat_df['target'] = target
plt.figure(figsize=(16, 10));
ax = sns.heatmap(coord_feat_df.corr(),annot=True,)


# Here i decided to investigate which exactly values it takes, and was surprised that there is no 0 coordinates: 

# In[ ]:


print('Min y coordinate for Radiant: {0}'.format(coord_feat_df[r_y_coord].min(axis=0).sort_values(ascending=True)[0:1].values))
print('Max y coordinate for Radiant: {0}'.format(coord_feat_df[r_y_coord].max(axis=0).sort_values(ascending=False)[0:1].values)) 
print('Min x coordinate for Radiant: {0}'.format(coord_feat_df[r_x_coord].min(axis=0).sort_values(ascending=True)[0:1].values))
print('Max x coordinate for Radiant: {0}'.format(coord_feat_df[r_x_coord].max(axis=0).sort_values(ascending=False)[0:1].values)) 


# In[ ]:


print('Min y coordinate for Dire: {0}'.format(coord_feat_df[d_y_coord].min(axis=0).sort_values(ascending=True)[0:1].values))
print('Max y coordinate for Dire: {0}'.format(coord_feat_df[d_y_coord].max(axis=0).sort_values(ascending=False)[0:1].values)) 
print('Min x coordinate for Dire: {0}'.format(coord_feat_df[d_x_coord].min(axis=0).sort_values(ascending=True)[0:1].values))
print('Max x coordinate for Dire: {0}'.format(coord_feat_df[d_x_coord].max(axis=0).sort_values(ascending=False)[0:1].values)) 


# It seems that range for y's finishes is: 116 while for x's: 122. 
# This means map is not completely symmetrical. 
# Let's see now how this values differs for Radiant and Dire victories.

# In[ ]:


#https://stackoverflow.com/questions/38783027/jupyter-notebook-display-two-pandas-tables-side-by-side
from IPython.display import display_html 
def display_side_by_side(*args):
    html_str=''
    for df in args:
        html_str+=df.to_html()
    display_html(html_str.replace('table','table style="display:inline"'),raw=True)


# In[ ]:


display_side_by_side(coord_feat_df[coord_feat_df['target']==1].describe().T,coord_feat_df[coord_feat_df['target']==0].describe().T)


# From the correlation table above we see some groups of features. <br>Let's manually unite them using mean.  

# In[ ]:


coord_feat_df_mean = coord_feat_df.copy()
coord_feat_df_mean['target'] = target

coord_feat_df_mean['r_y_mean'] = coord_feat_df_mean[r_y_coord].mean(axis=1)
coord_feat_df_mean['r_x_mean'] = coord_feat_df_mean[r_x_coord].mean(axis=1)
coord_feat_df_mean['d_y_mean'] = coord_feat_df_mean[d_y_coord].mean(axis=1)
coord_feat_df_mean['d_x_mean'] = coord_feat_df_mean[d_x_coord].mean(axis=1)
mean_cols = ['r_y_mean', 'r_x_mean', 'd_y_mean', 'd_x_mean']


# In[ ]:


coord_feat_df_mean.head(3)


# In[ ]:


plt.figure(figsize=(8, 5));
ax = sns.heatmap(coord_feat_df_mean[mean_cols+['target']].corr(),annot=True,)


# Let's now show how this mean coordinates features corresponds with each other and with target

# In[ ]:


sns_plot = sns.pairplot(coord_feat_df_mean[mean_cols+['target']])
sns_plot.savefig('pairplot.png')


# ## T-SNE on means coordinates features
# <div id="TSNE">
# </div>

# In[ ]:


from sklearn.manifold import TSNE


# This take a lot of time. 

# In[ ]:


get_ipython().run_cell_magic('time', '', 'tsne = TSNE(random_state=17)\ntsne_representation = tsne.fit_transform(coord_feat_df_mean[mean_cols]) #https://habr.com/ru/company/ods/blog/323210/')


# In[ ]:


plt.scatter(tsne_representation[:, 0], tsne_representation[:, 1], 
            c=coord_feat_df_mean['target'].map({0: 'blue', 1: 'orange'}));


# We see that points are cross each other, but there are at least 2 clusters which we could see in top left and top right corner. <br>
# Might try to find this 2 clusters based on mean coordinates features. 

# ## KDA (Kills|Deaths|Assists) 
# <div id="KDA">
# </div>

# I will create another separate DataFrame to analyze kills, death and assists.

# In[ ]:


r_kills = ['r{0}_kills'.format(i) for i in range(1,6)]
r_deaths = ['r{0}_deaths'.format(i) for i in range(1,6)]
r_assists = ['r{0}_assists'.format(i) for i in range(1,6)]
r_kda = r_kills+r_deaths+r_assists

d_kills = ['d{0}_kills'.format(i) for i in range(1,6)]
d_deaths = ['d{0}_deaths'.format(i) for i in range(1,6)]
d_assists = ['d{0}_assists'.format(i) for i in range(1,6)]
d_kda = d_kills+d_deaths+d_assists

kda_feat_df = df_train_features[r_kda+d_kda].copy()
kda_feat_df['target'] = target

kda_feat_df['r_tot_kills'] = kda_feat_df[r_kills].sum(axis=1)
kda_feat_df['r_tot_deaths'] = kda_feat_df[r_deaths].sum(axis=1)
kda_feat_df['r_tot_assists'] = kda_feat_df[r_assists].sum(axis=1)

kda_feat_df['d_tot_kills'] = kda_feat_df[d_kills].sum(axis=1)
kda_feat_df['d_tot_deaths'] = kda_feat_df[d_deaths].sum(axis=1)
kda_feat_df['d_tot_assists'] = kda_feat_df[d_assists].sum(axis=1)

tot_cols = ['r_tot_kills', 'r_tot_deaths', 'r_tot_assists', 'd_tot_kills', 'd_tot_deaths', 'd_tot_assists']

display(kda_feat_df.head(3))


# In[ ]:


plt.figure(figsize=(8, 5));
ax = sns.heatmap(kda_feat_df[tot_cols+['target']].corr(),annot=True,)


# KDA in dota is [calculated](https://steamcommunity.com/app/570/discussions/0/3307213006841396427/ ) as: (K+A)/D 
# 

# In[ ]:


kda_feat_df['r_kda'] = (kda_feat_df['r_tot_kills']+kda_feat_df['r_tot_assists'])/kda_feat_df['r_tot_deaths']
kda_feat_df['d_kda'] = (kda_feat_df['d_tot_kills']+kda_feat_df['d_tot_assists'])/kda_feat_df['d_tot_deaths']


# In[ ]:


plt.figure(figsize=(4.8, 3));
ax = sns.heatmap(kda_feat_df[['r_kda','d_kda','target']].corr(),annot=True,)


# Other feauteres could be analyzed in the same way. <br>
# Even more data is stored in JSON files. <br>
# Now let's implement and compare few models. 

# # Simple models comparison
# <div id="simplemodels">
# First, I am preparing data for learning and setting cross validation
# </div>

# In[ ]:


X = df_train_features
y = df_train_targets['radiant_win']
X_test = df_test_features
y_cat = pd.Series(df_train_targets['radiant_win'].map({True: 1, False: 0})) #catboost doesn't understand True,False 
#X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.3, random_state=17) #for holdout, don't use in kernel
n_fold = 5
folds = KFold(n_splits=n_fold, shuffle=True, random_state=11)
cv = ShuffleSplit(n_splits=n_fold, test_size=0.3, random_state=17) #same as in https://www.kaggle.com/c/mlcourse-dota2-win-prediction/kernels starter kernel 


# And now will use following models without hyperparams: 
# 
# RF, LGBM, XGB, CatBoost

# In[ ]:


get_ipython().run_cell_magic('time', '', "\nmodel_rf = RandomForestClassifier(n_estimators=100, n_jobs=4,\n                                   max_depth=None, random_state=17)\n\n# calcuate ROC-AUC for each split\ncv_scores_rf = cross_val_score(model_rf, X, y, cv=cv, scoring='roc_auc')")


# In[ ]:


get_ipython().run_cell_magic('time', '', "\nmodel_lgb = LGBMClassifier(random_state=17)\ncv_scores_lgb = cross_val_score(model_lgb, X, y, cv=cv, \n                                scoring='roc_auc', n_jobs=4)")


# In[ ]:


get_ipython().run_cell_magic('time', '', "\nmodel_xgb = xgb.XGBClassifier(random_state=17)\ncv_scores_xgb = cross_val_score(model_xgb, X, y, cv=cv,\n                                scoring='roc_auc', n_jobs=4)")


# Next cell runs ~ 13 min (it freezes completely with n_jobs not equal to 1 for unknown reason). <br>
# It's definitely better and faster to use native CatBoost CV than `sklearn` one. <br>
# You could check my [kernel](https://www.kaggle.com/vchulski/catboost-and-shap-for-dota-2-winner-prediction) dedicated to CatBoost.

# In[ ]:


get_ipython().run_cell_magic('time', '', "model_cat = CatBoostClassifier(random_state=17,silent=True)\ncv_scores_cat = cross_val_score(model_cat, X, y_cat, cv=cv,\n                                scoring='roc_auc', n_jobs=1) #pay attention n_jobs=1 here, just freezes with any other value")


# In[ ]:


cv_results = pd.DataFrame(data={'RF': cv_scores_rf, 'LGB':cv_scores_lgb, 'XGB':cv_scores_xgb, 'CAT':cv_scores_cat})
display_side_by_side(cv_results, cv_results.describe())


# As we see CatBoost gives best results among tested algorithms - but it's very rough comparison.After adding hyperparams this could change.
# Anyway, this gives some hint which models we definetly should try. 
# 
# Also, we see how fast LGBM is. I am not counting CatBoost which I will test later, but it's even 2 times faster than RF. 

# # Feature Importance
# <div id="FeatureImportance">
# </div>

# In[ ]:


#just visit https://lightgbm.readthedocs.io/en/latest/Parameters-Tuning.html
#https://medium.com/@pushkarmandot/https-medium-com-pushkarmandot-what-is-lightgbm-how-to-implement-it-how-to-fine-tune-the-parameters-60347819b7fc
params = {#'num_leaves': 31, # number of leaves in full tree (31 by default) 
         'learning_rate': 0.01, #this determines the impact of each tree on the final outcome. 

         'min_data_in_leaf': 50,
         'min_sum_hessian_in_leaf': 12.0,
         'objective': 'binary', 
         'max_depth': -1,
         'boosting': 'gbdt', #'dart' 
         'bagging_freq': 5,
         'bagging_fraction': 0.81,
         'boost_from_average':'false',
         'bagging_seed': 17,
         'metric': 'auc',
         'verbosity': -1,
         }


# In[ ]:


get_ipython().run_cell_magic('time', '', '# this part is based on great kernel https://www.kaggle.com/artgor/seismic-data-eda-and-baseline by @artgor\noof = np.zeros(len(X))\nprediction = np.zeros(len(X_test))\nscores = []\nfeature_importance = pd.DataFrame()\nfor fold_n, (train_index, valid_index) in enumerate(folds.split(X, y)):\n    print(\'Fold\', fold_n, \'started at\', time.ctime())\n    X_train, X_valid = X.iloc[train_index], X.iloc[valid_index]\n    y_train, y_valid = y.iloc[train_index], y.iloc[valid_index]\n    \n    model = LGBMClassifier(**params, n_estimators = 2000, nthread = 5, n_jobs = -1)\n    model.fit(X_train, y_train, \n              eval_set=[(X_train, y_train), (X_valid, y_valid)], eval_metric=\'auc\',\n              verbose=200, early_stopping_rounds=200)\n            \n    y_pred_valid = model.predict_proba(X_valid)[:, 1]\n    y_pred = model.predict_proba(X_test, num_iteration=model.best_iteration_)[:, 1]\n        \n    oof[valid_index] = y_pred_valid.reshape(-1,)\n    scores.append(roc_auc_score(y_valid, y_pred_valid))\n    prediction += y_pred    \n    \n    # feature importance\n    fold_importance = pd.DataFrame()\n    fold_importance["feature"] = X.columns\n    fold_importance["importance"] = model.feature_importances_\n    fold_importance["fold"] = fold_n + 1\n    feature_importance = pd.concat([feature_importance, fold_importance], axis=0)\n\nprediction /= n_fold')


# In[ ]:


print('CV mean score: {0:.4f}, std: {1:.4f}.'.format(np.mean(scores), np.std(scores)))
    
feature_importance["importance"] /= n_fold
    
cols = feature_importance[["feature", "importance"]].groupby("feature").mean().sort_values(
            by="importance", ascending=False)[:50].index

best_features = feature_importance.loc[feature_importance.feature.isin(cols)]

plt.figure(figsize=(14, 16));
sns.barplot(x="importance", y="feature", data=best_features.sort_values(by="importance", ascending=False));
plt.title('LGB Features (avg over folds)');


# Now it seems that gold is main feature in the game. 
# 
# But pay attention, results can be different based on parameters. 
# Check out [this](https://www.kaggle.com/shokhan/lightgbm-starter-code) kernel for instance. 

# # Submission
# <div id="Submission">
# </div>

# I won't share blend solution and that's why I will public simple LGB with almost random parameters, but I bet you will do better than me :)

# In[ ]:


lgb = LGBMClassifier(random_state=17)
lgb.fit(X, y)

X_test = df_test_features.values
y_test_pred = lgb.predict_proba(X_test)[:, 1]
df_submission = pd.DataFrame({'radiant_win_prob': y_test_pred}, 
                                 index=df_test_features.index)
submission_filename = 'lgb_{}.csv'.format(
    datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))
df_submission.to_csv(submission_filename)
print('Submission saved to {}'.format(submission_filename))


# In[ ]:


df_submission.head() #just to check that everything allright 


# It's my first ever public kernel on Kaggle so any feedback is appreciated.
