#!/usr/bin/env python
# coding: utf-8

# **This notebook is about handling highly imbalanced classes in a classification tasks.  
# The example is built on a fraud card transaction detection.**

# * [Download data](#id1)  
# * [Take a quick look on a dataset](#id2)  
# * [Take a closer look. Visualize](#id3)  
# * [Prepare Data](#id4)  
# * [Build Classification Model](#id5)  

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')

import os
from itertools import permutations
from collections import Counter

# data manipulation
import numpy as np 
import pandas as pd 

# charts
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

# ML models
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import roc_curve, precision_recall_fscore_support, roc_auc_score, precision_recall_curve, classification_report
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from imblearn.ensemble import BalancedRandomForestClassifier, BalancedBaggingClassifier, EasyEnsembleClassifier 
from imblearn.over_sampling import SMOTE


# # <a name="id1"></a> Download data

# In[ ]:


LOAD_DIR = '/kaggle/input/creditcardfraud'
FILENAME = 'creditcard.csv'
LOAD_PATH = os.path.join(LOAD_DIR, FILENAME)


# In[ ]:


get_ipython().run_cell_magic('time', '', 'data = pd.read_csv(LOAD_PATH)')


# # <a name="id2"></a> Take a quick look on a dataset

# In[ ]:


data.shape


# **The dataset contains 284 807 instances and 31 features (1 of them is target)**

# In[ ]:


data.head()


# In[ ]:


data.info()


# **All the data is numeric and clean.**

# In[ ]:


data.describe().round(2)


# **We see that all the *V*-features are centered (0 mean) but have different variance.  
# Percentiles also tell us that there are highly skewed and narrowed features.**

# # <a name="id3"></a> Take a closer look. Visualize

# In[ ]:


target_col = ['Class']
explicit_cols = ['Time', 'Amount']
V_cols = np.setdiff1d(data.columns, explicit_cols + target_col)
feature_cols = np.r_[V_cols, explicit_cols]


# **We have a binary classification task and it's good to know a class balance.**

# In[ ]:


class_pct = (np.bincount(data['Class']) / data.shape[0] * 100).round(2) 
print(f'normal transactions (negative class): {class_pct[0]}%')
print(f'fraud transactions (positive class): {class_pct[1]}%')
print(dict(Counter(data['Class'])))


# **Horrible! Huge imbalance! Too few a positive class data.**

# In[ ]:


def plot_density(frame, col):
    both = frame[col]
    normal = frame.loc[frame['Class'] == 0,col]
    fraud = frame.loc[frame['Class'] == 1,col]
    data = [both, normal, fraud]
    colors = ['b', 'g', 'r']
    titles = ['All transactions', 'Normal transactions', 'Fraud transactions']
    
    fig, ax = plt.subplots(1, 3, figsize=(18, 5), sharex='row')
    for axi, data, color, title in zip(ax, data, colors, titles):
        sns.distplot(data, 
                     hist=False,
                     rug=True,
                     kde_kws=dict(shade=True), 
                     color=color,
                     ax=axi)
        axi.set_title(title)


# **Take a look on distributions.**

# In[ ]:


get_ipython().run_cell_magic('time', '', "plot_density(data, 'Time')\nplot_density(data, 'Amount')")


# **As a *describe* method shown, *Amount* feature is highly skewed. I would not assert  
# that distributions for fraud and non-fraud transactions across these two variables  
# are significantly different.**

# In[ ]:


with sns.axes_style('whitegrid'):
    ax = data[V_cols].plot.box(figsize=(10, 30), vert=False);


# **This as much compact as possible visualization proves assertions about skewness and kurtosis of *V*-features.**

# # <a name="id4"></a> Prepare Data

# **The good news is that we will not do any complex data preprocessing steps. The reason  
# is that we'll use ensembles of decision trees and the thing I really like about them is  
# that they almost don't need any data prepatation steps, e.g. scaling is not required.  
# So, now we only have to split data in the training, validation and test sets using  
# stratified(!) sampling.**
# 

# ### Split Data

# In[ ]:


X = data[feature_cols].values
y = data[target_col].values.flatten()
X.shape, y.shape


# In[ ]:


def stratified_shuffle_split(X, y, train_size=None, val_size=None, test_size=None):
    assert not(train_size is None and test_size is None), 'both train_size and val_size are unfilled'
    
    if val_size is None:
        val_size = 0
    if train_size is None:
        train_size = X.shape[0] - test_size
    elif test_size is None:
        test_size = X.shape[0] - train_size
        
    assert isinstance(train_size, int) and isinstance(test_size, int) and isinstance(val_size, int),            'sizes must be integers'
    
    ssp = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=42)
    train_val_index, test_index = next(ssp.split(X, y))
    
    X_train_val = X[train_val_index]
    y_train_val = y[train_val_index]
    X_test = X[test_index]
    y_test = y[test_index]

    if val_size != 0:
        ssp2 = StratifiedShuffleSplit(n_splits=1, test_size=val_size, random_state=42)
        train_index, val_index = next(ssp2.split(X_train_val, y_train_val))
        
        X_train = X_train_val[train_index]
        y_train = y_train_val[train_index]
        X_val = X_train_val[val_index]
        y_val = y_train_val[val_index]
    
        return X_train, X_val, X_test, y_train, y_val, y_test
    else:
        X_train = X_train_val
        y_train = y_train_val
        
    return X_train, X_test, y_train, y_test


# In[ ]:


size = X.shape[0]
valid_size = int(np.ceil(size * 0.15))
test_size = int(valid_size)
train_size = int(size - valid_size - test_size)
assert train_size + valid_size + test_size == size


# In[ ]:


X_train, X_valid, X_test, y_train, y_valid, y_test = stratified_shuffle_split(X, y, train_size=train_size, test_size=test_size, val_size=valid_size)
print('shape of splits:')
print(X_train.shape, X_valid.shape, X_test.shape, y_train.shape, y_valid.shape, y_test.shape, end='\n\n')

train_abs = np.unique(y_train, return_counts=True)[1]
val_abs = np.unique(y_valid, return_counts=True)[1]
test_abs = np.unique(y_test, return_counts=True)[1]
total_abs = train_abs  + test_abs + val_abs

print('percentage of class samples per splits:')
print(train_abs / total_abs * 100)
print(test_abs / total_abs * 100)
print(test_abs / total_abs * 100)


# **Yes, even having very few positive class instances we have to hold out 30% of them!**

# # <a name="id5"></a> Build Classification Model

# **We will try two main techniques of handling imbalanced data:  
# 1) undersampling (+ balanced class weights)  
# 2) oversampling** 

# In[ ]:


def plot_classifier_roc_auc(classifier, recall_threshold=None, X_train=X_train, y_train=y_train, X_valid=X_valid, y_valid=y_valid):
    classifier.fit(X_train, y_train)
    y_valid_proba = classifier.predict_proba(X_valid)[:, 1]
    y_valid_pred = (y_valid_proba >= 0.5)

    auc = roc_auc_score(y_valid, y_valid_proba) 
    fpr, tpr, _ = roc_curve(y_valid, y_valid_proba)
    
    if recall_threshold:
        precisions, recalls, thresholds = precision_recall_curve(y_valid, y_valid_proba)
        i = np.argmin(recalls >= recall_threshold)
        recall_threshold = recalls[i]
        threshold = thresholds[i]
        y_valid_pred = (y_valid_proba >= threshold)
    else:
        precision, recall, fscore, support = precision_recall_fscore_support(y_valid, y_valid_pred)
        recall_threshold = recall[1]
    
    FPR = fpr[np.argmax(tpr >= recall_threshold)]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.plot(fpr, tpr, linewidth=2)
    ax.plot([0, 1], [0, 1], 'k--') # Dashed diagonal
    ax.hlines(recall_threshold, 0, FPR, linestyle='--', color='red')
    ax.vlines(FPR, 0, recall_threshold, linestyle='--', color='red')
    
    report = classification_report(y_valid, y_valid_pred)
    label = '\n'.join(report.split('\n')[:4]) +             '\n' + 25*" " + f'AUC = {np.round(auc, 4)}' 
    ax.scatter([FPR], [recall_threshold], s=50, c='r', label=label)
    
    ax.set_xlabel('FPR')
    ax.set_ylabel('TPR (Recall)')
    ax.set_title(classifier.__class__.__name__)
    fig.legend(loc=(0.365, 0.15))
    fig.show()


# ### Models with Undersampling

# In[ ]:


get_ipython().run_cell_magic('time', '', "classifiers_undersample =[\n    RandomForestClassifier(n_estimators=100, class_weight='balanced_subsample', random_state=0, n_jobs=-1),\n    BalancedBaggingClassifier(n_estimators=100, replacement=True, random_state=0, n_jobs=-1),\n    BalancedRandomForestClassifier(n_estimators=100, class_weight='balanced_subsample', replacement=True, random_state=0, n_jobs=-1),\n    EasyEnsembleClassifier(n_estimators=100, replacement=True, random_state=0, n_jobs=-1),\n    AdaBoostClassifier(n_estimators=100, random_state=0),\n    GradientBoostingClassifier(n_estimators=100, max_features='auto', random_state=0)\n]\n\nwith sns.axes_style('whitegrid'):\n    for classifier in classifiers_undersample:\n        print(classifier.__class__.__name__)\n        %time plot_classifier_roc_auc(classifier)\n        print()\nprint('TOTAL')")


# **Unfortunately, we see that none of the undersampling techniques helped to build a good  
# classifier, even with balancing class weights. The priority metric is positive class recall  
# and we failed to get even 90% without high drop in precision.**

# ### Models with Oversampling 

# **Let's don't try simple techniques and instantly apply smart one. The SMOTE (Synthetic  
# Minority Over-sampling Technique) is a great option.**

# In[ ]:


X_resampled, y_resampled = SMOTE().fit_resample(X_train, y_train)
Counter(y_resampled), Counter(y_train)


# **Note that we roughly doubled the size of the training set. This will increase training time**

# In[ ]:


get_ipython().run_cell_magic('time', '', "classifiers_oversample =[\n    RandomForestClassifier(n_estimators=100, random_state=0, n_jobs=-1),\n    ExtraTreesClassifier(n_estimators=100, bootstrap=True, random_state=0, n_jobs=-1),\n    AdaBoostClassifier(n_estimators=100, random_state=0),\n    GradientBoostingClassifier(n_estimators=100, max_features='auto', random_state=0)\n]\n\nwith sns.axes_style('whitegrid'):\n    for classifier in classifiers_oversample:\n        print(classifier.__class__.__name__)\n        %time plot_classifier_roc_auc(classifier, X_train=X_resampled, y_train=y_resampled)\n        print()    \nprint('TOTAL')")


# **We observe that oversampling didn't make things much better. But it worths to point out that  
# oversampling in some models resulted in a little bit better recall-precision trade-off in context  
# that high recall is more important then precision, but the last one is still important :).  
# For now, Random Forest trained on a oversampled data looks like the best ... from uglies.  
# In the next section we'll try to fit a Neural Network.**

# **coming soon ... **
