#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.


# In[ ]:


#import packages needed for data load, analysis and vis
import pandas as pd
import numpy as np
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import seaborn as sns

#Data Preprocessing and Feature Engineering
from textblob import TextBlob
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.sentiment.vader import SentimentIntensityAnalyzer #for sentiment analysis

#import packages needed for model building
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

get_ipython().run_line_magic('matplotlib', 'inline')


# # 1. Load data

# In[ ]:


#train data and test data
import pandas as pd
sample_submission = pd.read_csv("../input/nlp-getting-started/sample_submission.csv")
df_train = pd.read_csv("/kaggle/input/nlp-getting-started/train.csv", sep=",")
df_test = pd.read_csv("/kaggle/input/nlp-getting-started/test.csv", sep=",")


# In[ ]:


df_train.dtypes


# In[ ]:


df_train.head()


# In[ ]:


fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111)

sns.countplot(df_train.target)

plt.show()


# # 2. Text processing using TextBlob
# Getting features from tweet texts

# ### removal of punctions

# In[ ]:


def remove_punctions(tweet):
    tweet_blob = TextBlob(tweet)
    return ' '.join(tweet_blob.words)
df_train['text'] = df_train.text.apply(remove_punctions)


# ### get count of noun words
# The theory is when people tweet about a disaster or bad thing, they are more inclined to use verb instead of noun

# In[ ]:


def get_noun_count(tweet):
    tweet_blob = TextBlob(tweet)
    noun_count = tweet_blob.noun_phrases
    
    return len(noun_count)


# In[ ]:


df_train['noun_count'] = df_train.text.apply(get_noun_count)


# In[ ]:


##visualize
#the result validated the hypothesis above
fig = plt.figure(figsize=(12,5))
ax = fig.add_subplot(111)
sns.boxplot(y = df_train['noun_count'], x=df_train['target'], ax=ax)

plt.show()


# ### Function for Sentiment analysis
# 
# It is easy to understand that people are inclined to be negative instead of positive when disaster happens

# In[ ]:


def sentiment_negpos(tweet):
    vader_analyzer = SentimentIntensityAnalyzer()
    vader_res = vader_analyzer.polarity_scores(tweet)
    
    neg = vader_res['neg']
    pos = vader_res['pos']
    neu = vader_res['neu']
    
    return (neg, pos, neu)


# In[ ]:


negpos_info = df_train.text.apply(sentiment_negpos)
df_train['neg'] = [negpos_info.values[x][0] for x in df_train.index]
df_train['neu'] = [negpos_info.values[x][1] for x in df_train.index]
df_train['pos'] = [negpos_info.values[x][2] for x in df_train.index]


# *the code above takes time*

# In[ ]:


#take a look at the features generated
df_train.head()


# In[ ]:


##visualize
#the result validated the hypothesis above
fig = plt.figure(figsize=(12,5))
ax1 = fig.add_subplot(131)
sns.boxplot(y = df_train['neg'], x=df_train['target'], ax=ax1)

ax2 = fig.add_subplot(132)
sns.boxplot(y = df_train['neu'], x=df_train['target'], ax=ax2)

ax3 = fig.add_subplot(133)
sns.boxplot(y = df_train['pos'], x=df_train['target'], ax=ax3)

plt.show()


# # 3. Model building and evaluate
# 
# As presented above, we generated several features from text and show the differences between target 1 and 0.
# Let's build a Multinomial logistic regression model here to predict the test data.

# In[ ]:


#model building and accuracy check

cols = ['noun_count', 'neg','neu','pos'] 
x = df_train[cols]
y = df_train['target']
# Build a logreg and compute the feature importances
model_multilog = LogisticRegression()
#fit
model_multilog.fit(x, y)
#predict
predicted_target = model_multilog.predict(x)
#accuracy check
print("Accuracy: %.3f" % metrics.accuracy_score(y, predicted_target))
print("Precision: %.3f" % metrics.precision_score(y, predicted_target))
print("Recall: %.3f" % metrics.recall_score(y, predicted_target))

#parameters = model_multilog.coef_


# In[ ]:


#Model Evaluation using Confusion Matrix
cnf_matrix = metrics.confusion_matrix(y, predicted_target)
class_names=[0,1] # name  of classes
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111)

tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)
# create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
ax.xaxis.set_label_position("top")
plt.tight_layout()
plt.title('Confusion matrix', y=1.1)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
plt.show()


# In[ ]:


##Model Evaluation using ROC Curve
y_pred_proba = model_multilog.predict_proba(x)[::,1]
fpr, tpr, _ = metrics.roc_curve(y,  y_pred_proba)
auc = metrics.roc_auc_score(y, y_pred_proba)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()


# AUC score for the case is 0.70. need improvement. 

# # 4. Finish the submission

# In[ ]:


df_test


# In[ ]:


#features generated
df_test['text'] = df_test.text.apply(remove_punctions)
df_test['noun_count'] = df_test.text.apply(get_noun_count)
negpos_info = df_test.text.apply(sentiment_negpos)
df_test['neg'] = [negpos_info.values[x][0] for x in df_test.index]
df_test['neu'] = [negpos_info.values[x][1] for x in df_test.index]
df_test['pos'] = [negpos_info.values[x][2] for x in df_test.index]


# In[ ]:


sample_submission["target"] = model_multilog.predict(df_test[cols])

sample_submission.to_csv("submission.csv", index=False)


# Ref: https://towardsdatascience.com/twitter-sentiment-analysis-classification-using-nltk-python-fa912578614c

# In[ ]:





# In[ ]:




