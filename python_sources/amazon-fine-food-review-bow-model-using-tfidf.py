#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


import matplotlib.pyplot as plt 
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import re 
import sqlite3


# In[ ]:


test=pd.read_csv("/kaggle/input/amazon-fine-food-reviews/Reviews.csv")


# In[ ]:


test.head()


# In[ ]:


test.shape


# In[ ]:


test = test[test.HelpfulnessNumerator <= test.HelpfulnessDenominator]


# In[ ]:


test.shape


# In[ ]:


test['Score'] = test["Score"].apply(lambda x: "positive" if x > 3 else "negative")


# In[ ]:


test.head()


# In[ ]:


sorted_data = test.sort_values('ProductId',axis = 0, inplace = False, kind = 'quicksort',ascending = True)
sorted_data.head()


# In[ ]:


filtered_data = sorted_data.drop_duplicates(subset = {'UserId','ProfileName','Time'} ,keep = 'first', inplace = False)
filtered_data.shape


# In[ ]:


filtered_data['Score'].value_counts()


# In[ ]:


import nltk


# In[ ]:


stop = set(stopwords.words("english"))


# In[ ]:


stop


# In[ ]:


new_stop={'a',
 'about',
 'above',
 'after',
 'again',
 'against',
 
 'all',
 'am',
 'an',
 'and',
 'any',
 'are',

 'as',
 'at',
 'be',
 'because',
 'been',
 'before',
 'being',
 'below',
 'between',
 'both',
 'but',
 'by',
 'can',

 'd',
 'did',

 'do',
 'does',

 'doing',

 'down',
 'during',
 'each',
 'few',
 'for',
 'from',
 'further',
 'had',

 'has',
 'hasn',
 "hasn't",
 'have',

 'having',
 'he',
 'her',
 'here',
 'hers',
 'herself',
 'him',
 'himself',
 'his',
 'how',
 'i',
 'if',
 'in',
 'into',
 'is',

 'it',
 "it's",
 'its',
 'itself',
 'just',
 'll',
 'm',
 'ma',
 'me',

 'more',
 'most',

 'my',
 'myself',

 'no',

 'now',
 'o',
 'of',
 'off',
 'on',
 'once',
 'only',
 'or',
 'other',
 'our',
 'ours',
 'ourselves',
 'out',
 'over',
 'own',
 're',
 's',
 'same',

 'she',
 "she's",
 'should',
 "should've",

 'so',
 'some',
 'such',
 't',
 'than',
 'that',
 "that'll",
 'the',
 'their',
 'theirs',
 'them',
 'themselves',
 'then',
 'there',
 'these',
 'they',
 'this',
 'those',
 'through',
 'to',
 'too',
 'under',
 'until',
 'up',
 've',
 'very',
 'was',

 'we',
 'were',

 'what',
 'when',
 'where',
 'which',
 'while',
 'who',
 'whom',
 'why',
 'will',
 'with',

 'y',
 'you',
 "you'd",
 "you'll",
 "you're",
 "you've",
 'your',
 'yours',
 'yourself',
 'yourselves'}


# In[ ]:


st = PorterStemmer()
st.stem('burned')


# In[ ]:


def cleanhtml(sent):
    cleanr = re.compile('<.*?>')
    cleaned = re.sub(cleanr,' ',sent)
    return cleaned
def cleanpunc(sent):
    clean = re.sub(r'[?|!|$|#|\'|"|:]',r'',sent)
    clean = re.sub(r'[,|(|)|.|\|/]',r' ',clean)
    return clean


# In[ ]:


filtered_data.head()


# In[ ]:


corpus=[]
for p in filtered_data['Text'].values:
    review=cleanhtml(p)
    review=cleanpunc(review)
    review=re.sub('[^a-zA-Z]',' ',review)
    review=review.lower()
    review=review.split()
    ps=PorterStemmer()
    review=[ps.stem(word) for word in review if not word in new_stop]
    review=' '.join(review)
    corpus.append(review)
    
    


# In[ ]:


corpus


# In[ ]:


data={'Textt':corpus,'score':filtered_data['Score']}


# In[ ]:


df=pd.DataFrame(data)


# In[ ]:


df.head()


# In[ ]:


filtered_data.head()


# In[ ]:


filtered_data['Score']=filtered_data['Score'].apply(lambda x: 1 if x =="positive" else 0)


# In[ ]:


filtered_data.head()


# In[ ]:


df['score']=df['score'].apply(lambda x: 1 if x =="positive" else 0)


# In[ ]:


df.head()


# In[ ]:


from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer


# In[ ]:


X=df['Textt'].values


# In[ ]:


X = X[:100000]
y = df['score'].values
y = y[:100000]


# In[ ]:


X


# In[ ]:


y


# In[ ]:


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2,stratify = y)


# In[ ]:


tfidf_vect = TfidfVectorizer(binary =True) 
bow_train = tfidf_vect.fit_transform(X_train)
bow_test = tfidf_vect.transform(X_test)


# In[ ]:


optimal_clf = BernoulliNB(alpha = 0.01)
optimal_clf.fit(bow_train,y_train)
pred  = optimal_clf.predict(bow_test)


# In[ ]:


pred


# In[ ]:


from sklearn.metrics import recall_score , precision_score , roc_auc_score ,roc_curve


# In[ ]:


print(precision_score(y_test,pred,pos_label = 1))


# In[ ]:


from sklearn.metrics import confusion_matrix
import seaborn as sns
confusion = confusion_matrix(y_test , pred)


# In[ ]:


print(confusion)


# In[ ]:


acc = accuracy_score(y_test,pred)*100


# In[ ]:


print(acc)


# In[ ]:




