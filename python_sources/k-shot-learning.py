#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 5GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session


# In[ ]:


import re
import string


# In[ ]:


temp_df=pd.read_csv('/kaggle/input/indonesiandata1/data-indonesian-tweets.csv')


# In[ ]:


temp_df


# In[ ]:


temp_df.emotion.value_counts()


# In[ ]:


temp_df.drop(list(temp_df.loc[temp_df['emotion']=='no_emotion'].index),inplace=True)
print(temp_df.emotion.value_counts())


# In[ ]:


from nltk.corpus import stopwords
import nltk
stopwords.fileids()


# In[ ]:


def clean_text(text):
    '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
    and remove words containing numbers.'''
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

def text_preprocessing(text):
    """
    Cleaning and parsing the text.

    """
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    nopunc = clean_text(text)
    tokenized_text = tokenizer.tokenize(nopunc)
    remove_stopwords = [w for w in tokenized_text if w not in stopwords.words('indonesian')]
    combined_text = ' '.join(tokenized_text)
    return combined_text


# In[ ]:


temp_df['content']=temp_df['content'].apply(str).apply(lambda x: text_preprocessing(x))


# # Remove repititive characters

# In[ ]:


def rep(text):
    grp = text.group(0)
    if len(grp) > 1:
        return grp[0:1] # can change the value here on repetition
    return grp
   
def unique_char(rep,sentence):
    convert = re.sub(r'(\w)\1+', rep, sentence) 
    return convert

temp_df['content']=temp_df['content'].apply(lambda x : unique_char(rep,x))


# In[ ]:


temp_df.drop(['Unnamed: 0'],axis=1,inplace=True)
temp_df.head()


# # Selecting 90 rows from each emotion
# ## i.e k=90
# 

# In[ ]:


df=pd.DataFrame(columns=['content','emotion'])
for i in  temp_df.emotion.unique():
    emotion_c=temp_df.loc[temp_df['emotion']==str(i)][:90]
    df=df.append(emotion_c)
df=df.sample(frac=1)
df


# In[ ]:


temp_df=pd.DataFrame()
ls=[]
def token_after_clean(text):
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    tokenized_text = tokenizer.tokenize(text)
    ls.append(tokenized_text)
    return tokenized_text


df['content']=df['content'].apply(str).apply(lambda x: token_after_clean(x))


df


# In[ ]:


from gensim.models import FastText
model = FastText(size=150, window=3, min_count=1)
model.build_vocab(sentences=df.content)
model.train(sentences=df.content, total_examples=len(df.content), epochs=50)  # train


# Example of word vector developed after training

# In[ ]:


model.wv['ketua'] #ketua in english is chairman


# ## fasttext way of building sentence vector
# 
# refered [here](https://stackoverflow.com/questions/54181163/fasttext-embeddings-sentence-vectors)

# In[ ]:


def l2_norm(x):
    return np.sqrt(np.sum(x**2))

def div_norm(x):
    norm_value = l2_norm(x)
    if norm_value > 0:
        return x * ( 1.0 / norm_value)
    else:
        return x
    
final_vector=[]
def sentence_builder(ls):
    for i in ls:

        fast_sentence=0
        for j in i:
            v1=model.wv[str(j)]
            fast_sentence+=div_norm(v1)
        sentence_vector=(fast_sentence)/len(i)
        final_vector.append(sentence_vector)
    return final_vector

k=sentence_builder(ls) # ls is the lsit we developed earlier        


# # clustering

# In[ ]:


from sklearn.cluster import KMeans
true_k = 8
k_model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
k_model.fit(k)


# ## to  get centroids of each cluster

# In[ ]:


order_centroids = k_model.cluster_centers_.argsort()[:, ::-1]
terms=list(model.wv.vocab.keys())


# In[ ]:


for i in range(true_k):
    print('\n')
    print("Cluster %d:" % i)
    for ind in order_centroids[i, :10]:
        print("%s"% terms[ind])


# ## Next Step :-
# 1. convert to english top n words of each cluster to understand what each cluster is pointing to for help we can compare our translations to visualisation of top n grams of each emotion
#     done in visualtion kernel.
# 2. Suppose Cluster 8 represents **Disgust** now after testing we can compare how many sentences are correctly classified.
# 
# 3. We can use **Accuracy**as metric because here we have balanced Dataset.

# In[ ]:




