#!/usr/bin/env python
# coding: utf-8

# 

# # MovieLens Dataset analysis
# 

# 
#     I am a newbie to the field of data science , and will be attempting to work my way through the MovieLens dataset. Please consider upvoting if this is useful to you! :)
# 
#     Any feedback is welcome !
#     
#     About Dataset 
#     
#     This dataset (ml-20m) describes 5-star rating and free-text tagging activity from [MovieLens](http://movielens.org), a movie recommendation service. It contains 20000263 ratings and 465564 tag applications across 27278 movies. These data were created by 138493 users between January 09, 1995 and March 31, 2015. This dataset was generated on March 31, 2015, and updated on October 17, 2016 
#      
#      for further information read Readme.txt file attached to this dataset
#      
#     Contents
# 
#         1.Importing Libaries
#         2.Reading and Exploring the data
#         3.Data Analysis
#         4.Cleaning of data
#         5.Data Visualization

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

print('Import Complete')
# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


# lets explore movies.csv
movies_data= pd.read_csv('../input/movielens/movies.csv')
movies_data.head()


# In[ ]:


movies_data.shape


# 
# Here are 27278 movies released between January 09, 1995 and March 31, 2015 and have different genres like
# * Action,Adventure, Animation, Children's, Comedy, Crime, Documentary, Drama, Fantasy, Film-Noir, Horror, Musical, Mystery, Romance, Sci-Fi, Thriller, War, Western
# 
# 

# In[ ]:


movies_data.info()


# There are no null values in the dataset,no need to any cleaning process

# In[ ]:


movies_data.describe()


# In[ ]:


#to count unique movies from the table by using movie id , because movie id is unique
movies = movies_data['movieId'].unique().tolist()
len(movies)


# In[ ]:


#now explore details about ratings_data.csv  
ratings_data = pd.read_csv('../input/movielens/ratings.csv')
ratings_data.head()


# In[ ]:


ratings_data.shape


# In[ ]:


ratings_data.info()


# In[ ]:


ratings_data.describe()


# From this table in ratings column Maximum and Minimum Ratings of the movies are 5 and 0.5 respectively 
# 

# # Problem statement and Analysis from the Data
# 

# Before doing Analysis we have to clear out our problem statement of how we analyse the Data  
# 
# 1. Top 20 most Watched movies 
# 2. Top 20 High rated movies(Equal to 4 and above)
# 3. Top 20 Low rated movies(Equalto 1 and below)
# 4. Top 20 Users who watch More movies 
# 5. Which genre is highly occured in high rated movies list

# # Top 20 Most watched movies

# In[ ]:


# we have to combine both movies data and ratings data, so we have to delete unwanted from the data
del ratings_data['timestamp']
ratings_data


# In[ ]:


#Lets combine Movies data and ratings data
combined_data = movies_data.merge(ratings_data,on = 'movieId',how = 'inner')
combined_data.head(2)


# In[ ]:


# here no columns to about watched or not 
# so we we take most ranked movies as a most watched movies because no one rank before watching 
most_watched = combined_data.groupby('title').size().sort_values(ascending=False)
most_watched.head(10)


# In[ ]:


# Top 20 Most high rated movies

high_rated_movies = combined_data[combined_data['rating']>3.9]
high_rated_movies.head(5)

#this shows the movies rated more than 3.9 but not mostly high rated 


# In[ ]:



#top 20 most rated movies
top_high_rated = high_rated_movies.groupby('title').size().sort_values(ascending=False)
top_high_rated.head(20)


# # Top 20 Mostly low rated movies

# In[ ]:


#movies rated below 1.5
low_rated = combined_data[combined_data['rating']<1.5]
low_rated.head(5)


# In[ ]:


#top low rated movies 
top_low_rated = low_rated.groupby('title').size().sort_values(ascending=False)
top_low_rated.head(20)


# ## Top users who watched more movies

# In[ ]:


# groupby users and count the watch time and sort it out
top_usersId = combined_data.groupby('userId').size().sort_values(ascending=False)
top_usersId.head(10)


# ## most genres

# In[ ]:



#here we  make count of the genres: 
#first convert a series to list

genre_types = set()
for s in movies_data['genres'].str.split('|').values:
    genre_types = genre_types.union(set(s))


# In[ ]:


#define a function that counts the number of times each genre appear:
def word_count(df, ref_col, liste):
    keyword_count = dict()
    for s in liste: keyword_count[s] = 0
    for liste_keywords in df[ref_col].str.split('|'):
        if type(liste_keywords) == float and pd.isnull(liste_keywords): continue
        for s in liste_keywords: 
            if pd.notnull(s): keyword_count[s] += 1
    # convert the dictionary in a list to sort the keywords  by frequency
    keyword_occurences = []
    for k,v in keyword_count.items():
        keyword_occurences.append([k,v])
    keyword_occurences.sort(key = lambda x:x[1], reverse = True)
    return keyword_occurences, keyword_count


# In[ ]:


#counting how many times each of genres occur:
keyword_occurences, num = word_count(movies_data, 'genres', genre_types)
keyword_occurences


# ## Data Visualization

# In[ ]:


fig = plt.figure(1, figsize=(16,10))
ax2 = fig.add_subplot(2,1,2)
y_axis = [i[1] for i in keyword_occurences]
x_axis = [k for k,i in enumerate(keyword_occurences)]
x_label = [i[0] for i in keyword_occurences]
plt.xticks(rotation=85, fontsize = 15)
plt.yticks(fontsize = 15)
plt.xticks(x_axis, x_label)
plt.ylabel("No. of occurences", fontsize = 24, labelpad = 0)
ax2.bar(x_axis, y_axis, align = 'center', color='b')
plt.title("Popularity of Genres",bbox={'facecolor':'k', 'pad':5},color='w',fontsize = 30)
plt.show()

