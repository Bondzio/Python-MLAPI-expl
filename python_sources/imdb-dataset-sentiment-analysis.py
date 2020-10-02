#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from keras.models import Sequential 
from keras.layers import Dense 
import matplotlib.pyplot as plt

from textblob import TextBlob
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble
from sklearn import metrics
import textblob, string
from keras.preprocessing import text, sequence
from keras import layers, models, optimizers

import nltk
from nltk.corpus import stopwords


import pandas as pd
import seaborn as sns


# In[ ]:


test = pd.read_csv('../input/imdb-dataset-sentiment-analysis-in-csv-format/Test.csv')
train = pd.read_csv('../input/imdb-dataset-sentiment-analysis-in-csv-format/Train.csv')
valid = pd.read_csv('../input/imdb-dataset-sentiment-analysis-in-csv-format/Valid.csv')


# In[ ]:


train.head()


# In[ ]:


test.head()


# In[ ]:


valid.head()


# In[ ]:


plt.style.use('fivethirtyeight')
sns.countplot(data=train,x='label')


# In[ ]:


sns.countplot(data=test,x='label')


# In[ ]:


sns.countplot(data=valid,x='label')


# In[ ]:


def transformations(dataframe):
    # upper to lower character
    dataframe['text'] = dataframe['text'].apply(lambda x: " ".join(x.lower() for x in x.split()))
    #punctuations
    dataframe['text'] = dataframe['text'].str.replace('[^\w\s]','')
    #numbers
    dataframe['text'] = dataframe['text'].str.replace('\d','')
    # 
    sw = stopwords.words('english')
    dataframe['text'] = dataframe['text'].apply(lambda x: " ".join(x for x in x.split() if x not in sw))
    #rare characters deleting
    sil = pd.Series(' '.join(dataframe['text']).split()).value_counts()[-1000:]
    dataframe['text'] = dataframe['text'].apply(lambda x: " ".join(x for x in x.split() if x not in sil))
    
    #lemmi
    from textblob import Word
    #nltk.download('wordnet')
    dataframe['text'] = dataframe['text'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()])) 
    return dataframe


# In[ ]:


train = transformations(train)
train.head()


# In[ ]:


test = transformations(test)
test.head()


# In[ ]:


valid = transformations(valid)
valid.head()


# In[ ]:


train_x = train['text']
valid_x = valid["text"]
train_y = train["label"]
valid_y = valid["label"]


# In[ ]:


vectorizer = CountVectorizer()


# In[ ]:


vectorizer.fit(train_x)


# In[ ]:


x_train_count = vectorizer.transform(train_x)
x_valid_count = vectorizer.transform(valid_x)
x_test_count  = vectorizer.transform(test["text"])


# In[ ]:


model = Sequential() 
model.add(Dense(50,input_dim=x_train_count.shape[1], kernel_initializer="uniform", activation="relu")) 
#model.add(Dense(6, kernel_initializer="uniform", activation="relu")) 
model.add(Dense(1, kernel_initializer="uniform", activation="sigmoid")) 
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
# Fit the model
history = model.fit(x_train_count, train_y.values.reshape(-1,1), validation_data=(x_valid_count,valid_y), nb_epoch=2, batch_size=128)


# In[ ]:


# evaluate
loss, acc = model.evaluate(x_test_count, test["label"], verbose=0)
print('Test Accuracy: %f' % (acc*100))


# In[ ]:


comments = pd.Series(test["text"])
comments = vectorizer.transform(comments)


# In[ ]:


y_pred = model.predict_classes(comments)
nn_cm = metrics.confusion_matrix(test["label"],y_pred)
print(nn_cm)


# In[ ]:


comment_1 = pd.Series("this film is very nice and good i like it")
comment_2 = pd.Series("no not good look at that shit very bad")


# In[ ]:


comment_1  = vectorizer.transform(comment_1)
comment_2 = vectorizer.transform(comment_2)


# In[ ]:


model.predict_classes(comment_1)


# In[ ]:


model.predict_classes(comment_2)

