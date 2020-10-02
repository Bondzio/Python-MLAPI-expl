#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd
import numpy as np


# # About Boruta Feature Elimination
# 
# The Boruta algorithm is a wrapper built around the random forest classification algorithm. The algorithm tries to evaluate the features to rank their importance with respect to the target variable. Boruta compares the feature importance (Z-score) with the feature importance produced by a shuffled copy of the original dataset (called shadow features). Each time the feature has a higher Z-score than the maximum Z-score of its shadow features than the best of the shadow features, Robuta record a "hits" for that feature.
# 
# If a feature don't record a hit in certain amount of iteration, we put it in the reject bin.
# 
# High-level description can be found here: https://www.datacamp.com/community/tutorials/feature-selection-R-boruta
# 
# Original paper: https://www.jstatsoft.org/article/view/v036i11/v36i11.pdf
# 
# Python Implementation Kernel:https://www.kaggle.com/tilii7/boruta-feature-elimination/notebook
# 
# 
# **Note**: Depend on your data size, Boruta will takes while to complete. Mine took ~5 hours.
# 
# I can only run with almost half the dataset due to Kaggle 16GB ram limitation.

# In[ ]:


def reduce_mem_usage(df, verbose=True):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024**2    
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)    
    end_mem = df.memory_usage().sum() / 1024**2
    if verbose: print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem, 100 * (start_mem - end_mem) / start_mem))
    return df


# In[ ]:


train_identity = pd.read_csv("../input/ieee-fraud-detection/train_identity.csv", index_col='TransactionID')
train_transaction = pd.read_csv("../input/ieee-fraud-detection/train_transaction.csv", index_col='TransactionID')

train_identity = reduce_mem_usage(train_identity)
train_transaction = reduce_mem_usage(train_transaction)

train_full = train_transaction.merge(train_identity, how='left', left_index=True, right_index=True)

train_full = train_full.sample(frac = 0.4, random_state = 42)

del train_identity, train_transaction


# ## Feature Selection
# 
# In the baseline model, we learned that the information poor features such as TransactionDT was among the most important features. We will try Boruta, a method of eliminating these features by only capture the important, interesting features that have high degree of influence on the target variable.

# In[ ]:


from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from boruta import BorutaPy

train_full = train_full.fillna(-999)

# Label Encoding
for f in train_full.columns:
    if train_full[f].dtype=='object': 
        lbl = preprocessing.LabelEncoder()
        lbl.fit(list(train_full[f].values)) 
        train_full[f] = lbl.transform(list(train_full[f].values))

X = train_full.drop('isFraud', axis = 1).values
y = train_full['isFraud'].values


# In[ ]:


# Run Boruta 
rfc = RandomForestClassifier(n_estimators='auto', n_jobs=4, max_depth=6)
boruta_selector = BorutaPy(rfc, n_estimators='auto', verbose=2, max_iter = 70)
boruta_selector.fit(X, y)


# In[ ]:


# number of selected features
print ('\n Number of selected features:')
print (boruta_selector.n_features_)


# In[ ]:


train_identity = pd.read_csv("../input/ieee-fraud-detection/train_identity.csv", index_col='TransactionID')
train_transaction = pd.read_csv("../input/ieee-fraud-detection/train_transaction.csv", index_col='TransactionID')

train_full = train_transaction.merge(train_identity, how='left', left_index=True, right_index=True)

feature_df = pd.DataFrame(train_full.drop(['isFraud'], axis=1).columns.tolist(), columns=['features'])
feature_df['rank']=boruta_selector.ranking_
feature_df = feature_df.sort_values('rank', ascending=True).reset_index(drop=True)
print ('\n Top %d features:' % boruta_selector.n_features_)
print (feature_df.head(boruta_selector.n_features_))
feature_df.to_csv('feature-ranking.csv', index=False)


# In[ ]:


# check selected features
selected_features = train_full.drop('isFraud', axis = 1).columns[boruta_selector.support_]
rejected_features = train_full.drop('isFraud', axis = 1).columns[boruta_selector.support_ == False]

print('List of selected features: \n', selected_features)
print('\nList of rejected features: \n', rejected_features)

