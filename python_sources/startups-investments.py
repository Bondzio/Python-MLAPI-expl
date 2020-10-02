#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#codes from Rodrigo Lima  @rodrigolima82
from IPython.display import Image
Image(url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTlif8SG5U1SZ-8kajuOTaa4eV_6djX2qdNayeYzJBuMx7GsO3U',width=400,height=400)


# boardofinnovation.com

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import feature_extraction, linear_model, model_selection, preprocessing
import plotly.graph_objs as go
import plotly.offline as py

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


df = pd.read_csv('../input/startup-investments-crunchbase/investments_VC.csv', encoding='ISO-8859-2')


# In[ ]:


df.head()


# In[ ]:


df.dtypes


# In[ ]:


print(df.shape)


# In[ ]:


df.isnull().sum()


# Drop the rows having null values

# In[ ]:


df = df.dropna(subset=['founded_at', 'founded_month', 'state_code', 'founded_quarter', 'founded_year','country_code'])


# In[ ]:


from wordcloud import WordCloud, STOPWORDS
stopwords = set(STOPWORDS)

def show_wordcloud(data, title = None):
    wordcloud = WordCloud(
        background_color='black',
        stopwords=stopwords,
        max_words=200,
        max_font_size=40, 
        scale=3,
        random_state=1 # chosen at random by flipping a coin; it was heads
).generate(str(data))

    fig = plt.figure(1, figsize=(15, 15))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()

show_wordcloud(df['name'])


# I read DENTIST. That's what I am, a DDS.

# In[ ]:


cnt_srs = df['name'].value_counts().head()
trace = go.Bar(
    y=cnt_srs.index[::-1],
    x=cnt_srs.values[::-1],
    orientation = 'h',
    marker=dict(
        color=cnt_srs.values[::-1],
        colorscale = 'Blues',
        reversescale = True
    ),
)

layout = dict(
    title='Names distribution',
    )
data = [trace]
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename="Names")


# In[ ]:


df['name_lenght']=df['name'].apply(len)


# In[ ]:


plt.figure(figsize=(10,8))
ax=sns.countplot(df['region'])
ax.set_xlabel(xlabel="region",fontsize=17)
ax.set_ylabel(ylabel='No. of Regions',fontsize=17)
ax.axes.set_title('Regions',fontsize=17)
ax.tick_params(labelsize=13)


# In[ ]:


sns.set(font_scale=1.4)
plt.figure(figsize = (10,5))
sns.heatmap(df.corr(),cmap='coolwarm',annot=True,linewidths=.5)


# In[ ]:


from sklearn.model_selection import cross_val_score
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer

all_text=df['name']
train_text=df['name']
y=df['region']


# In[ ]:


word_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    strip_accents='unicode',
    analyzer='word',
    token_pattern=r'\w{1,}',
    stop_words='english',
    ngram_range=(1, 1),
    max_features=10000)
word_vectorizer.fit(all_text)
train_word_features = word_vectorizer.transform(train_text)


# In[ ]:


char_vectorizer = TfidfVectorizer(
    sublinear_tf=True,
    strip_accents='unicode',
    analyzer='char',
    stop_words='english',
    ngram_range=(2, 6),
    max_features=50000)
char_vectorizer.fit(all_text)
train_char_features = char_vectorizer.transform(train_text)

train_features = hstack([train_char_features, train_word_features])


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(train_features, y,test_size=0.3,random_state=101)


# In[ ]:


import xgboost as xgb


# In[ ]:


xgb=xgb.XGBClassifier()


# In[ ]:


#xgb.fit(X_train,y_train)

