#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


#Read the data and have a look at it

df = pd.read_json('../input/Dataset for Detection of Cyber-Trolls.json', lines= True)
df.head()


# In[ ]:


#Importing the needed libraries

from nltk.corpus import stopwords
import nltk
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


# In[ ]:


#Corpus contains lists of each review in a format that can be used to create the bag of words
corpus = []

for i in range (0, len(df)):                                #Iterating over each review
    review = re.sub('[^a-zA-Z]',' ',df['content'][i])       #Removing annotations
    review = review.lower()                                 #Converting everything to lower case
    review = review.split()                                 #Splitting each word in a review into a separate list
    review = ' '.join(review)                               #Joining all the words into a single list
    corpus.append(review)                                   #Forming our Corpus

corpus



# In[ ]:


bow_transformer =  CountVectorizer()               #Creating our vectorizer


# In[ ]:


bow_transformer = bow_transformer.fit(corpus)      #Fitting the vectorizer to our reviews


# In[ ]:


print(len(bow_transformer.vocabulary_))            #Looking at the extracted words from our reviews


# In[ ]:


messages_bow = bow_transformer.transform(corpus)  #Transforming to a sparse format (To use it for our training)


# In[ ]:


print(messages_bow.shape)


# In[ ]:


tfidf_transformer = TfidfTransformer().fit(messages_bow)  #Applying TF-ID to our reviews


# In[ ]:


X = tfidf_transformer.transform(messages_bow)             #Transforming to a sparse format(For training purposes)


# In[ ]:


y = []
for i in range(0,len(df)):
    y.append(df.annotation[i]['label'])           #Extracting labels from our dataset (From the dictionary)


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)   #Splitting train and test data


# In[ ]:


from sklearn.naive_bayes import MultinomialNB


# In[ ]:


classifier = MultinomialNB()   #Using Naive Byes algorithm(A common method in NLP)


# In[ ]:


classifier.fit(X_train,y_train)      #training the model
y_pred = classifier.predict(X_test)  #Predicting our test label


# In[ ]:


from sklearn.metrics import classification_report, accuracy_score


# In[ ]:


print(classification_report(y_test,y_pred))   #Results
print(accuracy_score(y_test, y_pred))


# In[ ]:





# In[ ]:





# In[ ]:




