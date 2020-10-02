#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import yake_helper_funcs as yhf

forum_posts = pd.read_csv("../input/meta-kaggle/ForumMessages.csv")

# get forum posts

# subsample forum posts
sample_posts = forum_posts.Message[-1000:].astype(str)


# # Extract set of keywords from each post

# In[ ]:


# extact keywords & tokenize
keywords = yhf.keywords_yake(sample_posts)
keywords_tokenized = yhf.tokenizing_after_YAKE(keywords)
keyword_sets = [set(post) for post in keywords_tokenized]


# # Get word vectors for keywords in post

# In[ ]:


vectors = pd.read_csv("../input/fine-tuning-word2vec-2-0/kaggle_word2vec.model", 
                      delim_whitespace=True,
                      skiprows=[0], 
                      header=None
                     )

# set words as index rather than first column
vectors.index = vectors[0]
vectors.drop(0, axis=1, inplace=True)


# In[ ]:


def vectors_from_post(post):
    all_words = [] 

    for words in post:
        all_words.append(words) 
        
    return(vectors[vectors.index.isin(all_words)])

    
vectors_from_post(keyword_sets[0])


# In[ ]:


# test out getting forum post embedding (in the dumbest way possible)
test_vectors = vectors_from_post(keyword_sets[0])

test_vectors.mean()

