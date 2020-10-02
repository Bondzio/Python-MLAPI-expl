#!/usr/bin/env python
# coding: utf-8

# In[1]:


import spacy
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import warnings
warnings.filterwarnings("ignore")


# In[2]:


train = pd.read_csv("../input/train.csv")


# In[3]:


train.shape


# In[4]:


test = pd.read_csv("../input/test.csv", delimiter=',',encoding='ISO-8859-1')


# In[5]:


sentences_train = train["comment_text"].fillna("_na_").values


# In[6]:


sentences_test = test["comment_text"].fillna("_na_").values


# In[7]:


# Embedding parameter set
embed_size = 100 # how big is each word vector
max_features = 20000 # how many unique words to use (i.e num rows in embedding vector)
maxlen = 50 # max number of words in a comment to use


# In[8]:


import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


# In[9]:


tokenizer = Tokenizer(num_words=max_features)
tokenizer.fit_on_texts(list(sentences_train))
tokens_train = tokenizer.texts_to_sequences(sentences_train)
tokens_test = tokenizer.texts_to_sequences(sentences_test)
X_train = pad_sequences(tokens_train, maxlen=maxlen)
X_test = pad_sequences(tokens_test, maxlen=maxlen)


# In[10]:


y_train=['toxic','severe_toxic','obscene','threat','insult','identity_hate']


# In[11]:


Y=train[y_train].values


# In[12]:


Y.shape


# In[13]:


from tensorflow import keras as tfk


# In[14]:


import warnings

from keras.models import Sequential
from keras.utils import to_categorical
from keras.layers import Dense,LSTM,Embedding,SpatialDropout1D
from keras.losses import categorical_crossentropy
from keras.activations import relu,softmax


# In[15]:


tb = tfk.callbacks.TensorBoard()


# In[16]:


model = Sequential()
model.add(Embedding(max_features, 128, input_length=X_train.shape[1]))
model.add(SpatialDropout1D(0.25))
model.add(LSTM(196,dropout=0.2))
model.add(Dense(6, activation="softmax"))


# In[17]:


model.compile(optimizer="rmsprop", loss=categorical_crossentropy, metrics=["acc"])


# In[19]:


model_history=model.fit(X_train,Y,batch_size=100,epochs=1 ,validation_split=0.2,callbacks=[tb])


# In[20]:


y_pred = model.predict(X_test, batch_size=100)


# In[21]:


y_pred


# In[22]:


Submit = pd.DataFrame(test.id,columns=['id'])
Submit2 = pd.DataFrame(y_pred,columns=y_train)
Submit = pd.concat([Submit,Submit2],axis=1)
Submit.to_csv("toxic_pred.csv",index=False)


# In[24]:


Submit.head()


# In[ ]:




