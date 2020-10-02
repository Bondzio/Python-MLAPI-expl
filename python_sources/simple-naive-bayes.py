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


# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


f1=pd.read_json('/kaggle/input/news-headlines-dataset-for-sarcasm-detection/Sarcasm_Headlines_Dataset.json',lines=True)


# In[ ]:


f2=pd.read_json('/kaggle/input/news-headlines-dataset-for-sarcasm-detection/Sarcasm_Headlines_Dataset_v2.json',lines=True)


# In[ ]:


df=pd.concat([f1,f2],axis=0,sort=False).drop('article_link',axis=1)
df.head()


# In[ ]:


df.info()


# In[ ]:


df.describe()


# In[ ]:


plt.hist(df['is_sarcastic'])
plt.show()


# In[ ]:


X=df['headline']
y=df['is_sarcastic']


# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer()


# In[ ]:


X=cv.fit_transform(X)


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=101)


# In[ ]:


from sklearn.naive_bayes import MultinomialNB


# In[ ]:


nb=MultinomialNB()


# In[ ]:


nb.fit(X_train,y_train)


# In[ ]:


pre=nb.predict(X_test)


# In[ ]:


from  sklearn.metrics import confusion_matrix,classification_report


# In[ ]:


print(confusion_matrix(y_test,pre))


# In[ ]:


print(classification_report(y_test,pre))


# In[ ]:




