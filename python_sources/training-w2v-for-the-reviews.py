#!/usr/bin/env python
# coding: utf-8

# # Context
# Webportals like Bhuvan get vast amount of feedback from the users. To go through all the feedback's can be a tedious job. You have to categorize opinions expressed in feedback forums. This can be utilized for feedback management system. We Classification of individual comments/reviews.and we also determining overall rating based on individual comments/reviews. So that company can get a complete idea on feedback's provided by customers and can take care on those particular fields. This makes more loyal Customers to the company, increase in business , fame ,brand value ,profits.
# 
# https://www.kaggle.com/eswarchandt/amazon-music-reviews#Musical_instruments_reviews.csv
# 
# # Content
# This file has reviewer ID , User ID, Reviewer Name, Reviewer text, helpful, Summary(obtained from Reviewer text),Overall Rating on a scale 5, Review time
# Description of columns in the file:
# 
# reviewerID - ID of the reviewer, e.g. A2SUAM1J3GNN3B
# 
# asin - ID of the product, e.g. 0000013714
# 
# reviewerName - name of the reviewer
# 
# helpful - helpfulness rating of the review, e.g. 2/3
# 
# reviewText - text of the review
# 
# overall - rating of the product
# 
# summary - summary of the review
# 
# unixReviewTime - time of the review (unix time)
# 
# reviewTime - time of the review (raw)
# 
# # Task
# You have to perform Sentimental Analysis for this data. Help the organization to understand better about their customer feedback's So that they can concentrate on those issues customer's are facing. Build the model which has highest accuracy in classifying the feedback as positive,Negative and neutral.
# 
# Task :1
# 
# You have to categorize opinions expressed in feedback forums
# 
# Task :2
# 
# You have to classify individual comments/reviews and you have to determine overall rating based on individual
# comments/reviews.
# 
# Inspiration
# This is the Problem Statement given by ISRO to classify the customer comments. This would be helpful for the organization to understand Customer feedbacks.

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings("ignore")


import pandas as pd
import numpy as np
import nltk
import string
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.metrics import roc_curve, auc
from nltk.stem.porter import PorterStemmer

import re
# Tutorial about Python regular expressions: https://pymotw.com/2/re/
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import pickle

from tqdm import tqdm
import os


# In[ ]:


raw_data = pd.read_csv('Musical_instruments_reviews.csv')
raw_data.head(5)


# In[ ]:


# Give reviews with Score>3 a positive rating, and reviews with a score<3 a negative rating.

def partition(x):
    if x < 3:
        return 0
    return 1

#changing reviews with score less than 3 to be positive and vice-versa
actualScore = raw_data['overall']
positiveNegative = actualScore.map(partition) 
raw_data['Score'] = positiveNegative
print("Number of data points in our data", raw_data.shape)
raw_data.head(5)


# # Droping Unnecessary coloums

# In[ ]:


raw_data.drop(columns='reviewerID',axis=1,inplace=True)


# In[ ]:


raw_data.drop(columns='asin',axis=1,inplace=True)
raw_data.drop(columns='helpful',axis=1,inplace=True)
raw_data.drop(columns='overall',axis=1,inplace=True)
raw_data.drop(columns='unixReviewTime',axis=1,inplace=True)
raw_data.drop(columns='reviewTime',axis=1,inplace=True)


# In[ ]:


#Sorting data according to ProductId in ascending order
sorted_data=raw_data.sort_values('reviewerID', axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')


# In[ ]:


final=sorted_data.drop_duplicates(subset={"reviewerID","reviewerName","reviewText"}, keep='first', inplace=False)
final.shape


# In[ ]:


final.head(20)


# In[ ]:


final['Score'].value_counts()

# 4.551213332033915% of negative reviews 


# # [3].  Text Preprocessing.
# 
# Now that we have finished deduplication our data requires some preprocessing before we go on further with analysis and making the prediction model.
# 
# Hence in the Preprocessing phase we do the following in the order below:-
# 
# 1. Begin by removing the html tags
# 2. Remove any punctuations or limited set of special characters like , or . or # etc.
# 3. Check if the word is made up of english letters and is not alpha-numeric
# 4. Check to see if the length of the word is greater than 2 (as it was researched that there is no adjective in 2-letters)
# 5. Convert the word to lowercase
# 6. Remove Stopwords
# 7. Finally Snowball Stemming the word (it was obsereved to be better than Porter Stemming)<br>
# 
# After which we collect the words used to describe positive and negative reviews

# In[ ]:


# printing some random reviews
sent_0 = final['reviewText'].values[0]
print(sent_0)
print("="*50)

sent_1000 = final['reviewText'].values[1000]
print(sent_1000)
print("="*50)

sent_1500 = final['reviewText'].values[1500]
print(sent_1500)
print("="*50)

sent_4900 = final['reviewText'].values[4900]
print(sent_4900)
print("="*50)


# In[ ]:


# https://stackoverflow.com/a/47091490/4084039
import re

def decontracted(phrase):
    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase


# In[ ]:


# https://gist.github.com/sebleier/554280
# we are removing the words from the stop words list: 'no', 'nor', 'not'
# <br /><br /> ==> after the above steps, we are getting "br br"
# we are including them into stop words list
# instead of <br /> if we have <br/> these tags would have revmoved in the 1st step

stopwords= set(['br', 'the', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",            "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',             'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their',            'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those',             'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',             'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',             'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',            'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',            'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very',             's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're',             've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',            "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',            "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't",             'won', "won't", 'wouldn', "wouldn't"])


# In[ ]:


# Combining all the above  
from tqdm import tqdm
from bs4 import BeautifulSoup


preprocessed_reviews = []
# tqdm is for printing the status bar
for sentance in tqdm(final['reviewText'].values):
    sentance = re.sub(r"http\S+","", str(sentance))
    sentance = BeautifulSoup(sentance, 'lxml').get_text()
    sentance = decontracted(sentance)
    sentance = re.sub("\S*\d\S*", "", sentance).strip()
    sentance = re.sub('[^A-Za-z]+', ' ', sentance)
    # https://gist.github.com/sebleier/554280
    sentance = ' '.join(e.lower() for e in sentance.split() if e.lower() not in stopwords)
    preprocessed_reviews.append(sentance.strip())


# In[ ]:


preprocessed_reviews[237]


# In[ ]:


final['reviewText']=preprocessed_reviews
final.head(5)


# <h2><font color='red'> Preprocess Summary</font></h2>

# In[ ]:


# Combining all the above  
from tqdm import tqdm
from bs4 import BeautifulSoup


preprocessed_summary = []
# tqdm is for printing the status bar
for sentance in tqdm(final['summary'].values):
    sentance = re.sub(r"http\S+","", str(sentance))
    sentance = BeautifulSoup(sentance, 'lxml').get_text()
    sentance = decontracted(sentance)
    sentance = re.sub("\S*\d\S*", "", sentance).strip()
    sentance = re.sub('[^A-Za-z]+', ' ', sentance)
    # https://gist.github.com/sebleier/554280
    sentance = ' '.join(e.lower() for e in sentance.split() if e.lower() not in stopwords)
    preprocessed_summary.append(sentance.strip())


# In[ ]:


preprocessed_summary[20]


# In[ ]:


final['summary']=preprocessed_summary
final.head(5)


# # Bag of Words

# In[ ]:


#BoW
count_vect = CountVectorizer() #in scikit-learn
count_vect.fit(preprocessed_reviews)
print("some feature names ", count_vect.get_feature_names()[:10])
print('='*50)

final_counts = count_vect.transform(preprocessed_reviews)
print("the type of count vectorizer ",type(final_counts))
print("the shape of out text BOW vectorizer ",final_counts.get_shape())
print("the number of unique words ", final_counts.get_shape()[1])


# # TF-IDF

# In[ ]:


tf_idf_vect = TfidfVectorizer(ngram_range=(1,2), min_df=10) #for unigram n bigram 1,2
tf_idf_vect.fit(preprocessed_reviews)
print("some sample features(unique words in the corpus)",tf_idf_vect.get_feature_names()[0:10])
print('='*50)

final_tf_idf = tf_idf_vect.transform(preprocessed_reviews)
print("the type of count vectorizer ",type(final_tf_idf))
print("the shape of out text TFIDF vectorizer ",final_tf_idf.get_shape())
print("the number of unique words including both unigrams and bigrams ", final_tf_idf.get_shape()[1])


# # Word2Vec
# 

# In[ ]:


# Train your own Word2Vec model using your own text corpus
i=0
list_of_sentance=[]
for sentance in preprocessed_reviews:
    list_of_sentance.append(sentance.split())


# In[ ]:


# Using Google News Word2Vectors

# in this project we are using a pretrained model by google
# its 3.3G file, once you load this into your memory 
# it occupies ~9Gb, so please do this step only if you have >12G of ram
# we will provide a pickle file wich contains a dict , 
# and it contains all our courpus words as keys and  model[word] as values
# To use this code-snippet, download "GoogleNews-vectors-negative300.bin" 
# from https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
# it's 1.9GB in size.


# http://kavita-ganesan.com/gensim-word2vec-tutorial-starter-code/#.W17SRFAzZPY
# you can comment this whole cell
# or change these varible according to your need

is_your_ram_gt_16g=False
want_to_use_google_w2v = False
want_to_train_w2v = True

if want_to_train_w2v:
    # min_count = 5 considers only words that occured atleast 5 times
    w2v_model=Word2Vec(list_of_sentance,min_count=5,size=50, workers=4)
    print(w2v_model.wv.most_similar('great'))
    print('='*50)
    print(w2v_model.wv.most_similar('worst'))
    
elif want_to_use_google_w2v and is_your_ram_gt_16g:
    if os.path.isfile('GoogleNews-vectors-negative300.bin'):
        w2v_model=KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
        print(w2v_model.wv.most_similar('great'))
        print(w2v_model.wv.most_similar('worst'))
    else:
        print("you don't have gogole's word2vec file, keep want_to_train_w2v = True, to train your own w2v ")


#  ##  We have trained our own model using the given corpus

# In[ ]:


w2v_words = list(w2v_model.wv.vocab)
print("number of words that occured minimum 5 times ",len(w2v_words))
print("sample words ", w2v_words[0:50])


# In[ ]:





# # Converting text into vector using Avg-W2V

# In[ ]:


# average Word2Vec
# compute average word2vec for each review.
sent_vectors = []; # the avg-w2v for each sentence/review is stored in this list
for sent in tqdm(list_of_sentance): # for each review/sentence
    sent_vec = np.zeros(50) # as word vectors are of zero length 50, you might need to change this to 300 if you use google's w2v
    cnt_words =0; # num of words with a valid vector in the sentence/review
    for word in sent: # for each word in a review/sentence
        if word in w2v_words:
            vec = w2v_model.wv[word]
            sent_vec += vec
            cnt_words += 1
    if cnt_words != 0:
        sent_vec /= cnt_words
    sent_vectors.append(sent_vec)
print(len(sent_vectors))
print(len(sent_vectors[0]))


# #  TFIDF W2V

# In[ ]:


# S = ["abc def pqr", "def def def abc", "pqr pqr def"]
model = TfidfVectorizer()
model.fit(preprocessed_reviews)
# we are converting a dictionary with word as a key, and the idf as a value
dictionary = dict(zip(model.get_feature_names(), list(model.idf_)))


# In[ ]:


# TF-IDF weighted Word2Vec
tfidf_feat = model.get_feature_names() # tfidf words/col-names
# final_tf_idf is the sparse matrix with row= sentence, col=word and cell_val = tfidf

tfidf_sent_vectors = []; # the tfidf-w2v for each sentence/review is stored in this list
row=0;
for sent in tqdm(list_of_sentance): # for each review/sentence 
    sent_vec = np.zeros(50) # as word vectors are of zero length
    weight_sum =0; # num of words with a valid vector in the sentence/review
    for word in sent: # for each word in a review/sentence
        if word in w2v_words and word in tfidf_feat:
            vec = w2v_model.wv[word]
#             tf_idf = tf_idf_matrix[row, tfidf_feat.index(word)]
            # to reduce the computation we are 
            # dictionary[word] = idf value of word in whole courpus
            # sent.count(word) = tf valeus of word in this review
            tf_idf = dictionary[word]*(sent.count(word)/len(sent))
            sent_vec += (vec * tf_idf)
            weight_sum += tf_idf
    if weight_sum != 0:
        sent_vec /= weight_sum
    tfidf_sent_vectors.append(sent_vec)
    row += 1


# In[ ]:


model.save("w2v_model.model")


# In[ ]:




