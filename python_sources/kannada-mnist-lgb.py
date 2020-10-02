#!/usr/bin/env python
# coding: utf-8

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

# importing libraries
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")


# #### Loading the training and testing datasets and showing some basic statistics using pandas in-built describe() and info() functions.

# In[ ]:


# loading the datasets

# loading the dig-minst.csv file

digit_df = pd.read_csv("/kaggle/input/Kannada-MNIST/Dig-MNIST.csv")


# In[ ]:



# loding the training data

train_df = pd.read_csv("/kaggle/input/Kannada-MNIST/train.csv")


# In[ ]:



# loading the testing data

test_df = pd.read_csv("/kaggle/input/Kannada-MNIST/test.csv")


# In[ ]:


digit_df.head()


# In[ ]:


digit_df.describe()


# In[ ]:


digit_df.info()


# In[ ]:


train_df.describe()


# In[ ]:


train_df.head()


# In[ ]:


train_df.info()


# In[ ]:


test_df.head()


# In[ ]:


test_df.describe()


# In[ ]:


test_df.info()


# In[ ]:


# checking the label distribution using sns - barchart

train_df['label'].value_counts().plot("bar")


# In[ ]:


digit_df['label'].value_counts().plot('bar')


# In[ ]:


# getting all unique labels

pd.unique(train_df['label'])


# In[ ]:


sns.distplot(train_df['label'])


# #### Standardising / normalizing the data and then feed the data into to our model

# In[ ]:


# removing the label from training data

train = train_df.drop(['label'], axis = 1)


# In[ ]:


train.head()


# In[ ]:


# getting the label as our target data

target = train_df['label']


# In[ ]:


target.head()


# In[ ]:


# removing the id from the test dataframe

test = test_df.drop("id", axis=1)


# In[ ]:


test.head()


# In[ ]:


# getting some meta information from our training and testing dataframes

print("No.f rows in train data set: {}".format(len(train)))
print("No.f rows in test data set: {}".format(len(test)))
print("No.f rows in target data set: {}".format(len(target)))


# In[ ]:


print("No.f columns in train data set: {}".format(len(train.columns)))
print("No.f columns in test data set: {}".format(len(test.columns)))


# #### Projecting the data into a 2D plan using - PCA

# In[ ]:


from sklearn.decomposition import PCA

pca = PCA(n_components=2)


# In[ ]:


principal_components = pca.fit_transform(train)


# In[ ]:


principalDF = pd.DataFrame(data = principal_components,
                                  columns=["Principal Component 1", "Principal Component 2"])


# In[ ]:


finalDF = pd.concat([principalDF, target], axis=1)


# In[ ]:


finalDF.head()


# In[ ]:


# visualizing the Mnist data using a 2D plot

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
plt.xlim([-1500, 1500])
plt.ylim([-1500, 1500])
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = [0, 1, 2, 3, 4, 5, 6]
colors = ["b", "g", "r", "c", "m", "y", "k"]
for label, color in zip(targets, colors):
    indicesToKeep = finalDF['label'] == label
    ax.scatter(finalDF.loc[indicesToKeep, 'Principal Component 1'], 
               finalDF.loc[indicesToKeep, 'Principal Component 2'], 
               c = color,
               s = 50)
ax.legend(targets)
ax.grid()


# In[ ]:


# Standardizing the data

from sklearn.preprocessing import StandardScaler

standard_scaler = StandardScaler()


# In[ ]:


# transform train and test dataset

# tranforming the training dataset
train_transformed = standard_scaler.fit_transform(train)


# In[ ]:


# tranforming the test dataset

test_tranformed = standard_scaler.fit_transform(test)


# In[ ]:


train_transformed[:2]


# In[ ]:


test_tranformed[:2]


# In[ ]:


# importing sklearn, lgb and other libraries

import sklearn
import lightgbm as lgb
from sklearn import metrics
from sklearn import model_selection

# for hyper parameter tuning we are using hypetopt instead of scikit-learn GridSearchCV
from hyperopt import hp, tpe, fmin, STATUS_OK, Trials


# In[ ]:


pca = PCA(0.95)


# In[ ]:


train_transformed = pca.fit_transform(train_transformed)


# In[ ]:


test_tranformed = pca.fit_transform(test_tranformed)


# In[ ]:


train_features, valid_features, y_train, y_valid = model_selection.train_test_split(train_transformed, target, test_size=0.30, random_state=123456789)


# In[ ]:


print("Shape of the train_features data: {}".format(train_features.shape))
print("Shape of the valid_features data: {}".format(valid_features.shape))


# In[ ]:


print("Shape of the y_train data: {}".format(y_train.shape))
print("Shape of the y_valid data: {}".format(y_valid.shape))


# In[ ]:


# scoring and optimizatin function for lightgbm

def lgb_score(space):
    print("Training with params: {}".format(space))
    
    num_leaves = int(space['num_leaves'])
    bagging_freq = int(space['bagging_freq'])
    n_estimators = int(space['n_estimators'])
    min_data_in_leaf = int(space['min_data_in_leaf'])

    del space['num_leaves']
    del space['bagging_freq']
    del space['n_estimators']
    del space['min_data_in_leaf']
    
    clf = lgb.LGBMClassifier(n_estimators=n_estimators,
                             learning_rate=space['learning_rate'],
                             min_data_in_leaf=min_data_in_leaf,
                             bagging_freq=bagging_freq,
                             min_sum_hessian_in_leaf=space['min_sum_hessian_in_leaf'],
                             feature_fraction=space['feature_fraction'],
                             bagging_fraction=space['bagging_fraction'],
                             num_leaves=num_leaves,
                             boost_from_average=space['boost_from_average'],
                             boosting_type='gbdt',
                             max_depth=-1,
                             num_threads=8,
                             verbosity=1,
                             tree_learner='serial',
                             objective = "multiclass")
    clf.fit(train_features, y_train, eval_set=[(valid_features, y_valid)], verbose=5000, eval_metric='multi_logloss', early_stopping_rounds=2500)
    predictions = clf.predict_proba(valid_features)[:, 1]
    score = metrics.roc_auc_score(y_valid, predictions)
    
    return {'loss': 1 - score, 'status': STATUS_OK}


# In[ ]:


# defining the space

def optimize(evals, random=42):
    
    space = {
        'n_estimators': hp.uniform('n_estimators', 25000, 35000),
        'learning_rate': hp.quniform('learning_rate', 0.00075, 0.0099, 0.00015),
        'min_data_in_leaf': hp.uniform('min_data_in_leaf', 50, 50),
        'bagging_freq': hp.uniform('bagging_freq', 5, 50),
        'min_sum_hessian_in_leaf': hp.quniform('min_sum_hessian_in_leaf', 5.0, 75.0, 2.5),
        'feature_fraction': hp.uniform('feature_fraction', 0.010, 0.095),
        'bagging_fraction': hp.uniform('bagging_fraction', 0.015, 0.995),
        'num_leaves': hp.uniform('num_leaves', 50, 100),
        'boost_from_average': hp.choice('boost_from_average', ['true', 'false'])
    }
    
    best = fmin(lgb_score, space=space, algo=tpe.suggest, max_evals=evals)
    return best


# In[ ]:


params = optimize(10)


# In[ ]:




