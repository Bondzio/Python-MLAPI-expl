#!/usr/bin/env python
# coding: utf-8
This kernel is building and training convolutional network for text classification. The architecture of the netwok is the same as in the paper of Kim https://arxiv.org/pdf/1408.5882.pdf
# ### Let's load data to see what we are dealing with ###

# In[ ]:


import numpy as np
import pandas as pd


# In[ ]:


train_data=pd.read_csv('../input/train.csv')
test_data=pd.read_csv('../input/test.csv')


# In[ ]:


train_data.head(3)


# In[ ]:


test_data.head(3)


# ### Lets see the size, and if we have missing values in the datasets ###

# In[ ]:


print(train_data.shape,test_data.shape)
print(train_data.isnull().sum())
print(test_data.isnull().sum())


# ### Ok, seems clean ###
# 

# ### Lets make categories of authors ###

# In[ ]:


authors=train_data.author.unique()
dic={}
for i,author in enumerate(authors):
    dic[author]=i
labels=train_data.author.apply(lambda x:dic[x])


# ### Lets divide our training data to train and validation ###

# In[ ]:


val_data=train_data.sample(frac=0.2,random_state=200)
train_data=train_data.drop(val_data.index)


# ### Tokenize text of the training data with keras text preprocessing functions ###

# In[ ]:


from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical


# In[ ]:


texts=train_data.text


# In[ ]:


NUM_WORDS=20000
tokenizer = Tokenizer(num_words=NUM_WORDS,filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n\'',
                      lower=True)
tokenizer.fit_on_texts(texts)
sequences_train = tokenizer.texts_to_sequences(texts)
sequences_valid=tokenizer.texts_to_sequences(val_data.text)
word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))


# In[ ]:


X_train = pad_sequences(sequences_train)
X_val = pad_sequences(sequences_valid,maxlen=X_train.shape[1])
y_train = to_categorical(np.asarray(labels[train_data.index]))
y_val = to_categorical(np.asarray(labels[val_data.index]))
print('Shape of X train and X validation tensor:', X_train.shape,X_val.shape)
print('Shape of label train and validation tensor:', y_train.shape,y_val.shape)


# ### word embedding ###

# ### lets load the pretrain Word2Vec model from Google https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit ###
# ### It might take time since it contains contains 300-dimensional vectors for 3 million words and phrases ###

# In[ ]:


import gensim
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess

from gensim.models.keyedvectors import KeyedVectors

word_vectors = KeyedVectors.load_word2vec_format('../GoogleNews-vectors-negative300.bin', binary=True)

EMBEDDING_DIM=300
vocabulary_size=min(len(word_index)+1,NUM_WORDS)
embedding_matrix = np.zeros((vocabulary_size, EMBEDDING_DIM))
for word, i in word_index.items():
    if i>=NUM_WORDS:
        continue
    try:
        embedding_vector = word_vectors[word]
        embedding_matrix[i] = embedding_vector
    except KeyError:
        embedding_matrix[i]=np.random.normal(0,np.sqrt(0.25),EMBEDDING_DIM)

del(word_vectors)

from keras.layers import Embedding
embedding_layer = Embedding(vocabulary_size,
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                            trainable=True)


# ### Without pretrained data we can just initalize embedding matrixs as: ###

# In[ ]:


from keras.layers import Embedding
EMBEDDING_DIM=300
vocabulary_size=min(len(word_index)+1,NUM_WORDS)

embedding_layer = Embedding(vocabulary_size,
                            EMBEDDING_DIM)


# ### Lets create the network and train it as long as validation loss goes down  ###

# In[ ]:


from keras.layers import Dense, Input, GlobalMaxPooling1D
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.models import Model
from keras.layers import Input, Dense, Embedding, Conv2D, MaxPooling2D, Dropout,concatenate
from keras.layers.core import Reshape, Flatten
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam
from keras.models import Model
from keras import regularizers
sequence_length = X_train.shape[1]
filter_sizes = [3,4,5]
num_filters = 100
drop = 0.5



inputs = Input(shape=(sequence_length,))
embedding = embedding_layer(inputs)
reshape = Reshape((sequence_length,EMBEDDING_DIM,1))(embedding)

conv_0 = Conv2D(num_filters, (filter_sizes[0], EMBEDDING_DIM),activation='relu',kernel_regularizer=regularizers.l2(0.01))(reshape)
conv_1 = Conv2D(num_filters, (filter_sizes[1], EMBEDDING_DIM),activation='relu',kernel_regularizer=regularizers.l2(0.01))(reshape)
conv_2 = Conv2D(num_filters, (filter_sizes[2], EMBEDDING_DIM),activation='relu',kernel_regularizer=regularizers.l2(0.01))(reshape)

maxpool_0 = MaxPooling2D((sequence_length - filter_sizes[0] + 1, 1), strides=(1,1))(conv_0)
maxpool_1 = MaxPooling2D((sequence_length - filter_sizes[1] + 1, 1), strides=(1,1))(conv_1)
maxpool_2 = MaxPooling2D((sequence_length - filter_sizes[2] + 1, 1), strides=(1,1))(conv_2)

merged_tensor = concatenate([maxpool_0, maxpool_1, maxpool_2], axis=1)
flatten = Flatten()(merged_tensor)
reshape = Reshape((3*num_filters,))(flatten)
dropout = Dropout(drop)(flatten)
output = Dense(units=3, activation='softmax',kernel_regularizer=regularizers.l2(0.01))(dropout)

# this creates a model that includes
model = Model(inputs, output)


# In[ ]:


adam = Adam(lr=1e-3)

model.compile(loss='categorical_crossentropy',
              optimizer=adam,
              metrics=['acc'])
callbacks = [EarlyStopping(monitor='val_loss')]
model.fit(X_train, y_train, batch_size=1000, epochs=10, verbose=1, validation_data=(X_val, y_val),
         callbacks=callbacks)  # starts training



# ### now lets use our model to predict test data ###

# In[ ]:


sequences_test=tokenizer.texts_to_sequences(test_data.text)
X_test = pad_sequences(sequences_test,maxlen=X_train.shape[1])
y_pred=model.predict(X_test)


# In[ ]:


to_submit=pd.DataFrame(index=test_data.id,data={'EAP':y_pred[:,dic['EAP']],
                                                'HPL':y_pred[:,dic['HPL']],
                                                'MWS':y_pred[:,dic['MWS']]})


# In[ ]:


to_submit.to_csv('submit.csv')


# In[ ]:




