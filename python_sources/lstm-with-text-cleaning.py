#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


df = pd.read_csv('../input/jigsaw-unintended-bias-in-toxicity-classification/train.csv')


# In[ ]:


df.head()


# In[ ]:


from keras.models import Sequential
from keras.layers import CuDNNLSTM,Embedding,Dense,Dropout,Bidirectional
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from string import punctuation
from tqdm import tqdm
from sklearn.model_selection import train_test_split


# In[ ]:


def classification(text):
    if text>0.5:
        return 1
    else:
        return 0


# In[ ]:


df['target'] = df['target'].apply(classification)


# In[ ]:


x = df['comment_text']
y = df['target']


# In[ ]:


f = open('../input/gloveembeddings/glove.6B.100d.txt')
embedding_values = {}
for line in f:
    values = line.split(' ')
    word = values[0]
    coef = np.array(values[1:],dtype = 'float32')
    embedding_values[word]= coef


# In[ ]:


token = Tokenizer()


# In[ ]:


token.fit_on_texts(x)


# In[ ]:


seq = token.texts_to_sequences(x)


# In[ ]:


pad_seq = pad_sequences(seq,maxlen=100)


# In[ ]:


vocab_size = len(token.word_index)+1


# In[ ]:


embeddings_matrix = np.zeros((vocab_size,100))
for word,i in (tqdm(token.word_index.items())):
    values = embedding_values.get(word)
    if values is not None:
        embeddings_matrix[i]=values


# In[ ]:


model = Sequential()
model.add(Embedding(vocab_size,100,input_length=100,weights = [embeddings_matrix],trainable = False))
model.add(Bidirectional(CuDNNLSTM(75)))
model.add(Dense(128,activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1,activation='sigmoid'))


# In[ ]:


model.compile(optimizer='adam',loss='binary_crossentropy',metrics = ['accuracy'])


# In[ ]:


history = []
for i in range(5):
    print("Model "+str(i))
    print('========'*12)
    x_train,x_test,y_train,y_test = train_test_split(pad_seq,y,test_size = 0.15,random_state = np.random.randint(0,1000))
    history.append(model.fit(x_train,y_train,epochs = 3,batch_size=512,validation_data=(x_test,y_test)))
    print('========'*12)


# In[ ]:


test = pd.read_csv('../input/jigsaw-unintended-bias-in-toxicity-classification/test.csv')


# In[ ]:


test.head()


# In[ ]:


test_seq = token.texts_to_sequences(test['comment_text'])
pad_test_seq = pad_sequences(test_seq,maxlen=100)


# In[ ]:


predict = model.predict(pad_test_seq)


# In[ ]:


submission = pd.DataFrame([test['id']]).T
submission['prediction'] = predict


# In[ ]:


submission.to_csv('submission.csv', index=False)


# In[ ]:




