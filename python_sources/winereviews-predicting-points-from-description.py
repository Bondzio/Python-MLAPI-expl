#!/usr/bin/env python
# coding: utf-8

# I'll try Predicting points from description using WineReviews dataset.

# Importing libraries.

# In[ ]:


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# loading dataset.

# In[ ]:


wine_base = pd.read_csv(os.path.join('../input/', 'winemag-data-130k-v2.csv'))
wine_base.head(5)


# spliting train set and test set.

# In[ ]:


from sklearn.model_selection import train_test_split
X = wine_base.drop(['points'], axis=1)
y = wine_base['points'].copy()

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)


# make vectors from description by countvectorizer.

# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

#vect = CountVectorizer(tokenizer=custom_tokenizer, min_df=5)
vect = CountVectorizer(min_df=5)
vect.fit(X_train['description'])
print("vocabulary size: {}".format(len(vect.vocabulary_)))
X_train_vectored = vect.transform(X_train['description'])


# In[ ]:


feature_names = vect.get_feature_names()
print("Number of Features: ", len(feature_names))
print("First 20 features: \n{}".format(feature_names[:20]))
print("features 10010 to 10030:\n{}".format(feature_names[10010:10030]))
print("Every 2000th feature:\n{}".format(feature_names[::2000]))


# train linear regression model,

# In[ ]:


from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import GridSearchCV

lr = LinearRegression()
lr.fit(X_train_vectored, y_train)


# evaluate predict result.

# In[ ]:


from sklearn.metrics import mean_squared_error
y_pred = lr.predict(X_train_vectored)
mse = mean_squared_error(y_train, y_pred)
rmse = np.sqrt(mse)
rmse


# It seems that it got a score not so bad.
# let's predict test set points.

# In[ ]:


X_test_vectored = vect.transform(X_test['description'])
y_test_pred = lr.predict(X_test_vectored)
mse = mean_squared_error(y_test, y_test_pred)
rmse = np.sqrt(mse)
rmse

