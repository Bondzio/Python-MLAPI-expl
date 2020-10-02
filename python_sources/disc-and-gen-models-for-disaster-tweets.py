#!/usr/bin/env python
# coding: utf-8

# **In this kernel we are going to classify Real or Not? NLP with Disaster Tweets dataset using five algorithm **
# 
# 1. importing libraries 

# In[ ]:


import nltk
from nltk.tokenize import word_tokenize
from nltk.classify import ClassifierI
from nltk.classify.scikitlearn import SklearnClassifier
from statistics import mode
from sklearn.naive_bayes import BernoulliNB,MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import NuSVC
import random
import pandas as pd
import numpy as np
import tensorflow as tf
import re
import string
from string import punctuation,ascii_letters
from nltk.corpus import stopwords
import plotly
import plotly.graph_objs as go
from plotly.offline import plot


# 2. Importing train and test data 

# In[ ]:


traintwitts = pd.read_csv('/kaggle/input/nlp-getting-started/train.csv')
testtwitts = pd.read_csv('/kaggle/input/nlp-getting-started/test.csv')
traintwitts.isna().sum()


# We will focus on the text column

# In[ ]:


twts = traintwitts.drop(columns=['id' ,'keyword',	'location'])
twts.head()


# 3. Preprocessing 
# 
# a- Documents for texts and labels 

# In[ ]:


text = []
for t in twts['text']:
    if t.isalpha:
        text.append(t)
doncuments = []
for r,t in zip(twts['text'],twts['target']):
    doncuments.append((r,t))
print('length of Document:',len(doncuments))


# b- Remove punctuation urls, stopwords and lowercase all words 

# In[ ]:


stop_words = set(stopwords.words('english'))
all_words = []
for i in text:
    for s in word_tokenize(i):
        url = re.findall(r'//\S+|www\.\S+|',s)
        if s not in stop_words and s not in punctuation and s not in url:
            all_words.append(s.lower())


# c- Word Frequancy

# In[ ]:


all_words = nltk.FreqDist(all_words)
words_keys = list(all_words.keys())


# d- 55 worlds cloud

# In[ ]:


dic = {}
for k,v in all_words.items():
    dic[k] = v
df = pd.DataFrame.from_dict(dic,orient='index')


# In[ ]:


colors = [plotly.colors.DEFAULT_PLOTLY_COLORS[random.randrange(1, 10)] for i in range(55)]

data = go.Scatter(x=[random.random() for i in range(55)],
                 y=[random.random() for i in range(55)],
                 mode='text',
                 text=df.index,
                 marker={'opacity': 0.3},
                 textfont={'size': df[0:55],
                           'color': colors})
layout = go.Layout({'xaxis': {'showgrid': True, 'showticklabels': False, 'zeroline': True},
                    'yaxis': {'showgrid': True, 'showticklabels': False, 'zeroline': True}})




fig = go.Figure(data=[data], layout=layout)

fig.show()


# e- Find features and split the data into train validation set

# In[ ]:


def f_feature(document):
    words = word_tokenize(document)
    features = {}
    for w in words_keys:
        features[w] = (w in words)
    return features


# In[ ]:


featuresets = [(f_feature(rev),category) for (rev,category) in doncuments]
random.shuffle(featuresets)
train_set = featuresets[:6500]
test_set = featuresets[6500:] 


# 4. Classifiers
# > a- Naive Bays

# In[ ]:


onb = nltk.NaiveBayesClassifier.train(train_set)
print("Original Naive Bayes Classifier accuracy:", (nltk.classify.accuracy(onb, test_set))*100,'%')
onb.show_most_informative_features(15)


# > b- Multinomial Naive Bays

# In[ ]:


MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(train_set)
print("MNB_classifier accuracy:", (nltk.classify.accuracy(MNB_classifier, test_set))*100,'%')


# > c- Bernoulli Naive Bays

# In[ ]:


BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(train_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, test_set))*100,'%')


# > d-Logistic Regression

# In[ ]:


LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(train_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, test_set))*100)


# > e-Nu SVM

# In[ ]:


NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(train_set)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, test_set))*100)


# 5. Predicting and Submission

# In[ ]:


sample_submission = pd.read_csv("/kaggle/input/nlp-getting-started/sample_submission.csv")

pred = []
for i in range(len(testtwitts['text'])):
    pred.append(MNB_classifier.classify(f_feature(testtwitts['text'][i])))
sample_submission['target'] = pred  
sample_submission.head()


# In[ ]:




