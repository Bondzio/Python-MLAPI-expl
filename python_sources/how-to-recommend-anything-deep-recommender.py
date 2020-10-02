#!/usr/bin/env python
# coding: utf-8

# # How To Recommend Anything?
# 
# **To support people best possible on their way through life, it is necessary to have an optimal recommendation on hand.**<br>
# Whether you want to introduce people among themselves in your social network, try to recommend a suitable supplement for the shopping basket of your customers or need a hint for yourself which movie to watch in the evening, there are unlimited possibilities to apply recommendation engines/systems around us.
# 
# In this notebook I will explore and compare different algorithms and approaches to recommend anything. I am using the **[netflix movie-dataset](https://www.kaggle.com/netflix-inc/netflix-prize-data/home)** and the **[movies-dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset/home)** for this purpose.
# 
# Feel free to suggest suggestions or to comment comments.
# 
# + [1. Import Libraries](#1)<br>
# + [2. Load Movie-Data](#2)<br>
# + [3. Load User-Data And Preprocess Data-Structure](#3)<br>
# + [4. When Were The Movies Released?](#4)<br>
# + [5. How Are The Ratings Distributed?](#5)<br>
# + [6. When Have The Movies Been Rated?](#6)<br>
# + [7. How Are The Number Of Ratings Distributed For The Movies And The Users?](#7)<br>
# + [8. Filter Sparse Movies And Users](#8)<br>
# + [9. Create Train- And Testset](#9)<br>
# + [10. Transform The User-Ratings To User-Movie-Matrix](#10)<br>
# + [11. Recommendation Engines](#11)<br>
#  + [11.1. Mean Rating](#11.1)<br>
#  + [11.2. Weighted Mean Rating](#11.2)<br>
#  + [11.3. Cosine User-User Similarity](#11.3)<br>
#  + [11.4. Cosine TFIDF Movie Description Similarity](#11.4)<br>
#  + [11.5. Matrix Factorisation With Keras And Gradient Descent](#11.5)<br>
#  + [11.6. Deep Learning With Keras](#11.6)<br>
#  + [11.7. Deep Hybrid System With Metadata And Keras](#11.7)<br>
# + [12. Exploring Python Libraries](#12)<br>
#  + [12.1. Surprise Library](#12.1)<br>
#  + [12.2. Lightfm Library](#12.2)<br>
# + [13. Conclusion](#13)<br>
# 
# ***
# ## <a id=1>1. Import Libraries</a>

# In[ ]:


# To store the data
import pandas as pd

# To do linear algebra
import numpy as np

# To create plots
import matplotlib.pyplot as plt

# To create interactive plots
from plotly.offline import init_notebook_mode, plot, iplot
import plotly.graph_objs as go
init_notebook_mode(connected=True)

# To shift lists
from collections import deque

# To compute similarities between vectors
from sklearn.metrics import mean_squared_error
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# To use recommender systems
import surprise as sp
from surprise.model_selection import cross_validate

# To create deep learning models
from keras.layers import Input, Embedding, Reshape, Dot, Concatenate, Dense, Dropout
from keras.models import Model

# To create sparse matrices
from scipy.sparse import coo_matrix

# To light fm
from lightfm import LightFM
from lightfm.evaluation import precision_at_k

# To stack sparse matrices
from scipy.sparse import vstack


# ***
# ## <a id=2>2. Load Movie-Data</a>

# In[ ]:


# Load data for all movies
movie_titles = pd.read_csv('../input/netflix-prize-data/movie_titles.csv', 
                           encoding = 'ISO-8859-1', 
                           header = None, 
                           names = ['Id', 'Year', 'Name']).set_index('Id')

print('Shape Movie-Titles:\t{}'.format(movie_titles.shape))
movie_titles.sample(5)


# There are roughly **18.000 movies** in the ratings dataset and the metadata for the movies contains only the **release date and the movie title.**

# In[ ]:


# Load a movie metadata dataset
movie_metadata = pd.read_csv('../input/the-movies-dataset/movies_metadata.csv', low_memory=False)[['original_title', 'overview', 'vote_count']].set_index('original_title').dropna()
# Remove the long tail of rarly rated moves
movie_metadata = movie_metadata[movie_metadata['vote_count']>10].drop('vote_count', axis=1)

print('Shape Movie-Metadata:\t{}'.format(movie_metadata.shape))
movie_metadata.sample(5)


# About **21.000 entries** are in the movie metadata dataset. 
# 
# ***
# ## <a id=3>3. Load User-Data And Preprocess Data-Structure</a>
# 
# The user-data structure has to be preprocessed to extract all ratings and form a matrix, since the file-structure is a messy mixture of json and csv.

# In[ ]:


# Load single data-file
df_raw = pd.read_csv('../input/netflix-prize-data/combined_data_1.txt', header=None, names=['User', 'Rating', 'Date'], usecols=[0, 1, 2])


# Find empty rows to slice dataframe for each movie
tmp_movies = df_raw[df_raw['Rating'].isna()]['User'].reset_index()
movie_indices = [[index, int(movie[:-1])] for index, movie in tmp_movies.values]

# Shift the movie_indices by one to get start and endpoints of all movies
shifted_movie_indices = deque(movie_indices)
shifted_movie_indices.rotate(-1)


# Gather all dataframes
user_data = []

# Iterate over all movies
for [df_id_1, movie_id], [df_id_2, next_movie_id] in zip(movie_indices, shifted_movie_indices):
    
    # Check if it is the last movie in the file
    if df_id_1<df_id_2:
        tmp_df = df_raw.loc[df_id_1+1:df_id_2-1].copy()
    else:
        tmp_df = df_raw.loc[df_id_1+1:].copy()
        
    # Create movie_id column
    tmp_df['Movie'] = movie_id
    
    # Append dataframe to list
    user_data.append(tmp_df)

# Combine all dataframes
df = pd.concat(user_data)
del user_data, df_raw, tmp_movies, tmp_df, shifted_movie_indices, movie_indices, df_id_1, movie_id, df_id_2, next_movie_id
print('Shape User-Ratings:\t{}'.format(df.shape))
df.sample(5)


# There are about **24.000.000 different ratings**.<br>
# I loaded only a single file of four to reduce memory footprint and accelerate computation. Keep in mind that this approach could introduce biases in the data.
# 
# ***
# ## <a id=4>4. When Were The Movies Released?</a>

# In[ ]:


# Get data
data = movie_titles['Year'].value_counts().sort_index()

# Create trace
trace = go.Scatter(x = data.index,
                   y = data.values,
                   marker = dict(color = '#db0000'))
# Create layout
layout = dict(title = '{} Movies Grouped By Year Of Release'.format(movie_titles.shape[0]),
              xaxis = dict(title = 'Release Year'),
              yaxis = dict(title = 'Movies'))

# Create plot
fig = go.Figure(data=[trace], layout=layout)
iplot(fig)


# Many movies on Netflix have been released in this millennial. Whether Netflix prefers young movies or there are no old movies left can not be deduced from this plot.<br>
# The decline for the rightmost point is probably caused by an **incomplete last year.**
# 
# ***
# ## <a id=5>5. How Are The Ratings Distributed?</a>

# In[ ]:


# Get data
data = df['Rating'].value_counts().sort_index(ascending=False)

# Create trace
trace = go.Bar(x = data.index,
               text = ['{:.1f} %'.format(val) for val in (data.values / df.shape[0] * 100)],
               textposition = 'auto',
               textfont = dict(color = '#000000'),
               y = data.values,
               marker = dict(color = '#db0000'))
# Create layout
layout = dict(title = 'Distribution Of {} Netflix-Ratings'.format(df.shape[0]),
              xaxis = dict(title = 'Rating'),
              yaxis = dict(title = 'Count'))
# Create plot
fig = go.Figure(data=[trace], layout=layout)
iplot(fig)


# Netflix movies rarely have a rating lower than three. **Most ratings have between three and four stars.**<br>
# The distribution is probably biased, since only people liking the movies proceed to be customers and others presumably will leave the platform.
# 
# ***
# ## <a id=6>6. When Have The Movies Been Rated?</a>

# In[ ]:


# Get data
data = df['Date'].value_counts()
data.index = pd.to_datetime(data.index)
data.sort_index(inplace=True)

# Create trace
trace = go.Scatter(x = data.index,
                   y = data.values,
                   marker = dict(color = '#db0000'))
# Create layout
layout = dict(title = '{} Movie-Ratings Grouped By Day'.format(df.shape[0]),
              xaxis = dict(title = 'Date'),
              yaxis = dict(title = 'Ratings'))

# Create plot
fig = go.Figure(data=[trace], layout=layout)
iplot(fig)


# With beginning of november 2005  a strange decline in ratings can be observed. Furthermore two unnormal peaks are in january and april 2005.
# 
# ***
# ## <a id=7>7. How Are The Number Of Ratings Distributed For The Movies And The Users?</a>
# 
# 

# In[ ]:


##### Ratings Per Movie #####
# Get data
data = df.groupby('Movie')['Rating'].count().clip(upper=9999)

# Create trace
trace = go.Histogram(x = data.values,
                     name = 'Ratings',
                     xbins = dict(start = 0,
                                  end = 10000,
                                  size = 100),
                     marker = dict(color = '#db0000'))
# Create layout
layout = go.Layout(title = 'Distribution Of Ratings Per Movie (Clipped at 9999)',
                   xaxis = dict(title = 'Ratings Per Movie'),
                   yaxis = dict(title = 'Count'),
                   bargap = 0.2)

# Create plot
fig = go.Figure(data=[trace], layout=layout)
iplot(fig)



##### Ratings Per User #####
# Get data
data = df.groupby('User')['Rating'].count().clip(upper=199)

# Create trace
trace = go.Histogram(x = data.values,
                     name = 'Ratings',
                     xbins = dict(start = 0,
                                  end = 200,
                                  size = 2),
                     marker = dict(color = '#db0000'))
# Create layout
layout = go.Layout(title = 'Distribution Of Ratings Per User (Clipped at 199)',
                   xaxis = dict(title = 'Ratings Per User'),
                   yaxis = dict(title = 'Count'),
                   bargap = 0.2)

# Create plot
fig = go.Figure(data=[trace], layout=layout)
iplot(fig)


# The ratings per movie as well as the ratings per user both have nearly a perfect **exponential decay**. Only very few 
# movies/users have many ratings. 
# 
# ***
# ## <a id=8>8. Filter Sparse Movies And Users</a>
# 
# To reduce the dimensionality of the dataset I am filtering rarely rated movies and rarely rating users out.

# In[ ]:


# Filter sparse movies
min_movie_ratings = 10000
filter_movies = (df['Movie'].value_counts()>min_movie_ratings)
filter_movies = filter_movies[filter_movies].index.tolist()

# Filter sparse users
min_user_ratings = 200
filter_users = (df['User'].value_counts()>min_user_ratings)
filter_users = filter_users[filter_users].index.tolist()

# Actual filtering
df_filterd = df[(df['Movie'].isin(filter_movies)) & (df['User'].isin(filter_users))]
del filter_movies, filter_users, min_movie_ratings, min_user_ratings
print('Shape User-Ratings unfiltered:\t{}'.format(df.shape))
print('Shape User-Ratings filtered:\t{}'.format(df_filterd.shape))


# After filtering sparse movies and users about **4.200.000 ratings** are left.
# 
# ***
# ## <a id=9>9. Create Train- And Testset</a>

# In[ ]:


# Shuffle DataFrame
df_filterd = df_filterd.drop('Date', axis=1).sample(frac=1).reset_index(drop=True)

# Testingsize
n = 100000

# Split train- & testset
df_train = df_filterd[:-n]
df_test = df_filterd[-n:]


# The trainset will be used to train all models and the **testset ensures comparibility** between all models with the **RMSE metric.**
# 
# ***
# ## <a id=10>10. Transform The User-Ratings To User-Movie-Matrix</a>
# 
# A **large, sparse matrix** will be created in this step. Each **row will represent a user** and its ratings and the **columns are the movies.**<br>
# The interesting entries are the empty values in the matrix. 
# 
# **Empty values are unrated movies and could contain high values** and therefore should be good recommendations for the respective user.<br>
# The objective is to **estimate the empty values** to help our users.

# In[ ]:


# Create a user-movie matrix with empty values
df_p = df_train.pivot_table(index='User', columns='Movie', values='Rating')
print('Shape User-Movie-Matrix:\t{}'.format(df_p.shape))
df_p.sample(3)


# ***
# ## <a id=11>11. Recommendation Engines</a>
# ### <a id=11.1>11.1. Mean Rating</a>
# 
# Computing the **mean rating for all movies** creates a ranking. The recommendation will be the same for all users and can be **used if there is no information on the user.**<br>
# Variations of this approach can be separate rankings for each country/year/gender/... and to use them individually to recommend movies/items to the user.
# 
# It has to be noted that this approach is **biased and favours movies with fewer ratings**, since large numbers of ratings tend to be less extreme in its mean ratings.

# In[ ]:


# Top n movies
n = 10

# Compute mean rating for all movies
ratings_mean = df_p.mean(axis=0).sort_values(ascending=False).rename('Rating-Mean').to_frame()

# Count ratings for all movies
ratings_count = df_p.count(axis=0).rename('Rating-Count').to_frame()

# Combine ratings_mean, ratings_count and movie_titles
ranking_mean_rating = ratings_mean.head(n).join(ratings_count).join(movie_titles.drop('Year', axis=1))


# Join labels and predictions
df_prediction = df_test.set_index('Movie').join(ratings_mean)[['Rating', 'Rating-Mean']]
y_true = df_prediction['Rating']
y_pred = df_prediction['Rating-Mean']

# Compute RMSE
rmse = np.sqrt(mean_squared_error(y_true=y_true, y_pred=y_pred))


# Create trace
trace = go.Bar(x = ranking_mean_rating['Rating-Mean'],
               text = ranking_mean_rating['Name'].astype(str) +': '+ ranking_mean_rating['Rating-Count'].astype(str) + ' Ratings',
               textposition = 'outside',
               textfont = dict(color = '#000000'),
               orientation = 'h',
               y = list(range(1, n+1)),
               marker = dict(color = '#db0000'))
# Create layout
layout = dict(title = 'Ranking Of Top {} Mean-Movie-Ratings: {:.4f} RMSE'.format(n, rmse),
              xaxis = dict(title = 'Mean-Rating',
                          range = (4.3, 4.55)),
              yaxis = dict(title = 'Movie'))
# Create plot
fig = go.Figure(data=[trace], layout=layout)
iplot(fig)


# ### <a id=11.2>11..2. Weighted Mean Rating</a>
# 
# To tackle the problem of the unstable mean with few ratings **e.g. IDMb uses a weighted rating.** Many good ratings outweigh few in this algorithm. 
# 

# In[ ]:


# Number of minimum votes to be considered
m = 1000

# Mean rating for all movies
C = df_p.stack().mean()

# Mean rating for all movies separatly
R = df_p.mean(axis=0).values

# Rating count for all movies separatly
v = df_p.count().values


# Weighted formula to compute the weighted rating
weighted_score = (v/ (v+m) *R) + (m/ (v+m) *C)
# Sort ids to ranking
weighted_ranking = np.argsort(weighted_score)[::-1]
# Sort scores to ranking
weighted_score = np.sort(weighted_score)[::-1]
# Get movie ids
weighted_movie_ids = df_p.columns[weighted_ranking]


# Join labels and predictions
df_prediction = df_test.set_index('Movie').join(pd.DataFrame(weighted_score, index=weighted_movie_ids, columns=['Prediction']))[['Rating', 'Prediction']]
y_true = df_prediction['Rating']
y_pred = df_prediction['Prediction']

# Compute RMSE
rmse = np.sqrt(mean_squared_error(y_true=y_true, y_pred=y_pred))


# Create DataFrame for plotting
df_plot = pd.DataFrame(weighted_score[:n], columns=['Rating'])
df_plot.index = weighted_movie_ids[:10]
ranking_weighted_rating = df_plot.join(ratings_count).join(movie_titles)
del df_plot


# Create trace
trace = go.Bar(x = ranking_weighted_rating['Rating'],
               text = ranking_weighted_rating['Name'].astype(str) +': '+ ranking_weighted_rating['Rating-Count'].astype(str) + ' Ratings',
               textposition = 'outside',
               textfont = dict(color = '#000000'),
               orientation = 'h',
               y = list(range(1, n+1)),
               marker = dict(color = '#db0000'))
# Create layout
layout = dict(title = 'Ranking Of Top {} Weighted-Movie-Ratings: {:.4f} RMSE'.format(n, rmse),
              xaxis = dict(title = 'Weighted Rating',
                          range = (4.15, 4.6)),
              yaxis = dict(title = 'Movie'))
# Create plot
fig = go.Figure(data=[trace], layout=layout)
iplot(fig)


# The variable **"m" can be seen as regularizing parameter.** Changing it determines how  much weight is put onto the movies with many ratings.<br>
# Even if there is a better ranking the RMSE decreased slightly. There is a **trade-off between interpretability and predictive power.**
# 
# ### <a id=11.3>11.3. Cosine User-User Similarity</a>
# 
# Interpreting each row of the matrix as a vector, a similarity between all user-vectors can be computed. This enables us to find all similar users and to work on user-specific recommendations. **Recommending high rated movies of similar users** to a specific user seems reasonable.<br>
# Since there are still empty values left in the matrix, we have to use a reliable way to impute a decent value. A simple first approach is to **fill in the mean of each user into the empty values.**<br>
# Afterwards the **ratings of all similar users will be weighted with their similarity score and the mean will be computed.** Filtering for the unrated movies of a user reveals the best recommendations.<br>
# You can easily adapt this process to find similar items by computing the item-item similarity the same way. Since the matrix is mostly sparse and there are more users than items, this could be better for the RMSE score.

# In[ ]:


# User index for recommendation
user_index = 0

# Number of similar users for recommendation
n_recommendation = 100

# Plot top n recommendations
n_plot = 10


# Fill in missing values
df_p_imputed = df_p.T.fillna(df_p.mean(axis=1)).T

# Compute similarity between all users
similarity = cosine_similarity(df_p_imputed.values)

# Remove self-similarity from similarity-matrix
similarity -= np.eye(similarity.shape[0])


# Sort similar users by index
similar_user_index = np.argsort(similarity[user_index])[::-1]
# Sort similar users by score
similar_user_score = np.sort(similarity[user_index])[::-1]


# Get unrated movies
unrated_movies = df_p.iloc[user_index][df_p.iloc[user_index].isna()].index

# Weight ratings of the top n most similar users with their rating and compute the mean for each movie
mean_movie_recommendations = (df_p_imputed.iloc[similar_user_index[:n_recommendation]].T * similar_user_score[:n_recommendation]).T.mean(axis=0)

# Filter for unrated movies and sort results
best_movie_recommendations = mean_movie_recommendations[unrated_movies].sort_values(ascending=False).to_frame().join(movie_titles)


# Create user-id mapping
user_id_mapping = {id:i for i, id in enumerate(df_p_imputed.index)}

prediction = []
# Iterate over all testset items
for user_id in df_test['User'].unique():
    
    # Sort similar users by index
    similar_user_index = np.argsort(similarity[user_id_mapping[user_id]])[::-1]
    # Sort similar users by score
    similar_user_score = np.sort(similarity[user_id_mapping[user_id]])[::-1]
    
    for movie_id in df_test[df_test['User']==user_id]['Movie'].values:

        # Compute predicted score
        score = (df_p_imputed.iloc[similar_user_index[:n_recommendation]][movie_id] * similar_user_score[:n_recommendation]).values.sum() / similar_user_score[:n_recommendation].sum()
        prediction.append([user_id, movie_id, score])
        

# Create prediction DataFrame
df_pred = pd.DataFrame(prediction, columns=['User', 'Movie', 'Prediction']).set_index(['User', 'Movie'])
df_pred = df_test.set_index(['User', 'Movie']).join(df_pred)


# Get labels and predictions
y_true = df_pred['Rating'].values
y_pred = df_pred['Prediction'].values

# Compute RMSE
rmse = np.sqrt(mean_squared_error(y_true=y_true, y_pred=y_pred))


# Create trace
trace = go.Bar(x = best_movie_recommendations.iloc[:n_plot, 0],
               text = best_movie_recommendations['Name'],
               textposition = 'inside',
               textfont = dict(color = '#000000'),
               orientation = 'h',
               y = list(range(1, n_plot+1)),
               marker = dict(color = '#db0000'))
# Create layout
layout = dict(title = 'Ranking Of Top {} Recommended Movies For A User Based On Similarity: {:.4f} RMSE'.format(n_plot, rmse),
              xaxis = dict(title = 'Recommendation-Rating',
                           range = (4.1, 4.5)),
              yaxis = dict(title = 'Movie'))
# Create plot
fig = go.Figure(data=[trace], layout=layout)
iplot(fig)


# ### <a id=11.4>11.4. Cosine TFIDF Movie Description Similarity</a>
# 
# If there is no historical data for a user or there is reliable metadata for each movie, it can be useful to **compare the metadata of the movies to find similar ones.**<br>
# In this approch I will use the **movie description to create a TFIDF-matrix**, which counts and weights words in all descriptions, and compute a cosine similarity between all of those sparse text-vectors. This can easily be extended to more or different features if you like.<br>
# Unfortunately it is impossible for this model to compute a RMSE score, since the model does not recommend the movies directly.<br>
# In this way it is possible to **find movies closly related to each other**, but it is **hard to find movies of different genres/categories.**

# In[ ]:


# Create tf-idf matrix for text comparison
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movie_metadata['overview'].dropna())


# Compute cosine similarity between all movie-descriptions
similarity = cosine_similarity(tfidf_matrix)
# Remove self-similarity from matrix
similarity -= np.eye(similarity.shape[0])


# Get index of movie to find similar movies
movie = 'Batman Begins'
n_plot = 10
index = movie_metadata.reset_index(drop=True)[movie_metadata.index==movie].index[0]

# Get indices and scores of similar movies
similar_movies_index = np.argsort(similarity[index])[::-1][:n_plot]
similar_movies_score = np.sort(similarity[index])[::-1][:n_plot]

# Get titles of similar movies
similar_movie_titles = movie_metadata.iloc[similar_movies_index].index


# Create trace
trace = go.Bar(x = similar_movies_score,
               text = similar_movie_titles,
               textposition = 'inside',
               textfont = dict(color = '#000000'),
               orientation = 'h',
               y = list(range(1, n_plot+1)),
               marker = dict(color = '#db0000'))
# Create layout
layout = dict(title = 'Ranking Of Top {} Most Similar Movie Descriptions For "{}"'.format(n_plot, movie),
              xaxis = dict(title = 'Cosine TFIDF Description Similarity',
                           range = (0, 0.4)),
              yaxis = dict(title = 'Movie'))
# Create plot
fig = go.Figure(data=[trace], layout=layout)
iplot(fig)


# ### <a id=11.5>11.5. Matrix Factorisation With Keras And Gradient Descent</a>
# 
# The **user-movie rating matrix is high dimensional and sparse**, therefore I am going to reduce the dimensionality to represent the data in a dense form.<br>
# **Using matrix factorisation a large matrix can be estimated/decomposed into two long but slim matrices.** With gradient descent it is possible to adjust these matrices to represent the given ratings. The **gradient descent algorithm finds latent variables which represent the underlying structure** of the dataset. Afterwards these latent variables can be used to reconstruct the original matrix and to predict the missing ratings for each user.<br>
# In this case the model has not been trained to convergence and is not hyperparameter optimized.

# In[ ]:


# Create user- & movie-id mapping
user_id_mapping = {id:i for i, id in enumerate(df_filterd['User'].unique())}
movie_id_mapping = {id:i for i, id in enumerate(df_filterd['Movie'].unique())}


# Create correctly mapped train- & testset
train_user_data = df_train['User'].map(user_id_mapping)
train_movie_data = df_train['Movie'].map(movie_id_mapping)

test_user_data = df_test['User'].map(user_id_mapping)
test_movie_data = df_test['Movie'].map(movie_id_mapping)


# Get input variable-sizes
users = len(user_id_mapping)
movies = len(movie_id_mapping)
embedding_size = 10


##### Create model
# Set input layers
user_id_input = Input(shape=[1], name='user')
movie_id_input = Input(shape=[1], name='movie')

# Create embedding layers for users and movies
user_embedding = Embedding(output_dim=embedding_size, 
                           input_dim=users,
                           input_length=1, 
                           name='user_embedding')(user_id_input)
movie_embedding = Embedding(output_dim=embedding_size, 
                            input_dim=movies,
                            input_length=1, 
                            name='item_embedding')(movie_id_input)

# Reshape the embedding layers
user_vector = Reshape([embedding_size])(user_embedding)
movie_vector = Reshape([embedding_size])(movie_embedding)

# Compute dot-product of reshaped embedding layers as prediction
y = Dot(1, normalize=False)([user_vector, movie_vector])

# Setup model
model = Model(inputs=[user_id_input, movie_id_input], outputs=y)
model.compile(loss='mse', optimizer='adam')


# Fit model
model.fit([train_user_data, train_movie_data],
          df_train['Rating'],
          batch_size=256, 
          epochs=1,
          validation_split=0.1,
          shuffle=True)

# Test model
y_pred = model.predict([test_user_data, test_movie_data])
y_true = df_test['Rating'].values

#  Compute RMSE
rmse = np.sqrt(mean_squared_error(y_pred=y_pred, y_true=y_true))
print('\n\nTesting Result With Keras Matrix-Factorization: {:.4f} RMSE'.format(rmse))


# ### <a id=11.6>11.6. Deep Learning With Keras</a>
# 
# With its embedding layers this is similar to the matrix factorization approach above, but instead of using a fixed dot-product as recommendation we will utilize some **dense layers so the network can find better combinations.**

# In[ ]:


# Setup variables
user_embedding_size = 20
movie_embedding_size = 10


##### Create model
# Set input layers
user_id_input = Input(shape=[1], name='user')
movie_id_input = Input(shape=[1], name='movie')

# Create embedding layers for users and movies
user_embedding = Embedding(output_dim=user_embedding_size, 
                           input_dim=users,
                           input_length=1, 
                           name='user_embedding')(user_id_input)
movie_embedding = Embedding(output_dim=movie_embedding_size, 
                            input_dim=movies,
                            input_length=1, 
                            name='item_embedding')(movie_id_input)

# Reshape the embedding layers
user_vector = Reshape([user_embedding_size])(user_embedding)
movie_vector = Reshape([movie_embedding_size])(movie_embedding)

# Concatenate the reshaped embedding layers
concat = Concatenate()([user_vector, movie_vector])

# Combine with dense layers
dense = Dense(256)(concat)
y = Dense(1)(dense)

# Setup model
model = Model(inputs=[user_id_input, movie_id_input], outputs=y)
model.compile(loss='mse', optimizer='adam')


# Fit model
model.fit([train_user_data, train_movie_data],
          df_train['Rating'],
          batch_size=256, 
          epochs=1,
          validation_split=0.1,
          shuffle=True)

# Test model
y_pred = model.predict([test_user_data, test_movie_data])
y_true = df_test['Rating'].values

#  Compute RMSE
rmse = np.sqrt(mean_squared_error(y_pred=y_pred, y_true=y_true))
print('\n\nTesting Result With Keras Deep Learning: {:.4f} RMSE'.format(rmse))


# ### <a id=11.7>11.7. Deep Hybrid System With Metadata And Keras</a>
# 
# One advantage of deep learning models is, that **movie-metadata can easily be added to the model.**<br>
# I will **tf-idf transform the short description** of all movies to a sparse vector. The model will learn to reduce the dimensionality of this vector and how to **combine metadata with the embedding of the user-id and the movie-id.** In this way you can add any additional metadata to your own recommender.<br>
# These kind of hybrid systems can learn how to reduce the impact of the cold start problem.

# In[ ]:


# Create user- & movie-id mapping
user_id_mapping = {id:i for i, id in enumerate(df['User'].unique())}
movie_id_mapping = {id:i for i, id in enumerate(df['Movie'].unique())}

# Use mapping to get better ids
df['User'] = df['User'].map(user_id_mapping)
df['Movie'] = df['Movie'].map(movie_id_mapping)


##### Combine both datasets to get movies with metadata
# Preprocess metadata
tmp_metadata = movie_metadata.copy()
tmp_metadata.index = tmp_metadata.index.str.lower()

# Preprocess titles
tmp_titles = movie_titles.drop('Year', axis=1).copy()
tmp_titles = tmp_titles.reset_index().set_index('Name')
tmp_titles.index = tmp_titles.index.str.lower()

# Combine titles and metadata
df_id_descriptions = tmp_titles.join(tmp_metadata).dropna().set_index('Id')
df_id_descriptions['overview'] = df_id_descriptions['overview'].str.lower()
del tmp_metadata,tmp_titles


# Filter all ratings with metadata
df_hybrid = df.drop('Date', axis=1).set_index('Movie').join(df_id_descriptions).dropna().drop('overview', axis=1).reset_index().rename({'index':'Movie'}, axis=1)


# Split train- & testset
n = 100000
df_hybrid = df_hybrid.sample(frac=1).reset_index(drop=True)
df_hybrid_train = df_hybrid[:1500000]
df_hybrid_test = df_hybrid[-n:]


# Create tf-idf matrix for text comparison
tfidf = TfidfVectorizer(stop_words='english')
tfidf_hybrid = tfidf.fit_transform(df_id_descriptions['overview'])


# Get mapping from movie-ids to indices in tfidf-matrix
mapping = {id:i for i, id in enumerate(df_id_descriptions.index)}

train_tfidf = []
# Iterate over all movie-ids and save the tfidf-vector
for id in df_hybrid_train['Movie'].values:
    index = mapping[id]
    train_tfidf.append(tfidf_hybrid[index])
    
test_tfidf = []
# Iterate over all movie-ids and save the tfidf-vector
for id in df_hybrid_test['Movie'].values:
    index = mapping[id]
    test_tfidf.append(tfidf_hybrid[index])


# Stack the sparse matrices
train_tfidf = vstack(train_tfidf)
test_tfidf = vstack(test_tfidf)


##### Setup the network
# Network variables
user_embed = 10
movie_embed = 10


# Create two input layers
user_id_input = Input(shape=[1], name='user')
movie_id_input = Input(shape=[1], name='movie')
tfidf_input = Input(shape=[24144], name='tfidf', sparse=True)

# Create separate embeddings for users and movies
user_embedding = Embedding(output_dim=user_embed,
                           input_dim=len(user_id_mapping),
                           input_length=1,
                           name='user_embedding')(user_id_input)
movie_embedding = Embedding(output_dim=movie_embed,
                            input_dim=len(movie_id_mapping),
                            input_length=1,
                            name='movie_embedding')(movie_id_input)

# Dimensionality reduction with Dense layers
tfidf_vectors = Dense(128, activation='relu')(tfidf_input)
tfidf_vectors = Dense(32, activation='relu')(tfidf_vectors)

# Reshape both embedding layers
user_vectors = Reshape([user_embed])(user_embedding)
movie_vectors = Reshape([movie_embed])(movie_embedding)

# Concatenate all layers into one vector
both = Concatenate()([user_vectors, movie_vectors, tfidf_vectors])

# Add dense layers for combinations and scalar output
dense = Dense(512, activation='relu')(both)
dense = Dropout(0.2)(dense)
output = Dense(1)(dense)


# Create and compile model
model = Model(inputs=[user_id_input, movie_id_input, tfidf_input], outputs=output)
model.compile(loss='mse', optimizer='adam')


# Train and test the network
model.fit([df_hybrid_train['User'], df_hybrid_train['Movie'], train_tfidf],
          df_hybrid_train['Rating'],
          batch_size=1024, 
          epochs=2,
          validation_split=0.1,
          shuffle=True)

y_pred = model.predict([df_hybrid_test['User'], df_hybrid_test['Movie'], test_tfidf])
y_true = df_hybrid_test['Rating'].values

rmse = np.sqrt(mean_squared_error(y_pred=y_pred, y_true=y_true))
print('\n\nTesting Result With Keras Hybrid Deep Learning: {:.4f} RMSE'.format(rmse))


# ***
# ## <a id=12>12. Exploring Python Libraries</a>
# ### <a id=12.1>12.1. Surprise Library</a>
# 
# The [surprise library](http://surpriselib.com/) was built for **creating and analyzing recommender systems.**<br>
# It has to be mentioned that most of the built-in algorithms use some kind of the above approches.
# I am going to **compare these algorithms to each other** in this section using **3-fold crossvalidation.** Since the algorithms and the dataset have a large memoryfootprint the comparison will be executed on a **subsampled dataset which is not comparable to the above models.**

# In[ ]:


# Load dataset into surprise specific data-structure
data = sp.Dataset.load_from_df(df_filterd[['User', 'Movie', 'Rating']].sample(20000), sp.Reader())

benchmark = []
# Iterate over all algorithms
for algorithm in [sp.SVD(), sp.SVDpp(), sp.SlopeOne(), sp.NMF(), sp.NormalPredictor(), sp.KNNBaseline(), sp.KNNBasic(), sp.KNNWithMeans(), sp.KNNWithZScore(), sp.BaselineOnly(), sp.CoClustering()]:
    # Perform cross validation
    results = cross_validate(algorithm, data, measures=['RMSE', 'MAE'], cv=3, verbose=False)
    
    # Get results & append algorithm name
    tmp = pd.DataFrame.from_dict(results).mean(axis=0)
    tmp = tmp.append(pd.Series([str(algorithm).split(' ')[0].split('.')[-1]], index=['Algorithm']))
    
    # Store data
    benchmark.append(tmp)


# In[ ]:


# Store results
surprise_results = pd.DataFrame(benchmark).set_index('Algorithm').sort_values('test_rmse', ascending=False)

# Get data
data = surprise_results[['test_rmse', 'test_mae']]
grid = data.values

# Create axis labels
x_axis = [label.split('_')[1].upper() for label in data.columns.tolist()]
y_axis = data.index.tolist()

x_label = 'Function'
y_label = 'Algorithm'


# Get annotations and hovertext
hovertexts = []
annotations = []
for i, y_value in enumerate(y_axis):
    row = []
    for j, x_value in enumerate(x_axis):
        annotation = grid[i, j]
        row.append('Error: {:.3f}<br>{}: {}<br>{}: {}<br>Fit Time: {:.3f}s<br>Test Time: {:.3f}s'.format(annotation, y_label, y_value ,x_label, x_value, surprise_results.loc[y_value]['fit_time'], surprise_results.loc[y_value]['test_time']))
        annotations.append(dict(x=x_value, y=y_value, text='{:.3f}'.format(annotation), ax=0, ay=0, font=dict(color='#000000')))
    hovertexts.append(row)

# Create trace
trace = go.Heatmap(x = x_axis,
                   y = y_axis,
                   z = data.values,
                   text = hovertexts,
                   hoverinfo = 'text',
                   colorscale = 'Picnic',
                   colorbar = dict(title = 'Error'))

# Create layout
layout = go.Layout(title = 'Crossvalidated Comparison Of Surprise Algorithms',
                   xaxis = dict(title = x_label),
                   yaxis = dict(title = y_label,
                                tickangle = -40),
                   annotations = annotations)

# Create plot
fig = go.Figure(data=[trace], layout=layout)
iplot(fig)


# ### <a id=12.2>12.2. Lightfm Library</a>
# 
# The [lightfm librariy](https://github.com/lyst/lightfm) focuses on **matrix factorization with explicit and implicit feedback.** Furthermore additional information like movie-metadata can be used to form a **hybrid model between content-based and collaborative recommendation** which reduces the cold-start problem.

# In[ ]:


# Create user- & movie-id mapping
user_id_mapping = {id:i for i, id in enumerate(df_filterd['User'].unique())}
movie_id_mapping = {id:i for i, id in enumerate(df_filterd['Movie'].unique())}


# Create correctly mapped train- & testset
train_user_data = df_train['User'].map(user_id_mapping)
train_movie_data = df_train['Movie'].map(movie_id_mapping)

test_user_data = df_test['User'].map(user_id_mapping)
test_movie_data = df_test['Movie'].map(movie_id_mapping)


# Create sparse matrix from ratings
shape = (len(user_id_mapping), len(movie_id_mapping))
train_matrix = coo_matrix((df_train['Rating'].values, (train_user_data.astype(int), train_movie_data.astype(int))), shape=shape)
test_matrix = coo_matrix((df_test['Rating'].values, (test_user_data.astype(int), test_movie_data.astype(int))), shape=shape)


# Instantiate and train the model
model = LightFM(loss='warp', no_components=20)
model.fit(train_matrix, epochs=20, num_threads=2)


# Evaluate the trained model
k = 20
print('Train precision at k={}:\t{:.4f}'.format(k, precision_at_k(model, train_matrix, k=k).mean()))
print('Test precision at k={}:\t\t{:.4f}'.format(k, precision_at_k(model, test_matrix, k=k).mean()))


# ***
# ## <a id=13>13. Conclusion</a>
# 
# There are many different ways to set up a recommender system and just like other machine learning algorithms it is very important to know which objective has to be optimized and therefore which layout should be choosen.<br>
# 
# **Here you can find more in-depth content: [Pinterest](https://www.pinterest.de/dataliftoff/recommender-systems/)**
# 
# ***
# 
# Other **python recommender libraries** are:
# + [implicit](https://github.com/benfred/implicit)
# + [spotlight](https://github.com/maciejkula/spotlight)
# + [turicreate](https://github.com/apple/turicreate/blob/master/README.md)
# + [mrec](https://github.com/Mendeley/mrec)
# + [recsys](https://github.com/ocelma/python-recsys)
# + [crab](http://muricoca.github.io/crab/)
# 
# ***
# ***
