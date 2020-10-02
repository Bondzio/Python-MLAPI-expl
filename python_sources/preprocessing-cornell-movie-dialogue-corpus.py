#!/usr/bin/env python
# coding: utf-8

# 

# In[ ]:


import pandas as pd
import pickle as pkl
import random

# Which tokenizer to use? TweetTokenizer is more robust than the vanilla tokenizer, but then,
# will the intelligence of tokenization matter in the long run when trained using DL?
from nltk.tokenize import word_tokenize, TweetTokenizer
tokenizer = TweetTokenizer(preserve_case = False)

from gensim.models import Word2Vec, KeyedVectors


# ## Create a list of dialogues
# 
# We join two different files namely `movie_lines.tsv` and `movie_conversations.tsv` to finally produce a list of dialogues. This list is further stored as a `pickle` file for further processing.

# In[ ]:


movie_lines_features = ["LineID", "Character", "Movie", "Name", "Line"]
movie_lines = pd.read_csv("../input/movie-corpus/movie_lines.txt", sep = "\+\+\+\$\+\+\+", engine = "python", index_col = False, names = movie_lines_features)

# Using only the required columns, namely, "LineID" and "Line"
movie_lines = movie_lines[["LineID", "Line"]]

# Strip the space from "LineID" for further usage and change the datatype of "Line"
movie_lines["LineID"] = movie_lines["LineID"].apply(str.strip)


# In[ ]:


movie_lines.head()


# In[ ]:


movie_conversations_features = ["Character1", "Character2", "Movie", "Conversation"]
movie_conversations = pd.read_csv("../input/movie-corpus/movie_conversations.txt", sep = "\+\+\+\$\+\+\+", engine = "python", index_col = False, names = movie_conversations_features)

# Again using the required feature, "Conversation"
movie_conversations = movie_conversations["Conversation"]


# In[ ]:


movie_conversations.head()


# In[ ]:


# This instruction takes lot of time, run it only once.
#conversation = [[str(list(movie_lines.loc[movie_lines["LineID"] == u.strip().strip("'"), "Line"])[0]).strip() for u in c.strip().strip('[').strip(']').split(',')] for c in movie_conversations]


# In[ ]:


with open("conversations.pkl", "wb") as handle:
    pkl.dump(conversation, handle)


# ## Create context and response pairs

# In[ ]:


with open("../input/processed-conversations/conversatons.pkl", "rb") as handle:
    conversation = pkl.load(handle)


# In[ ]:


# Calculate the dialogue length statistics

dialogue_lengths = [len(dialogue) for dialogue in conversation]
pd.Series(dialogue_lengths).describe()


# As observed above, the mean dialogue length is approximately 4 which is pretty less and we can take only the last utterence as the response. Yet to figure out a way to handle the larger ones though.

# In[ ]:


# Generate 50 sample pairs - 14/03/2019
indices = random.sample(range(len(conversation)), 50)
sample_context_list = []
sample_response_list = []

for index in indices:
    
    response = conversation[index][-1]
        
    context = "FS: " + conversation[index][0] + "\n"
    for i in range(1, len(conversation[index]) - 1):
        
        if i % 2 == 0:
            prefix = "FS: "
        else:
            prefix = "SS: "
            
        context += prefix + conversation[index][i] + "\n"
        
    sample_context_list.append(context)
    sample_response_list.append(response)

with open("cornell_movie_dialogue_sample.csv", "w") as handle:
    for c, r in zip(sample_context_list, sample_response_list):
        handle.write('"' + c + '"' + "#" + r + "\n")


# In[ ]:


def generate_pairs(conversation):
    
    context_list = []
    response_list = []
    
    for dialogue in conversation:
        
        response = word_tokenize(dialogue[-1])
        
        context = word_tokenize(dialogue[0])
        for index in range(1, len(dialogue) - 1):
            context += word_tokenize(dialogue[index])
        
        context_list.append(context)
        response_list.append(response)
        
    return context_list, response_list


# In[ ]:


context_list, response_list = generate_pairs(conversation)


# In[ ]:


def train_test_split(X,Y):
    
    # Population indices to sample from.
    pop_indices = [i for i in range(len(X))]
    
    # Randomly split the dataset into test and train with a 80%-20% split
    #test_indices = random.sample(pop_indices, int(0.2 * len(X)))
    test_indices = random.sample(pop_indices, 1000)
    train_indices = list(set(pop_indices) - set(test_indices))

    X_test = [X[i] for i in test_indices]
    Y_test = [Y[i] for i in test_indices]
    
    X_train = [X[i] for i in train_indices]
    Y_train = [Y[i] for i in train_indices]
    
    #Add negative samples to the test list
    X_test += X_test
    Y_test += Y_test[::-1]
    
    return X_train, Y_train, X_test, Y_test


# In[ ]:


X_train, Y_train, X_test, Y_test = train_test_split(context_list, response_list)


# In[ ]:


with open("X_train.pkl", "wb") as handle:
    pkl.dump(X_train, handle)
with open("Y_train.pkl", "wb") as handle:
    pkl.dump(Y_train, handle)
with open("X_test.pkl", "wb") as handle:
    pkl.dump(X_test, handle)
with open("Y_test.pkl", "wb") as handle:
    pkl.dump(Y_test, handle)


# ## Generate corpus using the conversation list

# In[ ]:


corpus = []
for c in conversation:
    context = []
    
    for s in c:
        context += word_tokenize(s)
    
    corpus.append(context)


# In[ ]:


with open("corpus.pkl", "wb") as handle:
    pkl.dump(corpus, handle)


# 
# ## Create word embeddings using Gensim

# In[ ]:


# Read the corpus text file
with open("corpus.pkl", "rb") as handle:
    corpus = pkl.load(handle)


# In[ ]:


# min_count = 1, says not to ignore any word occurence
# size = 50, is the size of word embedding
model = Word2Vec(corpus, min_count = 1, size = 50, sg = 1)


# In[ ]:


with open("embeddings.kv", "wb") as handle:
    model.wv.save(handle)


# In[ ]:


embeddings = KeyedVectors.load("embeddings.kv")


# In[ ]:


embeddings['Can']

