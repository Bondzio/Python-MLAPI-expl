#!/usr/bin/env python
# coding: utf-8

# # Exploring music genre's using Doc2Vec
# 
# I explore different music genre's using doc2vec and try to explore relationships between words along different dimensions. In this notebook I take the case of *Jazz* music, but you can change it to other genre's by setting the genre variable in cell 14. Training the model for genre's with log of songs doesn't succeed on the Kaggle kernel. 
# 
# Some interesting patterns appear based on the word vectors, when explored in context of opposing words. E.g:
# 
# * *pleasure* v/s *pain*
# * *baby* v/s *father*

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

from subprocess import check_output
print(check_output(["ls", "../input"]).decode("utf8"))

# Any results you write to the current directory are saved as output.


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as plt
# gensim modules
from gensim import utils, matutils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec, Word2Vec
import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import seaborn as sns


# In[ ]:


get_ipython().system(' head ../input/lyrics.csv')


# In[ ]:


df = pd.read_csv("../input/lyrics.csv")
df.head()


# In[ ]:


r = df.iloc[0]
for t in set(r['lyrics'].split('\n')):
    print(list(utils.tokenize(t, lowercase=True)))
r[['artist', 'genre']].tolist()    


# In[ ]:


df.artist.value_counts().sort_values(ascending=False).head()


# In[ ]:


df.genre.value_counts().sort_values(ascending=False).tail()


# In[ ]:


class LabeledDocuments(object):
    def __init__(self, df, text_col='lyrics',
                 label_cols=('artist', 'year', 'genre')):
        if label_cols is None:
            label_cols = ['index']
        self.label_cols = list(label_cols)
        self.text_col = text_col
        self.df = df
        
    def __iter__(self):
        for i, r in self.df.iterrows():
            text = r[self.text_col]
            if pd.isnull(text):
                continue
            try:
                text = set(text.split('\n'))
            except AttributeError as e:
                print(r)
                raise
            ## Break each line of the song for context
            for t in text:
                yield LabeledSentence(list(utils.tokenize(t, lowercase=True)),
                                     r[self.label_cols].tolist())
                
                
def get_relatively_positive_words(model, pos_word, neg_word, topn=10):
    pos_vec = model.wv[pos_word]
    neg_vec = model.wv[neg_word]
    if isinstance(pos_word, list):
        pos_vec = pos_vec.mean(axis=0)
    if isinstance(neg_word, list):
        neg_vec = neg_vec.mean(axis=0)
    return model.similar_by_vector(
        (pos_vec-neg_vec),
        topn=topn)


def get_top_directed_words(model, pos_word, neg_word,
                           topn=10, combination=np.mean,
                           return_probs=False
                          ):
    pos_vec = model.wv[pos_word]
    neg_vec = model.wv[neg_word]
    n_pos_words = 1
    n_neg_words = 1
    set_all_words=set()
    if isinstance(pos_word, list):
        pos_vec = combination(pos_vec, axis=0)
        n_pos_words = len(pos_word)
        set_all_words.update(pos_word)
    else:
        set_all_words.add(pos_word)
    if isinstance(neg_word, list):
        neg_vec = combination(neg_vec, axis=0)
        n_neg_words = len(neg_word)
        set_all_words.update(neg_word)
    else:
        set_all_words.add(neg_word)
    
    all_similar_words = model.similar_by_vector(
        (pos_vec-neg_vec),
        topn=False)
    if return_probs:
        all_similar_words = np.exp(all_similar_words)
        all_similar_words = all_similar_words / all_similar_words.sum()
    all_similar_words_idx = np.argsort(all_similar_words)[::-1]
    return {
        "positive": [(model.wv.index2word[wi], all_similar_words[wi])
            for wi in all_similar_words_idx[:topn+(n_pos_words)]
            if model.wv.index2word[wi] not in set_all_words],
        "negative": [(model.wv.index2word[wi], all_similar_words[wi])
            for wi in all_similar_words_idx[:-(topn+1+(n_neg_words)):-1]
            if model.wv.index2word[wi] not in set_all_words]
    }
    
    
def plot_words(directed_words, pos_title='positive', neg_title='negative'):
    sns.set(style="whitegrid")

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(6, 10))
    
    ## Get data
    rows = ([
        (pos_title,) + w
        for w in directed_words['positive']
        ]+[
        (neg_title,) + w
        for w in directed_words['negative'][::-1]
    ])
    df_t = pd.DataFrame(rows,
                        columns=['class_label','word', 'sim'])
    # Plot the total crashes
    sns.set_color_codes("pastel")
    sns.barplot(x="sim", y="word", hue='class_label',
                data=df_t,
                )
    ax.set(ylabel="",
           xlabel="Similarity")
    sns.despine(left=True, bottom=True)


# In[ ]:


get_ipython().run_cell_magic('time', '', 'all_docs = list(LabeledDocuments(df.head()))\nprint("Total %s documents found." % len(all_docs))')


# In[ ]:


all_docs[:5]


# In[ ]:


get_ipython().run_cell_magic('time', '', 'genre=\'Country\'\nall_docs = list(LabeledDocuments(df[df[\'genre\'] == genre], label_cols=[\'artist\', \'year\']))\nprint("Total %s documents found." % len(all_docs))')


# In[ ]:


all_docs[:5]


# In[ ]:


get_ipython().run_cell_magic('time', '', 'model = Doc2Vec(min_count=5, window=10, size=100, sample=1e-4, negative=5)\nmodel.build_vocab(all_docs)')


# In[ ]:


get_ipython().run_cell_magic('time', '', 'for epoch in range(10):\n    print("Epoch %s" % epoch)\n    model.train(all_docs)')


# In[ ]:


model.most_similar('good')


# In[ ]:


df[df['genre'] == genre]['artist'].value_counts().head()


# In[ ]:


model.docvecs.most_similar(2016)


# In[ ]:


model.most_similar('girl')


# In[ ]:


model.most_similar('fire')


# In[ ]:


model.most_similar('love')


# In[ ]:


model.most_similar('song')


# In[ ]:


model.most_similar('god')


# In[ ]:


model.most_similar(positive=["girl", "god"], negative=["love"])


# In[ ]:


get_relatively_positive_words(model, 'good', 'bad')


# In[ ]:


get_relatively_positive_words(model, 'girl', 'boy')


# In[ ]:


get_relatively_positive_words(model, 'god', 'man')


# In[ ]:


get_relatively_positive_words(model,
                              ['girl', 'woman', 'lady'],
                              ['guy', 'man', 'son'])


# In[ ]:


get_top_directed_words(model,
                              ['girl', 'woman', 'lady'],
                              ['guy', 'man', 'son'])


# In[ ]:


get_top_directed_words(model,
                              ['girl'],
                              ['guy'])


# In[ ]:


get_top_directed_words(model,
                              ['lady'],
                              ['man'])


# In[ ]:


get_relatively_positive_words(model,
                              ['lady'],
                              ['man'])


# In[ ]:


pos_word, neg_word = 'girl', 'guy'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'man', 'car'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'love', 'hate'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'heart', 'mind'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'heart', 'soul'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'god', 'man'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


sorted(((w,v.count)
    for w,v in model.wv.vocab.items()),
       key=lambda x: x[1], reverse=True
)[100:110]


# In[ ]:


word_dist = get_top_directed_words(model,
                              ['girl', 'woman', 'lady'],
                              ['man', 'guy', 'son'])
plot_words(word_dist, "Female", "Male")


# In[ ]:


pos_word, neg_word = 'pleasure', 'pain'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'young', 'old'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'white', 'black'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'lady', 'hoe'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'life', 'death'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'music', 'silence'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'warm', 'cold'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'day', 'night'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'lost', 'found'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'marriage', 'affair'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'baby', 'father'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'bread', 'wine'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'yes', 'no'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:


pos_word, neg_word = 'pain', 'relief'
word_dist = get_top_directed_words(model,
                              [pos_word],
                              [neg_word])
plot_words(word_dist, pos_word, neg_word)


# In[ ]:




