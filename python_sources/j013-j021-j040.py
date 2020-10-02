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


# #Nrutya Doshi J013 
# #Rishabh Jain J021
# #Reuben Rapose J040 

# Importing important libraries

# In[ ]:


import pandas as pd 
import numpy as np


# Importing dataset

# In[ ]:


# Import datasets
train = pd.read_csv('/kaggle/input/tweet-sentiment-extraction/train.csv')
test = pd.read_csv('/kaggle/input/tweet-sentiment-extraction/test.csv')
sample = pd.read_csv('/kaggle/input/tweet-sentiment-extraction/sample_submission.csv')


# Calculating & removing na values

# In[ ]:


# Calculating number of na values in dataframe
train.isnull().sum()


# In[ ]:


# Droping na values
train.dropna(inplace=True)


# In[ ]:


# Now no na values
train.isnull().sum()


# In[ ]:


train.head()


# Making a wordcloud representation

# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


def plotWordClouds(df_text,sentiment):
    text = " ".join(str(tmptext) for tmptext in df_text)
    text = text.lower()
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=300,
        max_font_size=40, 
        scale=3,
        random_state=1 # chosen at random by flipping a coin; it was heads
    ).generate(text)
  
    # plot the WordCloud image                        
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    plt.title('WordCloud - ' + sentiment)
    plt.show()         


# In[ ]:


subtext = train[train['sentiment']=='positive']['selected_text']
from wordcloud import WordCloud, STOPWORDS
stopwords = set(STOPWORDS) 
plotWordClouds(subtext,'positive')


# In[ ]:


subtext = train[train['sentiment']=='neutral']['selected_text']
plotWordClouds(subtext,'neutral')


# In[ ]:


subtext = train[train['sentiment']=='negative']['selected_text']
plotWordClouds(subtext,'negative')


# Pre-processing the data

# Converting the train & test data to lowercase

# In[ ]:


# Make all the text lowercase - casing doesn't matter when 
# we choose our selected text.
train['text'] = train['text'].apply(lambda x: x.lower())
test['text'] = test['text'].apply(lambda x: x.lower())


# Taking only words that contain alphabets in train data i.e. removing punctuations & numbers

# In[ ]:


import re


# In[ ]:


def text_data(str): # taking only the text data
  str_new = " ".join(re.findall("[a-zA-Z]+", str))
  return (str_new)


# In[ ]:


train['text'] = train['text'].apply(lambda x: text_data(x))
train['selected_text'] = train['selected_text'].apply(lambda x: text_data(x))


# In[ ]:


train.head()


# Splitting the train data into train & validation set as we want to see how the mdethod we created would would on the final test data

# In[ ]:


# Make training/test split
from sklearn.model_selection import train_test_split

X_train, X_val = train_test_split(train, train_size = 0.9, random_state = 0)


# In[ ]:


X_train.head()


# Cleaning the X_train data

# In[ ]:


import nltk
nltk.download("all")


# Tokenization

# In[ ]:


def tokenize(str_new): # tokenization
  tokens = []
  tokens = nltk.word_tokenize(str_new)
  return (tokens)


# In[ ]:


X_train['text'] = X_train['text'].apply(lambda x: tokenize(x))
X_train['selected_text'] = X_train['selected_text'].apply(lambda x: tokenize(x))


# Removing stopwords

# In[ ]:


from nltk.corpus import stopwords
def remove(tokens): # removing stopwords & punctuations
  removed = []
  stopword = stopwords.words('english') 
  for w in tokens:
    if (w not in stopword):
      removed.append(w)
  return (removed)


# In[ ]:


X_train['text'] = X_train['text'].apply(lambda x: remove(x))
X_train['selected_text'] = X_train['selected_text'].apply(lambda x: remove(x))


# POS tagging

# In[ ]:


def tagging(removed):
  pos = []
  pos.append(nltk.pos_tag(removed))
  return (pos)


# In[ ]:


X_train['text'] = X_train['text'].apply(lambda x: tagging(x))
X_train['selected_text'] = X_train['selected_text'].apply(lambda x: tagging(x))


# Lemmatization

# In[ ]:


from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


# In[ ]:


def lemmatization(pos):
  lem = WordNetLemmatizer()
  lemma = []
  for word in pos:
    for w in word:
      pos_value = ""
      if (w[1].startswith('J')):
        pos_value = wordnet.ADJ
      elif (w[1].startswith('V')):
        pos_value = wordnet.VERB
      elif (w[1].startswith('N')):
        pos_value = wordnet.NOUN
      elif (w[1].startswith('R')):
        pos_value = wordnet.ADV 
      else:
        continue
      lemma.append(lem.lemmatize(w[0],pos_value))
  return (lemma)


# In[ ]:


X_train['text'] = X_train['text'].apply(lambda x: lemmatization(x))
X_train['selected_text'] = X_train['selected_text'].apply(lambda x: lemmatization(x))


# Converting list to string

# In[ ]:


def to_string(lemma): # converting the data from list to string format for tfidf
  str1 = ' '.join([elem for elem in lemma]) 
  return (str1)


# In[ ]:


X_train['text'] = X_train['text'].apply(lambda x: to_string(x))
X_train['selected_text'] = X_train['selected_text'].apply(lambda x: to_string(x))


# In[ ]:


X_train.head()


# Creating different dataset for different sentiments

# In[ ]:


pos_train = X_train[X_train['sentiment'] == 'positive'] # contains all positive
neutral_train = X_train[X_train['sentiment'] == 'neutral']
neg_train = X_train[X_train['sentiment'] == 'negative']


# Using count vectorizer to convert words to numbers

# In[ ]:


# CountVectorizer will help calculate word counts
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(analyzer='word',max_df=0.95,stop_words='english')


# In[ ]:


X_train_cv = cv.fit_transform(X_train['text']) # has only text data


# In[ ]:


X_pos = cv.transform(pos_train['text'])
X_neutral = cv.transform(neutral_train['text'])
X_neg = cv.transform(neg_train['text'])


# In[ ]:


pos_count_df = pd.DataFrame(X_pos.toarray(), columns=cv.get_feature_names())
neutral_count_df = pd.DataFrame(X_neutral.toarray(), columns=cv.get_feature_names())
neg_count_df = pd.DataFrame(X_neg.toarray(), columns=cv.get_feature_names())


# We caculate a score for each word, which is like a tf-idf score

# Term frequency value is calculated, here for positive, pos contains the number of times a word occurs in the positive sentiment (datframe), pos_train.shape[0] will denote the number of documents 

# In[ ]:


# Create dictionaries of the words within each sentiment group, where the values are the proportions of tweets that contain those words

pos_words = {}
neutral_words = {}
neg_words = {}


# In[ ]:


for k in cv.get_feature_names(): # for every word 
    pos = pos_count_df[k].sum() # number of times the positive word occurs
    neutral = neutral_count_df[k].sum()
    neg = neg_count_df[k].sum()
    pos_words[k] = pos/pos_train.shape[0] # pos_train.shape[0] - total positive documents, therefore positive word/ positive documents, term frequency
    neutral_words[k] = neutral/neutral_train.shape[0]
    neg_words[k] = neg/neg_train.shape[0]


# Inverse document frequency is calculated here, for positive, the tf of negative & neutral is subtracted from positive, to determine how positive a word is

# In[ ]:


# We need to account for the fact that there will be a lot of words used in tweets of every sentiment.  
# Therefore, we reassign the values in the dictionary by subtracting the proportion of tweets in the other 
# sentiments that use that word.
pos_words_adj = {}
neutral_words_adj = {}
neg_words_adj = {}


# In[ ]:


for key, value in pos_words.items():
    pos_words_adj[key] = pos_words[key] - (neutral_words[key] + neg_words[key]) # this is basically idf, which means how positive is the word, does it occur in negative & neutral
    
for key, value in neutral_words.items():
    neutral_words_adj[key] = neutral_words[key] - (neg_words[key] + pos_words[key])

for key, value in neg_words.items():
    neg_words_adj[key] = neg_words[key] - (neutral_words[key] + pos_words[key])


# Here we determine the answer for the X_val, we make subset of words such that 1 gram, 2 gram, ..., then we calculate the score for the validation input using the scores for each word calculated in the previous cell, the subset with the highest score is the answer

# In[ ]:


def calculate_selected_text(df_row, tol = 0):
    
    tweet = df_row['text']
    sentiment = df_row['sentiment']
    
    if(sentiment == 'neutral'):
        return tweet 
    
    elif(sentiment == 'positive'):
        dict_to_use = pos_words_adj # Calculate word weights using the pos_words dictionary
    elif(sentiment == 'negative'):
        dict_to_use = neg_words_adj # Calculate word weights using the neg_words dictionary
        
    words = tweet.split()
    words_len = len(words)
    subsets = [words[i:j+1] for i in range(words_len) for j in range(i,words_len)] # taking combination of words 1 gram, 2 gram, ..., with 1st word, 2nd word
        
    score = 0
    selection_str = '' # This will be our choice
    lst = sorted(subsets, key = len) # Sort candidates by length for each subset
    
    
    for i in range(len(subsets)): # for all possiblities
        
        new_sum = 0 # Sum for the current substring
        
        # Calculate the sum of weights for each word in the substring
        for p in range(len(lst[i])): # go length wise
            if(lst[i][p] in dict_to_use.keys()):
                new_sum += dict_to_use[lst[i][p]]
                
            
        # If the sum is greater than the score, update our current selection
        if(new_sum > score + tol): 
            score = new_sum
            selection_str = lst[i]
            #tol = tol*5 # Increase the tolerance a bit each time we choose a selection

    # If we didn't find good substrings, return the whole text
    if(len(selection_str) == 0):
        selection_str = words                   
        
    return ' '.join(selection_str)


# In[ ]:


tol = 0.0015

X_val['predicted_selection'] = ''

for index, row in X_val.iterrows(): # rows in X validation set
    
    selected_text = calculate_selected_text(row, tol)
    
    X_val.loc[X_val['textID'] == row['textID'], ['predicted_selection']] = selected_text


# We calculate the jaccard score to see how accurate is our prediction, we basically see the similarity

# In[ ]:


def jaccard(str1, str2): # to see similarity
    a = set(str1.lower().split()) 
    b = set(str2.lower().split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c)) 


# In[ ]:


X_val['jaccard'] = X_val.apply(lambda x: jaccard(x['selected_text'], x['predicted_selection']), axis = 1)

print('The jaccard score for the validation set is:', np.mean(X_val['jaccard']))


# In[ ]:


X_val


# Now we fit the model on our entire train data & calculate the prediction for test data 

# In[ ]:


pos_tr = train[train['sentiment'] == 'positive']
neutral_tr = train[train['sentiment'] == 'neutral']
neg_tr = train[train['sentiment'] == 'negative']


# Count Vectorizer

# In[ ]:


cv = CountVectorizer(analyzer='word',max_df=0.95, min_df=2,stop_words='english')

final_cv = cv.fit_transform(train['text'])

X_pos = cv.transform(pos_tr['text'])
X_neutral = cv.transform(neutral_tr['text'])
X_neg = cv.transform(neg_tr['text'])

pos_final_count_df = pd.DataFrame(X_pos.toarray(), columns=cv.get_feature_names())
neutral_final_count_df = pd.DataFrame(X_neutral.toarray(), columns=cv.get_feature_names())
neg_final_count_df = pd.DataFrame(X_neg.toarray(), columns=cv.get_feature_names())


# Score for each word (TF-IDF value)

# In[ ]:


pos_words = {}
neutral_words = {}
neg_words = {}

for k in cv.get_feature_names():
    pos = pos_final_count_df[k].sum()
    neutral = neutral_final_count_df[k].sum()
    neg = neg_final_count_df[k].sum()
    
    pos_words[k] = pos/(pos_tr.shape[0])
    neutral_words[k] = neutral/(neutral_tr.shape[0])
    neg_words[k] = neg/(neg_tr.shape[0])


# In[ ]:


neg_words_adj = {}
pos_words_adj = {}
neutral_words_adj = {}

for key, value in neg_words.items():
    neg_words_adj[key] = neg_words[key] - (neutral_words[key] + pos_words[key])
    
for key, value in pos_words.items():
    pos_words_adj[key] = pos_words[key] - (neutral_words[key] + neg_words[key])
    
for key, value in neutral_words.items():
    neutral_words_adj[key] = neutral_words[key] - (neg_words[key] + pos_words[key])


# Prediction

# In[ ]:


tol = 0.001

for index, row in test.iterrows():
    
    selected_text = calculate_selected_text(row, tol)
    
    sample.loc[sample['textID'] == row['textID'], ['selected_text']] = selected_text


# In[ ]:


sample.head()


# Writing the prediction in the submission.csv file

# In[ ]:


sample.to_csv('submission.csv', index = False)


# In[ ]:




