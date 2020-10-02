#!/usr/bin/env python
# coding: utf-8

# **General information**
# In this kernel I'll work with data from Movie Review Sentiment Analysis Playground Competition.
# 
# This is a very basic notebook for begineers who wants to get into LSTM keras. I have created the basic model after that you can improve your model.

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


# **Reading the dataset**

# In[ ]:


train = pd.read_csv('../input/train.tsv', sep="\t")
test = pd.read_csv('../input/test.tsv', sep="\t")
sub = pd.read_csv('../input/sampleSubmission.csv', sep=",")


# In[ ]:


train.head()


# **Importing libraries required**
# We are using keras with tensorflow as backend.

# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import text, sequence
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
import re


# I am filtering the Phrases so only valid texts and words remain. Then, I define the number of max features as 2000 and use Tokenizer to vectorize and convert text into Sequences so the Network can deal with it as input.

# In[ ]:


train['Phrase'] = train['Phrase'].apply(lambda x: x.lower())
train['Phrase'] = train['Phrase'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))

test['Phrase'] = test['Phrase'].apply(lambda x: x.lower())
test['Phrase'] = test['Phrase'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))


# In[ ]:


print(set(train.Sentiment)) #Output Labels


# In[ ]:


max_fatures = 2000
tokenizer = Tokenizer(num_words=max_fatures,filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
                                   lower=True,split=' ')
tokenizer.fit_on_texts(train['Phrase'].values)
X = tokenizer.texts_to_sequences(train['Phrase'].values)
X = pad_sequences(X)


# **Creating the model**
# Next, I compose the LSTM Network. Note that embed_dim, lstm_out, batch_size, droupout_x variables are hyperparameters, their values are somehow intuitive, can be and must be played with in order to achieve good results. Please also note that I am using softmax as activation function. The reason is that our Network is using categorical crossentropy, and softmax is just the right activation method for that.

# In[ ]:


embed_dim = 128
lstm_out = 196

model = Sequential()
model.add(Embedding(max_fatures, embed_dim,input_length = X.shape[1]))
#model.add(SpatialDropout1D(0.4))
model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(5,activation='softmax'))
model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
print(model.summary())


# Hereby I declare the train and test dataset.

# In[ ]:


Y = pd.get_dummies(train['Sentiment']).values
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.20, random_state = 42)
print(X_train.shape,Y_train.shape)
print(X_test.shape,Y_test.shape)


# Here we train the Network.

# In[ ]:


batch_size = 32
model.fit(X_train, Y_train, epochs = 10, batch_size=batch_size, verbose = 1)


# In[ ]:


validation_size = 1200

X_validate = X_test[-validation_size:]
Y_validate = Y_test[-validation_size:]
X_test = X_test[:-validation_size]
Y_test = Y_test[:-validation_size]
score,acc = model.evaluate(X_test, Y_test, verbose = 2, batch_size = batch_size)
print("score: %.2f" % (score))
print("acc: %.2f" % (acc))


# In[ ]:


x_test = test['Phrase'].values
print(x_test)


# In[ ]:


x_test_tokenized = tokenizer.texts_to_sequences(x_test)
x_testing = sequence.pad_sequences(x_test_tokenized, maxlen=45)


# In[ ]:


y_testing = model.predict(x_testing, verbose = 1)


# In[ ]:


predictions = np.round(np.argmax(y_testing, axis=1)).astype(int)
sub['Sentiment'] = predictions
sub.to_csv("submission_result.csv", index=False)


# For improvement you can make a bigger network model. And also use the whole dataset and submit the prediction, you will get good accuracy. 
# If you like Applause. Thank you.
