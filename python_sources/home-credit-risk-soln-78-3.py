#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn as sb
get_ipython().run_line_magic('matplotlib', 'inline')

import os
import glob


# In[ ]:


data = pd.read_csv('../input/application_train.csv')
test = pd.read_csv('../input/application_test.csv')
prev = pd.read_csv('../input/previous_application.csv')
buro = pd.read_csv('../input/bureau.csv')
buro_balance = pd.read_csv('../input/bureau_balance.csv')
credit_card = pd.read_csv('../input/credit_card_balance.csv')
POS_CASH = pd.read_csv('../input/POS_CASH_balance.csv')
payments = pd.read_csv('../input/installments_payments.csv')


# In[ ]:


from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold


# In[ ]:


import xgboost as xgb
from xgboost import XGBClassifier

import gc


# In[ ]:


from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix
from sklearn.feature_selection import VarianceThreshold


# In[ ]:


from sklearn.model_selection import GridSearchCV
from skopt import BayesSearchCV
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold


# In[ ]:


def status_print(optim_result):
    """Status callback durring bayesian hyperparameter search"""
    
    # Get all the models tested so far in DataFrame format
    all_models = pd.DataFrame(bayes_cv_tuner.cv_results_)    
    
    # Get current parameters and the best parameters    
    best_params = pd.Series(bayes_cv_tuner.best_params_)
    print('Model #{}\nBest ROC-AUC: {}\nBest params: {}\n'.format(
        len(all_models),
        np.round(bayes_cv_tuner.best_score_, 4),
        bayes_cv_tuner.best_params_
    ))
    
    # Save all model results
    clf_name = bayes_cv_tuner.estimator.__class__.__name__
    all_models.to_csv(clf_name+"_cv_results.csv")


# In[ ]:


data.head()


# In[ ]:


#Separate target variable
y = data['TARGET']
del data['TARGET']


# In[ ]:


#One-hot encoding of categorical features in data and test sets
categorical_feature = [col for col in data.columns if data[col].dtype == 'object']


# In[ ]:


categorical_feature


# # Examine missing value

# In[ ]:


# Function to calculate missing values by column# Funct 
def missing_values_table(df):
        # Total missing values
        mis_val = df.isnull().sum()
        
        # Percentage of missing values
        mis_val_percent = 100 * df.isnull().sum() / len(df)
        
        # Make a table with the results
        mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        
        # Rename the columns
        mis_val_table_ren_columns = mis_val_table.rename(
        columns = {0 : 'Missing Values', 1 : '% of Total Values'})
        
        # Sort the table by percentage of missing descending
        mis_val_table_ren_columns = mis_val_table_ren_columns[
            mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
        
        # Print some summary information
        print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
            "There are " + str(mis_val_table_ren_columns.shape[0]) +
              " columns that have missing values.")
        
        # Return the dataframe with missing information
        return mis_val_table_ren_columns


# In[ ]:


# Missing values statistics
missing_values = missing_values_table(data)
missing_values.head(20)


# In[ ]:


data.dtypes.value_counts()


# In[ ]:


# Number of unique classes in each object column
#app_train.select_dtypes('object').apply(pd.Series.nunique, axis = 0) or
data.select_dtypes('object').nunique()


# In[ ]:


data.shape, test.shape


# In[ ]:


one_hot_df = pd.concat([data, test])


# In[ ]:


one_hot_df = pd.get_dummies(one_hot_df, columns=categorical_feature)


# In[ ]:


one_hot_df.shape


# In[ ]:


one_hot_df.head()


# In[ ]:


data = one_hot_df.iloc[:data.shape[0],:]
test = one_hot_df.iloc[data.shape[0]:,]


# In[ ]:


data.shape, test.shape


# In[ ]:


test.head()


# In[ ]:


data.head()


# In[ ]:


buro.head()


# #Pre-processing buro_balance

# In[ ]:


buro_grouped_size = buro_balance.groupby('SK_ID_BUREAU')['MONTHS_BALANCE'].size()
buro_grouped_max = buro_balance.groupby('SK_ID_BUREAU')['MONTHS_BALANCE'].max()
buro_grouped_min = buro_balance.groupby('SK_ID_BUREAU')['MONTHS_BALANCE'].min()


# In[ ]:


buro_grouped_size.head(),  buro_grouped_max.head(),   buro_grouped_min.head()


# In[ ]:


buro_balance.head()


# In[ ]:


buro_counts = buro_balance.groupby('SK_ID_BUREAU')['STATUS'].value_counts(normalize = False)


# In[ ]:


buro_balance.shape


# In[ ]:


buro_counts.head()


# In[ ]:


buro_counts_unstacked = buro_counts.unstack('STATUS')
buro_counts_unstacked.head()


# In[ ]:


buro_counts_unstacked.columns = ['STATUS_0', 'STATUS_1','STATUS_2','STATUS_3','STATUS_4','STATUS_5','STATUS_C','STATUS_X']
buro_counts_unstacked['MONTHS_COUNT'] = buro_grouped_size
buro_counts_unstacked['MONTHS_MIN'] = buro_grouped_min
buro_counts_unstacked['MONTHS_MAX'] = buro_grouped_max


# In[ ]:


buro_grouped_size.head(),  buro_grouped_max.head(),   buro_grouped_min.head()


# In[ ]:


buro = buro.join(buro_counts_unstacked, how ='left', on ='SK_ID_BUREAU')


# In[ ]:


buro.head()


# 
# Pre-processing previous_application

# In[ ]:


prev_cat_features = [pcol for pcol in prev.columns if prev[pcol].dtype == 'object']


# In[ ]:


prev_cat_features


# In[ ]:


prev.head()


# In[ ]:


prev.shape


# In[ ]:


prev = pd.get_dummies(prev, columns=prev_cat_features)


# In[ ]:


prev.head()


# In[ ]:


avg_prev = prev.groupby('SK_ID_CURR').mean()


# In[ ]:


avg_prev.head()


# In[ ]:


avg_prev.shape


# In[ ]:


cnt_prev = prev[['SK_ID_CURR', 'SK_ID_PREV']].groupby('SK_ID_CURR').count()


# In[ ]:


cnt_prev.head(),  cnt_prev.shape


# In[ ]:


avg_prev['nb_app'] = cnt_prev['SK_ID_PREV']


# In[ ]:


del avg_prev['SK_ID_PREV']


# 
# #Pre-processing buro

# In[ ]:


#One-hot encoding of categorical features in buro data set

buro_cat_features = [bcol for bcol in buro.columns if buro[bcol].dtype == 'object']
buro_cat_features 


# In[ ]:


buro = pd.get_dummies(buro, columns=buro_cat_features)


# In[ ]:


buro.head()


# In[ ]:


avg_buro = buro.groupby('SK_ID_CURR').mean()


# In[ ]:


avg_buro.head()


# In[ ]:


avg_buro['buro_count'] = buro[['SK_ID_BUREAU', 'SK_ID_CURR']].groupby('SK_ID_CURR').count()['SK_ID_BUREAU']
del avg_buro['SK_ID_BUREAU']


# 
# #Pre-processing POS_CASH

# In[ ]:


POS_CASH.head()


# In[ ]:


POS_CASH.shape


# In[ ]:


le = LabelEncoder()
POS_CASH['NAME_CONTRACT_STATUS'] = le.fit_transform(POS_CASH['NAME_CONTRACT_STATUS'].astype(str))
nunique_status = POS_CASH[['SK_ID_CURR', 'NAME_CONTRACT_STATUS']].groupby('SK_ID_CURR').nunique()
nunique_status2 = POS_CASH[['SK_ID_CURR', 'NAME_CONTRACT_STATUS']].groupby('SK_ID_CURR').max()
POS_CASH['NUNIQUE_STATUS'] = nunique_status['NAME_CONTRACT_STATUS']
POS_CASH['NUNIQUE_STATUS2'] = nunique_status2['NAME_CONTRACT_STATUS']
POS_CASH.drop(['SK_ID_PREV', 'NAME_CONTRACT_STATUS'], axis=1, inplace=True)


# 
# #Pre-processing credit_card

# In[ ]:


credit_card.head()


# In[ ]:


credit_card_cat_features = [c_col for c_col in credit_card.columns if credit_card[c_col].dtype == 'object']
credit_card_cat_features 


# In[ ]:


credit_card.shape


# In[ ]:


credit_card['NAME_CONTRACT_STATUS'] = le.fit_transform(credit_card['NAME_CONTRACT_STATUS'].astype(str))
nunique_status = credit_card[['SK_ID_CURR', 'NAME_CONTRACT_STATUS']].groupby('SK_ID_CURR').nunique()
nunique_status2 = credit_card[['SK_ID_CURR', 'NAME_CONTRACT_STATUS']].groupby('SK_ID_CURR').max()
credit_card['NUNIQUE_STATUS'] = nunique_status['NAME_CONTRACT_STATUS']
credit_card['NUNIQUE_STATUS2'] = nunique_status2['NAME_CONTRACT_STATUS']
credit_card.drop(['SK_ID_PREV', 'NAME_CONTRACT_STATUS'], axis=1, inplace=True)


# 
# #Pre-processing payments

# In[ ]:


payments.head()


# In[ ]:


payments.shape


# In[ ]:


avg_payments = payments.groupby('SK_ID_CURR').mean()
avg_payments2 = payments.groupby('SK_ID_CURR').max()
avg_payments3 = payments.groupby('SK_ID_CURR').min()
del avg_payments['SK_ID_PREV']


# 
# #Join data bases

# In[ ]:


data = data.merge(right=avg_prev.reset_index(), how='left', on ='SK_ID_CURR')


# In[ ]:


data.head()


# In[ ]:


test = test.merge(right=avg_prev.reset_index(), how='left', on='SK_ID_CURR')


# In[ ]:


test.head()


# In[ ]:


data = data.merge(right=avg_buro.reset_index(), how='left', on='SK_ID_CURR')
test = test.merge(right=avg_buro.reset_index(), how='left', on='SK_ID_CURR')


# In[ ]:


data = data.merge(POS_CASH.groupby('SK_ID_CURR').mean().reset_index(), how='left', on='SK_ID_CURR')
test = test.merge(POS_CASH.groupby('SK_ID_CURR').mean().reset_index(), how='left', on='SK_ID_CURR')


# In[ ]:


data = data.merge(credit_card.groupby('SK_ID_CURR').mean().reset_index(), how='left', on='SK_ID_CURR')
test = test.merge(credit_card.groupby('SK_ID_CURR').mean().reset_index(), how='left', on='SK_ID_CURR')


# In[ ]:


data = data.merge(right=avg_payments.reset_index(), how='left', on='SK_ID_CURR')
test = test.merge(right=avg_payments.reset_index(), how='left', on='SK_ID_CURR')


# In[ ]:


data = data.merge(right=avg_payments2.reset_index(), how='left', on='SK_ID_CURR')
test = test.merge(right=avg_payments2.reset_index(), how='left', on='SK_ID_CURR')


# In[ ]:


data = data.merge(right=avg_payments3.reset_index(), how='left', on='SK_ID_CURR')
test = test.merge(right=avg_payments3.reset_index(), how='left', on='SK_ID_CURR')


# In[ ]:


data.shape, test.shape


# In[ ]:


data.head()


# In[ ]:


test.head()


# 
# #Remove features with many missing values

# In[ ]:


test = test[test.columns[data.isnull().mean() < 0.80]]
data = data[data.columns[data.isnull().mean() < 0.80]]


# In[ ]:


data.head()


# In[ ]:


from lightgbm import LGBMClassifier
import gc

gc.enable()

folds = KFold(n_splits=5, shuffle=True, random_state=546789)
oof_preds = np.zeros(data.shape[0])
sub_preds = np.zeros(test.shape[0])

feature_importance_df = pd.DataFrame()

feats = [f for f in data.columns if f not in ['SK_ID_CURR']]

for n_fold, (trn_idx, val_idx) in enumerate(folds.split(data)):
    trn_x, trn_y = data[feats].iloc[trn_idx], y.iloc[trn_idx]
    val_x, val_y = data[feats].iloc[val_idx], y.iloc[val_idx]
    
    clf = LGBMClassifier(
        n_estimators=10000,
        learning_rate=0.02,
        num_leaves=255,
        colsample_bytree=0.81,
        subsample=0.82,
        max_depth = 8,
        reg_alpha=.1,
        reg_lambda=.1,
        min_split_gain=.01,
        #min_child_weight=250,
        min_sum_hessian_in_leaf = 150,
        silent=-1,
        verbose=-1,
        )
    
    clf.fit(trn_x, trn_y, 
            eval_set= [(trn_x, trn_y), (val_x, val_y)], 
            eval_metric='auc', verbose=100, early_stopping_rounds=200  #30
           )
    
    oof_preds[val_idx] = clf.predict_proba(val_x, num_iteration=clf.best_iteration_)[:, 1]
    sub_preds += clf.predict_proba(test[feats], num_iteration=clf.best_iteration_)[:, 1] / folds.n_splits
    
    fold_importance_df = pd.DataFrame()
    fold_importance_df["feature"] = feats
    fold_importance_df["importance"] = clf.feature_importances_
    fold_importance_df["fold"] = n_fold + 1
    feature_importance_df = pd.concat([feature_importance_df, fold_importance_df], axis=0)
    
    print('Fold %2d AUC : %.6f' % (n_fold + 1, roc_auc_score(val_y, oof_preds[val_idx])))
    del clf, trn_x, trn_y, val_x, val_y
    gc.collect()


# In[ ]:


print('Full AUC score %.6f' % roc_auc_score(y, oof_preds)) 


# In[ ]:


test['TARGET'] = sub_preds

test[['SK_ID_CURR', 'TARGET']].to_csv('home_risk_1submission.csv', index=False)


# In[ ]:




