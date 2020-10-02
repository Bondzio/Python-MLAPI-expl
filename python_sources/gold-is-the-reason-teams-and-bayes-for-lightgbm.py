#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm_notebook
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from tqdm import tqdm_notebook
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


import warnings
warnings.filterwarnings("ignore")


# This notebook is about two things:<br>
# 1. We have different fields for ordered list of characters. In fact, the order os heroes is not importent. So I want to make features for team, deleting the order
# 2. I will tune parameters for LightGBM with the help of baesian optimisation. Very pretty way
# 
# There is no real feature engeneering here. It is coming soon...

# ### Load the data

# In[ ]:


train_data = pd.read_csv('../input/train_features.csv', index_col='match_id_hash')
test_data = pd.read_csv('../input/test_features.csv', index_col='match_id_hash')
y_train = pd.read_csv('../input/train_targets.csv', index_col='match_id_hash')['radiant_win'].map({True: 1, False:0})


# We have fields for each hero. Hmmm. I want to aggregate them

# In[ ]:


train_data.head()


# ### Make team features

# This is the function to make one_hot_encoding for heroes in whole team

# In[ ]:


def hero_dammies(X_train, X_test, let):
    r_cols = [let +'%s_hero_id' %i for i in range(1, 6)]
    X = pd.concat([X_train, X_test])
    X['herois'+ let] = X.apply(lambda row: ' '.join(row.loc[r_cols].map(int).map(str)), axis=1)
    cvv = CountVectorizer()
    heroes = pd.DataFrame(cvv.fit_transform(X['herois'+let]).todense(), columns=cvv.get_feature_names(), index=X.index)
    return heroes.loc[X_train.index], heroes.loc[X_test.index]


# Let's do it! We get heroes for Radiant and Dire team in separated tables

# In[ ]:


train_r, test_r = hero_dammies(train_data, test_data, 'r')
train_d, test_d = hero_dammies(train_data, test_data, 'd')


# Now we want to find a way to count aggregate features for teams. Let's try to find the way to do this. I think it looks like good to use mean, max and min for each parameter.

# In[ ]:


X_train = train_data[['game_time', 'game_mode', 'lobby_type', 'objectives_len', 'chat_len']].copy()

mean_cols = ['kills','deaths', 'assists','denies','gold', 'lh','xp','health','max_health','max_mana', 'level', 'stuns','creeps_stacked', 'camps_stacked', 'rune_pickups', 'firstblood_claimed','teamfight_participation',
'towers_killed', 'roshans_killed', 'obs_placed', 'sen_placed']

for col in tqdm_notebook(mean_cols):
    for let in ['r','d']:
        full_cols = [x+col for x in [let +'%s_' %i for i in range(1, 6)]]
        X_train[let+col+'_mean'] = train_data[full_cols].apply(np.mean, axis=1)
        X_train[let+col+'_max'] = train_data[full_cols].apply(np.max, axis=1)
        X_train[let+col+'_min'] = train_data[full_cols].apply(np.min, axis=1)

X_test = test_data[['game_time', 'game_mode', 'lobby_type', 'objectives_len', 'chat_len']].copy()
for col in tqdm_notebook(mean_cols):
    for let in ['r','d']:
        full_cols = [x+col for x in [let +'%s_' %i for i in range(1, 6)]]
        X_test[let+col+'_mean'] = test_data[full_cols].apply(np.mean, axis=1)
        X_test[let+col+'_max'] = test_data[full_cols].apply(np.max, axis=1)
        X_test[let+col+'_min'] = test_data[full_cols].apply(np.min, axis=1)


# Last step - we gather all this data to dataset

# In[ ]:


X_train = X_train.join(train_r, rsuffix='_r').join(train_d, rsuffix='_d')

X_test = X_test.join(test_r, rsuffix='_r').join(test_d, rsuffix='_d')


# ### Parameters tuning for LightGBM

# In[ ]:


import lightgbm
from bayes_opt import BayesianOptimization


# We can find the way to choose parameters in docs:
# 
# https://lightgbm.readthedocs.io/en/latest/Parameters-Tuning.html
# 
# Thanks to this kernel: https://www.kaggle.com/qwe1398775315/eda-lgbm-bayesianoptimization

# In[ ]:


def lgb_eval(num_leaves,max_depth,lambda_l2,lambda_l1,min_child_samples, min_data_in_leaf):
    params = {
    "objective" : "binary",
    "metric" : "auc", 
    'is_unbalance': True,
    "num_leaves" : int(num_leaves),
    "max_depth" : int(max_depth),
    "lambda_l2" : lambda_l2,
    "lambda_l1" : lambda_l1,
    "num_threads" : 20,
    "min_child_samples" : int(min_child_samples),
    'min_data_in_leaf': int(min_data_in_leaf),
    "learning_rate" : 0.03,
    "subsample_freq" : 5,
    "bagging_seed" : 42,
    "verbosity" : -1
    }
    
    lgtrain = lightgbm.Dataset(X_train, y_train,categorical_feature=categorical_features)
    cv_result = lightgbm.cv(params,
                       lgtrain,
                       10000,
                       early_stopping_rounds=300,
                       stratified=True,
                       nfold=5)
    return cv_result['auc-mean'][-1]

def lgb_train(num_leaves,max_depth,lambda_l2,lambda_l1,min_child_samples, min_data_in_leaf):
    params = {
    "objective" : "binary",
    "metric" : "auc", 
    'is_unbalance': True,
    "num_leaves" : int(num_leaves),
    "max_depth" : int(max_depth),
    "lambda_l2" : lambda_l2,
    "lambda_l1" : lambda_l1,
    "num_threads" : 20,
    "min_child_samples" : int(min_child_samples),
    'min_data_in_leaf': int(min_data_in_leaf),
    "learning_rate" : 0.03,
    "subsample_freq" : 5,
    "bagging_seed" : 42,
    "verbosity" : -1
    }
    t_x,v_x,t_y,v_y = train_test_split(X_train, y_train,test_size=0.2)
    lgtrain = lightgbm.Dataset(t_x, t_y,categorical_feature=categorical_features)
    lgvalid = lightgbm.Dataset(v_x, v_y,categorical_feature=categorical_features)
    model = lightgbm.train(params, lgtrain, 4000, valid_sets=[lgvalid], early_stopping_rounds=400, verbose_eval=200)
    pred_test_y = model.predict(X_test, num_iteration=model.best_iteration)
    return pred_test_y, model
    
def param_tuning(init_points,num_iter,**args):
    lgbBO = BayesianOptimization(lgb_eval, {'num_leaves': (15, 200),
                                                'max_depth': (5, 63),
                                                'lambda_l2': (0.0, 5),
                                                'lambda_l1': (0.0, 5),
                                                'min_child_samples': (50, 5000),
                                                'min_data_in_leaf': (50, 300)
                                                })

    lgbBO.maximize(init_points=init_points, n_iter=num_iter,**args)
    return lgbBO


# In[ ]:


categorical_features= ['lobby_type', 'game_mode']


# In[ ]:


result = param_tuning(10,50)


# In[ ]:


params = result.max['params']
params


# We run learning for 3 times and take the mean value of predictions.

# In[ ]:


pred_test_y1, _ = lgb_train(**params)
pred_test_y2, _ = lgb_train(**params)
pred_test_y3, model = lgb_train(**params)
y_pred = (pred_test_y1 + pred_test_y2 + pred_test_y3)/3


# It is just a beginning! 

# In[ ]:


feature_importance = pd.DataFrame({'feature': X_train.columns, 'importance':model.feature_importance()}).sort_values('importance', ascending=False)[:100]

plt.figure(figsize=(14,28))
sns.barplot(x=feature_importance.importance, y=feature_importance.feature);


# The main thing is gold ;)

# In[1]:


df_submission_extended = pd.DataFrame(
    {'radiant_win_prob': y_pred}, 
    index=test_data.index)
df_submission_extended.to_csv('submission.csv')


# In[ ]:




