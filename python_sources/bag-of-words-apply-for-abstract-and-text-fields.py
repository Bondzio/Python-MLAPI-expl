#!/usr/bin/env python
# coding: utf-8

# ## About this notebook
# In this notebook, I applied bag of word for abstract and text columns and generated new files. I hope this will help some one who try to solve this tasks
# I used output files from [xhlulu's kernel output](https://www.kaggle.com/xhlulu/cord-19-eda-parse-json-and-generate-clean-csv),Go and check it and give credits.
# 

# In[ ]:


import nltk    
import random  
import string

import bs4 as bs  
import urllib.request  
import re 

import os

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)



import os

directory = '/kaggle/input/cord-19-eda-parse-json-and-generate-clean-csv/'

for dirname, _, filenames in os.walk(directory):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


comm_use_df = pd.read_csv("/kaggle/input/cord-19-eda-parse-json-and-generate-clean-csv/clean_comm_use.csv")


# In[ ]:


comm_use_df.head()


# In[ ]:


comm_use_df.columns


# **corpus into individual sentences**"
# convert the sentence to lower case, and then remove the punctuation and empty spaces from the text. and remove abstract key in every corpus

# **tokenize the sentences in the corpus and create a dictionary that contains words and their corresponding frequencies in the corpus**

# In[ ]:


def format_corpus(corpus):  
    for i in range(len(corpus)):
        corpus [i] = corpus [i].lower()
        corpus [i] = re.sub(r'\W',' ',corpus [i])
        corpus [i] = re.sub(r'\s+',' ',corpus [i])
    return corpus


# **tokenize the sentences in the corpus and create a dictionary that contains words and their corresponding frequencies in the corpus**

# In[ ]:


def word_frequencies(corpus):
    wordfreq = {}
    for sentence in corpus:
        tokens = nltk.word_tokenize(sentence)
        for token in tokens:
            if token not in wordfreq.keys():
                wordfreq[token] = 1
            else:
                wordfreq[token] += 1
    return wordfreq


# In[ ]:


def make_bow_csv(csv_df,df_name): 
    all_rows = []
    for i, row in csv_df.iterrows():
        row = []
        df = comm_use_df.loc[i]
        row.append(df["paper_id"])
        abstract = str(df["abstract"])[8:] ## 1st 8 chars contain abstract word
        abs_corpus = format_corpus(nltk.sent_tokenize(abstract))
        abs_wordfreq = word_frequencies(abs_corpus)
#         row.append(abs_wordfreq)
        
        csv_df["BOW abstract"] = str(abs_wordfreq)
        text = str(df["text"]) ## 1st 8 chars contain abstract word
        text_corpus = format_corpus(nltk.sent_tokenize(text))
        text_wordfreq = word_frequencies(text_corpus)
#         row.append(text_wordfreq)
        csv_df["BOW text"] = str(text_wordfreq)
    print(csv_df)


# In[ ]:


comm_use_df["BOW abstract"] = ""
comm_use_df["BOW text"] = ""
make_bow_csv(comm_use_df,"filename")


# In[ ]:


comm_use_df.to_csv('BOW_comm_use.csv', index=False)


# In[ ]:


non_comm_use_df = pd.read_csv("/kaggle/input/cord-19-eda-parse-json-and-generate-clean-csv/clean_noncomm_use.csv")


# In[ ]:


non_comm_use_df["BOW abstract"] = ""
non_comm_use_df["BOW text"] = ""
make_bow_csv(non_comm_use_df,"filename")


# In[ ]:


non_comm_use_df.to_csv('BOW_non_comm_use.csv', index=False)


# In[ ]:




