#!/usr/bin/env python
# coding: utf-8

# # Use different NLP methods to predict movie reviews
# 
# ### Adapted from the Kaggle 'Bag of Words Meets Bags of Popcorn' Competition
# 
# For data and detailed description visit: https://www.kaggle.com/c/word2vec-nlp-tutorial

# In[ ]:


import warnings
warnings.filterwarnings('ignore')
import pandas as pd
pd.set_option('display.max_colwidth', 100)
from bs4 import BeautifulSoup  
import re
import nltk
#nltk.download() 
from nltk.corpus import stopwords # Import the stop word list
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import gensim
from gensim.models import word2vec
from gensim.models import Word2Vec
from gensim.models.keyedvectors import KeyedVectors
import logging
from sklearn.cluster import KMeans
import time


# In[ ]:


# load data
train = pd.read_csv('../input/labeledTrainData.tsv', header=0, delimiter="\t", quoting=3)
test = pd.read_csv('../input/testData.tsv', header=0, delimiter="\t", quoting=3 )
unlabeled_train = pd.read_csv('../input/unlabeledTrainData.tsv', header=0, delimiter="\t", quoting=3 )


# ## Data Cleaning and Text Preprocessing for Bag of Words

# Removing HTML Markup and dealing with Punctuation, Numbers and Stopwords

# In[ ]:


# example BeatifulSoup object to remove HTML tags and markups
example1 = BeautifulSoup(train['review'][0], 'lxml')
example1.get_text()
# Use regular expressions to do a find-and-replace for punctuations and numbers
# [] indicates group membership and ^ means "not". In other words, the re.sub() statement says, "Find anything that is NOT a lowercase letter (a-z) or an upper case letter (A-Z), and replace it with a space."
letters_only = re.sub("[^a-zA-Z]",           # The pattern to search for
                      " ",                   # The pattern to replace it with
                      example1.get_text() )  # The text to search
lower_case = letters_only.lower()        # Convert to lower case
words = lower_case.split()               # Split into words
# Remove stop words from "words"
words = [w for w in words if not w in stopwords.words("english")]
#print(words)


# In[ ]:


def review_to_words(raw_review):
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and 
    # the output is a single string (a preprocessed movie review)
    #
    # 1. Remove HTML
    review_text = BeautifulSoup(raw_review, 'lxml').get_text() 
    #
    # 2. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    #
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))                  
    # 
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]   
    #
    # 6. Join the words back into one string separated by space, 
    # and return the result.
    return( " ".join( meaningful_words ))  


# In[ ]:


# do preprocessing for every review row
train['review_preprocessed'] = train['review'].apply(lambda x: review_to_words(x))
train.head()


# ### Convert text to bag of words representation

# In[ ]:


# Initialize the "CountVectorizer" object, which is scikit-learn's
# bag of words tool.
# choose only the 5000 most frequent words as features
vectorizer = CountVectorizer(analyzer = 'word',tokenizer = None,preprocessor = None,stop_words = None,max_features = 5000) 
# fit_transform() does two functions: First, it fits the model
# and learns the vocabulary; second, it transforms our training data
# into feature vectors. The input to fit_transform should be a list of 
# strings.
train_data_features = vectorizer.fit_transform(list(train['review_preprocessed']))
# Numpy arrays are easy to work with, so convert the result to an 
# array
train_data_features = train_data_features.toarray()
train_data_features.shape


# In[ ]:


# The words in the vocabulary
vocab = vectorizer.get_feature_names()

# Sum up the counts of each vocabulary word
dist = np.sum(train_data_features, axis=0)

# For each tuple (word in the vocabulary, count of the vocabulary word)
# print the vocabulary word and the number of times it appears in the training set
for tag, count in zip(vocab, dist):
    print(count, tag)


# ## Train a random forest model with a bag of words representation and predict the sentiment 

# In[ ]:


# Initialize a Random Forest classifier with 100 trees
# Fit the forest to the training set, using the bag of words as 
# features and the sentiment labels as the response variable
forest = RandomForestClassifier(n_estimators = 100).fit(X = train_data_features, y = train['sentiment'])


# In[ ]:


# do preprocessing for every review row in test set
test['review_preprocessed'] = test['review'].apply(lambda x: review_to_words(x))
# Get a bag of words for the test set, and convert to a numpy array
test_data_features = vectorizer.transform(list(test['review_preprocessed']))
test_data_features = test_data_features.toarray()


# In[ ]:


# Use the random forest to make sentiment label predictions
result = forest.predict(test_data_features)


# In[ ]:


# Copy the results to a pandas dataframe with an "id" column and
# a "sentiment" column
output = pd.DataFrame(data={"id":test["id"], "sentiment":result})

# Use pandas to write the comma-separated output file
output.to_csv('Bag_of_Words_model.csv', index=False, quoting=3)


# # Data Cleaning and Text Preprocessing for Word2Vec

# Word2Vec expects single sentences, each one as a list of words. In other words, the input format is a list of lists. For this reason, we'll use NLTK's punkt tokenizer for sentence splitting.
# 
# To train Word2Vec it is better not to remove stop words because the algorithm relies on the broader context of the sentence in order to produce high-quality word vectors. For this reason, we will make stop word removal optional in the function below. 

# In[ ]:


def review_to_sentenceslist(review, tokenizer, remove_stopwords=False):
    # Function to split a review into parsed sentences and converts them
    # to a sequence of words,
    # optionally removing stop words.  Returns a 
    # list of sentences, where each sentence is a list of words
    #
    # 1. Use the NLTK tokenizer to split the paragraph into sentences
    raw_sentences = tokenizer.tokenize(review.strip())
    #
    # 2. Loop over each sentence
    sentences = []
    for raw_sentence in raw_sentences:
        # If a sentence is empty, skip it
        if len(raw_sentence) > 0:
            # Otherwise, get a list of words of the sentence and append it to the sentences list
            #
            #  Remove HTML
            review_text = BeautifulSoup(raw_sentence,'lxml').get_text()
            #  
            #  Remove non-letters
            review_text = re.sub("[^a-zA-Z]"," ", review_text)
            #
            #  Convert words to lower case and split them
            words = review_text.lower().split()
            #
            #  Optionally remove stop words (false by default)
            if remove_stopwords:
                stops = set(stopwords.words("english"))
                words = [w for w in words if not w in stops]
            sentences.append(words)
    #
    # 3. return the list of sentences (each sentence is a list of words, so this returns a list of lists
    return(sentences)            


# In[ ]:


# Load the punkt tokenizer for sentence splitting
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
# apply function to every review and create list of sentences, where each sentence is a list of words
print('parse unlabeld train sentences')
unlabeled_train['sentencelist'] = unlabeled_train['review'].apply(lambda x: review_to_sentenceslist(x,tokenizer=tokenizer, remove_stopwords=False))
print('parse labeld train sentences')
train['sentencelist'] = train['review'].apply(lambda x: review_to_sentenceslist(x,tokenizer=tokenizer, remove_stopwords=False))


# #### we need to concatenate the lists of lists
# 
# append adds an element to a list, and extend concatenates the first list with another list (or another iterable, not necessarily a list.)
# 
# 
# * append adds its argument as a single element to the end of a list. The length of the list itself will increase by one
# 
# x = [1, 2, 3]  
# x.append([4, 5])  
# print (x)  
# 
# result: [1, 2, 3, [4, 5]]
# 
# * extend iterates over its argument adding each element to the list, extending the list. The length of the list will increase by however many elements were in the iterable argument
# 
# x = [1, 2, 3]  
# x.extend([4, 5])  
# print (x)  
# 
# result: [1, 2, 3, 4, 5]

# In[ ]:


# Initialize an empty list of sentences
sentences = [] 

# extend sentences list to concatenate list of sentences from labeled and unlabeled train Dataframes
print('extend sentences list with labeled training set sentences')
for sentencelist in train['sentencelist']:
    sentences.extend(sentencelist)

print('extend sentences list with unlabeled training set sentences')
for sentencelist in unlabeled_train['sentencelist']:
    sentences.extend(sentencelist)
print('number of sentences:',len(sentences))


# ## Train and save Word2Vec model

# In[ ]:


# configure logging to watch Word2Vec training flow
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# train the Word2Vec Model
print('train Word2Vec model...')
word2vec_model = word2vec.Word2Vec(sentences=sentences, workers=4, size=300, min_count=40, window=10, sample=1e-3)

# If you don't plan to train the model any further, calling 
# init_sims will make the model much more memory-efficient.
word2vec_model.init_sims(replace=True)

