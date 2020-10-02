#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import re

import logging
import nltk
import string
import collections
from collections import Counter
import wordcloud
from wordcloud import WordCloud


# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


pd.set_option('display.max_colwidth',200)


# In[ ]:


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s',datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger(__name__)
logger.info('Logger initialised...')


# In[ ]:


train_df=pd.read_csv('/kaggle/input/nlp-getting-started/train.csv')


# ## EDA

# In[ ]:


train_df.shape


# In[ ]:


train_df['target'].value_counts()


# In[ ]:


sns.countplot(train_df['target'])


# In[ ]:


logger.info("% of samples where keyword column is 0")
len(train_df[train_df['keyword'].isna()])*100/len(train_df)


# In[ ]:


logger.info("% of samples where location column is 0")
len(train_df[train_df['location'].isna()])*100/len(train_df)


# In[ ]:


sns.barplot(train_df['keyword'].value_counts()[:20].values,train_df['keyword'].value_counts()[:20].index,orient="H")


# In[ ]:


## Keyword chart when target is 1
sns.barplot(train_df[train_df['target']==1]['keyword'].value_counts()[:20].values,train_df[train_df['target']==1]['keyword'].value_counts()[:20].index,orient="H")


# In[ ]:


sns.barplot(train_df['location'].value_counts()[:20].values,            train_df['location'].value_counts()[:20].index,orient="H")


# In[ ]:


## Location chart when target is 1
sns.barplot(train_df[train_df['target']==1]['location'].value_counts()[:20].values,            train_df[train_df['target']==1]['location'].value_counts()[:20].index,orient="H")


# ## Data Preprocessing

# ### Cleaning text
# * Converting Text Lowercase
# * Tokenization
# * Removing Punctuatons
# * Stop Words removal
# * Stemmning
# * Lemmatization
# * POS Tagging

# #### 1. Make text lowercase

# In[ ]:


def to_lowercases(x):
    return x.lower()

train_df['text']=train_df['text'].apply(to_lowercases)


# In[ ]:


train_df.head(1)


# #### Clean text

# In[ ]:


def clean_text(x):
    text = re.sub('(\d+)','',x)    
    return text

train_df['text'] = train_df['text'].apply(clean_text)

train_df.head(2)


# #### Remove URL

# In[ ]:


def remove_url(x):
    text = re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})\/([a-zA-Z0-9_]+]*)',' ',x)
    return text

train_df['text'] = train_df['text'].apply(remove_url)


# #### Remove Punctuations

# In[ ]:


def remove_punct(x):
    text_without_puct = [t for t in x if t not in string.punctuation]
    text_without_puct = ''.join(text_without_puct)
    return text_without_puct

train_df['text'] = train_df['text'].apply(remove_punct)


# #### Tokenization

# In[ ]:


def get_tokens(x):
    tokens = nltk.word_tokenize(x)
    return tokens

train_df['text'] = train_df['text'].apply(get_tokens)


# #### Remove Stop Words

# In[ ]:


stop_words = nltk.corpus.stopwords.words('english')

def remove_stop_words(x):
    text_without_stopwords = [t for t in x if t not in stop_words]
    
    return text_without_stopwords

train_df['text'] = train_df['text'].apply(remove_stop_words)


# #### Lemmatization

# In[ ]:


from nltk.stem import WordNetLemmatizer
lemma = WordNetLemmatizer()

def lemmatization(x):
    try:
        lemmatized = np.vectorize(lemma.lemmatize)(x)
        return lemmatized
    except ValueError:
        return []
    
train_df['text_lemm'] = train_df['text'].apply(lemmatization)


# In[ ]:


train_df.head(2)


# ### Text Analysis

# In[ ]:


from nltk import FreqDist


# In[ ]:


fdist = FreqDist()
def freq_dist(x):
    for word in x:
        fdist[word]+=1
    
    return fdist


# In[ ]:


train_df['text_lemm'].apply(freq_dist)[1]


# In[ ]:


fdist = FreqDist()
def freq_dist(x):
    for word in x:
        fdist[word]+=1
    
    return fdist


# In[ ]:


most_common = Counter(train_df['text_lemm'].apply(freq_dist)[1]).most_common(50)
l=[]
for k,v in most_common:
    l.append(k.replace("\'",''))


# In[ ]:


wordcloud = WordCloud(background_color='white',
        max_words=200,
        max_font_size=40, 
        scale=3,
        random_state=1).generate(str(l))
plt.figure(figsize=(10,10))
plt.imshow(wordcloud)


# #### Bigrams and Trigrams

# In[ ]:


fdist = nltk.FreqDist()
def bigrams(x):
    y = list(nltk.bigrams(x))
    for word in y:
        fdist[word]+= 1
    
    return fdist


# In[ ]:


bigrams = train_df['text_lemm'].apply(bigrams)


# In[ ]:


Counter(fdist).most_common(20)


# In[ ]:


fdist = nltk.FreqDist()
def trigrams(x):
    y = list(nltk.trigrams(x))
    for word in y:
        fdist[word]+= 1
    
    return fdist


# In[ ]:


trigrams = train_df['text_lemm'].apply(trigrams)


# In[ ]:


Counter(fdist).most_common(20)


# #### Bag of Words

# In[ ]:


l = []
for i in range(len(train_df)):
    l.append(' '.join(train_df.loc[i,'text_lemm']))


# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer

countvect = CountVectorizer()

countvect_text = countvect.fit_transform(l)

countvect_text.get_shape()


# #### TFIDF

# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer

tf = TfidfVectorizer()
tf_text = tf.fit_transform(l)
tf_text.shape


# #### Glove Embeddings

# In[ ]:


f = open('../input/glove-100d-word-embeddings/glove.6B.100d.txt')
embeddings = {}
for line in f:
    word = line.split(' ')
    embeddings[word[0]] = np.asarray(word[1:])
f.close()


# In[ ]:


labels = train_df.target.values


# In[ ]:


from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical,plot_model


# In[ ]:


tokenizer = Tokenizer(num_words=10000)

tokenizer.fit_on_texts(l)

sequences = tokenizer.texts_to_sequences(l)

word_index = tokenizer.word_index


# In[ ]:


print("Unique Tokens %s"%len(tokenizer.word_index))


# In[ ]:


data = pad_sequences(list(sequences),maxlen=20,truncating='post',padding='post')


# In[ ]:


indices = np.arange(data.shape[0])
np.random.shuffle(indices)

data = data[indices]
labels_y = labels[indices]

nb_validation_sample = int(.15*data.shape[0])


# In[ ]:


x_train = data[:-nb_validation_sample]
y_train = labels_y[:-nb_validation_sample].reshape(-1,1)
x_test = data[-nb_validation_sample:]
y_test = labels_y[-nb_validation_sample:].reshape(-1,1)


# In[ ]:


embedding_matrix = np.zeros((len(word_index) + 1, 100))


# In[ ]:


for word,i in word_index.items():
    try:
        vector = embeddings[word]
        if vector is not None:
            # words not found in embedding index will be all-zeros.
            embedding_matrix[i] = vector
    except KeyError:
        continue


# In[ ]:


from tensorflow.keras import backend

from tensorflow.keras.layers import Input,Dense,Activation,Embedding,Flatten,LSTM,Dropout,SpatialDropout1D
from tensorflow.keras.models import Model,Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping,ModelCheckpoint


# In[ ]:


inp = Input(shape=(x_train.shape[1],))
emb = Embedding(len(embedding_matrix),
                100,
                weights=[embedding_matrix],
                trainable=False,
               input_length=20)(inp)

#out = Flatten()(emb)
out = SpatialDropout1D(rate=0.2)(emb)
out = LSTM(100)(out)
out = Dropout(rate=0.2)(out)
#out = Dense(20,activation='relu')(out)
out = Dense(1,activation='sigmoid')(out)
adam = Adam(learning_rate=.001)

model = Model(inputs=[inp],outputs=[out])


# In[ ]:


model.compile(loss='binary_crossentropy',optimizer=adam,metrics=['accuracy'])


# In[ ]:


model.fit(x_train,y_train,verbose=1,
          batch_size=4,
          epochs=10,
          validation_data=[x_test,y_test])


# In[ ]:


model.summary()


# In[ ]:




