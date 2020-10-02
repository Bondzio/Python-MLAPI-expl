#!/usr/bin/env python
# coding: utf-8

# **Objective**

# To predict the interest(High, Medium and Low) for new rental listing on RentHop receive.

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


#Preview train data
df_train = pd.read_json(open("../input/train.json", "r"))


# In[ ]:


df_train.head(2)


# In[ ]:


#Preview test data
df_test = pd.read_json(open("../input/test.json", "r"))


# In[ ]:


df_test.head(2)


# In[ ]:


#Find missing values
import missingno as msno
msno.matrix(df_train,figsize=(12,3))


# *Fine, no missing values in the data. So, we can proceed for modelling. No more preprocessing needed.*

# Taking useful columns from the data

# In[ ]:


df_train.columns


# In[ ]:


df_train_useful = df_train[["bathrooms","bedrooms","created","description","display_address","features","interest_level","price"]]


# In[ ]:


#Going to use "Description" for LinearSVC()
df_train_useful["description"].head(10)


# In[ ]:


#Preprocess the "Description" column text
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
stop = stopwords.words('english') + list(string.punctuation)
def desc_preprocess(data):
    return " ".join([i for i in word_tokenize(data.lower()) if i not in stop])


# In[ ]:


#Remove stops words and punctuation from the "Description" column
df_train_useful["Description_preprocessed"] = df_train_useful["description"].apply(desc_preprocess)


# In[ ]:


df_test["Description_preprocessed"] = df_test["description"].apply(desc_preprocess)


# In[ ]:


#Preview "Description" and "Description_preprocessed" data
df_train_useful[["description","Description_preprocessed"]].head(10)


# In[ ]:


df_test.columns


# In[ ]:


#Load attributes and features
X = df_train_useful["Description_preprocessed"]
y = df_train_useful["interest_level"]


# In[ ]:


#Convert the "interest_level" values to numerical by Encoder
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
y = le.fit_transform(y)


# In[ ]:


#Split the data to test,train data
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=1,stratify=y)


# In[ ]:


X_train = X_train.values
y_train = list(y_train)
X_test = X_test.values
y_test = list(y_test)


# In[ ]:


import numpy as np
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import cross_validation
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import log_loss


# In[ ]:


#Using pipeline to combine vectorizer and LinearSVC
svm_classifier = OneVsRestClassifier(LinearSVC())
classifier = Pipeline([
    ('vect', CountVectorizer(stop_words="english")),
    ('tfidf', TfidfTransformer()),
    ('clf2', CalibratedClassifierCV(svm_classifier, cv=2, method='isotonic'))])


# In[ ]:


clf=classifier.fit(X_train, y_train)


# In[ ]:


#Accuracy
scores = cross_validation.cross_val_score(clf, X_test, y_test, cv=5)


# In[ ]:


print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


# In[ ]:


classifier.fit(X_train, y_train)
y_test_pred = clf.predict_proba(X_test)
log_loss(y_test, y_test_pred)


# ##Prediction

# In[ ]:


labels2idx = {le.inverse_transform(label): i for i, label in enumerate(clf.classes_)}
labels2idx


# In[ ]:


X = df_test["Description_preprocessed"]
y = clf.predict_proba(X)


# In[ ]:


sub = pd.DataFrame()
sub["listing_id"] = df_test["listing_id"]
for label in ["high", "medium", "low"]:
    sub[label] = y[:, labels2idx[label]]
sub.to_csv("submission_rf.csv", index=False)

