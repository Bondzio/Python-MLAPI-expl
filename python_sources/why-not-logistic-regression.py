#!/usr/bin/env python
# coding: utf-8

# ![](https://i.imgflip.com/38r5hz.jpg)

# In[ ]:


get_ipython().run_cell_magic('time', '', "\nimport pandas as pd\nimport numpy as np\n\n# Load data\ntrain = pd.read_csv('../input/cat-in-the-dat/train.csv')\ntest = pd.read_csv('../input/cat-in-the-dat/test.csv')\n\nprint(train.shape)\nprint(test.shape)")


# In[ ]:


get_ipython().run_cell_magic('time', '', "\n# Subset\ntarget = train['target']\ntrain_id = train['id']\ntest_id = test['id']\ntrain.drop(['target', 'id'], axis=1, inplace=True)\ntest.drop('id', axis=1, inplace=True)\n\nprint(train.shape)\nprint(test.shape)")


# In[ ]:


get_ipython().run_cell_magic('time', '', '\n# One Hot Encode\ntraintest = pd.concat([train, test])\ndummies = pd.get_dummies(traintest, columns=traintest.columns, drop_first=True, sparse=True)\ntrain_ohe = dummies.iloc[:train.shape[0], :]\ntest_ohe = dummies.iloc[train.shape[0]:, :]\n\nprint(train_ohe.shape)\nprint(test_ohe.shape)')


# In[ ]:


get_ipython().run_cell_magic('time', '', "\n# To be honest, I am a bit confused what is going on with the new sparse dataframe interface in Pandas v0.25\n\n# It looks like `sparse = True` in `get_dummies` no longer makes anything sparse, and we have to explicitly convert\n# like this...\n\n# If you don't do this, the model takes forever... it is much much faster on sparse data!\n\ntrain_ohe = train_ohe.sparse.to_coo().tocsr()\ntest_ohe = test_ohe.sparse.to_coo().tocsr()")


# In[ ]:


get_ipython().run_cell_magic('time', '', "\nfrom sklearn.model_selection import KFold\nfrom sklearn.metrics import roc_auc_score as auc\nfrom sklearn.linear_model import LogisticRegression\n\n# Model\ndef run_cv_model(train, test, target, model_fn, params={}, eval_fn=None, label='model'):\n    kf = KFold(n_splits=5)\n    fold_splits = kf.split(train, target)\n    cv_scores = []\n    pred_full_test = 0\n    pred_train = np.zeros((train.shape[0]))\n    i = 1\n    for dev_index, val_index in fold_splits:\n        print('Started ' + label + ' fold ' + str(i) + '/5')\n        dev_X, val_X = train[dev_index], train[val_index]\n        dev_y, val_y = target[dev_index], target[val_index]\n        params2 = params.copy()\n        pred_val_y, pred_test_y = model_fn(dev_X, dev_y, val_X, val_y, test, params2)\n        pred_full_test = pred_full_test + pred_test_y\n        pred_train[val_index] = pred_val_y\n        if eval_fn is not None:\n            cv_score = eval_fn(val_y, pred_val_y)\n            cv_scores.append(cv_score)\n            print(label + ' cv score {}: {}'.format(i, cv_score))\n        i += 1\n    print('{} cv scores : {}'.format(label, cv_scores))\n    print('{} cv mean score : {}'.format(label, np.mean(cv_scores)))\n    print('{} cv std score : {}'.format(label, np.std(cv_scores)))\n    pred_full_test = pred_full_test / 5.0\n    results = {'label': label,\n              'train': pred_train, 'test': pred_full_test,\n              'cv': cv_scores}\n    return results\n\n\ndef runLR(train_X, train_y, test_X, test_y, test_X2, params):\n    print('Train LR')\n    model = LogisticRegression(**params)\n    model.fit(train_X, train_y)\n    print('Predict 1/2')\n    pred_test_y = model.predict_proba(test_X)[:, 1]\n    print('Predict 2/2')\n    pred_test_y2 = model.predict_proba(test_X2)[:, 1]\n    return pred_test_y, pred_test_y2\n\n\nlr_params = {'solver': 'lbfgs', 'C': 0.1}\nresults = run_cv_model(train_ohe, test_ohe, target, runLR, lr_params, auc, 'lr')")


# In[ ]:


get_ipython().run_cell_magic('time', '', "\n# We now have a model with a CV score of 0.8032. Nice! Let's submit that\n\n# Make submission\nsubmission = pd.DataFrame({'id': test_id, 'target': results['test']})\nsubmission.to_csv('submission.csv', index=False)")

