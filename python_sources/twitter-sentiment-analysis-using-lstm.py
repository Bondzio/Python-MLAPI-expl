#!/usr/bin/env python
# coding: utf-8

# In[ ]:


##importing libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer,text_to_word_sequence
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense,Dropout,LSTM,Embedding,Flatten
from keras.utils.np_utils import to_categorical
import re
from keras import backend as K 
from sklearn.metrics import confusion_matrix,classification_report


# In[ ]:


data=pd.read_csv('../input/first-gop-debate-twitter-sentiment/Sentiment.csv')


# In[ ]:


data.shape


# In[ ]:


data.columns


# In[ ]:


data.head()


# In[ ]:


data['sentiment'].unique()


# In[ ]:


data['sentiment'].value_counts()


# In[ ]:


##function to process text
def preprocess(a):
    if a=='RT' or a.startswith('@') or a.startswith('http'):
        pass
    else:
        return a


# In[ ]:


data['processed_text']=data['text'].apply(lambda x: ' '.join([re.sub('[^a-zA-z0-9\s]','',i) for i in x.split(' ') if preprocess(i)!= None]).lower())


# In[ ]:


data_for_model=data[['processed_text','sentiment']]


# In[ ]:


data_for_model.columns


# In[ ]:


t=Tokenizer()

t.fit_on_texts(data_for_model['processed_text'])

X=t.texts_to_sequences(data_for_model['processed_text'])

X=pad_sequences(X,maxlen=160)


# In[ ]:


len(t.word_index)


# In[ ]:


y=pd.get_dummies(data_for_model['sentiment']).values


# In[ ]:


train_X,test_X,train_y,test_y=train_test_split(X,y,test_size=0.3,random_state=1)


# In[ ]:


##model
K.clear_session()
model=Sequential()
model.add(Embedding(len(t.word_index)+1,50,input_length=160))
model.add(LSTM(128,dropout=0.2,recurrent_dropout=0.2))
model.add(Dense(3,activation='softmax'))
model.summary()


# In[ ]:


model.compile('adam',loss='categorical_crossentropy',metrics=['accuracy'])


# In[ ]:


model.fit(train_X,train_y,epochs=10,validation_split=0.2)


# **Prediction on Test Data**

# In[ ]:


test_X.shape


# In[ ]:


pred=model.predict(test_X.reshape(-1,test_X.shape[1]))


# In[ ]:


pred_y=np.argmax(pred,axis=1)


# In[ ]:


act_y=np.argmax(test_y,axis=1)


# In[ ]:


confusion_matrix(pred_y,act_y)


# In[ ]:


print(classification_report(pred_y,act_y))


# In[ ]:




