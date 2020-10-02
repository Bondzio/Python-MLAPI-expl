#!/usr/bin/env python
# coding: utf-8

# # Apply Pseudo Labelling to best TPOT Model in the Instant Gratification Competition
# Code of this notebook is borrowed from  [Pseudo Labeling - QDA - [0.969]](https://www.kaggle.com/cdeotte/pseudo-labeling-qda-0-969). Thanks to Chris for his work. We search the best model for the first 'wheezy-copper-turtle-magic' chunck of train dataset then apply it to the whole problem. Only a small number of iterations is performed to demonstrate the workflow. 
# ## Load Data

# In[ ]:


import numpy as np, pandas as pd, os
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import VarianceThreshold
from sklearn.metrics import roc_auc_score
from tpot import TPOTClassifier
from tqdm import tqdm 
from warnings import simplefilter
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


simplefilter(action='ignore', category=FutureWarning)


train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')


# ## Step 1: Find the best TPOT Model

# In[ ]:


get_ipython().run_cell_magic('time', '', "cols = [c for c in train.columns if c not in ['id', 'target']]\ncols.remove('wheezy-copper-turtle-magic')\noof = np.zeros(len(train))\npreds = np.zeros(len(test))\n\n# ONLY TRAIN WITH DATA WHERE WHEEZY EQUALS 0\n# Change i to choose another group of train data\ni=0\ntrain2 = train[train['wheezy-copper-turtle-magic']==i]\ntest2 = test[test['wheezy-copper-turtle-magic']==i]\nidx1 = train2.index; idx2 = test2.index\ntrain2.reset_index(drop=True,inplace=True)\n\n# FEATURE SELECTION (USE APPROX 40 OF 255 FEATURES)\nsel = VarianceThreshold(threshold=1.5).fit(train2[cols])\ntrain3 = sel.transform(train2[cols])\ntest3 = sel.transform(test2[cols])\n  \n#Change generations and population_size to find better pipelines\n# Visit http://epistasislab.github.io/tpot/api/ for the API documentation\ntpot = TPOTClassifier(generations=50, population_size=30, verbosity=2, scoring='roc_auc', cv=3, max_eval_time_mins=1, random_state=42, n_jobs=-1)\ntpot.fit(train3,  train2['target'])")


# ## Step 2 - Fit the TPOT model and predict on test

# In[ ]:


get_ipython().run_cell_magic('time', '', "# INITIALIZE VARIABLES\ncols = [c for c in train.columns if c not in ['id', 'target']]\ncols.remove('wheezy-copper-turtle-magic')\noof = np.zeros(len(train))\npreds = np.zeros(len(test))\n\n# BUILD 512 SEPARATE MODELS\nfor i in tqdm(range(512)):\n    # ONLY TRAIN WITH DATA WHERE WHEEZY EQUALS I\n    train2 = train[train['wheezy-copper-turtle-magic']==i]\n    test2 = test[test['wheezy-copper-turtle-magic']==i]\n    idx1 = train2.index; idx2 = test2.index\n    train2.reset_index(drop=True,inplace=True)\n    \n    # FEATURE SELECTION (USE APPROX 40 OF 255 FEATURES)\n    sel = VarianceThreshold(threshold=1.5).fit(train2[cols])\n    train3 = sel.transform(train2[cols])\n    test3 = sel.transform(test2[cols])\n    \n    # STRATIFIED K-FOLD\n    skf = StratifiedKFold(n_splits=11, random_state=42, shuffle=True)\n    for train_index, test_index in skf.split(train3, train2['target']):\n        \n        # MODEL AND PREDICT WITH TPOT best fitted pipeline\n        tpot.fitted_pipeline_.fit(train3[train_index,:],train2.loc[train_index]['target'])\n        oof[idx1[test_index]] = tpot.fitted_pipeline_.predict_proba(train3[test_index,:])[:,1]\n        preds[idx2] += tpot.fitted_pipeline_.predict_proba(test3)[:,1] / skf.n_splits\n       \n        \n# PRINT CV AUC\nauc = roc_auc_score(train['target'],oof)\nprint('TPOT scores CV =',round(auc,5))")


# ## Step 3 & 4 - Add pseudo label data and build QDA model 

# In[ ]:


get_ipython().run_cell_magic('time', '', "# INITIALIZE VARIABLES\ntest['target'] = preds\noof = np.zeros(len(train))\npreds = np.zeros(len(test))\n\n# BUILD 512 SEPARATE MODELS\nfor k in tqdm(range(512)):\n    # ONLY TRAIN WITH DATA WHERE WHEEZY EQUALS I\n    train2 = train[train['wheezy-copper-turtle-magic']==k] \n    train2p = train2.copy(); idx1 = train2.index \n    test2 = test[test['wheezy-copper-turtle-magic']==k]\n    \n    # ADD PSEUDO LABELED DATA\n    test2p = test2[ (test2['target']<=0.01) | (test2['target']>=0.99) ].copy()\n    test2p.loc[ test2p['target']>=0.5, 'target' ] = 1\n    test2p.loc[ test2p['target']<0.5, 'target' ] = 0 \n    train2p = pd.concat([train2p,test2p],axis=0)\n    train2p.reset_index(drop=True,inplace=True)\n    \n    # FEATURE SELECTION (USE APPROX 40 OF 255 FEATURES)\n    sel = VarianceThreshold(threshold=1.5).fit(train2p[cols])     \n    train3p = sel.transform(train2p[cols])\n    train3 = sel.transform(train2[cols])\n    test3 = sel.transform(test2[cols])\n        \n    # STRATIFIED K FOLD\n    skf = StratifiedKFold(n_splits=11, random_state=42, shuffle=True)\n    for train_index, test_index in skf.split(train3p, train2p['target']):\n        test_index3 = test_index[ test_index<len(train3) ] # ignore pseudo in oof\n        \n        # MODEL AND PREDICT WITH QDA\n        clf = QuadraticDiscriminantAnalysis(reg_param=0.5)\n        clf.fit(train3p[train_index,:],train2p.loc[train_index]['target'])\n        oof[idx1[test_index3]] = clf.predict_proba(train3[test_index3,:])[:,1]\n        preds[test2.index] += clf.predict_proba(test3)[:,1] / skf.n_splits\n               \n# PRINT CV AUC\nauc = roc_auc_score(train['target'],oof)\nprint('QDA scores CV =',round(auc,5))")


# ## Submit Predictions

# In[ ]:


sub = pd.read_csv('../input/sample_submission.csv')
sub['target'] = preds
sub.to_csv('submission.csv',index=False)

import matplotlib.pyplot as plt
plt.hist(preds,bins=100)
plt.title('Final Test.csv predictions')
plt.show()

