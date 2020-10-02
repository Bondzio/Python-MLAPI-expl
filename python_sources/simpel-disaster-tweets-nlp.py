#!/usr/bin/env python
# coding: utf-8

# ![image.png](attachment:image.png)

# # Disclaimer! This kernel is only for educational purposes and made for fun therefor the content of the kernel should not be taken to seriously!

# # Importing

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spacy

# machine learning
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# # Loading data

# In[ ]:


BASE = "/kaggle/input/nlp-getting-started/"
train = pd.read_csv(BASE + "train.csv")
test = pd.read_csv(BASE + "test.csv")
sub = pd.read_csv(BASE + "sample_submission.csv")


# In[ ]:


# Load the model to get the vectors
nlp = spacy.load('en_core_web_lg')

tweets = train[['text', 'target']]
tweets.head()


# ## training data prep

# In[ ]:


df=tweets.copy()


# In[ ]:


reviews = df #  300 columns
# We just want the vectors so we can turn off other models in the pipeline
with nlp.disable_pipes():
    vectors = np.array([nlp(tweets.text).vector for idx, tweets in reviews.iterrows()])
    
vectors.shape


# # Model

# In[ ]:


from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(vectors, tweets['target'], 
                                                    test_size=0.1, random_state=1)



# Create the LinearSVC model
model = LinearSVC(random_state=1, dual=False)
# Fit the model
model.fit(X_train,y_train)

# Uncomment and run to see model accuracy
print(f'Model test accuracy: {model.score(X_test, y_test)*100:.3f}%')


# # 5. Prediction and Submition

# In[ ]:


tweets_test = test[['id','text']]
tweets_test.head()


# ## test data prep

# In[ ]:


reviews = tweets_test #
# We just want the vectors so we can turn off other models in the pipeline
with nlp.disable_pipes():
    vectors = np.array([nlp(tweets.text).vector for idx, tweets in reviews.iterrows()])
    
vectors.shape


# In[ ]:


lr_pred = model.predict(vectors)


# In[ ]:


sub['target'] = lr_pred
sub.to_csv("submission.csv", index=False)
sub.head()


# In[ ]:


if len(sub) == len(test):
    print("Submission dataframe is the same length as test ({} rows).".format(len(sub)))
else:
    print("Dataframes mismatched, won't be able to submit to Kaggle.")

