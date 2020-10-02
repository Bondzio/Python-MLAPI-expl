#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import matplotlib.pyplot as plt
import seaborn as sns

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


get_ipython().system('pip install bert-for-tf2 ')

get_ipython().system('pip install sentencepiece')


# In[ ]:


import tensorflow as tf

import tensorflow_hub as hub

from tensorflow.keras import layers
import bert


# In[ ]:


#Training data
train = pd.read_csv('/kaggle/input/nlp-getting-started/train.csv')
print('Training data shape: ', train.shape)
train.head()


# In[ ]:


import re

test_str = train.loc[417, 'text']

def clean_text(text):
    text = re.sub(r'https?://\S+', '', text) # Remove link
    text = re.sub(r'#\w+', '', text) # Remove hashtag
    text = re.sub(r'@\w+', '', text) # Remove mentions
    text = re.sub(r'\n',' ', text) # Remove line breaks
    text = re.sub('\s+', ' ', text).strip() # Remove leading, trailing, and extra spaces
    return text

print("Original text: " + test_str)
print("Cleaned text: " + clean_text(test_str))


# In[ ]:


# Testing data 
test = pd.read_csv('/kaggle/input/nlp-getting-started/test.csv')
print('Testing data shape: ', test.shape)
test.head()


# In[ ]:


def find_hashtags(tweet):
    return " ".join([match.group(0)[1:] for match in re.finditer(r"#\w+", tweet)]) or 'no'

def find_mentions(tweet):
    return " ".join([match.group(0)[1:] for match in re.finditer(r"@\w+", tweet)]) or 'no'

def find_links(tweet):
    return " ".join([match.group(0)[:] for match in re.finditer(r"https?://\S+", tweet)]) or 'no'

def process_text(df):
    
    df['text_clean'] = df['text'].apply(lambda x: clean_text(x))
    df['hashtags'] = df['text'].apply(lambda x: find_hashtags(x))
    df['mentions'] = df['text'].apply(lambda x: find_mentions(x))
    df['links'] = df['text'].apply(lambda x: find_links(x))
    # df['hashtags'].fillna(value='no', inplace=True)
    # df['mentions'].fillna(value='no', inplace=True)
    
    return df
    
train = process_text(train)
test = process_text(test)


# ## Exploratory Data Analysis

# In[ ]:


#Missing values in training set
train.isnull().sum()


# In[ ]:


# Replacing the ambigious locations name with Standard names
train['location'].replace({'United States':'USA',
                           'New York':'USA',
                            "London":'UK',
                            "Los Angeles, CA":'USA',
                            "Washington, D.C.":'USA',
                            "California":'USA',
                             "Chicago, IL":'USA',
                             "Chicago":'USA',
                            "New York, NY":'USA',
                            "California, USA":'USA',
                            "FLorida":'USA',
                            "Nigeria":'Africa',
                            "Kenya":'Africa',
                            "Everywhere":'Worldwide',
                            "San Francisco":'USA',
                            "Florida":'USA',
                            "United Kingdom":'UK',
                            "Los Angeles":'USA',
                            "Toronto":'Canada',
                            "San Francisco, CA":'USA',
                            "NYC":'USA',
                            "Seattle":'USA',
                            "Earth":'Worldwide',
                            "Ireland":'UK',
                            "London, England":'UK',
                            "New York City":'USA',
                            "Texas":'USA',
                            "London, UK":'UK',
                            "Atlanta, GA":'USA',
                            "Mumbai":"India"},inplace=True)

sns.barplot(y=train['location'].value_counts()[:5].index,x=train['location'].value_counts()[:5],
            orient='h')


# In[ ]:


def bert_encode(texts, tokenizer, max_len=512):
    all_tokens = []
    all_masks = []
    all_segments = []
    
    for text in texts:
        text = tokenizer.tokenize(text)
            
        text = text[:max_len-2]
        input_sequence = ["[CLS]"] + text + ["[SEP]"]
        pad_len = max_len - len(input_sequence)
        
        tokens = tokenizer.convert_tokens_to_ids(input_sequence)
        tokens += [0] * pad_len
        pad_masks = [1] * len(input_sequence) + [0] * pad_len
        segment_ids = [0] * max_len
        
        all_tokens.append(tokens)
        all_masks.append(pad_masks)
        all_segments.append(segment_ids)
    
    return np.array(all_tokens), np.array(all_masks), np.array(all_segments)


# In[ ]:


BertTokenizer = bert.bert_tokenization.FullTokenizer
bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/1",
                            trainable=True)
vocabulary_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
to_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
tokenizer = BertTokenizer(vocabulary_file, to_lower_case)


# In[ ]:


tokenizer.tokenize("don't be so judgmental")


# In[ ]:


train =train.fillna(' ')
test = test.fillna(' ')
train['text_final'] = train['text_clean']+' '+ train['keyword']+' '+ train['location']
test['text_final'] = test['text_clean']+' '+ test['keyword']+' '+ test['location']


# In[ ]:


train['lowered_text'] = train['text_final'].apply(lambda x: x.lower())
test['lowered_text'] = test['text_final'].apply(lambda x: x.lower())


# In[ ]:


train_input = bert_encode(train.lowered_text.values, tokenizer, max_len=320)
test_input = bert_encode(test.lowered_text.values, tokenizer, max_len=320)
train_labels = train.target.values


# ## Creating Traing Model

# In[ ]:


from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint


# In[ ]:


def build_model(bert_layer, max_len=512):
    input_word_ids = Input(shape=(max_len,), dtype=tf.int32, name="input_word_ids")
    input_mask = Input(shape=(max_len,), dtype=tf.int32, name="input_mask")
    segment_ids = Input(shape=(max_len,), dtype=tf.int32, name="segment_ids")

    _, sequence_output = bert_layer([input_word_ids, input_mask, segment_ids])
    clf_output = sequence_output[:, 0, :]
    hidden1 = Dense(100, activation='relu')(clf_output)
    hidden2 = Dense(50, activation='relu')(hidden1)
    out = Dense(1, activation='sigmoid')(hidden2)
    
    model = Model(inputs=[input_word_ids, input_mask, segment_ids], outputs=out)
    model.compile(Adam(lr=2e-6), loss='binary_crossentropy', metrics=['accuracy'])
    
    return model


# In[ ]:


model = build_model(bert_layer, max_len=320)
model.summary()


# In[ ]:


train_history = model.fit(
    train_input, train_labels,
    validation_split=0.1,
    epochs=10,
    batch_size=16
)


# In[ ]:


model.save('bert100_50.h5')


# In[ ]:


print(train_history)


# In[ ]:





# In[ ]:


test_pred = model.predict(test_input)


# In[ ]:


#from sklearn.metrics import confusion_matrix, classification_report
#print(confusion_matrix(y_test, y_pred))
#print(classification_report(y_test, y_pred.round().astype(int)))


# In[ ]:


submission = pd.read_csv("/kaggle/input/nlp-getting-started/sample_submission.csv")
submission['target'] = test_pred.round().astype(int)
submission.to_csv('submission.csv', index=False)


# ## References
# https://towardsdatascience.com/bert-in-keras-with-tensorflow-hub-76bcbc9417b
# https://medium.com/analytics-vidhya/bert-in-keras-tensorflow-2-0-using-tfhub-huggingface-81c08c5f81d8
# https://github.com/strongio/keras-bert/blob/master/keras-bert.ipynb
# https://mccormickml.com/2019/05/14/BERT-word-embeddings-tutorial/
# http://jalammar.github.io/a-visual-guide-to-using-bert-for-the-first-time/
# https://medium.com/@vineet.mundhra/loading-bert-with-tensorflow-hub-7f5a1c722565
# https://towardsdatascience.com/building-a-search-engine-with-bert-and-tensorflow-c6fdc0186c8a
# https://github.com/google-research/bert/blob/master/predicting_movie_reviews_with_bert_on_tf_hub.ipynb
# https://gist.github.com/vineetm
# 
# ## Bert Google Research
# https://github.com/google-research/bert
# 
# ## Bert Models
# https://tfhub.dev/s?q=bert
# 
# ## Note
# Feel free to ask questions, initiate discussion on this topic. Please upvote the discussion and notebook to help me make more such contributions.
