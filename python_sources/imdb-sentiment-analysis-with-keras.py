#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from keras import models, layers
import os
print(os.listdir("../input"))


# In[ ]:


imdb = pd.read_csv('../input/IMDB Dataset.csv')


# In[ ]:


imdb.head()


# In[ ]:


le = LabelEncoder()

imdb['seintiment_target'] = le.fit_transform(imdb.sentiment)


# In[ ]:


imdb.head()


# In[ ]:


plt.figure(figsize=(6,4))
sns.countplot('sentiment',  data=imdb)


# In[ ]:


keras_token = Tokenizer(num_words=10000)
keras_token.fit_on_texts(imdb.review)


# In[ ]:


len(keras_token.word_index)


# In[ ]:


keras_result = keras_token.texts_to_sequences(imdb.review)


# In[ ]:


keras_pad_result = pad_sequences(keras_result, maxlen=500, padding='post')


# In[ ]:


keras_pad_result[0]


# In[ ]:


keras_pad_result.shape


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(keras_pad_result, 
                                                    imdb['seintiment_target'].values, 
                                                    test_size=0.3, 
                                                    random_state=42, 
                                                    stratify=imdb['seintiment_target'].values)


# In[ ]:


print(X_train.shape, y_train.shape)

print(X_test.shape, y_test.shape)


# In[ ]:


model = models.Sequential()
model.add(layers.Embedding(10000, 50, input_length=500))
model.add(layers.Conv1D(128, 8, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.MaxPool1D(3))
model.add(layers.Conv1D(256, 8, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Bidirectional(layers.LSTM(128, return_sequences=True, dropout=0.2, recurrent_dropout=0.2)))
model.add(layers.Bidirectional(layers.LSTM(256, dropout=0.2, recurrent_dropout=0.2)))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dropout(0.2))
model.add(layers.Dense(1, activation='sigmoid'))

model.summary()

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# In[ ]:


model.fit(X_train, y_train, batch_size=128, epochs=15, validation_data=(X_test, y_test))

