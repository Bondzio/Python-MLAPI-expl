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


data=pd.read_csv('../input/imdb-dataset-of-50k-movie-reviews/IMDB Dataset.csv')


# In[ ]:


data.head()


# In[ ]:


data.describe()


# In[ ]:


data['sentiment'].value_counts()


# In[ ]:


from bs4 import BeautifulSoup
import re


# In[ ]:


def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

#Removing the square brackets
def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)

#Removing the noisy text
def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    return text
#Apply function on review column
data['review']=data['review'].apply(denoise_text)


# In[ ]:


def remove_special_characters(text, remove_digits=True):
    pattern=r'[^a-zA-z0-9\s]'
    text=re.sub(pattern,'',text)
    return text
#Apply function on review column
data['review']=data['review'].apply(remove_special_characters)


# In[ ]:


from sklearn.preprocessing import LabelBinarizer


# In[ ]:


lb=LabelBinarizer()
data['sentiment']=lb.fit_transform(data['sentiment'])


# In[ ]:





# In[ ]:


train_sentiment=data.sentiment[:40000]
train_review=data.review[:40000]
test_sentiment=data.sentiment[40000:]
test_review=data.review[40000:]


# In[ ]:


from sklearn.feature_extraction.text import TfidfVectorizer


# In[ ]:


tf_vec=TfidfVectorizer(min_df=20,max_df=0.5,ngram_range=(1,2))


# In[ ]:


cv_train_review=tf_vec.fit_transform(train_review)
cv_test_review=tf_vec.transform(test_review)


# In[ ]:


#print(tf_vec.get_feature_names())


# In[ ]:


cv_train_review.shape,cv_test_review.shape


# In[ ]:


from sklearn.linear_model import LogisticRegression


# In[ ]:


lr=LogisticRegression()


# In[ ]:


model=lr.fit(cv_train_review,train_sentiment)


# In[ ]:


model.score(cv_train_review,train_sentiment)


# In[ ]:


model.score(cv_test_review,test_sentiment)


# In[ ]:


pred=model.predict(cv_test_review)


# In[ ]:


act=test_sentiment


# In[ ]:


from sklearn.metrics import classification_report,accuracy_score,confusion_matrix
import matplotlib.pyplot as plt


# In[ ]:


confusion_matrix(act,pred)


# In[ ]:


accuracy_score(act,pred)


# In[ ]:


print(classification_report(act,pred))


# In[ ]:


feature_to_coef = {
    word: coef for word, coef in zip(
        tf_vec.get_feature_names(), model.coef_[0]
    )
}
for best_positive in sorted(
    feature_to_coef.items(), 
    key=lambda x: x[1], 
    reverse=True)[:5]:
    print (best_positive)


# In[ ]:


for best_negative in sorted(
    feature_to_coef.items(), 
    key=lambda x: x[1])[:5]:
    print (best_negative)
    


# In[ ]:


pos_words=''
for best_positive in sorted(feature_to_coef.items(), key=lambda x: x[1], reverse=True)[:100]:
    pos_words=pos_words+ str(best_positive)
    


# In[ ]:


neg_words=''
for best_negative in sorted(feature_to_coef.items(), key=lambda x: x[1])[:100]:
    neg_words=neg_words+ str(best_negative)


# In[ ]:


from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator


# In[ ]:


# Create and generate a word cloud image:
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(pos_words)

# Display the generated image:
plt.figure(figsize=(20,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[ ]:


wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(neg_words)

# Display the generated image:
plt.figure(figsize=(20,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[ ]:




