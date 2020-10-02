#!/usr/bin/env python
# coding: utf-8

# ![FOOD](http://www.rykneldhomes.org.uk/EasysiteWeb/getresource.axd?AssetID=88915&type=full&servicetype=Inline)**Prediction of cuisine ** 

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print("Listing in the working directory:", os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# The files given are in json format

# In[2]:


# Load files and examine first few rows

train = pd.read_json('../input/train.json')
test = pd.read_json('../input/test.json')

train.head(10) 


# In[3]:


# What are the data types in the training dataset?
train.dtypes


# In[4]:


# What is the size of this data? 

train.shape


# In[5]:


# What are the different cuisines occuring in this data?
distinct_cuisines=train.cuisine.unique()
print(distinct_cuisines)


# In[6]:


# What is the count of these unique cuisines?
len(distinct_cuisines)


# In[7]:


# How many times have these cuisines occured in the data? 

train.cuisine.value_counts()


# In[8]:


# What is the cuisine with highest number of ingredients and the lowest?
max_item=train['ingredients'].str.len().max()
min_item=train['ingredients'].str.len().min()

print(max_item)
print(min_item)


# In[9]:


train.isnull().any()


# In[10]:


import matplotlib.pyplot as plt
train.hist()


# In[11]:


train['num_ingredients'] = train['ingredients'].apply(len)
train = train[train['num_ingredients'] > 1]


# In[12]:


features = [] # list of list containg the recipes
for item in train['ingredients']:
    features.append(item)


# In[13]:


ingredients = [] # this list stores all the ingredients in all recipes (with duplicates)
for item in train['ingredients']:
    for ingr in item:
        ingredients.append(ingr) 


# In[15]:


# Fit the TfidfVectorizer to data
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(vocabulary= list(set([str(i).lower() for i in ingredients])), max_df=0.99, norm='l2', ngram_range=(1, 4))
X_tr = tfidf.fit_transform([str(i) for i in features]) # X_tr - matrix of tf-idf scores
feature_names = tfidf.get_feature_names()


# In[16]:


from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(vocabulary= list(set([str(i).lower() for i in ingredients])), max_df=0.99, norm='l2', ngram_range=(1, 4))
X_tr = tfidf.fit_transform([str(i) for i in features]) # X_tr - matrix of tf-idf scores
feature_names = tfidf.get_feature_names()


# In[17]:


# Extract the target variable
target = train['cuisine']


# In[18]:


# Train sample 
print("How training data looks like at this stage (example of one recipe):")
print(str(features[0]) + '\n' )
print("Number of records: "+ str(len(features)) + '\n')
print("target variable for this record:")
print(target[0])


# In[20]:


# Train
import re

features_processed= [] # here we will store the preprocessed training features
for item in features:
    newitem = []
    for ingr in item:
        ingr.lower() # Case Normalization - convert all to lower case 
        ingr = re.sub("[^a-zA-Z]"," ",ingr) # Remove punctuation, digits or special characters 
        ingr = re.sub((r'\b(oz|ounc|ounce|pound|lb|inch|inches|kg|to)\b'), ' ', ingr) # Remove different units  
        newitem.append(ingr)
    features_processed.append(newitem)


# In[21]:


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

# Binary representation of the training set will be employed
vectorizer = CountVectorizer(analyzer = "word",
                             ngram_range = (1,1), # unigrams
                             binary = True, #  (the default is counts)
                             tokenizer = None,    
                             preprocessor = None, 
                             stop_words = None,  
                             max_df = 0.99)


# In[22]:


train_X = vectorizer.fit_transform([str(i) for i in features_processed])

lb = LabelEncoder()
train_Y = lb.fit_transform(target)


# In[23]:


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

X_train, X_test, Y_train, Y_test = train_test_split(train_X, train_Y, test_size=0.3, random_state=0)
logreg = LogisticRegression()
logreg.fit(train_X, train_Y)


# In[24]:


Y_pred = logreg.predict(X_test)
print('Accuracy of logistic regression model'.format(logreg.score(X_test, Y_test)))

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(Y_test, Y_pred)
print(confusion_matrix)


# In[25]:


from sklearn.metrics import classification_report
print(classification_report(Y_test, Y_pred))


# In[ ]:




