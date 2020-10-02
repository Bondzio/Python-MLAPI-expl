#!/usr/bin/env python
# coding: utf-8

# This notebook is intended to test the hero python library for principal component analysis.

# In[ ]:


get_ipython().system('pip install texthero')


# In[ ]:


import numpy as np
import texthero as hero
import pandas as pd

df = pd.read_csv("../input/ireland-historical-news/ireland-news-headlines.csv")
df.head(2)


# In[ ]:


df['pca'] = {
  df['headline_text']
  .pipe(hero.tokenize)
  .pipe(hero.tfidf)
  .pipe(hero.pca)
}

hero.scatterplot(df, 'pca', color='headline_category')


# In[ ]:


df['headline_clean'] = {
  df['headline_text'].str.lower()
  .pipe(hero.remove_digits)
  .pipe(hero.remove_punctuation)
  .pipe(hero.remove_diacritics)
  .pipe(hero.remove_stopwords)
}

df['pca_clean'] = {
  df['headline_clean']
  .pipe(hero.tokenize)
  .pipe(hero.tfidf)
  .pipe(hero.pca)
}

hero.scatterplot(df, 'pca_clean', color='headline_category')

