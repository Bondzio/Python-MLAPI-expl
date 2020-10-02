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


# In[ ]:



data = pd.read_csv("/kaggle/input/sms-spam-collection-dataset/spam.csv", encoding='latin-1')


# In[ ]:


data


# In[ ]:


data = data.drop(["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], axis=1)
data = data.rename(columns={"v1":"label", "v2":"text"})


# In[ ]:


data


# In[ ]:


data.describe()


# In[ ]:


data.groupby("label").describe()


# In[ ]:


data.label.value_counts()


# In[ ]:


data.label.value_counts().plot.bar()


# In[ ]:


# Data Cleaning and Pre-Processing


# In[ ]:


import re # Use for regular expression
import nltk # for doing stopword, bag of word, lemmitization , stemmin all present in this library


# In[ ]:


from nltk.corpus import stopwords  


# In[ ]:


from nltk.stem.porter import PorterStemmer # it is used for stemming , to find Base word.


# In[ ]:


ps = PorterStemmer()


# In[ ]:


corpus = [] # creating empty corpus list


# In[ ]:


for i in range(0, len(data)):
    review = re.sub('[^a-zA-Z]', ' ', data['text'][i]) 
# removing unnecessary charachter  and replaceing it with blank ' ' with re(regular expression) library except (capital & small a-z A-Z letter), then text feature in data given, i iterate over all given sentences
    review = review.lower()  
# now lower all letter so that there would not be having any duplicate
    review = review.split()
# Splitting each and every sentences for getting list of words.    
    
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
# In this list comprehension giving condition- word in review if word not present in stopword english list apply on it stemming process.
    review = ' '.join(review) # joining all list of word into sentences
    corpus.append(review)  # now appending in created corpus list.
print(corpus)   


# In[ ]:


# Creating the Bag of Words Model


# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer  # importing CountVectorizer for creating bag of word


# In[ ]:


cv = CountVectorizer(max_features = 2500)
X = cv.fit_transform(corpus).toarray()


# In[ ]:


X


# In[ ]:


y = pd.get_dummies(data['label'])
# convering categorical variable by using dummy


# In[ ]:


y


# In[ ]:


y = y.iloc[:, 1].values

# removing one column as one column specify to identify it is ham or spam, and avoiding 


# In[ ]:


y


# In[ ]:


# Train Test Split


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y ,test_size = 0.20, random_state = 0)


# In[ ]:


# Training Model using Naive Base Classifier


# In[ ]:


from sklearn.naive_bayes import MultinomialNB
spam_detect_model = MultinomialNB().fit(X_train, y_train)


# In[ ]:


y_pred = spam_detect_model.predict(X_test)


# In[ ]:


from sklearn.metrics import confusion_matrix


# In[ ]:


Confusion_m = confusion_matrix(y_test, y_pred)


# In[ ]:


Confusion_m


# In[ ]:


from sklearn.metrics import accuracy_score


# In[ ]:


accuracy = accuracy_score(y_test, y_pred)
accuracy


# In[ ]:




