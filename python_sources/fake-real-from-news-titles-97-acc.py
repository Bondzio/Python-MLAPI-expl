#!/usr/bin/env python
# coding: utf-8

# As a first baseline model, I will categorize real and fake news with a layers of Embeddings Biderectional LSTMs. For this approach I will use the news titles only, and disregards the rest of the information in the data set (i.e. text, date, category). 

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import random
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import json
import tensorflow as tf
import csv
import random
import numpy as np

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import regularizers


# I load the data in the notebook and add labels (1 for real and 0 for fake news). These are the property I will predict). Once the label column is added, the two data sets are joined.

# In[ ]:


real_news = pd.read_csv("../input/fake-and-real-news-dataset/True.csv")
fake_news = pd.read_csv("../input/fake-and-real-news-dataset/Fake.csv")
real_news['label'] = 1
fake_news['label'] = 0
whole_dataset = pd.concat([real_news, fake_news])


# I split the data into training (80% of the data) and validation (20% of the data), I stratify the label column, to have the same amount of fake news in the training and validation set (and the same for the real news). 

# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(whole_dataset['title'], whole_dataset['label'], test_size=0.2, random_state=10, stratify = whole_dataset['label'])


# In[ ]:


print(X_test.head())
print(y_test.head())


# I will tokenize the titles and pad them to have all the same length, which is set to the length of the longest title

# In[ ]:



lengths = [len(x) for x in whole_dataset['title']]
max_length = max(lengths)
trunc_type = 'post'
padding_type = 'post'

embedding_dim = 100
oov_tok = "<OOV>"

tokenizer = Tokenizer(oov_token=oov_tok)
tokenizer.fit_on_texts(X_train)

word_index = tokenizer.word_index
vocab_size=len(word_index)

sequences = tokenizer.texts_to_sequences(X_train)
padded = pad_sequences(sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

test_sequences = pad_sequences(tokenizer.texts_to_sequences(X_test), maxlen=max_length, padding=padding_type, truncating=trunc_type)


print(X_train.iloc[0], y_train[0])
print(X_train.iloc[1], y_train[1])
#print(padded[0])


# The data is now reday for the modeling. I define an early stopping callback to prevent too much overfitting. The model is a sequential stacking of 6 layers.
# The model is reaching a 97% validation accuracy and has an early stoppinf after 6 epochs.

# In[ ]:


from keras.callbacks import EarlyStopping
overfitCallback = EarlyStopping(monitor='val_loss',
                              min_delta=0,
                              patience=5,
                              verbose=0, mode='auto')

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size+1, 15, input_length=max_length),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Conv1D(64, 5, activation='relu'),
    tf.keras.layers.MaxPooling1D(pool_size=4),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
model.summary()

num_epochs = 50
history = model.fit(padded, y_train, epochs=num_epochs, validation_data=(test_sequences, y_test), verbose=2, callbacks=[overfitCallback])

print("Training Complete")


# Next steps:
# - clean up of the titles
# - inclusion of news text in the prediction
# - plotting of the results and word clouds
