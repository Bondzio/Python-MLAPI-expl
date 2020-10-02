#!/usr/bin/env python
# coding: utf-8

# **Thanks for viewing my Kernel! If you like my work and find it useful, please leave an upvote! :)**
# 
# **Key Insights:** 
# 
# * 6.2% of the questions in training data are insincere
# * Insincere questions are dominated by words like trump, women, white, men, indian, muslims, black, americans, girls, indians, sex and india. More reference to specific groups of people of directly a person i.e. Donald Trump. 
# * Top 3 bigrams in the insincere questions are 'Donald Trump', 'White People' and 'Black People'. Questions related to race are highly insincere. Presence of Chinese people, Indian muslims, Indian girls, North Indians, Indian women and White Women confirm the same.
# * Insincere questions are related to hypothetical scenarios, age, race, etc
# * Sincere questions are related to tips, advices, suggestions, facts, etc. 
# * Insincere questions have more words, characters, stop words and punctuations

# In[ ]:


from IPython.display import Image
Image(filename="../input/quora-image/quora.jpg")


# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import random

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns

from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from collections import defaultdict
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model
import eli5

import os
print(os.listdir("../input/quora-insincere-questions-classification"))


# In[ ]:


train = pd.read_csv('../input/quora-insincere-questions-classification/train.csv')
test = pd.read_csv('../input/quora-insincere-questions-classification/test.csv')
sub = pd.read_csv('../input/quora-insincere-questions-classification/sample_submission.csv')

print('Train data: \nRows: {}\nCols: {}'.format(train.shape[0],train.shape[1]))
print(train.columns)

print('\nTest data: \nRows: {}\nCols: {}'.format(test.shape[0],test.shape[1]))
print(test.columns)

print('\nSubmission data: \nRows: {}\nCols: {}'.format(sub.shape[0],sub.shape[1]))
print(sub.columns)


# **6.2 % of train questions are insincere**

# In[ ]:


temp = train['target'].value_counts(normalize=True).reset_index()

colors = ['#4f92ff', '#4ffff0']
explode = (0.05, 0.05)
 
plt.pie(temp['target'], explode=explode, labels=temp['index'], colors=colors,
         autopct='%1.1f%%', shadow=True, startangle=0)
 
fig = plt.gcf()
fig.set_size_inches(12, 6)
fig.suptitle('% Target Distribution', fontsize=16)
plt.rcParams['font.size'] = 14
plt.axis('equal')
plt.show()


# Thanks to [SRK's](https://www.kaggle.com/sudalairajkumar) exploratory [kernel](https://www.kaggle.com/sudalairajkumar/simple-exploration-notebook-qiqc) for the custom functions. I modified them a bit so that I can reuse for any dataframe and n-gram combination. 

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

def comparison_plot(df_1,df_2,col_1,col_2, space):
    fig, ax = plt.subplots(1, 2, figsize=(20,10))
    
    sns.barplot(x=col_2, y=col_1, data=df_1, ax=ax[0], color="palegreen")
    sns.barplot(x=col_2, y=col_1, data=df_2, ax=ax[1], color="palegreen")

    ax[0].set_xlabel('Word count', size=14, color="green")
    ax[0].set_ylabel('Words', size=14, color="green")
    ax[0].set_title('Top words in sincere questions', size=18, color="green")

    ax[1].set_xlabel('Word count', size=14, color="green")
    ax[1].set_ylabel('Words', size=14, color="green")
    ax[1].set_title('Top words in insincere questions', size=18, color="green")

    fig.subplots_adjust(wspace=space)
    
    plt.show()


# **Top 20 1-gram words in sincere and insincere questions**
# * Sincere questions are dominated by words like best, will, people, good, one, etc. with no reference to any specific nouns.  Some of these words are high even in insincere words - meaning they are not significant to the classification. 
# * Insincere questions are dominated by words like trump, women, white, men, indian, muslims, black, americans, girls, indians, sex and india. More reference to specific groups of people of directly a person i.e. Donald Trump. 

# In[ ]:


sincere_1gram = generate_ngrams(train[train["target"]==0], 'question_text', 1, 20)
insincere_1gram = generate_ngrams(train[train["target"]==1], 'question_text', 1, 20)

comparison_plot(sincere_1gram,insincere_1gram,'word','wordcount', 0.25)


# **Top 20 2-gram words in sincere and insincere questions**
# * Top 3 bigrams in the insincere questions are 'Donald Trump', 'White People' and 'Black People'. Questions related to race are highly insincere. 
# * Presence of Chinese people, Indian muslims, Indian girls, North Indians, Indian women and White Women confirm the same.
# * Sincere questions have best way, year old, will happen, etc. as the top ones. No clear trend there but 'best' is the key word to look for. 

# In[ ]:


sincere_2gram = generate_ngrams(train[train["target"]==0], 'question_text', 2, 20)
insincere_2gram = generate_ngrams(train[train["target"]==1], 'question_text', 2, 20)

comparison_plot(sincere_2gram,insincere_2gram,'word','wordcount', .35)


# **Top 20 3-gram words in sincere and insincere questions**
# * Insincere questions are related to hypothetical scenarios, age, race, etc
# * Sincere questions are related to tips, advices, suggestions, facts, etc. 

# In[ ]:


sincere_3gram = generate_ngrams(train[train["target"]==0], 'question_text', 3, 20)
insincere_3gram = generate_ngrams(train[train["target"]==1], 'question_text', 3, 20)

comparison_plot(sincere_3gram,insincere_3gram,'word','wordcount', .45)


# **Insincere questions have more words per question**

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


# Number of unique words in the questions
train["unique_word_count"] = train["question_text"].apply(lambda x: len(set(str(x).split())))
test["unique_word_count"] = test["question_text"].apply(lambda x: len(set(str(x).split())))

fig, ax = plt.subplots(figsize=(15,2))
sns.boxplot(x="unique_word_count", y="target", data=train, ax=ax, palette=sns.color_palette("RdYlGn_r", 10), orient='h')
ax.set_xlabel('Unique Word Count', size=10, color="#0D47A1")
ax.set_ylabel('Target', size=10, color="#0D47A1")
ax.set_title('[Horizontal Box Plot] Unique Word Count distribution', size=12, color="#0D47A1")
plt.gca().xaxis.grid(True)
plt.show()


# **Insincere questions have more characters than sincere questions**

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


# **Insincere questions have more stop words than sincere questions**

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


# **Insincere questions have more punctuations**

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


# **More upper case words in Sincere questions**

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


# **A base model with vectorized matrix shows that insincere words are predominantly due to identification of religion, nationality, race, caste, political affiliation, etc. **

# In[ ]:


# Get the tfidf vectors
tfidf_vec = TfidfVectorizer(stop_words='english', ngram_range=(1,3))
tfidf_vec.fit_transform(train['question_text'].values.tolist() + test['question_text'].values.tolist())
train_tfidf = tfidf_vec.transform(train['question_text'].values.tolist())
test_tfidf = tfidf_vec.transform(test['question_text'].values.tolist())


# In[ ]:


y_train = train["target"].values

x_train = train_tfidf
x_test = test_tfidf

model = linear_model.LogisticRegression(C=5., solver='sag')
model.fit(x_train, y_train)
y_test = model.predict_proba(x_test)[:,1]


# In[ ]:


eli5.show_weights(model, vec=tfidf_vec, top=100, feature_filter=lambda x: x != '<BIAS>')


# In[ ]:


sub['prediction'] = y_test
sub.to_csv('baseline_submission.csv',index=False)


# **More to come!!!**
# * Note to self: Questions marks are present in the words. Should remove them while processing.
