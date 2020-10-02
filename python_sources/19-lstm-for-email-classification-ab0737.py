#!/usr/bin/env python
# coding: utf-8

# # Ch. 19 - LSTM for Email classification
# 
# In the last chapter we already learned about basic recurrent neural networks. In theory, simple RNN's should be able to retain even long term memories. However, in practice, this approach often falls short. This is because of the 'vanishing gradients' problem. Over many timesteps, the network has a hard time keeping up meaningful gradients. See e.g. [Learning long-term dependencies with gradient descent is difficult (Bengio, Simard and Frasconi, 1994)](http://www.iro.umontreal.ca/~lisa/pointeurs/ieeetrnn94.pdf) for details.
# 
# In direct response to the vanishing gradients problem of simple RNN's, the Long Short Term Memory layer was invented. Before we dive into details, let's look at a simple RNN 'unrolled' over time:
# 
# ![Unrolled RNN](https://storage.googleapis.com/aibootcamp/Week%204/assets/unrolled_simple_rnn.png)

# You can see that this is the same as the RNN we saw in the previous chapter, just unrolled over time.
# 
# ## The Carry 
# The central addition of an LSTM over an RNN is the carry. The carry is like a conveyor belt which runs along the RNN layer. At each time step, the carry is fed into the RNN layer. The new carry gets computed in a separate operation from the RNN layer itself from the input, RNN output and old carry.
# 
# ![LSTM](https://storage.googleapis.com/aibootcamp/Week%204/assets/LSTM.png)

# The ``Compute Carry`` can be understood as three parts:
# 
# Determine what should be added from input and state:
# 
# $$i_t = a(s_t \cdot Ui + in_t \cdot Wi + bi)$$
# 
# $$k_t = a(s_t \cdot Uk + in_t \cdot Wk + bk)$$
# 
# where $s_t$ is the state at time $t$ (output of the simple rnn layer), $in_t$ is the input at time $t$ and $Ui$, $Wi$ $Uk$, $Wk$ are model parameters (matrices) which will be learned. $a()$ is an activation function.
# 
# Determine what should be forgotten from state an input:
# 
# $$f_t = a(s_t \cdot Uf) + in_t \cdot Wf + bf)$$
# 
# The new carry is the computed as 
# 
# $$c_{t+1} = c_t * f_t + i_t * k_t$$
# 
# While the standard theory claims that the LSTM layer learns what to add and what to forget, in practice nobody knows what really happens inside an LSTM. However, they have been shown to be quite effective at learning long term memory.
# 
# Note that ``LSTM``layers do not need an extra activation function as they already come with a tanh activation function out of the box.

# ## The Data
# 
# Without much further ado, let's dive into the task of this chapter. The [Newsgroup 20 Dataset](http://qwone.com/~jason/20Newsgroups/) is a collection of about 20,000 messages from 20 newsgroups. [Usenet Newsgroups](https://en.wikipedia.org/wiki/Usenet_newsgroup) where a form of discussion group that where quite popular in the early days of the Internet. They are technically distinct but functionally quite similar to web forums. The newsgroups where usually dedicated to a certain topic, such as cars or apple computers. We can download the newsgroup 20 dataset directly through scikit learn.

# In[ ]:


get_ipython().system('ls ../input')


# In[ ]:


from sklearn.datasets.base import get_data_home, _pkl_filepath
import os
CACHE_NAME = "20news-bydate.pkz"
TRAIN_FOLDER = "20news-bydate-train"
TEST_FOLDER = "20news-bydate-test"

data_home = get_data_home()
print(data_home)
cache_path = _pkl_filepath(data_home, CACHE_NAME)
print(cache_path)
twenty_home = os.path.join(data_home, "20news_home")
print(twenty_home)

if not os.path.exists(data_home):
    os.makedirs(data_home)
    
if not os.path.exists(twenty_home):
    os.makedirs(twenty_home)


# In[ ]:


os.path.exists(data_home)


# In[ ]:


get_ipython().system('ls /tmp')


# In[ ]:


get_ipython().system('cp ../input/20-newsgroup-sklearn/20news-bydate_py3* /tmp/scikit_learn_data')


# In[ ]:


os.path.exists(cache_path)


# In[ ]:


from sklearn.datasets import fetch_20newsgroups
twenty_train = fetch_20newsgroups(subset='train', shuffle=True, download_if_missing=False)


# The posts in the newsgroup are very similar to emails. (The \n in the text means a line break)

# In[ ]:


twenty_train.data[1]


# From the text you might be able to judge that this text is about computer hardware. More specifically it is about Apple computers. You are not expected to have expertise in the discussions around Macs in the 90's so we can also just look at a label:

# In[ ]:


twenty_train.target_names[twenty_train.target[1]]


# ## Preprocessing the data
# 
# You already learned that we have to tokenize the text before we can feed it into a neural network. This tokenization process will also remove some of the features of the original text, such as all punctuation or words that are less common.

# In[ ]:


texts = twenty_train.data # Extract text


# In[ ]:


target = twenty_train.target # Extract target


# In[ ]:


# Load tools we need for preprocessing
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


# Remember we have to specify the size of our vocabulary. Words that are less frequent will get removed. In this case we want to retain the 20,000 most common words.

# In[ ]:


vocab_size = 20000


# In[ ]:


tokenizer = Tokenizer(num_words=vocab_size) # Setup tokenizer
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts) # Generate sequences


# In[ ]:


word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))


# Our text is now converted to sequences of numbers. It makes sense to convert some of those sequences back into text to check what the tokenization did to our text. To this end we create an inverse index that maps numbers to words while the tokenizer maps words to numbers.

# In[ ]:


# Create inverse index mapping numbers to words
inv_index = {v: k for k, v in tokenizer.word_index.items()}


# In[ ]:


# Print out text again
for w in sequences[1]:
    x = inv_index.get(w)
    print(x,end = ' ')


# ### Measuring text length
# 
# In previous chapters, we specified a sequence length and made sure all sequences had the same length. For LSTMs this is not strictly necessary as LSTMs can work with different lengths of sequences. However, it can be a pretty good idea to restrict sequence lengths for the sake of restricting the time needed to train the network and process sequences.

# In[ ]:


import numpy as np


# In[ ]:


# Get the average length of a text
avg = sum( map(len, sequences) ) / len(sequences)

# Get the standard deviation of the sequence length
std = np.sqrt(sum( map(lambda x: (len(x) - avg)**2, sequences)) / len(sequences))

avg,std


# You can see, the average text is about 300 words long. However, the standard deviation is quite large which indicates that some texts are much much longer. If some user decided to write an epic novel in the newsgroup it would massively slow down training. So for speed purposes we will restrict sequence length to 100 words. You should try out some different sequence lengths and experiment with processing time and accuracy gains.

# In[ ]:


max_length = 100


# In[ ]:


data = pad_sequences(sequences, maxlen=max_length)


# ## Turning labels into One-Hot encodings
# 
# Labels can quickly be encoded into one-hot vectors with Keras:

# In[ ]:


import numpy as np
from keras.utils import to_categorical
labels = to_categorical(np.asarray(target))
print('Shape of data:', data.shape)
print('Shape of labels:', labels.shape)


# ## Loading GloVe embeddings
# 
# We will use GloVe embeddings as in the chapters before. This code has been copied from previous chapters:

# In[ ]:


import os
glove_dir = '../input/glove-global-vectors-for-word-representation' # This is the folder with the dataset

embeddings_index = {} # We create a dictionary of word -> embedding
f = open(os.path.join(glove_dir, 'glove.6B.100d.txt')) # Open file

# In the dataset, each line represents a new word embedding
# The line starts with the word and the embedding values follow
for line in f:
    values = line.split()
    word = values[0] # The first value is the word, the rest are the values of the embedding
    embedding = np.asarray(values[1:], dtype='float32') # Load embedding
    embeddings_index[word] = embedding # Add embedding to our embedding dictionary
f.close()

print('Found %s word vectors.' % len(embeddings_index))


# In[ ]:


# Create a matrix of all embeddings
all_embs = np.stack(embeddings_index.values())
emb_mean = all_embs.mean() # Calculate mean
emb_std = all_embs.std() # Calculate standard deviation
emb_mean,emb_std


# In[ ]:


embedding_dim = 100 # We use 100 dimensional glove vectors


# In[ ]:


word_index = tokenizer.word_index
nb_words = min(vocab_size, len(word_index)) # How many words are there actually

# Create a random matrix with the same mean and std as the embeddings
embedding_matrix = np.random.normal(emb_mean, emb_std, (nb_words, embedding_dim))

# The vectors need to be in the same position as their index. 
# Meaning a word with token 1 needs to be in the second row (rows start with zero) and so on

# Loop over all words in the word index
for word, i in word_index.items():
    # If we are above the amount of words we want to use we do nothing
    if i >= vocab_size: 
        continue
    # Get the embedding vector for the word
    embedding_vector = embeddings_index.get(word)
    # If there is an embedding vector, put it in the embedding matrix
    if embedding_vector is not None: 
        embedding_matrix[i] = embedding_vector


# ## Using the LSTM layer
# 
# In Keras, the LSTM layer can be used in exactly the same way as the ``SimpleRNN``layer we used earlier. It only takes the size of the layer as an input, much like a dense layer. An LSTM layer returns only the last output of the sequence by default, just like a ``SimpleRNN``. A simple LSTM network can look like this:

# In[ ]:


from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation, Embedding


# In[ ]:


model = Sequential()
model.add(Embedding(vocab_size, 
                    embedding_dim, 
                    input_length=max_length, 
                    weights = [embedding_matrix], 
                    trainable = False))
model.add(LSTM(128))
model.add(Dense(20))
model.add(Activation('softmax'))
model.summary()


# In[ ]:


model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['acc'])

model.fit(data,labels,validation_split=0.2,epochs=2)


# Our model achieves more than 95% accuracy on the validation set in only 2 epochs. Systems like these can be used to assign emails in customer support centers, suggest responses, or classify other forms of text like invoices which need to be assigned to an department. Let's take a look at how our model classified one of the texts:

# In[ ]:


example = data[20] # get the tokens
print(example)


# In[ ]:





# In[ ]:


# Print tokens as text
for w in example:
    x = inv_index.get(w)
    print(x,end = ' ')


# In[ ]:


# Get prediction
pred = model.predict(example.reshape(1,100))


# In[ ]:


# Output predicted category
twenty_train.target_names[np.argmax(pred)]


# ## Recurrent Dropout
# 
# You have already heard of dropout. Dropout removes some elements of one layers input at random. A common and important tool in recurrent neural networks is [_recurrent dropout_](https://arxiv.org/pdf/1512.05287.pdf). Recurrent dropout does not remove any inputs between layers but inputs between _time steps_.
# 
# ![Recurrent Dropout](https://storage.googleapis.com/aibootcamp/Week%204/assets/recurrent_dropout.png)
# 
# Just as regular dropout, recurrent dropout has a regularizing effect and can prevent overfitting. It is used in Keras by simply passing an argument to the LSTM or RNN layer. Recurrent Dropout, unlike regular dropout, does not have an own layer.

# In[ ]:


model = Sequential()
model.add(Embedding(vocab_size, 
                    embedding_dim, 
                    input_length=max_length, 
                    weights = [embedding_matrix], 
                    trainable = False))

# Now with recurrent dropout with a 10% chance of removing any element
model.add(LSTM(128, recurrent_dropout=0.1)) 
model.add(Dense(20))
model.add(Activation('softmax'))
model.summary()


# In[ ]:


model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['acc'])

model.fit(data,labels,validation_split=0.2,epochs=2)


# ## Summary
# In this chapter you have learned about LSTMs and how to use them for email classification. You also learned about recurrent dropout. Before you head into the weekly challenge, try these exercises:
# 
# ## Exercises:
# - Try running the LSTM with a longer max sequence length, or no max sequence length
# - Try combining an LSTM with a Conv1D. A good idea is to first use a ``Conv1D`` layer, followed by a ``MaxPooling1D`` layer followed by an LSTM layer. This will allow you to use longer sequences at reasonable speed.
# - Try using a [``GRU``](https://keras.io/layers/recurrent/#gru). GRUs work a lot like LSTMs but are a bit faster and simpler.
