#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.probability import FreqDist

dataset = pd.read_csv('../input/kindle_reviews.csv', na_filter=False)
df = dataset[:10000]


# ### Lets Review the data 

# In[2]:


df.head()


# In[3]:


df.columns


# In[4]:


df.dtypes


# In[5]:


print ("Shape of the dataset - ", df.shape)
#check for the missing values
df.apply(lambda x: sum(x.isnull()))


# ###  We have reviews in the range of [1-5]. Lets consider "3" as the neutral review, we can summarize the following points:

# In[6]:


df['overall'].value_counts()


# ### Lets label all the reviews as "negative review" where rating = 1 or 2 and else as "Postive reviews"

# In[7]:


# Remove neutral rated
df = df[df['overall'] != 3]
df['Positively Rated'] = np.where(df['overall'] > 3, 1, 0)

# 22 rows from reviewText are blank. Lets add sample review for it
#df['reviewText']=newdf['reviewText'].fillna("No Review", inplace=True)
#df = newdf.replace(np.nan, '', regex=True)
#df.apply(lambda x: sum(x.isnull()))
#print (newdf['reviewText'].head(10))


# In[8]:


# Number of rating which are positively rated 
df['Positively Rated'].mean()


#  ### Let's split the data in train and test datasets and apply Logistic Regression model.

# In[9]:


from  sklearn.model_selection import train_test_split

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(df['reviewText'],df['Positively Rated'], random_state=0)
print('X_train first entry: ', X_train.iloc[1])
print('\nX_train shape: ', X_train.shape)


# In[10]:


from  sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from  sklearn.metrics import roc_auc_score

# Fit the CountVectorizer to the training data
# transform the documents in the training data to a document-term matrix
vect = CountVectorizer().fit(X_train)
X_train_vectorized = vect.transform(X_train)
# Train the model
model = LogisticRegression()
model.fit(X_train_vectorized, y_train)
# Predict the transformed test documents
predictions = model.predict(vect.transform(X_test))
print('AUC: ', roc_auc_score(y_test, predictions))
# get the feature names as numpy array
feature_names = np.array(vect.get_feature_names())
# Sort the coefficients from the model
sorted_coef_index = model.coef_[0].argsort()
# Find the 10 smallest and 10 largest coefficients
# The 10 largest coefficients are being indexed using [:-11:-1] 
# so the list returned is in order of largest to smallest
print('Smallest Coefs:\n{}\n'.format(feature_names[sorted_coef_index[:10]]))
print('Largest Coefs: \n{}'.format(feature_names[sorted_coef_index[:-11:-1]]))

