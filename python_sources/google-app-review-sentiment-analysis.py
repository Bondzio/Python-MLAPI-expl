#!/usr/bin/env python
# coding: utf-8

# ## Google app review on sentiment and translated_review classification of sentiment

# In[ ]:


# import dataset 
import pandas as pd 
import warnings 
warnings.filterwarnings('ignore')

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[ ]:


base_dataset=pd.read_csv("/kaggle/input/google-play-store-apps/googleplaystore_user_reviews.csv")
base_dataset.shape


# In[ ]:


base_dataset.head()


# In[ ]:


base_dataset['Sentiment'].unique()


# In[ ]:


base_dataset.dropna(axis=0,inplace=True)


# In[ ]:


base_dataset.shape


# In[ ]:


base_dataset['Sentiment'].unique()


# In[ ]:


x=[]
for i in base_dataset['Sentiment']:
    if i=='Positive':
        x.append(0)
    elif i=='Neutral':
        x.append(1)
    else :
        x.append(2)


# In[ ]:


base_dataset['y']=x


# In[ ]:


base_dataset.head()


# In[ ]:


base_dataset['y'].value_counts()


# In[ ]:


base_dataset=base_dataset.sample(8000)


# # Manual Pre Processing

# In[ ]:


unique_words=[]
total_words=[]
for i in base_dataset['Translated_Review'].str.split():
    for j in i:
        total_words.append(j)
        if i not in unique_words:
            unique_words.append(i)
len(unique_words),len(total_words)


# In[ ]:


x=[]  
for i in unique_words:  
    count=0  
    for j in base_dataset['Translated_Review']:  
        for k in j.split(): 
            if i==k:
                count=count+1  
    x.append([i,count])


# ## wordCloud 

# In[ ]:


import matplotlib.pyplot as plt
from wordcloud import WordCloud
plt.subplots(figsize=(12,12))
wordcloud=WordCloud(background_color="white",width=1024,height=768).generate(" ".join(total_words))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()


# ### stop words
# 
# #### --> process for stopwords removal 

# In[ ]:


from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize  
 
example_sent = "This is a sample sentence, showing off the stop words filtration."  
 
stop_words = set(stopwords.words('english'))  
 
word_tokens = word_tokenize(example_sent)  
 
filtered_sentence = [w for w in word_tokens if not w in stop_words]  
 
filtered_sentence = []  
 
for w in word_tokens:  
    if w not in stop_words:  
        filtered_sentence.append(w)  
 
print(word_tokens)  
print(filtered_sentence) 


# ### stemming - concept

# In[ ]:


# import these modules 
from nltk.stem import PorterStemmer 

   
ps = PorterStemmer() 
  
# choose some words to be stemmed 
words = ["program", "programs", "programer", "programing", "programers"] 
  
for w in words: 
    print(w, " : ", ps.stem(w))


# # Actual model

# In[ ]:


x=base_dataset['Translated_Review']
y=base_dataset['Sentiment']


# In[ ]:


y.unique()


# ### Train_test_split datadet

# In[ ]:


from sklearn.model_selection import train_test_split
# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=0.2)


# In[ ]:


print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)


# ### count vctorization

# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer  
# Fit the CountVectorizer to the training data  
vect = CountVectorizer(stop_words='english',strip_accents='ascii',max_features=1000).fit(X_train)  
len(vect.get_feature_names())


# In[ ]:


X_train.shape


# In[ ]:


# transform the documents in the training data to a document-term matrix  
X_train_vectorized = vect.transform(X_train)  
X_train_vectorized


# In[ ]:


X_train_vectorized.toarray()


# In[ ]:


x_test_transformed = vect.transform(X_test)


# ### DecisionTree

# In[ ]:


from sklearn.tree import DecisionTreeClassifier
dt=DecisionTreeClassifier()
dt.fit(X_train_vectorized,y_train)

from sklearn.metrics import confusion_matrix
print(confusion_matrix(y_test,dt.predict(x_test_transformed)))

from sklearn.metrics import accuracy_score
print("accuracy_score : ",accuracy_score(y_test,dt.predict(x_test_transformed)))


# ### RandomForest

# In[ ]:


from sklearn.ensemble import RandomForestClassifier
rf=RandomForestClassifier(random_state=121)
rf.fit(X_train_vectorized,y_train)
rf.predict(x_test_transformed)

pd.DataFrame([X_test.values,rf.predict(x_test_transformed)]).T

rf.predict(x_test_transformed)[1:20] # first 20 sentiment prediction


# ### final prediction

# In[ ]:


test=vect.transform(["the app is nice fantastic in using and fun to use"])

rf.predict(test)


# In[ ]:




