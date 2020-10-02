#!/usr/bin/env python
# coding: utf-8

# # Multi Class Classification Dataset for Turkish 
# ## Benchmark dataset for Turkish text classification
# * It contians 430K lines, 32 categories
# * Each category roughly has 13K comments  
# * Data is collected from Turkish web sites
# * the data contains the comments of the products and product categories
# * Baseline algoritm , Naive Bayes gets %86 F1 score  as follows

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


from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
import sklearn


# In[ ]:


import pandas as pd
df=pd.read_csv("/kaggle/input/multiclass-classification-data-for-turkish-tc32/ticaret-yorum.csv")
df=df.sample(df.shape[0])
df.head()


# In[ ]:


df.shape


# In[ ]:


df.category.nunique()


# In[ ]:


df.category.value_counts()


# # Baseline Algorithm with Naive Bayes

# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report


# In[ ]:


vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df.text)


# In[ ]:


data_labels=df.category
models_name = ["Multi NB", "LR" ]
#models = [ MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True), LogisticRegression()]
models = [ MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)]
for j in range(len(models)):
 print(models_name[j]+ " ")
 predicted = sklearn.model_selection.cross_val_predict(models[j], X, data_labels , cv=4)
 acc=sklearn.metrics.accuracy_score(data_labels, predicted)    
 print(classification_report(data_labels, predicted))
 print("***")


# In[ ]:




