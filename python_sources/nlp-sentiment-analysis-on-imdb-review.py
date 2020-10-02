#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import string
import unidecode

import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

import nltk
from nltk import tokenize
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer

from wordcloud import WordCloud

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.model_selection import train_test_split


# In[ ]:


np.random.seed(42)


# In[ ]:


df = pd.read_csv('../input/imdb-reviews-pt-br.csv')
df.set_index('id', inplace=True)
df['review'] = df['sentiment'].replace(['neg', 'pos'], [0, 1])

df.shape


# In[ ]:


df['sentiment'].value_counts()


# In[ ]:


df.head()


# In[ ]:


df.tail()


# In[ ]:


df['text_pt'] = df['text_pt'].str.lower()
df['text_pt'] = df['text_pt'].apply(lambda text: unidecode.unidecode(text))


# In[ ]:


STOP_WORDS = stopwords.words('portuguese') + list(string.punctuation)

def filter_by_stop_words(text, stop_words=STOP_WORDS):
    tokenizer = tokenize.WordPunctTokenizer()
    stemmer = RSLPStemmer()
    tokens = tokenizer.tokenize(text)
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(tokens)


# In[ ]:


df['text_pt'] = df['text_pt'].apply(filter_by_stop_words)


# In[ ]:


df.sample(n=5)


# In[ ]:


words = ' '.join([text for text in df['text_pt']])


# In[ ]:


word_cloud = WordCloud(collocations=False,
                       width=800,
                       height=500,
                       max_font_size=110,
                       background_color ='white').generate(words)


# In[ ]:


plt.figure(figsize=(10,7))
plt.imshow(word_cloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[ ]:


tokenizer = tokenize.WordPunctTokenizer()
words_tokens = tokenizer.tokenize(words)
words_frequency = nltk.FreqDist(words_tokens)


# In[ ]:


df_words_frequency = pd.DataFrame({
    'word': list(words_frequency.keys()),
    'frequency': list(words_frequency.values())
})

top = df_words_frequency.nlargest(columns='frequency', n=15)

plt.figure(figsize=(12,8))
ax = sns.barplot(data=top, x='word', y='frequency')
ax.set(ylabel='frequency')
plt.show()


# In[ ]:


vectorizer = TfidfVectorizer(lowercase=False, max_features=500, ngram_range=(1,2))
bag_of_words = vectorizer.fit_transform(df['text_pt'])

features = pd.SparseDataFrame(bag_of_words, columns=vectorizer.get_feature_names())
features.shape


# In[ ]:


X = bag_of_words
y = df['review']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)


# In[ ]:


dummy_classifier = DummyClassifier()
dummy_classifier.fit(X_train, y_train)
dummy_classifier.score(X_test, y_test)


# In[ ]:


model = LogisticRegression(solver='lbfgs')
model.fit(X_train, y_train)
model.score(X_test, y_test)


# In[ ]:


weights = pd.DataFrame(
    model.coef_[0].T,
    index=vectorizer.get_feature_names()
)


# In[ ]:


weights.nlargest(10, 0).T


# In[ ]:


weights.nsmallest(10, 0).T

