#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import os
os.chdir('../input')
from nltk.corpus import stopwords

def process_words(file_url, words, titles_read):
    with open(file_url) as f:
        f = f.read()
        these_regex="<title.*?>(.+?)</title>"
        pattern=re.compile(these_regex)
        titles=re.findall(pattern,f)
        try:
            titles.remove('South China Morning Post')
            titles.remove('South China Morning Post')
        except:
            pass
    for t in titles:
        if t in titles_read:
            continue
        else:
            titles_read.add(t)
        t = t.split(" ")
        for w in t:
            if w not in stopwords.words('english'):
                words.append(w)

titles_read = set()
all_words = []
for xml_file in ["sport.xml","china.xml","europe.xml","hong_kong.xml", "news.xml", "food.xml","tech.xml","travel.xml"]:
    process_words(xml_file, all_words, titles_read)


# In[ ]:


word_count = {}
for word in all_words:
    word_count[word] = word_count.get(word, 0) + 1


# In[ ]:


# word_count
# Partial View of the first 20 word count
dict(list(word_count.items())[0:20])


# In[ ]:


import nltk
allWords = nltk.tokenize.word_tokenize(' '.join(all_words))


# In[ ]:


# allWords

# Partial View of the first 20 Words
allWords[0:20]


# In[ ]:


allWordDist = nltk.FreqDist(w.lower() for w in allWords)


# In[ ]:


allWordDist.most_common(50)


# In[ ]:


feature_words = ['china', 'us', 'chinese', 'hong', 'kong', 'trade', 'chef', 'tech', 'war', 'trump', 'british', 'uk', 'recipes', 'world', 'beijing', 'police', 'donald', 'ambassador', 'huawei', 'classic', 'championship']


# In[ ]:


all_titles = sorted(titles_read)


# In[ ]:


title_vectors = []


# In[ ]:


for current_title in all_titles:
    current_vector = []
    for feature_word in feature_words:
        feature_word_present = feature_word in current_title
        current_vector.append(feature_word_present)
    title_vectors.append(current_vector)


# In[ ]:


#title_vectors


# In[ ]:


c = 0
for i in title_vectors:
    g = [not k for k in i]
    if all(g):
        c += 1
print(c)


# In[ ]:


len(feature_words)


# In[ ]:




