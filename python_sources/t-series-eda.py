#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import plotly.graph_objs as go
from wordcloud import WordCloud,STOPWORDS 
import spacy
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stopWords = stopwords.words('english')
RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
get_ipython().run_line_magic('matplotlib', 'inline')
stopwords = set(STOPWORDS)
get_ipython().system('pip install spacy-langdetect')
from spacy_langdetect import LanguageDetector
nlp = spacy.load('en_core_web_lg', parse=True, tag=True, entity=True)
language_detector = LanguageDetector()
nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)
import plotly.express as px


# In[ ]:


tseries = pd.read_csv('../input/pewdiepie-vs-tseries/tseries_ytstats.csv')
tseries.head()


# # Number of null values

# In[ ]:


tseries.isnull().sum()


# In[ ]:


tseries.dropna(inplace=True)
tseries.reset_index(drop=True)
tseries['durationSec'] = tseries['durationSec'].astype(int)
tseries['publishedAtSQL'] = tseries['publishedAtSQL'].apply(lambda x:x[:10])


# # **Numerical Features Ranking of the T-Series Video Library**
# ## Note - as of May 17th 2020
# ### 1. Views
# ### 2. Likes
# ### 3. Dislikes
# ### 4. Comments
# ### 5. Duration of the Video

# # Top 10 Most Viewed Videos

# In[ ]:


tseries.loc[tseries['viewCount'].nlargest(10).index][['videoTitle','viewCount']]


# # Top 10 Liked Videos

# In[ ]:


tseries.loc[tseries['likeCount'].nlargest(10).index][['videoTitle','likeCount']]


# # Top 10 Disliked Videos

# In[ ]:


tseries.loc[tseries['dislikeCount'].nlargest(10).index][['videoTitle','dislikeCount']]


# # Top 10 most commented videos

# In[ ]:


tseries.loc[tseries['commentCount'].nlargest(10).index][['videoTitle','commentCount']]


# # Top 10 longest videos

# In[ ]:


tseries.loc[tseries['durationSec'].nlargest(10).index][['videoTitle','durationSec']]


# In[ ]:


title_wc = ' '.join(titles for titles in tseries['videoTitle'].tolist())
wordcloud = WordCloud(background_color='white',stopwords=stopwords).generate(title_wc)
figure(figsize=(20, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# ### **Stop words particular to T-Series Context**
# 'tseries', 'song', 'songs', 'video', 'lyrical', 'music', 'remix', 'hai'

# In[ ]:


stopWords = stopWords + ['tseries', 'song', 'songs', 'video', 'lyrical', 'music', 'remix', 'hai']


# In[ ]:


def clean_text(text):
    text = re.sub('#', '', text)  # remove hashtags
    text = re.sub('@\S+', '', text)  # remove mentions
    text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-/:;<=>?@[\]^_`{|}~"""), '', text)  # remove punctuations
    text = re.sub('\s+', ' ', text)  # remove extra whitespace
    text = RE_EMOJI.sub('',text)
    words = word_tokenize(text)
    clean_text = []
    for word in words:
        if word not in stopWords:
            clean_text.append(word)
    cln_txt = ' '.join(clean_text)
    return cln_txt.lower()

tseries['Clean Title'] = tseries['videoTitle'].apply(clean_text)
tseries.head()


# In[ ]:


def find_persons(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ == 'PERSON']

tseries['Personalities'] = tseries['Clean Title'].apply(find_persons)
tseries.head()


# In[ ]:


dishes = ' '.join(dish for dish_list in tseries['Personalities'].tolist() for dish in dish_list)
wordcloud = WordCloud(background_color='white',stopwords=stopWords).generate(dishes)
figure(figsize=(20, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[ ]:


fig = px.histogram(tseries, x="publishedAtSQL")
fig.show()


# In[ ]:


fig = go.Figure(data=[go.Bar(
                x = tseries['videoCategoryLabel'].value_counts()[:10].index.tolist(),
                y = tseries['videoCategoryLabel'].value_counts()[:10].values.tolist())])

fig.show()


# In[ ]:




