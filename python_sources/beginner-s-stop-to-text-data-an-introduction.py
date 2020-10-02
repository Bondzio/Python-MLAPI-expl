#!/usr/bin/env python
# coding: utf-8

# # A simple K-fold approach for Quora Sincerity Prediction
# ### The main goal of this kernel is just a simple introduction to NLP using a couple of generic NLP functions (not detailed NLP approach)
# 
# - An existential problem for any major website today is how to handle toxic and divisive content. 
# - Quora wants to tackle this problem head-on to keep their platform a place where users can feel safe sharing their knowledge with the world.
# 
# - Quora is a platform that empowers people to learn from each other. On Quora, people can ask questions and connect with others who contribute unique insights and quality answers. 
# - A key challenge is to weed out insincere questions -- those founded upon false premises, or that intend to make a statement rather than look for helpful answers.
# 
# ![](https://assets.entrepreneur.com/content/3x2/2000/20190211224126-quora-logo-crop.jpeg?width=700&crop=2:1)
# 
# In this competition, Kagglers developed models that identify and flag insincere questions. To date, Quora has employed both machine learning and manual review to address this problem. They developed more scalable methods to detect toxic and misleading content.

# # This notebook aims only a simple introduction to word processing, it will not give a great score but if you're a complete beginner, I believe it will be helpful towards your studies.
# ![](https://s3-eu-west-1.amazonaws.com/beyondchocolate-cdn/beta/wp-content/uploads/2013/10/31161231/stop.png)

# # importing the required libraries

# In[ ]:


import os
import nltk
import numpy as np 
import pandas as pd 
print(os.listdir("../input"))
from nltk.corpus import stopwords
from sklearn.metrics import f1_score
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.naive_bayes import GaussianNB,MultinomialNB,ComplementNB,BernoulliNB


# # a small function to see all the columns

# In[ ]:


def display_all(df):
    with pd.option_context("display.max_rows", 1000, "display.max_columns", 1000): 
        display(df)


# # getting the files

# In[ ]:


train = pd.read_csv('../input/train.csv')
test  = pd.read_csv('../input/test.csv')


# # checking the files

# In[ ]:


display_all(train.head())


# In[ ]:


train['target'].value_counts()


# In[ ]:


train_text = train['question_text']
test_text = test['question_text']
train_target = train['target']
all_text = train_text.append(test_text)


# # vectorizing
# 
# ## vectorizing can be considered as a key method in word processing and text analysis, but considering the recent achievements, TfiedVectorizers are conventional but not the most powerful
# 
# -more info about TfiedVectorizer can be found here 
# 
# https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
# 
# ![](https://chrisalbon.com/images/machine_learning_flashcards/TF-IDF_print.png)

# In[ ]:


tfidf_vectorizer = TfidfVectorizer()
tfidf_vectorizer.fit(all_text)

count_vectorizer = CountVectorizer()
count_vectorizer.fit(all_text)

train_text_features_cv = count_vectorizer.transform(train_text)
test_text_features_cv = count_vectorizer.transform(test_text)

train_text_features_tf = tfidf_vectorizer.transform(train_text)
test_text_features_tf = tfidf_vectorizer.transform(test_text)


# In[ ]:


train_text.head()


# # 5 Fold Cross Validation
# 
# Cross-validation is a resampling procedure used to evaluate machine learning models on a limited data sample. The procedure has a single parameter called k that refers to the number of groups that a given data sample is to be split into. As such, the procedure is often called k-fold cross-validation
# 
# ![](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/K-fold_cross_validation_EN.svg/1280px-K-fold_cross_validation_EN.svg.png)

# In[ ]:


kfold = KFold(n_splits = 5, shuffle = True, random_state = 2018)
test_preds = 0
oof_preds = np.zeros([train.shape[0],])

for i, (train_idx,valid_idx) in enumerate(kfold.split(train)):
    x_train, x_valid = train_text_features_tf[train_idx,:], train_text_features_tf[valid_idx,:]
    y_train, y_valid = train_target[train_idx], train_target[valid_idx]
    classifier = LogisticRegression()
    print('fitting.......')
    classifier.fit(x_train,y_train)
    print('predicting......')
    print('\n')
    oof_preds[valid_idx] = classifier.predict_proba(x_valid)[:,1]
    test_preds += 0.2*classifier.predict_proba(test_text_features_tf)[:,1]


# In[ ]:


pred_train = (oof_preds > .25).astype(np.int)
f1_score(train_target, pred_train)


# # submission

# In[ ]:


submission1 = pd.DataFrame.from_dict({'qid': test['qid']})
submission1['prediction'] = (test_preds>0.25).astype(np.int)
submission1.to_csv('submission.csv', index=False)
submission1['prediction'] = (test_preds>0.25)


# # Appendix

# # Several NLP Libraries to help !
# 
# ![](data:image/jpeg;base64,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)
# 
# - **TextBlob** - Providing a consistent API for diving into common natural language processing (NLP) tasks. Stands on the giant shoulders of Natural Language Toolkit (NLTK) and Pattern, and plays nicely with both 
# - **spaCy** - Industrial strength NLP with Python and Cython 
# - **textacy** - Higher level NLP built on spaCy
# - **gensim** - Python library to conduct unsupervised semantic modelling from plain text 
# - **scattertext** - Python library to produce d3 visualizations of how language differs between corpora
# - **GluonNLP** - A deep learning toolkit for NLP, built on MXNet/Gluon, for research prototyping and industrial deployment of state-of-the-art models on a wide range of NLP tasks.
# - **AllenNLP** - An NLP research library, built on PyTorch, for developing state-of-the-art deep learning models on a wide variety of linguistic tasks.
# - **PyTorch-NLP** - NLP research toolkit designed to support rapid prototyping with better data loaders, word vector loaders, neural network layer representations, common NLP metrics such as BLEU
# - **Rosetta** - Text processing tools and wrappers (e.g. Vowpal Wabbit)
# - **PyNLPl** - Python Natural Language Processing Library. General purpose NLP library for Python. Also contains some specific modules for parsing common NLP formats, most notably for FoLiA, but also ARPA language models, Moses phrasetables, GIZA++ alignments.
# - **jPTDP** - A toolkit for joint part-of-speech (POS) tagging and dependency parsing. jPTDP provides pre-trained models for 40+ languages.
# - **BigARTM** - a fast library for topic modelling
# - **Snips NLU** - A production ready library for intent parsing
# - **Chazutsu** - A library for downloading&parsing standard NLP research datasets
# - **Word Forms** - Word forms can accurately generate all possible forms of an English word
# - **Multilingual** Latent Dirichlet Allocation (LDA) - A multilingual and extensible document clustering pipeline
# - **NLP Architect** - A library for exploring the state-of-the-art deep learning topologies and techniques for NLP and NLU
# - **Flair** - A very simple framework for state-of-the-art multilingual NLP built on PyTorch. Includes BERT, ELMo and Flair embeddings.
# - **Kashgari** - Simple, Keras-powered multilingual NLP framework, allows you to build your models in 5 minutes for named entity recognition (NER), part-of-speech tagging (PoS) and text classification tasks. Includes BERT and word2vec embedding.
# - **FARM** - FARM makes cutting-edge transfer learning simple and helps you to leverage pretrained language models for your own NLP tasks.
# - **Rita DSL** - a DSL, loosely based on RUTA on Apache UIMA. Allows to define language patterns (rule-based NLP) which are then translated into spaCy, or if you prefer less features and lightweight - regex patterns.
# 
# 
# 
# 
# 
# 
# 
# 

# * # Great Courses from Stanford, Oxford, Carnegie Mellon, Yandex, and fast.ai
# 
# 
# - https://github.com/oxford-cs-deepnlp-2017/lectures
# - https://web.stanford.edu/class/cs224n/
# - http://phontron.com/class/nn4nlp2017/
# - https://github.com/yandexdataschool/nlp_course
# - https://www.fast.ai/2019/07/08/fastai-nlp/ 

# ## Thank you very much!
# ## Planning to add more stuff soon
