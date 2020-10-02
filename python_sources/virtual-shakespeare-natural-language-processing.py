#!/usr/bin/env python
# coding: utf-8

# ## Virtual Shakespeare - Natural Language Processing
# <img src="https://upload.wikimedia.org/wikipedia/commons/a/a2/Shakespeare.jpg" width="200" height="200"/>
# 
# #### Hola folks! Don't be fooled by the clickbait title.<br> In this quest to recreate Shakespeare, I was partly successful. Actually, no I wasn't.<br> Still, I was able to create a 3 year old Shakespeare, with some broken words and a bit of a hate for grammar.
# 
# #### Okay, coming to this notebook. I have used a dataset of Shakespeare's works to train a model, which on giving an input text, will produce an output text of desired length.
# 
# #### In the output text, you can observe that they follow the same structure as shakespeare's works, uses similar words and similar dialogues.<br> This output text is completely computer generated and not a subset of the dataset. 
# 
# #### The dataset has over 5 million characters, and 84 distinct characters.
# 
# ##### I will not be documenting the entire notebook, although comments have been provided for easy understanding.<br>As I am still learning NLP, some part of this notebook might not be correct or it may contain things that don't make sense. I'm really sorry about those. 
# 
# ### Corrections and improvements to this notebook are most welcome. It will really help me in learning more.
# 
# ### Do upvote it, if you like it!

# ####  I have provided a sample output at the top, please go through the entire notebook, to understand how it all works. 

# In[ ]:


#Sample output
print(generate_text(model, 'Et tu, Brute?', gen_size = 1000))


# In[ ]:


#importing libraries and packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf


# In[ ]:


#load the dataset containing shakespeare's works
text = open('../input/shakespeare.txt', 'r').read()
print(text[:1000])


# # Dataset Statistics

# In[ ]:


total_char = len(list(text))
unique_char = len(set(text))

text_cleaned = ''
alphalist = [chr(i) for i in range(ord('A'), ord('z')+1)]

for i in text:
    if i.isalpha():
        text_cleaned += i
    else:
        text_cleaned += ' '

char_count = {}
for i in text_cleaned.split():
    if i in char_count:
        char_count[i] += 1
    else:
        char_count[i] = 1
        
df = pd.DataFrame(char_count.items(), columns=['Words','Count'])
df.sort_values('Count', axis=0, ascending=False, inplace=True)
df.reset_index(drop=True, inplace=True)


# In[ ]:


print('Total Characters: ', total_char)
print('Unique Characters: ', unique_char)
print('Most used words:')
display(df.head(10))


# # Text Preprocessing

# In[ ]:


#Get all the unique characters
vocab = sorted(set(text))
vocab_size = len(vocab)
print(vocab)
print('Total uniques characters: ',vocab_size)


# In[ ]:


#Map characters to numbers and numbers to characters
char_to_ind = {u:i for i,u in enumerate(vocab)}
ind_to_char = {i:u for i,u in enumerate(vocab)}
print(char_to_ind)
print('\n')
print(ind_to_char)


# In[ ]:


#encode the first 1000 characters as numbers
encoded_text = np.array([char_to_ind[c] for c in text])
print(encoded_text[:1000])


# # Training Sequence

# In[ ]:


#number of sequences to generate
seq_len = 120
total_num_seq = len(text)//(seq_len+1)
print('Total Number of Sequences: ', total_num_seq)


# In[ ]:


#Create training sequences
#tf.data.Dataset.from_tensor_slices function converts a text vector
#into a stream of character indices
char_dataset = tf.data.Dataset.from_tensor_slices(encoded_text)

for i in char_dataset.take(500):
    print(ind_to_char[int(i)],end="")


# In[ ]:


#batch method converts these individual character calls into sequences
#which we can feed in as a batch
#we use seq_len+1 because we will use seq_len characters
#and shift them one step forward
#drop remainder drops the remaining characters < batch_size
sequences = char_dataset.batch(seq_len+1, drop_remainder=True)


# In[ ]:


#this function will grab a sequence
#take the [0:n-1] characters as input text
#take the [1:n] characters as target text
#return a tuple of both
def create_seq_targets(seq):
    input_txt = seq[:-1]
    target_txt = seq[1:]
    return input_txt, target_txt


# In[ ]:


#this will convert the series of sequences into
#a series of tuple containing input and target text
dataset = sequences.map(create_seq_targets)


# In[ ]:


for input_txt, target_txt in dataset.take(1):
    print(''.join([ind_to_char[i] for i in np.array(input_txt)]))
    print('\n')
    print(''.join([ind_to_char[i] for i in np.array(target_txt)]))

#the target is shifter 1 character forward
#the last character is a space and is thus not visible


# # Generating training batches

# In[ ]:


batch_size = 128 #number of sequence tuples in each batch
buffer_size = 10000 #shuffle this many sequences in the dataset

#first shuffle the dataset and divide it into batches
#drop the last sequences < batch_size
dataset = dataset.shuffle(buffer_size).batch(batch_size, drop_remainder=True)


# In[ ]:


#count the number of batches
#i couldn't find a function to do it in O(1)
#please let me know

x = 0
for i in dataset:
    x += 1


# In[ ]:


print('Total Batches:', x)
print('Sequences in each batch: ', batch_size)
print('Characters in each sequence:', seq_len)
print('Characters in dataset: ', len(list(text)))


# # Creating the Model

# In[ ]:


#importing keras modules
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense,Embedding,Dropout,GRU
from tensorflow.keras.losses import sparse_categorical_crossentropy


# In[ ]:


#using sparse_categorical_crossentropy because
#out predictions will be numbers and not one hot encodings
#we need to define a custom loss function so that we can change
#the from_logits parameter to True
def sparse_cat_loss(y_true, y_pred):
    return sparse_categorical_crossentropy(y_true, y_pred, from_logits=True)


# In[ ]:


def create_model(batch_size):
    vocab_size_func = vocab_size
    embed_dim = 64 #the embedding dimension
    rnn_neurons = 1024 #number of rnn units
    batch_size_func = batch_size
    
    model = Sequential()
    
    model.add(Embedding(vocab_size_func, 
                        embed_dim, 
                        batch_input_shape=[batch_size_func, None]))
    model.add(GRU(rnn_neurons, 
                  return_sequences=True, 
                  stateful=True, 
                  recurrent_initializer='glorot_uniform'))
    
    model.add(Dense(vocab_size_func))    
    model.compile(optimizer='adam', loss=sparse_cat_loss)    
    
    return model


# In[ ]:


model = create_model(batch_size)
model.summary()


# # Training the Model

# #### As we have  created the model, random weights and biases have been assigned, so before begining training lets first check whether the model is working or not.

# In[ ]:


#note this will generate random characters
#dataset.take(1) contains 1 batch = 128 sequence tuples
#model will output 120 characters per sequence
#in the form of probability of those 84 vocab characters
for ex_input, ex_target in dataset.take(1):
    ex_pred = model(ex_input)
print(ex_pred.shape)

#changes the character probabilities to integers
sampled_indices = tf.random.categorical(ex_pred[0], num_samples=1)

#maps those integers to characters
char_pred = ''.join([ind_to_char[int(i)] for i in sampled_indices])

print(char_pred)


# In[ ]:


#training the model
model.fit(dataset, epochs=30, verbose=1)


# In[ ]:


#save the model
model.save('shakespeare.h5')


# # Generating text

# In[ ]:


# importing load_model to load the keras model
from tensorflow.keras.models import load_model


# In[ ]:


#create a new model with a batch size of 1
model = create_model(batch_size=1)

#load the weights from the previous model to our new model
model.load_weights('shakespeare.h5')

#build the model
model.build(tf.TensorShape([1, None]))

#view model summary
print(model.summary())


# In[ ]:


#function to generate text based on an input text
#we enter the text on which our output will be based
#we define how many characters we want in output

def generate_text(model, start_seed, gen_size=100):
    num_generate = gen_size
    input_eval = [char_to_ind[s] for s in start_seed]
    input_eval = tf.expand_dims(input_eval, 0)
    
    text_generated = []
    
    model.reset_states()
    
    for i in range(num_generate):
        predictions = model(input_eval)
        predictions = tf.squeeze(predictions, 0)
        
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1, 0].numpy()
        
        input_eval = tf.expand_dims([predicted_id], 0)
        
        text_generated.append(ind_to_char[predicted_id])
        
    return (start_seed + ''.join(text_generated))


# In[ ]:


#generate a text based on input
#note that, this out is not part of the dataset
#but completely auto generated
auto_text = generate_text(model, 'How art thou?', gen_size = 1000)
print(auto_text)


# In[ ]:


#download the saved model
model.save('shakespeare.h5')
from IPython.display import FileLink
FileLink(r'shakespeare.h5')

