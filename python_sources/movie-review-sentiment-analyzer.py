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


df=pd.read_csv('/kaggle/input/imdb-dataset-of-50k-movie-reviews/IMDB Dataset.csv')


# In[ ]:


df.head()


# In[ ]:


# One review
df['review'][0]


# # **Text Cleaning**
# 
# 1. Sample 10,000 rows
# 2. Remove html tags
# 3. Converting every thing to lower case
# 4. Remove special characters
# 5. Removing Stop words
# 6. Stemming

# In[ ]:


#1
#df=df.sample(10000)


# In[ ]:


df.shape


# In[ ]:


df.info()
#Clearly seem that here is no missing data


# In[ ]:


df['sentiment'].replace({'positive': 1, 'negative': 0}, inplace= True)


# In[ ]:


df.head()


# In[ ]:


#2
# Using regex library to remove html tags
import re
clean=re.compile('<.*?>')
print(df.iloc[2].review)
# Test After Cleaning of one data
re.sub(clean,'',df.iloc[2].review)


# In[ ]:


#Function to clean html tags
def clean_html(text):
    clean=re.compile('<.*?>')
    return re.sub(clean,'',text)


# In[ ]:


df['review']=df['review'].apply(clean_html)


# In[ ]:


#3
#converting everything to lower
def convert_lower(text):
    return text.lower()


# In[ ]:


df['review']=df['review'].apply(convert_lower)


# In[ ]:


#4
#function to remove special characters
def remove_special(text):
    x=''
    
    for i in text:
        #checking is the character in the given string is alphanumeric or not
        if i.isalnum(): 
            x+=i
        else:
            x+=' '
    return x


# In[ ]:


df['review']=df['review'].apply(remove_special)


# In[ ]:


# 5
# Remove the stop words
# using natural language tool kit and stopwords class
import nltk 
from nltk.corpus import stopwords


# In[ ]:


stopwords.words('english')


# In[ ]:



def remove_stopwords(text):
    x=[]
    for i in text.split():
        if i not in stopwords.words('english'):
            x.append(i)
    y=x[:]
    x.clear()
    return y
            


# In[ ]:


df['review']=df['review'].apply(remove_stopwords)


# In[ ]:


df


# In[ ]:


# 6
# Perform stemming
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()


# In[ ]:


def stem_words(text):
    y=[]
    for i in text:
        y.append(ps.stem(i))
    z=y[:]
    y.clear()
    return z


# In[ ]:


stem_words(['I','Loved','Loving','it'])


# In[ ]:


df['review']=df['review'].apply(stem_words)


# In[ ]:


df


# In[ ]:


#join back
def join_back(list_input):
    return " ".join(list_input)


# In[ ]:


df['review']=df['review'].apply(join_back)


# In[ ]:


df


# In[ ]:


# Creating the input features
# Using CountVectorizer class
X=df.iloc[:,0:-1].values


# In[ ]:


X.shape


# In[ ]:


from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=500)


# In[ ]:


X=cv.fit_transform(df['review']).toarray()


# In[ ]:


X.shape


# In[ ]:


#taking the output
y=df.iloc[:,-1].values


# In[ ]:


y.shape


# In[ ]:


# Next step: Split the data in two parts
# X,y
# training set
# test set(Already know the result)


# In[ ]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)


# In[ ]:


X_train.shape


# In[ ]:


X_test.shape


# In[ ]:


y_train.shape


# In[ ]:


y_test.shape


# In[ ]:


from sklearn.naive_bayes import GaussianNB,MultinomialNB,BernoulliNB
clf1=GaussianNB()
clf2=MultinomialNB()
clf3=BernoulliNB()


# In[ ]:


clf1.fit(X_train,y_train)
clf2.fit(X_train,y_train)
clf3.fit(X_train,y_train)


# In[ ]:


y_pred1=clf1.predict(X_test)
y_pred2=clf2.predict(X_test)
y_pred3=clf3.predict(X_test)


# In[ ]:


y_pred3.shape


# In[ ]:


y_test.shape


# In[ ]:


from sklearn.metrics import accuracy_score


# In[ ]:


print('Gaussian:',accuracy_score(y_test,y_pred1)*100,'%')
print('Multinomial:',accuracy_score(y_test,y_pred2)*100,'%')
print('Bernoulli:',accuracy_score(y_test,y_pred3)*100,'%')


# In[ ]:


#Calculating accurary of GaussianNB manually
print(np.sum(y_test==y_pred1)/y_pred1.shape[0]*100)


# In[ ]:


#Visualizing the reviews
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# In[ ]:


# All positive reviews
norm_text_pos=""
for i in range(0,df.shape[0]):
    if(df.iloc[i].sentiment==1):
        norm_text_pos+=df.iloc[i].review
len(norm_text_pos)


# In[ ]:


#word cloud for positive review words
plt.figure(figsize=(10,10))
positive_text=norm_text_pos
WC=WordCloud(width=1000,height=500,max_words=500,min_font_size=5)
positive_words=WC.generate(positive_text)
plt.imshow(positive_words,interpolation='bilinear')
plt.show()


# In[ ]:


# All negative reviews
norm_text_neg=""
for i in range(0,df.shape[0]):
    if(df.iloc[i].sentiment==0):
        norm_text_neg+=df.iloc[i].review
len(norm_text_neg)


# In[ ]:


#Word cloud for negative review words
plt.figure(figsize=(10,10))
negative_text=norm_text_neg
WC=WordCloud(width=1000,height=500,max_words=500,min_font_size=5)
negative_words=WC.generate(negative_text)
plt.imshow(negative_words,interpolation='bilinear')
plt.show()


# In[ ]:





# ## Conclusion:
# 
# ### 1. We can observed that both Bernoulli naive bayes and Multinomial naive bayes model performing well compared to Gaussian naive bayes.
# 
# ### 2. We can also use other different classification algorithms to see which one predicts best.

# In[ ]:




