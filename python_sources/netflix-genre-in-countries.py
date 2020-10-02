#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[ ]:


#reading Dataset
netflix = pd.read_csv("/kaggle/input/netflix-shows/netflix_titles.csv",  sep = ',',encoding = "ISO-8859-1", header= 0)


# In[ ]:


netflix.head()


# In[ ]:


#Na Handling
netflix.isnull().values.any()
netflix.isnull().values.sum()
netflix.isnull().sum()*100/netflix.shape[0]


# In[ ]:


netflix_data = netflix.dropna()


# In[ ]:



netflix_data.isnull().sum()


# In[ ]:


netflix_data.head()


# In[ ]:


from collections import Counter
genre = netflix_data['listed_in']
genre_count = pd.Series(dict(Counter(','.join(genre).replace(' ,',',').replace(', ',',')
                                       .split(',')))).sort_values(ascending=False)

genre_count


# In[ ]:


genre_top = genre_count[:20]
plt.figure(figsize=(20,12))
sns.barplot(genre_top, genre_top.index)
plt.show()


# In[ ]:


country = netflix_data['country']
country_count = pd.Series(dict(Counter(','.join(country).replace(' ,',',').replace(', ',',')
                                       .split(',')))).sort_values(ascending=False)


# In[ ]:


country_top = country_count[:20]
plt.figure(figsize=(20,12))
sns.barplot(country_top, country_top.index)
plt.show()


# In[ ]:


## Concatinating both Genre and Country


# In[ ]:


netflix_data['primary_country'] = netflix_data['country'].apply(lambda x: x.split(',')[0])
netflix_data['genre'] = netflix_data['listed_in'].apply(lambda x: x.split(',')[0])


# In[ ]:


netflix_data['genre_country'] = netflix_data['primary_country'] + '&' + netflix_data['genre']


# In[ ]:


netflix_data['genre_country'].head()


# In[ ]:


netflix_data_c = netflix_data['genre_country']
netflix_data_count = pd.Series(dict(Counter(','.join(netflix_data_c).replace(' ,',',').replace(', ',',')
                                       .split(',')))).sort_values(ascending=False)


# In[ ]:


## Printing top 20 countries 
netflix_data_top = netflix_data_count[:20]
plt.figure(figsize=(20,12))
sns.barplot(netflix_data_top, netflix_data_top.index)
plt.show()


# In[ ]:


## Trying for Squarify plot
import squarify
squarify.plot(sizes=netflix_data_top.values,label=netflix_data_top.index, color=sns.color_palette('RdGy'),
             linewidth=10, text_kwargs={'fontsize':50})
plt.axis('off')
plt.rcParams['figure.figsize'] = (100,120)
plt.title('Top 20 movie genre and country')
plt.show()


# In[ ]:


## Getting most Genre type of all times
from wordcloud import WordCloud, STOPWORDS
stopwords = STOPWORDS
wordcloud = WordCloud(width=800,height=400,stopwords=stopwords, min_font_size=10,max_words=150).generate(' '.join
                                                                                           (netflix_data['genre']))


# In[ ]:


plt.imshow(wordcloud)
plt.axis('off')
plt.title("Most Popular words in Title", fontsize=25)
plt.show()


# In[ ]:


from datetime import datetime
netflix_data['date_added'] = pd.to_datetime(netflix_data['date_added'])


# In[ ]:


netflix_data.head()


# In[ ]:


netflix_data.shape


# In[ ]:


netflix_data_safe = netflix_data.copy()


# In[ ]:


netflix_data['lead_cast'] = netflix_data['cast'].apply(lambda x: x.split(',')[0])


# In[ ]:


netflix_data['season_count'] = netflix_data.apply(lambda x : x['duration'].split(" ")[0] if "Season" in x['duration'] else "", axis = 1)
netflix_data['duration'] = netflix_data.apply(lambda x : x['duration'].split(" ")[0] if "Season" not in x['duration'] else "", axis = 1)
netflix_data['duration'] =netflix_data.apply(lambda x : '0' if x['duration']=='' else x['duration'],axis=1)
netflix_data['duration'] =  netflix_data['duration'].astype(float)


# In[ ]:


netflix_data['date_added'] = netflix_data['date_added'].dt.strftime('%Y %B')


# In[ ]:


netflix_data.head(5)


# In[ ]:


netflix_data_genre = netflix_data.groupby('genre')


# In[ ]:


sns.countplot(data=netflix_data, y=netflix_data['genre'],order=netflix_data['genre'].value_counts().index)
sns.set(font_scale=25.0)
plt.show()


# In[ ]:




