#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


train = pd.read_csv("../input/alta-2019-challenge/train.csv")


# In[ ]:


train.head()


# In[ ]:


len(train)


# Let's output the most common target words

# In[ ]:


from collections import Counter
counter = Counter()
for i, row in train.iterrows():
    if type(row['Prediction']) != str:
        print('WARNING:', row)
        continue
    counter.update(row['Prediction'].split())
print(counter.most_common(50))


# Based on this, let's write a baseline that does this:
# 1. Return all personal and possessive pronouns
# 2. If there are no pronouns, return OUTSIDE

# In[ ]:


import nltk
def baseline_pronouns(text):
    tokens = nltk.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    result = [w.lower() for w, t in pos if t in ['PRP', 'PRP$']]
    if len(result) == 0:
        result =['OUTSIDE']
    return " ".join(set(result))


# In[ ]:


baseline_pronouns("You think it's bad now, as I recall with ")


# Let's now evaluate using the training data. We will perform cross-validation with 10 folds.

# In[ ]:


def dice(predicted, target):
    # This implementation of DICE should be equivalent to Kaggle's Mean F score (but I haven't tested it)
    p = set(predicted.split())
    t = set(target.split())
    return len(p & t)/(len(p) + len(t))


# In[ ]:


from sklearn.model_selection import KFold
kf = KFold(n_splits=10)
folds_evaluation = []
for i_train, i_test in kf.split(train):
    evaluation = []
    for i in i_test:
        row = train.iloc[i]
        prediction = baseline_pronouns(row['Comment'])
        if type(row['Prediction']) != str:
            print("WARNING:", row)
            continue
        evaluation.append(dice(prediction, row['Prediction']))
    print("Evaluation results:", np.mean(evaluation))
    folds_evaluation.append(np.mean(evaluation))
print("Cross-validation result:", np.mean(folds_evaluation))


# Let's compare with a system that always returns 'OUTSIDE'

# In[ ]:


from sklearn.model_selection import KFold
kf = KFold(n_splits=10)
folds_evaluation = []
for i_train, i_test in kf.split(train):
    evaluation = []
    for i in i_test:
        row = train.iloc[i]
        prediction = 'OUTSIDE'
        if type(row['Prediction']) != str:
            print("WARNING:", row)
            continue
        evaluation.append(dice(prediction, row['Prediction']))
    print("Evaluation results:", np.mean(evaluation))
    folds_evaluation.append(np.mean(evaluation))
print("Cross-validation result:", np.mean(folds_evaluation))


# Let's now generate runs of these two baselines

# In[ ]:


test_baseline_pronouns = pd.read_csv("../input/alta-2019-challenge/test_noannotations.csv")
test_baseline_pronouns.head()


# In[ ]:


test_baseline_pronouns['Prediction'] = test_baseline_pronouns['Comment'].apply(baseline_pronouns)
test_baseline_pronouns.head()


# In[ ]:


test_baseline_pronouns[['ID', 'Prediction']].to_csv('test_baseline_pronouns.csv', index=False)


# In[ ]:


test_baseline_outside = pd.read_csv("../input/alta-2019-challenge/test_noannotations.csv")
test_baseline_outside['Prediction'] = 'OUTSIDE'
test_baseline_outside.head()


# In[ ]:


test_baseline_outside[['ID', 'Prediction']].to_csv('test_baseline_outside.csv', index=False)


# In[ ]:


ls


# * [Download test_baseline_pronouns.csv](test_baseline_pronouns.csv)
# * [Download test_baseline_outside.csv](test_baseline_outside.csv)

# In[ ]:




