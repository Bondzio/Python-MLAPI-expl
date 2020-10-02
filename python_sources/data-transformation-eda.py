#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go


# ### Data Insights

# In[ ]:


movies_data = pd.read_csv('../input/movietweetings/movies.dat', delimiter='::', engine='python', header=None, names = ['Movie ID', 'Movie Title', 'Genre'])
users_data = pd.read_csv('../input/movietweetings/users.dat', delimiter='::', engine='python', header=None, names = ['User ID', 'Twitter ID'])
ratings_data = pd.read_csv('../input/movietweetings/ratings.dat', delimiter='::', engine='python', header=None, names = ['User ID', 'Movie ID', 'Rating', 'Rating Timestamp'])


# In[ ]:


print("The movies dataset has {0} rows and {1} columns".format(movies_data.shape[0], movies_data.shape[1]))
print("The users dataset has {0} rows and {1} columns".format(users_data.shape[0], movies_data.shape[1]))
print("The ratings dataset has {0} rows and {1} columns".format(ratings_data.shape[0], movies_data.shape[1]))


# Checking whether movies dataset has duplicate rows

# In[ ]:


pd.concat(g for _, g in movies_data.groupby("Movie ID") if len(g) > 1)


# Removing the duplicates from the dataset

# In[ ]:


cleared_movies = movies_data.drop_duplicates('Movie ID')


# ### Merging Movies and Ratings

# In[ ]:


merged_data = ratings_data.merge(cleared_movies, how = 'inner', on = ['Movie ID'])
merged_data.head()


# ### Extract Info from Timestamp

# In[ ]:


time_info = []

for i in range(merged_data.shape[0]):
    ts = int(merged_data.iloc[i]['Rating Timestamp'])
    current_info = [datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d'), datetime.utcfromtimestamp(ts).strftime('%m'), datetime.utcfromtimestamp(ts).strftime('%Y'), datetime.utcfromtimestamp(ts).strftime('%H:%M:%S')]
    time_info.append(current_info)


# In[ ]:


merged_data[['Date', 'Month', 'Year', 'Time']] = pd.DataFrame(time_info)


# In[ ]:


merged_data = merged_data.drop('Rating Timestamp', axis=1)


# In[ ]:


merged_data.head()


# In[ ]:


genre_data = pd.DataFrame(merged_data.groupby('Genre')['Movie ID'].nunique()).reset_index()


# In[ ]:


fig = go.Figure(data=[go.Pie(labels=genre_data.head(5)['Genre'], values=genre_data.head(5)['Movie ID'])])
fig.show()


# In[ ]:


fig = px.box(merged_data, y="Rating")
fig.show()


# In[ ]:


date_count = pd.DataFrame(merged_data.groupby('Date')['User ID'].count()).reset_index()
date_count = date_count.sort_values('Date')


# In[ ]:


fig = px.line(date_count, x='Date', y='User ID')
fig.show()


# In[ ]:


genre = {}

for i in range(merged_data.shape[0]):
    genre_data = merged_data.iloc[i]['Genre']
    
    if pd.isna(genre_data) == False:
        try:
            if '|' in genre_data:
                genre_list = genre_data.split('|')

                for key in genre_list:
                    if key in genre:
                        genre[key]+=1
                    else:
                        genre[key]=1            

            else:
                if genre_data in genre:
                    genre[genre_data]+=1
                else:
                    genre[genre_data]=1
        except:
            print(genre_data)


# In[ ]:


fig = go.Figure(data=[go.Pie(labels=list(genre.keys()), values=list(genre.values()))])
fig.show()


# In[ ]:




