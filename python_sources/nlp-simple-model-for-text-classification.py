#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
os.listdir("../input")


# In[ ]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# In[ ]:


df=pd.read_csv('../input/GrammarandProductReviews.csv')
df.head()


# In[ ]:


df['reviews.rating'].value_counts()


# In[ ]:


df.isnull().sum()


# In[ ]:


df.dropna(subset=['reviews.text'], inplace=True)


# In[ ]:


df.isnull().sum()


# In[ ]:


X=df['reviews.text']
y=df['reviews.rating']


# In[ ]:


X_vector=TfidfVectorizer().fit_transform(X)


# In[ ]:


X_train, X_test, y_train, y_test=train_test_split(X_vector,y,test_size=0.2, random_state=42)


# In[ ]:


model=RandomForestClassifier()
model.fit(X_train,y_train)
print('In Sample Accuracy: ', model.score(X_train, y_train))


# In[ ]:


y_pred=model.predict(X_test)


# In[ ]:


print('Out Sample Accuracy: ', accuracy_score(y_pred, y_test))


# In[ ]:


cm=confusion_matrix(y_test, y_pred)
cm=pd.DataFrame(cm, index=[i+1 for i in range(5)], columns=[i+1 for i in range(5)])
plt.figure(figsize=(5,5))
sns.heatmap(cm, cmap='Blues',linecolor='black',linewidths=1, annot=True, fmt='')

