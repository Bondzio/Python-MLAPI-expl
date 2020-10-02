#!/usr/bin/env python
# coding: utf-8

# # Notes on matrix factorization machines
# 
# ## Matrix factorization
# 
# We may construct an array representing the coincidence of one set of features with another set of features, with the values within the array representing the strength of intersection of those two features. In the classic example of this phenomenon, the Netflix movie recommendation problem, the features are users and movies they could watch.
# 
# In practice the resulting array is highly sparse: no users have seen much of the Netflix catalog, and many have in fact seen very little of it.
# 
# Matrix factorization is the problem in linear algebra of finding a set of two arrays which, when multiplied against one another, create some other array. If we consider our end product, the users-movies matrix, as the "target" matrix, an interesting problem is that of finding a set of two matrices, one based on users and one based on movies, that, when multiplied against one another, approximates the users-to-movies matrix result:
# 
# ![](https://i.imgur.com/weE1qz6.png)
# 
# This sparse matrix factorization problem is a well-known one in the literature, and there are relatively efficient stochastic algorithms that have been developed to solve it approximately. And solving this problem has the nice "side effect" of also generating predictions for every other element in the (sparse) matrix! Matrix factorization may be used as a machine learning algorithm in this way. It is a pretty effective technique for highly sparse datasets; hence its application to the movie recommendation engine problem.
# 
# I wrote a kernel implementing matrix factorization for a recommendation engine. That lives [here](https://www.kaggle.com/residentmario/recommending-chess-openings), and was itself inspired by [this excellent kernel](https://www.kaggle.com/philippsp/book-recommender-collaborative-filtering-shiny) demonstrating the same approach to a slightly different problem (book recommendation) in R.
# 
# ## Factorization machine
# 
# A factorization machine is a generalization of the matrix factorization technique. It takes a degree $n$ as a hyperparameter, and allows us to train on feature interactions amongst the chosen $n$ number of features. In other words, if our movie matrix includes both "Goodfellas" and "Die Hard", the degree-2 factorization machine would train on a "Goodfellas + Die Hard" feature. Movies that co-occur often in the matrix are given a higher weight, and movies that co-occur rarely are given a lower weight. For example, a "Goodfellas"-"Pride and Prejudice" feature would matter little, but a "Goodfellas"-"Die Hard" feature might matter quite a lot. The level of weight is determined very simply: by calculating the dot product between the two movies (and then optionally normalizing the weights).
# 
# Suppose we have these three movies (let's call them A, B, and C, respectively). Suppose we also have just three users (u1, u2, u3). Let $X$ be feature matrix (of users against movie recommendations), and let $v_{A, u}$ be a specific value in that matrix $X$. In this case the prediction generated by a factorization machine would be:
# 
# $$P = w_0 + w_A x_A + w_B x_B + w_C x_C + \sum_{j \in \{A, B, C\}} \langle v_{j1}, v_{j2} \rangle x_{j1} x_{j2}$$
# 
# The first term in this expression is the intercept. The next three terms are the weights assigned by the algorithm to each of the movies. The interesting part is the last term, the sum. Every element in the sum is dot product of the two movies being considered as the weight, multiplied against the recommendation value for these two movies that has been set by the user.
# 
# For example, for movie A this would expand out to:
# 
# $$\langle v_{A}, v_{B} \rangle = v_{A, u1} * v_{B, u1} + v_{A, u2} * v_{B, u2} + v_{A, u3} * v_{B, u3}$$
# 
# Factorization machines treat problems like this one by considering not just lone variables but also variable interactions. They can take up to as many possible interactions as necessary for the problem at hand. Because they use matrix factorization factorization machines are a good fit for sparse data; and because they treat combinations of variables, they are a good fit for modeling in scenarios where feature interactions are important.
# 
# ## Field-aware factorization machine
# 
# Field-aware factorizations machines are the implementation of factorization machines used in practice.
# 
# Factorization machines assign weights to and train on each possible variable value in the dataset: so $w_{A}$ etcetera. However, their purview is limited to just the one recommendation predictor variable being used. Other variables in the dataset are ignored, which prevents us from adding any further information or features to our prediction systems.
# 
# Field-aware factorization machines adress this problem.  Suppose we add gender into the dataset. If that additional variable provides useful information towards prediction, finding just $w_{A}$ would fall short. Instead, we would want to define and find $w_{A, \text{Male}}$ and $w_{A, \text{Female}}$; and that is what field-aware factorization machines do.
# 
# Doing this is methodologically simple (but requires good juggling skills in the code). Instead of calculating a weight for all of $A$, partition the dataset into male and female sections, and perform the cosine distance calculation for each portion of the data separately. Use that to train and assign a weight on the relevant portion of the data.

# In[30]:


# import pandas as pd
# pd.set_option('max_columns', None)
# ratings = pd.read_csv("../input/goodbooks-10k/ratings.csv")
# books = pd.read_csv("../input/goodbooks-10k/books.csv")


# In[31]:


# len(ratings), len(books)


# In[32]:


# import matplotlib.pyplot as plt
# plt.style.use('fivethirtyeight')

# ratings['user_id'].value_counts().plot.hist(bins=50, title='N(Recommendations) per User', figsize=(12, 6))


# In[33]:


# (books
#      .drop(['id', 'best_book_id', 'work_id', 'authors', 'original_title', 'title', 'language_code', 'image_url', 'small_image_url', 'isbn', 'isbn13'], axis='columns')
#      .drop(['work_ratings_count', 'work_text_reviews_count'], axis='columns')
#      .set_index('book_id')
#      .head()
# )


# # Conclusion
# 
# The recommended library for implementing FFMs at the time of writing is [xLearn](http://xlearn-doc.readthedocs.io/en/latest/python_api.html). However, this cannot be custom-installed on Kaggle, as of the time of writing, so implementation of an FFM will have to wait for another time. 
# 
# FFMs were used to solve clickthrough prediction problem competitions:
# * https://www.kaggle.com/c/criteo-display-ad-challenge
# * https://www.kaggle.com/c/avazu-ctr-prediction
# * https://www.kaggle.com/c/outbrain-click-prediction
# 
# The best reference for this material is: https://www.analyticsvidhya.com/blog/2018/01/factorization-machines/
