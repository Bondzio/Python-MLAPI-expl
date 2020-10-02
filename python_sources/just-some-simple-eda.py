#!/usr/bin/env python
# coding: utf-8

# ## Overview
# 
# The purpose of this kernel is to take a look at the data, come up with some insights, and attempt to create a predictive model or two. This notebook is still **very** raw. I will work on it as my very limited time permits, and hope to expend it in the upcoming days and weeks.
# 
# ## Packages
# 
# First, let's load a few useful Python packages. This section will keep growing in subsequent versions of this EDA.

# In[ ]:


import os
import numpy as np
import pandas as pd
import time
from tqdm import tqdm
import h2o

import lightgbm as lgb

from sklearn.metrics import f1_score
from sklearn.model_selection import KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB

import nltk
from nltk.corpus import stopwords
import string

from scipy.sparse import hstack

import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# This is a kernels-only competition, which means that we can only use tools and data that are available to us in a single Kaggle kernel. The Pyhon libraries that are available to us are the standard Kaggle kernels compute environment. So let's take a look at the data that's available to us: 

# In[ ]:


import os
print(os.listdir("../input"))


# We see that the input folder contains, in addition to the standard train, test, and sample_submission files, another folder which presumably contains various embeddings. Let's take a look at what embeddings are availabel to us. 

# In[ ]:


print(os.listdir("../input/embeddings"))


# We see that we have access to four different 300-dimensional embeddings. 300-dimensional embeddings are probably the best ones from the standpoint of a single-best-model, but having access to lower dimensional embeddings would have been nice from the prototyping standpoint. We'll get back to the embeddings later, but let's now take a look at the train and test files.

# In[ ]:


train = pd.read_csv('../input/train.csv').fillna(' ')
test = pd.read_csv('../input/test.csv').fillna(' ')


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


train.shape


# In[ ]:


test.shape


# Seems farily straightforward - just ID, text and target firlds. In addition, the train set is very decently sized - 1.3 million records is probably enough for a decent text classifier. 
# 
# Let's take a look at the targetvariable:
# 

# In[ ]:


train_target = train['target'].values

np.unique(train_target)


# In[ ]:


train_target.mean()


# That's pretty good: just two classes, but the positive class makes just over 6% of the total. So the target is heavily unbalanced, which is why a metric such as F1 seems appropriate for this kind of problem. 

# In[ ]:


eng_stopwords = set(stopwords.words("english"))


# For EDA and later modeling, it might be a good idea to create some metafeatures. This work is partly based on SRK's great EDAs, and [this one](http://www.kaggle.com/sudalairajkumar/simple-feature-engg-notebook-spooky-author) in particular. The metafeatures that we'll create are:
# 
# 
# * Number of words in the text
# * Number of unique words in the text
# * Number of characters in the text
# * Number of stopwords
# * Number of punctuations
# * Number of upper case words
# * Number of title case words
# * Average length of the words

# In[ ]:


## Number of words in the text ##
train["num_words"] = train["question_text"].apply(lambda x: len(str(x).split()))
test["num_words"] = test["question_text"].apply(lambda x: len(str(x).split()))

## Number of unique words in the text ##
train["num_unique_words"] = train["question_text"].apply(lambda x: len(set(str(x).split())))
test["num_unique_words"] = test["question_text"].apply(lambda x: len(set(str(x).split())))

## Number of characters in the text ##
train["num_chars"] = train["question_text"].apply(lambda x: len(str(x)))
test["num_chars"] = test["question_text"].apply(lambda x: len(str(x)))

## Number of stopwords in the text ##
train["num_stopwords"] = train["question_text"].apply(lambda x: len([w for w in str(x).lower().split() if w in eng_stopwords]))
test["num_stopwords"] = test["question_text"].apply(lambda x: len([w for w in str(x).lower().split() if w in eng_stopwords]))

## Number of punctuations in the text ##
train["num_punctuations"] =train['question_text'].apply(lambda x: len([c for c in str(x) if c in string.punctuation]) )
test["num_punctuations"] =test['question_text'].apply(lambda x: len([c for c in str(x) if c in string.punctuation]) )

## Number of title case words in the text ##
train["num_words_upper"] = train["question_text"].apply(lambda x: len([w for w in str(x).split() if w.isupper()]))
test["num_words_upper"] = test["question_text"].apply(lambda x: len([w for w in str(x).split() if w.isupper()]))

## Number of title case words in the text ##
train["num_words_title"] = train["question_text"].apply(lambda x: len([w for w in str(x).split() if w.istitle()]))
test["num_words_title"] = test["question_text"].apply(lambda x: len([w for w in str(x).split() if w.istitle()]))

## Average length of the words in the text ##
train["mean_word_len"] = train["question_text"].apply(lambda x: np.mean([len(w) for w in str(x).split()]))
test["mean_word_len"] = test["question_text"].apply(lambda x: np.mean([len(w) for w in str(x).split()]))


# In[ ]:


plt.figure(figsize=(12,8))
sns.violinplot(data=train['num_words'])
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
sns.violinplot(data=train['num_unique_words'])
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
sns.violinplot(data=train['num_chars'])
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
sns.violinplot(data=train['num_stopwords'])
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
sns.violinplot(data=train['num_punctuations'])
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
sns.violinplot(data=train['num_words_upper'])
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
sns.violinplot(data=train['num_words_title'])
plt.show()


# In[ ]:


plt.figure(figsize=(12,8))
sns.violinplot(data=train['mean_word_len'])
plt.show()


# In[ ]:


eng_features = ['num_words', 'num_unique_words', 'num_chars', 
                'num_stopwords', 'num_punctuations', 'num_words_upper', 
                'num_words_title', 'mean_word_len']


# In[ ]:


kf = KFold(n_splits=5, shuffle=True, random_state=43)
test_pred = 0
oof_pred = np.zeros([train.shape[0],])

x_test = test[eng_features].values
for i, (train_index, val_index) in tqdm(enumerate(kf.split(train))):
    x_train, x_val = train.loc[train_index][eng_features].values, train.loc[val_index][eng_features].values
    y_train, y_val = train_target[train_index], train_target[val_index]
    classifier = LogisticRegression(C= 0.1)
    classifier.fit(x_train, y_train)
    val_preds = classifier.predict_proba(x_val)[:,1]
    preds = classifier.predict_proba(x_test)[:,1]
    test_pred += 0.2*preds
    oof_pred[val_index] = val_preds


# In[ ]:


pred_train = (oof_pred > 0.5).astype(np.int)
f1_score(train_target, pred_train)


# In[ ]:


f1_score(train_target, pred_train)


# In[ ]:


pred_train = (oof_pred > 0.12).astype(np.int)
f1_score(train_target, pred_train)


# For our second model we'll use TF-IDF with a logistic regression. The next couple of secontions are based on my [LR with n-grams notebook](https://www.kaggle.com/tunguz/lr-with-words-n-grams-baseline). Firtst, let's embed all the text vectors:

# In[ ]:


train_text = train['question_text']
test_text = test['question_text']
all_text = pd.concat([train_text, test_text])

word_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    strip_accents='unicode',
    analyzer='word',
    token_pattern=r'\w{1,}',
    stop_words='english',
    ngram_range=(1, 1),
    max_features=5000)
word_vectorizer.fit(all_text)
train_word_features = word_vectorizer.transform(train_text)
test_word_features = word_vectorizer.transform(test_text)


# Now let's see how well a logistic regression trained on these features does:

# In[ ]:


kf = KFold(n_splits=5, shuffle=True, random_state=43)
test_pred_tf = 0
oof_pred_tf = np.zeros([train.shape[0],])

for i, (train_index, val_index) in tqdm(enumerate(kf.split(train))):
    x_train, x_val = train_word_features[train_index,:], train_word_features[val_index,:]
    y_train, y_val = train_target[train_index], train_target[val_index]
    classifier = LogisticRegression(class_weight = "balanced", C=0.5, solver='sag')
    classifier.fit(x_train, y_train)
    val_preds = classifier.predict_proba(x_val)[:,1]
    preds = classifier.predict_proba(test_word_features)[:,1]
    test_pred_tf += 0.2*preds
    oof_pred_tf[val_index] = val_preds


# In[ ]:


pred_train = (oof_pred_tf > 0.8).astype(np.int)
f1_score(train_target, pred_train)


# In[ ]:





# In[ ]:


0.566075663947416


# In[ ]:


pred_train = (0.8*oof_pred_tf+0.2*oof_pred > 0.68).astype(np.int)
f1_score(train_target, pred_train)


# In[ ]:


0.5705038831309178


# The following LightGBM model is based on Peter's [LGB Baseline notebook](https://www.kaggle.com/peterhurford/lgb-baseline):

# In[ ]:


import lightgbm as lgb

def lgb_f1_score(y_hat, data):
    y_true = data.get_label()
    y_hat = np.round(y_hat) # scikits f1 doesn't like probabilities
    return 'f1', f1_score(y_true, y_hat), True

params = {'learning_rate': 0.05,
          'application': 'regression',
          'max_depth': 9,
          'num_leaves': 100,
          'verbosity': -1,
          'metric': 'rmse',
          'data_random_seed': 3,
          'bagging_fraction': 0.8,
          'feature_fraction': 0.4,
          'nthread': 16,
          'lambda_l1': 1,
          'lambda_l2': 1,
          'num_rounds': 2700,
          'verbose_eval': 100}


kf = KFold(n_splits=5, shuffle=True, random_state=43)
test_pred_lgb = 0
oof_pred_lgb = np.zeros([train.shape[0],])

for i, (train_index, val_index) in tqdm(enumerate(kf.split(train))):
    x_train, x_val = train_word_features[train_index,:], train_word_features[val_index,:]
    y_train, y_val = train_target[train_index], train_target[val_index]
    
    d_train = lgb.Dataset(x_train, label=y_train)
    d_valid = lgb.Dataset(x_val, label=y_val)

    num_rounds = 2500
    model = lgb.train(params,
                  train_set=d_train,
                  num_boost_round=num_rounds,
                  valid_sets=[d_train, d_valid],
                  valid_names=['train', 'val'],
                  verbose_eval=0)
    
    val_preds = model.predict(x_val)
    preds = classifier.predict(test_word_features)
    test_pred_lgb += 0.2*preds
    oof_pred_lgb[val_index] = val_preds


# In[ ]:


pred_train = (oof_pred_lgb > 0.3).astype(np.int)
f1_score(train_target, pred_train)


# In[ ]:


pred_train = (0.65*oof_pred_lgb+0.35*oof_pred_tf+0.1*oof_pred > 0.5).astype(np.int)
f1_score(train_target, pred_train)


# The following Logistic Regression is based on Premvardhan's [Count Vectorizer notebook](https://www.kaggle.com/premvardhan/quora-insincere-question-classification):

# In[ ]:


# Train Vectorizor
from sklearn.feature_extraction.text import CountVectorizer 

bow = CountVectorizer()


# In[ ]:


kf = KFold(n_splits=5, shuffle=True, random_state=43)
test_pred_cv = 0
oof_pred_cv = np.zeros([train.shape[0],])


for i, (train_index, val_index) in tqdm(enumerate(kf.split(train))):
    x_train, x_val = train.loc[train_index]['question_text'].values, train.loc[val_index]['question_text'].values
    y_train, y_val = train_target[train_index], train_target[val_index]
    x_test = test['question_text'].values
    
    bow = CountVectorizer()
    x_train = bow.fit_transform(x_train)
    x_val = bow.transform(x_val)
    x_test = bow.transform(x_test)

    classifier = LogisticRegression(penalty = "l1", C = 1.25, class_weight = "balanced")
    
    classifier.fit(x_train, y_train)
    val_preds = classifier.predict_proba(x_val)[:,1]
    preds = classifier.predict_proba(x_test)[:,1]
    test_pred_cv += 0.2*preds
    oof_pred_cv[val_index] = val_preds


# The following classifiers are inspired by dust's [Naive Bayes notebook](https://www.kaggle.com/stardust0/naive-bayes-and-logistic-regression-baseline):

# In[ ]:


kf = KFold(n_splits=5, shuffle=True, random_state=43)
test_pred_cv_2 = 0
oof_pred_cv_2 = np.zeros([train.shape[0],])
test_pred_cv_3 = 0
oof_pred_cv_3 = np.zeros([train.shape[0],])


for i, (train_index, val_index) in tqdm(enumerate(kf.split(train))):
    x_train, x_val = train.loc[train_index]['question_text'].values, train.loc[val_index]['question_text'].values
    y_train, y_val = train_target[train_index], train_target[val_index]
    x_test = test['question_text'].values
    
    bow = CountVectorizer()
    x_train = bow.fit_transform(x_train)
    x_val = bow.transform(x_val)
    x_test = bow.transform(x_test)
    
    classifier2 = MultinomialNB()
    classifier3 = BernoulliNB()
    
    classifier2.fit(x_train, y_train)
    val_preds = classifier2.predict_proba(x_val)[:,1]
    preds = classifier2.predict_proba(x_test)[:,1]
    test_pred_cv_2 += 0.2*preds
    oof_pred_cv_2[val_index] = val_preds
    
    classifier3.fit(x_train, y_train)
    val_preds = classifier3.predict_proba(x_val)[:,1]
    preds = classifier3.predict_proba(x_test)[:,1]
    test_pred_cv_3 += 0.2*preds
    oof_pred_cv_3[val_index] = val_preds


# In[ ]:


pred_train = (oof_pred_cv > 0.75).astype(np.int)
f1_score(train_target, pred_train)


# In[ ]:


pred_train = (oof_pred_cv_2 > 0.7).astype(np.int)
f1_score(train_target, pred_train)


# In[ ]:


pred_train = (oof_pred_cv_3 > 0.7).astype(np.int)
f1_score(train_target, pred_train)


# In[ ]:


pred_train = (0.7*oof_pred_cv+0.2*oof_pred_cv_2+0.1*oof_pred_cv_3 > 0.7).astype(np.int)
f1_score(train_target, pred_train)


# In[ ]:


pred_train = (0.63*(0.7*oof_pred_cv+0.2*oof_pred_cv_2+0.1*oof_pred_cv_3) +0.37*(0.65*oof_pred_lgb+0.35*oof_pred_tf+0.1*oof_pred)> 0.59).astype(np.int)
f1_score(train_target, pred_train)


# In[ ]:


stack_train = np.hstack((oof_pred.reshape(-1,1), oof_pred_tf.reshape(-1,1), oof_pred_lgb.reshape(-1,1), 
                         oof_pred_cv_3.reshape(-1,1), oof_pred_cv_2.reshape(-1,1), oof_pred_cv.reshape(-1,1)))


# In[ ]:


stack_test = np.hstack((test_pred.reshape(-1,1), test_pred_tf.reshape(-1,1), test_pred_lgb.reshape(-1,1), 
                         test_pred_cv_3.reshape(-1,1), test_pred_cv_2.reshape(-1,1), test_pred_cv.reshape(-1,1)))


# In[ ]:


stack_train.shape


# In[ ]:


stack_test.shape


# In[ ]:


kf = KFold(n_splits=5, shuffle=True, random_state=43)
test_pred_stack = 0
oof_pred_stack = np.zeros([train.shape[0],])

for i, (train_index, val_index) in tqdm(enumerate(kf.split(train))):
    x_train, x_val = stack_train[train_index,:], stack_train[val_index,:]
    y_train, y_val = train_target[train_index], train_target[val_index]
    classifier = LogisticRegression(class_weight = "balanced", C=0.5, solver='sag')
    classifier.fit(x_train, y_train)
    val_preds = classifier.predict_proba(x_val)[:,1]
    preds = classifier.predict_proba(stack_test)[:,1]
    test_pred_stack += 0.2*preds
    oof_pred_stack[val_index] = val_preds


# In[ ]:


score = 0
thresh = .5
for i in np.arange(0.1, 0.951, 0.01):
    temp_score = f1_score(train_target, (oof_pred_stack > i))
    if(temp_score > score):
        score = temp_score
        thresh = i

print("CV: {}, Threshold: {}".format(score, thresh))


# In[ ]:





# In[ ]:


0.6207799320845656


# Now we'll train on the full set and make predictions based on that:

# In[ ]:


pred_test = ( test_pred_stack> thresh).astype(np.int)
submission = pd.DataFrame.from_dict({'qid': test['qid']})
submission['prediction'] = pred_test
submission.to_csv('submission.csv', index=False)


# To be continued ...

# In[ ]:


1


# In[ ]:




