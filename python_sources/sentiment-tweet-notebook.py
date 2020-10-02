#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
import re


# In[2]:


data = pd.read_csv('../input/Sentiment.csv')

# Keeping only the neccessary columns
data = data[['text','sentiment']]
print(len(data))


# In[3]:


data = data[data.sentiment != "Neutral"]
data['text'] = data['text'].apply(lambda x: x.lower())
data['text'] = data['text'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))

#print(data[ data['sentiment'] == 'Positive'].size)
#print(data[ data['sentiment'] == 'Negative'].size)

for idx,row in data.iterrows():
    row[0] = row[0].replace('rt',' ')
    
batch_size = 5000
tokenizer = Tokenizer(nb_words=batch_size, split=' ')

tokenizer.fit_on_texts(data['text'].values)
X = tokenizer.texts_to_sequences(data['text'].values)

maxx = 0
c=0
for ll in X:
    c=len(ll)
    if c>maxx:
        maxx=c
print('Max',maxx)
X = pad_sequences(X)
print(len(X[0]))


# In[4]:


embed_dim = 128
lstm_out = 128
model = Sequential()
model.add(Embedding(batch_size, embed_dim,input_length = X.shape[1], dropout=0.2))
model.add(LSTM(lstm_out, dropout_U=0.2, dropout_W=0.2))
model.add(Dense(2,activation='softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
print(model.summary())


# In[5]:


print(data['sentiment'].values)
Y = pd.get_dummies(data['sentiment']).values
print(Y)
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.33, random_state = 42)
print(X_train.shape,Y_train.shape)
print(X_test.shape,Y_test.shape)


# In[8]:


model.fit(X_train, Y_train, nb_epoch = 2, batch_size=32)


# In[9]:


z=np.array(X_test[9]).reshape(1,29)


# In[10]:


z


# In[11]:


model.predict(z)


# In[12]:


Y_test[9]


# In[19]:


s1 = "john is a nice guy you would love to work with him"
s2 = "that was a bummer and an epic fail movie just dont go to watch"
hh = tokenizer.texts_to_sequences([s1])


# In[20]:


hh


# In[22]:


X_test[9].shape


# In[23]:


hh = pad_sequences(hh, maxlen=29)


# In[24]:


hh=np.array(hh[0]).reshape(1,29)


# In[25]:


model.predict(hh)


# In[ ]:


model.save('sentiment.h5')


# In[ ]:


del model


# In[ ]:




