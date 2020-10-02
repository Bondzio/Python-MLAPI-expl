#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

import nltk
from nltk.tokenize import word_tokenize 

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[2]:


df = pd.read_csv("../input/salary-train.csv")
df.head()
df.shape


# In[3]:


import string
def remove_punctuation_lower(s):
    s1 = s.lower()
    s2=''
    for word in s1:
        if word.isalnum()==True:
            s2=s2+word
        else:
            s2=s2+' '
        
    return s2


# In[4]:


df['FullDescription']=df['FullDescription'].apply(remove_punctuation_lower)


# In[5]:


df.head()


# In[6]:


from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(min_df=0.00008).fit(df['FullDescription'])


# In[7]:


tfidf_transform=tfidf.transform(df['FullDescription'])


# In[8]:


print(tfidf_transform)


# In[ ]:





# In[9]:


df['LocationNormalized'].fillna('nan', inplace=True)
df['ContractTime'].fillna('nan', inplace=True)


# In[10]:


from sklearn.feature_extraction import DictVectorizer
enc=DictVectorizer()
df1=enc.fit_transform(df[['LocationNormalized','ContractTime']].to_dict('records'))
#x=list(df['LocationNormalized'].value_counts().index)
#dict_location={x:i for (x, i) in zip(x,list(range(len(x))))}


# In[11]:


df1.shape


# In[19]:


from scipy.sparse import coo_matrix, hstack
A=tfidf_transform
B=df1
X_new=hstack([A,B])


# In[20]:


X_new.shape


# In[21]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_new, df['SalaryNormalized'], test_size=0.25, random_state=5)


# In[22]:


from sklearn.linear_model import Ridge
ridge=Ridge(alpha=1.0).fit(X_train,y_train)
y_pred = ridge.predict(X_test)


# In[24]:


from sklearn.metrics import mean_squared_error
mean_squared_error(y_test, y_pred)


# In[25]:


alpha=np.logspace(-2,2,5)
print(alpha)


# In[29]:


from sklearn.model_selection import GridSearchCV
ridge_params={'alpha':np.logspace(-2,2,5)}
ridge_grid=GridSearchCV(ridge,ridge_params,cv=5)
ridge_grid.fit(X_train,y_train)


# In[30]:


ridge_grid.best_params_


# In[31]:


from sklearn.metrics import r2_score
r2_score(y_test, y_pred)


# In[ ]:




