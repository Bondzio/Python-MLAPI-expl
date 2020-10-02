#!/usr/bin/env python
# coding: utf-8

# This analytical study attempts to answer the question: "By what criteria besides intuition can you be guided to make the film successful as a business project, that is, to get the most out of the invested capital?"
# 
# So, the development of investor's intuition may include such questions:
# Prediction of popularity - can you say which film will be successful theoretically if you collect it as the developer of the best successful variables? To understand the image of victory and focus on young and undervalued actors and directors who copy the famous?
# As a beginner, I will be grateful for the criticism and comments on how to improve the analytics).
# 
# To be continued...

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # To plot
get_ipython().run_line_magic('matplotlib', 'inline')
import os
from wordcloud import WordCloud
import seaborn as sns # may be usefull

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


# We import the database file and check the first 5 rows: data
data = pd.read_csv('../input/movie_metadata.csv')
# Let's see the information about our table
data.info()


# In[ ]:


# I check the dependent between 'budget' and 'movie_facebook_likes' in slice every film: movie_fb_likes
movie_fb_likes = data.groupby('movie_title')['budget', 'movie_facebook_likes'].agg('sum')
movie_fb_likes.head()


# In[ ]:


# Vizulisation to explore dependent
plt.scatter(movie_fb_likes['budget'], movie_fb_likes['movie_facebook_likes'], marker='.')
plt.xlabel('Budget per film [dollars]')
plt.ylabel('Number of FB Likes')
plt.show()
"""The tendency to a strong relationship between the budget and the likes of facebook is not observed in the context of each film"""


# In[ ]:


# What the movies came in Top-20?
top20_movie_fb_likes = movie_fb_likes.sort_values(by='movie_facebook_likes', ascending=False).head(20)
top20_movie_fb_likes


# In[ ]:


top20_movie_fb_likes.describe()


# In[ ]:


# I check the dependent between 'budget' and 'movie_facebook_likes' in slice director: director_fb_like_films
director_fb_like_films = data.groupby('director_name')['budget', 'movie_facebook_likes'].agg('mean')


# In[ ]:


# Plot dependent between the average budget and the average number of likes of facebook
plt.scatter(director_fb_like_films['budget'], director_fb_like_films['movie_facebook_likes'], marker='.')
plt.xlabel('Average budget per film [dollars]')
plt.ylabel('Number of FB Likes')
plt.show()
"""In the context of every director the tendency to a strong dependent between the average budget and the average number of likes of facebook is not observed."""


# In[ ]:


top20_director_fb_like_films = director_fb_like_films.sort_values(by='movie_facebook_likes', ascending=False).head(20)
top20_director_fb_like_films

#  Maybe the such directors styles have success to users facebook 


# In[ ]:


top20_director_fb_like_films.describe()


# In[ ]:


# Let's see which genres have much money:genres_money
genres_money = data.groupby('genres')['gross', 'budget'].sum()
genres_money = genres_money.sort_values(['gross'], ascending=False)
genres_money.describe()


# In[ ]:


# For what genres the market most votes by dollars?
top20_genres_money_gross = genres_money['gross'].sort_values(ascending=False).head(20)
top20_genres_money_gross


# In[ ]:


type(top20_genres_money_gross)


# In[ ]:


top20_genres_money_gross_name = dict(top20_genres_money_gross)
top20_genres_money_gross_name.keys()


# In[ ]:


list_top20_genres = [key for key in top20_genres_money_gross_name.keys()]
list_top20_genres = [genre.split("|") for genre in list_top20_genres]
str(list_top20_genres)


# In[ ]:


# Creating a word cloud of the top genres
tagsString = str(list_top20_genres)
top20_genres_name = WordCloud(background_color='white', width=500, height=200).generate(tagsString)
plt.rcParams["figure.figsize"] = [7,7]
plt.imshow(top20_genres_name)
plt.axis('off')
plt.show()

"""People most pay for Action, Adventure, Comedy, Drama, Thriller and Crime. Make money on people's emotions! ))"""


# In[ ]:


# Add a profitability column to the common table 'data': 'profitability'
data['profitability'] = np.round(100 - 100 * data['gross'] / data['budget'])
data.head()


# In[ ]:


profit_grand = data.sort_values(by='profitability', ascending=False)[:1000]
profit_grand = profit_grand.groupby(['genres', 'director_name'])['profitability', 'budget'].mean()
profit_grand.head()


# In[ ]:


profit_grand = profit_grand.sort_values(by='budget')
profit_grand.head()


# In[ ]:


plt.scatter(profit_grand['budget'], profit_grand['profitability'], marker='.')
plt.xlabel('Average budget by director in genre [dollars]')
plt.ylabel('Profitability mean')
plt.show()


# In[ ]:


profit_grand.describe()


# In[ ]:


type(profit_grand)


# In[ ]:


action_crime_thriller = profit_grand.loc[['Action|Crime|Thriller']]
action_crime_thriller


# In[ ]:


plt.scatter(action_crime_thriller['budget'], action_crime_thriller['profitability'], marker='o', color='red')
plt.xlabel('Average budget by director in genre [dollars]')
plt.ylabel('Profitability mean')
plt.title('action_crime_thriller')
plt.show()

