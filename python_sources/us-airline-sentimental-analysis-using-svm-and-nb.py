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


import pandas as pd
filename = "/kaggle/input/twitter-airline-sentiment/Tweets.csv"
df = pd.read_csv(filename)
df.head()


# In[ ]:


df['airline_sentiment'].value_counts()


# In[ ]:


df.isnull().sum()


# In[ ]:


x=df['text'].values
y=df['airline_sentiment'].values


# # **Cleaning**

# In[ ]:


from nltk.corpus import stopwords
import string
stop_words = stopwords.words('english')
stop_words += list(string.punctuation)


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y,random_state = 0)


# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 4000, analyzer = 'word', stop_words = stop_words, ngram_range = (1,4), max_df = 0.8)


# In[ ]:


x_train_vec = cv.fit_transform(X_train)
x_test_vec  = cv.transform(X_test)


# # SVM

# In[ ]:


from sklearn.svm import SVC
svc = SVC(gamma = 'auto')
svc.fit(x_train_vec, y_train)


# In[ ]:


svc.score(x_test_vec, y_test)


# # NAIVE BAYES

# In[ ]:


from sklearn.naive_bayes import MultinomialNB
NBClassifer = MultinomialNB(alpha = 0.1)
NBClassifer.fit(x_train_vec, y_train)


# In[ ]:


NBClassifer.score(x_test_vec, y_test)


# In[ ]:


x_test_vec  = cv.transform(X_test)
y_predicted = NBClassifer.predict(x_test_vec)


# In[ ]:


y_predicted


# In[ ]:


np.savetxt("/kaggle/working/output.csv", y_predicted, fmt='%s')


# In[ ]:





# In[ ]:





# In[ ]:




