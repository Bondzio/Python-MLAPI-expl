#!/usr/bin/env python
# coding: utf-8

# This kernel is very basic model. I hope it will help you.
# 
# **Please upvote to encourage me to do more.**

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


train = pd.read_csv('../input/train.csv')
train.head()


# In[ ]:


train['author'].unique()


# **hp lovecraft**
# ![](data:image/jpeg;base64,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)

# **edgar allan poe**
# ![](data:image/jpeg;base64,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)

# **Mary Wollstonecraft Shelley**
# ![](data:image/jpeg;base64,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)

# In[ ]:


import seaborn as sns


# In[ ]:


sns.countplot('author',data = train)


# In[ ]:


train['length'] = train.text.str.count(' ')


# In[ ]:


train.head()


# In[ ]:


train[train["author"]=="MWS"]["length"].describe()


# In[ ]:


train[train["author"]=="HPL"]["length"].describe()


# In[ ]:


train[train["author"]=="EAP"]["length"].describe()


# In[ ]:


train[train['length'] == 860]


# In[ ]:


train.text.values[9215]


# In[ ]:


sns.boxplot(x = 'author',y = 'length',data = train)


# In[ ]:


import nltk


# In[ ]:


print(nltk.word_tokenize(train.text[0]))


# In[ ]:


from sklearn.feature_extraction.text    import CountVectorizer,TfidfVectorizer


# In[ ]:


text = list(train.text.values)
text


# In[ ]:


tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                stop_words='english')
tf = tf_vectorizer.fit_transform(text)


# In[ ]:


print(tf_vectorizer.get_feature_names()[0:100])


# In[ ]:


train.head()


# In[ ]:


from sklearn.model_selection import train_test_split

train1 ,test1 = train_test_split(train,test_size=0.2) 
np.random.seed(0)
train1.head()


# In[ ]:


X_train = train1['text'].values
X_test = test1['text'].values
y_train = train1['author'].values
y_test = test1['author'].values


# In[ ]:


X_train[1],y_train[0]


# In[ ]:


X_test[0],y_test[0]


# In[ ]:


from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import svm


# **Here i used Countvectorizer only, you can try TfidfVectorizer also.**

# In[ ]:


text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', svm.LinearSVC())
                    ])
text_clf = text_clf.fit(X_train,y_train)
y_test_predicted = text_clf.predict(X_test)
np.mean(y_test_predicted == y_test)


# In[ ]:


text_clf = Pipeline([('vect', TfidfVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', svm.LinearSVC())
                    ])
text_clf = text_clf.fit(X_train,y_train)
y_test_predicted = text_clf.predict(X_test)
np.mean(y_test_predicted == y_test)


# In[ ]:


from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier
import xgboost as xgb
import lightgbm as lgbm
from sklearn.naive_bayes import MultinomialNB


# In[ ]:


rfc = RandomForestClassifier()
etrc = ExtraTreesClassifier()
xgbc = xgb.XGBClassifier()
lgbmc = lgbm.LGBMClassifier()
mnb = MultinomialNB()


# In[ ]:


text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', rfc)
                    ])
text_clf = text_clf.fit(X_train,y_train)
y_test_predicted = text_clf.predict(X_test)
np.mean(y_test_predicted == y_test)


# In[ ]:


text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', xgbc)
                    ])
text_clf = text_clf.fit(X_train,y_train)
y_test_predicted = text_clf.predict(X_test)
np.mean(y_test_predicted == y_test)


# In[ ]:


text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', lgbmc)
                    ])
text_clf = text_clf.fit(X_train,y_train)
y_test_predicted = text_clf.predict(X_test)
np.mean(y_test_predicted == y_test)


# In[ ]:


text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', mnb)
                    ])
text_clf = text_clf.fit(X_train,y_train)
y_test_predicted = text_clf.predict(X_test)
np.mean(y_test_predicted == y_test)


# **Here i'm trying to apply LSA and extraxt the top words of author EAP**

# In[ ]:


train.head()


# In[ ]:


text = list(train[train['author']=='EAP'].text.values)


# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(lowercase=True,stop_words='english')


# In[ ]:


X =vectorizer.fit_transform(text)


# In[ ]:


from sklearn.decomposition import TruncatedSVD
lsa = TruncatedSVD(n_components=3,n_iter=500)


# In[ ]:


lsa.fit(X)


# In[ ]:


terms = vectorizer.get_feature_names()


# In[ ]:


for i,comp in enumerate(lsa.components_):
    termsInComp = zip(terms,comp)
    sortedterms = sorted(termsInComp, key=lambda x: x[1],reverse=True)[:10]
    print("Concept %d:" % i)
    for term in sortedterms:
        print(term[0])
    print(" ")


# Further :
# * tune the parameters of the model to get high accuracy
# * clean the data further if needed like removing common words and stop words
# * ensemble models
# * data visulazation
# * if needed feature engineering 
# and many things to do ....
# 
# 

# **More to come...**
# 
# **Please upvote to encourage me.**
# 
# **Thank you :)** 

# In[ ]:




