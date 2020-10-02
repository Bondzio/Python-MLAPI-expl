#!/usr/bin/env python
# coding: utf-8

# This notebook is based on this tutorial from datacamp : https://www.datacamp.com/community/tutorials/wordcloud-python

# In[ ]:


# Start with loading all necessary libraries
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

data_forum = {}
import os
for dirname, _, filenames in os.walk('/kaggle/input/meta-kaggle'):
    for filename in filenames:
        if 'Forum' in filename:
            data_forum[filename.split('.csv')[0]] = pd.read_csv(os.path.join(dirname, filename))


# In[ ]:


for filename, df in data_forum.items():
    print(filename)
    print(df.head())
    print("-"*20)


# Let's first try with only `ForumTopics`, working on `Title`.

# In[ ]:


data_forum['ForumTopics']['Title'] = data_forum['ForumTopics']['Title'].astype(str)


# In[ ]:


text = " ".join(data_forum['ForumTopics']['Title'].values.tolist())

# Create and generate a word cloud image:
wordcloud = WordCloud().generate(text)

# Display the generated image:
fig, ax = plt.subplots(figsize=(15, 10))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
plt.show()


# In[ ]:


# Create stopword list:
stopwords = set(STOPWORDS)
# stopwords.update(["to"])

# Generate a word cloud image
wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)

# Display the generated image:
# the matplotlib way:
fig, ax = plt.subplots(figsize=(15, 10))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
plt.show()


# Now, we can also try to take into account the "hotness". For this, I will just weight observations with the total number of messages in the forum.

# In[ ]:


def weight_topic(df):
    return " ".join([df['Title'] for _ in range(df['TotalMessages'])])
data_forum['ForumTopics']['Title_weighted'] = data_forum['ForumTopics'].apply(weight_topic, axis=1)
text_weighted = " ".join(data_forum['ForumTopics']['Title_weighted'].values.tolist())
data_forum['ForumTopics'].head()


# In[ ]:


wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white").generate(text_weighted)
fig, ax = plt.subplots(figsize=(15, 10))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
plt.show()


# `place solution` seems to be much more represented ! Probably the topics of solutions to competitons are those who create the more discussions.

# Now let's do it for discussion messages : 

# In[ ]:


data_forum['ForumMessages']['Message'] = data_forum['ForumMessages']['Message'].astype(str)
text_messages = " ".join(data_forum['ForumMessages']['Message'].values.tolist())


# In[ ]:


wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white").generate(text_messages)
fig, ax = plt.subplots(figsize=(15, 10))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
plt.show()


# This time, we will try to weight them by `(5-Medal)` (otherwise non-medaled topics won't be taken into account):

# In[ ]:


data_forum['ForumMessages'].Medal.describe(), data_forum['ForumMessages'].Medal.isna().describe()


# In[ ]:


data_forum['ForumMessages']['Medal'].fillna(4, inplace=True)
def weight_message(df):
    return " ".join([df['Message'] for _ in range(5-df['Medal'])])
data_forum['ForumMessages']['Message_weighted'] = data_forum['ForumMessages'].apply(weight_message, axis=1)
message_weighted = " ".join(data_forum['ForumMessages']['Message_weighted'].values.tolist())
data_forum['ForumMessages'].head()


# In[ ]:


wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white").generate(message_weighted)
fig, ax = plt.subplots(figsize=(15, 10))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
plt.show()

