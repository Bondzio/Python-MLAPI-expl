#!/usr/bin/env python
# coding: utf-8

# This notebook is based on [my CNN kernel](https://www.kaggle.com/antmarakis/cnn-baseline-model). I merely changed the CNN architecture with a GRU (a variation of RNN).

# In[ ]:


seed = 0

import random
import numpy as np
from tensorflow import set_random_seed

random.seed(seed)
np.random.seed(seed)
set_random_seed(seed)


# In[ ]:


import pandas as pd

train = pd.read_csv('../input/train.tsv',  sep="\t")
test = pd.read_csv('../input/test.tsv',  sep="\t")


# In[ ]:


def format_data(train, test, max_features, maxlen):
    """
    Convert data to proper format.
    1) Shuffle
    2) Lowercase
    3) Sentiments to Categorical
    4) Tokenize and Fit
    5) Convert to sequence (format accepted by the network)
    6) Pad
    7) Voila!
    """
    from keras.preprocessing.text import Tokenizer
    from keras.preprocessing.sequence import pad_sequences
    from keras.utils import to_categorical
    
    train = train.sample(frac=1).reset_index(drop=True)
    train['Phrase'] = train['Phrase'].apply(lambda x: x.lower())
    test['Phrase'] = test['Phrase'].apply(lambda x: x.lower())

    X = train['Phrase']
    test_X = test['Phrase']
    Y = to_categorical(train['Sentiment'].values)

    tokenizer = Tokenizer(num_words=max_features)
    tokenizer.fit_on_texts(list(X))

    X = tokenizer.texts_to_sequences(X)
    X = pad_sequences(X, maxlen=maxlen)
    test_X = tokenizer.texts_to_sequences(test_X)
    test_X = pad_sequences(test_X, maxlen=maxlen)

    return X, Y, test_X


# In[ ]:


maxlen = 100
max_features = 10000

X, Y, test_X = format_data(train, test, max_features, maxlen)


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.25, random_state=seed)


# In[ ]:


from keras.models import Sequential
from keras.layers import Dense, Embedding, GRU, Dropout, Bidirectional, SpatialDropout1D


# In[ ]:


model = Sequential()

model.add(Embedding(max_features, 125, input_length=X.shape[1]))
model.add(SpatialDropout1D(0.2))
model.add(Bidirectional(GRU(75)))
model.add(Dropout(0.2))

model.add(Dense(5, activation='sigmoid'))


# In[ ]:


epochs = 2
batch_size = 32


# In[ ]:


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, Y_train, validation_data=(X_val, Y_val), epochs=epochs, batch_size=batch_size, verbose=1)


# In[ ]:


sub = pd.read_csv('../input/../input/sampleSubmission.csv')

sub['Sentiment'] = model.predict_classes(test_X, batch_size=batch_size, verbose=1)
sub.to_csv('sub_gru.csv', index=False)

