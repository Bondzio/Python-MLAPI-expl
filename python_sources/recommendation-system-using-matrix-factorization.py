#!/usr/bin/env python
# coding: utf-8

# # Recommendation System using Matrix Factorization

# In[ ]:


from sklearn.datasets import dump_svmlight_file
import numpy as np
import pandas as pd
import os
import urllib
import zipfile
from sklearn.model_selection import train_test_split
import shutil
 
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
 
import tensorflow as tf
from tensorflow import keras
from keras.optimizers import Adam

get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


datasets = {'ml100k':'http://files.grouplens.org/datasets/movielens/ml-100k.zip',
            'ml20m':'http://files.grouplens.org/datasets/movielens/ml-20m.zip',
            'mllatestsmall':'http://files.grouplens.org/datasets/movielens/ml-latest-small.zip',
            'ml10m':'http://files.grouplens.org/datasets/movielens/ml-10m.zip',
            'ml1m':'http://files.grouplens.org/datasets/movielens/ml-1m.zip'
            }


# In[ ]:


get_ipython().system('mkdir sample_data')


# In[ ]:


dt = "mllatestsmall"
dt_name = os.path.basename(datasets[dt])
 
print('Downloading {}'.format(dt_name))
with urllib.request.urlopen(datasets[dt]) as response, open('./sample_data/'+dt_name, 'wb') as out_file:
    shutil.copyfileobj(response, out_file)
print('Download completed')


# In[ ]:


get_ipython().system('unzip sample_data/ml-latest-small.zip')
get_ipython().system(' ls -Rp .')


# In[ ]:


dataset = pd.read_csv("./ml-latest-small/ratings.csv",sep=',',names="user_id,item_id,rating,timestamp".split(","), skiprows=1)
print(dataset.shape)
dataset.head()


# In[ ]:


dataset.user_id = dataset.user_id.astype('category').cat.codes.values
dataset.item_id = dataset.item_id.astype('category').cat.codes.values


# In[ ]:


train, test = train_test_split(dataset, test_size=0.2)


# In[ ]:


n_users, n_movies = len(dataset.user_id.unique()), len(dataset.item_id.unique())
n_latent_factors = 20


# In[ ]:


keras.backend.clear_session()

movie_input = keras.layers.Input(shape=[1],name='Item')
movie_embedding = keras.layers.Embedding(n_movies + 1, n_latent_factors, name='Movie-Embedding')(movie_input)
movie_vec = keras.layers.Flatten(name='FlattenMovies')(movie_embedding)
 
user_input = keras.layers.Input(shape=[1],name='User')
user_vec = keras.layers.Flatten(name='FlattenUsers')(keras.layers.Embedding(n_users + 1, n_latent_factors,name='User-Embedding')(user_input))
 
prod = keras.layers.dot([movie_vec, user_vec], axes=1,name='DotProduct')
model = keras.Model([user_input, movie_input], prod)

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae', 'mse'])
model.summary()


# In[ ]:


tf.keras.utils.plot_model(model)


# In[ ]:


history = model.fit([train.user_id, train.item_id], train.rating, batch_size=32, epochs=150, verbose=1)


# In[ ]:


model.predict([train.user_id[:3], train.item_id[:3]])


# In[ ]:


train.rating[:3]


# In[ ]:


pd.Series(history.history['loss']).plot()
plt.xlabel("Epoch")
plt.ylabel("Training Error")


# In[ ]:


results = model.evaluate((test.user_id, test.item_id), test.rating, batch_size=1)


# # We now can obtain two embedding matrices for users and items.

# In[ ]:


movie_embedding_learnt = model.get_layer(name='Movie-Embedding').get_weights()[0]
pd.DataFrame(movie_embedding_learnt).describe()


# In[ ]:


user_embedding_learnt = model.get_layer(name='User-Embedding').get_weights()[0]


# In[ ]:


def recommend(user_id, number_of_movies=5):
  movies = user_embedding_learnt[user_id]@movie_embedding_learnt.T
  mids = np.argpartition(movies, -number_of_movies)[-number_of_movies:]
  return mids


# In[ ]:


recommend(user_id=1)


# [ref](https://petamind.com/)

# In[ ]:




