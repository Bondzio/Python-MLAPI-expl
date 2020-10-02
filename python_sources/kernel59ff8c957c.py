#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as py
color= sns.color_palette()
import plotly.graph_objs as go
py.init_notebook_mode(connected=True)
import plotly.tools as tls
import warnings
warnings.filterwarnings('ignore')
import os 
os.listdir("../input")


# In[ ]:


df = pd.read_csv('../input/grammar-and-online-product-reviews/GrammarandProductReviews.csv')
df.head()


# In[ ]:


df.shape


# In[ ]:


df.dtypes


# In[ ]:


df.isnull().sum()


# In[ ]:


df=df.dropna(subset=['reviews.text'])


# In[ ]:


cnt_srs = df['reviews.rating'].value_counts().head()
trace = go.Bar(
    y = cnt_srs.index[::-1],
    x=cnt_srs.values[::-1],
    orientation = 'h',
    marker = dict(
        color=cnt_srs.values[::-1],
        colorscale = 'Blues',
        reversescale = True
    ),
)

layout = dict(
    title='Ratings distribution',
)
data = [trace]
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename="Ratings")


# In[ ]:


df['reviews_length']=df['reviews.text'].apply(len)


# In[ ]:


sns.set(font_scale=2.0)

g = sns.FacetGrid(df, col='reviews.rating', size=5)
g.map(plt.hist, 'reviews_length')


# In[ ]:


df['reviews.didPurchase'].fillna("Reviews N/A", inplace=True)


# In[ ]:


plt.figure(figsize=(10, 8))
ax = sns.countplot(df['reviews.didPurchase'])
ax.set_xlabel(xlabel="People's Reviews", fontsize=17)
ax.set_ylabel(ylabel='No. of Reviews', fontsize=17)
ax.axes.set_title('Genuine No. of Reviews', fontsize=17)
ax.tick_params(labelsize=13)


# In[ ]:


sns.set(font_scale=1.4)
plt.figure(figsize=(10, 5))
sns.heatmap(df.corr(), cmap='coolwarm', annot=True, linewidth=.5)


# In[ ]:


from sklearn.model_selection import cross_val_score
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer

all_text =df['reviews.text']
train_text= df['reviews.text']
y=df['reviews.rating']


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
train_word_feature = word_vectorizer.transform(train_text)


# In[ ]:


char_vectorizer=TfidfVectorizer(
    sublinear_tf=True,
    strip_accents='unicode',
    analyzer='char',
    stop_words='english',
    ngram_range=(2, 6),
    max_features=50000)
char_vectorizer.fit(all_text)
train_char_features= char_vectorizer.transform(train_text)

train_features =hstack([train_char_features, train_word_feature])


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(train_features, y, test_size=0.3, random_state=10)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier

classifier = RandomForestClassifier()
classifier.fit(X_train, y_train)
preds=classifier.predict(X_test)


# In[ ]:


from sklearn.metrics import accuracy_score


# In[ ]:


import xgboost as xgb


# In[ ]:


xgb=xgb.XGBClassifier()


# In[ ]:


xgb.fit(X_train, y_train)


# In[ ]:


preds2 = xgb.predict(X_test)


# In[ ]:


xgb_accuracy=accuracy_score(preds2, y_test)


# In[ ]:


rf_accuracy=accuracy_score(preds,y_test)


# In[ ]:


print("Random Forest Model accuracy", rf_accuracy)


# In[ ]:


print("XGBoost Model accuracy", xgb_accuracy)


# In[ ]:


df['sentiment'] = df['reviews.rating']<4


# In[ ]:


from sklearn.model_selection import train_test_split
train_text, test_text, train_y, test_y = train_test_split(df['reviews.text'], df['sentiment'], test_size=0.2)


# In[ ]:


from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM
from keras.utils.np_utils import to_categorical
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
from keras.optimizers import Adam


# In[ ]:


MAX_NB_WORDS = 20000

# get the raw text data
texts_train = train_text.astype(str)
texts_test = test_text.astype(str)

# finally, vectorize the text samples into a 2D integer tensor
tokenizer = Tokenizer(nb_words=MAX_NB_WORDS, char_level=False)
tokenizer.fit_on_texts(texts_train)
sequences = tokenizer.texts_to_sequences(texts_train)
sequences_test = tokenizer.texts_to_sequences(texts_test)

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))


# In[ ]:


MAX_SEQUENCES_LENGTH = 200

x_train = pad_sequences(sequences, maxlen = MAX_SEQUENCES_LENGTH)
x_test = pad_sequences(sequences_test, maxlen=MAX_SEQUENCES_LENGTH)
print('shape of data tensor:', x_train.shape)
print('shape of data test tensor:', x_test.shape)


# In[ ]:


model = Sequential()
model.add(Embedding(MAX_NB_WORDS, 128))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2, input_shape=(1,)))
model.add(Dense(1, activation='sigmoid'))


# In[ ]:


model.compile(loss='binary_crossentropy',
             optimizer = 'adam',
             metrics = ['accuracy'])


# In[ ]:


model.fit(x_train, train_y,
          batch_size=128,
          epochs=10,
          validation_data=(x_test, test_y))


# In[ ]:




