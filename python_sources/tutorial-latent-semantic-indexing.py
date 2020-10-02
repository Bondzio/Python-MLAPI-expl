#!/usr/bin/env python
# coding: utf-8

# # Tutorial: Latent Semantic Indexing
# This is a basic guide to efficiently training a LSI/LSA model on the English Wikipedia dump using Gensim.

# In[ ]:


from gensim.corpora import Dictionary
from gensim.models import TfidfModel, LsiModel
from multiprocessing import Pool
import sqlite3 as sql
import pandas as pd
import numpy as np
import logging
import time
import re

db = '../input/english-wikipedia-articles-20170820-sqlite/enwiki-20170820.db'
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# In[ ]:


def get_query(select, db=db):
    '''
    1. Connects to SQLite database (db)
    2. Executes select statement
    3. Return results and column names
    
    Input: 'select * from analytics limit 2'
    Output: ([(1, 2, 3)], ['col_1', 'col_2', 'col_3'])
    '''
    with sql.connect(db) as conn:
        c = conn.cursor()
        c.execute(select)
        col_names = [str(name[0]).lower() for name in c.description]
    return c.fetchall(), col_names

def tokenize(text, lower=True):
    '''
    1. Strips apostrophes
    2. Searches for all alpha tokens (exception for underscore)
    3. Return list of tokens

    Input: 'The 3 dogs jumped over Scott's tent!'
    Output: ['the', 'dogs', 'jumped', 'over', 'scotts', 'tent']
    '''
    text = re.sub("'", "", text)
    if lower:
        tokens = re.findall('''[a-z_]+''', text.lower())
    else:
        tokens = re.findall('''[A-Za-z_]''', text)
    return tokens

def get_article(article_id):
    '''
    1. Construct select statement
    2. Retrieve all section_texts associated with article_id
    3. Join section_texts into a single string (article_text)
    4. Tokenize article_text
    5. Return list of tokens
    
    Input: 100
    Output: ['the','austroasiatic','languages','in',...]
    '''
    select = '''select section_text from articles where article_id=%d''' % article_id
    docs, _ = get_query(select)
    docs = [doc[0] for doc in docs]
    doc = '\n'.join(docs)
    tokens = tokenize(doc)
    return tokens
       
class Corpus():
    def __init__(self, article_ids, dictionary, tfidf):
        self.article_ids = article_ids
        self.len = len(article_ids)
        self.dictionary = dictionary
        self.tfidf = tfidf

    def __iter__(self):
        article_ids = np.random.choice(self.article_ids, self.len, replace=False)
        with Pool(processes=4) as pool:
            docs = pool.imap_unordered(get_article, article_ids)
            for doc in docs:
                yield tfidf[dictionary.doc2bow(doc)]

    def __len__(self):
        return self.len


# First step, grab the index we'll be iterating over. In this case, we want to use section text, so let's use the implicit column: **rowid**.

# In[ ]:


select = '''select distinct article_id from articles'''
article_ids, _ = get_query(select)
article_ids = [article_id[0] for article_id in article_ids]


# Now we'll load the pre-trained/trimmed dictionary from earlier and also create a TF-IDF model.

# In[ ]:


dictionary = Dictionary.load('../input/english-wikipedia-articles-20170820-models/enwiki_2017_08_20_trimmed.dict')
tfidf = TfidfModel(dictionary=dictionary)


# Now let's train a LSA model. We'll do a single pass, and feed tokens from full articles to build the topic model.

# In[ ]:


start = time.time()
# To keep training time reasonable, let's just look at a random 10K section text sample.
sample_article_ids = np.random.choice(article_ids, 10000, replace=False)
docs = Corpus(sample_article_ids, dictionary, tfidf)
lsa = LsiModel(docs, num_topics=200, id2word=dictionary)
end = time.time()
print('Time to train LSA from generator: %0.2fs' % (end - start))


# Gensim offers built-in functionality for examining topics. Note that we only trained on a subset of the articles, so these topics are likely to be a little incoherent.

# In[ ]:


for i in range(10):
    print('Topic %d' % i)
    print(lsa.print_topic(i))


# Instead, let's look at a pre-trained LSA model.

# In[ ]:


lsa = LsiModel.load('../input/english-wikipedia-articles-20170820-models/enwiki_2017_08_20_lsa.model')


# In[ ]:




