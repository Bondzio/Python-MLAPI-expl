#!/usr/bin/env python
# coding: utf-8

# This initial concept is based upon [this Medium post](https://medium.com/@curiousily/making-a-predictive-keyboard-using-recurrent-neural-networks-tensorflow-for-hackers-part-v-3f238d824218) by Venelin Valkov. The model from the article has been modified in this notebook to allow multiple LSTM layers, and to accept prediction inputs of less than the maximum sequence length.
# 
#  - Use a pre-trained model so that training starts from a better position

# In[ ]:


import numpy as np
import pandas as pd
import nltk


# # Import Corpuses
# 
# Next we will import the corpuses that we are going to use to train our model. These corpuses are taken from Project Gutenberg.

# In[ ]:


#nltk.download('gutenberg')
corpuses = [' '.join(list(nltk.corpus.gutenberg.words(corpus))) for corpus in nltk.corpus.gutenberg.fileids()][:2]
#corpus = list(nltk.corpus.gutenberg.words('carroll-alice.txt'))
#corpus_string = ' '.join(corpus)

print(len(corpuses), 'corpuses found')
print(sum([len(x) for x in corpuses]), 'characters in corpuses')


# We will need a unique list of characters that are found in our corpus. We will also need two dictionaries that allow us to convert our characters into unique integers and vice versa, so they will also be created below. We define two extra characters that can be used by our model; the first is a padding character so that we can take smaller inputs, while the second is an unknown character incase we come across characters that were not in our training data.

# In[ ]:


PADDING_CHAR = -1
UNKNOWN_CHAR = -2


# In[ ]:


characters = sorted(list(set(''.join(corpuses))))
char_indices = dict((c, i) for i, c in enumerate(characters))
indices_char = dict((i, c) for i, c in enumerate(characters))

char_indices[''] = PADDING_CHAR
indices_char[PADDING_CHAR] = ''
indices_char[UNKNOWN_CHAR] = ''

print(len(characters), 'unique characters in the corpus')


# In[ ]:


def string_to_indices(string, ind_map=char_indices):
    return [ind_map[c] if c in ind_map else UNKNOWN_CHAR for c in string]

def indices_to_string(indices, char_map=indices_char):
    return ''.join([char_map[i] for i in indices])

def char_to_probabilities(char, chars=characters):
    return [1 if c==char else 0 for c in chars]


# # Prepare Training Data
# 
# Now we will split our corpus into training data, where each data point has a size SEQUENCE_LENGTH. In this case we will use a sequence length of 40, meaning our predictions will be based on 40 previous characters. STEP allows us to choose how many data points we have, as each data point will be separated by STEP characters. Setting STEP to 1 allows us to select every possible point.

# In[ ]:


SEQUENCE_LENGTH = 40
STEP = 1

sentences = []
next_chars = []
for corpus_string in corpuses:
    for i in range(0, len(corpus_string) - 1, STEP):
        sentences.append(corpus_string[i: i + SEQUENCE_LENGTH])
        next_chars.append(corpus_string[min(i + SEQUENCE_LENGTH, len(corpus_string) - 1)])

print(len(sentences), 'training data points')


# The following method allows us to convert our text into a list of indices that can be understood by our model. We will then prepare our sentences and characters from our corpus so they can be used to train our model.

# In[ ]:


def prepare_text_indices(text):
    ind_text = string_to_indices(text)
    if len(ind_text) < SEQUENCE_LENGTH:
        ind_text = ([PADDING_CHAR] * (SEQUENCE_LENGTH - len(ind_text))) + ind_text
    elif len(ind_text) > SEQUENCE_LENGTH:
        ind_text = ind_text[-SEQUENCE_LENGTH:]
    return np.array(ind_text) / len(characters)


# In[ ]:


X_train = np.array([prepare_text_indices(s) for s in sentences])
X_train = X_train.reshape((X_train.shape[0], SEQUENCE_LENGTH, 1))
Y_train = np.array([char_to_probabilities(c) for c in next_chars])


# # Build Model

# The following cells will be used to build and train our model. The first cell defines our model architecture. It also allows us to load model weights if we have saved them previously. This method is used in the second cell, where we train our model and then reload the best weights (in terms of training loss).

# In[ ]:


from keras.models import Sequential, load_model
from keras.layers import Dense, Activation
from keras.layers import LSTM, Dropout
from keras.layers import TimeDistributed
from keras.layers.core import Dense, Activation, Dropout, RepeatVector
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint

def build_model(input_shape, output_shape, weight_path=None):
    model = Sequential()
    model.add(LSTM(512, input_shape=input_shape, return_sequences=True, dropout=0.25))
    #model.add(LSTM(512, return_sequences=True, dropout=0.25))
    model.add(LSTM(512, dropout=0.25))
    model.add(Dense(output_shape))
    model.add(Activation('softmax'))
    
    if weight_path != None:
        model.load_weights(weight_path)
    
    optimizer = Adam(learning_rate=0.001)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    return model


# In[ ]:


# Get model architecture
model = build_model((SEQUENCE_LENGTH, 1), len(characters), weight_path='../input/predictive-text-model-weights/weights-512-512.hdf5')

# Fit model and save best weights
checkpoint = ModelCheckpoint('weights-512-512.hdf5', monitor='loss', verbose=1, save_best_only=True, mode='min')
model.fit(X_train, Y_train, batch_size=512, epochs=50, shuffle=True, callbacks=[checkpoint])

# Load trained weights
model = build_model((SEQUENCE_LENGTH, 1), len(characters), weight_path='weights-512-512.hdf5')


# # Make Predictions
# We are going to create two functions that will allow us to make predictions. The first function will take our text and predict the next character. The second function will take our text and predict the next word (or word ending) by making use of our first function.

# In[ ]:


def make_char_prediction(text, model=model, pred_length=SEQUENCE_LENGTH):
    ind_text = prepare_text_indices(text)
        
    X_text = np.array(ind_text).reshape((1, pred_length, 1))
    pred = model.predict(X_text)
    top_pred = np.argmax(pred)
    char_pred = characters[top_pred]
    return char_pred

def make_word_prediction(text, model=model, min_length=2, pred_length=SEQUENCE_LENGTH):
    pred_text = ''
    while True:
        x = (text + pred_text)[-SEQUENCE_LENGTH:]
        pred = make_char_prediction(x, model)
        pred_text += pred
        if len(pred_text) >= min_length and (pred == ' '):
            return pred_text


# Now we will take a few examples and make some predictions.

# In[ ]:


test_texts = ["I\'ve believed as many as six impossible ",
              "no use going back to yesterday, because ",
              "A pessimist sees the difficulty in every",
              "sometimes you just have to create a rand",
              "The score was nil nil until the striker ",
              "if I could dream of such things then the",
              "We should follow the path on the left as",
              "Let\'s write a short program to display a",
              "no"]

test_preds = []
test_preds_long = []
for text in test_texts:
    test_preds.append(make_word_prediction(text, model=model))
    test_preds_long.append(make_word_prediction(text, model=model, min_length=10))

pd.DataFrame({'Text' : test_texts, 'Prediction' : test_preds, 'Long Prediction' : test_preds_long})


# In[ ]:


long_test_text = 'We should follow the path on the left as'
new_long_test_text = long_test_text + make_word_prediction(long_test_text, model=model, min_length=20)

print('Original:', long_test_text)
print('New:     ', new_long_test_text)

