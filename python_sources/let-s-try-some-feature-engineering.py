#!/usr/bin/env python
# coding: utf-8

# ![](https://i.imgflip.com/38zy2c.jpg)

# All code belongs to @peterhurford and his awesome kernel https://www.kaggle.com/peterhurford/why-not-logistic-regression/notebook
# Please, upvote it!

# In[ ]:


get_ipython().run_cell_magic('time', '', "\nimport pandas as pd\nimport numpy as np\n\n# Load data\ntrain = pd.read_csv('../input/cat-in-the-dat/train.csv')\ntest = pd.read_csv('../input/cat-in-the-dat/test.csv')\n\nprint(train.shape)\nprint(test.shape)")


# In[ ]:


get_ipython().run_cell_magic('time', '', "\n# Subset\ntarget = train['target']\ntrain_id = train['id']\ntest_id = test['id']\ntrain.drop(['target', 'id'], axis=1, inplace=True)\ntest.drop('id', axis=1, inplace=True)\n\nprint(train.shape)\nprint(test.shape)")


# In[ ]:


def count_transform(column):
    return column.map(column.value_counts().to_dict())


# In[ ]:


rang = {"Grandmaster" : 4, "Master" : 3, "Expert" : 2, "Contributor" : 1, "Novice" : 0}
temperature = {"Freezing" : 0, "Cold": 1, "Warm" : 2, "Hot": 3, "Boiling Hot" : 4, "Lava Hot" : 5}


# In[ ]:


traintest = pd.concat([train, test])


# In[ ]:


get_ipython().run_cell_magic('time', '', "from scipy.sparse import csr_matrix, hstack\n# One Hot Encode\ntraintest['ord_1_new'] = traintest['ord_1'].map(rang)\ntraintest['ord_2_new'] = traintest['ord_2'].map(temperature)\ntraintest['ord_3_new'] = traintest['ord_3'].map({val : idx for idx, val in enumerate(np.unique(traintest['ord_3']))})\ntraintest['ord_4_new'] = traintest['ord_4'].map({val : idx for idx, val in enumerate(np.unique(traintest['ord_4']))})\ntraintest['ord_5_new_1'] = traintest['ord_5'].apply(lambda x: x[0])\ntraintest['ord_5_new_1'] = traintest['ord_5_new_1'].map({val : idx for idx, val in enumerate(np.unique(traintest['ord_5_new_1']))})\ntraintest['ord_5_new_2'] = traintest['ord_5'].apply(lambda x: x[1])\ntraintest['ord_5_new_2'] = traintest['ord_5_new_2'].map({val : idx for idx, val in enumerate(np.unique(traintest['ord_5_new_2']))})\ntraintest['ord_5_new_2'] = traintest['ord_5_new_2'].map({val : idx for idx, val in enumerate(np.unique(traintest['ord_5_new_2']))})\n#traintest['new_month_sin'] = np.sin(2 * np.pi * traintest['month']/12.0)\n#traintest['new_month_sin'] = np.cos(2 * np.pi * traintest['month']/12.0)\n#traintest['new_day_sin'] = np.sin(2 * np.pi * traintest['day']/7.0)\n#traintest['new_day_sin'] = np.sin(2 * np.pi * traintest['day']/7.0)\n\ndummies = pd.get_dummies(traintest, columns=traintest.columns, drop_first=True, sparse=True).to_sparse().to_coo()\n#count_encode = csr_matrix(traintest.apply(count_transform))\ntraintest_new = csr_matrix(traintest[list(filter(lambda x: 'new' in x, traintest.columns))])")


# In[ ]:


feature_df = hstack([dummies, traintest_new]).tocsr()


# In[ ]:


train_idx = np.array(list(train.index))
train_ohe = feature_df[train_idx, :]
test_ohe = feature_df[np.max(train_idx) + np.array(list(test.index)), :]

print(train_ohe.shape)
print(test_ohe.shape)


# In[ ]:


get_ipython().run_cell_magic('time', '', 'from lightgbm import LGBMClassifier\nfrom sklearn.model_selection import KFold\nfrom sklearn.metrics import roc_auc_score as auc\nfrom sklearn.linear_model import LogisticRegression, Lasso, Ridge\nfrom sklearn.naive_bayes import BernoulliNB\nfrom sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA\n# Model\ndef run_cv_model(train, test, target, model_fn, params={}, eval_fn=None, label=\'model\'):\n    kf = KFold(n_splits=5)\n    fold_splits = kf.split(train, target)\n    cv_scores = []\n    pred_full_test = 0\n    coefs = []\n    pred_train = np.zeros((train.shape[0]))\n    i = 1\n    for dev_index, val_index in fold_splits:\n        print(\'Started \' + label + \' fold \' + str(i) + \'/5\')\n        dev_X, val_X = train[dev_index], train[val_index]\n        dev_y, val_y = target[dev_index], target[val_index]\n        params2 = params.copy()\n        trn_res = model_fn(dev_X, dev_y, val_X, val_y, test, params2)\n        pred_val_y, pred_test_y = trn_res[\'pred_val_y\'], trn_res[\'pred_test_y\']\n        pred_full_test = pred_full_test + pred_test_y\n        pred_train[val_index] = pred_val_y\n        if eval_fn is not None:\n            cv_score = eval_fn(val_y, pred_val_y)\n            cv_scores.append(cv_score)\n            coefs.append(trn_res[\'coef\'])\n            print(label + \' cv score {}: {}\'.format(i, cv_score))\n        i += 1\n    print(\'{} cv scores : {}\'.format(label, cv_scores))\n    print(\'{} cv mean score : {}\'.format(label, np.mean(cv_scores)))\n    print(\'{} cv std score : {}\'.format(label, np.std(cv_scores)))\n    pred_full_test = pred_full_test / 5.0\n    results = {\'label\': label,\n              \'train\': pred_train, \'test\': pred_full_test,\n              \'cv\': cv_scores, \n              \'coefs\' : coefs}\n    return results\n\n\ndef runLR(train_X, train_y, test_X, test_y, test_X2, params):\n    print(\'Train LR\')\n    model = LogisticRegression(**params)\n    model.fit(train_X, train_y)\n    print(\'Predict 1/2\')\n    pred_test_y = model.predict_proba(test_X)[:, 1]\n    print(\'Predict 2/2\')\n    pred_test_y2 = model.predict_proba(test_X2)[:, 1]\n    return {\'pred_val_y\' : pred_test_y, \'pred_test_y\' : pred_test_y2, \'coef\' : model.coef_}\n\ndef runRLR(train_X, train_y, test_X, test_y, test_X2, params):\n    print(\'Train LR\')\n    model = Ridge(**params)\n    model.fit(train_X, train_y)\n    print(\'Predict 1/2\')\n    pred_test_y = model.predict(test_X)\n    print(\'Predict 2/2\')\n    pred_test_y2 = model.predict(test_X2)\n    return pred_test_y, pred_test_y2\nrr_params = {\'alpha\' : 1, \'solver\': \'lsqr\', "fit_intercept" : False}\n#rr_params = {\'alpha\' : 1, \'solver\': \'sparse_cg\'}\nlr_params = {\'solver\': \'lbfgs\', \'C\': 0.1,\'max_iter\' : 1000}\nresults = run_cv_model(train_ohe, test_ohe, target, runLR, lr_params, auc, \'Ridge\')')


# In[ ]:


get_ipython().run_cell_magic('time', '', "\n# We now have a model with a CV score of 0.8032. Nice! Let's submit that\n\n# Make submission\nsubmission = pd.DataFrame({'id': test_id, 'target': results['test']})\nsubmission.to_csv('submission.csv', index=False)")


# In[ ]:




