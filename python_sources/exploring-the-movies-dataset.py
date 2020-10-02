#!/usr/bin/env python
# coding: utf-8

# ## Import Libraries
# 
# Import the necessary Python libraries

# In[89]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import ast


# In[90]:


get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('whitegrid')


# ## Load Data
# 
# Load movies csv file and perform two tasks while loading:
# 
# Convert date field to datetime.date type
# Convert all column with json data as json type

# In[91]:


def load_movies_metadata(file_path):
    df = pd.read_csv(file_path, dtype='unicode')
    # covert each item of release_date to datetime.date type entity
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce').apply(lambda x: x.date())
    # all json columns`
    json_columns = ['belongs_to_collection', 'genres', 'production_companies', 'production_countries', 'spoken_languages']
    for column in json_columns:
        # use ast because json data has single quotes in the csv, which is invalid for a json object; it should be " normally
        df[column] = df[column].apply(lambda x: np.nan if pd.isnull(x) else ast.literal_eval(x))
    return df


# Load the movies metadata csv file

# In[92]:


movies = load_movies_metadata(r"../input/movies_metadata.csv")


# In[93]:


movies.head(3)


# Let's see how many observations are null for each column.

# In[94]:


movies.isnull().sum()


# Below code does some more exploratory data analysis

# In[95]:


movies.shape


# In[96]:


movies.columns


# In[97]:


movies.info()


# ## Data Visualization
# 
# Let's plot the most profitable movie genre using 'revenue' and 'genre' information.

# In[98]:


genre_revenue = {}

for i in range(movies.shape[0]):
    for item in movies['genres'][i]:
        if 'name' in item and movies.iloc[i]['revenue'] is not np.nan:
            a = item['name']
            b = int(movies.iloc[i]['revenue'])/1000000
            if a in genre_revenue:
                genre_revenue[a]['total_revenue'] += b 
            else:
                genre_revenue[a] = {}
                genre_revenue[a]['genre'] = a
                genre_revenue[a]['total_revenue'] = b

most_profitable_genre = pd.DataFrame(None,None,columns=['genre','revenue'])

for k,v in genre_revenue.items():
    most_profitable_genre =  most_profitable_genre.append({'genre':v['genre'],'revenue':v['total_revenue']},ignore_index=True)


# In[99]:


most_profitable_genre = most_profitable_genre.sort_values(by='revenue',ascending=False)


# In[100]:


most_profitable_genre.head()


# In[101]:


plt.figure(figsize=(17,7))
ax = sns.barplot(x=most_profitable_genre['genre'],y=most_profitable_genre['revenue'])
x=ax.set_xlabel("Movie Genre")
b=ax.set_ylabel("Revenue (in Million Dollars)")
c=ax.set_xticklabels(labels=ax.get_xticklabels(),rotation=30)
d=ax.set_title("Most Profitable Movies by Genre")


# We can also plot the most popular genre in termn of popularity points.

# Below row had to be dropped because it contains invalid values.

# In[102]:


movies.drop(movies.index[35587],inplace=True)


# In[103]:


genre_popularity = {}

for i,_ in movies.iterrows():
    for item in movies['genres'][i]:
        if 'name' in item and movies.iloc[i]['popularity'] is not np.nan:
            a = item['name']
            b = float(movies.iloc[i]['popularity'])
            if a in genre_popularity:
                genre_popularity[a]['total_popularity_points'] += b 
                genre_popularity[a]['total_popularity_counts'] += 1
            else:
                genre_popularity[a] = {}
                genre_popularity[a]['genre'] = a
                genre_popularity[a]['total_popularity_points'] = b
                genre_popularity[a]['total_popularity_counts'] = 0

most_popular_genre = pd.DataFrame(None,None,columns=['genre','average_popularity_points'])

for k,v in genre_popularity.items():
    most_popular_genre =  most_popular_genre.append({'genre':v['genre'],'average_popularity_points':v['total_popularity_points']/v['total_popularity_counts']},ignore_index=True)


# In[104]:


most_popular_genre = most_popular_genre.sort_values(by='average_popularity_points',ascending=False)


# In[105]:


plt.figure(figsize=(17,7))
ax = sns.barplot(x=most_popular_genre['genre'],y=most_popular_genre['average_popularity_points'])
x=ax.set_xlabel("Movie Genre")
b=ax.set_ylabel("Average Popularity Points")
c=ax.set_xticklabels(labels=ax.get_xticklabels(),rotation=30)
d=ax.set_title("Most Popular Movies by Genre")


# Next, let's plot the genres by longest runtime.

# In[106]:


genre_length = {}

for i,_ in movies.iterrows():
    for item in movies['genres'][i]:
        if 'name' in item and movies.iloc[i]['runtime'] is not np.nan:
            a = item['name']
            b = float(movies.iloc[i]['runtime'])
            if a in genre_length:
                genre_length[a]['total_runtime_time'] += b 
                genre_length[a]['total_runtime_count'] += 1
            else:
                genre_length[a] = {}
                genre_length[a]['genre'] = a
                genre_length[a]['total_runtime_time'] = b
                genre_length[a]['total_runtime_count'] = 0

longest_runtime_genre = pd.DataFrame(None,None,columns=['genre','average_runtime'])

for k,v in genre_length.items():
    longest_runtime_genre =  longest_runtime_genre.append({'genre':v['genre'],'average_runtime':v['total_runtime_time']/v['total_runtime_count']},ignore_index=True)


# In[107]:


longest_runtime_genre = longest_runtime_genre.sort_values(by='average_runtime',ascending=False)


# In[108]:


longest_runtime_genre.head()


# In[109]:


plt.figure(figsize=(17,7))
ax = sns.barplot(x=longest_runtime_genre['genre'],y=longest_runtime_genre['average_runtime'])
x=ax.set_xlabel("Movie Genre")
b=ax.set_ylabel("Average Runtime (in minutes)")
c=ax.set_xticklabels(labels=ax.get_xticklabels(),rotation=30)
d=ax.set_title("Longest Runtime of Movies by Genre")


# We can also see maximum vote count for each movie genre.

# In[110]:


genre_vote_count = {}

for i,_ in movies.iterrows():
    for item in movies['genres'][i]:
        if 'name' in item and movies.iloc[i]['vote_count'] is not np.nan:
            a = item['name']
            b = int(movies.iloc[i]['vote_count'])/1000000
            if a in genre_vote_count:
                genre_vote_count[a]['total_votes'] += b 
            else:
                genre_vote_count[a] = {}
                genre_vote_count[a]['genre'] = a
                genre_vote_count[a]['total_votes'] = b

most_votes_genre = pd.DataFrame(None,None,columns=['genre','total_votes'])

for k,v in genre_vote_count.items():
    most_votes_genre =  most_votes_genre.append({'genre':v['genre'],'total_votes':v['total_votes']},ignore_index=True)


# In[111]:


most_votes_genre = most_votes_genre.sort_values(by='total_votes',ascending=False)


# In[112]:


most_votes_genre.head()


# In[113]:


plt.figure(figsize=(17,7))
ax = sns.barplot(x=most_votes_genre['genre'],y=most_votes_genre['total_votes'])
x=ax.set_xlabel("Movie Genre")
b=ax.set_ylabel("Total number of votes (in Millions)")
c=ax.set_xticklabels(labels=ax.get_xticklabels(),rotation=30)
d=ax.set_title("Total Votes by Genre")


# And we can also see average votes for each movie genre.

# In[114]:


genre_average_votes = {}

for i,_ in movies.iterrows():
    for item in movies['genres'][i]:
        if 'name' in item and movies.iloc[i]['vote_average'] is not np.nan:
            a = item['name']
            b = float(movies.iloc[i]['vote_average'])
            if a in genre_average_votes:
                genre_average_votes[a]['total_votes_points'] += b 
                genre_average_votes[a]['total_votes_counts'] += 1
            else:
                genre_average_votes[a] = {}
                genre_average_votes[a]['genre'] = a
                genre_average_votes[a]['total_votes_points'] = b 
                genre_average_votes[a]['total_votes_counts'] = 1

highest_voted_genre = pd.DataFrame(None,None,columns=['genre','average_votes'])

for k,v in genre_average_votes.items():
    highest_voted_genre =  highest_voted_genre.append({'genre':v['genre'],'average_votes':v['total_votes_points']/v['total_votes_counts']},ignore_index=True)


# In[115]:


highest_voted_genre = highest_voted_genre.sort_values(by='average_votes',ascending=False)


# In[116]:


highest_voted_genre.head()


# In[117]:


plt.figure(figsize=(17,7))
ax = sns.barplot(x=highest_voted_genre['genre'],y=highest_voted_genre['average_votes'])
x=ax.set_xlabel("Movie Genre")
b=ax.set_ylabel("Votes Average")
c=ax.set_xticklabels(labels=ax.get_xticklabels(),rotation=30)
d=ax.set_title("Highest Voted Genre")


# Below code prints unique list of languages in the dataset

# In[118]:


langs = []

for i,row in movies.iterrows():
    if row['spoken_languages'] is not np.nan:
        a = row['spoken_languages']
        for item in a:
            if item['name'] not in langs:
                langs.append(item['name'])

print(langs)


# Below rows had to be delted because of the incorrect data placement in these rows

# In[119]:


movies.drop(movies.index[19730],inplace=True)
movies.drop(movies.index[29502],inplace=True)
movies.drop(movies.index[35585],inplace=True)


# Below code prints unique list of countries in the dataset

# In[120]:


countries = []

for i,row in movies.iterrows():
    if row['production_countries'] is not np.nan:
        a = row['production_countries']
        for item in a:
            if item['name'] not in countries:
                countries.append(item['name'])

print(countries)


# Below code prints unique list of genres in the dataset

# In[121]:


genres = []

for i,row in movies.iterrows():
    if row['genres'] is not np.nan:
        a = row['genres']
        for item in a:
            if item['name'] not in genres:
                genres.append(item['name'])

print(genres)


# In the next notebook, we do some tranformations to deserialize json in order to process them later
