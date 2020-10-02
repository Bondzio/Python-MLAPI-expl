#!/usr/bin/env python
# coding: utf-8

# # Pythonic Python Script for Making Monty Python Scripts
# The python language was named after Monty Python's Flying Circus so why not use python to generate an unlimited supply of new Monty Python scripts? This notebook is a compressed version of my text generating AI. Text generator like this one require a lot of computational power so it only became really feasible to do them on Kaggle Kernels when they upgraded to have a GPU and a 6 hour computational limit. Even so, 6 hours is still kind of lean for an LSTM text generator but I can make it work quite well anyways. 
# 
# The goal of this notebook is to serve as a introduction to text generation NLPs. These LSTM text generator are actually not that difficult to make. However, most tutorials on the topic are incomplete and/or generate poor results. I'll try to talk about every step of the process thoroughly and clearly. Other than that, this notebook is pretty easy to adapt to any text generation you might want to do. Just pop in any sizeable txt file and the model will learn to make more text in that style. Things like Shakespeare are common and work well for this type of text generation. Make sure that GPU is enabled in settings. Now lets make an AI generate something completely different.
# 
# ## Imports
# As always, a block of imports.
# 

# In[ ]:


import numpy as np
import pandas as pd
import keras as K
import random
import sqlite3

from keras.layers import Input, Dropout, Dense, concatenate, Embedding
from keras.layers import Flatten, Activation
from keras.optimizers import Adam
from keras.models import Model
from keras.utils import np_utils

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.models import load_model
from keras.layers import LSTM, CuDNNGRU, CuDNNLSTM
from keras.layers import MaxPooling1D
from keras.callbacks import EarlyStopping, ModelCheckpoint, Callback

import warnings
warnings.filterwarnings('ignore')
import os
print(os.listdir("../input"))


# # Changing Database into Text
# The first thing that needs to be done is change the Monty Python database into one nice long string of all the scripts. Originally, I tried putting both the directions and dialogue into the text. However, since there are so many directions this ends up making a script that is mostly stuff like "cut to a picture of a man in the street." or "cut to stock video of a train" ect. We will just focus on the dialogue to make something more interesting to read. 

# In[ ]:


conn = sqlite3.connect('../input/database.sqlite')
df = pd.read_sql(con=conn, sql='select * from scripts')

df.character = df.character.astype(str)
df.actor = df.actor.astype(str)
df.segment = df.segment.astype(str)
df[:10]


# In[ ]:


get_ipython().run_cell_magic('time', '', "All_MP_Scripts = ''\nlast_seg = ''\n\nfor index, line in df.iterrows():\n    seg = line[3].lower()\n    type_of_line = line[4]\n    actor = line[5].lower()\n    character = line[6].lower()\n    detail = line[7].lower()\n    Script = ''\n    if seg != last_seg:\n        Script += '<scene '\n        if seg != 'none':\n            Script += seg\n        Script += '>\\n\\n'\n    if type_of_line != 'Direction':\n        Script += character+': '+ detail+' \\n\\n'\n    last_seg = seg\n    All_MP_Scripts += Script\n\nprint(All_MP_Scripts[:1000])")


# Now that we have our scripts, let's save it and move on to real work.

# In[ ]:


text_file = open("All_MP_Scripts.txt", "w")
text_file.write(All_MP_Scripts)
text_file.close()


# # Prep the Text for the RNN
# Next we will prepare an index of every unique character in our text. We are only getting rid of capitalization for simplicity, but still keeping all special characters. This will give us an output that retains the punctuation and format of the original. 
# 
# Note that if you want to replace the Monty Python scripts with some other text to duplicate, here would be the place to do it. Just replace the All_MP_Scripts with any other text file and the rest of the notebook will run the same. (the bigger the better, anything ~1MB+ is great) 

# In[ ]:


Text_Data = All_MP_Scripts.lower()

charindex = list(set(Text_Data))
charindex.sort() 
print(charindex)

np.save("charindex.npy", charindex)


# # Create Sequences
# In a nutshell, this model will look at the last 75 characters in the script and attempt to predict the 76th. Our X variable will be a 75 character sequence and our Y variable will be the 76th character. This block chops the text data into such sequences of characters. 
# 
# Note that this part also tokenizes the characters, which is to say it replaces each character with a number that corresponds to it's index in charindex. This is why it is important to save a copy of the charindex with your model just in case. We will need it to decode our predictions later.
# 

# In[ ]:


get_ipython().run_cell_magic('time', '', 'CHARS_SIZE = len(charindex)\nSEQUENCE_LENGTH = 75\nX_train = []\nY_train = []\nfor i in range(0, len(Text_Data)-SEQUENCE_LENGTH, 1 ): \n    X = All_MP_Scripts[i:i + SEQUENCE_LENGTH]\n    Y = All_MP_Scripts[i + SEQUENCE_LENGTH]\n    X_train.append([charindex.index(x) for x in X])\n    Y_train.append(charindex.index(Y))\n\nX_train = np.reshape(X_train, (len(X_train), SEQUENCE_LENGTH))\n\nY_train = np_utils.to_categorical(Y_train)')


# # Create the Model
# The model uses 3 LSTMs stacked on top of each. Adding another LSTM layer and/or running it a lot longer or in multiple session will give better results. However, the 3 LSTM should do fine in 6 hour and adding the loopbreaker to our code later will make even under trained models give good results. Also note that we are using CuDNNLSTMs. If you don't know what that is, it is a special LSTM layer specially made for NIVDA GPUs. These function the same as regular LSTM layers but are automatically optimised for the GPU. You lose some customization with these layers but they work roughly twice as fast as regular LSTMs layers if conditions are right.
# 

# In[ ]:


def get_model():
    model = Sequential()
    inp = Input(shape=(SEQUENCE_LENGTH, ))
    x = Embedding(CHARS_SIZE, 75, trainable=False)(inp)
    x = CuDNNLSTM(512, return_sequences=True,)(x)
    x = CuDNNLSTM(512, return_sequences=True,)(x)
    x = CuDNNLSTM(512,)(x)
    x = Dense(256, activation="elu")(x)
    x = Dense(128, activation="elu")(x)
    outp = Dense(CHARS_SIZE, activation='softmax')(x)
    
    model = Model(inputs=inp, outputs=outp)
    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(lr=0.001),
                  metrics=['accuracy'],
                 )

    return model

model = get_model()

model.summary()


# # Checkpoints and Custom Callback
# We will use 3 callbacks. Checkpoint, EarlyStopping, and a custom TextSample callback. Text sample prints a sample line at the end of every epoch to see how the model is progressing each epoch. For Kaggle, this is less important as you have to commit your code to run this long enough to output results.

# In[ ]:


filepath="model_checkpoint.hdf5"

checkpoint = ModelCheckpoint(filepath,
                             monitor='loss',
                             verbose=1,
                             save_best_only=True,
                             mode='min')

early = EarlyStopping(monitor="loss",
                      mode="min",
                      patience=1)


# In[ ]:


class TextSample(Callback):

    def __init__(self):
       super(Callback, self).__init__() 

    def on_epoch_end(self, epoch, logs={}):
        pattern = X_train[700]
        outp = []
        seed = [charindex[x] for x in pattern]
        sample = 'TextSample:' +''.join(seed)+'|'
        for t in range(100):
          x = np.reshape(pattern, (1, len(pattern)))
          pred = self.model.predict(x)
          result = np.argmax(pred)
          outp.append(result)
          pattern = np.append(pattern,result)
          pattern = pattern[1:len(pattern)]
        outp = [charindex[x] for x in outp]
        outp = ''.join(outp)
        sample += outp
        print(sample)

textsample = TextSample()


# 
# # Load Model
# Load models or weights here. For following up on partially trained models saved by checkpoint.

# In[ ]:


# model = load_model(filepath)


# 
# # Train Model
# Even with a GPU, this can take a while. As is, I'm setting this notebook to take almost the full 6 hour limit. I have played around with training these types of models for 12 or even 24 hours wit more layers.  However, usually if gotten to roughly around 1.0 loss the generator is good enough to go. Can train almost indefinitely on most models. We are not *really* worried about overfitting. Hypothetically, if the loss gets too low the text might become overfit, which in this case means just copying the text in the most inefficient way possible. However, it should take an unrealistically long time to get to that point (or just impossible).
# 

# In[ ]:


model_callbacks = [checkpoint, early, textsample]
model.fit(X_train, Y_train,
          batch_size=256,
          epochs=15,
          verbose=1,
          callbacks = model_callbacks)


# # Save the Model
# Training is done, save it. This is also a great place to load any pretrained models before generating new text.

# In[ ]:


# model = load_model(filepath)
model.save_weights("full_train_weights.hdf5")
model.save("full_train_model.hdf5")


# # Generating New Monty Python Scripts
# This block generates new text in the style of the input text of TEXT_LENGTH size in characters. It takes a random seed pattern from the training set, predicts the next character, adds it to the end of the pattern, then drops the first character of the pattern and predicts on the new pattern and so forth.
# 
# Pretty much this text generator *tries* to accurately duplicate the Monty Python script but inevitably makes errors ,and those errors compound, but is still trained well enough that it ends up making Monty Python *like* scripts 
# 
# ## The Loopbreaker
# This is simple bit of I came up with while putting this together. Every so many character predictions, the program just changes one of the characters in the pattern to predict on (except the last few, to prevent spelling errors). This causes our model to perceive a slightly different text which causes it to change it's overall predictions slightly too. Without this, even a well trained model might start to repeat itself at some point and get caught in a loop. The loopbreaker can even prevent overfitting or allow under trained models to perform much better. Without a loopbreaker like this, models will need to be trained for many more hours before they can function without looping in on themselves.
# 
# Changing this value up and down an interesting way to significantly change the output. Setting it high will have more repeated speech, slightly lower might get many line starting the same then vering off into different directions, really low will get lots of varied text but line structures and format might become unstable. Probably keep it somewhere between 1 and 10.
# 

# In[ ]:



get_ipython().run_cell_magic('time', '', 'TEXT_LENGTH  = 5000\nLOOPBREAKER = 3\n\n\nx = np.random.randint(0, len(X_train)-1)\npattern = X_train[x]\noutp = []\nfor t in range(TEXT_LENGTH):\n  if t % 500 == 0:\n    print("%"+str((t/TEXT_LENGTH)*100)+" done")\n  \n  x = np.reshape(pattern, (1, len(pattern)))\n  pred = model.predict(x, verbose=0)\n  result = np.argmax(pred)\n  outp.append(result)\n  pattern = np.append(pattern,result)\n  pattern = pattern[1:len(pattern)]\n  ####loopbreaker####\n  if t % LOOPBREAKER == 0:\n    pattern[np.random.randint(0, len(pattern)-10)] = np.random.randint(0, len(charindex)-1)')


# # Let's See the Results
# As you can see, the output is not bad. Text generators like this are pretty good on a line by line basis. Some of the lines and scene names seem really plausible as Monty Python dialogue. Plot and scene structure is off. Different characters show up talking about irrelevant things. In some ways that works wit Monty Python. Still, more AI structures are needed to keep track of the plot and such. Anyways, this is the extent of most AI text generation these days. This is why stuff like Shakespeare and poetry are popular by AI generation, abstract language makes imperfect text generation less detectable. 
# 
# A final thing I find interesting is that, while typos are generally few when trained well, the AI actually sometimes makes up new words in the same style. I guess this is from the AI making a typo but covering it with something that sounds right to it. So it is making some typos but they are just not overt and they seem like uncommon words. For example, once this script generated the phrase "I say some perpilly cricket". While that is a very british/Monty Python sounding phrase, the word perpilly does not appear in the original Monty Python scripts anywhere and is not a word in english at all! Something to look for when generating your now unlimited supply of Monty Python scripts.
# 

# In[ ]:


outp = [charindex[x] for x in outp]
outp = ''.join(outp)

print(outp)


# # Save Text Output

# In[ ]:


f =  open("output_text_sample.txt","w")
f.write(outp)
f.close()

