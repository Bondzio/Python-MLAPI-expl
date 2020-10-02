#!/usr/bin/env python
# coding: utf-8

# Reference:  
# https://www.kaggle.com/peterhurford/why-not-logistic-regression  
# https://www.kaggle.com/superant/oh-my-cat  
# 
# Just enter this competition and read the above kernels. This notebook is modified from the references. Approaches therein are simple feature engineering and logistic regression, which is elegant. Keep exploring more advanced approach.

# In[ ]:


get_ipython().run_cell_magic('time', '', "\nimport pandas as pd\nimport numpy as np\n\n# Load data\ntrain = pd.read_csv('../input/cat-in-the-dat/train.csv')\ntest = pd.read_csv('../input/cat-in-the-dat/test.csv')\n\nprint(train.shape)\nprint(test.shape)")


# In[ ]:


get_ipython().run_cell_magic('time', '', "\n# Subset\ntarget = train['target'].values\ntrain_id = train['id'].tolist()\ntest_id = test['id'].tolist()\ntrain.drop(['target', 'id'], axis=1, inplace=True)\ntest.drop('id', axis=1, inplace=True)\n\nprint(train.shape)\nprint(test.shape)")


# Some simple preprocessing and feature engineering

# In[ ]:


def reduce_dim(df, column):
    # summarize those showing only once to one category
    for index, dup in df[column].duplicated(keep=False).iteritems():
        if dup == False:
            df.at[index, column] = -1
    # re-index
    new_index = {idx:i for i, idx in enumerate(df[column].unique())}
    df[column] = df[column].map(new_index)
    return df


def data_treatment(df):
    for col in list(df.columns):
        if col.startswith('bin'):
            bins = df[col].unique()
            df[col] = df[col].map({bins[0]:0, bins[1]:1}).astype('int8')
    
    df['ord_5'] = df['ord_5'].str[0]
    df['isweekend'] = (df['day'] >= 5).astype('int8')
    
    return df


# In[ ]:


get_ipython().run_cell_magic('time', '', '\n# Preprocessing\nwhole = pd.concat([train, test])\nwhole = data_treatment(whole)\n\ncat_cols = whole.columns[5:-1]\nnon_cat_cols = list(set(whole.columns)-set(cat_cols))\nfor category in cat_cols:\n    whole = reduce_dim(whole, category)')


# Rather than using pd.get_dummies(), OneHotEncoder in sklearn could be much faster with the sparse output.

# In[ ]:


get_ipython().run_cell_magic('time', '', "\n# One-hot encoding\nfrom sklearn.preprocessing import OneHotEncoder\nfrom scipy.sparse import hstack\n\nenc = OneHotEncoder(handle_unknown='ignore')\nenc = enc.fit(whole[cat_cols])\nwhole_ohe = enc.transform(whole[cat_cols])\nwhole_ohe = hstack((whole_ohe, whole[non_cat_cols]))\nwhole_ohe = whole_ohe.tocsr()\n\ntrain_ohe = whole_ohe[:train.shape[0], :]\ntest_ohe = whole_ohe[train.shape[0]:, :]\n\nprint(train_ohe.shape)\nprint(test_ohe.shape)")


# In[ ]:


get_ipython().run_cell_magic('time', '', "\nfrom sklearn.model_selection import KFold, StratifiedKFold\nfrom sklearn.metrics import roc_auc_score as auc\nfrom sklearn.linear_model import LogisticRegression\n\n# Model\ndef run_cv_model(train, test, target, model_fn, params={}, eval_fn=None, model_type='logreg'):\n    kf = StratifiedKFold(n_splits=5)\n    fold_splits = kf.split(train, target)\n    \n    trn_scores = []\n    cv_scores = []\n    pred_oof = np.zeros((train.shape[0]))\n    pred_full_test = 0\n    \n    for i, (dev_index, val_index) in enumerate(fold_splits, 1):\n        print(f'Start fold {i}/5')\n        trn_X, val_X = train[dev_index], train[val_index]\n        trn_y, val_y = target[dev_index], target[val_index]\n        pred_trn, pred_val, pred_test = model_fn(trn_X, trn_y, val_X, val_y, test, params)\n        pred_oof[val_index] = pred_val\n        pred_full_test += pred_test / 5.0\n        if eval_fn is not None:\n            trn_sc = eval_fn(trn_y, pred_trn)\n            cv_sc = eval_fn(val_y, pred_val)\n            trn_scores.append(trn_sc)\n            cv_scores.append(cv_sc)\n            print(f'trn score {i}: {trn_sc}')\n            print(f'cv score {i}: {cv_sc}')\n            print()\n    \n    print(f'trn scores : {trn_scores}')\n    print(f'trn mean score : {np.mean(trn_scores)}')\n    print(f'trn std score : {np.std(trn_scores)}')\n    print()\n    \n    print(f'oof cv scores : {eval_fn(target, pred_oof)}')\n    print(f'cv scores : {cv_scores}')\n    print(f'cv mean score : {np.mean(cv_scores)}')\n    print(f'cv std score : {np.std(cv_scores)}')\n    print()\n    \n    results = {'model_type': model_type,\n               'pred_oof': pred_oof, 'pred_test': pred_full_test,\n               'trn_scores': trn_scores, 'cv_scores': cv_scores}\n    \n    return results\n\n\ndef runLR(train_X, train_y, val_X, val_y, test_X, params):\n    print('Training Logistic Regression...')\n    model = LogisticRegression(**params)\n    model.fit(train_X, train_y)\n    print('Predicting 1/3...')\n    pred_trn = model.predict_proba(train_X)[:, 1]\n    print('Predicting 2/3...')\n    pred_val = model.predict_proba(val_X)[:, 1]\n    print('Predicting 3/3...')\n    pred_test = model.predict_proba(test_X)[:, 1]\n    return pred_trn, pred_val, pred_test\n\n\nlr_params = {'solver': 'lbfgs', 'C': 0.1, 'max_iter': 1000}\nresults = run_cv_model(train_ohe, test_ohe, target, runLR, lr_params, auc)")


# In[ ]:


# Make submission

submission = pd.DataFrame({'id': test_id, 'target': results['pred_test']})
submission.to_csv('submission.csv', index=False)

