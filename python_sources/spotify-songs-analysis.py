#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install wikipedia')


# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import wikipedia as wiki
import seaborn as sns
import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# # Set Plotting style

# In[ ]:


plt.figure(figsize=(16,8))


# In[ ]:


import spacy
nlp = spacy.load('en')


# # Read file

# In[ ]:


path = "/kaggle/input/top-spotify-songs-from-20102019-by-year/top10s.csv"
df = pd.read_csv(path,encoding='ISO-8859-1',index_col=0)


# # Head

# In[ ]:


df.head()


# # Columns

# In[ ]:


df.columns


# # Duration Trend

# In[ ]:


df.groupby(['year']).dur.mean().plot()


# # Artist appear most top 10

# In[ ]:


df.artist.value_counts().reset_index().head(10)


# # Music Type Top 10 pie chart

# In[ ]:


top_10_type = df['top genre'].value_counts().nlargest(10).index
df_updated = df.where(df['top genre'].isin(top_10_type),other='Other')
df_updated['top genre'].value_counts().plot(kind='pie')


# # 2019 Music type Top 10 pie chart

# In[ ]:


df_19 = df[df.year==2019]
df[df.year==2019]['top genre'].value_counts().plot(kind='pie')


# # 2019 Danceability top 10

# In[ ]:


dnce_19_df = df_19.sort_values(by='dnce',ascending=False)
dnce_19_df[['title','artist','dnce']].head(10)


# # History Danceability top 10

# In[ ]:


his_dnce_df = df.sort_values(by='dnce',ascending=False).head(10)
his_dnce_df[['title','artist','dnce']]


# # Artist locations share

# In[ ]:


# artists
artists_arr = df.artist.value_counts().head(10).index


# In[ ]:


def get_location_info(summary):
    doc = nlp(summary)
    ents = {}
    for ent in doc.ents:
        # Save interesting entities
        if ent.label_ in ['NORP','PERSON']:
            ents[ent.label_] = ent.text
    return ents


# In[ ]:


artist_loc_dict_arr = []

for artist in artists_arr:
    dict_info = get_location_info(wiki.summary(artist))
    artist_loc_dict_arr.append(dict_info)


# In[ ]:


artist_loc_df = pd.DataFrame(artist_loc_dict_arr)


# In[ ]:


plt.figure(figsize=(16,8))
plt.title('Most frequent Artist location',fontsize=30)
plt.xlabel('Location', fontsize=20)
plt.ylabel('Count', fontsize=20)

artist_loc_df.NORP.value_counts().plot(kind='bar')

plt.xticks(size=20,rotation=90)
plt.yticks(size=20)
sns.despine(bottom=True, left=True)
plt.show()


# # Popular Songs

# In[ ]:


plt.figure(figsize=(16,8))
df.sort_values(by='pop',ascending=False).artist.value_counts().head(10).plot(kind='pie')

