#!/usr/bin/env python
# coding: utf-8

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


import pandas as pd 
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
import nltk


# In[ ]:


data = pd.read_csv('/kaggle/input/amazon-music-reviews/Musical_instruments_reviews.csv')
data.head()


# In[ ]:


import pandas_profiling
data.profile_report(title='Sentiment Analysis - Report' , progress_bar = False)


# Deleting na values from reviews

# In[ ]:



data.reviewText.fillna("",inplace = True)

data.isna().sum()



# Data Preprocessing
# 

# In[ ]:


del data['reviewerID']
del data['asin']
del data['reviewerName']
del data['helpful']
del data['unixReviewTime']
del data['reviewTime']
data.head()


# In[ ]:


data['rtexts'] = data['reviewText'] + ' ' + data['summary']
del data['summary']
del data['reviewText']
data.head()


# In[ ]:


data.overall.value_counts()


# Creating a function to change values for rating and make it binary 

# In[ ]:


def convert_rating(rating):
    if(int(rating == 1) or int(rating) == 2 or int(rating) == 3):
        return 0
    else:
        return 1
   
    
data.overall = data.overall.apply(convert_rating)


# In[ ]:


data.head()
data.overall.value_counts()


# In[ ]:


sn.set(style="darkgrid")
sn.countplot(x = 'overall' , hue = 'overall' , data = data)
plt.show()


# As we cann see it is a hugely unbalanced data set , Balance this with oversampling

# Let's do the data preprocessing

# In[ ]:


from nltk.corpus import stopwords
import string
stop = set(stopwords.words('english'))
punctuation = list(string.punctuation)
stop.update(punctuation)


# In[ ]:


from nltk.corpus import wordnet
from nltk import pos_tag
def get_simple_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


# In[ ]:


from nltk.stem import LancasterStemmer,WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
def lemmatize_words(text):
    final_text = []
    for i in text.split():
        if i.strip().lower() not in stop:
            pos = pos_tag([i.strip()])
            word = lemmatizer.lemmatize(i.strip(),get_simple_pos(pos[0][1]))
            final_text.append(word.lower())
    return " ".join(final_text)


# In[ ]:


data.head()


# In[ ]:


data.rtexts = data.rtexts.apply(lemmatize_words)


# In[ ]:


data.head()


# In[ ]:


X = data['rtexts']
Y = data['overall']


# We will implement tf idf on our words and then try to balance our data set

# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer
   
tf=TfidfVectorizer(min_df=0,max_df=1,use_idf=True,ngram_range=(1,2))
  
X=tf.fit_transform(X)    
    


# In[ ]:


X.shape


# Balancing the imbalance data set

# In[ ]:


from imblearn.combine import SMOTETomek
from imblearn.under_sampling import NearMiss

smk = SMOTETomek(random_state=42 , sampling_strategy = 0.8)
X_res,y_res=smk.fit_sample(X,Y)

y_res.value_counts()


# Applying logistic regression on it

# In[ ]:


from sklearn.model_selection import train_test_split
x_train1,x_test1,y_train1,y_test1 = train_test_split(X_res,y_res,test_size = 0.2 , random_state = 0)


# In[ ]:


from sklearn.linear_model import LogisticRegression
logistic=LogisticRegression(penalty='l2',max_iter=500,C=1,random_state=0)


# In[ ]:


lr=logistic.fit(x_train1,y_train1)
print(lr)


# In[ ]:


lr_predict1=lr.predict(x_test1)


# In[ ]:


from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
lr_tfidf_report1=classification_report(y_test1,lr_predict1,target_names=['0','1'])
print(lr_tfidf_report1)


# Applying Multinomial naive bayes on it 

# In[ ]:


from sklearn.naive_bayes import MultinomialNB
mnb=MultinomialNB()
mnb_model=mnb.fit(x_train1,y_train1)


# In[ ]:


mnb_bow_predict=mnb_model.predict(x_test1)
mnb_bow1=mnb_model.predict(x_train1)


# In[ ]:


mnb_bow_report = classification_report(y_test1,mnb_bow_predict)
print(mnb_bow_report)
mnb_bow_repor = classification_report(y_train1,mnb_bow1)
print(mnb_bow_repor)

