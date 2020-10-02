#!/usr/bin/env python
# coding: utf-8

# Useful links:
# * https://www.kaggle.com/kyakovlev/ieee-gb-2-make-amount-useful-again
# * https://www.kaggle.com/vincentlugat/ieee-catboost-gpu-baseline-5-kfold
# 
# 
# https://www.kaggle.com/luisfredgs/ieee-cis-fraud-detection-catboost?scriptVersionId=18955915 - 0.9322
# https://www.kaggle.com/luisfredgs/ieee-cis-fraud-detection-catboost?scriptVersionId=18995695 - 0.9373

# In[ ]:


import numpy as np 
import pandas as pd 
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold
from bayes_opt import BayesianOptimization
from datetime import datetime
from sklearn.metrics import precision_score, recall_score, confusion_matrix, accuracy_score, roc_auc_score, f1_score, roc_curve, auc,precision_recall_curve

from sklearn import metrics
from sklearn import preprocessing
import catboost
from catboost import Pool
import warnings
warnings.filterwarnings("ignore")
import itertools
from scipy import interp

# Plots
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import rcParams

#Timer
def timer(start_time=None):
    if not start_time:
        start_time = datetime.now()
        return start_time
    elif start_time:
        thour, temp_sec = divmod((datetime.now() - start_time).total_seconds(), 3600)
        tmin, tsec = divmod(temp_sec, 60)
        print('Time taken for Modeling: %i hours %i minutes and %s seconds.' % (thour, tmin, round(tsec, 2)))


# ## DATASETS

# In[ ]:


get_ipython().run_cell_magic('time', '', "train_transaction = pd.read_csv('../input/train_transaction.csv', index_col='TransactionID')\ntest_transaction = pd.read_csv('../input/test_transaction.csv', index_col='TransactionID')\ntrain_identity = pd.read_csv('../input/train_identity.csv', index_col='TransactionID')\ntest_identity = pd.read_csv('../input/test_identity.csv', index_col='TransactionID')\nsample_submission = pd.read_csv('../input/sample_submission.csv', index_col='TransactionID')")


# ## MERGE, MISSING VALUE, FILL NA

# In[ ]:


# merge 
train_df = train_transaction.merge(train_identity, how='left', left_index=True, right_index=True)
test_df = test_transaction.merge(test_identity, how='left', left_index=True, right_index=True)

print("Train shape : "+str(train_df.shape))
print("Test shape  : "+str(test_df.shape))


# In[ ]:


train_df["diff_V319_V320"] = np.zeros(train_df.shape[0])

train_df.loc[train_df["V319"]!=train_df["V320"],"diff_V319_V320"] = 1

test_df["diff_V319_V320"] = np.zeros(test_df.shape[0])

test_df.loc[test_df["V319"]!=test_df["V320"],"diff_V319_V320"] = 1

train_df["diff_V109_V110"] = np.zeros(train_df.shape[0])

train_df.loc[train_df["V109"]!=train_df["V110"],"diff_V109_V110"] = 1

test_df["diff_V109_V110"] = np.zeros(test_df.shape[0])

test_df.loc[test_df["V109"]!=test_df["V110"],"diff_V109_V110"] = 1


# In[ ]:


pd.set_option('display.max_columns', 500)


# In[ ]:


# GPreda, missing data
def missing_data(data):
    total = data.isnull().sum()
    percent = (data.isnull().sum()/data.isnull().count()*100)
    tt = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    types = []
    for col in data.columns:
        dtype = str(data[col].dtype)
        types.append(dtype)
    tt['Types'] = types
    return(np.transpose(tt))


# In[ ]:


display(missing_data(train_df), missing_data(test_df))


# In[ ]:


#fillna
train_df = train_df.fillna(-999)
test_df = test_df.fillna(-999)


# # Make day and hour features

# In[ ]:


# From https://www.kaggle.com/fchmiel/day-and-time-powerful-predictive-feature

def make_day_feature(df, offset=0.58, tname='TransactionDT'):
    """
    Creates a day of the week feature, encoded as 0-6.
    """
    days = df[tname] / (3600 * 24)
    encoded_days = np.floor(days - 1 + offset) % 7
    return encoded_days

def make_hour_feature(df, tname='TransactionDT'):
    """
    Creates an hour of the day feature, encoded as 0-23.
    """
    hours = df[tname] / (3600)
    encoded_hours = np.floor(hours) % 24
    return encoded_hours


# In[ ]:


plt.hist(train_df['TransactionDT'] / (3600 * 24), bins=1800)
plt.xlim(70, 78)
plt.xlabel('Days')
plt.ylabel('Number of transactions')
plt.ylim(0,1000)


# In[ ]:


train_df['Weekday'] = make_day_feature(train_df)
train_df['Hour'] = make_hour_feature(train_df)


# In[ ]:


plt.plot(train_df.groupby('Hour').mean()['isFraud'])
plt.xlabel('Encoded hour')
plt.ylabel('Fraction of fraudulent transactions')


# In[ ]:


test_df['Weekday'] = make_day_feature(test_df)
test_df['Hour'] = make_hour_feature(test_df)


# # Remove timestamp

# In[ ]:


train_df = train_df.sort_values('TransactionDT').drop('TransactionDT', axis=1)
test_df = test_df.sort_values('TransactionDT').drop('TransactionDT', axis=1)


# In[ ]:


del train_transaction, train_identity, test_transaction, test_identity


# # Frequence encoding

# In[ ]:


i_cols = ['card1','card2','card3','card5',
          'C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12','C13','C14',
          'D1','D2','D3','D4','D5','D6','D7','D8','D9',
          'addr1','addr2',
          'dist1','dist2',
          'P_emaildomain', 'R_emaildomain'
         ]

for col in i_cols:
    if col in train_df and col in test_df:
        temp_df = pd.concat([train_df[[col]], test_df[[col]]])
        fq_encode = temp_df[col].value_counts().to_dict()   
        train_df[col+'_fq_enc'] = train_df[col].map(fq_encode)
        test_df[col+'_fq_enc']  = test_df[col].map(fq_encode)


# # Check if Transaction Amount is common or not

# In[ ]:


get_ipython().run_cell_magic('time', '', "# Check if Transaction Amount is common or not (we can use freq encoding here)\n# In our dialog with model we are telling to trust or not to these values  \nvalid_card = train_df['TransactionAmt'].value_counts()\nvalid_card = valid_card[valid_card>10]\nvalid_card = list(valid_card.index)\n    \ntrain_df['TransactionAmt_check'] = np.where(train_df['TransactionAmt'].isin(test_df['TransactionAmt']), 1, 0)\ntest_df['TransactionAmt_check']  = np.where(test_df['TransactionAmt'].isin(train_df['TransactionAmt']), 1, 0)\n\n# For our model current TransactionAmt is a noise (even when features importances are telling contrariwise)\n# There are many unique values and model doesn't generalize well\n# Lets do some aggregations\ni_cols = ['card1','card2','card3','card5']\n\nfor col in i_cols:\n    for agg_type in ['mean', 'std']:\n        new_col_name = col+'_TransactionAmt_'+agg_type\n        temp_df = pd.concat([train_df[[col, 'TransactionAmt']], test_df[[col,'TransactionAmt']]])\n        temp_df = temp_df.groupby([col])['TransactionAmt'].agg([agg_type]).reset_index().rename(\n                                                columns={agg_type: new_col_name})\n        \n        temp_df.index = list(temp_df[col])\n        temp_df = temp_df[new_col_name].to_dict()   \n    \n        train_df[new_col_name] = train_df[col].map(temp_df)\n        test_df[new_col_name]  = test_df[col].map(temp_df)")


# # Anomaly Search in geo information

# In[ ]:


get_ipython().run_cell_magic('time', '', "# Let's look on bank addres and client addres matching\n# card3/card5 bank country and name?\n# Addr2 -> Clients geo position (country)\n# Most common entries -> normal transactions\n# Less common etries -> some anonaly\n\ntrain_df['bank_type'] = train_df['card3'].astype(str)+'_'+train_df['card5'].astype(str)\ntest_df['bank_type']  = test_df['card3'].astype(str)+'_'+test_df['card5'].astype(str)\n\ntrain_df['address_match'] = train_df['bank_type'].astype(str)+'_'+train_df['addr2'].astype(str)\ntest_df['address_match']  = test_df['bank_type'].astype(str)+'_'+test_df['addr2'].astype(str)\n\nfor col in ['address_match','bank_type']:\n    temp_df = pd.concat([train_df[[col]], test_df[[col]]])\n    temp_df[col] = np.where(temp_df[col].str.contains('nan'), np.nan, temp_df[col])\n    temp_df = temp_df.dropna()\n    fq_encode = temp_df[col].value_counts().to_dict()   \n    train_df[col] = train_df[col].map(fq_encode)\n    test_df[col]  = test_df[col].map(fq_encode)\n\ntrain_df['address_match'] = train_df['address_match']/train_df['bank_type'] \ntest_df['address_match']  = test_df['address_match']/test_df['bank_type']")


