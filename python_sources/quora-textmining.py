#!/usr/bin/env python
# coding: utf-8

# In[3]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

data=pd.read_csv('../input/train.csv')

# Any results you write to the current directory are saved as output.


# In[7]:


data.head()
print(data.shape)


# In[8]:


data[data['target']==1].head()


# In[21]:


len(data[data['target']==1])/len(data['target'])


# In[20]:


data['target'].value_counts()


# In[19]:


from wordcloud import WordCloud
import matplotlib.pyplot as plt
insincere_rows=data[data['target']==1]
wc=WordCloud(background_color='white').generate(' '.join(insincere_rows['question_text']))

plt.imshow(wc)


# In[23]:


from sklearn.model_selection import train_test_split

train,validate=train_test_split(data,test_size=0.3,random_state=1)

train.shape,validate.shape


# In[27]:


import nltk
def clean_sentence(doc,stopwords,stemmer):
    words=doc.split(' ')
    words_clean=[stemmer.stem(word) for word in words if word not in stopwords]
    return ' '.join(words_clean)
def clean_documents(docs_raw):
    stopwords=nltk.corpus.stopwords.words('english')
    stemmer=nltk.stem.PorterStemmer()
    docs=docs_raw.str.lower().str.replace('[^a-z ]','')
    docs_clean=docs.apply(lambda doc:clean_sentence(doc,stopwords,stemmer))
    return docs_clean
train_docs_clean=clean_documents(train['question_text'])
train_docs_clean.head()


# In[29]:


from sklearn.feature_extraction.text import CountVectorizer

vectorizer=CountVectorizer(min_df=10).fit(train_docs_clean)

dtm=vectorizer.transform(train_docs_clean)


# In[30]:


dtm.shape


# In[31]:


#pd.DataFrame(dtm.array())   ------>Memory Error


# In[33]:


from sklearn.tree import DecisionTreeClassifier

model_df=DecisionTreeClassifier(max_depth=10).fit(dtm,train['target'])


# In[35]:


validate_docs_clean = clean_documents(validate['question_text'])
dtm_validate= vectorizer.transform(validate_docs_clean)
dtm_validate


# In[38]:


predict=model_df.predict(dtm_validate)


# In[36]:


from sklearn.metrics import accuracy_score,classification_report,confusion_matrix,f1_score


# In[39]:


f1_score(validate['target'],predict)


# In[40]:


from sklearn.naive_bayes import MultinomialNB

nb=MultinomialNB().fit(dtm,train['target'])

validate_pred=nb.predict(dtm_validate)

f1_score(validate['target'],validate_pred)


# In[42]:


#from sklearn.model_selection import GridSearchCV


# In[43]:


test=pd.read_csv('../input/test.csv')

docs_clean=clean_documents(test['question_text'])

dtm_test=vectorizer.transform(docs_clean)

dtm_test


# In[45]:


test_pred=nb.predict(dtm_test)

test_pred


# In[47]:


sam_sub=pd.read_csv('../input/sample_submission.csv')


submission=pd.DataFrame({'qid':test['qid'],'prediction':test_pred})


submission[['qid','prediction']].to_csv('submission.csv',index=False)

