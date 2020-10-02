#!/usr/bin/env python
# coding: utf-8

# **In this year's Halloween playground competition, you're challenged to predict the author of excerpts from horror stories by Edgar Allan Poe, Mary Shelley, and HP Lovecraft**

# In[ ]:


import numpy as np
import pandas as pd
from collections import defaultdict
import keras
import keras.backend as K
from keras.layers import Dense, GlobalAveragePooling1D, Embedding
from keras.callbacks import EarlyStopping
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split


# In[ ]:


df = pd.read_csv('./../input/train.csv')


# **This is what the data looks like. It is a CSV file. 
# 
# **We have a column titled "text" containing sentences and a column titled "author" containing author initials.****

# In[ ]:


sample = df.values[0:3]
print(sample)
df.head(20)


# **Preprocess Text:**    
#     1) Add a space on both sides of punctuation to avoid forming new words based off of punctuation.
#     2) Convert author label to categorical label for better compatability with classification algorithms.

# In[ ]:


def preprocess(text):
    text = text.strip()
    text = text.replace("' ", " ' ")
    signs = set(',.:;"?!')
    prods = set(text) & signs
    if not prods:
        return text

    for sign in prods:
        text = text.replace(sign, ' {} '.format(sign) )
    return text


# In[ ]:


a2c = {'EAP': 0, 'HPL' : 1, 'MWS' : 2}
y = np.array([a2c[a] for a in df.author])
y = to_categorical(y)


# **An N-gram is a contiguous sequence of n items from a given sequence of text or speech. The items can be phonemes, syllables, letters, words or base pairs according to the application (e.g. 2-gram sequence: "to be, be or, or not, not to, to be"; 3-gram sequence: "to be or, be or not, or not to, not to be".
# 
# **Next I visualize some N-grams for Edgar Allan Poe.****

# In[ ]:


from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
from plotly import tools
import plotly.plotly as py
from collections import Counter
from nltk.util import ngrams
from nltk.corpus import stopwords
import re


tokenize_regex = re.compile("[\w]+")
sw = set(stopwords.words("english"))

def preprocessText(text, ngram_order):
    """
    Transform text into a list of ngrams. Feel free to play with the order parameter
    """
    text = text.lower()
    
    text = [" ".join(ngram) for ngram in ngrams((tokenize_regex.findall(text)), ngram_order)             if (set(ngram) - sw)] # instead of filtering stopwords, let's just filter out the ngrams
                                  # with nothing but stopwords
    return text

def draw_word_histogram(texts, title, bars=30):
    """
    Draw a barplot for word frequency distribution.
    """
    # first, do the counting
    ngram_counter = Counter()
    for text in texts:
        ngram_counter.update(text)
    # for plotly, we need two lists: xaxis values and the corresponding yaxis values
    # this is how we split a list of two-element tuples into two lists
    features, counts = zip(*ngram_counter.most_common(bars))
    # now let's define the barplot
    bars = go.Bar(
        x=counts[::-1],  # inverse the values to have the largest on the top
        y=features[::-1],
        orientation="h",  # this makes it a horizontal barplot 
        marker=dict(
            color='rgb(128, 0, 32)'  # this color is called oxblood... spooky, isn't it?
        )
    )
    # this is how we customize the looks of our barplot
    layout = go.Layout(
        paper_bgcolor='rgb(0, 0, 0)',  # color of the background under the title and in the margins
        plot_bgcolor='rgb(0, 0, 0)',  # color of the plot background
        title=title,
        autosize=False,  # otherwise the plot would be too small to contain axis labels
        width=600,
        height=800,
        margin=go.Margin(
            l=120, # to make space for y-axis labels
        ),
        font=dict(
            family='Serif',
            size=13, # a lucky number
            color='rgb(200, 200, 200)'
        ),
        xaxis=dict(
            showgrid=True,  # all the possible lines - try switching them off
            zeroline=True,
            showline=True,
            zerolinecolor='rgb(200, 200, 200)',
            linecolor='rgb(200, 200, 200)',
            gridcolor='rgb(200, 200, 200)',
        ),
        yaxis=dict(
            ticklen=8  # to add some space between yaxis labels and the plot
        )
        
    )
    fig = go.Figure(data=[bars], layout=layout)
    iplot(fig, filename='h-bar')
    return


# In[ ]:


init_notebook_mode(connected=True)


poe = df[df.author=="EAP"].text.apply(preprocessText, ngram_order=1)
draw_word_histogram(poe, "Edgar Allan Poe Most Common Mono-grams")


# In[ ]:


poe = df[df.author=="EAP"].text.apply(preprocessText, ngram_order=2)
draw_word_histogram(poe, "Edgar Allan Poe Most Common Bi-grams")


# In[ ]:


poe = df[df.author=="EAP"].text.apply(preprocessText, ngram_order=3)
draw_word_histogram(poe, "Edgar Allan Poe Most Common Tri-grams")


# In[ ]:


poe = df[df.author=="EAP"].text.apply(preprocessText, ngram_order=4)
draw_word_histogram(poe, "Edgar Allan Poe Most Common Quad-grams")


# Here we create N-grams for N = (1 to 4) for each author.  These N-grams will be our features for classification.

# In[ ]:


def create_docs(df, n_gram_max=4):
    def add_ngram(q, n_gram_max):
            ngrams = []
            for n in range(1, n_gram_max+1):
                for w_index in range(len(q)-n+1):
                    ngrams.append('--'.join(q[w_index:w_index+n]))
            return q + ngrams
        
    docs = []
    for doc in df.text:
        doc = preprocess(doc).split()
        docs.append(' '.join(add_ngram(doc, n_gram_max)))
    
    return docs


# In[ ]:


min_count = 15

docs = create_docs(df)
tokenizer = Tokenizer(lower=True, filters='')
tokenizer.fit_on_texts(docs)
num_words = sum([1 for _, v in tokenizer.word_counts.items() if v >= min_count])

tokenizer = Tokenizer(num_words=num_words, lower=True, filters='')
tokenizer.fit_on_texts(docs)
docs = tokenizer.texts_to_sequences(docs)

maxlen = None

docs = pad_sequences(sequences=docs, maxlen=maxlen)


# **Here I use Keras to build a custom neural network for this natural language processing problem.  
# 
# **Note that accuracy can be improved by increasing the number of epochs while speed can be improved by decreasing the number of epochs.****

# In[ ]:


input_dim = np.max(docs) + 1
embedding_dims = 20


# In[ ]:


def create_model(embedding_dims=20, optimizer='adam'):
    model = Sequential()
    model.add(Embedding(input_dim=input_dim, output_dim=embedding_dims))
    model.add(GlobalAveragePooling1D())
    model.add(Dense(3, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizer,
                  metrics=['accuracy'])
    return model


# In[ ]:


epochs = 20
x_train, x_test, y_train, y_test = train_test_split(docs, y, test_size=0.2)

model = create_model()
hist = model.fit(x_train, y_train,
                 batch_size=16,
                 validation_data=(x_test, y_test),
                 epochs=epochs,
                 callbacks=[EarlyStopping(patience=2, monitor='val_loss')])


# **>80% Accuracy!  Great!  Next, we can improve the accuracy by increasing the number of epochs.**

# In[ ]:


# test_df = pd.read_csv('../input/test.csv')
# docs = create_docs(test_df)
# docs = tokenizer.texts_to_sequences(docs)
# docs = pad_sequences(sequences=docs, maxlen=maxlen)
# y = model.predict_proba(docs)

# result = pd.read_csv('../input/sample_submission.csv')
# for a, i in a2c.items():
#     result[a] = y[:, i]
# result.to_csv('_new_submission_1.csv', index=False)


# **Credit:** Note that many of the functions are adaptations from https://www.kaggle.com/nzw0301/simple-keras-fasttext-val-loss-0-31 and https://www.kaggle.com/mamamot/human-intelligible-machine-learning.
