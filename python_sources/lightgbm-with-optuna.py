#!/usr/bin/env python
# coding: utf-8

# # LightGBM_with_Optuna
# This notebook show you how to use lightGBM and how to tuning with optuna.  
# This is my first public kernel and I'm a beginner of ML (and also English...). So if you feel "I don't understand what this note say" please don't hesitate to comments and questions. 
#   
#   
# The highlight of this kernel is :  
# Using optuna to tuning hyperparameter : Hyperparameter tuning is always bother but optuna automatically find them.  
# Using PCA to drop feature dim : The titanic dataset is not learge and doesn't have too many cols to learn but in ML this is a rare case. This kernel introduce how to drop dims with PCA.  
# Using SMOTE to oversampling : Survived label is imblance and sometimes imbalance dataset makes difficult to predict. So I show the way to use SMOTE the library to preprocess imblanced data. (Maybe this not suit titanic dataset...)

# In[ ]:


from logging import getLogger, StreamHandler, DEBUG, INFO
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False


# In[ ]:


import numpy as np
import pandas as pd
from tqdm import tqdm

import pandas_profiling as pdp

import lightgbm as lgb
import optuna, os, uuid, pickle

from sklearn import datasets
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder

import scipy.stats

from imblearn.over_sampling import SMOTE

import matplotlib
import matplotlib.pyplot as plt #Visulization
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('ggplot') 


# ### Very simple EDA
# Titanic dataset is quite famous and there are a lot of great EDA. So I don't spend time to EDA. Just use pandas-profiling.

# In[ ]:


pdp.ProfileReport(pd.read_csv('../input/train.csv'))


# ### Preprocess : use only int or float
# PCA can't handle non numeric value and NaN. This is simple way to preprocess. If you want to get high score, you have to this process seriously.

# In[ ]:


train_df = pd.read_csv('../input/train.csv')
test_df = pd.read_csv('../input/test.csv')
test_df['Fare'] = test_df['Fare'].fillna(0)

genders = {'male': 0, 'female': 1} 
train_df['Sex'] = train_df['Sex'].map(genders) 
test_df['Sex'] = test_df['Sex'].map(genders)
# to dummy
train_df = pd.get_dummies(train_df, columns=['Pclass', 'Embarked']) 
test_df = pd.get_dummies(test_df, columns = ['Pclass', 'Embarked'])
# remove unuse cols
train_df.drop(['PassengerId', 'Name', 'Cabin', 'Ticket'], axis=1, inplace=True) 
test_df.drop(['PassengerId', 'Name', 'Cabin', 'Ticket'], axis=1, inplace=True)

train_df['Age'] = train_df['Age'].fillna(200)
test_df['Age'] = test_df['Age'].fillna(200)

train_df.sample(5)


# In[ ]:


train_df.shape[1]


# ### PCA to drop dims
# As you can see, This dataset(droped some cols) has just 10 dims. But usually ML problem has a lot of features and this make ML difficult. So I some times use PCA to get features has more info less cols.  
# At first, PCA with all cols (of course without "Answer col"), then check explained variance ratio like this.

# In[ ]:


pca_n_components = train_df.shape[1] - 1
pca_all = PCA(n_components=pca_n_components)
X_train_pca_all = pca_all.fit_transform(train_df.drop('Survived', axis=1))


# In[ ]:


plt.bar(range(1, pca_n_components+1), pca_all.explained_variance_ratio_, alpha=0.5, align='center')
plt.step(range(1, pca_n_components+1), np.cumsum(pca_all.explained_variance_ratio_), where='mid')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal components')

plt.show()


# Oh... In this case, we need only 2 features to explane 9 original cols. So let's take 2 cols like bellow.   
# (Usually only few cols can't explane all of origins. We shoud consider balance of Explained variance ratio and feature dims. For example, "take 32 cols to explane 80% of origins".)

# In[ ]:


pca_n_components = 2
pca = PCA(n_components=pca_n_components)

X_train = pca.fit_transform(train_df.drop('Survived', axis=1))
X_test = pca.fit_transform(test_df)

y_train = np.array(train_df['Survived'])


# In[ ]:


# you can see result of pca like this way
# PCA_cols = ['PCA_' + str(i) for i in range(pca_n_components)]
# train_df_pca = pd.DataFrame(X_train, columns=PCA_cols)
# test_df_pca = pd.DataFrame(X_test, columns=PCA_cols)

# train_df_pca['Survived'] = train_df['Survived']
# train_df_pca.sample(5)


# ### SMOTE
# SMOTE give us easily over/down sampling imblance dataset. In this kernel, I chose oversampling smaller label. If your target is not binaly_classification, you can use this cell without changes.  
# But you have to change k_neighbors to fit your data. This sets how many neighbors data SMOTE chose.  
# details : https://imbalanced-learn.readthedocs.io/en/stable/generated/imblearn.over_sampling.SMOTE.html
# 
# And unfotunately, downsampling and bagging may be better approach...  
# https://www.semanticscholar.org/paper/Class-Imbalance%2C-Redux-Wallace-Small/a8ef5a810099178b70d1490a4e6fc4426b642cde

# In[ ]:


sm = SMOTE(random_state=84, k_neighbors=20)
X_res, y_res = sm.fit_sample(X_train, y_train)

print(X_res.shape)
print(y_res.shape)


# In[ ]:


def shuffle_samples(X, y):
    zipped = list(zip(X, y))
    np.random.shuffle(zipped)
    X_result, y_result = zip(*zipped)
    return np.asarray(X_result), np.asarray(y_result)

X_res, y_res = shuffle_samples(X_res, y_res)


# By the way, fearture engineering needs a lot of variables (and RAMs). The next cell show variables with memory usage. If you find needless huge variable(s), you can drop it to exec  
# del var

# In[ ]:


import sys

print("{}{: >25}{}{: >10}{}".format('|','Variable Name','|','Memory','|'))
print(" ------------------------------------ ")
for var_name in dir():
    if not var_name.startswith("_") and sys.getsizeof(eval(var_name)) > 10000:
        print("{}{: >25}{}{: >10}{}".format('|',var_name,'|',sys.getsizeof(eval(var_name)),'|'))


# ### Optuna : tuning hyperparameters
# The next cell, recode uuid of every trial of optuna. You can change range of hyperparameters to improve output. This is not suit this dataset.  
# And at first, you should set small number at NUM_BOOST_ROUND. Titanic is small dataset (and also we have only 2 dims) so it doesn't take long time. But in other dataset, I recommend to run small NUM_BOOST_ROUND and narrowing the parameter width sometimes. And then set NUM_BOOST_ROUND what you want.
# 
# And this cell print a lot of things...

# In[ ]:


TRIAL_TIMES = 1000
NUM_BOOST_ROUND = 1000
EARLY_STOP_COUNTS = 10

def train_optuna(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=84)
    
    def objectives(trial):
        # set UUID
        trial_uuid = str(uuid.uuid4())
        trial.set_user_attr("uuid", trial_uuid)

        # if you want to tune multi-class learning, you have to 
        # change objective to "multiclass", metric to {'multi_logloss', 'multi_error'} and 
        # add 'num_class': "your_class_count"
        params = {
            'boosting_type': trial.suggest_categorical('boosting', ['gbdt', 'goss']),#, 'dart']),
            'objective': 'binary',
            'metric': {'binary', 'binary_error', 'auc'},
            'num_leaves': trial.suggest_int("num_leaves", 10, 1000),
            'learning_rate': trial.suggest_loguniform("learning_rate", 1e-4, 1),
            'feature_fraction': trial.suggest_uniform("feature_fraction", 0.0, 1.0),
#             'device' : 'gpu',
            'verbose' : 0
        }
        if params['boosting_type'] == 'dart':
            params['drop_rate'] = trial.suggest_loguniform('drop_rate', 1e-8, 1.0)
            params['skip_drop'] = trial.suggest_loguniform('skip_drop', 1e-8, 1.0)
        if params['boosting_type'] == 'goss':
            params['top_rate'] = trial.suggest_uniform('top_rate', 0.0, 1.0)
            params['other_rate'] = trial.suggest_uniform('other_rate', 0.0, 1.0 - params['top_rate'])

        pruning_callback = optuna.integration.LightGBMPruningCallback(trial, "binary_logloss")
        gbm = lgb.train(params, lgb.Dataset(X_train, y_train), num_boost_round=NUM_BOOST_ROUND,
                        valid_sets=lgb.Dataset(X_test, y_test), callbacks=[pruning_callback],
                        early_stopping_rounds=EARLY_STOP_COUNTS
                       )

        # check train/eval error
        y_pred_train = np.rint(gbm.predict(X_train))
        y_pred_test = np.rint(gbm.predict(X_test))
        error_train = 1.0 - accuracy_score(y_train, y_pred_train)
        error_test = 1.0 - accuracy_score(y_test, y_pred_test)

        # set error rate
        trial.set_user_attr("train_error", error_train)
        trial.set_user_attr("test_error", error_test)

        # save model
        if not os.path.exists("lgb_output"):
            os.mkdir("lgb_output")
        with open("lgb_output/"+f"{trial_uuid}.pkl", "wb") as fp:
            pickle.dump(gbm, fp)

        return error_test

    study = optuna.create_study()
    study.optimize(objectives, n_trials=TRIAL_TIMES)

    print(study.best_params)
    print(study.best_value)

    print(study.best_trial.user_attrs)

    df = study.trials_dataframe()
    df.to_csv("optuna_lgb.csv")
    
    return study.best_trial.user_attrs

optuna.logging.disable_default_handler()
result_dict = train_optuna(X_res, y_res)


# In[ ]:


best_uuid = result_dict['uuid']
print(best_uuid)

def load_model(X, y):
    with open('lgb_output/' + str(best_uuid) + '.pkl', 'rb') as fp:
        gbm = pickle.load(fp)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=84)
    y_pred = np.rint(gbm.predict(X_test))
    print("Test Accuracy")
    print(accuracy_score(y_test, y_pred))
    return gbm
    
gbm = load_model(X_train, y_train)
y_pred = np.rint(gbm.predict(X_test))
output_df = pd.DataFrame(y_pred, columns=['Survived']).astype('int')
output_df['PassengerId'] = pd.read_csv('../input/test.csv')['PassengerId']
output_df = output_df.loc[:,['PassengerId', 'Survived']]
output_df.to_csv('submit.csv', header=True, index=False)


# This is not so bad... But not good.  
# Let's see data.

# In[ ]:


plt.scatter(X_train[:,0], X_train[:,1])
plt.show()


# In[ ]:


plt.scatter(X_test[:,0], X_test[:,1])
plt.show()


# In[ ]:


X_train_resize = X_train
X_train_resize[:,0] = X_train_resize[:,0] / max(abs(X_train_resize[:,0]))
X_train_resize[:,1] = X_train_resize[:,1] / max(abs(X_train_resize[:,1]))

X_test_resize = X_test
X_test_resize[:,0] = X_test_resize[:,0] / max(abs(X_test_resize[:,0]))
X_test_resize[:,1] = X_test_resize[:,1] / max(abs(X_test_resize[:,1]))


# ### KMEANS
# As you can see, train/test dataset distribution is not so far and distributed not evenly. So let's try clustering methods to split train/eval data keep distribution.  
# The bellow cell show k_means clustering. You can modify "n_clusters" to decide cluster counts.

# In[ ]:


from sklearn.cluster import KMeans
n_clusters = 6
cmap = plt.get_cmap("tab10")
kmeans_model_train = KMeans(n_clusters=n_clusters, random_state=84).fit(X_train_resize)
kmeans_model_test = KMeans(n_clusters=n_clusters, random_state=84).fit(X_test_resize)

shape_dict = {0:'x', 1:'+'}
# plt.figure()
plt.subplot(1, 2, 1)
for (i, label) in enumerate(tqdm(kmeans_model_train.labels_)):
    plt.scatter(X_train_resize[i, 0], X_train_resize[i, 1], c=cmap(label), marker=shape_dict[y_train[i]])

