#!/usr/bin/env python
# coding: utf-8

# Below is the Data preprocessing and feature extraction

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
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
from sklearn.metrics import cohen_kappa_score
from sklearn.model_selection import KFold, StratifiedKFold
import gc
import json
pd.set_option('display.max_columns', 1000)


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




def encode_title(train, test, train_labels):
    # encode title
    # make a list with all the unique 'titles' from the train and test set
    list_of_user_activities = list(set(train['title'].unique()).union(set(test['title'].unique())))
    # make a list with all the unique 'event_code' from the train and test set
    list_of_event_code = list(set(train['event_code'].unique()).union(set(test['event_code'].unique())))
    # make a list with all the unique worlds from the train and test set
    list_of_worlds = list(set(train['world'].unique()).union(set(test['world'].unique())))
    # create a dictionary numerating the titles
    activities_map = dict(zip(list_of_user_activities, np.arange(len(list_of_user_activities))))
    activities_labels = dict(zip(np.arange(len(list_of_user_activities)), list_of_user_activities))
    activities_world = dict(zip(list_of_worlds, np.arange(len(list_of_worlds))))
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
    return train, test, train_labels, win_code, list_of_user_activities, list_of_event_code, activities_labels

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
    event_code_count = {eve: 0 for eve in list_of_event_code}
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
    # itarates through each session of one instalation_id
    for i, session in user_sample.groupby('game_session', sort=False):
        # i = game_session_id
        # session is a DataFrame that contain only one game_session
        
        # get some sessions information
        session_type = session['type'].iloc[0]
        session_title = session['title'].iloc[0]
                    
            
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
            features.update(event_code_count.copy())
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
        n_of_event_codes = Counter(session['event_code'])
        
        for key in n_of_event_codes.keys():
            event_code_count[key] += n_of_event_codes[key]
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


train, test, train_labels, specs, sample_submission = read_data()
# get usefull dict with maping encode
train, test, train_labels, win_code, list_of_user_activities, list_of_event_code, activities_labels = encode_title(train, test, train_labels)
# tranform function to get the train and test set
reduce_train, reduce_test, categoricals = get_train_and_test(train, test)


# In[ ]:


def preprocess(reduce_train, reduce_test):
    for df in [reduce_train, reduce_test]:
        df['installation_session_count'] = df.groupby(['installation_id'])['Clip'].transform('count')
        df['installation_duration_mean'] = df.groupby(['installation_id'])['duration_mean'].transform('mean')
        #df['installation_duration_std'] = df.groupby(['installation_id'])['duration_mean'].transform('std')
        df['installation_title_nunique'] = df.groupby(['installation_id'])['session_title'].transform('nunique')
        
        df['sum_event_code_count'] = df[[2050, 4100, 4230, 5000, 4235, 2060, 4110, 5010, 2070, 2075, 2080, 2081, 2083, 3110, 4010, 3120, 3121, 4020, 4021, 
                                        4022, 4025, 4030, 4031, 3010, 4035, 4040, 3020, 3021, 4045, 2000, 4050, 2010, 2020, 4070, 2025, 2030, 4080, 2035, 
                                        2040, 4090, 4220, 4095]].sum(axis = 1)
        
        df['installation_event_code_count_mean'] = df.groupby(['installation_id'])['sum_event_code_count'].transform('mean')
        #df['installation_event_code_count_std'] = df.groupby(['installation_id'])['sum_event_code_count'].transform('std')
        
    features = reduce_train.loc[(reduce_train.sum(axis=1) != 0), (reduce_train.sum(axis=0) != 0)].columns # delete useless columns
    features = [x for x in features if x not in ['accuracy_group', 'installation_id']]
    return reduce_train, reduce_test, features
# call feature engineering function
reduce_train, reduce_test, features = preprocess(reduce_train, reduce_test)


# Loading h2o cluster on local host.

# In[ ]:


import h2o
h2o.init(
  nthreads=-1,            ## -1: use all available threads
  max_mem_size = "8G")  


# Converting train and test in h2o data frame format

# In[ ]:


# names1=list(reduce_train.columns)
# names1.remove('accuracy_group')
# names1.remove('installation_id')


# In[ ]:


#type(reduce_test)
#f = lambda x: np.sign(x) * np.power(abs(x), 1./2)
reduce_train1=reduce_train
#reduce_train1[names1]=(reduce_train1[names1]-reduce_train1[names1].min())/(reduce_train1[names1].max()-reduce_train1[names1].min())
#reduce_train1[names]=f(reduce_train[names])
reduce_train1.columns = reduce_train1.columns.map(str)
XX=h2o.H2OFrame(reduce_train1)
#XX[names]=f(XX[names])


# In[ ]:


reduce_test1=reduce_test
#reduce_test1[names]=f(reduce_test[names])
#reduce_test1[names1]=(reduce_test1[names1]-reduce_test1[names1].min())/(reduce_test1[names1].max()-reduce_test1[names1].min())
reduce_test1.columns = reduce_test1.columns.map(str)
test=h2o.H2OFrame(reduce_test1)
#XX1[names]=f(XX1[names])


# In[ ]:


XX["accuracy_group"] = XX["accuracy_group"].asfactor()
names=list(XX.columns)
names.remove('accuracy_group')
names.remove('installation_id')


# Simple XGBoost model h2o 

# In[ ]:


param = {
      "ntrees" : 200
    , "max_depth" : 10
    , "learn_rate" : 0.02
    , "sample_rate" : 0.7
    , "col_sample_rate_per_tree" : 0.9
    , "min_rows" : 5
    , "seed": 4241
    , "score_tree_interval": 100,"stopping_metric" :"MSE","nfolds":8,"fold_assignment":"AUTO","keep_cross_validation_predictions" : True,"booster":"dart"
}
from h2o.estimators import H2OXGBoostEstimator
model_xgb = H2OXGBoostEstimator(**param)
model_xgb.train(x = names, y = "accuracy_group", training_frame = XX)


# In[ ]:


model_xgb


# In[ ]:


param = {
      "ntrees" : 500
    , "max_depth" : 5
    , "learn_rate" : 0.02
    , "sample_rate" : 0.7
    , "col_sample_rate_per_tree" : 0.9
    , "min_rows" : 5
    , "seed": 4241
    , "score_tree_interval": 100,"stopping_metric" :"MSE","nfolds":8,"fold_assignment":"AUTO","keep_cross_validation_predictions" : True
}
from h2o.estimators import H2OXGBoostEstimator
model_xgb2 = H2OXGBoostEstimator(**param)
model_xgb2.train(x = names, y = "accuracy_group", training_frame = XX)


# In[ ]:


model_xgb2


# In[ ]:


param = {
      "ntrees" : 200
    , "max_depth" : 10
    , "learn_rate" : 0.02
    , "sample_rate" : 0.7
    , "col_sample_rate_per_tree" : 0.9
    , "min_rows" : 5
    , "seed": 4241
    , "score_tree_interval": 100,"stopping_metric" :"MSE","nfolds":8,"fold_assignment":"AUTO","keep_cross_validation_predictions" : True
}
from h2o.estimators import H2OXGBoostEstimator
model_xgb3 = H2OXGBoostEstimator(**param)
model_xgb3.train(x = names, y = "accuracy_group", training_frame = XX)


# In[ ]:


model_xgb3


# Random Forest h2o model

# In[ ]:


param = {
      "ntrees" : 200
    , "max_depth" : 10
    #, "learn_rate" : 0.02
    , "sample_rate" : 0.7
    , "col_sample_rate_per_tree" : 0.9
    , "min_rows" : 5
    , "seed": 4241
    , "score_tree_interval": 100,"stopping_metric" :"logloss","nfolds":8,"fold_assignment":"AUTO","keep_cross_validation_predictions" : True
}
from h2o.estimators.random_forest import H2ORandomForestEstimator
model_rf = H2ORandomForestEstimator(**param)
model_rf.train(x = names, y = "accuracy_group", training_frame = XX)


# In[ ]:


model_rf


# Deep learning model h2o

# In[ ]:


param = {
    "hidden":[32,32,32],
    "epochs":1000,
    "stopping_tolerance":0.01,
    "seed":4241,
    "activation":"Tanh",
    "stopping_metric" :"MSE","nfolds":8,"fold_assignment":"AUTO","keep_cross_validation_predictions" : True
}
from h2o.estimators import H2ODeepLearningEstimator
model_dl1 = H2ODeepLearningEstimator(**param)
model_dl1.train(x = names, y = "accuracy_group", training_frame = XX)


# In[ ]:


model_dl1


# Ensemble model of all three, to ensemble the `nfolds` and `"keep_cross_validation_predictions" : True` should be same.

# In[ ]:


from h2o.estimators import H2OStackedEnsembleEstimator
stack = H2OStackedEnsembleEstimator(model_id="ensemble11",
                                       training_frame=XX,
                                       #validation_frame=test,
                                       base_models=[model_xgb.model_id,model_xgb2.model_id,model_xgb3.model_id, model_rf.model_id,model_dl1.model_id],metalearner_algorithm="glm")
stack.train(x=names, y="accuracy_group", training_frame=XX)
#stack.model_performance()


# In[ ]:


stack


# Predicting

# In[ ]:


prediction = stack.predict(test)


# In[ ]:


pred_all=prediction.as_data_frame()


# Calculating prediction probability

# In[ ]:


pred_all['prob']=pred_all['p1']+pred_all['p2']*2+pred_all['p3']*3


# In[ ]:


coefficients = [1.12232214, 1.73925866, 2.22506454]
import numpy
oof=list(pred_all['prob'])
i=0
while i < len(oof):
    if oof[i]<=coefficients[0]:
        oof[i]=0
    if oof[i]>coefficients[0] and oof[i]<=coefficients[1]:
        oof[i]=1
    if oof[i]>coefficients[1] and oof[i]<=coefficients[2]:
        oof[i]=2
    if oof[i]>coefficients[2]:
        oof[i]=3
    i=i+1


# In[ ]:


#oof=list(pred_all['prob'])
pred_all['prob']=oof
final_sub=pd.DataFrame(reduce_test["installation_id"])
final_sub["accuracy_group"]=pred_all['prob']


# In[ ]:


final_sub.to_csv('submission.csv', index = False)

