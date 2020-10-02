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


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import copy
from nltk.corpus import stopwords


# In[ ]:


fake = pd.read_csv('/kaggle/input/fake-and-real-news-dataset/True.csv')
true = pd.read_csv('/kaggle/input/fake-and-real-news-dataset/Fake.csv')


# In[ ]:


fake.head()


# In[ ]:


true.head()


# In[ ]:


fake.groupby('subject').describe()


# In[ ]:


true.groupby('subject').describe()


# In[ ]:


fake.count()


# In[ ]:


true.count()


# In[ ]:


fake['fake'] = 1
true['fake'] = 0


# In[ ]:


merge = pd.merge(fake, true, how='outer')
df = merge.copy()


# In[ ]:


df.count()


# In[ ]:


df['lenght'] = df['title'].apply(len)


# In[ ]:


sns.countplot(df['lenght'], hue='fake', data=df)


# In[ ]:


df.hist(column='lenght', by='fake', figsize=(20,5), bins=50)


# Lets Try with Ttitle only

# In[ ]:


import string

def text_process(title):
    
    nop = [char for char in title if char not in string.punctuation]
    
    nop = ''.join(nop)
    
    return [word for word in nop.split() if word in word.lower() not in stopwords.words('english')]


# ******Modeling**

# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix


# In[ ]:


piplineTitle = Pipeline([
    ('bow', CountVectorizer(analyzer=text_process)),
    ('tfidf', TfidfTransformer()),
    ('classifier', MultinomialNB()),
])


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(df['title'], df['fake'], test_size=0.2, random_state=42)


# In[ ]:


piplineTitle.fit(X_train, y_train)


# In[ ]:


prediction = piplineTitle.fit(X_train, y_train).predict(X_test)

print('Classification report', classification_report(prediction, y_test))