# access its model.wv property, which holds the standalone keyed vectors
word2vec_model = word2vec_model.wv


# In order to share word vector querying code between different training algos(Word2Vec, Fastext, WordRank, VarEmbed) Google separated storage and querying of word vectors into a separate class KeyedVectors.

# In[ ]:


# It can be helpful to create a meaningful model name and 
# save the model for later use. You can load it later using Word2Vec.load()
model_name = '300features_40minwords_10context_word2vec_model'
word2vec_model.save(model_name)


# In[ ]:


# load the saved model
word2vec_model = KeyedVectors.load('300features_40minwords_10context_word2vec_model')


# ## From Words To Paragraphs, Attempt 1: Vector Averaging
# 
# One challenge with the IMDB dataset is the variable-length reviews. We need to find a way to take individual word vectors and transform them into a feature set that is the same length for every review.
# 
# Since each word is a vector in 300-dimensional space, we can use vector operations to combine the words in each review. One method is to simply average the word vectors in a given review (for this purpose, we removed stop words, which would just add noise). We add all up all values of the 300-dimensionl word vectors in one review and divide it by the number of words in the review. 
# 
# ##### Example with a 2 word review:
# 
# Vector1 = (0.1, 0.3, 0.5, ...) = word 1  
# Vector2 = (0.2, 0.5, 0.6, ...) = word 2  
# 
# average_Vector = (Vector1 + Vector2)/2 = [(0.1, 0.3, 0.5, ...)+(0.2, 0.5, 0.6, ...)]/2 = (0.3, 0.8, 1.1, ...)/2  
# average_Vector = (0.15, 0.4, 0.55, ...)

# In[ ]:


def makeFeatureVec(words, model, vector_dimensionality):
    # Function to average all of the word vectors in a given
    # paragraph
    #
    # Pre-initialize an empty numpy array (for speed)
    featureVec = np.zeros((vector_dimensionality,),dtype='float32')
    #
    number_of_words = 0.
    # 
    # Index2word is a list that contains the names of the words in 
    # the model's vocabulary. Convert it to a set, for speed 
    index2word_set = set(model.index2word)
    #
    # Loop over each word in the review and, if it is in the model's
    # vocaublary, add its feature vector to the total
    for word in words:
        if word in index2word_set: 
            number_of_words = number_of_words + 1.
            featureVec = np.add(featureVec,model[word])
    # 
    # Divide the result by the number of words to get the average
    featureVec = np.divide(featureVec,number_of_words)
    return featureVec

def review_to_wordlist(review, remove_stopwords=False):
    # Function to convert a document to a sequence of words,
    # optionally removing stop words.  Returns a list of words.
    #
    # 1. Remove HTML
    review_text = BeautifulSoup(review).get_text()
    #  
    # 2. Remove non-letters
    review_text = re.sub("[^a-zA-Z]"," ", review_text)
    #
    # 3. Convert words to lower case and split them
    words = review_text.lower().split()
    #
    # 4. Optionally remove stop words (false by default)
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    #
    # 5. Return a list of words
    return(words)


# In[ ]:


# split the train and test reviews into words (stop word removal = True)

print('split train reviews into words')
train['words'] = train['review'].apply(lambda x: review_to_wordlist(x, remove_stopwords=True))
print('split test reviews into words')
test['words'] = test['review'].apply(lambda x: review_to_wordlist(x, remove_stopwords=True))


# In[ ]:


# Calculate average feature vectors for train and test

print('calculate average feature vector for train')
train['average_feature_vector'] = train['words'].apply(lambda x: makeFeatureVec(words=x,model=word2vec_model,vector_dimensionality=word2vec_model.vector_size))
print('calculate average feature vector for test')
test['average_feature_vector'] = test['words'].apply(lambda x: makeFeatureVec(words=x,model=word2vec_model,vector_dimensionality=word2vec_model.vector_size))


# ### Train a Random Forest Model with the calculated average feature vector of reviews from the Word2Vec model

# In[ ]:


# convert average feature vectors to 300-dimenesional numpy array for random forest classifier
train_average_vectors = list(train['average_feature_vector'])
train_average_vectors = np.asarray(train_average_vectors)
print('shape of train array:',train_average_vectors.shape)

