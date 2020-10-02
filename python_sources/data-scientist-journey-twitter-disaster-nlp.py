#!/usr/bin/env python
# coding: utf-8

# # Import libraries
# main libraries including pandas,numpy,matplotlib,seaborn

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
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# # Load dataset

# In[ ]:


train = pd.read_csv("/kaggle/input/nlp-getting-started/train.csv",index_col='id')
test = pd.read_csv("/kaggle/input/nlp-getting-started/test.csv",index_col='id')
submission = pd.read_csv("/kaggle/input/nlp-getting-started/sample_submission.csv")
display(train,test,submission)


# # Dataset overview

# ## What are shapes of those datasets?

# In[ ]:


print(f"Training set has a shape of {train.shape}")
print(f"Testing set has a shape of {test.shape}")


# ## What is the distribution of target variables?

# In[ ]:


display(train.target.value_counts())
sns.distplot(train.target,kde=False)


# ## What are features containing NaN and how many in each?

# In[ ]:


[(col,train[col].isnull().sum()) for col in train if train[col].isnull().any()]


# ## What keywords have highest frequency? and Locations?

# In[ ]:


train.keyword.value_counts()


# In[ ]:


train.location.value_counts()


# **- `fatalities` is the most common keyword**  
# **- `USA` is the most common location but overlapping with `United States`, also `New York` is a city in USA**  
# **- Some location variables appear to be unrecgonizable.**

# ## How many characters in each tweet?

# In[ ]:


sns.distplot(train.text.str.len(),kde=False)


# **- Nearly `140` characters as the most common length among the dataset **

# ### The above plot includes all data points, Is there any difference between fake and real points?

# In[ ]:


sns.distplot(train.text[train.target == 1].str.len(),kde=False,color='g')
plt.title('Character Count for Real Target Tweet')
plt.figure()
plt.title('Character Count for Fake Target Tweet')
sns.distplot(train.text[train.target == 0].str.len(),kde=False,color='m')


# **- There is no major difference in the number of characters between fake and real tweets**

# ## How many words in each tweet?

# In[ ]:


sns.distplot(train.text[train.target == 1].str.split().map(lambda x:len(x)),kde=False,color='g')
plt.title('Word Count for Real Target Tweet')
plt.figure()
plt.title('Word Count for Fake Target Tweet')
sns.distplot(train.text[train.target == 0].str.split().map(lambda x:len(x)),kde=False,color='m')


# **- `15 - 20` words are the most common for both real and fake tweets**

# ## What is the average word length?

# In[ ]:


sns.distplot(train.text[train.target == 1].str.split().map(lambda x:np.mean([len(y) for y in x])),kde=False,color='g')
plt.title('Average Word Length for Real Target Tweet')
plt.figure()
plt.title('Average Word Length for Fake Target Tweet')
sns.distplot(train.text[train.target == 0].str.split().map(lambda x:np.mean([len(y) for y in x])),kde=False,color='m')


# **- `4-8` word length in average for both real and fake tweets**

# ## What are common stopwords and their frequencies?

# In[ ]:


from collections import Counter
total_real,total_fake = Counter(),Counter()

for row in pd.Series(train.text[train.target == 1].str.split()):
    total_real += Counter(row)

for row in pd.Series(train.text[train.target == 0].str.split()):
    total_fake += Counter(row)


# In[ ]:


x,y = zip(*total_real.most_common(10))
sns.barplot(list(x),list(y))
plt.title("Common Stopwords for Real Tweets")
total_real.most_common(10)


# In[ ]:


i,j = zip(*total_fake.most_common(10))
sns.barplot(list(i),list(j))
plt.title("Common Stopwords for Fake Tweets")
total_fake.most_common(10)


# **- Most common stopwords are `the,in,of` for real tweets and `the,a,to` for fake tweets**

# ## What are most common punctuations and their frequenies?

# In[ ]:


import string
punctuation_collect_real = sorted([k for k in total_real.items() if k[0] in string.punctuation],key=lambda x:x[1],reverse=True)
i,j = zip(*punctuation_collect_real)
plt.title("Common Punctuations for Real Tweets")
sns.barplot(list(i),list(j))
punctuation_collect_real


# In[ ]:


punctuation_collect_fake = sorted([k for k in total_fake.items() if k[0] in string.punctuation],key=lambda x:x[1],reverse=True)
i,j = zip(*punctuation_collect_fake)
plt.title("Common Punctuations for Fake Tweets")
sns.barplot(list(i),list(j))
punctuation_collect_fake


# # Using Google BERT

# In[ ]:


import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow_hub as hub

get_ipython().system('wget --quiet https://raw.githubusercontent.com/tensorflow/models/master/official/nlp/bert/tokenization.py')
import tokenization


# In[ ]:


def bert_encode(texts,tokenizer,max_len=512):
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
        
    return np.array(all_tokens),np.array(all_masks),np.array(all_segments)


# In[ ]:


def build_model(bert_layer,max_len=512):
    input_word_ids = Input(shape=(max_len,), dtype=tf.int32, name="input_word_ids")
    input_mask = Input(shape=(max_len,), dtype=tf.int32, name="input_mask")
    segment_ids = Input(shape=(max_len,), dtype=tf.int32, name="segment_ids")

    _, sequence_output = bert_layer([input_word_ids, input_mask, segment_ids])
    clf_output = sequence_output[:, 0, :]
    out = Dense(1, activation='sigmoid')(clf_output)
    
    model = Model(inputs=[input_word_ids, input_mask, segment_ids], outputs=out)
    model.compile(Adam(lr=2e-6), loss='binary_crossentropy', metrics=['accuracy'])
    
    return model


# In[ ]:


get_ipython().run_cell_magic('time', '', 'module_url = "https://tfhub.dev/tensorflow/bert_en_uncased_L-24_H-1024_A-16/1"\nbert_layer = hub.KerasLayer(module_url, trainable=True)')


# In[ ]:


vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
tokenizer = tokenization.FullTokenizer(vocab_file,do_lower_case)


# In[ ]:


train_input = bert_encode(train.text.values,tokenizer,max_len=160)
test_input = bert_encode(test.text.values,tokenizer,max_len=160)
train_labels = train.target.values


# In[ ]:


model = build_model(bert_layer,max_len=160)
model.summary()


# In[ ]:


train_log = model.fit(train_input,train_labels,validation_split=0.25,epochs=3,batch_size=16)

model.save('model.h5')


# In[ ]:


preds = model.predict(test_input)


# In[ ]:


submission['target'] = preds.round().astype(int)
submission.to_csv('submission.csv',index=False)
submission.head()