plt.subplot(1, 2, 2)
for (i, label) in enumerate(tqdm(kmeans_model_test.labels_)):
    plt.scatter(X_test_resize[i, 0], X_test_resize[i, 1], c=cmap(label))
    
plt.show()


# In[ ]:


cols = ['PCA_' + str(i) for i in range(pca_n_components)]
train_resize_df = pd.DataFrame(X_train_resize, columns=cols)
train_resize_df['KMEANS_ID'] = kmeans_model_train.labels_
train_resize_df.sample(5)


# In[ ]:


id_df_train = pd.DataFrame(train_resize_df['KMEANS_ID'].value_counts())
id_df_train = id_df_train.reset_index()
id_df_train.columns = ['KMEANS_ID', 'count']
id_df_train


# ### Downsampling and Bagging

# In[ ]:


from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import roc_auc_score

def imbalanced_data_split(X, y, test_size=0.1):
    sss = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=0)
    for train_index, test_index in sss.split(X, y.tolist()):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        return X_train, X_test, y_train, y_test

def gbm_train(X_train, X_eval, y_train, y_eval, gbm_params):
    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = lgb.Dataset(X_eval, y_eval, reference=lgb_train)
    model = lgb.train(gbm_params, lgb_train, num_boost_round=NUM_BOOST_ROUND,
                      valid_sets=lgb_eval, early_stopping_rounds=20
                     )
    return model
    
def bagging(seed, X_df, y, gbm_params):
    sampler = RandomUnderSampler(random_state=seed, replacement=True)
    X_resampled, y_resampled = sampler.fit_resample(X_df, y)
    X_train, X_eval, y_train, y_eval = imbalanced_data_split(X_resampled, y_resampled, test_size=0.1)
    logger.debug('X_train.shape:' + str(X_train.shape))
    logger.debug('X_train:' + str(X_train))
    logger.debug('y_train.shape:' + str(y_train.shape))
    logger.debug('y_train:' + str(y_train))
    logger.debug('X_eval.shape:' + str(X_eval.shape))
    logger.debug('X_eval:' + str(X_eval))
    logger.debug('y_eval.shape:' + str(y_eval.shape))
    logger.debug('y_eval:' + str(y_eval))
    
    model_bagging = gbm_train(X_train, X_eval, y_train, y_eval, gbm_params)
    return model_bagging


# In[ ]:


gbm_params = gbm.params
models = []
for i in tqdm(range(10)):
    models.append(bagging(i, train_resize_df, y_train, gbm_params))


# In[ ]:


y_preds = []

for model in models:
    y_preds.append(model.predict(X_test, num_iteration=model.best_iteration))

y_preds_bagging = sum(y_preds)/len(y_preds)

my_answer = np.rint(y_preds_bagging)
my_answer_df = pd.DataFrame(my_answer, columns=['Survived']).astype('int')
my_answer_df['PassengerId'] = pd.read_csv('../input/test.csv')['PassengerId']
my_answer_df = output_df.loc[:,['PassengerId', 'Survived']]
my_answer_df.to_csv('submit_bagging.csv', header=True, index=False)


# In[ ]:


my_answer_df.sample(15)


# In[ ]:





# In[ ]:


# doubt PCA
models = []
for i in tqdm(range(10)):
    models.append(bagging(i, train_df, y_train, gbm_params))

y_preds = []

for model in models:
    y_preds.append(model.predict(test_df, num_iteration=model.best_iteration))

y_preds_bagging = sum(y_preds)/len(y_preds)

my_answer = np.rint(y_preds_bagging)
my_answer_df = pd.DataFrame(my_answer, columns=['Survived']).astype('int')
my_answer_df['PassengerId'] = pd.read_csv('../input/test.csv')['PassengerId']
my_answer_df = output_df.loc[:,['PassengerId', 'Survived']]
my_answer_df.to_csv('submit_bagging_noPCA.csv', header=True, index=False)


# In[ ]:


logger.debug(y_preds)
logger.debug(y_preds_bagging)


# In[ ]:




