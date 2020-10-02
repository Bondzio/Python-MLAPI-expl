#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


df = pd.read_csv('../input/clean_data.csv')


# In[ ]:


df.head()


# In[ ]:


from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


# In[ ]:


clf = Pipeline(steps =[
    ('preprocessing', CountVectorizer()),
    ('classifier', LogisticRegression())
])


# In[ ]:


X = df.SentimentText
y = df.Sentiment


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2,
                                                   random_state = 0)


# In[ ]:


clf.fit(X_train, y_train)


# In[ ]:


clf.score(X_test, y_test)


# In[ ]:


clf.predict(['titanic is a flop'])


# In[ ]:




