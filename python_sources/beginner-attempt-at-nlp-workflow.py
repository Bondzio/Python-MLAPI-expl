#!/usr/bin/env python
# coding: utf-8

# **Introduction** 
# 
# The aim of this notebook is to leverage insights from several public kernels to eventually formalize a workflow for NLP beginners on kaggle, like me.  Any comments, recommendations and insights would thus be very appreciated!
# 
# **Credits**
# 
# EDA code was heavily sourced from: 
#  
# https://www.kaggle.com/arunsankar/key-insights-from-quora-insincere-questions
# 
# Data Pre-processing code adapted from:
# 
# https://www.kaggle.com/enerrio/scary-nlp-with-spacy-and-keras
# 
# Word Embedding model was heavily adapted from:
# 
# https://www.kaggle.com/theoviel/improve-your-score-with-some-text-preprocessing
# 
# LSTM architecture was adapted from:
# 
# https://www.kaggle.com/mihaskalic/lstm-is-all-you-need-well-maybe-embeddings-also
# 
# 
# **Analysis Sections**
# * Data Understanding
#     * EDA plot 1 - Word Cloud
#     * EDA plot 2 - side by side plot comparison using N-gram
#     * EDA Plot 3 - Word count distribution, Character Length Distribution, Stop words, Punctuation, Upper case
#     * Overview of EDA results
# * Data Preparation 
# * Modelling
# * Evaluation
# 
# **Other helpful kernels and links**
# 
# *Kernels* :
# 
# * https://www.kaggle.com/mjbahmani/a-data-science-framework-for-quora
# * https://www.kaggle.com/shujian/test-the-difficulty-of-this-classification-tasks
# * https://www.kaggle.com/enerrio/scary-nlp-with-spacy-and-keras
# * https://www.kaggle.com/wakamezake/visualizing-word-vectors
# 
# *Links*
# * https://www.kdnuggets.com/2017/02/natural-language-processing-key-terms-explained.html
# 
# **Next Steps**
# 
# * Investigate how dimensionality reduction techniques affect the model
# * Implement oversampling to cater for unbalanced positive classes
# 
# **Thanks for reading!**
# 

# # **Data Understanding**
#  
# In order to start the anlaysis, the nature of the datasets and the files provided will first need to be examined. This normally involves examining the shape of the datasets,  followed by an EDA, with the objective to understand what defines a question as insincere or sincere.
# 

# In[ ]:


# Input data files are available in the "../input/" directory.
# For example, running this will list the files in the input directory
import os
print(os.listdir("../input"))


# Word Embeddings allow words that are used in similar ways to result in having similar vector representations, naturally capturing their meaning.
# 
# Further details at: https://machinelearningmastery.com/what-are-word-embeddings/

# In[ ]:


#Verify which embeddings are provided
get_ipython().system('ls ../input/embeddings')
#there are 4 embeddings provided with the dataset


# In[ ]:


#import packages
import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import random
import spacy
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import re
from bs4 import BeautifulSoup
import unicodedata
from collections import defaultdict
import string

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

from sklearn.model_selection import train_test_split

from nltk.corpus import stopwords
from sklearn.metrics import log_loss
from tqdm import tqdm
stopwords = stopwords.words('english')
sns.set_context('notebook')


# In[ ]:


#Code adapted from: https://www.kaggle.com/arunsankar/key-insights-from-quora-insincere-questions
#import the different datasets and print the characteristics of each
train = pd.read_csv('../input/train.csv')
test = pd.read_csv('../input/test.csv')
sub = pd.read_csv('../input/sample_submission.csv')

#Print the different statistics of the different files
print('Train data: \nRows: {}\nCols: {}'.format(train.shape[0],train.shape[1]))
print(train.columns)

print('\nTest data: \nRows: {}\nCols: {}'.format(test.shape[0],test.shape[1]))
print(test.columns)

print('\nSubmission data: \nRows: {}\nCols: {}'.format(sub.shape[0],sub.shape[1]))
print(sub.columns)


# In[ ]:


#View the first 5 entries of the training data
train.head()


# In[ ]:


#View information about the train dataset
train.info()
##1306122 observations and 3 columns


# In[ ]:


#check for the number of positive and negative classes
pd.crosstab(index = train.target, columns = "count" )
#There seems to be unbalanced classes in the dataset [first issue]


# **EDA plot 1 - Word Cloud**
# 
# Word clouds can identify trends and patterns that would otherwise be unclear or difficult to see in a tabular format. Frequently used keywords stand out better in a word cloud. Common words that might be overlooked in tabular form are highlighted in larger text making them pop out when displayed in a word cloud.

# In[ ]:


#Code sourced from : https://www.kaggle.com/sudalairajkumar/simple-exploration-notebook-qiqc

#import the wordcloud package
from wordcloud import WordCloud, STOPWORDS

#Define the word cloud function with a max of 200 words
def plot_wordcloud(text, mask=None, max_words=200, max_font_size=100, figure_size=(24.0,16.0), 
                   title = None, title_size=40, image_color=False):
    stopwords = set(STOPWORDS)
    #define additional stop words that are not contained in the dictionary
    more_stopwords = {'one', 'br', 'Po', 'th', 'sayi', 'fo', 'Unknown'}
    stopwords = stopwords.union(more_stopwords)
    #Generate the word cloud
    wordcloud = WordCloud(background_color='black',
                    stopwords = stopwords,
                    max_words = max_words,
                    max_font_size = max_font_size, 
                    random_state = 42,
                    width=800, 
                    height=400,
                    mask = mask)
    wordcloud.generate(str(text))
    #set the plot parameters
    plt.figure(figsize=figure_size)
    if image_color:
        image_colors = ImageColorGenerator(mask);
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear");
        plt.title(title, fontdict={'size': title_size,  
                                  'verticalalignment': 'bottom'})
    else:
        plt.imshow(wordcloud);
        plt.title(title, fontdict={'size': title_size, 'color': 'black', 
                                  'verticalalignment': 'bottom'})
    plt.axis('off');
    plt.tight_layout()  


# In[ ]:


#Select insincere questions from training dataset
insincere = train.loc[train['target'] == 1]
#run the function on the insincere questions
plot_wordcloud(insincere["question_text"], title="Word Cloud of Insincere Questions")


# In[ ]:


#Select sincere questions from training dataset
sincere = train.loc[train['target'] == 0]
#run the function on the insincere questions
plot_wordcloud(sincere["question_text"], title="Word Cloud of Sincere Questions")


# **EDA plot 2 - side by side plot comparison using N-gram**
# 
# An n-gram is a contiguous sequence of n items from a given sample of text or speech. Different definitions of n-grams will allow for the identification of the most prevalent words/sentences in the training data and thus help distinguish what comprises insincere and sincere questions.
# 
# It should be noted that prior to displaying individual words or sentences, the text will first be tokenized (based on a desired integer) and then put into a dataframe which will be used to construct side by side plots. 
# 
# Tokenization is, generally, an early step in the NLP process, a step which splits longer strings of text into smaller pieces, or tokens. Larger chunks of text can be tokenized into sentences, sentences can be tokenized into words, etc. 

# In[ ]:


def ngram_extractor(text, n_gram):
    token = [token for token in text.lower().split(" ") if token != "" if token not in STOPWORDS]
    ngrams = zip(*[token[i:] for i in range(n_gram)])
    return [" ".join(ngram) for ngram in ngrams]

# Function to generate a dataframe with n_gram and top max_row frequencies
def generate_ngrams(df, col, n_gram, max_row):
    temp_dict = defaultdict(int)
    for question in df[col]:
        for word in ngram_extractor(question, n_gram):
            temp_dict[word] += 1
    temp_df = pd.DataFrame(sorted(temp_dict.items(), key=lambda x: x[1])[::-1]).head(max_row)
    temp_df.columns = ["word", "wordcount"]
    return temp_df

#Function to construct side by side comparison plots
def comparison_plot(df_1,df_2,col_1,col_2, space):
    fig, ax = plt.subplots(1, 2, figsize=(20,10))
    
    sns.barplot(x=col_2, y=col_1, data=df_1, ax=ax[0], color="royalblue")
    sns.barplot(x=col_2, y=col_1, data=df_2, ax=ax[1], color="royalblue")

    ax[0].set_xlabel('Word count', size=14)
    ax[0].set_ylabel('Words', size=14)
    ax[0].set_title('Top words in sincere questions', size=18)

    ax[1].set_xlabel('Word count', size=14)
    ax[1].set_ylabel('Words', size=14)
    ax[1].set_title('Top words in insincere questions', size=18)

    fig.subplots_adjust(wspace=space)
    
    plt.show()


# In[ ]:


#Obtain sincere and insincere ngram based on 1 gram (top 20)
sincere_1gram = generate_ngrams(train[train["target"]==0], 'question_text', 1, 20)
insincere_1gram = generate_ngrams(train[train["target"]==1], 'question_text', 1, 20)
#compare the bar plots
comparison_plot(sincere_1gram,insincere_1gram,'word','wordcount', 0.25)


# In[ ]:


#Obtain sincere and insincere ngram based on 2 gram (top 20)
sincere_2gram = generate_ngrams(train[train["target"]==0], 'question_text', 2, 20)
insincere_2gram = generate_ngrams(train[train["target"]==1], 'question_text', 2, 20)
#compare the bar plots
comparison_plot(sincere_2gram,insincere_2gram,'word','wordcount', 0.25)


# In[ ]:


#Obtain sincere and insincere ngram based on 3 gram (top 20)
sincere_3gram = generate_ngrams(train[train["target"]==0], 'question_text', 3, 20)
insincere_3gram = generate_ngrams(train[train["target"]==1], 'question_text', 3, 20)
#compare the bar plots
comparison_plot(sincere_3gram,insincere_3gram,'word','wordcount', 0.25)


# **EDA Plot 3 - Word count distribution, Character Length Distribution, Stop words, Punctuation, Upper case **

# In[ ]:


# Number of words in the questions
train["word_count"] = train["question_text"].apply(lambda x: len(str(x).split()))
test["word_count"] = test["question_text"].apply(lambda x: len(str(x).split()))

fig, ax = plt.subplots(figsize=(15,2))
sns.boxplot(x="word_count", y="target", data=train, ax=ax, palette=sns.color_palette("RdYlGn_r", 10), orient='h')
ax.set_xlabel('Word Count', size=10, color="#0D47A1")
ax.set_ylabel('Target', size=10, color="#0D47A1")
ax.set_title('[Horizontal Box Plot] Word Count distribution', size=12, color="#0D47A1")
plt.gca().xaxis.grid(True)
plt.show()


# In[ ]:


# Number of characters in the questions
train["char_length"] = train["question_text"].apply(lambda x: len(str(x)))
test["char_length"] = test["question_text"].apply(lambda x: len(str(x)))

fig, ax = plt.subplots(figsize=(15,2))
sns.boxplot(x="char_length", y="target", data=train, ax=ax, palette=sns.color_palette("RdYlGn_r", 10), orient='h')
ax.set_xlabel('Character Length', size=10, color="#0D47A1")
ax.set_ylabel('Target', size=10, color="#0D47A1")
ax.set_title('[Horizontal Box Plot] Character Length distribution', size=12, color="#0D47A1")
plt.gca().xaxis.grid(True)
plt.show()


# In[ ]:


# Number of stop words in the questions
train["stop_words_count"] = train["question_text"].apply(lambda x: len([w for w in str(x).lower().split() if w in STOPWORDS]))
test["stop_words_count"] = test["question_text"].apply(lambda x: len([w for w in str(x).lower().split() if w in STOPWORDS]))

fig, ax = plt.subplots(figsize=(15,2))
sns.boxplot(x="stop_words_count", y="target", data=train, ax=ax, palette=sns.color_palette("RdYlGn_r", 10), orient='h')
ax.set_xlabel('Number of stop words', size=10, color="#0D47A1")
ax.set_ylabel('Target', size=10, color="#0D47A1")
ax.set_title('[Horizontal Box Plot] Number of Stop Words distribution', size=12, color="#0D47A1")
plt.gca().xaxis.grid(True)
plt.show()


# In[ ]:


# Number of punctuations in the questions
train["punc_count"] = train["question_text"].apply(lambda x: len([c for c in str(x) if c in string.punctuation]))
test["punc_count"] = test["question_text"].apply(lambda x: len([c for c in str(x) if c in string.punctuation]))

fig, ax = plt.subplots(figsize=(15,2))
sns.boxplot(x="punc_count", y="target", data=train[train['punc_count']<train['punc_count'].quantile(.99)], ax=ax, palette=sns.color_palette("RdYlGn_r", 10), orient='h')
ax.set_xlabel('Number of punctuations', size=10, color="#0D47A1")
ax.set_ylabel('Target', size=10, color="#0D47A1")
ax.set_title('[Horizontal Box Plot] Punctuation distribution', size=12, color="#0D47A1")
plt.gca().xaxis.grid(True)
plt.show()


# In[ ]:


# Number of upper case words in the questions
train["upper_words"] = train["question_text"].apply(lambda x: len([w for w in str(x).split() if w.isupper()]))
test["upper_words"] = test["question_text"].apply(lambda x: len([w for w in str(x).split() if w.isupper()]))

fig, ax = plt.subplots(figsize=(15,2))
sns.boxplot(x="upper_words", y="target", data=train[train['upper_words']<train['upper_words'].quantile(.99)], ax=ax, palette=sns.color_palette("RdYlGn_r", 10), orient='h')
ax.set_xlabel('Number of Upper case words', size=10, color="#0D47A1")
ax.set_ylabel('Target', size=10, color="#0D47A1")
ax.set_title('[Horizontal Box Plot] Upper case words distribution', size=12, color="#0D47A1")
plt.gca().xaxis.grid(True)
plt.show()


# In[ ]:


# Number of title words in the questions
train["title_words"] = train["question_text"].apply(lambda x: len([w for w in str(x).split() if w.istitle()]))
test["title_words"] = test["question_text"].apply(lambda x: len([w for w in str(x).split() if w.istitle()]))

fig, ax = plt.subplots(figsize=(15,2))
sns.boxplot(x="title_words", y="target", data=train[train['title_words']<train['title_words'].quantile(.99)], ax=ax, palette=sns.color_palette("RdYlGn_r", 10), orient='h')
ax.set_xlabel('Number of Title words', size=10, color="#0D47A1")
ax.set_ylabel('Target', size=10, color="#0D47A1")
ax.set_title('[Horizontal Box Plot] Title words distribution', size=12, color="#0D47A1")
plt.gca().xaxis.grid(True)
plt.show()


# In[ ]:


# Mean word length in the questions
train["word_length"] = train["question_text"].apply(lambda x: np.mean([len(w) for w in str(x).split()]))
test["word_length"] = test["question_text"].apply(lambda x: np.mean([len(w) for w in str(x).split()]))

fig, ax = plt.subplots(figsize=(15,2))
sns.boxplot(x="word_length", y="target", data=train[train['word_length']<train['word_length'].quantile(.99)], ax=ax, palette=sns.color_palette("RdYlGn_r", 10), orient='h')
ax.set_xlabel('Mean word length', size=10, color="#0D47A1")
ax.set_ylabel('Target', size=10, color="#0D47A1")
ax.set_title('[Horizontal Box Plot] Distribution of mean word length', size=12, color="#0D47A1")
plt.gca().xaxis.grid(True)
plt.show()


# *Overview of EDA results*
# 
# The EDA has helped outline a few characteristics which define insincere questions as such:
# 
# * Insincere questions are mostly focused at politics, religion and can contain profanity.
# * Insincere questions (Class 1) are generally more lengthy, with the exceptions of certain outliers for sincere questions. They thus have more stop words, punctions, characters, a higher average word count and title words.
# * Insincere questions are mostly lower case.
# * There are no missing cases.
# 
# The EDA has also revealed a few issues about the dataset which can be regrouped as:
# 
# * Unbalanced classes : a model trained on the current split of classes for the target variable will create a model more apt at predicting the '0' class rather than the '1' class, leading to false negatives in the predictions.
# * Uneven length of questions: the questions asked do not have a standard length and can thus lead to some questions being longer or shorter than others. 
# * Unstandardized letter cases
# * Punctuations
# * Stop Words
# * Outliers

# # Data Preparation 
# 
# 

# There are two ways of fitting an NLP model:
# 
# * Without the use of Word Embeddings (this will include steps such as lemmentization, removal of stopwords, punctuation and standardizing the characters)
# * With Word Embeddings (this should involve limited pre-processing steps as compared to the above)
# 
# This version of the kernel will focus on the use of Word Embeddings for sentiment analysis, with some sample code for text pre-processing should word embeddings not be present  (as shown below).
# 

# In[ ]:


# nlp = spacy.load('en_core_web_sm')
# # Clean text before feeding it to model
# punctuations = string.punctuation

# # Define function to cleanup text by removing personal pronouns, stopwords, puncuation and reducing all characters to lowercase 
# def cleanup_text(docs, logging=False):
#     texts = []
#     for doc in tqdm(docs):
#         doc = nlp(doc, disable=['parser', 'ner'])
#         tokens = [tok.lemma_.lower().strip() for tok in doc if tok.lemma_ != '-PRON-']
#         #remove stopwords and punctuations
#         tokens = [tok for tok in tokens if tok not in stopwords and tok not in punctuations]
#         tokens = ' '.join(tokens)
#         texts.append(tokens)
#     return pd.Series(texts)


# In[ ]:


# # Cleanup text and make sure it retains original shape
# print('Original training data shape: ', train['question_text'].shape)
# train_cleaned = cleanup_text(train['question_text'], logging=True)
# print('Cleaned up training data shape: ', train_cleaned.shape)


# In[ ]:


#use 90-10 split for validation dataset
train, val_df = train_test_split(train, test_size=0.1)


# In[ ]:


# embdedding setup
# Source https://blog.keras.io/using-pre-trained-word-embeddings-in-a-keras-model.html
#Based on https://www.kaggle.com/theoviel/improve-your-score-with-some-text-preprocessing
#GloVe is the most comprehensive word embedding

embeddings_index = {}
f = open('../input/embeddings/glove.840B.300d/glove.840B.300d.txt')
for line in tqdm(f):
    values = line.split(" ")
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()

print('Found %s word vectors.' % len(embeddings_index))


# In[ ]:


# Convert values to embeddings
def text_to_array(text):
    empyt_emb = np.zeros(300)
    text = text[:-1].split()[:30]
    embeds = [embeddings_index.get(x, empyt_emb) for x in text]
    embeds+= [empyt_emb] * (30 - len(embeds))
    return np.array(embeds)

# train_vects = [text_to_array(X_text) for X_text in tqdm(train["question_text"])]
val_vects = np.array([text_to_array(X_text) for X_text in tqdm(val_df["question_text"][:3000])])
val_y = np.array(val_df["target"][:3000])


# In[ ]:


# Data providers
batch_size = 128

def batch_gen(train):
    n_batches = math.ceil(len(train) / batch_size)
    while True: 
        train = train.sample(frac=1.)  # Shuffle the data.
        for i in range(n_batches):
            texts = train.iloc[i*batch_size:(i+1)*batch_size, 1]
            text_arr = np.array([text_to_array(text) for text in texts])
            yield text_arr, np.array(train["target"][i*batch_size:(i+1)*batch_size])


# # Modelling

# In[ ]:


#import Bi-Directional LSTM 
from keras.models import Sequential
from keras.layers import CuDNNLSTM, Dense, Bidirectional
import math


# In[ ]:


#Define the model architecture
model = Sequential()
model.add(Bidirectional(CuDNNLSTM(64, return_sequences=True),
                        input_shape=(30, 300)))
model.add(Bidirectional(CuDNNLSTM(64)))
model.add(Dense(1, activation="sigmoid"))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


# In[ ]:


mg = batch_gen(train)
#remember to change the number of epochs
model.fit_generator(mg, epochs=10,
                    steps_per_epoch=1000,
                    validation_data=(val_vects, val_y),
                    verbose= True)


# In[ ]:


# prediction part
batch_size = 256
def batch_gen(test):
    n_batches = math.ceil(len(test) / batch_size)
    for i in range(n_batches):
        texts = test.iloc[i*batch_size:(i+1)*batch_size, 1]
        text_arr = np.array([text_to_array(text) for text in texts])
        yield text_arr

test = pd.read_csv("../input/test.csv")

all_preds = []
for x in tqdm(batch_gen(test)):
    all_preds.extend(model.predict(x).flatten())


# In[ ]:


#Submit predictions
y_te = (np.array(all_preds) > 0.5).astype(np.int)

submit_df = pd.DataFrame({"qid": test["qid"], "prediction": y_te})
submit_df.to_csv("submission.csv", index=False)


# # Evaluation
# 
# The current model configuration leads to a score of around 0.547 
# 
# The next steps for this kernel will be:
# 
# * Investigate how dimensionality reduction techniques affect the model
# * Implement oversampling to cater for unbalanced positive classes
# * Implement the callback history in the model defintion to allow for the mapping of training and testing error (overfitting detection)
# * Apply rules of thumb for LSTM architecture defintion (sourced from journals)
# * Implement text treatment as per: https://www.kaggle.com/theoviel/improve-your-score-with-text-preprocessing-v2
# 
# **Thanks for reading so far!**
# 
# **Any comments, advice, recommendations and upvotes would be much appreciated!**

# 