test_average_vectors = list(test['average_feature_vector'])
test_average_vectors = np.asarray(test_average_vectors)
print('shape of test array:',test_average_vectors.shape)


# In[ ]:


# init random forest classifier 
word2vec_forest = RandomForestClassifier(n_estimators = 100)

# fit model on train
word2vec_forest = word2vec_forest.fit(train_average_vectors, train['sentiment'])

# predict on test
avg_features_result = word2vec_forest.predict(test_average_vectors)


# In[ ]:


# Write the test results 
output2 = pd.DataFrame(data={'id':test['id'], 'sentiment':avg_features_result} )
output2.to_csv('Word2Vec_AverageVectors.csv', index=False, quoting=3 )


# ## From Words to Paragraphs, Attempt 2: Clustering 
# 
# Word2Vec creates clusters of semantically related words, so another possible approach is to exploit the similarity of words within a cluster. Grouping vectors in this way is known as "vector quantization." To accomplish this, we first need to find the centers of the word clusters, which we can do by using a clustering algorithm such as K-Means.

# In[ ]:


# Start time
start = time.time()

# Set "k" (num_clusters) to be 1/5th of the vocabulary size, or an
# average of 5 words per cluster
num_clusters = round(word2vec_model.syn0.shape[0] / 5)

# Initalize a k-means object and use it to extract centroids
# The cluster assignment for each word is then stored in 'kmeans_cluster'
kmeans_cluster = KMeans(n_clusters = num_clusters).fit_predict(word2vec_model.syn0)

# Get the end time and print how long the process took
end = time.time()
elapsed = end - start
print('Time taken for K Means clustering:', elapsed, 'seconds.')


# In[ ]:


# Create a Word : Centroid dictionary, mapping each vocabulary word to a cluster number                                                                                
word_centroid_dict = dict(zip(word2vec_model.index2word, kmeans_cluster))


# In[ ]:


# Function to convert reviews into bags-of-centroids
# This works just like Bag of Words but uses semantically related clusters instead of individual words

def create_bag_of_centroids(wordlist, word_centroid_dict):
    #
    # The number of clusters is equal to the highest cluster index
    # in the word / centroid map
    num_centroids = max(word_centroid_dict.values()) + 1
    #
    # Pre-allocate the bag of centroids vector (for speed)
    bag_of_centroids = np.zeros(num_centroids, dtype='float32')
    #
    # Loop over the words in the review. If the word is in the vocabulary,
    # find which cluster it belongs to, and increment that cluster count 
    # by one
    for word in wordlist:
        if word in word_centroid_dict:
            index = word_centroid_dict[word]
            bag_of_centroids[index] += 1
    #
    # Return the "bag of centroids"
    return bag_of_centroids


# In[ ]:


# Create bags of centroids for our train and test

print('calculate bags of centroids for train')
train['bags_of_centroids'] = train['words'].apply(lambda x: create_bag_of_centroids(wordlist=x,word_centroid_dict=word_centroid_dict))
print('calculate bags of centroids for test')
test['bags_of_centroids'] = test['words'].apply(lambda x: create_bag_of_centroids(wordlist=x,word_centroid_dict=word_centroid_dict))


# ### Train a Random Forest Model with a bag of words representation of kmeans centroids of Word2Vec model

# In[ ]:


# convert average feature vectors to numpy array for random forest classifier
train_bags_of_centroids = list(train['bags_of_centroids'])
train_bags_of_centroids = np.asarray(train_bags_of_centroids)
print('shape of train array:',train_bags_of_centroids.shape)

test_bags_of_centroids = list(test['bags_of_centroids'])
test_bags_of_centroids = np.asarray(test_bags_of_centroids)
print('shape of test array:',test_bags_of_centroids.shape)


# In[ ]:


# init random forest classifier 
bags_of_centroids_forest = RandomForestClassifier(n_estimators = 100)

# fit model on train
bags_of_centroids_forest = bags_of_centroids_forest.fit(train_bags_of_centroids, train['sentiment'])

# predict on test
bags_of_centroids_result = bags_of_centroids_forest.predict(test_bags_of_centroids)


# In[ ]:


# Write the test results 
output3 = pd.DataFrame(data={'id':test['id'], 'sentiment':bags_of_centroids_result})
output3.to_csv('BagOfCentroids.csv', index=False, quoting=3)

