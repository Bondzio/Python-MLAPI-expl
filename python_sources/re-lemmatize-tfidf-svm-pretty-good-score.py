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


# data exploring and basic libraries
import random
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from collections import deque as dq

# NLP preprocessing
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize as TK
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder as LE

# binary class classification model
from sklearn.svm import SVC

# One vs All wrapper
from sklearn.multiclass import OneVsRestClassifier as OVRC

# Pretty display for notebooks
from IPython.display import display # Allows the use of display() for DataFrames
get_ipython().run_line_magic('matplotlib', 'inline')


# In[ ]:


# load the data - test data
rawdf_te = pd.read_json(path_or_buf='../input/test.json')
rawdf_te.head(n=3)
# load the data - train data
rawdf_tr = pd.read_json(path_or_buf='../input/train.json')
rawdf_tr.head(n=3)


# In[ ]:


# cuisine distribution
sns.countplot(y='cuisine', data=rawdf_tr, palette ='Set3')

# number of recipes for each cuisines
print('Weight\t Recipe\t Cuisine\n')
for _ in (Counter(rawdf_tr['cuisine']).most_common()):print(round(_[1]/rawdf_tr.cuisine.count()*100, 2),'%\t',_[1],'\t', _[0])


# In[ ]:


# change id column type to string
rawdf_tr = rawdf_tr.set_index('id')
rawdf_te = rawdf_te.set_index('id')

# Total number of recipes
print('Total of %d recipes\n'% len(rawdf_tr))

# total number of UNIQUE cuisines
print('Total of %d types of cuisines including %s\n' %       (len(rawdf_tr['cuisine'].unique()), rawdf_tr['cuisine'].unique().tolist()))
                                          
# UNIQUE # ingredients set - ingredients_set()
# training ingredient list
ingredients_list_tr = []
for _ in rawdf_tr['ingredients']:
    ingredients_list_tr.append(_)
# ingredients set - ingredients_set()
ingredients_set_tr = set()
for a in range(len(ingredients_list_tr)):
    for _ in range(len(ingredients_list_tr[a])):
        ingredients_set_tr.add(ingredients_list_tr[a][_])
print("Total of %d unique ingredients\n" % len(ingredients_set_tr))

# total ingredients list (with repition) occurred in the train data
total_ingredients_list_tr = []
for i in range(len(ingredients_list_tr)):
    for j in range(len(ingredients_list_tr[i])):
        total_ingredients_list_tr.append(ingredients_list_tr[i][j])
print("Most common ingredients used:\n")
for _ in range(len(Counter(total_ingredients_list_tr).most_common(11))):
    print(Counter(total_ingredients_list_tr).most_common(11)[_])


# What does the ingredients column look like?

# In[ ]:


print(rawdf_tr['ingredients'].loc[41935])
print(rawdf_tr['ingredients'].loc[27566])
print(rawdf_tr['ingredients'].loc[32596])
print(rawdf_tr['ingredients'].loc[8476])


# Preprocess the datasets

# In[ ]:


# copy the series from the dataframe
ingredients_tr = rawdf_tr['ingredients']
# do the test.json while at it
ingredients_te = rawdf_te['ingredients']


# In[ ]:


# substitute the matched pattern
def sub_match(pattern, sub_pattern, ingredients):
    for i in ingredients.index.values:
        for j in range(len(ingredients[i])):
            ingredients[i][j] = re.sub(pattern, sub_pattern, ingredients[i][j].strip())
            ingredients[i][j] = ingredients[i][j].strip()
    re.purge()
    return ingredients

def regex_sub_match(series):
    # remove all units
    p0 = re.compile(r'\s*(oz|ounc|ounce|pound|lb|inch|inches|kg|to)\s*[^a-z]')
    series = sub_match(p0, ' ', series)
    # remove all digits
    p1 = re.compile(r'\d+')
    series = sub_match(p1, ' ', series)
    # remove all the non-letter characters
    p2 = re.compile('[^\w]')
    series = sub_match(p2, ' ', series)
    return series


# In[ ]:


# regex train data
ingredients_tr = regex_sub_match(ingredients_tr)
# regex test.json data
ingredients_te = regex_sub_match(ingredients_te)


# Lemmatize!

# In[ ]:


# declare instance from WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# remove all the words that are not nouns -- keep the essential ingredients
def lemma(series):
    for i in series.index.values:
        for j in range(len(series[i])):
            # get rid of all extra spaces
            series[i][j] = series[i][j].strip()
            # Tokenize a string to split off punctuation other than periods
            token = TK(series[i][j])
            # set all the plural nouns into singular nouns
            for k in range(len(token)):
                token[k] = lemmatizer.lemmatize(token[k])
            token = ' '.join(token)
            # write them back
            series[i][j] = token
    return series


# In[ ]:


# lemmatize the train data
ingredients_tr = lemma(ingredients_tr)
# lemmatize test.json
ingredients_te = lemma(ingredients_te)


# What do they look like now?

# In[ ]:


print(ingredients_tr[41935])
print(ingredients_tr[27566])
print(ingredients_tr[32596])
print(ingredients_tr[8476])


# In[ ]:


# copy back to the dataframe
rawdf_tr['ingredients_lemma'] = ingredients_tr
rawdf_tr['ingredients_lemma_string'] = [' '.join(_).strip() for _ in rawdf_tr['ingredients_lemma']]
# do the same for the test.json dataset
rawdf_te['ingredients_lemma'] = ingredients_te
rawdf_te['ingredients_lemma_string'] = [' '.join(_).strip() for _ in rawdf_te['ingredients_lemma']]


# TF-IDF vectorizing

# In[ ]:


# DataFrame for training and validation
traindf = rawdf_tr[['cuisine', 'ingredients_lemma_string']].reset_index(drop=True)
# same for the test set
testdf = rawdf_te[['ingredients_lemma_string']]


# In[ ]:


# training ===================
# X_train
X_train = traindf['ingredients_lemma_string']
vectorizertr = TfidfVectorizer(stop_words='english', analyzer="word", max_df=0.65, min_df=2, binary=True)
X_train = vectorizertr.fit_transform(X_train)

# y_train
y_train = traindf['cuisine']
# for xgboost the labels need to be labeled with encoder
le = LE()
y_train_ec = le.fit_transform(y_train)

# predicting =================
# X_pred
X_pred = testdf['ingredients_lemma_string']
vectorizerts = TfidfVectorizer(stop_words='english')
X_pred = vectorizertr.transform(X_pred)

# y_true


# > SVM model wiht 'ovr'

# In[ ]:


# Best parameters after running the grid search for One-Versus-All SVM
clf_ovrc_svm = SVC(C=3.25, cache_size=500, class_weight=None, coef0=0.0,  decision_function_shape='ovr', degree=3, gamma=1, kernel='rbf',  max_iter=-1, probability=False, random_state=0, shrinking=True,  tol=0.001, verbose=False)

clf_ovrc_svm = clf_ovrc_svm.fit(X_train, y_train)

y_pred_ovrc_svm = clf_ovrc_svm.predict(X_pred)

testdf['cuisine'] = y_pred_ovrc_svm
d = pd.DataFrame(data=testdf['cuisine'], index=testdf.index).sort_index().reset_index().to_csv('submission_ovr_svm.csv', index=False)

