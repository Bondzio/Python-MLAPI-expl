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


import glob
import time
import pandas as pd
# from xml.dom import minidom
from nltk import ngrams
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.stem import PorterStemmer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize


# In[ ]:


import pandas as pd
df = pd.read_csv("../input/sqli.csv",encoding='utf-16')


# In[ ]:




from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer( min_df=2, max_df=0.7, stop_words=stopwords.words('english'))
posts = vectorizer.fit_transform(df['Sentence'].values.astype('U')).toarray()


# In[ ]:


transformed_posts=pd.DataFrame(posts)


# In[ ]:


df=pd.concat([df,transformed_posts],axis=1)


# In[ ]:


X=df[df.columns[2:]]


# In[ ]:


y=df['Label']


# In[ ]:


from sklearn.model_selection import train_test_split


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# In[ ]:


from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(random_state=0).fit(X_train, y_train)


# ### Using Logistic Regression

# In[ ]:


from sklearn.metrics import accuracy_score


# In[ ]:


y_pred=clf.predict(X_test)


# In[ ]:


accuracy_score(y_test, y_pred)


# ### Using simple Neural Network[](http://)

# In[ ]:


from keras.models import Sequential
from keras import layers
from keras.preprocessing.text import Tokenizer
from keras.wrappers.scikit_learn import KerasClassifier


# In[ ]:


input_dim = X_train.shape[1]  # Number of features

model = Sequential()
model.add(layers.Dense(20, input_dim=input_dim, activation='relu'))
model.add(layers.Dense(10,  activation='tanh'))
model.add(layers.Dense(1024, activation='relu'))

model.add(layers.BatchNormalization())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1, activation='sigmoid'))


# In[ ]:


model.compile(loss='binary_crossentropy', 
              optimizer='adam', 
              metrics=['accuracy'])
model.summary()


# In[ ]:


classifier_nn = model.fit(X_train,y_train,
                    epochs=10,
                    verbose=True,
                    validation_data=(X_test, y_test),
                    batch_size=15)


# In[ ]:


pred=model.predict(X_test)


# In[ ]:


for i in range(len(pred)):
    if pred[i]>0.5:
        pred[i]=1
    elif pred[i]<=0.5:
        pred[i]=0


# In[ ]:


accuracy_score(y_test,pred)


# In[ ]:


def accuracy_function(tp,tn,fp,fn):
    
    accuracy = (tp+tn) / (tp+tn+fp+fn)
    
    return accuracy


# In[ ]:


def precision_function(tp,fp):
    
    precision = tp / (tp+fp)
    
    return precision


# In[ ]:


def recall_function(tp,fn):
    
    recall=tp / (tp+fn)
    
    return recall


# In[ ]:


def confusion_matrix(truth,predicted):
    
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0
    
    for true,pred in zip(truth,predicted):
        if true == 1:
            if pred == true:
                true_positive += 1
            elif pred != true:
                false_negative += 1

        elif true == 0:
            if pred == true:
                true_negative += 1
            elif pred != true:
                false_positive += 1
            
    accuracy=accuracy_function(true_positive, true_negative, false_positive, false_negative)
    precision=precision_function(true_positive, false_positive)
    recall=recall_function(true_positive, false_negative)
    
    return (accuracy,
            precision,
           recall)


# In[ ]:


accuracy,precision,recall=confusion_matrix(y_test,pred)


# In[ ]:


print(" Accuracy : {0} \n Precision : {1} \n Recall : {2}".format(accuracy, precision, recall))


# In[ ]:


from sklearn.metrics import precision_score
precision_score(y_test, pred)


# In[ ]:


from sklearn.metrics import recall_score
recall_score(y_test, pred)


# In[ ]:




