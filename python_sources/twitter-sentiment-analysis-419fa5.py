#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # data visualization library
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns # interactive visualization library built on top on matplotlib

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
import re
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.
df = pd.read_csv('/kaggle/input/train.csv') # importing training data


# In[ ]:


df.head()


# In[ ]:


df['tweet'].apply(lambda x : len(x)).plot(kind="hist", bins=50)


# **Data cleaning**

# In[ ]:





# In[ ]:


#df['tweet'].apply(lambda x : len(x)).plot(kind="bar")


# Handle user 

# In[ ]:


def normalizer(tweet):
    tweets = " ".join(filter(lambda x: x[0]!= '@' , tweet.split()))
    return tweets
df["normalized_tweet"]=df['tweet'].apply(normalizer)
df.head()


# remove non alphabetical

# In[ ]:


def normalizer(tweet):
    tweets = re.sub('[^a-zA-Z#]', ' ', tweet)
    return tweets
df["normalized_tweet"]=df['normalized_tweet'].apply(normalizer)
df.head()


# remove short words

# In[ ]:


df["normalized_tweet"]=df['normalized_tweet'].apply(lambda x: ' '.join([ w for w in x.split() if len(w)>3]))
df.head()


# 

# In[ ]:


from nltk.corpus import stopwords

def removing_stops(tweet):
    tweets = ' '.join([word for word in tweet.split() if word not in stopwords.words("english")])
    return tweets

df["normalized_tweet"]=df['normalized_tweet'].apply(removing_stops) 
df.head()


# In[ ]:


df.head()


# In[ ]:


from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
import nltk 

porter = PorterStemmer()
lancaster=LancasterStemmer()

def lemmatization (tweet):
    word_list=nltk.word_tokenize(tweet)
    lemmatized_output = ' '.join([porter.stem(w) for w in word_list])
    return lemmatized_output
df["normalized_tweet"]=df['normalized_tweet'].apply(lemmatization) 


# In[ ]:


df.head()


# In[ ]:


df['normalized_tweet'].apply(lambda x : len(x)).plot(kind="hist",bins=50)


# features engineering 

# tf-idf

# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer


# In[ ]:


vectorizer_tfidf = TfidfVectorizer(ngram_range=(1,3), min_df=10, stop_words=stopwords.words('english'))
tf_idf_matrix = vectorizer_tfidf.fit_transform(df["normalized_tweet"])


# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer
vectorizer_bow = CountVectorizer()
bow= vectorizer_bow.fit_transform(df["normalized_tweet"])


# In[ ]:


import pickle 
pickle.dump(vectorizer_bow, open('bow.sav', 'wb'))
pickle.dump(vectorizer_tfidf, open('tfidf.sav', 'wb'))

#vectorizer_bow
#vectorizer_tfidf


# In[ ]:


from imblearn.under_sampling import RandomUnderSampler
from imblearn.under_sampling import TomekLinks
from imblearn.under_sampling import NeighbourhoodCleaningRule
tl = TomekLinks(return_indices=False, ratio='majority',n_jobs=-1)
rus = RandomUnderSampler(return_indices=False)
ncl=NeighbourhoodCleaningRule(sampling_strategy='majority', n_neighbors=3, n_jobs=-1)


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


#X=tf_idf_matrix.toarray()
X=bow
y=df["label"]

X_rus, y_rus= rus.fit_sample(X, y)
#X_tl, y_tl, id_tl = tl.fit_sample(X, y)

X_train, X_test, y_train, y_test = train_test_split(X_rus, y_rus,stratify= y_rus, test_size=0.33, random_state=42)


# In[ ]:


X_train.shape


# In[ ]:


X_test.shape


# In[ ]:


X_test.shape


# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=13,metric="cosine",n_jobs=-1)
knn.fit(X_train,y_train)
y_pred = knn.predict(X_test)


# In[ ]:


def rapport(y_test, y_pred):
    print(confusion_matrix(y_test,y_pred))
    print(classification_report(y_test, y_pred))
rapport(y_test, y_pred)


# In[ ]:


message_hate="I hate you motherfucker bad detest negative death "


# In[ ]:


message_love="Hate you Fuck you !"


# In[ ]:


def normalizer_all(tweet):
    tweets = " ".join(filter(lambda x: x[0]!= '@' , tweet.split()))
    tweets = re.sub('[^a-zA-Z]', ' ', tweets)
    tweets = tweets.lower()
    tweets = tweets.split()
    tweets = [word for word in tweets if not word in set(stopwords.words('english'))]
    tweets =' '.join([porter.stem(w) for w in tweets])
    return tweets
clean_message=normalizer_all(message_love)
clean_message


# In[ ]:


a=vectorizer_bow.transform([clean_message])


# In[ ]:


#a.shape


# In[ ]:


#svm_bow.predict(a)


# In[ ]:


#svm_bow.predict_proba(a)


# In[ ]:





# In[ ]:


from sklearn import svm
SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto',class_weight='balanced',probability=True)
SVM.fit(X_train,y_train)
y_pred = SVM.predict(X_test)


# In[ ]:


rapport(y_test, y_pred)


# In[ ]:


SVM.predict(a.toarray())
SVM.predict_proba(a.toarray())


# In[ ]:


from sklearn.linear_model import LogisticRegression
log_reg=LogisticRegression(verbose=1, solver='liblinear',random_state=0, C=5, penalty='l2',max_iter=10000)
log_reg.fit(X_train,y_train)
y_pred = log_reg.predict(X_test)


# In[ ]:


rapport(y_test, y_pred)


# In[ ]:


log_reg.predict_proba(a)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier

clf=RandomForestClassifier(n_estimators=200, max_depth=5, random_state=0)#,class_weight={0:0.49,1:0.52}
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)


# In[ ]:





# In[ ]:


rapport(y_test, y_pred)


# In[ ]:


knn = KNeighborsClassifier(n_neighbors=13,metric="cosine",n_jobs=-1)
SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto',class_weight='balanced',probability=True)
log_reg=LogisticRegression(verbose=1, solver='liblinear',random_state=0, C=5, penalty='l2',max_iter=10000)


# In[ ]:


X_bow=bow
y=df["label"]
X_bow_rus, y_bow_rus= rus.fit_sample(X_bow, y)
knn_bow=knn
knn_bow.fit(X_bow_rus, y_bow_rus)
svm_bow=SVM
svm_bow.fit(X_bow_rus, y_bow_rus)
log_reg_bow=log_reg
log_reg_bow.fit(X_bow_rus, y_bow_rus)


# In[ ]:


X_bow_rus.shape


# In[ ]:


import pickle 
pickle.dump(knn_bow, open('knn_bow.sav', 'wb'))
pickle.dump(svm_bow, open('svm_bow.sav', 'wb'))
pickle.dump(log_reg_bow, open('log_reg_bow.sav', 'wb'))


# In[ ]:



X_bow=bow
y=df["label"]
X_bow_rus, y_bow_rus= rus.fit_sample(X_bow, y)
knn_bow=knn
knn_bow.fit(X_bow_rus, y_bow_rus)
svm_bow=SVM
svm_bow.fit(X_bow_rus, y_bow_rus)
#log_reg_bow=log_reg
#log_reg_bow.fit(X_bow_rus, y_bow_rus)


# In[ ]:





# In[ ]:





# * knn_bow \\
# * svm_bow \\
# * log_reg_bow
# 

# In[ ]:


X_bow_rus.shape


# In[ ]:


svm_bow


# In[ ]:


y_pred =svm_bow.predict(X_test.toarray())
rapport(y_test, y_pred)


# In[ ]:


test= pd.read_csv('/kaggle/input/test.csv') # importing training data


# In[ ]:


test.head()


# In[ ]:


def normalizer_all(tweet):
    tweets = " ".join(filter(lambda x: x[0]!= '@' , tweet.split()))
    tweets = re.sub('[^a-zA-Z]', ' ', tweets)
    tweets = tweets.lower()
    tweets = tweets.split()
    tweets = [word for word in tweets if not word in set(stopwords.words('english'))]
    tweets =' '.join([porter.stem(w) for w in tweets])
    return tweets
test["clean"]=test['tweet'].apply(normalizer_all)


# In[ ]:


test.head()


# In[ ]:


a=vectorizer_bow.transform(test["clean"].values)


# In[ ]:


a.shape


# In[ ]:


test.shape


# In[ ]:


y_pred =svm_bow.predict_proba(a.toarray())


# In[ ]:


test['%loyal']=y_pred[:,0]
test['%not_loyal']=y_pred[:,1]


# In[ ]:


test.head(n=10)


# In[ ]:


test.to_csv('out.csv', index = False)


# In[ ]:


""""
X=tf_idf_matrix.toarray()
y=df["label"]
X_tfidf_rus, y_tfidf_rus= rus.fit_sample(X, y)
knn_tfidf=knn
knn_tfidf.fit(X_tfidf_rus, y_tfidf_rus)
svm_tfidf=SVM
svm_tfidf.fit(X_tfidf_rus, y_tfidf_rus)
log_reg_tfidf=log_reg
log_reg_tfidf.fit(X_tfidf_rus, y_tfidf_rus)
"""


# * svm_tfidf
# * knn_tfidf
# * log_reg_tfidf

# In[ ]:


#y_pred = svm_bow.predict(X_test.toarray())


# * knn_bow \\
# * svm_bow \\
# * log_reg_bow
# 

# * svm_tfidf
# * knn_tfidf
# * log_reg_tfidf

# In[ ]:


""""import pickle 
pickle.dump(knn_bow, open('knn_bow.sav', 'wb'))
pickle.dump(svm_bow, open('svm_bow.sav', 'wb'))
pickle.dump(log_reg_bow, open('log_reg_bow.sav', 'wb'))
pickle.dump(svm_tfidf, open('svm_tfidf.sav', 'wb'))
pickle.dump(knn_tfidf, open('knn_tfidf.sav', 'wb'))
pickle.dump(log_reg_tfidf, open('log_reg_tfidf.sav', 'wb'))
pickle.dump(vectorizer_bow, open('bow.sav', 'wb'))
pickle.dump(vectorizer_tfidf, open('tfidf.sav', 'wb'))"""

