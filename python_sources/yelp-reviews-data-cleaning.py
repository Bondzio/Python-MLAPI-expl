#!/usr/bin/env python
# coding: utf-8

# ## Data

# In[7]:


get_ipython().system('ls -al ../input')


# ## Imports

# In[8]:


# basics
import numpy as np
import pandas as pd


# In[9]:


businesses = pd.read_csv("../input/yelp_business.csv")
reviews = pd.read_csv("../input/yelp_review.csv")


# ### Restaurants

# In[10]:


# keep only restaurants
restaurants = businesses[businesses['categories'].str.contains("Restaurants")]
# keep only the relevant columns
restaurants.drop(['neighborhood', 'address', 'city', 'state', 'latitude', 'longitude'], axis=1, inplace=True)


# In[11]:


restaurants.head(10)
print("Total number of businesses: {}".format(businesses.shape))
print("Number of restaurants: {} ({} %)".format(restaurants.shape, (restaurants.shape[0]/businesses.shape[0]*100)))


# ### Reviews

# In[12]:


# set index
# restaurants.set_index('business_id')
# reviews.set_index('business_id')


# In[13]:


# Keep only the restaurant reviews
print("Total number of reviews: {}".format(reviews.shape))
restaurant_reviews = reviews[reviews['business_id'].isin(restaurants['business_id'])]
print("Number of restaurant reviews: {} ({} %)".format(restaurant_reviews.shape, (restaurant_reviews.shape[0]/reviews.shape[0]*100)))


# In[21]:


# Save restaurants.csv
restaurants.to_csv('restaurants.csv', encoding='utf-8')
# Save restaurants_reviews.csv
restaurant_reviews.to_csv('restaurant_reviews.csv', encoding='utf-8')

