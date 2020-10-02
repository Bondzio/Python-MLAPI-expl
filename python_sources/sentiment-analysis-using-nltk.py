#!/usr/bin/env python
# coding: utf-8

# # Sentiment Analysis for IMDB Reviews Using NLTK and Bayes Classification Approach
# This is a basic, getting started tutorial that shows how you can do sentiment analysis on IMDB reviews by using following steps :-
# 1). Data Loading
# 2). Pre-Processing(basic NLP steps for pre-processing)
# 3). Feature Extraction (bag of words approach for feature extraction)
# 4). Training and Evaluation( Bayes classification for predicting sentiment class(positive or negative))

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
      #  print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/output'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# # Imports

# In[ ]:


import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
import re


# # Loading Sentiments

# In[ ]:


files_pos = os.listdir('/kaggle/input/imdb-movie-reviews-dataset/aclimdb/aclImdb/train/pos/')
files_pos = [open('/kaggle/input/imdb-movie-reviews-dataset/aclimdb/aclImdb/train/pos/'+f, 'r').read() for f in files_pos]
files_neg = os.listdir('/kaggle/input/imdb-movie-reviews-dataset/aclimdb/aclImdb/train/neg/')
files_neg = [open('/kaggle/input/imdb-movie-reviews-dataset/aclimdb/aclImdb/train/neg/'+f, 'r').read() for f in files_neg]


# In[ ]:


len(files_neg)


# # Preprocessing

# In[ ]:


all_words = []
documents = []

from nltk.corpus import stopwords
import re
# Setting English Stop Words
stop_words = list(set(stopwords.words('english')))

#  j is adject, r is adverb, and v is verb
#allowed_word_types = ["J","R","V"]
allowed_word_types = ["J"]

for p in  files_pos:
    
    # create a list of tuples where the first element of each tuple is a review
    # the second element is the label
    documents.append( (p, "pos") )
    
    # remove punctuations
    cleaned = re.sub(r'[^(a-zA-Z)\s]','', p)
    
    # tokenize 
    tokenized = word_tokenize(cleaned)
    
    # remove stopwords 
    stopped = [w for w in tokenized if not w in stop_words]
    
    # parts of speech tagging for each word 
    pos = nltk.pos_tag(stopped)
    
    # make a list of  all adjectives identified by the allowed word types list above
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

    
for p in files_neg:
    # create a list of tuples where the first element of each tuple is a review
    # the second element is the label
    documents.append( (p, "neg") )
    
    # remove punctuations
    cleaned = re.sub(r'[^(a-zA-Z)\s]','', p)
    
    # tokenize 
    tokenized = word_tokenize(cleaned)
    
    # remove stopwords 
    stopped = [w for w in tokenized if not w in stop_words]
    
    # parts of speech tagging for each word 
    neg = nltk.pos_tag(stopped)
    
    # make a list of  all adjectives identified by the allowed word types list above
    for w in neg:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())


# In[ ]:


len(all_words)


# # Selecting Allowed Word Types

# In[ ]:


pos_A = []
for w in pos:
    if w[1][0] in allowed_word_types:
        pos_A.append(w[0].lower())
pos_N = []
for w in neg:
    if w[1][0] in allowed_word_types:
        pos_N.append(w[0].lower())


# In[ ]:


len(pos_N)


# # Word Cloud

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

text = ' '.join(pos_A)
wordcloud = WordCloud().generate(text)

plt.figure(figsize = (15, 9))
# Display the generated image:
plt.imshow(wordcloud, interpolation= "bilinear")
plt.axis("off")
plt.show()


# # Negative Word Cloud

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

text = ' '.join(neg_A)
wordcloud = WordCloud().generate(text)

plt.figure(figsize = (15, 9))
# Display the generated image:
plt.imshow(wordcloud, interpolation= "bilinear")
plt.axis("off")
plt.show()


# In[ ]:


len(pos)


# # Save Documents

# In[ ]:


# pickling the list documents to save future recalculations 
#save_documents = 'documents.pickle'
#save_documents = open("../output/kaggle/working/documents.pickle","w")
#pickle.dump(documents, save_documents)
#save_documents.close()


# # Bag of Words(BOW) as Feature

# In[ ]:


# creating a frequency distribution of each adjectives. 
BOW = nltk.FreqDist(all_words)


# In[ ]:


# listing the 5000 most frequent words
word_features = list(BOW.keys())[:5000]
word_features[0], word_features[-1]


# # Feature Extraction for Reviews

# In[ ]:


# function to create a dictionary of features for each review in the list document.
# The keys are the words in word_features 
# The values of each key are either true or false for wether that feature appears in the review or not
def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

# Creating features for each review
featuresets = [(find_features(rev), category) for (rev, category) in documents]

# Shuffling the documents 
random.shuffle(featuresets)
print(len(featuresets))


# # Train-Test Split

# In[ ]:


training_set = featuresets[:20000]
testing_set = featuresets[20000:]
print( 'training_set :', len(training_set), '\ntesting_set :', len(testing_set))


# # Sentiment Classification Using Bayes Approach

# In[ ]:


classifier = nltk.NaiveBayesClassifier.train(training_set)

print("Classifier accuracy percent:",(nltk.classify.accuracy(classifier, testing_set))*100)

classifier.show_most_informative_features(15)

