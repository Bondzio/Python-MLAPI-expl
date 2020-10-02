#!/usr/bin/env python
# coding: utf-8

# > Please go through Giba's post and kernel  to underrstand what this leak is all about
# > https://www.kaggle.com/titericz/the-property-by-giba (kernel)
# > https://www.kaggle.com/c/santander-value-prediction-challenge/discussion/61329 (post)
# > 
# > Also, go through this Jiazhen's kernel which finds more columns to exploit leak
# > https://www.kaggle.com/johnfarrell/giba-s-property-extended-result
# > 
# > I just exploit data property in brute force way and then fill in remaining by row non zero means! This should bring everyone on level-playing field.
# > 
# > **Let the competition begin! :D**
# 
# > ### Just some small modifications from [original baseline](https://www.kaggle.com/tezdhar/breaking-lb-fresh-start)~
# >- The leak rows are calculated separately on train/test set
# >- Calculated the leaky values, correctness, for each lag
# >- Hope this can help to do some *lag_selection*
# 
# >### Update leak process codes to Dmitry Frumkin's *fast* [version](https://www.kaggle.com/dfrumkin/a-simple-way-to-use-giba-s-features-v2)
# >- The result of Dmitry's original function and result of Hasan's function seem slightly different
# >- Modified to make the output consistent with Hasan's function (Seems better score)

# Updated this Kernel by Jiazhen Xi with some of the new patterns I found. Using 6 of the 40 those patterns. Hope this helps everyone and provide them with some sort of help in this dying stage of the competition.

# In[ ]:


import warnings
warnings.filterwarnings('ignore')

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
print(os.listdir("../input"))

import lightgbm as lgb
from sklearn.model_selection import *
from sklearn.metrics import mean_squared_error, make_scorer
from scipy.stats import mode, skew, kurtosis, entropy
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_squared_error

import matplotlib.pyplot as plt
import seaborn as sns

import dask.dataframe as dd
from dask.multiprocessing import get

from tqdm import tqdm, tqdm_notebook
tqdm.pandas(tqdm_notebook)

# Any results you write to the current directory are saved as output.


# In[ ]:


train = pd.read_csv("../input/santander-value-prediction-challenge/train.csv")
test = pd.read_csv("../input/santander-value-prediction-challenge/test.csv")

transact_cols = [f for f in train.columns if f not in ["ID", "target"]]
y = np.log1p(train["target"]).values


# In[ ]:


test["target"] = train["target"].mean()


# We take time series columns from [here](https://www.kaggle.com/johnfarrell/giba-s-property-extended-result)

# In[ ]:


all_df = pd.concat([train, test]).reset_index(drop=True)
all_df.columns = all_df.columns.astype(str)
print(all_df.shape)


# In[ ]:


cols = ['f190486d6', '58e2e02e6', 'eeb9cd3aa', '9fd594eec', '6eef030c1', '15ace8c9f', 
        'fb0f5dbfe', '58e056e12', '20aa07010', '024c577b9', 'd6bb78916', 'b43a7cfd5', 
        '58232a6fb', '1702b5bf0', '324921c7b', '62e59a501', '2ec5b290f', '241f0f867', 
        'fb49e4212', '66ace2992', 'f74e8f13d', '5c6487af1', '963a49cdc', '26fc93eb7', 
        '1931ccfdd', '703885424', '70feb1494', '491b9ee45', '23310aa6f', 'e176a204a', 
        '6619d81fc', '1db387535', 
        'fc99f9426', '91f701ba2', '0572565c2', '190db8488', 'adb64ff71', 'c47340d97', 'c5a231d81', '0ff32eb98'
       ]


# In[ ]:


pattern_1964666 = pd.read_csv('../input/pattern-found/pattern_1964666.66.csv')
pattern_1166666 = pd.read_csv('../input/pattern-found/pattern_1166666.66.csv')
pattern_812666 = pd.read_csv('../input/pattern-found/pattern_812666.66.csv')
pattern_2002166 = pd.read_csv('../input/pattern-found/pattern_2002166.66.csv')
pattern_3160000 = pd.read_csv('../input/pattern-found/pattern_3160000.csv')
pattern_3255483 = pd.read_csv('../input/pattern-found/pattern_3255483.88.csv')


# In[ ]:


pattern_1964666.drop(['Unnamed: 0','value_count'],axis=1,inplace=True)
pattern_1166666.drop(['Unnamed: 0','value_count'],axis=1,inplace=True)
pattern_812666.drop(['Unnamed: 0','value_count'],axis=1,inplace=True)
pattern_2002166.drop(['Unnamed: 0','value_count'],axis=1,inplace=True)
pattern_3160000.drop(['Unnamed: 0','value_count'],axis=1,inplace=True)
pattern_3255483.drop(['Unnamed: 0','value_count'],axis=1,inplace=True)


# In[ ]:


pattern_1166666.rename(columns={'8.50E+43': '850027e38'},inplace=True)


# In[ ]:


l=[]
l.append(pattern_1964666.columns.values.tolist())
l.append(pattern_1166666.columns.values.tolist())
l.append(pattern_812666.columns.values.tolist())
l.append(pattern_2002166.columns.values.tolist())
l.append(pattern_3160000.columns.values.tolist())
l.append(pattern_3255483.columns.values.tolist())


# Updating this function on the basis of the hint provided by Paradox [here](http://www.kaggle.com/c/santander-value-prediction-challenge/discussion/61472#363394).

# In[ ]:


def _get_leak(df, cols,extra_feats, lag=0):
    f1 = cols[:((lag+2) * -1)]
    f2 = cols[(lag+2):]
    for ef in extra_feats:
        f1 += ef[:((lag+2) * -1)]
        f2 += ef[(lag+2):]
    
    d1 = df[f1].apply(tuple, axis=1).to_frame().rename(columns={0: 'key'})
    d1.to_csv('extra_d1.csv')
    d2 = df[f2].apply(tuple, axis=1).to_frame().rename(columns={0: 'key'}) 

    d2['pred'] = df[cols[lag]]
#     d2.to_csv('extra_d2.csv')
    #d2 = d2[d2.pred != 0] ### to make output consistent with Hasan's function
    d3 = d2[~d2.duplicated(['key'], keep=False)]
    d4 = d1[~d1.duplicated(['key'], keep=False)]
    d5 = d4.merge(d3, how='inner', on='key')
    
    d6 = d1.merge(d5, how='left', on='key')
    d6.to_csv('extra_d6.csv')
    
    return d1.merge(d5, how='left', on='key').pred.fillna(0)


# In[ ]:


def compiled_leak_result():
    
    max_nlags = len(cols)-2
    train_leak = train[["ID", "target"] + cols]
    train_leak["compiled_leak"] = 0
    train_leak["nonzero_mean"] = train[transact_cols].apply(
        lambda x: np.expm1(np.log1p(x[x!=0]).mean()), axis=1
    )
    scores = []
    leaky_value_counts = []
    leaky_value_corrects = []
    leaky_cols = []
    
    for i in range(max_nlags):
        c = "leaked_target_"+str(i)
        print('Processing lag', i)
        train_leak[c] = _get_leak(train, cols,l, i)
        
        leaky_cols.append(c)
        train_leak = train.join(
            train_leak.set_index("ID")[leaky_cols+["compiled_leak", "nonzero_mean"]], 
            on="ID", how="left"
        )[["ID", "target"] + cols + leaky_cols+["compiled_leak", "nonzero_mean"]]
        zeroleak = train_leak["compiled_leak"]==0
        train_leak.loc[zeroleak, "compiled_leak"] = train_leak.loc[zeroleak, c]
        leaky_value_counts.append(sum(train_leak["compiled_leak"] > 0))
        _correct_counts = sum(train_leak["compiled_leak"]==train_leak["target"])
        leaky_value_corrects.append(_correct_counts*1.0/leaky_value_counts[-1])
        print("Leak values found in train", leaky_value_counts[-1])
        print(
            "% of correct leaks values in train ", 
            leaky_value_corrects[-1]
        )
        tmp = train_leak.copy()
        tmp.loc[zeroleak, "compiled_leak"] = tmp.loc[zeroleak, "nonzero_mean"]
        print('Na count',tmp.compiled_leak.isna().sum())
        scores.append(np.sqrt(mean_squared_error(y, np.log1p(tmp["compiled_leak"]).fillna(14.49))))
        print(
            'Score (filled with nonzero mean)', 
            scores[-1]
        )
    result = dict(
        score=scores, 
        leaky_count=leaky_value_counts,
        leaky_correct=leaky_value_corrects,
    )
    return train_leak, result


# In[ ]:


train_leak, result = compiled_leak_result()


# In[ ]:


result = pd.DataFrame.from_dict(result, orient='columns')
result.T


# In[ ]:


result.to_csv('train_leaky_stat.csv', index=False)


# In[ ]:


train_leak.head()


# In[ ]:


best_score = np.min(result['score'])
best_lag = np.argmin(result['score'])
print('best_score', best_score, '\nbest_lag', best_lag)

