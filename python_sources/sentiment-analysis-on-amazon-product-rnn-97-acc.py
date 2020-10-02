#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression
from keras.preprocessing.sequence import pad_sequences


from collections import Counter
import nltk
import seaborn as sns
import string
from nltk.corpus import stopwords
# import re
# from autocorrect import spell
import regex as re

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

from keras.models import Sequential
from keras.layers import Dense
from keras.backend import eval
from keras.optimizers import Adam
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.layers import Dropout
from keras.layers.convolutional import Conv1D,MaxPooling1D
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


# In[ ]:


data=pd.read_csv('../input/1429_1.csv')
data.head()


# In[ ]:


# yelp['label'] = ['1' if star > 3 else '0' for star in yelp['stars']];


# In[ ]:


review=pd.DataFrame(data.groupby('reviews.rating').size().sort_values(ascending=False).rename('No of Users').reset_index())
review.head()


# import seaborn as sns
# import matplotlib.pyplot as plt
# sns.set(style="whitegrid")
# 
# f, ax = plt.subplots(figsize=(15, 10))
# sns.set_color_codes("pastel")
# sns.barplot(y="reviews.rating", x="No of Users", data=review.iloc[:20, :10],label="Score", color="pink")
# 
# ax.legend(ncol=2, loc="upper left", frameon=True)
# ax.set(xlabel="No of People",ylabel="Rating")
# sns.despine(left=True, bottom=True)
# plt.show()

# In[ ]:


permanent = data[['reviews.rating' , 'reviews.text' , 'reviews.title' , 'reviews.username']]
mpermanent=permanent.dropna()
mpermanent.head()


# In[ ]:


check =  mpermanent[mpermanent["reviews.text"].isnull()]
check.head()


# In[ ]:


actualrating = mpermanent[(mpermanent['reviews.rating'] == 1) | (mpermanent['reviews.rating'] == 5)]
actualrating.shape


# In[ ]:


y = actualrating['reviews.rating']
x = actualrating['reviews.text'].reset_index()
# X =x[xindex(False)]


# In[ ]:


len(y)
# len(X)


# In[ ]:


X = x['reviews.text']
print(X)


# In[ ]:


print(len(X))


# In[ ]:


import string
from nltk.corpus import stopwords
# stop=set(stopwords.words('english'))
def text_process(text):
    '''
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove all stopwords
    3. Return the cleaned text as a list of words
    '''
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]


# In[ ]:


tokens = X[0].split()
print(tokens)


# In[ ]:


sample_text = "Hey there! This is a sample review, which happens to contain punctuations."
print(text_process(sample_text))


# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer
# next we need to vectorize our input variable (X)
#we use the count vectoriser function and the analyser we use is the above lines of code
# this should return a vector array
bow_transformer = CountVectorizer(analyzer=text_process).fit(X)


# In[ ]:


len(bow_transformer.vocabulary_)


# In[ ]:


review_24 = X[24]


# In[ ]:


bow_25 = bow_transformer.transform([review_24])
bow_25


# In[ ]:


print(bow_25)


# In[ ]:


X = bow_transformer.transform(X)


# In[ ]:


#Lets start training the model
from sklearn.model_selection import train_test_split
#using 30% of the data for testing, this will be revised once we do not get the desired accuracy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)


# **Naive Bayes Classifier**

# In[ ]:


from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()
nb.fit(X_train, y_train)


# In[ ]:


preds = nb.predict(X_test)


# In[ ]:


from sklearn.metrics import confusion_matrix, classification_report
print(confusion_matrix(y_test, preds))
print('\n')
print(classification_report(y_test, preds))
nb.score(X_train, y_train)


# **support vector machine**

# In[ ]:


from sklearn.svm import SVC
clf = SVC()
clf.fit(X_train, y_train) 
predsvm=clf.predict(X_test)


# In[ ]:


from sklearn.metrics import confusion_matrix, classification_report
print(confusion_matrix(y_test, preds))
print('\n')
print(classification_report(y_test, predsvm))
predsvm=clf.predict(X_test)
clf.score(X_train,y_train)


# **KNeighborsClassifier**

# In[ ]:


from sklearn.neighbors import KNeighborsClassifier
neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(X, y) 


# In[ ]:


predsknn=neigh.predict(X_test)


# In[ ]:


from sklearn.metrics import confusion_matrix, classification_report
print(confusion_matrix(y_test, predsknn))
print('\n')
print(classification_report(y_test, predsknn))
neigh.score(X_train,y_train)


# **GradientBoostingClassifier**

# In[ ]:


from sklearn.ensemble import GradientBoostingClassifier
model= GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
model.fit(X_train, y_train)
predicted= model.predict(X_test)


# In[ ]:


from sklearn.metrics import confusion_matrix, classification_report
print(confusion_matrix(y_test, predicted))
print('\n')
print(classification_report(y_test, predicted))
model.score(X_train,y_train)


# In[ ]:


positive_review = actualrating['reviews.text'][2]
positive_review


# In[ ]:


positive_review_transformed = bow_transformer.transform([positive_review])
nb.predict(positive_review_transformed)[0]


# In[ ]:


positive_review = actualrating['reviews.text'][11]
positive_review


# In[ ]:


positive_review_transformed = bow_transformer.transform([positive_review])
model.predict(positive_review_transformed)[0]


# In[ ]:


negative_review = mpermanent['reviews.text'][34650]
print(negative_review)


# In[ ]:


negative_review_transformed = bow_transformer.transform([negative_review])
nb.predict(negative_review_transformed)[0]


# In[ ]:


negative_review_transformed = bow_transformer.transform([negative_review])
neigh.predict(negative_review_transformed)[0]


# In[ ]:


negative_review = mpermanent['reviews.text'][34656]
print(negative_review)


# In[ ]:


negative_review_transformed = bow_transformer.transform([negative_review])
nb.predict(negative_review_transformed)[0]


# In[ ]:


negative_review_transformed = bow_transformer.transform([negative_review])
neigh.predict(negative_review_transformed)[0]


# In[ ]:


#we need to have a label for 
# lets have a label which group the stars into two groups, 1 for good, 0 for bad 
# so anything more than 3 , 3 being neutral is good, rest bad
# data['label'] = ['1' if reviews.rating > 3 else '0' for reviews.rating in data['reviews.rating']];
mpermanent['label'] = ['1' if star >= 3 else '0' for star in mpermanent['reviews.rating']];


# In[ ]:


mpermanent


# In[ ]:


mpermanent.tail()


# In[ ]:


reviews = mpermanent['reviews.text']
labels = mpermanent['label']


# In[ ]:


print(len(reviews))


# In[ ]:


print(len(labels))


# In[ ]:


reviews[3]


# In[ ]:


stop = set(stopwords.words('english'))


# In[ ]:


def clean_document(doco):
    punctuation = string.punctuation
    punc_replace = ''.join([' ' for s in punctuation])
    doco_link_clean = re.sub(r'http\S+', '', doco)
    doco_clean_and = re.sub(r'&\S+', '', doco_link_clean)
    doco_clean_at = re.sub(r'@\S+', '', doco_clean_and)
    doco_clean = doco_clean_at.replace('-', ' ')
    doco_alphas = re.sub(r'\W +', ' ', doco_clean)
    trans_table = str.maketrans(punctuation, punc_replace)
    doco_clean = ' '.join([word.translate(trans_table) for word in doco_alphas.split(' ')])
    doco_clean = doco_clean.split(' ')
    p = re.compile(r'\s*\b(?=[a-z\d]*([a-z\d])\1{3}|\d+\b)[a-z\d]+', re.IGNORECASE)
    doco_clean = ([p.sub("", x).strip() for x in doco_clean])
    doco_clean = [word.lower() for word in doco_clean if len(word) > 2]
    doco_clean = ([i for i in doco_clean if i not in stop])
#     doco_clean = [spell(word) for word in doco_clean]
#     p = re.compile(r'\s*\b(?=[a-z\d]*([a-z\d])\1{3}|\d+\b)[a-z\d]+', re.IGNORECASE)
    doco_clean = ([p.sub("", x).strip() for x in doco_clean])
#     doco_clean = ([spell(k) for k in doco_clean])
    return doco_clean


# In[ ]:


# Generate a cleaned reviews array from original review texts
review_cleans = [clean_document(doc) for doc in reviews];
sentences = [' '.join(r) for r in review_cleans ]


# In[ ]:


print(sentences[7])


# In[ ]:


print(reviews[7])


# In[ ]:


reviews.shape
# sentences.shape


# In[ ]:


#Keras
tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)


# In[ ]:


text_sequences = np.array(tokenizer.texts_to_sequences(sentences))
sequence_dict = tokenizer.word_index
word_dict = dict((num, val) for (val, num) in sequence_dict.items())


# In[ ]:


print(text_sequences)


# In[ ]:


print(sequence_dict)


# In[ ]:


print(word_dict)


# In[ ]:


reviews_encoded = [];
for i,review in enumerate(review_cleans):
    reviews_encoded.append([sequence_dict[x] for x in review]);


# In[ ]:


lengths = [len(x) for x in reviews_encoded]
plt.hist(lengths, bins=range(25))


# In[ ]:


print(reviews_encoded[135])


# In[ ]:


max_cap =8;
X = pad_sequences(reviews_encoded, maxlen=max_cap, truncating='post')


# In[ ]:


Y = np.array([[0,1] if '0' in label else [1,0] for label in labels])


# In[ ]:


np.random.seed(1024);
random_posits = np.arange(len(X))
np.random.shuffle(random_posits);


# In[ ]:


X = X[random_posits];
Y = Y[random_posits];


# In[ ]:


train_cap = int(0.85 * len(X));
dev_cap = int(0.93 * len(X));


# In[ ]:


X_train, Y_train = X[:train_cap], Y[:train_cap]
X_dev, Y_dev = X[train_cap:dev_cap], Y[train_cap:dev_cap]
X_test1, Y_test1 = X[dev_cap:], Y[dev_cap:]


# In[ ]:


from keras.models import Sequential
from keras.layers import Dense
from keras.backend import eval
from keras.optimizers import Adam
from keras.layers import LSTM
from keras.layers.embeddings import Embedding


model1 = Sequential();
model1.add(Embedding(len(word_dict)+1, max_cap, input_length=max_cap));
#adding a LSTM layer of dim 1--
model1.add(LSTM(150, return_sequences=True));
model1.add(LSTM(150, return_sequences=False));
#adding a dense layer with activation function of relu
model1.add(Dense(100, activation='relu', init='uniform'));#best 50,relu
#adding the final output activation with activation function of softmax
model1.add(Dense(2, activation='sigmoid', init='uniform'));
print(model1.summary());
optimizer = Adam(lr=0.0001, decay=0.0001);

model1.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
# fit model and run it for 5 epochs
model1.fit(X_train, Y_train, batch_size=16, epochs=5, validation_data=(X_dev, Y_dev))


# In[ ]:


score = model1.evaluate(X_test1, Y_test1)
print("Test accuracy: %0.4f%%" % (score[1]*100))

