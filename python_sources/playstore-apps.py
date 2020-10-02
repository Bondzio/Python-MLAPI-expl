#!/usr/bin/env python
# coding: utf-8

# ## Load the Libraries

# In[ ]:



import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

import cufflinks as cf
import plotly.offline
import pandas_profiling
from plotly.offline import iplot, init_notebook_mode

import plotly.plotly as py
import plotly.graph_objs as go

import pprint

from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import json
import re, string, unicodedata
from bs4 import Comment
from collections import OrderedDict
from wordcloud import WordCloud

import os
print(os.listdir("../input"))


# In[ ]:


cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)
init_notebook_mode(connected=True)


# ## Import the Data

# In[ ]:


apps = pd.read_csv("../input/googleplaystore.csv")
reviews = pd.read_csv("../input/googleplaystore_user_reviews.csv")


# ## EDA

# #### Let us first see the apps on the Google Play store

# In[ ]:


apps.head()


# In[ ]:


apps.shape


# In[ ]:


apps.isnull().sum()


# #### Removing the duplicated rows 

# In[ ]:


apps = apps.drop_duplicates(['App'],keep='last')


# #### few of the apps does not have any ratings

# #### Top Rated Apps

# In[ ]:


trace2 = go.Bar(
    x=apps.sort_values(['Rating'],ascending=False)['App'][:30],
    y=apps.sort_values(['Rating'],ascending=False)['Rating'][:30],
    name='Top 30 apps'
)

d = [trace2]
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=d, layout=layout)
iplot(fig)


# In[ ]:


apps.sort_values(['Rating'],ascending=False)[['App','Rating']][:30]


# #### Seems like the app 'Life Made WI-Fi Touchscreen Photo Frame' has incorrect ratings. Assuming 5 is the higest rating we will change any rating above 5 to 5.

# In[ ]:


apps['Rating'] = apps['Rating'].apply(lambda x : 5 if x > 5 else x)


# In[ ]:


trace2 = go.Bar(
    x=apps.sort_values(['Rating'],ascending=False)['App'][:30],
    y=apps.sort_values(['Rating'],ascending=False)['Rating'][:30],
    name='Top 30 apps'
)

d = [trace2]
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=d, layout=layout)
iplot(fig)


# #### Avg and Median of Ratings

# In[ ]:


np.mean(apps['Rating'].mean())


# In[ ]:


np.median(apps['Rating'].mean())


# In[ ]:


apps.Rating.iplot(kind='box')


# In[ ]:


apps.iplot(kind='histogram',columns=['Rating'])


# #### Histogram is a bit skewed towards the right and there are few apps that have ratings less than 3

# #### Most reviewed Apps

# ##### we need to clean and make the scale same for all the values in the column

# In[ ]:


apps.head()


# In[ ]:


apps['Reviews'] = apps['Reviews'].apply(lambda x: float(x[:-1]) * 1000000 if 'M' in x else float(x))


# In[ ]:


trace2 = go.Bar(
    x=apps.sort_values(['Reviews'],ascending=False)['App'][:30],
    y=apps.sort_values(['Reviews'],ascending=False)['Reviews'][:30],
    name='Top Reviewed apps'
)

d = [trace2]
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=d, layout=layout)
iplot(fig)


# #### Facebook and its other applications has the highest reviews

# In[ ]:


np.mean(apps['Reviews'].mean())


# In[ ]:


np.median(apps['Reviews'].mean())


# #### Most installed applications

# In[ ]:


apps['Installs'].unique()


# In[ ]:


apps['Installs'] = apps['Installs'].fillna(0)
apps['Installs'] = apps['Installs'].apply(lambda x: 0 if x == 'Free' else x.replace(',', '')[:-1])


# In[ ]:


apps['Installs'] = apps['Installs'].apply(lambda x: 0 if x == '' else float(x))


# In[ ]:


trace2 = go.Bar(
    x=apps.sort_values(['Installs'],ascending=False)['App'][:30],
    y=apps.sort_values(['Installs'],ascending=False)['Installs'][:30],
    name='Top Installed apps'
)

d = [trace2]
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=d, layout=layout)
iplot(fig)


# ### Reviews v/s Installs

# In[ ]:


apps['Reviews'].corr( apps['Installs'])


# In[ ]:


plt.figure(figsize = (14,12))
sns.regplot(x = 'Reviews', y ='Installs', data = apps)


# #### We can't say more installs lead to more reviews but there is a bit of correlation

# ### Lets see which category dominates the playstore

# In[ ]:


apps['Category'].unique()


# In[ ]:


category = apps.groupby(['Category']).count().reset_index().sort_values(['App'], ascending = False)


trace2 = go.Bar(
    x=category['Category'],
    y=category['App'],
    name='Top Installed apps'
)

d = [trace2]
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=d, layout=layout)
iplot(fig)


# #### Family, Game, Tools dominates the most

# In[ ]:


percent_category = round(category['App'], 2)

print("Category percentual: ")
#print(percent_category/percent_category.sum() * 100,2)

types = round(category['App']/ len(category['App']) * 100,2)

labels = list(category['Category'][:10])
values = list(types[:10].values)

trace1 = go.Pie(labels=labels, values=values, marker=dict(colors=['red']), text=percent_category.values)

layout = go.Layout(title="Percentual of Categories", 
                   legend=dict(orientation="h"));

fig = go.Figure(data=[trace1], layout=layout)
iplot(fig)


# ### Lets see the Content Rating

# In[ ]:


plt.figure(figsize = (14,12))
g1 = sns.countplot(x='Content Rating', data = apps)
g1.set_title("Content Ratings Count", fontsize=20)
g1.set_xlabel("Content Rating", fontsize=15)
g1.set_ylabel("Count", fontsize=15)

plt.show()


# ####  Most applications are for everyone

# ### Free v/s Paid apps

# In[ ]:


type_of_apps = apps.groupby(['Type']).count().reset_index()[['Type','Installs']]


# In[ ]:


pprint.pprint(type_of_apps)


# In[ ]:


type_of_apps = type_of_apps[type_of_apps['Type']!='0']


# In[ ]:


plt.figure(figsize = (12,10))
plt.bar(type_of_apps['Type'],type_of_apps['Installs'])
plt.title("Paid v/s Free installs", fontsize=20)
plt.xlabel("Type", fontsize=15)
plt.ylabel("Count", fontsize=15)

plt.show()


# ## User Reviews

# In[ ]:


reviews.head()


# In[ ]:


reviews.shape


# #### Lets create bag of words for the reviews

# In[ ]:


def remove_non_ascii(words):
        """Remove non-ASCII characters from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
        return new_words

def to_lowercase(words):
        """Convert all characters to lowercase from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = word.lower()
            new_words.append(new_word)
        return new_words

def remove_punctuation(words):
        """Remove punctuation from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words

def replace_numbers(words):
        """Replace all interger occurrences in list of tokenized words with textual representation"""
        p = inflect.engine()
        new_words = []
        for word in words:
            if word.isdigit():
                new_word = p.number_to_words(word)
                new_words.append(new_word)
            else:
                new_words.append(word)
        return new_words

def remove_stopwords(words):
        """Remove stop words from list of tokenized words"""
        new_words = []
        for word in words:
            if word not in stopwords.words('english'):
                new_words.append(word)
        return new_words

def lemmatize_verbs(words):
        """Lemmatize verbs in list of tokenized words"""
        lemmatizer = WordNetLemmatizer()
        lemmas = []
        for word in words:
            lemma = lemmatizer.lemmatize(word, pos='v')
            lemmas.append(lemma)
        return lemmas

def normalize(words):
        words = remove_non_ascii(words)
        words = to_lowercase(words)
        words = remove_punctuation(words)
        #words = replace_numbers(words)
        words = remove_stopwords(words)
        return words


# In[ ]:


get_ipython().run_cell_magic('time', '', '\ndocuments=[]\nfor i in range(reviews.shape[0]):\n            if( pd.isnull(reviews[\'Translated_Review\'][i])==True):\n                continue\n            words = reviews[\'Translated_Review\'][i].split()\n            words = normalize(words)\n            words=" ".join(words)\n            documents.append(words)\n            \n    ')


# In[ ]:


len(documents)


# In[ ]:


#Bag of Words
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 3000)#filter non relevant words #keep max 3000
X=cv.fit_transform(documents).toarray()


# In[ ]:


print(X.shape)


# In[ ]:


words = cv.inverse_transform(X)
from collections import Counter
counts={}
for word in words:
    for w in word:
        if w in counts:
            counts[w] +=1
        else:
            counts[w] = 1
OrderedDict(sorted(counts.items(),reverse=True, key=lambda t: t[1]))


# ### Most common words

# In[ ]:


#Wordcloud
plt.figure(figsize = (16, 10))
wordcloud = WordCloud(background_color="white",width=1000,height=1000,
                max_words=30,relative_scaling=0.5,normalize_plurals=False).generate_from_frequencies(counts)

plt.imshow(wordcloud)
plt.title('Top used words')
plt.axis("off")
plt.show()


# ### Positive vs Negative Sentiments

# In[ ]:


plt.figure(figsize = (16, 10))
g1 = sns.countplot(x='Sentiment', data = reviews)
g1.set_title("Sentiment Analysis", fontsize=20)
g1.set_xlabel("Sentiment", fontsize=15)
g1.set_ylabel("Count", fontsize=15)

plt.show()


# ### Apps that got most neutral, positve and negative sentiments

# In[ ]:


#reviews['Sentiment'] = reviews['Sentiment'].map({'Positive':1,'Negative':0})
sentiments = pd.crosstab(reviews.App, reviews.Sentiment).reset_index()


# In[ ]:


trace2 = go.Bar(
    x=sentiments.sort_values(['Positive'],ascending=False)['App'][:30],
    y=sentiments.sort_values(['Positive'],ascending=False)['Positive'][:30],
    name='Top Reviewed apps'
)

d = [trace2]
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=d, layout=layout)
iplot(fig)


# In[ ]:


trace2 = go.Bar(
    x=sentiments.sort_values(['Negative'],ascending=False)['App'][:30],
    y=sentiments.sort_values(['Negative'],ascending=False)['Negative'][:30],
    name='Top Reviewed apps'
)

d = [trace2]
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=d, layout=layout)
iplot(fig)


# In[ ]:


trace2 = go.Bar(
    x=sentiments.sort_values(['Neutral'],ascending=False)['App'][:30],
    y=sentiments.sort_values(['Neutral'],ascending=False)['Neutral'][:30],
    name='Top Reviewed apps'
)

d = [trace2]
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=d, layout=layout)
iplot(fig)


# ### Avg Sentiment_Polarity and Sentiment_Subjectivity**

# In[ ]:


reviews.groupby(['App']).mean()['Sentiment_Polarity'].nlargest(30).iplot(kind='bar',
                                                                     xTitle='App', yTitle='Sentiment Polarity',
                                                                     title='Apps with most Sentiment_Polarity',colors = 'red')


# In[ ]:


reviews.groupby(['App']).mean()['Sentiment_Subjectivity'].nlargest(30).iplot(kind='bar',
                                                                     xTitle='App', yTitle='Sentiment Subjectivity',
                                                                     title='Apps with most Sentiment Subjectivity',colors = 'green')


# # Next - Prediction

# In[ ]:




