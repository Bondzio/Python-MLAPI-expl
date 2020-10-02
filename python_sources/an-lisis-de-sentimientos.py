#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt 
from stop_words import get_stop_words
from collections import Counter
from nltk.tokenize import RegexpTokenizer 
import re

import os
print(os.listdir("../input"))


# In[ ]:


def wc(data,bgcolor,title):
    plt.figure(figsize = (100,100))
    wc = WordCloud(background_color = bgcolor, max_words = 1000,  max_font_size = 50)
    wc.generate(' '.join(data))
    plt.imshow(wc)
    plt.axis('off')


# In[ ]:


dataTexto=pd.read_csv('../input/datosAnalisisSentimientos.csv',encoding = "ISO-8859-1")


# In[ ]:


dataTexto.head()


# In[ ]:


desc_lower = dataTexto['DESCRIPCION'].str.lower().str.cat(sep=' ')


# In[ ]:


desc_lower


# In[ ]:


desc_remove_pun = re.sub('[^A-Za-z]+', ' ', desc_lower)


# In[ ]:


desc_remove_pun 


# In[ ]:


stop_words = list(get_stop_words('spanish'))        


# In[ ]:


stop_words


# In[ ]:


import nltk
from nltk.corpus import stopwords
nltk_words = list(stopwords.words('spanish')) 


# In[ ]:


nltk_words


# In[ ]:


stop_words.extend(nltk_words)


# In[ ]:


stop_words


# In[ ]:


from nltk import sent_tokenize, word_tokenize
word_tokens = word_tokenize(desc_remove_pun)


# In[ ]:


filtered_sentence = [w for w in word_tokens if not w in stop_words]


# In[ ]:


filtered_sentence = []
for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)


# In[ ]:


without_single_chr = [word for word in filtered_sentence if len(word) > 2]


# In[ ]:


cleaned_data_title = [word for word in without_single_chr if not word.isnumeric()]       


# In[ ]:


top_N = 1000
word_dist_desc  = nltk.FreqDist(cleaned_data_title)
rslt_desc = pd.DataFrame(word_dist_desc.most_common(top_N),
                    columns=['Word', 'Frequency'])


# In[ ]:


import seaborn as sns
plt.figure(figsize=(10,10))
sns.set_style("whitegrid")
ax = sns.barplot(x="Word", y="Frequency", data=rslt_desc.head(7))


# In[ ]:


from wordcloud import WordCloud
wc(cleaned_data_title,'black','Frequent Words' )


# In[ ]:


def explain_text_entities(text):
    doc = nlp(text)
    for ent in doc.ents:
        print(f'Entity: {ent}, Label: {ent.label_}, {spacy.explain(ent.label_)}')


# In[ ]:


explain_text_entities(dataTexto['DESCRIPCION'])

