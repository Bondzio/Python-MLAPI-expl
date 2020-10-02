#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Firstly, please note that the performance of google word2vec is better on big datasets. 
# In this example we are considering only 25000 training examples from the imdb dataset.
# Therefore, the performance is similar to the "bag of words" model.

import warnings
warnings.filterwarnings('ignore')

# Importing libraries
import numpy as np
import pandas as pd
# BeautifulSoup is used to remove html tags from the text
from bs4 import BeautifulSoup 
import re # For regular expressions

# Stopwords can be useful to undersand the semantics of the sentence.
# Therefore stopwords are not removed while creating the word2vec model.
# But they will be removed  while averaging feature vectors.
from nltk.corpus import stopwords


# In[ ]:


# # Read data from files
# train = pd.read_csv("../input/labeledTrainData.tsv", header=0,\
#                     delimiter="\t", quoting=3)

# test = pd.read_csv("../input/testData.tsv",header=0,\
#                     delimiter="\t", quoting=3)

train = pd.read_csv('../input/innoplexusav/train.csv')
test = pd.read_csv("../input/innoplexusav/test.csv")


# In[ ]:


# This function converts a text to a sequence of words.
def review_wordlist(review, remove_stopwords=False):
    # 1. Removing html tags
    review_text = BeautifulSoup(review).get_text()
    # 2. Removing non-letter.
    review_text = re.sub("[^a-zA-Z]"," ",review_text)
    # 3. Converting to lower case and splitting
    words = review_text.lower().split()
    # 4. Optionally remove stopwords
    if remove_stopwords:
        stops = set(stopwords.words("english"))     
        words = [w for w in words if not w in stops]
    
    return(words)


# In[ ]:



# word2vec expects a list of lists.
# Using punkt tokenizer for better splitting of a paragraph into sentences.

import nltk.data
#nltk.download('popular')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


# In[ ]:


# This function splits a review into sentences
def review_sentences(review, tokenizer, remove_stopwords=False):
    # 1. Using nltk tokenizer
    raw_sentences = tokenizer.tokenize(review.strip())
    sentences = []
    # 2. Loop for each sentence
    for raw_sentence in raw_sentences:
        if len(raw_sentence)>0:
            sentences.append(review_wordlist(raw_sentence,                                            remove_stopwords))

    # This returns the list of lists
    return sentences


# In[ ]:



sentences = []
print("Parsing sentences from training set")
for review in train["text"]:
    sentences += review_sentences(review, tokenizer)
    


# In[ ]:


# Importing the built-in logging module
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# In[ ]:


# Creating the model and setting values for the various parameters
num_features = 1000  # Word vector dimensionality
min_word_count = 40 # Minimum word count
num_workers = 4     # Number of parallel threads
context = 10        # Context window size
downsampling = 1e-3 # (0.001) Downsample setting for frequent words

# Initializing the train model
from gensim.models import word2vec
print("Training model....")
model = word2vec.Word2Vec(sentences,                          workers=num_workers,                          size=num_features,                          min_count=min_word_count,                          window=context,
                          sample=downsampling)

# To make the model memory efficient
model.init_sims(replace=True)

# Saving the model for later use. Can be loaded using Word2Vec.load()
model_name = "300features_40minwords_10context"
model.save(model_name)


# In[ ]:


# Few tests: This will print the odd word among them 
model.wv.doesnt_match("man woman dog child kitchen".split())


# In[ ]:


model.wv.doesnt_match("france england germany berlin".split())


# In[ ]:


# This will print the most similar words present in the model
model.wv.most_similar("man")


# In[ ]:


model.wv.most_similar("awful")


# In[ ]:


# This will give the total number of words in the vocabolary created from this dataset
model.wv.syn0.shape


# In[ ]:


# Function to average all word vectors in a paragraph
def featureVecMethod(words, model, num_features):
    # Pre-initialising empty numpy array for speed
    featureVec = np.zeros(num_features,dtype="float32")
    nwords = 0
    
    #Converting Index2Word which is a list to a set for better speed in the execution.
    index2word_set = set(model.wv.index2word)
    
    for word in  words:
        if word in index2word_set:
            nwords = nwords + 1
            featureVec = np.add(featureVec,model[word])
    
    # Dividing the result by number of words to get average
    featureVec = np.divide(featureVec, nwords)
    return featureVec


# In[ ]:


# Function for calculating the average feature vector
def getAvgFeatureVecs(reviews, model, num_features):
    counter = 0
    reviewFeatureVecs = np.zeros((len(reviews),num_features),dtype="float32")
    for review in reviews:
        # Printing a status message every 1000th review
        if counter%1000 == 0:
            print("Review %d of %d"%(counter,len(reviews)))
            
        reviewFeatureVecs[counter] = featureVecMethod(review, model, num_features)
        counter = counter+1
        
    return reviewFeatureVecs


# In[ ]:


# Calculating average feature vector for training set
clean_train_reviews = []
for review in train['text']:
    clean_train_reviews.append(review_wordlist(review, remove_stopwords=True))
    
trainDataVecs = getAvgFeatureVecs(clean_train_reviews, model, num_features)


# In[ ]:


# Calculating average feature vactors for test set     
clean_test_reviews = []
for review in test["text"]:
    clean_test_reviews.append(review_wordlist(review,remove_stopwords=True))
    
testDataVecs = getAvgFeatureVecs(clean_test_reviews, model, num_features)


# In[ ]:


trn_x = pd.DataFrame(trainDataVecs)
trn_x = trn_x.dropna()

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
trn_x = scaler.fit_transform(trn_x)

trn_x = pd.DataFrame(trn_x)

trn_y = train.loc[:5276, "sentiment"]
trn_y = pd.DataFrame(trn_y)

tst = pd.DataFrame(testDataVecs)


# In[ ]:


from sklearn.model_selection import train_test_split
x_train, x_val, y_train, y_val = train_test_split(trn_x, trn_y, test_size=0.2)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, f1_score
import collections
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, VotingClassifier


# In[ ]:


# Fitting a random forest classifier to the training data

classifiers = [
    KNeighborsClassifier(3),
    SVC(probability=True),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    AdaBoostClassifier(),
    GradientBoostingClassifier()]

for clf in classifiers:
    clf.fit(x_train, y_train)
    pred_val = clf.predict(x_val)
    print(clf)
    print(classification_report(y_val, pred_val))
    print(collections.Counter(pred_val))
    ans = clf.predict(tst)
    print(collections.Counter(ans))
    print("\n")


# In[ ]:





# In[ ]:




