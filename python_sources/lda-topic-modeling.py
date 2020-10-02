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


import pandas as pd

data = pd.read_csv('../input/abcnews-date-text.csv', error_bad_lines=False);
data_text = data[['headline_text']]
data_text['index'] = data_text.index
documents = data_text


# In[ ]:


len(documents)
data.tail()
#data.iloc[:,0]


# In[ ]:


documents[:5]


# In[ ]:


import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(2018)


# In[ ]:


import nltk
#nltk.download('wordnet')


# In[ ]:


print(WordNetLemmatizer().lemmatize('went', pos='v'))


# In[ ]:


stemmer = SnowballStemmer('english')
original_words = ['caresses', 'flies', 'dies', 'mules', 'denied','died', 'agreed', 'owned', 
           'humbled', 'sized','meeting', 'stating', 'siezing', 'itemization','sensational', 
           'traditional', 'reference', 'colonizer','plotted']
singles = [stemmer.stem(plural) for plural in original_words]
pd.DataFrame(data = {'original word': original_words, 'stemmed': singles})


# In[ ]:


def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result


# In[ ]:


doc_sample = documents[documents['index'] == 4310].values[0][0]

print('original document: ')
words = []
for word in doc_sample.split(' '):
    words.append(word)
print(words)
print('\n\n tokenized and lemmatized document: ')
print(preprocess(doc_sample))


# In[ ]:


processed_docs = documents['headline_text'].map(preprocess)


# In[ ]:


processed_docs[:10]


# In[ ]:


dictionary = gensim.corpora.Dictionary(processed_docs)


# In[ ]:


count = 0
for k, v in dictionary.iteritems():
    print(k, v)
    count += 1
    if count > 10:
        break


# In[ ]:


dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)


# In[ ]:


bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
bow_corpus[4310]


# In[ ]:


bow_doc_4310 = bow_corpus[4310]

for i in range(len(bow_doc_4310)):
    print("Word {} (\"{}\") appears {} time.".format(bow_doc_4310[i][0], 
                                                     dictionary[bow_doc_4310[i][0]], 
                                                     bow_doc_4310[i][1]))


# In[ ]:


from gensim import corpora, models

tfidf = models.TfidfModel(bow_corpus)


# In[ ]:


corpus_tfidf = tfidf[bow_corpus]


# In[ ]:


from pprint import pprint

for doc in corpus_tfidf:
    pprint(doc)
    break


# In[ ]:


lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=10, id2word=dictionary, passes=2, workers=2)


# In[ ]:


for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))


# In[ ]:


lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=10, id2word=dictionary, passes=2, workers=4)


# In[ ]:


for idx, topic in lda_model_tfidf.print_topics(-1):
    print('Topic: {} Word: {}'.format(idx, topic))


# In[ ]:



processed_docs[4]


# In[ ]:


data.head()


# In[ ]:


for index, score in sorted(lda_model[bow_corpus[4]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model.print_topic(index, 10)))


# In[ ]:


for index, score in sorted(lda_model_tfidf[bow_corpus[4]], key=lambda tup: -1*tup[1]):
    print("\nScore: {}\t \nTopic: {}".format(score, lda_model_tfidf.print_topic(index, 10)))


# In[ ]:




