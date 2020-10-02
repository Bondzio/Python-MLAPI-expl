#!/usr/bin/env python
# coding: utf-8

# # Classification of News Articles 
# 
# It is a notebook for multiclass classification of News articles which are having classes numbered 1 to 4, where 1 is "World News", 2 is "Sports News", 3 is "Business News" and 4 is "Science-Technology News".

# ### Importing libraries

# In[ ]:


import numpy as np 
import pandas as pd 
import nltk
import string as s
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
import re
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


train_data=pd.read_csv("/kaggle/input/ag-news-classification-dataset/train.csv",header=0,names=['classid','title','desc'])
test_data=pd.read_csv("/kaggle/input/ag-news-classification-dataset/test.csv",header=0,names=['classid','title','desc'])


# ## Analyzing Data

# In[ ]:


train_data.head()


# In[ ]:


test_data.head()


# In[ ]:


train_data.shape


# In[ ]:


test_data.shape


# **Countplot of Train data**

# In[ ]:


sns.countplot(train_data.classid);


# **Countplot of Testdata**

# In[ ]:


sns.countplot(test_data.classid);


# Seeing the countplot of the training data and testing data we can say that the datasets are balanced

# ## Splitting Data into Input and Label 

# In[ ]:


train_x=train_data.desc
test_x=test_data.desc
train_y=train_data.classid
test_y=test_data.classid


# # Preprocessing of Data
# 
# The data is preprocessed, in NLP it is also known as text normalization. Some of the most common methods of text normalization are 
# * Tokenization
# * Lemmatization
# * Stemming
# 

# ## Removal of HTML tags

# In[ ]:


def remove_html(text):
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', text)

train_x=train_x.apply(remove_html)
test_x=test_x.apply(remove_html)


# ## Removal of URLs

# In[ ]:


def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

train_x=train_x.apply(remove_urls)
test_x=test_x.apply(remove_urls)


# ## Tokenization of Data

# In[ ]:


def word_tokenize(txt):
    tokens = re.findall("[\w']+", txt)
    return tokens
train_x=train_x.apply(word_tokenize)
test_x=test_x.apply(word_tokenize)


# ## Removal of Stopwords

# In[ ]:


def remove_stopwords(lst):
    stop=stopwords.words('english')
    new_lst=[]
    for i in lst:
        if i.lower() not in stop:
            new_lst.append(i)
    return new_lst

train_x=train_x.apply(remove_stopwords)
test_x=test_x.apply(remove_stopwords) 


# ## Removal of Punctuation Symbols

# In[ ]:


def remove_punctuations(lst):
    new_lst=[]
    for i in lst:
        for  j in  s.punctuation:
            i=i.replace(j,'')
        new_lst.append(i)
    return new_lst
train_x=train_x.apply(remove_punctuations) 
test_x=test_x.apply(remove_punctuations)


# ## Removal of Numbers(digits)

# In[ ]:


def remove_numbers(lst):
    nodig_lst=[]
    new_lst=[]

    for i in  lst:
        for j in  s.digits:
            i=i.replace(j,'')
        nodig_lst.append(i)
    for i in  nodig_lst:
        if  i!='':
            new_lst.append(i)
    return new_lst
train_x=train_x.apply(remove_numbers)
test_x=test_x.apply(remove_numbers)


# ## Stemming of Dataset

# In[ ]:


import nltk

def stemming(text):
    porter_stemmer = nltk.PorterStemmer()
    roots = [porter_stemmer.stem(each) for each in text]
    return (roots)

train_x=train_x.apply(stemming)
test_x=test_x.apply(stemming)


# ## Lemmatization of Data

# In[ ]:


lemmatizer=nltk.stem.WordNetLemmatizer()
def lemmatzation(lst):
    new_lst=[]
    for i in lst:
        i=lemmatizer.lemmatize(i)
        new_lst.append(i)
    return new_lst
train_x=train_x.apply(lemmatzation)
test_x=test_x.apply(lemmatzation)


# In[ ]:


def remove_extrawords(lst):
    stop=['href','lt','gt','ii','iii','ie','quot','com']
    new_lst=[]
    for i in lst:
        if i not in stop:
            new_lst.append(i)
    return new_lst

train_x=train_x.apply(remove_extrawords)
test_x=test_x.apply(remove_extrawords) 


# In[ ]:


train_x=train_x.apply(lambda x: ''.join(i+' ' for i in x))
test_x=test_x.apply(lambda x: ''.join(i+' '  for i in x))


# ## Feature Extraction
#  
#  Features are extracted from the dataset and TF-IDF(Term Frequency - Inverse Document Frequency) is used for this purpose.

# In[ ]:


from sklearn.feature_extraction.text  import TfidfVectorizer
tfidf=TfidfVectorizer(min_df=8,ngram_range=(1,3))
train_1=tfidf.fit_transform(train_x)
test_1=tfidf.transform(test_x)
print("No. of features extracted")
print(len(tfidf.get_feature_names()))
print(tfidf.get_feature_names()[:100])

train_arr=train_1.toarray()
test_arr=test_1.toarray()


# In[ ]:


pd.DataFrame(train_arr[:100], columns=tfidf.get_feature_names())


# # Training of Model
# 
# ### Model 1- Multinomial Naive Bayes

# In[ ]:


get_ipython().run_cell_magic('time', '', 'from sklearn.naive_bayes  import MultinomialNB \nNB_MN=MultinomialNB(alpha=0.52)\nNB_MN.fit(train_arr,train_y)\npred=NB_MN.predict(test_arr)\n')


# In[ ]:


print("first 20 actual labels")
print(test_y.tolist()[:20])
print("first 20 predicted labels")
print(pred.tolist()[:20])


# ## Evaluation of Results

# In[ ]:


from sklearn.metrics  import f1_score,accuracy_score
print("F1 score of the model")
print(f1_score(test_y,pred,average='micro'))
print("Accuracy of the model")
print(accuracy_score(test_y,pred))
print("Accuracy of the model in percentage")
print(round(accuracy_score(test_y,pred)*100,3),"%")


# In[ ]:


from sklearn.metrics import  confusion_matrix
sns.set(font_scale=1.5)
cof=confusion_matrix(test_y, pred)
cof=pd.DataFrame(cof, index=[i for i in range(1,5)], columns=[i for i in range(1,5)])
plt.figure(figsize=(8,8))

sns.heatmap(cof, cmap="PuRd",linewidths=1, annot=True,square=True,cbar=False,fmt='d',xticklabels=['World','Sports','Business','Science'],yticklabels=['World','Sports','Business','Science'])
plt.xlabel("Predicted Class");
plt.ylabel("Actual Class");

plt.title("Confusion Matrix for News Article Classification");

