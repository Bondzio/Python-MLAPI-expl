#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from textblob import TextBlob
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble

import pandas, xgboost, numpy, textblob, string
from keras.preprocessing import text, sequence
from keras import layers, models, optimizers


from warnings import filterwarnings
filterwarnings('ignore')


# In[ ]:


import pandas as pd
data=pd.read_csv("../input/fake-news-detection/data.csv")


# In[ ]:


data.head()


# In[ ]:


data["Label"].value_counts()


# In[ ]:


#checking missing values
data.isnull().sum()


# In[ ]:


data=data.fillna(' ')


# In[ ]:


data.isnull().sum()


# In[ ]:


df = pd.DataFrame()
df["text"] = data["Body"]
df["label"] = data["Label"]


# In[ ]:


df.head()


# In[ ]:


#Checking for outliers

df["length"] = df["text"].str.len()
df.head()


# In[ ]:


#checking for minumum,maximum and average length
#looks like there are outliers

min(df['length']), max(df['length']), round(sum(df['length'])/len(df['length']))


# In[ ]:


# dropping the outliers which are less than 50 word

df = df.drop(df['text'][df['length'] < 50].index, axis = 0)


# In[ ]:


min(df['length']), max(df['length']), round(sum(df['length'])/len(df['length']))


# In[ ]:


df.head()


# # Text Preprocessing

# In[ ]:


#upper-lower transform
df['text'] = df['text'].apply(lambda x: " ".join(x.lower() for x in x.split()))
#punctuations
df['text'] = df['text'].str.replace('[^\w\s]','')
#numbers
df['text'] = df['text'].str.replace('\d','')
#stopwords
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
sw = stopwords.words('english')
df['text'] = df['text'].apply(lambda x: " ".join(x for x in x.split() if x not in sw))
#deleting sparse words
sil = pd.Series(' '.join(df['text']).split()).value_counts()[-1000:]
df['text'] = df['text'].apply(lambda x: " ".join(x for x in x.split() if x not in sil))
#lemmi
from textblob import Word
#nltk.download('wordnet')
df['text'] = df['text'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()])) 


# In[ ]:


df.head()


# In[ ]:


# Word Cloud Visualization


# In[ ]:


from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt


# In[ ]:


text = " ".join(i for i in df.text)


# In[ ]:


wordcloud = WordCloud(max_font_size = 50, 
                     background_color = "white").generate(text)
plt.figure(figsize = [10,10])
plt.imshow(wordcloud, interpolation = "bilinear")
plt.axis("off")
plt.show()


# # Train-Test

# In[ ]:


train_x, test_x, train_y, test_y = model_selection.train_test_split(df["text"],
                                                                   df["label"], 
                                                                    random_state = 1)


# In[ ]:


train_y[0:5]


# In[ ]:


encoder = preprocessing.LabelEncoder()


# In[ ]:


train_y = encoder.fit_transform(train_y)
test_y = encoder.fit_transform(test_y)


# In[ ]:


train_y[0:5]


# In[ ]:


test_y[0:5]


# # TF-IDF

# In[ ]:


# ngram level tf-idf


# In[ ]:


tf_idf_ngram_vectorizer = TfidfVectorizer(ngram_range = (2,3))
tf_idf_ngram_vectorizer.fit(train_x)


# In[ ]:


x_train_tf_idf_ngram = tf_idf_ngram_vectorizer.transform(train_x)
x_test_tf_idf_ngram = tf_idf_ngram_vectorizer.transform(test_x)


# In[ ]:


loj = linear_model.LogisticRegression()
loj_model = loj.fit(x_train_tf_idf_ngram,train_y)
accuracy = model_selection.cross_val_score(loj_model, 
                                           x_test_tf_idf_ngram, 
                                           test_y, 
                                           cv = 10).mean()

print("N-GRAM TF-IDF Accuracy Rate:", accuracy)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




