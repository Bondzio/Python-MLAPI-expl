#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import string
import heapq
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
import nltk
import keras
from keras.models import Sequential 
from keras.preprocessing.text import one_hot
from keras.layers import Dense,Dropout,LSTM,Embedding
from keras.preprocessing.sequence import pad_sequences


# In[ ]:


data = pd.read_csv('../input/twitter-airline-sentiment/Tweets.csv')
data.head()


# In[ ]:


len(data)


# In[ ]:


data.isna().sum()


# In[ ]:


plt.style.use('seaborn')
sns.countplot(data=data,x='airline_sentiment')


# In[ ]:


data.columns


# In[ ]:


plt.style.use('dark_background')
sns.countplot(data=data,x='airline')


# In[ ]:


sns.set(rc={'figure.figsize':(25,15)})
sns.countplot(data=data,x='negativereason')


# In[ ]:


data = data[['text','airline_sentiment']]
data.head()


# In[ ]:


data['text'][5]


# In[ ]:


def remove_stopwords(inp_text):
    stop = nltk.corpus.stopwords.words('english')
    punc = string.punctuation
    stop.append(punc)
    whitelist = ["n't", "not", "no"]
    clean_words = []
    words = nltk.word_tokenize(inp_text)
    for word in words:
        if word not in stop or word not in whitelist and len(word)>1:
            clean_words.append(word)
    return " ".join(clean_words)


# In[ ]:


remove_stopwords(data['text'][5])


# In[ ]:


def remove_mentions(input_text):
        return re.sub(r'@ \w+', '', input_text)


# In[ ]:


data.text = data.text.apply(remove_stopwords).apply(remove_mentions)
data.head()


# In[ ]:


word2count = {}

for i in range(len(data['text'])):
    words = nltk.word_tokenize(data['text'][i])
    
    for word in words:
        if word not in word2count.keys():
            word2count[word] = 1
        else:
            word2count[word] += 1


# In[ ]:


word2count


# In[ ]:


print("Vocabluray of our corpus is: {}".format(len(word2count)))


# In[ ]:


word_freq = heapq.nlargest(10000,word2count,key=word2count.get)
word_freq[:15]


# In[ ]:


vocab_size = len(word_freq)


# In[ ]:


onehot_text = []
for sentences in data['text']:
    Z = one_hot(sentences,vocab_size)
    onehot_text.append(Z)


# In[ ]:


onehot_text[:5]


# In[ ]:


length = 20
embedded_sents = pad_sequences(onehot_text,padding='pre',maxlen=length)


# In[ ]:


embedded_sents[:5]


# In[ ]:


labels = data['airline_sentiment']
labels


# In[ ]:


lb = LabelBinarizer()


# In[ ]:


labels = lb.fit_transform(labels)
labels


# In[ ]:


X = embedded_sents
y = labels


# In[ ]:


X = np.asarray(X)
y = np.asarray(y)


# In[ ]:





# In[ ]:


len(X)


# In[ ]:


len(y)


# In[ ]:


X_train = X[:13000]
y_train = y[:13000]


# In[ ]:


X_test = X[13000:]
y_test = y[13000:]


# In[ ]:


X_train.shape


# In[ ]:


y_train.shape


# In[ ]:


X_test.shape


# In[ ]:


y_test.shape


# In[ ]:


X_training,X_valid,y_training,y_valid = train_test_split(X_train,y_train,test_size=0.2)


# In[ ]:


X_training.shape


# In[ ]:


X_valid.shape


# In[ ]:


model = Sequential()


# Traditional Deep Learning Model

# In[ ]:


model.add(Dense(512,activation='relu',input_shape=(20,)))
model.add(Dropout(0.2))
model.add(Dense(256,activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(128,activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(3,activation='softmax'))


# In[ ]:


model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])


# In[ ]:


history = model.fit(X_training,y_training,validation_data=(X_valid,y_valid),epochs=100,batch_size=64)


# In[ ]:


plt.style.use('dark_background')
fig, ax = plt.subplots(2, 2, figsize=(10, 10))
sns.lineplot(x=np.arange(1, 101), y=history.history.get('loss'), ax=ax[0, 0])
sns.lineplot(x=np.arange(1, 101), y=history.history.get('accuracy'), ax=ax[0, 1])
sns.lineplot(x=np.arange(1, 101), y=history.history.get('val_loss'), ax=ax[1, 0])
sns.lineplot(x=np.arange(1, 101), y=history.history.get('val_accuracy'), ax=ax[1, 1])
ax[0, 0].set_title('Training Loss vs Epochs')
ax[0, 1].set_title('Training Accuracy vs Epochs')
ax[1, 0].set_title('Validation Loss vs Epochs')
ax[1, 1].set_title('Validation Accuracy vs Epochs')
plt.suptitle('Traditional Deep learning model',size=16)
plt.show()


# LSTM RNN Model

# In[ ]:


embedding_feature_vectors = 40
model1 = Sequential()
model1.add(Embedding(vocab_size,embedding_feature_vectors,input_length=length))
model1.add(Dropout(0.2))
model1.add(LSTM(200,dropout=0.2,recurrent_dropout=0.3))
model.add(Dropout(0.2))
model.add(Dense(100, activation='relu'))
model.add(Dropout(0.2))
model1.add(Dense(3,activation='softmax'))


# In[ ]:


model1.compile(loss='binary_crossentropy',optimizer=keras.optimizers.Adadelta(),metrics=['accuracy'])


# In[ ]:


history1 = model1.fit(X_training,y_training,validation_data=(X_valid,y_valid),epochs=10,batch_size=32,verbose=2)


# In[ ]:


plt.style.use('dark_background')
fig, ax = plt.subplots(2, 2, figsize=(10, 10))
sns.lineplot(x=np.arange(1, 11), y=history1.history.get('loss'), ax=ax[0, 0])
sns.lineplot(x=np.arange(1, 11), y=history1.history.get('accuracy'), ax=ax[0, 1])
sns.lineplot(x=np.arange(1, 11), y=history1.history.get('val_loss'), ax=ax[1, 0])
sns.lineplot(x=np.arange(1, 11), y=history1.history.get('val_accuracy'), ax=ax[1, 1])
ax[0, 0].set_title('Training Loss vs Epochs')
ax[0, 1].set_title('Training Accuracy vs Epochs')
ax[1, 0].set_title('Validation Loss vs Epochs')
ax[1, 1].set_title('Validation Accuracy vs Epochs')
plt.suptitle('LSTM RNN model',size=16)
plt.show()


# Test accurcy using Traditional DL Model

# In[ ]:


score_dl = model.evaluate(X_test,y_test)
score_dl


# In[ ]:


print("Accuracy of Traditional DL model: {}".format(score_dl[1]*100))


# Test Accuracy of LSTM RNN Model

# In[ ]:


score_lstm = model1.evaluate(X_test,y_test)
score_lstm


# In[ ]:


print("Accuracy of LSTM RNN model: {}".format(score_lstm[1]*100))


# In[ ]:




