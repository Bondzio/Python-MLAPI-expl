#!/usr/bin/env python
# coding: utf-8

# ## Daniel Cruz

# In[ ]:


#I deleted some things by mistake in the previous commit

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt 
import seaborn as sns

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
df = pd.read_csv('/kaggle/input/CORD-19-research-challenge/2020-03-13/all_sources_metadata_2020-03-13.csv')
df.head(10)


# In[ ]:


df.info()


# In[ ]:


df.describe(include='all').T


# In[ ]:


df.sha.head(10)


# In[ ]:


df.isnull().sum()


# In[ ]:


df.source_x.head(5)


# In[ ]:


df.source_x.value_counts()


# In[ ]:


pd.get_dummies(df.source_x)


# In[ ]:


pd.get_dummies(df.has_full_text).iloc[:,1:]


# In[ ]:


df.columns


# In[ ]:


short = df[['title','publish_time','abstract','authors','journal','Microsoft Academic Paper ID', 'has_full_text']]


# In[ ]:


short.head()


# In[ ]:


short.publish_time.value_counts()


# In[ ]:


short.dropna(inplace = True)


# In[ ]:


short.isnull().sum()


# In[ ]:


from collections import Counter
from functools import reduce

#short1.apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0)
#short1.str.split().str.len()
#short['title'].str.count(' ') + 1
title_counter = Counter(" ".join(short.title).split(" ")).items()
abstract_counter = Counter(" ".join(short.abstract).split(" ")).items()
journal_counter = Counter(" ".join(short.journal).split(" ")).items()


# In[ ]:


import nltk
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
print(stop_words)


# In[ ]:


import re
title_counter = re.sub("[^a-zA-Z]"," ",str(title_counter))
abstract_counter = re.sub("[^a-zA-Z]"," ",str(abstract_counter))
journal_counter = re.sub("[^a-zA-Z]"," ",str(journal_counter))


# In[ ]:


from nltk.tokenize import word_tokenize
tokens0 = word_tokenize(title_counter)
tokens0 = [w.lower() for w in tokens0]
tokens1 = word_tokenize(abstract_counter)
tokens1 = [w.lower() for w in tokens1]
tokens2 = word_tokenize(journal_counter)
tokens2 = [w.lower() for w in tokens2]
# remove punctuation from each word
import string
table = str.maketrans('', '', string.punctuation)
stripped0 = [w.translate(table) for w in tokens0]
stripped1 = [w.translate(table) for w in tokens1]
stripped2 = [w.translate(table) for w in tokens2]

# remove remaining tokens that are not alphabetic
words0 = [word for word in stripped0 if word.isalpha()]
words1 = [word for word in stripped1 if word.isalpha()]
words2 = [word for word in stripped2 if word.isalpha()]


# filter out stop words
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
words0 = [w for w in words0 if not w in stop_words]
words1 = [w for w in words1 if not w in stop_words]
words2 = [w for w in words2 if not w in stop_words]


# In[ ]:


title_counter = Counter(" ".join(words0).split(" ")).items()
abstract_counter = Counter(" ".join(words1).split(" ")).items()
journal_counter = Counter(" ".join(words2).split(" ")).items()


# In[ ]:


tc = pd.DataFrame(title_counter)
tc.columns=["Word","Frequency"]
ac = pd.DataFrame(abstract_counter)
ac.columns=["Word","Frequency"]
jc = pd.DataFrame(journal_counter)
jc.columns=["Word","Frequency"]


# In[ ]:


tc20 = tc.head(20)


# In[ ]:


tc20.plot.bar(x='Word',y='Frequency')
plt.show()


# In[ ]:


ac20 = ac.head(20)


# In[ ]:


ac20.plot.bar(x='Word',y='Frequency')
plt.show()


# In[ ]:


jc20 = jc.head(20)


# In[ ]:


jc20.plot.bar(x='Word',y='Frequency')
plt.show()


# In[ ]:





# In[ ]:




