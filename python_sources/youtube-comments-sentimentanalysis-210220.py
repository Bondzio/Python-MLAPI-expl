#!/usr/bin/env python
# coding: utf-8

# **Youtube Comments Sentiment Analysis**
# 
# First of all thank you @gsc ankith for upload this dataset. Here I have tried to perform a very simple sentiment analysis using AFINN library

# In[ ]:


#installing contractions library
get_ipython().system('pip install contractions')


# In[ ]:


#Generic Data Processing & Visualization Libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re,string,unicodedata
import contractions #import contractions_dict
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


#Importing text processing libraries
import spacy
import spacy.cli
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.tokenize import word_tokenize
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

#downloading wordnet/punkt dictionary
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')


# In[ ]:


#Installing & Importing Sentiment Analysis Library  - AFINN
get_ipython().system('pip install afinn')
from afinn import Afinn


# In[ ]:


data = pd.read_csv("../input/nlp-dataset-collected-from-youtube-comments/iran.csv")


# **Data Exploration**

# In[ ]:


data.shape


# In[ ]:


#checking for null/missing values
data.isna().sum()


# In[ ]:


#dropping the index with missing comments
data = data.dropna()
data.shape


# In[ ]:


#creating a new column in the dataset for word count
data ['word_count'] = data['Comments'].apply(lambda x:len(str(x).split(" ")))


# In[ ]:


data.head()


# In[ ]:


#taking a copy of the clean dataset
data_clean = data.copy()


# **Data Preperation**

# In[ ]:


#lowering cases
data_clean['Comments'] = data_clean['Comments'].str.lower()


# In[ ]:


#stripping leading spaces (if any)
data_clean['Comments'] = data_clean['Comments'].str.strip()


# In[ ]:


#removing punctuations
from string import punctuation

def remove_punct(text):
  for punctuations in punctuation:
    text = text.replace(punctuations, '')
  return text

#apply to the dataset
data_clean['Comments'] = data_clean['Comments'].apply(remove_punct)


# In[ ]:


#function to remove special characters
def remove_special_chars(text, remove_digits=True):
  pattern = r'[^a-zA-z0-9\s]'
  text = re.sub(pattern, '', text)
  return text

#applying the function on the clean dataset
data_clean['Comments'] = data_clean['Comments'].apply(remove_special_chars)


# In[ ]:


#function to remove macrons & accented characters
def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

#applying the function on the clean dataset
data_clean['Comments'] = data_clean['Comments'].apply(remove_accented_chars)  


# In[ ]:


#Function to expand contractions
def expand_contractions(con_text):
  con_text = contractions.fix(con_text)
  return con_text

#applying the function on the clean dataset
data_clean['Comments'] = data_clean['Comments'].apply(expand_contractions)  


# In[ ]:


data_clean.head()


# In[ ]:


#dropping 'label' column as it is does not serve any purpose
data_clean = data_clean.drop(columns='label',axis=1)


# In[ ]:


#back up of the prepared data
data_clean_bckup = data_clean.copy()


# **Text Processing/Normalization - Removing Stop Words**

# In[ ]:


stopword_list = set(stopwords.words('english'))


# In[ ]:


tokenizer = ToktokTokenizer()


# In[ ]:


#function to remove stopwords
def remove_stopwords(text, is_lower_case=False):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)    
    return filtered_text

#applying the function
data_clean['Comments_Clean'] = data_clean['Comments'].apply(remove_stopwords)      


# **Text Processing/Normalization - Stemming**
# 
# applying the most simplest stemmer i.e. PorterStemmer

# In[ ]:


#Function for stemming
def simple_stemmer(text):
  ps = nltk.porter.PorterStemmer()
  text = ' '.join([ps.stem(word) for word in text.split()])
  return text

#applying the function
data_clean['Normalized_Comments'] = data_clean['Comments_Clean'].apply(simple_stemmer)


# In[ ]:


#dropping unwanted columns
data_clean = data_clean.drop(columns=data_clean[['Comments_Clean']],axis=1)
data_clean.head()


# In[ ]:


#rearranging columns
data_clean = data_clean[['Comments','Normalized_Comments','word_count']]

#taking backup 
data_clean_bckup_norm = data_clean.copy()

data_clean.head()


# **Sentiment Analysis - Using Afinn Library**

# In[ ]:


#Instantiating Afinn Library
af = Afinn()


# In[ ]:


#function to perform Afinn Sentiment Analyis
def afinn_sent_analysis(text):
  score = af.score(text)
  return score

#applying the function to Normalized Comments
data_clean['afinn_score'] = [afinn_sent_analysis(comm) for comm in data_clean['Normalized_Comments']]


# In[ ]:


#function to categorize the afinn sentiment score
def afinn_sent_category(score):
  categories = ['positive','negative','neutral']
  if score > 0:
    return categories[0]
  elif score < 0:
    return categories[1]
  else:
    return categories[2]  

data_clean['afinn_sent_category'] = [afinn_sent_category(scr) for scr in data_clean['afinn_score']]


# In[ ]:


#taking backup 
data_clean_bckup_afinn = data_clean.copy()


# **Visualisation**

# In[ ]:


data_clean.head()


# In[ ]:


sns.set(style="darkgrid")
fig, ax = plt.subplots(figsize=(8,8))
ax = sns.countplot(x="afinn_sent_category", data=data_clean)
plt.title('Sentiment Category Count Plot')
plt.ylabel('Count')
plt.xlabel('Sentiment Category')

#ax.set_xticklabels(ax.get_xticklabels(),rotation=0)
#i=0
#for p in ax.patches:
#    height = p.get_height()
#    ax.text(p.get_x()+p.get_width()/2., height + 1,
#        data_clean['afinn_sent_category'].value_counts()[i],ha="center")
#    i += 1


# In[ ]:


sns.set(style="whitegrid")
f, ax = plt.subplots(figsize=(15, 10))
sns.despine(f, left=True, bottom=True)
sns.scatterplot(x="afinn_score", y="word_count", 
                hue="afinn_sent_category", 
                palette="ch:r=-.2,d=.3_r", 
                sizes=(1,8), 
                data=data_clean, ax=ax)