# ## ENCODING

# In[ ]:


# Label Encoding
for f in train_df.columns:
    if  train_df[f].dtype=='object': 
        lbl = preprocessing.LabelEncoder()
        lbl.fit(list(train_df[f].values) + list(test_df[f].values))
        train_df[f] = lbl.transform(list(train_df[f].values))
        test_df[f] = lbl.transform(list(test_df[f].values))  
train_df = train_df.reset_index()
test_df = test_df.reset_index()


# In[ ]:


features = list(train_df)
features.remove('isFraud')
features.remove('bank_type')
target = 'isFraud'


# ## CONFUSION MATRIX

# In[ ]:


# Confusion matrix 
def plot_confusion_matrix(cm, classes,
                          normalize = False,
                          title = 'Confusion matrix"',
                          cmap = plt.cm.Blues) :
    plt.imshow(cm, interpolation = 'nearest', cmap = cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation = 0)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])) :
        plt.text(j, i, cm[i, j],
                 horizontalalignment = 'center',
                 color = 'white' if cm[i, j] > thresh else 'black')
 
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


# In[ ]:


param_cb = {
        'learning_rate': 0.2,
        'bagging_temperature': 0.1, 
        'l2_leaf_reg': 30,
        'depth': 12, 
        #'max_leaves': 48,
        'max_bin':255,
        'iterations' : 1000,
        'task_type':'GPU',
        'loss_function' : "Logloss",
        'objective':'CrossEntropy',
        'eval_metric' : "AUC",
        'bootstrap_type' : 'Bayesian',
        'random_seed':1337,
        'early_stopping_rounds' : 100,
        'use_best_model': True 
}


# In[ ]:





# ## CV 7 FOLDS AND METRICS

# In[ ]:


print('CatBoost GPU modeling...')
start_time = timer(None)
plt.rcParams["axes.grid"] = True

nfold = 7
skf = StratifiedKFold(n_splits=nfold, shuffle=True, random_state=42)

oof = np.zeros(len(train_df))
mean_fpr = np.linspace(0,1,100)
cms= []
tprs = []
aucs = []
y_real = []
y_proba = []
recalls = []
roc_aucs = []
f1_scores = []
accuracies = []
precisions = []
predictions = np.zeros(len(test_df))
feature_importance_df = pd.DataFrame()

i = 1
for train_idx, valid_idx in skf.split(train_df, train_df.isFraud.values):
    print("\nfold {}".format(i))

    
    trn_data = Pool(train_df.iloc[train_idx][features].values,label=train_df.iloc[train_idx][target].values)
    val_data = Pool(train_df.iloc[valid_idx][features].values,label=train_df.iloc[valid_idx][target].values)   

    clf = catboost.train(trn_data, param_cb, eval_set= val_data, verbose = 300)

    oof[valid_idx]  = clf.predict(train_df.iloc[valid_idx][features].values)   
    oof[valid_idx]  = np.exp(oof[valid_idx]) / (1 + np.exp(oof[valid_idx]))
    
    predictions += clf.predict(test_df[features]) / nfold
    predictions = np.exp(predictions)/(1 + np.exp(predictions))
    
    # Scores 
    roc_aucs.append(roc_auc_score(train_df.iloc[valid_idx][target].values, oof[valid_idx]))
    accuracies.append(accuracy_score(train_df.iloc[valid_idx][target].values, oof[valid_idx].round()))
    recalls.append(recall_score(train_df.iloc[valid_idx][target].values, oof[valid_idx].round()))
    precisions.append(precision_score(train_df.iloc[valid_idx][target].values ,oof[valid_idx].round()))
    f1_scores.append(f1_score(train_df.iloc[valid_idx][target].values, oof[valid_idx].round()))
    
    # Roc curve by fold
    f = plt.figure(1)
    fpr, tpr, t = roc_curve(train_df.iloc[valid_idx][target].values, oof[valid_idx])
    tprs.append(interp(mean_fpr, fpr, tpr))
    roc_auc = auc(fpr, tpr)
    aucs.append(roc_auc)
    plt.plot(fpr, tpr, lw=2, alpha=0.3, label='ROC fold %d (AUC = %0.4f)' % (i,roc_auc))

    # Precion recall by folds
    g = plt.figure(2)
    precision, recall, _ = precision_recall_curve(train_df.iloc[valid_idx][target].values, oof[valid_idx])
    y_real.append(train_df.iloc[valid_idx][target].values)
    y_proba.append(oof[valid_idx])
    plt.plot(recall, precision, lw=2, alpha=0.3, label='P|R fold %d' % (i))  
    
    i= i+1
    
    # Confusion matrix by folds
    cms.append(confusion_matrix(train_df.iloc[valid_idx][target].values, oof[valid_idx].round()))
    
    # Features imp
    fold_importance_df = pd.DataFrame()
    fold_importance_df["Feature"] = features
    fold_importance_df["importance"] = clf.get_feature_importance()
    fold_importance_df["fold"] = nfold + 1
    feature_importance_df = pd.concat([feature_importance_df, fold_importance_df], axis=0)

# Metrics
print(
        '\nCV roc score        : {0:.4f}, std: {1:.4f}.'.format(np.mean(roc_aucs), np.std(roc_aucs)),
        '\nCV accuracy score   : {0:.4f}, std: {1:.4f}.'.format(np.mean(accuracies), np.std(accuracies)),
        '\nCV recall score     : {0:.4f}, std: {1:.4f}.'.format(np.mean(recalls), np.std(recalls)),
        '\nCV precision score  : {0:.4f}, std: {1:.4f}.'.format(np.mean(precisions), np.std(precisions)),
        '\nCV f1 score         : {0:.4f}, std: {1:.4f}.'.format(np.mean(f1_scores), np.std(f1_scores))
)

#ROC
f = plt.figure(1)
plt.plot([0,1],[0,1],linestyle = '--',lw = 2,color = 'grey')
mean_tpr = np.mean(tprs, axis=0)
mean_auc = auc(mean_fpr, mean_tpr)
plt.plot(mean_fpr, mean_tpr, color='blue',
         label=r'Mean ROC (AUC = %0.4f)' % (np.mean(roc_aucs)),lw=2, alpha=1)

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Catboost ROC curve by folds')
plt.legend(loc="lower right")

# PR plt
g = plt.figure(2)
plt.plot([0,1],[1,0],linestyle = '--',lw = 2,color = 'grey')
y_real = np.concatenate(y_real)
y_proba = np.concatenate(y_proba)
precision, recall, _ = precision_recall_curve(y_real, y_proba)
plt.plot(recall, precision, color='blue',
         label=r'Mean P|R')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Catboost P|R curve by folds')
plt.legend(loc="lower left")

# Confusion maxtrix & metrics
plt.rcParams["axes.grid"] = False
cm = np.average(cms, axis=0)
class_names = [0,1]
plt.figure()
plot_confusion_matrix(cm, 
                      classes=class_names, 
                      title= 'CatBoost Confusion matrix [averaged/folds]')
# Timer end    
timer(start_time)


# In[ ]:





# # <a id='3'>3. Feature importance</a> 

# In[ ]:


"""
plt.style.use('dark_background')
cols = (feature_importance_df[["Feature", "importance"]]
    .groupby("Feature")
    .mean()
    .sort_values(by="importance", ascending=False)[:30].index)
best_features = feature_importance_df.loc[feature_importance_df.Feature.isin(cols)]

plt.figure(figsize=(10,10))
sns.barplot(x="importance", y="Feature", data=best_features.sort_values(by="importance",ascending=False),
        edgecolor=('white'), linewidth=2, palette="rocket")
plt.title('CatBoost Features importance (averaged/folds)', fontsize=18)
plt.tight_layout()
"""


# # <a id='4'>4. Submission</a> 

# In[ ]:


sample_submission['isFraud'] = predictions
sample_submission.to_csv('submission_IEEE.csv')

