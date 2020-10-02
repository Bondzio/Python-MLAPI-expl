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


img_dir = "../input/flickr30k_images/flickr30k_images/flickr30k_images"
results = "../input/flickr30k_images/flickr30k_images/results.csv"


# In[ ]:


df = pd.read_csv(results, error_bad_lines=False)


# In[ ]:


data = list(df[df.columns[0]])


# In[ ]:


mapping = {}

key = data[0].split('.jpg')[0]
mapping[key] = []

i = 0

for d in data:
     
    i += 1
        
    if d.split('.jpg')[0] != key:
        key = d.split('.jpg')[0]
        mapping[key] = []
    if i == 18005:    
        mapping[key].append(" ".join(d.split()[2:]))
        continue
        
    mapping[key].append(d.split('|')[2])


# In[ ]:


len(mapping)


# In[ ]:


cleaned_mapping = {}

for key, desc in mapping.items():
    if len(mapping[key]) == 3:
        cleaned_mapping[key] = mapping[key]


# In[ ]:


import re
import string

mapping = {}

re_punc = re.compile( '[%s]' % re.escape(string.punctuation))
for key, descs in cleaned_mapping.items():
    mapping[key] = []
    for desc in descs:
        desc = desc.split()
        desc = [word.lower() for word in desc]
        desc = [re_punc.sub( '' , w) for w in desc]
        desc = [word for word in desc if len(word)>1]
        desc = ' '.join(desc)
        mapping[key].append(desc)


# In[ ]:


from keras.preprocessing.image import load_img, img_to_array


# In[ ]:


from keras.applications.vgg16 import VGG16
from keras.models import Model

model = VGG16()
model.layers.pop()
model = Model(inputs=model.inputs, outputs=model.layers[-1].output)
model.summary()


# In[ ]:


from keras.applications.vgg16 import preprocess_input

features = {}

for key in mapping.keys():
    img = load_img(img_dir + '/' + key + '.jpg', target_size=(224, 224))
    img = img_to_array(img)
    img = img.reshape((1, img.shape[0], img.shape[1], img.shape[2]))
    img = preprocess_input(img)
    feature = model.predict(img, verbose=0)
    features[key] = feature
    print(key)


# In[ ]:


desc = []

for ds in list(mapping.values()):
    for d in ds:
        desc.append(d)


# In[ ]:


descs = []

for d in desc:
    d = d.split()
    d.insert(0, 'START')
    d.append('END')
    descs.append(' '.join(d))


# In[ ]:


from keras.preprocessing.text import Tokenizer
# prepare tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(descs)
vocab_size = len(tokenizer.word_index) + 1
print( ' Vocabulary Size: %d ' % vocab_size)


# In[ ]:


encoded = tokenizer.texts_to_sequences(descs) 


# In[ ]:


label = list(features.keys())


# In[ ]:


sequence = []

labels = []
i = 0

for desc in encoded:
    
    l = label[int(i/3)]
    i += 1
    for j in range(1, len(desc)):
        d = desc[0:j+1]
        sequence.append(d)
        labels.append(l)


# In[ ]:


max_length = max([len(s) for s in sequence]) 


# In[ ]:


max_length


# In[ ]:


from keras.preprocessing.sequence import pad_sequences

sequence = pad_sequences(sequence, maxlen = max_length, padding = 'pre')


# In[ ]:


from numpy import array
sequence = array(sequence)


# In[ ]:


sequence.shape


# In[ ]:


x , y = sequence[:,:-1], sequence[:,-1]


# In[ ]:


from keras.utils import to_categorical

y = to_categorical(y, num_classes = vocab_size)


# In[ ]:


from keras.layers import Input, LSTM, Dense,Embedding, Dropout
from keras.layers.merge import add
from keras.callbacks import ModelCheckpoint


# In[ ]:


input1 = Input(shape = (4096, ))
fe1 = Dropout(0.25)(input1)
fe2 = Dense(256, activation='relu')(fe1)


# In[ ]:


input2 = Input(shape = (max_length - 1,))
se1 = Embedding(vocab_size, 256, mask_zero=True)(input2)
se2 = Dropout(0.5)(se1)
se3 = LSTM(256)(se2)


# In[ ]:


decoder1 = add([fe2, se3])
decoder2 = Dense(256, activation= 'relu' )(decoder1)
outputs = Dense(vocab_size, activation= 'softmax' )(decoder2)


# In[ ]:


model = Model(inputs=[input1, input2], outputs=outputs)


# In[ ]:


model.compile(loss= 'categorical_crossentropy' , optimizer= 'adam' )


# In[ ]:


model.summary()


# In[ ]:


checkpoint = ModelCheckpoint( 'model.h5' , monitor= 'loss' , verbose=1, save_best_only=True, mode= 'min' )


# In[ ]:


photos = []

for label in labels:
    photos.append(features[label])


# In[ ]:


features = []
for i in range(len(photos)):
    features.append(photos[i][0])


# In[ ]:


from numpy import array

features = array(features)


# In[ ]:


model.fit([features, x], y, epochs = 20, verbose=1, callbacks=[checkpoint])


# In[ ]:




