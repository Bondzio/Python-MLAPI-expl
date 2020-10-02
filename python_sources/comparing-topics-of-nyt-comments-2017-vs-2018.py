#!/usr/bin/env python
# coding: utf-8

# # Comparing topics of NYT comments (2017 vs 2018)
# 
# In 2017 readers discussed Obamacare and Donald Trump presidential campaign. In 2018 the most popular topics are Mueller's Investigation, NRA boycott and Tax Cuts Act.

# In[63]:


# Loading libraries
import pandas as pd 
import numpy as np 
import nltk
from nltk.corpus import stopwords
from sklearn.utils import resample
from gensim import corpora, models 
import warnings
warnings.filterwarnings('ignore')


# ## Preparing data of 2017 year

# In[64]:


# Loading and consolidating data
df17 = pd.read_csv('../input/Comments'+'Jan'+'2017.csv')
df17 = df17[['commentBody']]
for i in ['Feb', 'March', 'April', 'May']:
    df_temp = pd.read_csv('../input/Comments'+i+'2017.csv')
    df_temp = df_temp[['commentBody']]
    df17 = pd.concat([df17, df_temp], ignore_index=True)
del df_temp


# In[65]:


# Random selecting of 1/4 data
df17 = resample(df17, replace=False, n_samples=int(len(df17)/4), random_state=123)
df17 = df17.reset_index()


# In[66]:


# Clearing data
df17.commentBody = df17.commentBody.str.lower()
df17.commentBody = df17.commentBody.str.replace('[^A-Za-z0-9_]', ' ')
df17.commentBody = df17.commentBody.str.replace('(br)|(nytimes)|(com)|(www)|(https)|(html)|(_blank)|(href)|(title)|(click)|(rref)', '')


# In[67]:


# Function for removing stop words
stop_words = set(stopwords.words('english'))
def remove_stops(df):
    return ' '.join([w for w in df.split() if not w in stop_words])


# In[68]:


# Removing stop words
df17.commentBody = df17.commentBody.apply(remove_stops, 1)


# In[69]:


# Creating corpus of texts
documents17 = [[word for word in document.split()] for document in df17.commentBody.tolist()]
dictionary17 = corpora.Dictionary(documents17)
corpus17 = [dictionary17.doc2bow(text) for text in documents17]
tfidf17 = models.TfidfModel(corpus17)
corpus_tfidf17 = tfidf17[corpus17]


# ## Preparing data of 2018 year

# In[70]:


# Loading and consolidating data
df18 = pd.read_csv('../input/Comments'+'Jan'+'2018.csv')
df18 = df18[['commentBody']]
for i in ['Feb', 'March', 'April']:
    df_temp = pd.read_csv('../input/Comments'+i+'2018.csv')
    df_temp = df_temp[['commentBody']]
    df18 = pd.concat([df18, df_temp], ignore_index=True)
del df_temp


# In[71]:


# Random selecting of 1/4 data
df18 = resample(df18, replace=False, n_samples=int(len(df18)/4), random_state=123)
df18 = df18.reset_index()


# In[72]:


# Clearing data
df18.commentBody = df18.commentBody.str.lower()
df18.commentBody = df18.commentBody.str.replace('[^A-Za-z0-9_]', ' ')
df18.commentBody = df18.commentBody.str.replace('(br)|(nytimes)|(com)|(www)|(https)|(html)|(_blank)|(href)|(title)|(click)|(rref)', '')


# In[73]:


# Removing stop words
df18.commentBody = df18.commentBody.apply(remove_stops, 1)


# In[74]:


# Creating corpus of texts
documents18 = [[word for word in document.split()] for document in df18.commentBody.tolist()]
dictionary18 = corpora.Dictionary(documents18)
corpus18 = [dictionary18.doc2bow(text) for text in documents18]
tfidf18 = models.TfidfModel(corpus18)
corpus_tfidf18 = tfidf18[corpus18]


# ## Topic modeling

# ### Topics of 2017

# In[75]:


lsi17 = models.LsiModel(corpus_tfidf17, id2word=dictionary17, num_topics=5)
lsi17.print_topics(num_topics=5, num_words=10)


# ### Topics of 2018

# In[76]:


lsi18 = models.LsiModel(corpus_tfidf18, id2word=dictionary18, num_topics=5)
lsi18.print_topics(num_topics=5, num_words=10)

