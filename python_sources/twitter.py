#!/usr/bin/env python
# coding: utf-8

# Importing the necessary libraries

# In[ ]:


import numpy as np 
import pandas as pd 
import os
import seaborn as sns
import string
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import linear_model
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score


# Loading the training and test data using pandas library

# In[ ]:


from sklearn.model_selection import train_test_split
train = pd.read_csv('../input/nlp-getting-started/train.csv')
test = pd.read_csv('../input/nlp-getting-started/test.csv')
submit = pd.read_csv("/kaggle/input/nlp-getting-started/sample_submission.csv")


# Reading the first five values of the training dataset

# In[ ]:


train.head()


# In[ ]:


print (train.shape, test.shape, submit.shape)


# Looking at the count of the null values

# In[ ]:


print(train.isnull().sum())
print(test.isnull().sum())


# In[ ]:


import matplotlib.pyplot as plt
sns.countplot(y=train.target)


# Looking at some examples of training before cleaning the text

# In[ ]:


train['text']


# Defining a function to clean the dataset

# In[ ]:


import re
def clean(text):
    text=re.sub(r'https?://\S+', '', text)
    text=re.sub(r'<.*?>','',text) 
    text=re.sub(r'\n',' ', text)
    text=re.sub('\s+', ' ', text).strip()
    return text


# In[ ]:


train['text'] = train['text'].apply(lambda x : clean(x))


# Looking at the examples after cleaning the dataset

# In[ ]:


train['text']


# In[ ]:


def remove_emoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

train['text'] = train['text'].apply(lambda x: remove_emoji(x))


# Reference : https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b


# In[ ]:


train['text']


# In[ ]:


def remove_punct(text):
    table=str.maketrans('','',string.punctuation)
    return text.translate(table)

#train_data['text'] = train_data['text'].apply(lambda x : remove_punct(x)


# Assigning x to our text and y to our target column
# 
# Splitting the training and testing dataset/
# 

# In[ ]:


x = train["text"]
y = train["target"]
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


# We need to vectorize the training dataset examples

# In[ ]:


vectorize = CountVectorizer(stop_words = 'english')
x_vector_train = vectorize.fit_transform(X_train)
x_vector_test = vectorize.transform(X_test)


# Our first model is the multinomial Naive Bayes model. Using the fit and predict methods and calculating the accuracy

# In[ ]:


model = MultinomialNB()
model.fit(x_vector_train, y_train)
prediction = model.predict(x_test_cv)
acc=accuracy_score(y_test,prediction)
print(acc)


# We will test one more model called as Ridge Classifier and printing the accuracy

# In[ ]:


clf =  linear_model.RidgeClassifier()
clf.fit(x_vector_train, y_train)
prediction1=clf.predict(x_test_cv)
acc1=accuracy_score(y_test,prediction1)
print(acc1)


# As we can see Multinomial Naive Bayes model performs a little better than Naive Bayes model by almost 2 percentage. Thus we will use that model to make our submission file

# In[ ]:


#predicting on the test values
x_test=test["text"]

#vectorizing the data
x_test_vector=vectorize.transform(x_test)

#making predictions
prediction=model.predict(x_test_vector)

#making submission
submit["target"]=prediction

print(submit.head(10))



# In[ ]:


submit.to_csv("submission.csv",index=False)


# In[ ]:




