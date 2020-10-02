#!/usr/bin/env python
# coding: utf-8

# # Building a Recommender System with Podcasts
# 
# I listen to a lot of podcasts. If you're looking for some to start listedning too, my favorites are The MFCEO Project, The School of Greatness with Lewis Howes, and UMD Newman Catholic Campus Ministry.
# 
# I mainly use Apple's Podcast app to find and listen to podcasts (although I just started using Spotify - it functions *much* better), but I had no way of finding new podcasts aside from browsing the 'featured' page. When I build the courage to drudge through the "new and noteworthy' section, I  get exhausted looking through all the podcasts that simply don't interest me. There isn't a great way for me to find new podcasts that I like.
# 
# Enter: Recommender Systems.
# 
# Recommender systems take the things that you like, and find other similar things. All your favorite apps and businesses use one - Spotify, Netflix, Amazon. You'd be hard pressed to find any content consumption platform that serve you recommendation in some shape or form (unless that platform is Apple Podcasts). PS: if you're an analyst and want to provide *immense* value to your company, build a recommender system if they don't already have one. It's a simple project, and can catapult your analytics compitencies forward.
# 
# In this kernel, I'm going to use iTunes podcast data to build a recommender system, and see if I can't find some new podcasts that I'd like. A quick thank you to Chris Clark, whose tutorial I used to build this recommender system. Go check out his blog for a lot of useful posts!
# 
# First, let's import some packages. We're going to import a few of the usuals: NumPy, Pandas, and OS to read , manipulate the data. We're also going to import some not-so-usual packages, both from the sklearn module: TfidfVectorizer and linear_kernel. I'll explain what each do a little bit later when I'm ready to use them.

# In[ ]:


import numpy as np
import pandas as pd 
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
print(os.listdir("../input"))

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# This data provided by ListenNotes has both podcast and episode metadata. I'm only going to be working with the podcast metadata in this example, although you could theoretically build a recommender system for individual episodes.

# In[ ]:


podcasts = pd.read_csv('../input/podcasts.csv')
podcasts.head()
podcasts.info()


# This dataset has over 120,000 podcasts! I'm not going to be able to use all that data so I'm going to take a sample. But first we need to clean this up a bit. 
# 
# "Language" is a column, so I expect there might be some podcasts that aren't in English, which could throw a wrench in the recommendations.

# In[ ]:


(podcasts
 .language
 .value_counts()
 .to_frame()
 .head(10))


# It looks like there are podcasts in many different langauges in this data. I'm only going to include those that are recorded in English.

# In[ ]:


podcasts = podcasts[podcasts.language == 'English']


# When I loaded the data, I also noticed that there were some records that didn't have a description. These aren't going to be very useful, so I'm going to drop those records.
# 
# Just to be sure we're working with cleaned data, I'm also going to drop any records that might be duplicates.

# In[ ]:


podcasts = podcasts.dropna(subset=['description'])
podcasts = podcasts.drop_duplicates('itunes_id')
sum(podcasts.description.isnull())


# Since we're building a recommender system based on podcast descriptions, we want to make sure that the descriptions have enough sontent in them to serve as useful inputs. Below I'm going to find the length of each podcast description and describe it.

# In[ ]:


podcasts['description_length'] = [len(x.description.split()) for _, x in podcasts.iterrows()]
podcasts['description_length'].describe()


# At lease a quarter of our descriptions have less than 11 words. I'm certain these won't serve as good inputs when we build the recommender system. Just to be safe, I'm only going to include descriptions that have at least 20 words in them.

# In[ ]:


podcasts = podcasts[podcasts.description_length >= 20]


# Like I mentioned earlier, I'm not going to use the entire dataset - I just don't have enough computaitonal power. Instead, I'm going to sample 15,000 records from this data set and build the recommender system on that sample.
# 
# At the end of this, I want to be able to find podcasts similar to the ones that I mentioned above, so I'm going to pull those into a seperate dataframe, and load them back in after I've created my sample.

# In[ ]:


favorite_podcasts = ['The MFCEO Project', 'Up and Vanished', 'Lore']
favorites = podcasts[podcasts.title.isin(favorite_podcasts)]
favorites


# In[ ]:


podcasts = podcasts[~podcasts.isin(favorites)].sample(15000)
data = pd.concat([podcasts, favorites], sort = True).reset_index(drop = True)


# Here comes the fun! Now that I have my dataset prepared, I can start to build the recommender system.
# 
# I'm going to use TfidVecortizer to find the **term frequency inverse document frequency** (tf-idf or TFIDF). This measure is meant to score how *important* a word in it's document. TFIDF uses two measures to find the most important words: **term frequency** and **inverse-document frequency**.
# 
# Let's assume the example below is one ad out of 100 ads found in a magazine.
# 
# Cleaning the gutters in your home is crutial in keeping the exterior of your hom ein wonderful condition. Out pattented gutter guard blocked debries from clogging your gutter, and saves your the trouble of cleaning them yourself.
# 
# In the example above, the word 'your' appears four times. This is the raw term frequency which is used in scikit-learn's TfidfVectorizer function. There area a few other ways to calcualte term frequency that involves normalization - you can read more about those here.
# 
# 'Your' is a pretty common word, so let's assume it's in 90 out of the 100 ads. The formula for inverse-document frequncy is:
# 
# log(Number of total documents / Number of documents containing the term) + 1
# 
# In this case, the inverse-document frequency would be log(100/90), or 1.04. This is a relatively low score, and shows us that 'your' doesn't reflect what the ad above is talking about. If we used a word like "gutter", we could expect a different result.
# 
# TfidfVectorizer allows you to remove stopwords, include bigrams, and filter out words based on how frequently they appear. You can read more about all the parameters here..
# 
# In this example, I'm removing English stop words, and looking at bigrams and trigrams (collections of terms in groups of two and three).

# In[ ]:


tf = TfidfVectorizer(analyzer = 'word', ngram_range = (1, 3), min_df = 0, stop_words = "english")
tf_idf = tf.fit_transform(data['description'])
tf_idf


# What's returned is a sparse matrix that contains the tf-idf values of each word, bigram, and trigram in the podcast descriptions. 
# 
# Next, we're going to use the linear_kernal function to calculate the similarity between the podcasts. If two podcasts have tfidf scores that are close to each other, this value is going to be close to 1. If they don't share any similar scores, the score will be closer to 0. This is the score we're going to use to find similar podcasts.

# In[ ]:


similarity = linear_kernel(tf_idf, tf_idf)
similarity


# We can now use this similarity dataframe to find similar podcasts. While we could return scores for every podcast, I'm only going examine the 3 most similar podcasts.
# 
# Let's take a look at podcasts similar to "Up and Vanished".

# In[ ]:


x = data[data.title == 'Up and Vanished'].index[0]
similar_idx = similarity[x].argsort(axis = 0)[-4:-1]
for i in similar_idx:
    print(similarity[x][i], '-', data.title[i], '-', data.description[i], '\n')
print('Original - ' + data.description[x])


# These look like some good recommendations, but there's something interesting about the most similar podcast "VANISHED: The Tara Calico Investication" an our original  podcast "Up and Vanished". They're both investigating the disappearnce of a woman names Tara.
# 
# This highlights where content recommendation systems fails. When there are unique words that don't help in describing the topic of the content (names, uncommon adjectives, company name, etc.), the recommendations get skewed. Look at the recommendations for another one of my favorites: Lore.

# In[ ]:


x = data[data.title == 'Lore'].index[0]
similar_idx = similarity[x].argsort(axis = 0)[-4:-1]
for i in similar_idx:
    print(similarity[x][i], '-', data.title[i], '-', data.description[i], '\n')
print('Original - ' + data.description[x])


# Here, we don't get three horror podcasts, rather we get podcasts that contain the word "bi-weekly". 
# 
# Content based recommendations are great for building a quick data product, but fall short in offering good recommendations, especially when the content is limited. This method would work much better if we were recommending articles, or books. If you were to use collabortive filtering to build a recommender system with this dataset, it should be paired with a collaborative recommender system to make it more effective.
# 
# Thanks for reading through my kernel! I have a few other ideas on what to do with these podcast descriptions, so stay tuned for more!+
