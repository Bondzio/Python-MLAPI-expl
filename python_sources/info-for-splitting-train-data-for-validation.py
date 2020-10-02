#!/usr/bin/env python
# coding: utf-8

# This kernel was created to determine the best way of splitting the training data set into train and validation sets.
# 
# After seeing that the distributions of the train and test data sets are extremely similar, I show that splitting the data set into two parts without any sort of sampling or shuffling produces a validation data set that is also extremely similar to the test set distribution. For this example I use the final 20% of the dataset (as it is ordered in the CSV file) as the validation data.
# 
# This would also seem to support the assertion in [this kernel (I have to say this...)](https://www.kaggle.com/kamilkk/i-have-to-say-this) that the data is chronologically ordered.

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# Read CSV Files and Merge Data
# ---

# In[ ]:


train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')
songs = pd.read_csv('../input/songs.csv')
members = pd.read_csv('../input/members.csv')


# In[ ]:


train_merged = train.merge(songs, how='left', on='song_id').merge(members, how='left', on='msno')


# In[ ]:


test_merged = test.merge(songs, how='left', on='song_id').merge(members, how='left', on='msno')


# In[ ]:


train_merged.head()


# Basic Information
# ---

# In[ ]:


print("Train size:\t", len(train_merged))
print("Test size:\t", len(test_merged))
print("Ratio:\t\t", "{0: 0.4f}".format(len(test_merged) / len(train_merged)))


# In[ ]:


only_train_merged = train_merged[:int(len(train_merged)*0.8)]
val_merged = train_merged[int(len(train_merged)*0.8):]


# Members
# -----

# In[ ]:


new_members = test_merged[~test_merged.msno.isin(train_merged.msno)]
new_val_members = val_merged[~val_merged.msno.isin(only_train_merged.msno)]


# In[ ]:


print("New members in test set:\t", len(new_members))
print("Ratio of new members in test:\t", "{0: 0.4f}".format(
    len(new_members) / (len(test_merged))
))
print("Ratio of new members in val:\t", "{0: 0.4f}".format(
    len(new_val_members) / (len(val_merged))
))


# In[ ]:


sns.distplot(train_merged.bd[train_merged.bd < 100])
sns.distplot(test_merged.bd[test_merged.bd < 100])
sns.distplot(val_merged.bd[val_merged.bd < 100])
plt.legend(['Train', 'Test', 'Val'])


# In[ ]:


city_ratios = pd.concat([
    train_merged.city.value_counts(normalize=True),
    test_merged.city.value_counts(normalize=True),
    val_merged.city.value_counts(normalize=True)
], keys=['Train', 'Test', 'Val']).reset_index()
city_ratios.columns = ['Dataset', 'City', 'Ratio']
sns.barplot(data=city_ratios, hue='Dataset', x='City', y='Ratio')


# In[ ]:


gender_ratios = pd.concat([
    train_merged.gender.value_counts(normalize=True),
    test_merged.gender.value_counts(normalize=True),
    val_merged.gender.value_counts(normalize=True)
], keys=['Train', 'Test', 'Val']).reset_index()
gender_ratios.columns = ['Dataset', 'Gender', 'Ratio']
sns.barplot(data=gender_ratios, hue='Dataset', x='Gender', y='Ratio')


# Songs
# ----

# In[ ]:


new_songs = test_merged[~test_merged.song_id.isin(train_merged.song_id)]
new_val_songs = val_merged[~val_merged.song_id.isin(only_train_merged.song_id)]


# In[ ]:


print("Ratio of new songs test:\t", "{0: 0.4f}".format(
    len(new_songs) / (len(test_merged))
))
print("Ratio of new songs in val:\t", "{0: 0.4f}".format(
    len(new_val_songs) / (len(val_merged))
))


# In[ ]:


language_ratios = pd.concat([
    train_merged.language.value_counts(normalize=True),
    test_merged.language.value_counts(normalize=True),
    val_merged.language.value_counts(normalize=True)
], keys=['Train', 'Test', 'Val']).reset_index()
language_ratios.columns = ['Dataset', 'Language', 'Ratio']
sns.barplot(data=language_ratios, hue='Dataset', x='Language', y='Ratio')


# In[ ]:


sns.distplot(train_merged.song_length[train_merged.song_length < 5000].dropna())
sns.distplot(test_merged.song_length[test_merged.song_length < 5000].dropna())
sns.distplot(val_merged.song_length[val_merged.song_length < 5000].dropna())
plt.legend(['Train', 'Test', 'Val'])


# In[ ]:


train_genre_set = set(train_merged.genre_ids)
test_genre_set = set(test_merged.genre_ids)
val_genre_set = set(val_merged.genre_ids)
only_train_genre_set = set(only_train_merged.genre_ids)
print("Ratio of new genres in test:", "{0: 0.4f}".format(len(test_genre_set - train_genre_set) / len(test_genre_set)))
print("Ratio of new genres in val:", "{0: 0.4f}".format(len(val_genre_set - only_train_genre_set) / len(val_genre_set)))


# In[ ]:


train_artist_set = set(train_merged.artist_name)
test_artist_set = set(test_merged.artist_name)
val_artist_set = set(val_merged.artist_name)
only_train_artist_set = set(only_train_merged.artist_name)
print("Ratio of new artists in test:", "{0: 0.4f}".format(len(test_artist_set - train_artist_set) / len(test_artist_set)))
print("Ratio of new artists in val:", "{0: 0.4f}".format(len(val_artist_set - only_train_artist_set) / len(val_artist_set)))


# In[ ]:




