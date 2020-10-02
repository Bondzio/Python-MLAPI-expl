#!/usr/bin/env python
# coding: utf-8

# Simple exploration notebook 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from nltk.corpus import stopwords

get_ipython().run_line_magic('matplotlib', 'inline')


# **Wordcloud on tags:**
# 
# Let us create a word cloud on the tags column for all topics and see the important tags.

# In[ ]:


topics_list = ['biology', 'cooking', 'crypto', 'diy', 'robotics', 'travel']

for ind, topic in enumerate(topics_list):
    tags = np.array(pd.read_csv("../input/"+topic+".csv", usecols=['tags'])['tags'])
    text = ''
    for ind, tag in enumerate(tags):
        text = " ".join([text, tag])
    text = text.strip()
    
    wordcloud = WordCloud(background_color='white', width=600, height=300, max_font_size=50, max_words=40).generate(text)
    wordcloud.recolor(random_state=ind*312)
    plt.imshow(wordcloud)
    plt.title("Wordcloud for topic : "+topic)
    plt.axis("off")
    plt.show()


# **Wordcloud for topic Biology:**
#    
# Let us take a single topic 'biology' and then see how the word clouds from each of the three fields title, content, tags compare with each other.

# In[ ]:


bio = pd.read_csv("../input/biology.csv")
title = np.array(bio['title'])
content = np.array(bio['content'])
tags = np.array(bio['tags'])

# wordcloud for tags #
text = ''
for ind, tag in enumerate(tags):
    text = " ".join([text, tag])
text = text.strip()

wordcloud = WordCloud(background_color='white', width=600, height=300, max_font_size=50, max_words=80).generate(text)
wordcloud.recolor(random_state=218)
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Wordcloud on 'tags' for biology ")
plt.show()

# wordcloud for title #
text = ''
for ind, tag in enumerate(title):
    text = " ".join([text, tag])
text = text.strip()

stop_words = set(stopwords.words('english') + ['sas', 'ss', 'fas', 'des', 'les', 'ess'])
wordcloud = WordCloud(background_color='white', width=600, height=300, stopwords=stop_words, max_font_size=50, max_words=80).generate(text)
wordcloud.recolor(random_state=218)
plt.imshow(wordcloud)
plt.axis("off")
plt.title("Wordcloud on 'title' for biology ")
plt.show()

### Commenting this out for now as it throws error while rendering and not while running it at the backend ###
## wordcloud for content #
#text = ''
#for ind, tag in enumerate(content):
#    text = " ".join([text, tag])
#text = text.strip()

#stop_words = set(stopwords.words('english') + ['rbs', 'sas', 'ss', 'fas', 'des', 'ess', 'les', 'bas', 'poses', 'los', 'ros', 'cs'])
#wordcloud = WordCloud(background_color='white', width=600, height=300, stopwords=stop_words, max_font_size=50, max_words=80).generate(text)
#wordcloud.recolor(random_state=218)
#plt.imshow(wordcloud)
#plt.axis("off")
#plt.title("Wordcloud on 'content' for biology ")
#plt.show()


# As we can see, wordcloud from 'topic' is decent and has some important words related to the topic and can be used for tag creation.
# 
# Wordcloud from 'content' has more irrelevant (html) words and so we need to do proper cleaning to remove those before we start with our modeling / learning.
# 
# More to come...!
