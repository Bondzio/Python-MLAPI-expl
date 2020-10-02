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

get_ipython().system('unzip ../input/sentiment-analysis-on-movie-reviews/test.tsv.zip ')
get_ipython().system('unzip ../input/sentiment-analysis-on-movie-reviews/train.tsv.zip ')

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


# !pip install sentencepiece
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import logging

logging.basicConfig(level=logging.INFO)


# We will need bert `Tokenization` class

# In[ ]:


get_ipython().system('wget --quiet https://raw.githubusercontent.com/tensorflow/models/master/official/nlp/bert/tokenization.py')


# # Step_1 load packages and data

# In[ ]:


get_ipython().run_cell_magic('time', '', 'import tensorflow_hub as hub \nimport tokenization\nmodule_url = "https://tfhub.dev/tensorflow/bert_en_uncased_L-24_H-1024_A-16/1"\nbert_layer = hub.KerasLayer(module_url, trainable=True)')


# In[ ]:


train = pd.read_csv('train.tsv', sep='\t')
test = pd.read_csv('test.tsv', sep='\t')


# # Step_2: build bert_layer and model

# In[ ]:


get_ipython().run_cell_magic('time', '', "import tensorflow_hub as hub \nimport tokenization\nmodule_url = 'https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/2'\nbert_layer = hub.KerasLayer(module_url, trainable=True)")


# In[ ]:


vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
tokenizer = tokenization.FullTokenizer(vocab_file, do_lower_case)

def bert_encode(texts, tokenizer, max_len=512):
    all_tokens = []
    all_masks = []
    all_segments = []
    
    for text in texts:
        text = tokenizer.tokenize(text)
            
        text = text[:max_len-2]
        input_sequence = ["[CLS]"] + text + ["[SEP]"]
        pad_len = max_len - len(input_sequence)
        
        tokens = tokenizer.convert_tokens_to_ids(input_sequence) + [0] * pad_len
        pad_masks = [1] * len(input_sequence) + [0] * pad_len
        segment_ids = [0] * max_len
        
        all_tokens.append(tokens)
        all_masks.append(pad_masks)
        all_segments.append(segment_ids)
    
    return np.array(all_tokens), np.array(all_masks), np.array(all_segments)

def build_model(bert_layer, max_len=512):
    input_word_ids = tf.keras.Input(shape=(max_len,), dtype=tf.int32, name="input_word_ids")
    input_mask = tf.keras.Input(shape=(max_len,), dtype=tf.int32, name="input_mask")
    segment_ids = tf.keras.Input(shape=(max_len,), dtype=tf.int32, name="segment_ids")

    pooled_output, sequence_output = bert_layer([input_word_ids, input_mask, segment_ids])
    clf_output = sequence_output[:, 0, :]
    net = tf.keras.layers.Dense(64, activation='relu')(clf_output)
    net = tf.keras.layers.Dropout(0.2)(net)
    net = tf.keras.layers.Dense(32, activation='relu')(net)
    net = tf.keras.layers.Dropout(0.2)(net)
    out = tf.keras.layers.Dense(5, activation='softmax')(net)
    
    model = tf.keras.models.Model(inputs=[input_word_ids, input_mask, segment_ids], outputs=out)
    model.compile(tf.keras.optimizers.Adam(lr=1e-5), loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model


# We check only the first 150 characters of each review. 
# 
# You can also increase this length, but the running time will increase too.

# In[ ]:


max_len = 150
train_input = bert_encode(train.Phrase.values, tokenizer, max_len=max_len)
test_input = bert_encode(test.Phrase.values, tokenizer, max_len=max_len)
train_labels = tf.keras.utils.to_categorical(train.Sentiment.values, num_classes=5)


# In[ ]:


model = build_model(bert_layer, max_len=max_len)
model.summary()


# # Step_3: Run model and export predictions

# Each epoch takes about 1 hours (even with GPU acceleration). After all, we have a large dataset.

# In[ ]:


get_ipython().run_cell_magic('time', '', "checkpoint = tf.keras.callbacks.ModelCheckpoint('model.h5', monitor='val_accuracy', save_best_only=True, verbose=1)\nearlystopping = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=5, verbose=1)\n\ntrain_history = model.fit(\n    train_input, train_labels, \n    validation_split=0.2,\n    epochs=3,\n    callbacks=[checkpoint, earlystopping],\n    batch_size=32,\n    verbose=1\n)")


# In[ ]:


get_ipython().run_cell_magic('time', '', "model.load_weights('model.h5')\ntest_pred = model.predict(test_input)\n\nsub = pd.read_csv('../input/sentiment-analysis-on-movie-reviews/sampleSubmission.csv')\nsub['Sentiment'] = np.argmax(test_pred, axis=-1)\nsub.to_csv('submission.csv', index=False)")

