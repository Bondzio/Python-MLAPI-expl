#!/usr/bin/env python
# coding: utf-8

# In[13]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np
import os
import pandas as pd
import sys
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import nltk
from wordcloud import WordCloud,STOPWORDS

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[2]:


df = pd.read_csv('../input/bhagavad-gita.csv')


# In[24]:


plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 15
plt.rcParams['font.size'] = 15


# In[3]:


df.head()


# # Chapter-wise distribution of verses

# In[26]:


li = df['title'].astype(int)
plt.figure(figsize=(12,8))
plt.tick_params(labelsize=11)
sns.countplot(li)
plt.xlabel("Chapter")
plt.ylabel("Number of verses")
plt.show()


# **Chapter 18** has *highest* number of verses whereas **Chapter 12** and **Chapter 15** have *lowest* number of verses.

# # Chapter-wise WordCloud

# In[41]:


#chapter count
list_counts = li.value_counts()
start = 0
for i in range(1,19):
    chap_length = list_counts[i]
    #print(chap_length)
    chap_df = df[start:start+chap_length]
    start = start + chap_length
    #print(chap_df.shape)
    
    # create wordcloud
    words = chap_df["verse_text_no_samdhis"][~pd.isnull(chap_df["verse_text_no_samdhis"])]
    wordcloud = WordCloud(max_font_size=50, width=600, height=300).generate(' '.join(words))
    plt.figure(figsize=(12,12))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title("Chapter "+ str(i))
    plt.axis("off")


# # Wordcloud with all chapters

# In[4]:


words = df["verse_text_no_samdhis"][~pd.isnull(df["verse_text_no_samdhis"])]


# In[5]:


wordcloud = WordCloud(max_font_size=50, width=600, height=300,max_words=2000).generate(' '.join(words))


# In[42]:


plt.figure(figsize=(12,12))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title("All chapters")
plt.axis("off")


# In[ ]:




