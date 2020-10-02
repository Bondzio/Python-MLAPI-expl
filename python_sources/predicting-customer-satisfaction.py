#!/usr/bin/env python
# coding: utf-8

# ## Contents
# **1) Analysis**
# 
# **2) Preprocessing**
# 
# **3) Creating Bag of Words model**
# 
# **4)Creating Naive Bayes classifier**
# 
# **5)Evaluating Training and Test Set**

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


import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


dataset = pd.read_csv('../input/employee_reviews.csv')


# In[ ]:


dataset.head()


# In[ ]:


dataset.info()


# In[ ]:


dataset["overall-ratings"].unique()


# In[ ]:


dataset["Liked"] = [1 if i > 2.5 else 0 for i in dataset['overall-ratings']]


# In[ ]:


dataset['Liked']


# In[ ]:


data = dataset[['pros','Liked']]


# In[ ]:


data


# In[ ]:


sns.countplot(x = data['Liked'],data = data)


# **This plot shows that there are more satisfied employee are there than unsatisfied employee**

# ### Language Preprocessing

# In[ ]:


import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
ss = SnowballStemmer('english')


# In[ ]:


corpus = []
for i in range(0,67529):
    pro = re.sub('[^a-zA_Z]',' ',data['pros'][i])
    pro = pro.lower()
    pro = pro.split()
    pro = [ss.stem(word) for word in pro if word not in set(stopwords.words('english'))]
    pro = ' '.join(pro)
    corpus.append(pro)


# In[ ]:


corpus[0]


# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer


# In[ ]:


cv = CountVectorizer(max_features=2000)


# In[ ]:


x = cv.fit_transform(corpus).toarray()


# In[ ]:


y = data['Liked']


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.2,random_state = 40)


# ### Building Naive Bayes Classifier

# In[ ]:


from sklearn.naive_bayes import MultinomialNB


# In[ ]:


mnb = MultinomialNB()


# In[ ]:


mnb.fit(x_train,y_train)


# In[ ]:


y_pred = mnb.predict(x_test)


# ### Training Set Predictions

# In[ ]:


y_train_pred = mnb.predict(x_train)


# ### Evaluation

# In[ ]:


from sklearn.metrics import classification_report,confusion_matrix,accuracy_score


# ### Training Set Evaluation

# In[ ]:


print(classification_report(y_train,y_train_pred))
print(confusion_matrix(y_train,y_train_pred))


# ### Test Set Evaluation

# In[ ]:


print(classification_report(y_test,y_pred))


# In[ ]:


confusion_matrix(y_test,y_pred)


# In[ ]:


print('Training Accuracy ---->',accuracy_score(y_train,y_train_pred))
print('Testing Accuracy  ---->',accuracy_score(y_test,y_pred))

