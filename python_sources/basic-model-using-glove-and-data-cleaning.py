#!/usr/bin/env python
# coding: utf-8

# # Import Libraries

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from nltk.corpus import stopwords
from nltk.util import ngrams
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict
from collections import  Counter
plt.style.use('ggplot')
stop=set(stopwords.words('english'))
import re
from nltk.tokenize import word_tokenize
import gensim
import string
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from tqdm import tqdm
from keras.models import Sequential
from keras.layers import Embedding,LSTM,Dense,SpatialDropout1D
from keras.initializers import Constant
from sklearn.model_selection import train_test_split
from keras.optimizers import Adam


# # Import Data

# In[ ]:


import os
tweet= pd.read_csv('../input/nlp-getting-started/train.csv')
test=pd.read_csv('../input/nlp-getting-started/test.csv')
tweet.head(3)


# In[ ]:


df=pd.concat([tweet,test], sort = False)
df.shape


# In[ ]:


def remove_URL(text):
    url = re.compile(r'https?://\S+|www\.\S+')
    return url.sub(r'',text)


# In[ ]:


df['text']=df['text'].apply(lambda x : remove_URL(x))


# In[ ]:


def remove_html(text):
    html=re.compile(r'<.*?>')
    return html.sub(r'',text)


# In[ ]:


df['text']=df['text'].apply(lambda x : remove_html(x))


# In[ ]:


def remove_emoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


# In[ ]:


df['text']=df['text'].apply(lambda x: remove_emoji(x))


# In[ ]:


def remove_punct(text):
    table=str.maketrans('','',string.punctuation)
    return text.translate(table)


# In[ ]:


df['text']=df['text'].apply(lambda x : remove_punct(x))


# In[ ]:


#!pip install pyspellchecker


# In[ ]:


#from spellchecker import SpellChecker


# In[ ]:


#spell = SpellChecker()
def correct_spellings(text):
    corrected_text = []
    misspelled_words = spell.unknown(text.split())
    for word in text.split():
        if word in misspelled_words:
            corrected_text.append(spell.correction(word))
        else:
            corrected_text.append(word)
    return " ".join(corrected_text)


# In[ ]:


#Not working - Need to check
#df['text']=df['text'].apply(lambda x : correct_spellings(x)#)


# ## Globe Vectorization

# In[ ]:


def create_corpus(df):
    corpus=[]
    for tweet in tqdm(df['text']):
        words=[word.lower() for word in word_tokenize(tweet) if((word.isalpha()==1) & (word not in stop))]
        corpus.append(words)
    return corpus


# In[ ]:


corpus=create_corpus(df)


# In[ ]:


embedding_dict={}
with open('../input/glove-global-vectors-for-word-representation/glove.6B.100d.txt','r') as f:
    for line in f:
        values=line.split()
        word=values[0]
        vectors=np.asarray(values[1:],'float32')
        embedding_dict[word]=vectors
f.close()


# In[ ]:


MAX_LEN=50
tokenizer_obj=Tokenizer()
tokenizer_obj.fit_on_texts(corpus)
sequences=tokenizer_obj.texts_to_sequences(corpus)

tweet_pad=pad_sequences(sequences,maxlen=MAX_LEN,truncating='post',padding='post')


# In[ ]:


word_index=tokenizer_obj.word_index
print('Number of unique words:',len(word_index))


# In[ ]:


num_words=len(word_index)+1
embedding_matrix=np.zeros((num_words,100))

for word,i in tqdm(word_index.items()):
    if i > num_words:
        continue
    
    emb_vec=embedding_dict.get(word)
    if emb_vec is not None:
        embedding_matrix[i]=emb_vec


# ## Base Model

# In[ ]:


model=Sequential()

embedding=Embedding(num_words,100,embeddings_initializer=Constant(embedding_matrix),
                   input_length=MAX_LEN,trainable=False)

model.add(embedding)
model.add(SpatialDropout1D(0.2))
model.add(LSTM(64, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(1, activation='sigmoid'))


optimzer=Adam(learning_rate=1e-5)

model.compile(loss='binary_crossentropy',optimizer=optimzer,metrics=['accuracy'])


# In[ ]:


model.summary()


# In[ ]:


train=tweet_pad[:tweet.shape[0]]
test=tweet_pad[tweet.shape[0]:]


# In[ ]:


X_train,X_test,y_train,y_test=train_test_split(train,tweet['target'].values,test_size=0.15)
print('Shape of train',X_train.shape)
print("Shape of Validation ",X_test.shape)


# In[ ]:


history=model.fit(X_train,y_train,batch_size=4,epochs=15,validation_data=(X_test,y_test),verbose=2)


# In[ ]:


sample_sub=pd.read_csv('../input/nlp-getting-started/sample_submission.csv')


# In[ ]:


y_pre=model.predict(test)
y_pre=np.round(y_pre).astype(int).reshape(3263)
sub=pd.DataFrame({'id':sample_sub['id'].values.tolist(),'target':y_pre})
sub.to_csv('submission.csv',index=False)


# In[ ]:


sub.head()

