#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import standard libraries
import pandas as pd
import numpy as np

# import spacy for NLP and re for regular expressions
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import re

# import sklearn transformers, models and pipelines
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, GridSearchCV

# Load the small language model from spacy
nlp = spacy.load('en_core_web_sm')

# set pandas text output to 400
pd.options.display.max_colwidth = 400


# ## Load and Prepare Data
# There are duplicate rows. Some have the same text and target, while others only have the same text but different target. Here, I do not remove them because after removing them model performance gets worse. This behavior is unintuitive, especially since there are tweets with the same text but different labels. 
# 
# After that, I create a word embedding for each document using Word2Vec. Word2Vec creates a dense representation for each word, such that words appearing in similar contexts have similar vectors. To get an embedding for the entire tweet, the mean of all vectors for the words in the tweet are taken. The assumption now is that similar tweets have similar vectors. 

# In[ ]:


# load data
train = pd.read_csv('/kaggle/input/nlp-getting-started/train.csv')
test = pd.read_csv('/kaggle/input/nlp-getting-started/test.csv')
sample_submission = pd.read_csv('/kaggle/input/nlp-getting-started/sample_submission.csv')

# print shape of datasets
print('Train shape: {}'.format(train.shape))
print('Test shape: {}'.format(test.shape))
print('Sample submission shape: {}'.format(sample_submission.shape))

# inspect train set
train.head()


# In[ ]:


# Load the en_core_web_lg model
nlp = spacy.load('en_core_web_lg', disable=["tagger", "parser", "ner"])

# create train set by getting the document vector
docs_train = [nlp(doc).vector for doc in train.text]
X_train = np.vstack(docs_train)
print('Shape of train set: {}'.format(X_train.shape))

# create test set likewise
docs_test = [nlp(doc).vector for doc in test.text]
X_test = np.vstack(docs_test)
print('Shape of test set: {}'.format(X_test.shape))

# create target
y_train = train.target.copy()


# ## Create Machine Learning Pipeline
# The first step is creating a machine learning pipeline using the `Pipeline` class from scikit-learn. Creating a pipeline is important to have a robust workflow. For example, it ensures that all preprocessing steps that are learned on data are done within the cross-validation, to ensure that no data is leaked to the model.
# 
# In this case, it doesn't add much value since the only step in the pipeline is an estimator (here a logistic regression). However, since it's useful for pipelines with data preprocessing steps that are learned on data, such standard scaling, I even do it when it's not required. 
# 
# One advantage even when just using an estimator is that I can treat the estimator like a hyperparameter in the grid search. 

# In[ ]:


# create machine learning pipeline
word2vec_pipe = Pipeline([('estimator', LogisticRegression())])

# cross validate
print('F1 score: {:.3f}'.format(np.mean(cross_val_score(word2vec_pipe, X_train, y_train, scoring = 'f1'))))

# fit pipeline
word2vec_pipe.fit(X_train, y_train)

# predict on test set
pred = word2vec_pipe.predict(X_test)

# submit prediction
sample_submission.target = pred
sample_submission.to_csv('word2vec_baseline.csv', index = False)


# ## Hyperparameter Tuning
# After creating the baseline, I now want to test if a more complex model works better than the logistic regression. I chose a kernel SVM in this case, as SVM models are one of the classical machine learning models commonly used for text classification. 
# 
# I tune the regularization parameter C for both the logistic regression and SVM and the gamma parameter for the SVM. The hyperparameters influence the model complexity, with more complex models having a higher chance of overfitting. In case of the SVM, a more complex model can even find decision boundaries which are considered non-linear in the original feature space. 

# In[ ]:


# create a parameter grid
param_grid = [{'estimator' : [LogisticRegression()], 
               'estimator__C' : np.logspace(-3, 3, 7)},
              {'estimator' : [SVC()], 
               'estimator__C' : np.logspace(-1, 1, 3), 
               'estimator__gamma' : np.logspace(-2, 2, 5) / X_train.shape[0]}]

# create a RandomizedSearchCV object
word2vec_grid_search = GridSearchCV(
    estimator = word2vec_pipe,
    param_grid = param_grid,
    scoring = 'f1',
    n_jobs = -1,
    refit = True,
    verbose = 1,
    return_train_score = True
)

# fit RandomizedSearchCV object
word2vec_grid_search.fit(X_train, y_train)

# print grid search results
cols = ['param_estimator',
        'param_estimator__C',
        'param_estimator__gamma',
        'mean_test_score',
        'mean_train_score']

pd.options.display.max_colwidth = 50

word2vec_grid_search_results = pd.DataFrame(word2vec_grid_search.cv_results_).sort_values(by = 'mean_test_score', 
                                                                                          ascending = False)
word2vec_grid_search_results[cols].head(10)


# In[ ]:


# predict on test set with the best model from the randomized search
pred = word2vec_grid_search.predict(X_test)

# submit prediction
sample_submission.target = pred
sample_submission.to_csv('word2vec_tuned.csv', index = False)

