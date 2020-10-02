#!/usr/bin/env python
# coding: utf-8

# # Introduction
# 
# The aim of this notebook is to select the features that maximizes the score,
# by forward selection.
# 
# The script will begin with no features
# and it will add the feature which contribute more to the score.
# 
# First the accuracy of the current set of features is calculated.
# Then, for all the features of the set,
# it calculates the accuracy if only this feature is dropped.
# The feature set with the greatest accuracy,
# means that a new set of features without this feature,
# scores more.
# Then this feature is dropped.
# 
# Finally, the functions continues with this new set until there are only two values left.
#     
# The models are fitted and predicted with the optimized parameters and new features of the notebook ([Tactic 06. Feature engineering](https://www.kaggle.com/juanmah/tactic-06-feature-engineering/)).
# 
# The results are collected at [Tactic 99. Summary](https://www.kaggle.com/juanmah/tactic-99-summary).

# In[ ]:


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pip._internal as pip
pip.main(['install', '--upgrade', 'numpy==1.17.2'])
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.model_selection import cross_val_predict, cross_val_score
from tqdm import tqdm_notebook
import pickle

from lwoku import get_accuracy, add_features


# # Prepare data

# In[ ]:


# Read training and test files
X_train = pd.read_csv('../input/learn-together/train.csv', index_col='Id', engine='python')
X_test = pd.read_csv('../input/learn-together/test.csv', index_col='Id', engine='python')

# Define the dependent variable 
y_train = X_train['Cover_Type'].copy()

# Define a training set
X_train = X_train.drop(['Cover_Type'], axis='columns')


# In[ ]:


# Add new features
print('     Number of features (before adding): {}'.format(len(X_train.columns)))
X_train = add_features(X_train)
X_test = add_features(X_test)
print('     Number of features (after adding): {}'.format(len(X_train.columns)))


# In[ ]:


print('  -- Drop features')
print('    -- Drop columns with few values (or almost)')
features_to_drop = ['Soil_Type7', 'Soil_Type8', 'Soil_Type15', 'Soil_Type27', 'Soil_Type37']
X_train.drop(features_to_drop, axis='columns', inplace=True)
X_test.drop(features_to_drop, axis='columns', inplace=True)
print('    -- Drop columns with low importance')
features_to_drop = ['Soil_Type5', 'Slope', 'Soil_Type39', 'Soil_Type18', 'Soil_Type20', 'Soil_Type35', 'Soil_Type11',
                    'Soil_Type31']
X_train.drop(features_to_drop, axis='columns', inplace=True)
X_test.drop(features_to_drop, axis='columns', inplace=True)
print('     Number of features (after drop): {}'.format(len(X_train.columns)))


# # LightGBM
# 
# Examine the full hyperparameter optimization details for this model in the following notebook: [Tactic 03. Hyperparameter optimization. LightGBM](https://www.kaggle.com/juanmah/tactic-03-hyperparameter-optimization-lightgbm)

# In[ ]:


with open('../input/tactic-03-hyperparameter-optimization-lightgbm/clf.pickle', 'rb') as fp:
    clf = pickle.load(fp)
lg_clf = clf.best_estimator_
lg_clf


# In[ ]:


lg_clf_fast = LGBMClassifier(boosting_type='gbdt', class_weight=None, colsample_bytree=0.9,
               importance_type='split', learning_rate=0.7, max_depth=21,
               min_child_samples=5, min_child_weight=1e-15, min_split_gain=0.0,
               n_estimators=200, n_jobs=-1, num_leaves=38, objective=None,
               random_state=42, reg_alpha=0.0, reg_lambda=0.0, silent=True,
               subsample=1.0, subsample_for_bin=987, subsample_freq=0,
               verbosity=1)
lg_clf_fast


# In[ ]:


get_ipython().run_cell_magic('time', '', "## Get accuracy for the original data without feature engineering\naccuracy = get_accuracy(lg_clf_fast, X_train, y_train)\nprint('Accuracy without feature engineering: {:.2f}\\u00A0%'.format(accuracy * 100))")


# In[ ]:


# noinspection PyPep8Naming
def accuracy_table_by_expanding():
    """
    This function calculates the accuracy of the current set of features, and put it in 'Base' column.
    Then it calculates the accuracy if only one feature is added.
    The feature with the greatest accuracy, mean that a new set of features with this feature, scores more.
    Then this feature is added.
    And then, the functions continues with this new set until there are no new features left. 
    :return: A table with the base accuracy and the accuracy of the added feature for each iteration
    """
    table = pd.DataFrame(columns=['Base'])
    X_features = pd.DataFrame()

    progress_bar = tqdm_notebook(total=(len(X_train.columns) + 1) * len(X_train.columns) / 2)
    while len(X_features.columns) <= len(X_train.columns):
        print(len(X_features.columns))
        if len(X_features.columns) == 0:
            row = {'Base': 0}
        else:
            row = {'Base': get_accuracy(lg_clf_fast, X_features, y_train)}
        for feature in X_train.columns.drop(X_features.columns):
            X_temp = X_features.copy()
            X_temp[feature] = X_train[feature]
            row[feature] = get_accuracy(lg_clf_fast, X_temp, y_train)
        progress_bar.update(len(X_train.columns) - len(X_features.columns))
        table = table.append(row, ignore_index=True)
        feature_to_add = table.iloc[-1][1:].idxmax()
        print('Feature to add: {}'.format(feature_to_add))
        if pd.isnull(feature_to_add):
            break
        else:
            X_features[feature_to_add] = X_train[feature_to_add]
#         print(X_features.columns.tolist())
    progress_bar.close()
    return table


# Get the table for expanding
expanding_table = accuracy_table_by_expanding()


# # Export

# In[ ]:


expanding_table.to_csv('expanding_table.csv', index=False)


# # Get the features set with largest accuracy

# In[ ]:


# Get the largest accuracy
expanding_table_accuracy = expanding_table['Base'].max()
print('Maximum accuracy: {:.2f}\u00A0%'.format(expanding_table_accuracy * 100))

# Get the features set with largest accuracy
expanding_table_best_row = expanding_table.iloc[expanding_table['Base'].idxmax()]
expanding_table_best_row.dropna(inplace=True)
expanding_table_best_row.drop('Base', inplace=True)
expanding_table_features = X_train.columns.drop(expanding_table_best_row.axes[0].tolist()).tolist()
print('For this set of features: {}'.format(expanding_table_features))


# # Submit

# In[ ]:


# Predict with test data
lg_clf.fit(X_train[expanding_table_features], y_train)
y_test_pred = pd.Series(lg_clf.predict(X_test[expanding_table_features]))

# Submit
output = pd.DataFrame({'ID': X_test.index, 'Cover_Type': y_test_pred})

output.to_csv('submission.csv', index=False)

