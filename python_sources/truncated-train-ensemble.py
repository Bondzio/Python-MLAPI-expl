#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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
from time import time
from tqdm import tqdm_notebook as tqdm
from collections import Counter
from scipy import stats
import lightgbm as lgb
from sklearn.metrics import cohen_kappa_score, mean_squared_error
from sklearn.model_selection import GroupKFold, KFold
import gc
import json
pd.set_option('display.max_columns', 1000)
from sklearn import metrics
import warnings
warnings.filterwarnings('ignore')
import random


# # Objective

# Truncate train set and perform an ensemble. When you truncate the training set the adversarial validation auc roc is 0.5 (aprox), test set is also truncated (don't know about private, it should be the same). This notebook shows how we can truncate the train set a lot of times (get 1 observation of each installation id random) and train 20 models and then take the average of their predictions.
# 
# * This method aligns well with the lb. Check mean cv score for the 20 models and the lb(we have a lower cohen kappa cv)

# In[ ]:


def read_data():
    print('Reading train.csv file....')
    train = pd.read_csv('/kaggle/input/data-science-bowl-2019/train.csv')
    print('Training.csv file have {} rows and {} columns'.format(train.shape[0], train.shape[1]))

    print('Reading test.csv file....')
    test = pd.read_csv('/kaggle/input/data-science-bowl-2019/test.csv')
    print('Test.csv file have {} rows and {} columns'.format(test.shape[0], test.shape[1]))

    print('Reading train_labels.csv file....')
    train_labels = pd.read_csv('/kaggle/input/data-science-bowl-2019/train_labels.csv')
    print('Train_labels.csv file have {} rows and {} columns'.format(train_labels.shape[0], train_labels.shape[1]))

    print('Reading specs.csv file....')
    specs = pd.read_csv('/kaggle/input/data-science-bowl-2019/specs.csv')
    print('Specs.csv file have {} rows and {} columns'.format(specs.shape[0], specs.shape[1]))

    print('Reading sample_submission.csv file....')
    sample_submission = pd.read_csv('/kaggle/input/data-science-bowl-2019/sample_submission.csv')
    print('Sample_submission.csv file have {} rows and {} columns'.format(sample_submission.shape[0], sample_submission.shape[1]))
    return train, test, train_labels, specs, sample_submission


# In[ ]:


def encode_title(train, test, train_labels):
    # encode title
    train['title_event_code'] = list(map(lambda x, y: str(x) + '_' + str(y), train['title'], train['event_code']))
    test['title_event_code'] = list(map(lambda x, y: str(x) + '_' + str(y), test['title'], test['event_code']))
    all_title_event_code = list(set(train["title_event_code"].unique()).union(test["title_event_code"].unique()))
    # make a list with all the unique 'titles' from the train and test set
    list_of_user_activities = list(set(train['title'].unique()).union(set(test['title'].unique())))
    # make a list with all the unique 'event_code' from the train and test set
    list_of_event_code = list(set(train['event_code'].unique()).union(set(test['event_code'].unique())))
    list_of_event_id = list(set(train['event_id'].unique()).union(set(test['event_id'].unique())))
    # make a list with all the unique worlds from the train and test set
    list_of_worlds = list(set(train['world'].unique()).union(set(test['world'].unique())))
    # create a dictionary numerating the titles
    activities_map = dict(zip(list_of_user_activities, np.arange(len(list_of_user_activities))))
    activities_labels = dict(zip(np.arange(len(list_of_user_activities)), list_of_user_activities))
    activities_world = dict(zip(list_of_worlds, np.arange(len(list_of_worlds))))
    assess_titles = list(set(train[train['type'] == 'Assessment']['title'].value_counts().index).union(set(test[test['type'] == 'Assessment']['title'].value_counts().index)))
    # replace the text titles with the number titles from the dict
    train['title'] = train['title'].map(activities_map)
    test['title'] = test['title'].map(activities_map)
    train['world'] = train['world'].map(activities_world)
    test['world'] = test['world'].map(activities_world)
    train_labels['title'] = train_labels['title'].map(activities_map)
    win_code = dict(zip(activities_map.values(), (4100*np.ones(len(activities_map))).astype('int')))
    # then, it set one element, the 'Bird Measurer (Assessment)' as 4110, 10 more than the rest
    win_code[activities_map['Bird Measurer (Assessment)']] = 4110
    # convert text into datetime
    train['timestamp'] = pd.to_datetime(train['timestamp'])
    test['timestamp'] = pd.to_datetime(test['timestamp'])
    return train, test, train_labels, win_code, list_of_user_activities, list_of_event_code, activities_labels, assess_titles, list_of_event_id, all_title_event_code


# In[ ]:


def get_data(user_sample, test_set=False):
    '''
    The user_sample is a DataFrame from train or test where the only one 
    installation_id is filtered
    And the test_set parameter is related with the labels processing, that is only requered
    if test_set=False
    '''
    # Constants and parameters declaration
    last_activity = 0
    
    user_activities_count = {'Clip':0, 'Activity': 0, 'Assessment': 0, 'Game':0}
    
    # new features: time spent in each activity
    last_session_time_sec = 0
    accuracy_groups = {0:0, 1:0, 2:0, 3:0}
    all_assessments = []
    accumulated_accuracy_group = 0
    accumulated_accuracy = 0
    accumulated_correct_attempts = 0 
    accumulated_uncorrect_attempts = 0
    accumulated_actions = 0
    counter = 0
    time_first_activity = float(user_sample['timestamp'].values[0])
    durations = []
    last_accuracy_title = {'acc_' + title: -1 for title in assess_titles}
    last_game_time_title = {'lgt_' + title: 0 for title in assess_titles}
    ac_game_time_title = {'agt_' + title: 0 for title in assess_titles}
    ac_true_attempts_title = {'ata_' + title: 0 for title in assess_titles}
    ac_false_attempts_title = {'afa_' + title: 0 for title in assess_titles}
    event_code_count: Dict[str, int] = {ev: 0 for ev in list_of_event_code}
    event_id_count: Dict[str, int] = {eve: 0 for eve in list_of_event_id}
    title_count: Dict[str, int] = {eve: 0 for eve in activities_labels.values()} 
    title_event_code_count: Dict[str, int] = {t_eve: 0 for t_eve in all_title_event_code}
    
    # itarates through each session of one instalation_id
    for i, session in user_sample.groupby('game_session', sort=False):
        # i = game_session_id
        # session is a DataFrame that contain only one game_session
        
        # get some sessions information
        session_type = session['type'].iloc[0]
        session_title = session['title'].iloc[0]
        session_title_text = activities_labels[session_title]
                    
            
        # for each assessment, and only this kind off session, the features below are processed
        # and a register are generated
        if (session_type == 'Assessment') & (test_set or len(session)>1):
            # search for event_code 4100, that represents the assessments trial
            all_attempts = session.query(f'event_code == {win_code[session_title]}')
            # then, check the numbers of wins and the number of losses
            true_attempts = all_attempts['event_data'].str.contains('true').sum()
            false_attempts = all_attempts['event_data'].str.contains('false').sum()
            # copy a dict to use as feature template, it's initialized with some itens: 
            # {'Clip':0, 'Activity': 0, 'Assessment': 0, 'Game':0}
            features = user_activities_count.copy()
            features.update(last_accuracy_title.copy())
            features.update(event_code_count.copy())
            features.update(title_count.copy())
            features.update(event_id_count.copy())
            features.update(title_event_code_count.copy())
            features.update(last_game_time_title.copy())
            features.update(ac_game_time_title.copy())
            features.update(ac_true_attempts_title.copy())
            features.update(ac_false_attempts_title.copy())
            # get installation_id for aggregated features
            features['installation_id'] = session['installation_id'].iloc[-1]
            # add title as feature, remembering that title represents the name of the game
            features['session_title'] = session['title'].iloc[0]
            # the 4 lines below add the feature of the history of the trials of this player
            # this is based on the all time attempts so far, at the moment of this assessment
            features['accumulated_correct_attempts'] = accumulated_correct_attempts
            features['accumulated_uncorrect_attempts'] = accumulated_uncorrect_attempts
            accumulated_correct_attempts += true_attempts 
            accumulated_uncorrect_attempts += false_attempts
            
            # ----------------------------------------------
            ac_true_attempts_title['ata_' + session_title_text] += true_attempts
            ac_false_attempts_title['afa_' + session_title_text] += false_attempts
            
            
            last_game_time_title['lgt_' + session_title_text] = session['game_time'].iloc[-1]
            ac_game_time_title['agt_' + session_title_text] += session['game_time'].iloc[-1]
            # ----------------------------------------------
            
            # the time spent in the app so far
            if durations == []:
                features['duration_mean'] = 0
            else:
                features['duration_mean'] = np.mean(durations)
            durations.append((session.iloc[-1, 2] - session.iloc[0, 2] ).seconds)
            # the accurace is the all time wins divided by the all time attempts
            features['accumulated_accuracy'] = accumulated_accuracy/counter if counter > 0 else 0
            accuracy = true_attempts/(true_attempts+false_attempts) if (true_attempts+false_attempts) != 0 else 0
            accumulated_accuracy += accuracy
            last_accuracy_title['acc_' + session_title_text] = accuracy
            # a feature of the current accuracy categorized
            # it is a counter of how many times this player was in each accuracy group
            if accuracy == 0:
                features['accuracy_group'] = 0
            elif accuracy == 1:
                features['accuracy_group'] = 3
            elif accuracy == 0.5:
                features['accuracy_group'] = 2
            else:
                features['accuracy_group'] = 1
            features.update(accuracy_groups)
            accuracy_groups[features['accuracy_group']] += 1
            # mean of the all accuracy groups of this player
            features['accumulated_accuracy_group'] = accumulated_accuracy_group/counter if counter > 0 else 0
            accumulated_accuracy_group += features['accuracy_group']
            # how many actions the player has done so far, it is initialized as 0 and updated some lines below
            features['accumulated_actions'] = accumulated_actions
            
            # there are some conditions to allow this features to be inserted in the datasets
            # if it's a test set, all sessions belong to the final dataset
            # it it's a train, needs to be passed throught this clausule: session.query(f'event_code == {win_code[session_title]}')
            # that means, must exist an event_code 4100 or 4110
            if test_set:
                all_assessments.append(features)
            elif true_attempts+false_attempts > 0:
                all_assessments.append(features)
                
            counter += 1
        
        # this piece counts how many actions was made in each event_code so far
        def update_counters(counter: dict, col: str):
                num_of_session_count = Counter(session[col])
                for k in num_of_session_count.keys():
                    x = k
                    if col == 'title':
                        x = activities_labels[k]
                    counter[x] += num_of_session_count[k]
                return counter
            
        event_code_count = update_counters(event_code_count, "event_code")
        event_id_count = update_counters(event_id_count, "event_id")
        title_count = update_counters(title_count, 'title')
        title_event_code_count = update_counters(title_event_code_count, 'title_event_code')

        # counts how many actions the player has done so far, used in the feature of the same name
        accumulated_actions += len(session)
        if last_activity != session_type:
            user_activities_count[session_type] += 1
            last_activitiy = session_type 
                        
    # if it't the test_set, only the last assessment must be predicted, the previous are scraped
    if test_set:
        return all_assessments[-1]
    # in the train_set, all assessments goes to the dataset
    return all_assessments


# In[ ]:


def get_train_and_test(train, test):
    compiled_train = []
    compiled_test = []
    for i, (ins_id, user_sample) in tqdm(enumerate(train.groupby('installation_id', sort = False)), total = 17000):
        compiled_train += get_data(user_sample)
    for ins_id, user_sample in tqdm(test.groupby('installation_id', sort = False), total = 1000):
        test_data = get_data(user_sample, test_set = True)
        compiled_test.append(test_data)
    reduce_train = pd.DataFrame(compiled_train)
    reduce_test = pd.DataFrame(compiled_test)
    categoricals = ['session_title']
    return reduce_train, reduce_test, categoricals


# In[ ]:


# thank to Bruno
def eval_qwk_lgb_regr(y_pred, train_t):
    """
    Fast cappa eval function for lgb.
    """
    dist = Counter(train_t['accuracy_group'])
    for k in dist:
        dist[k] /= len(train_t)
    
    acum = 0
    bound = {}
    for i in range(3):
        acum += dist[i]
        bound[i] = np.percentile(y_pred, acum * 100)

    def classify(x):
        if x <= bound[0]:
            return 0
        elif x <= bound[1]:
            return 1
        elif x <= bound[2]:
            return 2
        else:
            return 3

    y_pred = np.array(list(map(classify, y_pred)))
    
    return y_pred


def predict(sample_submission, y_pred):
    
    """
    Fast cappa eval function for lgb.
    """
    dist = Counter(reduce_train['accuracy_group'])
    for k in dist:
        dist[k] /= len(reduce_train)
    
    acum = 0
    bound = {}
    for i in range(3):
        acum += dist[i]
        bound[i] = np.percentile(y_pred, acum * 100)

    def classify(x):
        if x <= bound[0]:
            return 0
        elif x <= bound[1]:
            return 1
        elif x <= bound[2]:
            return 2
        else:
            return 3

    y_pred = np.array(list(map(classify, y_pred)))

    sample_submission['accuracy_group'] = y_pred
    sample_submission['accuracy_group'] = sample_submission['accuracy_group'].astype(int)
    sample_submission.to_csv('submission.csv', index = False)
    print(sample_submission['accuracy_group'].value_counts(normalize = True))


# In[ ]:


def get_random_assessment(reduce_train):
    used_idx = []
    for iid in tqdm(set(reduce_train['installation_id'])):
        list_ = list(reduce_train[reduce_train['installation_id']==iid].index)
        cur = random.choices(list_, k = 1)[0]
        used_idx.append(cur)
    reduce_train_t = reduce_train.loc[used_idx].reset_index(drop = True)
    return reduce_train_t


# In[ ]:


def run_lgb(reduce_train, reduce_test, features):
    
    # features found in initial bayesian optimization
    params = {'boosting_type': 'gbdt', 
              'metric': 'rmse', 
              'objective': 'regression', 
              'n_jobs': -1, 
              'seed': 42, 
              'num_leavs': 21, 
              'learning_rate': 0.027091035494468625, 
              'max_depth': 22, 
              'lambda_l1': 0.0609996908935434, 
              'lambda_l2': 1.0970788941187797, 
              'bagging_fraction': 0.7525277174040448, 
              'bagging_freq': 1, 
              'colsample_bytree': 0.8488159181363383}
    
    # define a GroupKFold strategy because we are predicting unknown installation_ids
    kf = GroupKFold(n_splits = 5)
    target = 'accuracy_group'
    oof_pred = np.zeros(len(reduce_train))
    y_pred = np.zeros(len(reduce_test))
    
    # train a baseline model and record the cohen cappa score as our best score
    for fold, (tr_ind, val_ind) in enumerate(kf.split(reduce_train, groups = reduce_train['installation_id'])):
        print('Fold:', fold + 1)
        x_train, x_val = reduce_train[features].iloc[tr_ind], reduce_train[features].iloc[val_ind]
        y_train, y_val = reduce_train[target][tr_ind], reduce_train[target][val_ind]
        train_set = lgb.Dataset(x_train, y_train, categorical_feature = ['session_title'])
        val_set = lgb.Dataset(x_val, y_val, categorical_feature = ['session_title'])
        
        model = lgb.train(params, train_set, num_boost_round = 100000, early_stopping_rounds = 100, 
                         valid_sets = [train_set, val_set], verbose_eval = 100)
        
        oof_pred[val_ind] = model.predict(x_val)
        y_pred += model.predict(reduce_test[features]) / kf.n_splits
        
    # calculate loss
    oof_rmse_score = np.sqrt(mean_squared_error(reduce_train[target], oof_pred))
    oof_cohen_score = cohen_kappa_score(reduce_train[target], eval_qwk_lgb_regr(oof_pred, reduce_train), weights = 'quadratic')
    print('Our oof rmse score is:', oof_rmse_score)
    print('Our oof cohen kappa score is:', oof_cohen_score)
    
    return y_pred, oof_rmse_score, oof_cohen_score


# In[ ]:


# read data
train, test, train_labels, specs, sample_submission = read_data()
# get usefull dict with maping encode
train, test, train_labels, win_code, list_of_user_activities, list_of_event_code, activities_labels, assess_titles, list_of_event_id, all_title_event_code = encode_title(train, test, train_labels)
# tranform function to get the train and test set
reduce_train, reduce_test, categoricals = get_train_and_test(train, test)


# In[ ]:


# extracted from feature elimination first round script
old_features = ['Activity', 'Assessment', 'Clip', 'Game', 'acc_Bird Measurer (Assessment)', 'acc_Cart Balancer (Assessment)', 
                'acc_Cauldron Filler (Assessment)', 'acc_Chest Sorter (Assessment)', 'acc_Mushroom Sorter (Assessment)', 2050, 
                4100, 2060, 4110, 2070, 2075, 2080, 2081, 2083, 3110, 3120, 3121, 4220, 4230, 5000, 4235, 5010, 4010, 4020, 
                4021, 4022, 4025, 4030, 4031, 3010, 4035, 4040, 3020, 3021, 4045, 2000, 4050, 2010, 2020, 4070, 2025, 2030, 
                4080, 2035, 2040, 4090, 4095, 'Cauldron Filler (Assessment)', 'Leaf Leader', 'Welcome to Lost Lagoon!', 
                'Lifting Heavy Things', 'Sandcastle Builder (Activity)', 'Crystal Caves - Level 3', 
                'Chest Sorter (Assessment)', 'Crystal Caves - Level 2', 'Slop Problem', 'Magma Peak - Level 2', 
                'All Star Sorting', 'Chow Time', 'Tree Top City - Level 1', 'Fireworks (Activity)', 'Dino Dive', 
                'Scrub-A-Dub', 'Tree Top City - Level 2', 'Bug Measurer (Activity)', 'Crystals Rule', 
                'Flower Waterer (Activity)', 'Tree Top City - Level 3', 'Crystal Caves - Level 1', "Pirate's Tale", 
                'Watering Hole (Activity)', 'Bird Measurer (Assessment)', 'Treasure Map', 'Happy Camel', 
                'Chicken Balancer (Activity)', 'Dino Drink', 'Air Show', 'Mushroom Sorter (Assessment)', 'Ordering Spheres', 
                'Cart Balancer (Assessment)', 'Rulers', 'Bubble Bath', 'Balancing Act', 'Bottle Filler (Activity)', 
                'Honey Cake', '12 Monkeys', 'Pan Balance', 'Costume Box', 'Egg Dropper (Activity)', 'Magma Peak - Level 1', 
                'lgt_Mushroom Sorter (Assessment)', 'lgt_Cauldron Filler (Assessment)', 'lgt_Cart Balancer (Assessment)', 
                'lgt_Bird Measurer (Assessment)', 'lgt_Chest Sorter (Assessment)', 'agt_Mushroom Sorter (Assessment)', 
                'agt_Cauldron Filler (Assessment)', 'agt_Cart Balancer (Assessment)', 'agt_Bird Measurer (Assessment)', 
                'agt_Chest Sorter (Assessment)', 'ata_Mushroom Sorter (Assessment)', 'ata_Cauldron Filler (Assessment)', 
                'ata_Cart Balancer (Assessment)', 'ata_Bird Measurer (Assessment)', 'ata_Chest Sorter (Assessment)', 
                'afa_Mushroom Sorter (Assessment)', 'afa_Cauldron Filler (Assessment)', 'afa_Cart Balancer (Assessment)', 
                'afa_Bird Measurer (Assessment)', 'afa_Chest Sorter (Assessment)', 'session_title', 
                'accumulated_correct_attempts', 'accumulated_uncorrect_attempts', 'duration_mean', 'accumulated_accuracy', 
                0, 1, 2, 3, 'accumulated_accuracy_group', 'accumulated_actions']

event_id_features = list(reduce_train.columns[95:479])
title_event_code_cross = list(reduce_train.columns[479:882])
features = old_features + event_id_features + title_event_code_cross

def remove_correlated_features(reduce_train):
    counter = 0
    to_remove = []
    for feat_a in features:
        for feat_b in features:
            if feat_a != feat_b and feat_a not in to_remove and feat_b not in to_remove:
                c = np.corrcoef(reduce_train[feat_a], reduce_train[feat_b])[0][1]
                if c > 0.995:
                    counter += 1
                    to_remove.append(feat_b)
                    print('{}: FEAT_A: {} FEAT_B: {} - Correlation: {}'.format(counter, feat_a, feat_b, c))
    return to_remove
to_remove = remove_correlated_features(reduce_train)
features = [col for col in features if col not in to_remove]
features = [col for col in features if col not in ['Heavy, Heavier, Heaviest_2000']]
print('Training with {} features'.format(len(features)))


# In[ ]:


reduce_train_t_1 = get_random_assessment(reduce_train)
reduce_train_t_2 = get_random_assessment(reduce_train)
reduce_train_t_3 = get_random_assessment(reduce_train)
reduce_train_t_4 = get_random_assessment(reduce_train)
reduce_train_t_5 = get_random_assessment(reduce_train)
reduce_train_t_6 = get_random_assessment(reduce_train)
reduce_train_t_7 = get_random_assessment(reduce_train)
reduce_train_t_8 = get_random_assessment(reduce_train)
reduce_train_t_9 = get_random_assessment(reduce_train)
reduce_train_t_10 = get_random_assessment(reduce_train)
reduce_train_t_11 = get_random_assessment(reduce_train)
reduce_train_t_12 = get_random_assessment(reduce_train)
reduce_train_t_13 = get_random_assessment(reduce_train)
reduce_train_t_14 = get_random_assessment(reduce_train)
reduce_train_t_15 = get_random_assessment(reduce_train)
reduce_train_t_16 = get_random_assessment(reduce_train)
reduce_train_t_17 = get_random_assessment(reduce_train)
reduce_train_t_18 = get_random_assessment(reduce_train)
reduce_train_t_19 = get_random_assessment(reduce_train)
reduce_train_t_20 = get_random_assessment(reduce_train)


# In[ ]:


y_pred_1, oof_rmse_score_1, oof_cohen_score_1 = run_lgb(reduce_train_t_1, reduce_test, features)


# In[ ]:


y_pred_2, oof_rmse_score_2, oof_cohen_score_2 = run_lgb(reduce_train_t_2, reduce_test, features)


# In[ ]:


y_pred_3, oof_rmse_score_3, oof_cohen_score_3 = run_lgb(reduce_train_t_3, reduce_test, features)


# In[ ]:


y_pred_4, oof_rmse_score_4, oof_cohen_score_4 = run_lgb(reduce_train_t_4, reduce_test, features)


# In[ ]:


y_pred_5, oof_rmse_score_5, oof_cohen_score_5 = run_lgb(reduce_train_t_5, reduce_test, features)


# In[ ]:


y_pred_6, oof_rmse_score_6, oof_cohen_score_6 = run_lgb(reduce_train_t_6, reduce_test, features)


# In[ ]:


y_pred_7, oof_rmse_score_7, oof_cohen_score_7 = run_lgb(reduce_train_t_7, reduce_test, features)


# In[ ]:


y_pred_8, oof_rmse_score_8, oof_cohen_score_8 = run_lgb(reduce_train_t_8, reduce_test, features)


# In[ ]:


y_pred_9, oof_rmse_score_9, oof_cohen_score_9 = run_lgb(reduce_train_t_9, reduce_test, features)


# In[ ]:


y_pred_10, oof_rmse_score_10, oof_cohen_score_10 = run_lgb(reduce_train_t_10, reduce_test, features)


# In[ ]:


y_pred_11, oof_rmse_score_11, oof_cohen_score_11 = run_lgb(reduce_train_t_11, reduce_test, features)


# In[ ]:


y_pred_12, oof_rmse_score_12, oof_cohen_score_12 = run_lgb(reduce_train_t_12, reduce_test, features)


# In[ ]:


y_pred_13, oof_rmse_score_13, oof_cohen_score_13 = run_lgb(reduce_train_t_13, reduce_test, features)


# In[ ]:


y_pred_14, oof_rmse_score_14, oof_cohen_score_14 = run_lgb(reduce_train_t_14, reduce_test, features)


# In[ ]:


y_pred_15, oof_rmse_score_15, oof_cohen_score_15 = run_lgb(reduce_train_t_15, reduce_test, features)


# In[ ]:


y_pred_16, oof_rmse_score_16, oof_cohen_score_16 = run_lgb(reduce_train_t_16, reduce_test, features)


# In[ ]:


y_pred_17, oof_rmse_score_17, oof_cohen_score_17 = run_lgb(reduce_train_t_17, reduce_test, features)


# In[ ]:


y_pred_18, oof_rmse_score_18, oof_cohen_score_18 = run_lgb(reduce_train_t_18, reduce_test, features)


# In[ ]:


y_pred_19, oof_rmse_score_19, oof_cohen_score_19 = run_lgb(reduce_train_t_19, reduce_test, features)


# In[ ]:


y_pred_20, oof_rmse_score_20, oof_cohen_score_20 = run_lgb(reduce_train_t_20, reduce_test, features)


# In[ ]:


mean_rmse_score = (oof_rmse_score_1 + oof_rmse_score_2 + oof_rmse_score_3 + oof_rmse_score_4 + oof_rmse_score_5 +                    oof_rmse_score_6 + oof_rmse_score_7 + oof_rmse_score_8 + oof_rmse_score_9 + oof_rmse_score_10 +                    oof_rmse_score_11 + oof_rmse_score_12 + oof_rmse_score_13 + oof_rmse_score_14 + oof_rmse_score_15 +                    oof_rmse_score_16 + oof_rmse_score_17 + oof_rmse_score_18 + oof_rmse_score_19 + oof_rmse_score_20) / 20
mean_cappa_score = (oof_cohen_score_1 + oof_cohen_score_2 + oof_cohen_score_3 + oof_cohen_score_4 + oof_cohen_score_5 +                     oof_cohen_score_6 + oof_cohen_score_7 + oof_cohen_score_8 + oof_cohen_score_9 + oof_cohen_score_10 +                     oof_cohen_score_11 + oof_cohen_score_12 + oof_cohen_score_13 + oof_cohen_score_14 + oof_cohen_score_15 +                     oof_cohen_score_16 + oof_cohen_score_17 + oof_cohen_score_18 + oof_cohen_score_19 +                     oof_cohen_score_20) / 20
print('Our mean rmse score for our ensemble is: ', mean_rmse_score)
print('Our mean cappa score for our ensemble is: ', mean_cappa_score)
y_final = (y_pred_1 + y_pred_2 + y_pred_3 + y_pred_4 + y_pred_5 + y_pred_6 + y_pred_7 + y_pred_8 + y_pred_9 + y_pred_10 +            y_pred_11 + y_pred_12 + y_pred_13 + y_pred_14 + y_pred_15 + y_pred_16 + y_pred_17 + y_pred_18 + y_pred_19 +            y_pred_20) / 20
y_final = np.array(y_final)
predict(sample_submission, y_final)

