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


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

from wordcloud import WordCloud, STOPWORDS


# In[ ]:


data=pd.read_csv("../input/top-spotify-songs-from-20102019-by-year/top10s.csv",encoding="ISO-8859-1")


# In[ ]:


data.head()


# In[ ]:


#removing the unnamed:0 col
data.drop('Unnamed: 0', axis=1, inplace=True)


# In[ ]:


data.info()


# In[ ]:


data.isna().sum()


# In[ ]:


#no Null values in the dataset from above output


# In[ ]:


data.describe().T


# In[ ]:


corr=data.corr()
plt.figure(figsize=(10,8))
sns.heatmap(corr,annot=True)


# In[ ]:


#Renaming the cols for convenience
data.rename(columns = {'top genre': 'top_genre', 'bpm': 'beats_per_minute', 'nrgy': 'energy', 
                       'dnce': 'danceability', 'dB': 'loudness(dB)', 'live': 'liveness', 
                       'val': 'valence', 'dur': 'length', 'acous': 'acousticness', 
                       'spch': 'speechiness', 'pop': 'popularity'}, inplace=True)


# In[ ]:


sns.distplot(data["popularity"])


# In[ ]:


sns.scatterplot(x=data.liveness,y=data.popularity,data=data)


# In[ ]:


sns.catplot(y="beats_per_minute", x="year", data=data)


# In[ ]:


sns.boxplot(y="beats_per_minute", x="year", data=data)


# In[ ]:


plt.figure(figsize=(14,10))
plt.title('Most frequent Artist',fontsize=15)
plt.xlabel('Artist', fontsize=15)
plt.ylabel('Count', fontsize=15)

sns.countplot(data.artist,order=pd.value_counts(data.artist).iloc[:15].index,palette=sns.color_palette("cubehelix", 15))

plt.xticks(size=20,rotation=90)
plt.yticks(size=20)
sns.despine(bottom=True, left=True)
plt.show()


# In[ ]:


#Katy Perry ,Justin Bieber and Rihanna are the top 3 artist for the years 2010-2019


# In[ ]:


plt.figure(figsize=(14,10))
plt.title('Most frequent Artist',fontsize=15)
plt.xlabel('Artist', fontsize=15)
plt.ylabel('Count', fontsize=15)

sns.countplot(data.title,order=pd.value_counts(data.title).iloc[:25].index,palette=sns.color_palette("BrBG", 25))

plt.xticks(size=20,rotation=90)
plt.yticks(size=20)
sns.despine(bottom=True, left=True)
plt.show


# In[ ]:


#Say Something is the most listened song in the 2010 decade


# In[ ]:


import squarify
plt.figure(figsize=(28,12))
squarify.plot(sizes=data.artist.value_counts(), label=data["artist"], alpha=.8 , text_kwargs={'fontsize':10})
plt.axis('off')
plt.show()


# In[ ]:


wordcloud = WordCloud(width = 1000, height = 600, max_font_size = 200, max_words = 150,
                      background_color='white').generate(" ".join(data.top_genre))

plt.figure(figsize=[10,10])
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

