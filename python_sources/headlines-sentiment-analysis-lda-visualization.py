#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


# In[3]:


df = pd.read_csv("../input/abcnews-date-text.csv",error_bad_lines=False,warn_bad_lines=False)
df.head()


# In[ ]:


df.shape


# In[ ]:


df.publish_date = pd.to_datetime(df.publish_date,format="%Y%m%d")


# In[ ]:


df.publish_date.min(),df.publish_date.max()


# In[ ]:


df.publish_date.max() - df.publish_date.min()


# In[ ]:


len(df.publish_date.unique())


# In[ ]:


s = df.groupby('publish_date').tail(2)


# In[ ]:


s.head()


# In[ ]:


all_headlines = s.headline_text.values


# ## Get the sentiment for each headline and list positive , negative and neutral headlines separately

# In[ ]:


from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.corpus import stopwords
StopWords = stopwords.words("english")
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()


# In[ ]:


get_ipython().run_cell_magic('time', '', 'sia = SIA()\npos_list = []\nneg_list = []\nneu_list = []\nfor post in all_headlines:\n    post = " ".join([stemmer.stem(word) for word in str(post).lower().split() if word not in set(StopWords)])\n    res = sia.polarity_scores(post)\n    if res[\'compound\'] > 0.0:\n        pos_list.append(post)\n    elif res[\'compound\'] < 0.0:\n        neg_list.append(post)\n    else:\n        neu_list.append(post)')


# In[ ]:


print("Number of Positive Headlines : {}\nNumber of Negative Headlines : {}\nNumber of Neutral Headlines : {}".format(len(pos_list),len(neg_list),len(neu_list)))


# In[ ]:


from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')


# In[ ]:


pos_words = []
for line in pos_list:
    words = tokenizer.tokenize(line)
    for w in words:
        pos_words.append(w.lower())
    
    


# In[ ]:


neg_words = []
for line in neg_list:
    words = tokenizer.tokenize(line)
    for w in words:
        neg_words.append(w.lower())


# ## Most common positive words in the headlines

# In[ ]:


from nltk import FreqDist
pos_words = FreqDist(pos_words)
for x in pos_words.most_common(10):
    print(x[0],":",x[1])


# ## Most common negative words in the headlines

# In[ ]:


neg_words = FreqDist(neg_words)
for x in neg_words.most_common(10):
    print(x[0],":",x[1])


# ## Distribution of words in Positive Headlines

# In[ ]:


import matplotlib
import matplotlib.pylab as plt
get_ipython().run_line_magic('matplotlib', 'inline')
matplotlib.rcParams['xtick.labelsize'] = 14
plt.figure(figsize=(20,10))
pos_words.plot(50,cumulative=False)


# ## Distribution of words in Negative Headlines

# In[ ]:


plt.figure(figsize=(20,10))
neg_words.plot(50,cumulative=False)


# ####  The distribution is as expected, few words repeated most of the times in both positive and negative headlines. The frequency in case of Positive words dips quickly than Negative words

# ## NEXT UP : CLUSTERING INTO TOPICS

# In[ ]:


sample = pos_list+neg_list+neu_list


# ### Load gensim package for LDA and create a document-term matrix out of the headlines

# In[ ]:


import gensim
from gensim import corpora

sample_clean = [text.split() for text in sample] 


# In[ ]:


# Creating the term dictionary of our courpus, where every unique term is assigned an index. 
dictionary = corpora.Dictionary(sample_clean)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in sample_clean]


# ### Fit a LDA model for the document-term matrix, number of topics is set to be 10. 
# ### If you have only few documents increasing passes might help and if the documents are small (sparse) increasing iterations should help

# In[ ]:


get_ipython().run_cell_magic('time', '', '# Creating the object for LDA model using gensim library\nLda = gensim.models.ldamodel.LdaModel\nnum_topics = 10\n# Running and Trainign LDA model on the document term matrix.\nldamodel = Lda(doc_term_matrix, num_topics=num_topics, id2word = dictionary, passes=50,iterations=100)')


# ### Get the Document-Topic distribution and Topic-Word distributions

# In[ ]:


dtm = ldamodel.get_document_topics(doc_term_matrix)
K = ldamodel.num_topics
topic_word_matrix = ldamodel.print_topics(K)


# In[ ]:


print("The topics are: \n")
for x in topic_word_matrix:
    print(x[0],":",x[1],"\n")


# ### Preparing the document-topic matrix for t-SNE visualization

# In[ ]:


from gensim import matutils


# In[ ]:


document_topic_matrix = matutils.corpus2dense(corpus=dtm,num_docs=len(all_headlines),num_terms=K)


# In[ ]:


a = document_topic_matrix.transpose()


# In[ ]:


get_ipython().run_cell_magic('time', '', "from sklearn.manifold import TSNE\n\n# a t-SNE model\n# angle value close to 1 means sacrificing accuracy for speed\n# pca initializtion usually leads to better results \ntsne_model = TSNE(n_components=2, verbose=1, random_state=0,init='pca',)\n\n# 8-D -> 2-D\ntsne_lda = tsne_model.fit_transform(a)")


# In[ ]:


_lda_keys = []
for i in range(a.shape[0]):
    _lda_keys.append(a[i].argmax())
len(_lda_keys)


# ### Using Bokeh to plot a interactive-visualization

# In[ ]:


import bokeh.plotting as bp
from bokeh.io import output_notebook
from bokeh.plotting import show

# 10 colors
colormap = np.array(["#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c","#98df8a", "#d62728", "#ff9896","#bcbd22", "#dbdb8d"])
output_notebook()


# In[ ]:


plot_lda = bp.figure(plot_width=1000, plot_height=1000,
                     title="LDA t-SNE Viz",
                     tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
                     x_axis_type=None, y_axis_type=None, min_border=1)


# In[ ]:


n = len(a)
plot_lda.scatter(x=tsne_lda[:, 0], y=tsne_lda[:, 1],
                 color=colormap[_lda_keys][:n],
                 source=bp.ColumnDataSource({
                   "content": sample_clean[:n],
                   "topic_key": _lda_keys[:n]
                   }))


# ### Annotate the graph with words from each topic. Below we are just setting the coordinats for the text and get the word distribution form topic-word matrix

# In[ ]:


topic_summaries = [x[1] for x in topic_word_matrix]
topic_coord = np.empty((a.shape[1], 2)) * np.nan
for topic_num in _lda_keys:
    topic_coord[topic_num] = tsne_lda[_lda_keys.index(topic_num)]


# In[ ]:


# add topic words to graph
for i in range(a.shape[1]):
    plot_lda.text(topic_coord[i, 0], topic_coord[i, 1], [topic_summaries[i]])


# In[ ]:


show(plot_lda)


# ### The plot is really messy, reason should definitely be LDA model.. Each topic consist of similar words like "world","women","australia"..  For documents, the probablity of even most probable topic is also really low. Model can't distinguish documents into topics. Using more documents and tuning parameters should help.
