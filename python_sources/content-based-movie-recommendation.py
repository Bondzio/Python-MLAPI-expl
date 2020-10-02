#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd


# In[ ]:


credits = pd.read_csv('../input/tmdb-movie-metadata/tmdb_5000_credits.csv')
movies = pd.read_csv('../input/tmdb-movie-metadata/tmdb_5000_movies.csv')


# In[ ]:


credits.head()


# In[ ]:


movies.head()


# In[ ]:


print("Credits Shape: ",credits.shape)
print("Movies Shape: ",movies.shape)


# In[ ]:


credit_renamed = credits.rename(index=str,columns={'movie_id':'id'})
movies_df = movies.merge(credit_renamed,on='id')
movies_df.head()


# In[ ]:


movies_df.columns


# In[ ]:


movies_df = movies_df.drop(columns=['homepage','title_x','title_y','production_countries'])
movies_df.head()


# In[ ]:


movies_df.columns


# In[ ]:


movies_df.info()


# In[ ]:


movies_df.head(2)['overview']


# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer


# In[ ]:


tfv = TfidfVectorizer(min_df=3, max_features=None,
                     strip_accents='unicode',analyzer='word',token_pattern=r'\w{1,}',
                     ngram_range=(1,3),
                     stop_words='english')

movies_df['overview'] = movies_df['overview'].fillna('')


# In[ ]:


tfv_matrix = tfv.fit_transform(movies_df['overview'])


# In[ ]:


print(tfv_matrix[0])


# In[ ]:


tfv_matrix.shape


# In[ ]:


from sklearn.metrics.pairwise import sigmoid_kernel


# In[ ]:


sig = sigmoid_kernel(tfv_matrix,tfv_matrix)


# In[ ]:


sig[0]


# In[ ]:


indices = pd.Series(movies_df.index,index=movies_df['original_title']).drop_duplicates()


# In[ ]:


indices


# In[ ]:


indices['Newlyweds']


# In[ ]:


sig[4799]


# In[ ]:


list(enumerate(sig[indices['Newlyweds']]))


# In[ ]:


sorted(list(enumerate(sig[indices['Newlyweds']])), key=lambda x: x[1], reverse=True)


# In[ ]:


def give_rec(title,sig=sig):
    idx = indices[title]
    sig_score = list(enumerate(sig[idx]))
    sig_score = sorted(sig_score, key=lambda x: x[1], reverse=True)
    sig_score = sig_score[1:11]
    movie_indices = [i[0] for i in sig_score]
    return movies_df['original_title'].iloc[movie_indices]


# In[ ]:


give_rec('Avatar')


# In[ ]:


give_rec('The Dark Knight')


# In[ ]:




