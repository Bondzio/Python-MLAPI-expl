#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


train=pd.read_csv('/kaggle/input/quora-question-pairs/train.csv.zip')


# In[ ]:


train.shape


# In[ ]:


train.head()


# In[ ]:


test=pd.read_csv('/kaggle/input/quora-question-pairs/test.csv')


# In[ ]:


test.head()


# In[ ]:


train[train['is_duplicate']==1].head()


# In[ ]:


train.info()


# In[ ]:


#dropping null values
train=train.dropna()


# In[ ]:


train_list1=list(train['question1'])
train_list2=list(train['question2'])
train_list=train_list1+train_list2


# In[ ]:


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# In[ ]:


vocab_size=20000
tokenizer=Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts(train_list)


# In[ ]:


sequence1=tokenizer.texts_to_sequences(train_list1)
sequence2=tokenizer.texts_to_sequences(train_list2)


# In[ ]:


#padding the sequences to a constant size
max_length=100
sequence1=pad_sequences(sequence1,maxlen=max_length,padding='post')
sequence2=pad_sequences(sequence2,maxlen=max_length,padding='post')


# In[ ]:


train['seq1']=list(sequence1)


# In[ ]:


train['seq2']=list(sequence2)


# In[ ]:


train.head()


# In[ ]:


labels=np.asarray(train['is_duplicate'])


# In[ ]:


#functional API
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense,Embedding,LSTM,concatenate


# In[ ]:


from tensorflow.keras import Input

text_input1=Input(shape=(None,),dtype='int32')
embedding1=Embedding(vocab_size,64)(text_input1)
encoded_text1=LSTM(32)(embedding1)

text_input2=Input(shape=(None,),dtype='int32')
embedding2=Embedding(vocab_size,64)(text_input2)
encoded_text2=LSTM(32)(embedding2)

concatenated=concatenate([encoded_text1,encoded_text2],axis=-1)

output=Dense(64,activation='relu')(concatenated)
output=Dense(1,activation='sigmoid')(output)


# In[ ]:


model=Model([text_input1,text_input2],output)
model.compile(optimizer='rmsprop',loss='binary_crossentropy',metrics=['accuracy'])


# In[ ]:


model.summary()


# In[ ]:


hist=model.fit([sequence1,sequence2],labels,epochs=2,batch_size=128)


# In[ ]:





# In[ ]:




