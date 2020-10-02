#!/usr/bin/env python
# coding: utf-8

# # Multi-label text classification with keras
# 

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import keras

import os
print(os.listdir("../input"))
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


df_questions = pd.read_csv('../input/Questions.csv', encoding='iso-8859-1')
df_tags = pd.read_csv('../input/Tags.csv', encoding='iso-8859-1')
df_questions.head(n=2)


# In[ ]:


grouped_tags = df_tags.groupby("Tag", sort='count').size().reset_index(name='count')
grouped_tags.Tag.describe()


# ## Reducing the problem to the most common tags in the dataset
# We only use the top 100 (arbitrarily picked number) tags because for rare tags there are simply not enough samples available to get reliable results.

# In[ ]:


num_classes = 100
grouped_tags = df_tags.groupby("Tag").size().reset_index(name='count')
most_common_tags = grouped_tags.nlargest(num_classes, columns="count")
df_tags.Tag = df_tags.Tag.apply(lambda tag : tag if tag in most_common_tags.Tag.values else None)
df_tags = df_tags.dropna()


# ## Preparing the contents of the dataframe
# 
# The question body contains html tags that we don't want to feed into our model. We will thus strip all tags and combine title and question body into a single field for simplicity.

# In[ ]:


import re 

def strip_html_tags(body):
    regex = re.compile('<.*?>')
    return re.sub(regex, '', body)

df_questions['Body'] = df_questions['Body'].apply(strip_html_tags)
df_questions['Text'] = df_questions['Title'] + ' ' + df_questions['Body']


# In[ ]:


# denormalize tables

def tags_for_question(question_id):
    return df_tags[df_tags['Id'] == question_id].Tag.values

def add_tags_column(row):
    row['Tags'] = tags_for_question(row['Id'])
    return row

df_questions = df_questions.apply(add_tags_column, axis=1)


# In[ ]:


pd.set_option('display.max_colwidth', 400)
df_questions[['Id', 'Text', 'Tags']].head()


# ## Tokenizing the text
# The text has to be vectorized so that we can feed it into our model. Keras comes with [several text preprocessing classes](https://keras.io/preprocessing/text/) that we can use for that.
# 
# The labels need encoded as well, so that the 100 labels will be represented as 100 binary values in an array. This can be done with the [MultiLabelBinarizer](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MultiLabelBinarizer.html) from the sklearn library.

# In[ ]:


from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import MultiLabelBinarizer

multilabel_binarizer = MultiLabelBinarizer()
multilabel_binarizer.fit(df_questions.Tags)
labels = multilabel_binarizer.classes_

maxlen = 180
max_words = 5000
tokenizer = Tokenizer(num_words=max_words, lower=True)
tokenizer.fit_on_texts(df_questions.Text)

def get_features(text_series):
    """
    transforms text data to feature_vectors that can be used in the ml model.
    tokenizer must be available.
    """
    sequences = tokenizer.texts_to_sequences(text_series)
    return pad_sequences(sequences, maxlen=maxlen)


def prediction_to_label(prediction):
    tag_prob = [(labels[i], prob) for i, prob in enumerate(prediction.tolist())]
    return dict(sorted(tag_prob, key=lambda kv: kv[1], reverse=True))


# In[ ]:


from sklearn.model_selection import train_test_split

x = get_features(df_questions.Text)
y = multilabel_binarizer.transform(df_questions.Tags)
print(x.shape)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=9000)


# ## Imbalanced Classes
# Some tags occur more often than others, thus the classes are not well balanced. The imbalanced class problem can be addressed by applying class weights, thus  weighting less frequent tags higher than very frequent tags.

# In[ ]:


most_common_tags['class_weight'] = len(df_tags) / most_common_tags['count']
class_weight = {}
for index, label in enumerate(labels):
    class_weight[index] = most_common_tags[most_common_tags['Tag'] == label]['class_weight'].values[0]
    
most_common_tags.head()


# ## Building a 1D Convolutional Neural Network

# In[ ]:


from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding, Flatten, GlobalMaxPool1D, Dropout, Conv1D
from keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint
from keras.losses import binary_crossentropy
from keras.optimizers import Adam

filter_length = 300

model = Sequential()
model.add(Embedding(max_words, 20, input_length=maxlen))
model.add(Dropout(0.1))
model.add(Conv1D(filter_length, 3, padding='valid', activation='relu', strides=1))
model.add(GlobalMaxPool1D())
model.add(Dense(num_classes))
model.add(Activation('sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['categorical_accuracy'])
model.summary()

callbacks = [
    ReduceLROnPlateau(), 
    EarlyStopping(patience=4), 
    ModelCheckpoint(filepath='model-conv1d.h5', save_best_only=True)
]

history = model.fit(x_train, y_train,
                    class_weight=class_weight,
                    epochs=20,
                    batch_size=32,
                    validation_split=0.1,
                    callbacks=callbacks)


# In[ ]:


cnn_model = keras.models.load_model('model-conv1d.h5')
metrics = cnn_model.evaluate(x_test, y_test)
print("{}: {}".format(model.metrics_names[0], metrics[0]))
print("{}: {}".format(model.metrics_names[1], metrics[1]))

