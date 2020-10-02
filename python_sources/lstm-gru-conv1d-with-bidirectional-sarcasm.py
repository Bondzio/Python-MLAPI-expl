#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Deep Learning necessities
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, Flatten, Dense, LSTM, Bidirectional, Dropout, Conv1D, MaxPool1D
from keras.layers import GlobalMaxPool1D, GRU
from keras import optimizers

import matplotlib.pyplot as plt

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# <a id='contents'></a>
# ## Contents:
# 
# ### 1. [Understand folder structure, view a few data points](#1.1)
# ### 2. [Prepare Data for modelling](#2.1)
# ### 3. [Build and train Fully Connected Model](#3.1)
# ### 4. [Build and train LSTM model ](#4)
# ### 5. [Build and train Conv1D model](#5)
# ### 6. [Build and train Conv1D + GRU model](#6)

# In[2]:


# Util functions
def prep_data(text, tok):
    seq = tok.texts_to_sequences([text])
    data = pad_sequences(seq, MAX_SEQ_LENGTH)
    return data

def plot(history):
    hist = history.history
    train_loss, train_acc = hist['loss'], hist['acc']
    val_loss, val_acc = hist['val_loss'], hist['val_acc']
    epochs = range(1, len(train_acc)+1)
    
    plt.plot(epochs, train_acc, 'g', label='Training acc')
    plt.plot(epochs, val_acc, 'o', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.figure()
    plt.plot(epochs, train_loss, 'g', label='Training loss')
    plt.plot(epochs, val_loss, 'o', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.show()


# <a id='1.1'></a>
# # 1. Understand folder structure, view a few data points 

# In[3]:


df = pd.read_json('../input/Sarcasm_Headlines_Dataset.json', lines=True)
df.head()


# <a id='2.1'></a>
# # 2. Prepare Data for Modelling

# In[4]:


df = df[['headline', 'is_sarcastic']]


# In[5]:


MAX_WORDS = 20000


# In[6]:


tok = Tokenizer(num_words = MAX_WORDS) # keeping 10000 now for first iteration
tok.fit_on_texts(df.headline)
seqs = tok.texts_to_sequences(df.headline)


# In[7]:


# Find length of sentence 
df['length'] = df['headline'].apply(lambda x: len(x.split(' ')))


# In[8]:


# Dataset seems balanced
df.is_sarcastic.value_counts()


# In[9]:


MAX_SEQ_LENGTH = 40


# In[10]:


data = pad_sequences(seqs, MAX_SEQ_LENGTH)


# In[11]:


seqs[0]


# In[12]:


labels = np.asarray(df.is_sarcastic)


# In[13]:


data.shape


# In[14]:


labels.shape


# In[15]:


training_samples  = 24000
validation_samples = 2709


# In[16]:


# Train val split
indices = np.arange(data.shape[0])
np.random.shuffle(indices)
data = data[indices]
labels = labels[indices]
x_train = data[:training_samples]
y_train = labels[:training_samples]
x_val = data[training_samples: training_samples + validation_samples]
y_val = labels[training_samples: training_samples + validation_samples]


# In[17]:


print('X train shape',x_train.shape)
print('y train shape',y_train.shape)


# In[18]:


print('X val shape',x_val.shape)
print('y val shape',y_val.shape)


# In[19]:


# For using pretrained embeddings
# emb_path = 'path of the embedding'
# embeddings_index = {}
# f = open(emb_path)
# for line in f:
#     values = line.split()
#     word = values[0]
#     coefs = np.asarray(values[1:], dtype='float32')
#     embeddings_index[word] = coefs
# f.close()

# embedding_dim = 100
# embedding_matrix = np.zeros((max_words, embedding_dim))
# for word, i in word_index.items():
# if i < max_words:
# embedding_vector = embeddings_index.get(word)
# if embedding_vector is not None:
# embedding_matrix[i] = embedding_vector


# <a id='3.1'></a>
# # 3. Build and Train a Fully Connected model
# 

# In[20]:


# define dense model
EMB_DIM = 6
def fcmodel():
    model = Sequential()
    model.add(Embedding(input_dim=MAX_WORDS, output_dim= EMB_DIM, input_length=MAX_SEQ_LENGTH))    
    
    # Flatten Layer
    model.add(Flatten())
    
    # FC1
    model.add(Dense(64, activation='relu'))
    
    # Output layer
    model.add(Dense(1, activation='sigmoid'))
    
    # print model summary
    model.summary()
    
    # When using pretrained embeddings
    #model.layers[0].set_weights([embedding_matrix])
    #model.layers[0].trainable = False
              
    # Compile the model
    model.compile(optimizer = 'rmsprop',
                 loss = 'binary_crossentropy',
                 metrics = ['acc'])
    return model

fcmod = fcmodel()


# In[21]:


EPOCHS = 9
BATCH_SIZE =512


# In[22]:


# Train the model
fchist = fcmod.fit(x_train, y_train,
         epochs = EPOCHS,
         batch_size = BATCH_SIZE,
         validation_data = (x_val, y_val))


# In[23]:


plot(fchist)


# <a id='4'></a>
# # 4. Build and Train LSTM model

# In[24]:


# Lstm model

def lstm():
    model = Sequential()
    
    model.add(Embedding(input_dim=MAX_WORDS, output_dim=EMB_DIM, input_length=MAX_SEQ_LENGTH))
    
    model.add(Bidirectional(LSTM(16, return_sequences=True, recurrent_dropout=0.1, dropout=0.1)))
    
    model.add(Bidirectional(LSTM(32, recurrent_dropout=0.1, dropout=0.1)))
    
    model.add(Dense(1, activation='sigmoid'))
    
    # Compile the model
    model.compile(optimizer = 'rmsprop',
                  loss = 'binary_crossentropy',
                  metrics = ['acc'])
    
    return model

lsmod = lstm()


# In[25]:


# Train the model
lshist = lsmod.fit(x_train, y_train,
         epochs = EPOCHS,
         batch_size = BATCH_SIZE,
         validation_data = (x_val, y_val))


# In[26]:


plot(lshist)


# <a id='5'></a>
# # 5. Build and Train Conv1D model

# In[27]:


# Using CONV 1D

def conv1d():
    
    model = Sequential()
    
    model.add(Embedding(input_dim=MAX_WORDS,output_dim=EMB_DIM, input_length=MAX_SEQ_LENGTH))
    
    model.add(Conv1D(filters=32, kernel_size=7, activation='relu'))
    
    model.add(MaxPool1D(pool_size=5))
    
    model.add(Conv1D(filters=32, kernel_size=3, activation='relu'))
    
    model.add(Dropout(0.1))
    
    model.add(GlobalMaxPool1D())
    
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics= ['acc'])
    
    return model

convmod = conv1d()


# In[28]:


convhist = convmod.fit(x_train, y_train,
                      epochs = 20,
                      batch_size = BATCH_SIZE,
                      validation_data = (x_val, y_val))
plot(convhist)


# <a id='6'></a>
# # 6. Build and Train Conv1D + GRU model

# In[29]:


# Using CONV 1D with GRU

def convgru():
    
    model = Sequential()
    
    model.add(Embedding(input_dim=MAX_WORDS,output_dim=EMB_DIM, input_length=MAX_SEQ_LENGTH))
    
    model.add(Conv1D(filters=32, kernel_size=7, activation='relu'))
    
    model.add(MaxPool1D(pool_size=5))
    
    model.add(Conv1D(filters=32, kernel_size=3, activation='relu'))
    
    model.add(GRU(32, dropout=0.1, recurrent_dropout=0.5))
    
    model.add(Dense(1, activation='sigmoid'))
    
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics= ['acc'])
    
    return model

convgrumod = convgru()


# In[30]:


convgruhist = convgrumod.fit(x_train, y_train, 
                           epochs = 6,
                           batch_size=BATCH_SIZE,
                           validation_data = (x_val, y_val))
plot(convgruhist)


# ## It's been a long EPOCH, THANKS FOR STAYING TILL THE END and NOT EARLY STOPPING :)
# ### Your comments, corrections, advice are whole heartedly welcome

# In[ ]:




