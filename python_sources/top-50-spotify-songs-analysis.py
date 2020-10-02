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


# # Predicting the popularity of a song
# ![spotify](https://www.ft.com/__origami/service/image/v2/images/raw/http%3A%2F%2Fcom.ft.imagepublish.upp-prod-us.s3.amazonaws.com%2F97fcb70e-447a-11ea-9a2a-98980971c1ff?fit=scale-down&source=next&width=700)
# 
# **Spotify is a digital music service that gives you access to millions of songs. When a new user who signs up for spotify and has no idea about music, can listen to new songs based on the popularity.****
# 
# I have predicted the popularity of a song by using various features. The order by which the entire life cycle of this project is listed below.
# 
# 
# 1. ### Importing and understanding the data.
# 2. ### Data Pre-processing
# 3. ### Exploratory Data Analysis
# 4. ### Training the model for Prediction
# 5. ### Predicting the output using the test data.

# # 1. Importing and Understanding the data
# 

# In[ ]:


import matplotlib.pyplot as plt
import seaborn as sns


get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df = pd.read_csv('/kaggle/input/top50spotify2019/top50.csv',encoding='ISO-8859-1')
df.head(50)


# # 2. Data Pre-processing
df.drop('Unnamed: 0', axis = 1, inplace = True)
# -> As the first column is not useful for further steps, I remove it.

# In[ ]:


delete_row = df[df["Track.Name"]== 'Panini'].index
df = df.drop(delete_row)


# **-> As there is no track in the name of '0.958333333333333', I delete that particular row.**

# In[ ]:


f, axes = plt.subplots(3,3, figsize=(30,10))

plt.subplots_adjust(bottom = -5.0)
x1 = sns.boxplot(x = 'Genre', y = 'Beats.Per.Minute', data = df, ax = axes[0][0])
x1.set_xticklabels(x1.get_xticklabels(), rotation=90)
x2 = sns.boxplot(x = 'Genre', y = 'Danceability', data = df, ax = axes[0][1])
x2.set_xticklabels(x2.get_xticklabels(), rotation=90)
x3 = sns.boxplot(x = 'Genre', y = 'Energy', data = df, ax = axes[0][2])
x3.set_xticklabels(x3.get_xticklabels(), rotation=90)
x4 = sns.boxplot(x = 'Genre', y = 'Loudness..dB..', data = df, ax = axes[1][0])
x4.set_xticklabels(x4.get_xticklabels(), rotation=90)
x5 = sns.boxplot(x = 'Genre', y = 'Liveness', data = df, ax = axes[1][1])
x5.set_xticklabels(x5.get_xticklabels(), rotation=90)
x6 = sns.boxplot(x = 'Genre', y = 'Valence.', data = df,  ax = axes[1][2])
x6.set_xticklabels(x6.get_xticklabels(), rotation=90)
x7 = sns.boxplot(x = 'Genre', y = 'Length.', data = df,  ax = axes[2][0])
x7.set_xticklabels(x7.get_xticklabels(), rotation=90)
x8 = sns.boxplot(x = 'Genre', y = 'Acousticness..', data = df,  ax = axes[2][1])
x8.set_xticklabels(x8.get_xticklabels(), rotation=90)
x9 = sns.boxplot(x = 'Genre', y =  'Speechiness.', data = df,  ax = axes[2][2])
x9.set_xticklabels(x9.get_xticklabels(), rotation=90)


# **-> Even though there are a few outliers, I do not tend to remove or replace them.**

# In[ ]:


df.isnull().sum()


# **-> As there are no missing values in any of the columns, I finish my data processing my data preprocessing with this step. **

# # 3. Exploratory Data Analysis

# In[ ]:


plt.figure(figsize=(50,25))
ax = df.groupby(['Track.Name'])['Popularity'].agg(max).sort_values(ascending = False).plot(kind = 'bar', fontsize = 30)
ax = plt.xlabel('Track Name', fontsize = 30)
ax = plt.ylabel('Popularity', fontsize = 30)
ax = plt.title('Track.Name vs Popularity', fontsize = 50)
ax = plt.rcParams.update({'font.size': 22})


# **-> The Track.Name 'bag guy' has the highest popularity and 'If I Can't Have You' has the least popularity. **

# In[ ]:


fig = plt.figure(figsize = (15,7))
df.groupby('Genre')['Popularity'].count().sort_values(ascending=False).plot(kind = 'bar')
plt.ylabel('Popularity', fontsize = 25)
plt.title('Genre vs Popularity')


# ** -> The Genre 'dance pop' has the most popularity and 'boy band' has the least popularity.**

# In[ ]:


f, axes = plt.subplots(3, 3, figsize=(20,20))

sns.distplot(df["Beats.Per.Minute"], kde = False, bins = 10, ax=axes[0][0])
sns.distplot(df['Energy'], kde = False, bins= 10, ax=axes[0][1])
sns.distplot(df['Danceability'],  kde = False, bins = 10, ax=axes[0][2])
sns.distplot(df['Loudness..dB..'],  kde = False, bins = 10, ax=axes[1][0])
sns.distplot(df['Liveness'],  kde = False, bins = 10, ax=axes[1][1])
sns.distplot(df['Valence.'],  kde = False, bins = 10, ax=axes[1][2])
sns.distplot(df['Length.'],  kde = False, bins = 10, ax=axes[2][0])
sns.distplot(df['Acousticness..'],  kde = False, bins = 10, ax=axes[2][1])
sns.distplot(df['Speechiness.'],  kde = False, bins = 10, ax = axes[2][2])


# **-> Above is the histogram of all the features which determine the popularity of a song.**

# In[ ]:


df.columns


# In[ ]:


fig = plt.figure(figsize = (15,7))
df.groupby(['Genre'])['Length.'].agg(max).plot(kind = 'bar')
plt.xticks(rotation=90)


# **-> Genre 'reggaeton flow' has the maximum length and 'trap music' has the minimum length.**

# In[ ]:


corr_data = df[['Beats.Per.Minute', 'Energy',
       'Danceability', 'Loudness..dB..', 'Liveness', 'Valence.', 'Length.',
       'Acousticness..', 'Speechiness.', 'Popularity']].corr()
plt.figure(figsize=(15,10))
sns.heatmap(corr_data, annot = True)


# **-> The heatmap above says the follwing**
# * Beats.Per.Minute and Speechiness. are highly correlated with each other.
# * Energy and Loudness..dB.. are highly correlated with each other.
# 
# **
# -> Accordingly, when two variables are highly correlated with each other, they tend to have higher variance in both the variables.
#    So, high correlations make it hard to estimate the actual effect of each variable.**

# In[ ]:


xtick = ['dance pop', 'pop', 'latin', 'edm', 'canadian hip hop',
       'panamanian pop', 'electropop', 'reggaeton flow', 'canadian pop',
       'reggaeton', 'dfw rap', 'brostep', 'country rap', 'escape room',
       'trap music', 'big room', 'boy band', 'pop house', 'australian pop',
       'r&b en espanol', 'atl hip hop']
length = np.arange(len(xtick))
genre_groupby = df.groupby('Genre')['Track.Name'].agg(len).sort_values(ascending = False)
plt.figure(figsize = (15,7))
plt.bar(length, genre_groupby)
plt.xticks(length,xtick)
plt.xticks(rotation = 90)
plt.xlabel('Genre', fontsize = 20)
plt.ylabel('Count of the tracks', fontsize = 20)
plt.title('Genre vs Count of the tracks', fontsize = 25)


# In[ ]:


df.head()


# In[ ]:


df.pivot_table(index = ['Genre','Track.Name'], values = ['Popularity'], aggfunc = 'max')


# In[ ]:


df.loc[df['Genre'] == 'pop', ['Track.Name','Artist.Name']]


# In[ ]:


import squarify as sq
plt.figure(figsize = (20,7))
sq.plot(sizes = df.Genre.value_counts(), label = df.Genre.unique())
plt.axis('off')
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 32}
plt.rc('font')
plt.show()


# In[ ]:


c = np.arange(1,50)
plt.subplots_adjust(bottom = -5.0)
fig = plt.figure(figsize=(25,15))

plt.subplot(331)
plt.scatter(df['Beats.Per.Minute'],df['Popularity'], c = c)
plt.xlabel('Beats per minute', fontsize = 15)
plt.ylabel('Energy', fontsize = 15)
plt.title('Beats per minute vs Energy')

plt.subplot(332)
plt.scatter(df['Energy'],df['Popularity'], c = c)
plt.xlabel('Energy', fontsize = 15)
plt.ylabel('Popularity', fontsize = 15)
plt.title('Energy vs Popularity')

plt.subplot(333)
plt.scatter(df['Loudness..dB..'],df['Popularity'], c = c)
plt.xlabel('Loudness..dB..', fontsize = 15)
plt.ylabel('Popularity', fontsize = 15)
plt.title('Loudness..dB.. vs Popularity')

plt.subplot(334)
plt.scatter(df['Danceability'],df['Popularity'], c = c)
plt.xlabel('Danceability', fontsize = 15)
plt.ylabel('Popularity', fontsize = 15)
plt.title('Danceability vs Popularity')

plt.subplot(335)
plt.scatter(df['Liveness'],df['Popularity'], c = c)
plt.xlabel('Liveness', fontsize = 15)
plt.ylabel('Popularity', fontsize = 15)
plt.title('Liviness vs Popularity')

plt.subplot(336)
plt.scatter(df['Valence.'],df['Popularity'], c = c)
plt.xlabel('Valence.', fontsize = 15)
plt.ylabel('Popularity', fontsize = 15)
plt.title('Valence. vs Popularity')

plt.subplot(337)
plt.scatter(df['Length.'],df['Popularity'], c = c)
plt.xlabel('Length.', fontsize = 15)
plt.ylabel('Popularity', fontsize = 15)
plt.title('Length. vs Popularity')

plt.subplot(338)
plt.scatter(df['Acousticness..'],df['Popularity'], c = c)
plt.xlabel('Acousticness..', fontsize = 15)
plt.ylabel('Popularity', fontsize = 15)
plt.title('Acousticness.. vs Popularity')

plt.subplot(339)
plt.scatter(df['Speechiness.'],df['Popularity'], c = c)
plt.xlabel('Speechiness.', fontsize = 15)
plt.ylabel('Popularity', fontsize = 15)
plt.title('Speechiness. vs Popularity')
fig.tight_layout() 


# In[ ]:


labels = ['dance pop',
 'pop',
 'latin',
 'canadian hip hop',
 'edm',
 'reggaeton',
 'reggaeton flow',
 'dfw rap',
 'canadian pop',
 'panamanian pop',
 'electropop',
 'brostep',
 'country rap',
 'atl hip hop',
 'trap music',
 'australian pop',
 'pop house',
 'big room',
 'boy band',
 'escape room',
 'r&b en espanol']
sizes = [8, 7, 5, 3, 3, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]
plt.figure(figsize=(18,13))
patches, texts = plt.pie(sizes,autopct='%.2f')
plt.legend(patches, labels,loc="best")
plt.axis('equal')
plt.tight_layout()
plt.show()


# In[ ]:


from wordcloud import WordCloud
plt.style.use('seaborn')
wrds1 = df.groupby("Artist.Name")["Popularity"].agg(len).sort_values(ascending = False).keys()
wc1 = WordCloud(scale=5,max_words=1000,colormap="rainbow",background_color="white").generate(" ".join(wrds1))
plt.figure(figsize = (15,7))
plt.imshow(wc1,interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud between the Artist Names\n\n", color = "black", fontsize = 30)
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




