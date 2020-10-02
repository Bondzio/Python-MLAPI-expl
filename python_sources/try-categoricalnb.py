#!/usr/bin/env python
# coding: utf-8

# # Categorical feature Encoding2(try_CategoricalNB)
# 
# I tried CategoricalNB implemented in scikit-learn 0.22.
# 
# When I made a simple process and tried it, I got a certain level of auc score.
# 
# cv score: 0.7826 :lb score 0.78111

# In[ ]:


# !pip uninstall sklearn -y
get_ipython().system('pip install -U scikit-learn==0.22.1')
import sklearn
sklearn.__version__


# In[ ]:


import numpy as np
import pandas as pd
import scipy
import os, gc
from collections import Counter
from sklearn.model_selection import KFold,StratifiedKFold,RepeatedKFold,RepeatedStratifiedKFold
from sklearn.metrics import roc_auc_score as auc
from sklearn.linear_model import LogisticRegression
import category_encoders as ce

import warnings
warnings.filterwarnings('ignore')
pd.options.display.max_columns = 50
BIN_COL  = [f'bin_{i}' for i in range(5)]
NOM_COL  = [f'nom_{i}' for i in range(10)]
ORD_COL  = [f'ord_{i}' for i in range(6)]
NOM_5_9  = ['nom_5', 'nom_6', 'nom_7', 'nom_8', 'nom_9']
NOM_0_4  = ['nom_0', 'nom_1', 'nom_2', 'nom_3', 'nom_4']
DATE_COL = ['day','month']
# from imblearn.over_sampling import RandomOverSampler,SMOTE
import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


get_ipython().run_cell_magic('time', '', '\nsubmission = pd.read_csv("../input/cat-in-the-dat-ii/sample_submission.csv")\ntrain = pd.read_csv("../input/cat-in-the-dat-ii/train.csv")\ntest  = pd.read_csv("../input/cat-in-the-dat-ii/test.csv")')


# In[ ]:


def read_csv():
    train = pd.read_csv('../input/cat-in-the-dat-ii/train.csv')
    test  = pd.read_csv('../input/cat-in-the-dat-ii/test.csv')

    train_id = train['id']
    test_id  = test['id']
    train.drop('id', axis=1, inplace=True)
    test.drop('id',  axis=1, inplace=True)
    return train, test, train_id, test_id

def preprocessing(df):
    df.bin_3.replace({'F':0, 'T':1}, inplace=True)
    df.bin_4.replace({'N':0, 'Y':1}, inplace=True)
   
    ord_1_map = {'Novice':1,'Contributor':2,'Expert':3,'Master':4,'Grandmaster':5}
    ord_2_map = {'Freezing':1, 'Cold':2,'Warm':3,'Hot':4, 'Boiling Hot':5,'Lava Hot':6}
    df.loc[df['ord_1'].notnull(),'ord_1'] = df.loc[df['ord_1'].notnull(),'ord_1'].map(ord_1_map)
    df.loc[df['ord_2'].notnull(),'ord_2'] = df.loc[df['ord_2'].notnull(),'ord_2'].map(ord_2_map)
    df.loc[df['ord_3'].notnull(),'ord_3'] = df.loc[df['ord_3'].notnull(),'ord_3'].apply(
        lambda c: ord(c) - ord('a') + 1)
    df.loc[df['ord_4'].notnull(),'ord_4'] = df.loc[df['ord_4'].notnull(),'ord_4'].apply(
        lambda c: ord(c) - ord('A') + 1)
    for col in ['ord_1','ord_2','ord_3','ord_4',]:
        df[col] = df[col].astype(np.float32)
    
    df.loc[df.ord_5.notnull(), 'ord_5_1'] = df.loc[df.ord_5.notnull(), 'ord_5'].apply(lambda x: x[0])
    df.loc[df.ord_5.notnull(), 'ord_5_2'] = df.loc[df.ord_5.notnull(), 'ord_5'].apply(lambda x: x[1])
    df.loc[df['ord_5_1'].notnull(),'ord_5_1'] = df.loc[df['ord_5_1'].notnull(),'ord_5_1'].apply(
        lambda c: ord(c) - ord('a') + 33).astype(np.float32)
    df.loc[df['ord_5_2'].notnull(),'ord_5_2'] = df.loc[df['ord_5_2'].notnull(),'ord_5_2'].apply(
        lambda c: ord(c) - ord('a') + 33)#.astype(float)
    return df    

def filling_NaN(df):
#     df.fillna(-1, inplace=True)#Can't use negative values
    df.fillna(9999, inplace=True)
    df.day   = df.day.astype(int)
    df.month = df.month.astype(int)
    return df

def target_encoding(cols, smoothing=1.0, min_samples_leaf=1):
    for col in cols:
        encoder = ce.TargetEncoder(cols=col, 
                                   smoothing=smoothing, 
                                   min_samples_leaf=min_samples_leaf)#ce.leave_one_out.LeaveOneOutEncoder()
        train[f'{col}_mean'] = encoder.fit_transform(train[col], train['target'])[col].astype(np.float32)
        test[f'{col}_mean']  = encoder.transform(test[col])[col].astype(np.float32)  
    del encoder
    gc.collect() 


# In[ ]:


get_ipython().run_cell_magic('time', '', "\ntrain, test, train_id, test_id = read_csv()\ntrain = preprocessing(train)\ntest  = preprocessing(test)\nprint(f'train day unique value:{train.day.unique()}')\nprint(f'test  day unique value:{test.day.unique()}')\n\nfor col in test.columns:\n    if len(set(train[col].dropna().unique().tolist())^ set(test[col].dropna().unique().tolist()))>0:\n        train_only = list(set(train[col].dropna().unique().tolist()) - set(test[col].dropna().unique().tolist()))\n        test_only  = list(set(test[col].dropna().unique().tolist()) - set(train[col].dropna().unique().tolist()))\n        print(col, '(train only)', train_only, '(test only)', test_only) \n        train.loc[train[col].isin(train_only), col] = np.NaN\n        test.loc[test[col].isin(test_only), col]    = np.NaN  \n\n\nfor i in range(10):\n    encoder = ce.OrdinalEncoder(handle_missing='return_nan')\n    encoder.fit(\n        pd.concat(\n            [train[f'nom_{i}'],test[f'nom_{i}']]))\n    train[f'nom_{i}'] = encoder.transform(train[f'nom_{i}'])\n    test[f'nom_{i}']  = encoder.transform(test[f'nom_{i}'])\n\nfilling_NaN(train)\nfilling_NaN(test)")


# In[ ]:


train.describe()


# In[ ]:


train.info()


# In[ ]:


from sklearn.model_selection import train_test_split
X = train.drop(columns=['target','ord_5'])
y = train.target
X_test = test.drop(columns=['ord_5'])
(X_train,X_val, y_train, y_val) = train_test_split(X, y)
print(X_train.shape,X_val.shape, y_train.shape, y_val.shape)


# In[ ]:


from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import roc_auc_score as auc

model = CategoricalNB(alpha=5.0,#1.0,
                     )
model.fit(X_train, y_train)
auc(y_val, model.predict_proba(X_val)[:, 1])


# In[ ]:


get_ipython().run_cell_magic('time', '', '\nkf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)\noof_preds = np.zeros(len(X)).astype(np.float32)\nsub_preds = np.zeros(len(X_test)).astype(np.float32)\nfor fold_, (train_idx, val_idx) in enumerate(kf.split(X,y=y)):\n    X_train = X.loc[train_idx] \n    y_train = y.loc[train_idx]\n    X_val, y_val = X.loc[val_idx], y.loc[val_idx]\n    model = CategoricalNB()\n    model.fit(X_train, y_train)\n    oof_preds[val_idx] = model.predict_proba(X_val)[:, 1]\n    sub_preds += model.predict_proba(X_test)[:, 1] / kf.n_splits')


# In[ ]:


plt.title(f'auc_score:{auc(y, oof_preds)}')
sns.distplot(oof_preds)
sns.distplot(sub_preds)
plt.legend(['train','test'])
plt.show()   


# In[ ]:


pd.Series(sub_preds).describe()


# In[ ]:


submission = pd.DataFrame(
    {'id': test_id, 
     'target': sub_preds,
    })
submission.to_csv('submission.csv', index=False)

